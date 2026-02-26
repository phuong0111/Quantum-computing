import numpy as np
import random
from typing import Tuple, List, Optional

class RingLWE:
    """
    Ring Learning With Errors (Ring-LWE) implementation with ciphertext compression
    Based on the anti-cyclic ring Z_q[x]/(x^n + 1)
    """
    
    def __init__(self, n: int = 512, q: int = 12289, sigma: float = 1.2, p: int = 256):
        """
        Initialize Ring-LWE parameters
        
        Args:
            n: Polynomial degree (power of 2)
            q: Modulus for coefficients (prime)
            sigma: Standard deviation for Gaussian noise
            p: Compression modulus (typically 256 for byte operations)
        """
        self.n = n
        self.q = q
        self.sigma = sigma
        self.p = p  # Compression modulus
        
        # Precompute compression parameters
        self.compress_offset = 23
        self.compress_divisor = 48
        
        # Global parameter 'a' can be shared across multiple users
        self.a = self._uniform_poly()
    
    def _uniform_poly(self) -> np.ndarray:
        """Generate uniform random polynomial in Z_q^n"""
        return np.random.randint(0, self.q, self.n, dtype=np.int32)
    
    def _binary_poly(self) -> np.ndarray:
        """Generate binary polynomial with coefficients in {0,1}^n"""
        return np.random.randint(0, 2, self.n, dtype=np.int32)
    
    def _gaussian_poly(self) -> np.ndarray:
        """
        Generate polynomial with coefficients from discrete Gaussian distribution D_σ^n
        Approximated using rounded continuous Gaussian
        """
        # Generate continuous Gaussian and round to integers
        continuous = np.random.normal(0, self.sigma, self.n)
        discrete = np.round(continuous).astype(np.int32)
        
        # Ensure coefficients are in valid range [-(q-1)/2, (q-1)/2]
        discrete = np.clip(discrete, -(self.q-1)//2, (self.q-1)//2)
        
        # Convert to positive representation mod q
        return discrete % self.q
    
    def _poly_mul_anticyclic(self, a: np.ndarray, b: np.ndarray, mod: int) -> np.ndarray:
        """
        Multiply two polynomials in the anti-cyclic ring Z_mod[x]/(x^n + 1)
        Uses the relation x^n ≡ -1
        """
        result = np.zeros(self.n, dtype=np.int64)  # Use int64 to prevent overflow
        
        for i in range(self.n):
            for j in range(self.n):
                coeff_pos = (i + j) % (2 * self.n)
                if coeff_pos < self.n:
                    # Normal term
                    result[coeff_pos] += a[i] * b[j]
                else:
                    # Anti-cyclic: x^n = -1, so x^(n+k) = -x^k
                    result[coeff_pos - self.n] -= a[i] * b[j]
        
        return result % mod
    
    def _poly_add(self, a: np.ndarray, b: np.ndarray, mod: int) -> np.ndarray:
        """Add two polynomials modulo mod"""
        return (a + b) % mod
    
    def _poly_sub(self, a: np.ndarray, b: np.ndarray, mod: int) -> np.ndarray:
        """Subtract two polynomials modulo mod"""
        return (a - b) % mod
    
    def _compress_coefficient(self, x: int) -> int:
        """
        Compression function T(x) = floor((x mod q + 23) / 48) mod p
        Maps from Z_q to Z_p
        """
        return ((x % self.q) + self.compress_offset) // self.compress_divisor % self.p
    
    def _compress_poly(self, poly: np.ndarray) -> np.ndarray:
        """Compress a polynomial from Z_q to Z_p"""
        return np.array([self._compress_coefficient(coeff) for coeff in poly], dtype=np.uint8)
    
    def _center_coefficient(self, x: int, mod: int) -> int:
        """Center coefficient to range [-(mod-1)/2, (mod-1)/2]"""
        x = x % mod
        if x > mod // 2:
            x -= mod
        return x
    
    def keygen(self) -> Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Generate Ring-LWE key pair
        
        Returns:
            private_key: Binary secret polynomial s
            public_key: Tuple (a, p) where p = e_0 - a * s
        """
        # Private key: binary polynomial
        s = self._binary_poly()
        
        # Noise for key generation
        e0 = self._gaussian_poly()
        
        # Public key: p = e_0 - a * s
        a_times_s = self._poly_mul_anticyclic(self.a, s, self.q)
        p = self._poly_sub(e0, a_times_s, self.q)
        
        return s, (self.a, p)
    
    def encrypt(self, message: np.ndarray, public_key: Tuple[np.ndarray, np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Encrypt an n-bit message using Ring-LWE
        
        Args:
            message: Binary message array of length n
            public_key: Tuple (a, p)
            
        Returns:
            Ciphertext tuple (u, v)
        """
        a, p = public_key
        
        # Encode message: m = floor(q/2) * z
        m = (self.q // 2) * message
        
        # Generate fresh noise polynomials
        e1 = self._gaussian_poly()
        e2 = self._gaussian_poly()
        e3 = self._gaussian_poly()
        
        # Compute ciphertext
        # u = a * e1 + e2
        u = self._poly_add(
            self._poly_mul_anticyclic(a, e1, self.q),
            e2,
            self.q
        )
        
        # v = p * e1 + e3 + m
        v = self._poly_add(
            self._poly_add(
                self._poly_mul_anticyclic(p, e1, self.q),
                e3,
                self.q
            ),
            m,
            self.q
        )
        
        return u, v
    
    def decrypt(self, ciphertext: Tuple[np.ndarray, np.ndarray], private_key: np.ndarray) -> np.ndarray:
        """
        Decrypt ciphertext using Ring-LWE
        
        Args:
            ciphertext: Tuple (u, v)
            private_key: Binary secret polynomial s
            
        Returns:
            Recovered message bits
        """
        u, v = ciphertext
        s = private_key
        
        # m' = u * s + v
        u_times_s = self._poly_mul_anticyclic(u, s, self.q)
        m_prime = self._poly_add(u_times_s, v, self.q)
        
        # Decode message bits
        message = np.zeros(self.n, dtype=np.int32)
        for i in range(self.n):
            # Center coefficient
            centered = self._center_coefficient(m_prime[i], self.q)
            
            # Decision rule: |m'_i| > q/4 implies z_i = 1
            if abs(centered) > self.q // 4:
                message[i] = 1
            else:
                message[i] = 0
        
        return message
    
    def compress_ciphertext(self, ciphertext: Tuple[np.ndarray, np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compress ciphertext from Z_q to Z_p for efficient storage/computation
        
        Args:
            ciphertext: Original ciphertext (u, v) in Z_q
            
        Returns:
            Compressed ciphertext (u_comp, v_comp) in Z_p
        """
        u, v = ciphertext
        u_compressed = self._compress_poly(u)
        v_compressed = self._compress_poly(v)
        return u_compressed, v_compressed
    
    def decrypt_compressed(self, ciphertext_compressed: Tuple[np.ndarray, np.ndarray], 
                          private_key: np.ndarray) -> np.ndarray:
        """
        Decrypt compressed ciphertext directly in Z_p
        
        Args:
            ciphertext_compressed: Compressed ciphertext (u_comp, v_comp) in Z_p
            private_key: Binary secret polynomial s
            
        Returns:
            Recovered message bits
        """
        u_comp, v_comp = ciphertext_compressed
        s = private_key
        
        # m = u_comp * s + v_comp (in Z_p)
        u_times_s = self._poly_mul_anticyclic(u_comp, s, self.p)
        m = self._poly_add(u_times_s, v_comp, self.p)
        
        # Decode message bits (adapted for compressed domain)
        message = np.zeros(self.n, dtype=np.int32)
        threshold = self.p // 4  # Adjusted threshold for Z_p
        
        for i in range(self.n):
            # Center coefficient in Z_p
            centered = self._center_coefficient(m[i], self.p)
            
            # Decision rule adapted for compressed domain
            if abs(centered) > threshold:
                message[i] = 1
            else:
                message[i] = 0
        
        return message
    
    def test_scheme(self, message: Optional[np.ndarray] = None, message_length: int = None) -> dict:
        """
        Test the Ring-LWE scheme with and without compression
        
        Args:
            message: Specific message to encrypt (optional)
            message_length: Length of random test message if message not provided
            
        Returns:
            Dictionary with test results and statistics
        """
        if message is not None:
            # Use provided message
            original_message = message
            message_length = len(message)
        else:
            # Generate random binary message
            if message_length is None:
                message_length = self.n
            original_message = np.random.randint(0, 2, message_length, dtype=np.int32)
        
        # Pad message to n bits if necessary
        if message_length < self.n:
            padded_message = np.zeros(self.n, dtype=np.int32)
            padded_message[:message_length] = original_message
            full_message = padded_message
        else:
            full_message = original_message[:self.n]
        
        # Key generation
        private_key, public_key = self.keygen()
        
        # Encryption
        ciphertext = self.encrypt(full_message, public_key)
        
        # Regular decryption
        decrypted_message = self.decrypt(ciphertext, private_key)
        
        # Compression
        ciphertext_compressed = self.compress_ciphertext(ciphertext)
        
        # Compressed decryption
        decrypted_compressed = self.decrypt_compressed(ciphertext_compressed, private_key)
        
        # Calculate statistics
        regular_errors = np.sum(full_message != decrypted_message)
        compressed_errors = np.sum(full_message != decrypted_compressed)
        
        # Compression ratio
        original_bits = ciphertext[0].nbytes + ciphertext[1].nbytes
        compressed_bits = ciphertext_compressed[0].nbytes + ciphertext_compressed[1].nbytes
        compression_ratio = compressed_bits / original_bits
        
        return {
            'parameters': {
                'n': self.n,
                'q': self.q,
                'p': self.p,
                'sigma': self.sigma
            },
            'original_message': original_message,
            'regular_decryption': decrypted_message[:message_length],
            'compressed_decryption': decrypted_compressed[:message_length],
            'regular_error_count': regular_errors,
            'compressed_error_count': compressed_errors,
            'regular_error_rate': regular_errors / self.n,
            'compressed_error_rate': compressed_errors / self.n,
            'compression_ratio': compression_ratio,
            'storage_savings': 1 - compression_ratio,
            'ciphertext_original_size': original_bits,
            'ciphertext_compressed_size': compressed_bits
        }


def demo_ringlwe():
    """Demonstration of Ring-LWE with compression"""
    
    print("=== Ring-LWE Implementation Demo ===\n")
    
    # Initialize with smaller parameters for demo
    ring_lwe = RingLWE(n=256, q=12289, sigma=1.2, p=256)
    
    # Test with a short message
    test_message = "Hello, Ring-LWE!"
    
    # Convert string to binary
    binary_message = []
    for char in test_message:
        binary_message.extend([int(b) for b in format(ord(char), '08b')])
    
    binary_message = np.array(binary_message, dtype=np.int32)
    
    print(f"Original message: '{test_message}'")
    print(f"Binary representation ({len(binary_message)} bits): {binary_message[:32]}...")
    
    # Run test with the specific message
    results = ring_lwe.test_scheme(message=binary_message)
    
    print(f"\n=== Parameters ===")
    print(f"n = {results['parameters']['n']}")
    print(f"q = {results['parameters']['q']}")
    print(f"p = {results['parameters']['p']} (compression)")
    print(f"sigma = {results['parameters']['sigma']}")
    
    print(f"\n=== Results ===")
    print(f"Regular decryption errors: {results['regular_error_count']}/{results['parameters']['n']}")
    print(f"Regular error rate: {results['regular_error_rate']:.6f}")
    print(f"Compressed decryption errors: {results['compressed_error_count']}/{results['parameters']['n']}")
    print(f"Compressed error rate: {results['compressed_error_rate']:.6f}")
    
    print(f"\n=== Compression Benefits ===")
    print(f"Original ciphertext size: {results['ciphertext_original_size']} bytes")
    print(f"Compressed ciphertext size: {results['ciphertext_compressed_size']} bytes")
    print(f"Compression ratio: {results['compression_ratio']:.3f}")
    print(f"Storage savings: {results['storage_savings']:.1%}")
    
    # Verify that we're using the right message
    print(f"\n=== Message Verification ===")
    print(f"Input binary:     {binary_message}")
    print(f"Encrypted binary: {results['original_message']}")
    print(f"Messages match:   {'✓ YES' if np.array_equal(binary_message, results['original_message']) else '✗ NO'}")
    
    # Decode binary back to string for verification
    if results['regular_error_count'] == 0:
        decoded_chars = []
        recovered_binary = results['regular_decryption']
        for i in range(0, len(recovered_binary), 8):
            byte_bits = recovered_binary[i:i+8]
            if len(byte_bits) == 8:
                char_code = sum(bit * (2 ** (7-j)) for j, bit in enumerate(byte_bits))
                if 32 <= char_code <= 126:  # Printable ASCII
                    decoded_chars.append(chr(char_code))
        
        decoded_message = ''.join(decoded_chars)
        print(f"\nDecoded message (regular): '{decoded_message}'")
        print(f"Regular recovery: {'✓ Success' if decoded_message == test_message else '✗ Failed'}")
    
    # Also test compressed decryption
    if results['compressed_error_count'] == 0:
        decoded_chars_comp = []
        recovered_binary_comp = results['compressed_decryption']
        for i in range(0, len(recovered_binary_comp), 8):
            byte_bits = recovered_binary_comp[i:i+8]
            if len(byte_bits) == 8:
                char_code = sum(bit * (2 ** (7-j)) for j, bit in enumerate(byte_bits))
                if 32 <= char_code <= 126:  # Printable ASCII
                    decoded_chars_comp.append(chr(char_code))
        
        decoded_message_comp = ''.join(decoded_chars_comp)
        print(f"Decoded message (compressed): '{decoded_message_comp}'")
        print(f"Compressed recovery: {'✓ Success' if decoded_message_comp == test_message else '✗ Failed'}")


if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Run demonstration
    demo_ringlwe()
    
    print("\n" + "="*60)
    print("Additional tests with different parameters:")
    
    # Test with standard parameters
    standard_lwe = RingLWE(n=512, q=12289, sigma=1.2, p=256)
    results = standard_lwe.test_scheme(message_length=128)  # Test with 128-bit random message
    
    print(f"\nStandard parameters (n=512) with random 128-bit message:")
    print(f"Error rates - Regular: {results['regular_error_rate']:.6f}, Compressed: {results['compressed_error_rate']:.6f}")
    print(f"Storage savings: {results['storage_savings']:.1%}")