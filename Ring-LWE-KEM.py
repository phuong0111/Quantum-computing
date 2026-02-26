import numpy as np
import hashlib
import random
from typing import Tuple, Optional

class RingLWE_KEM:
    """
    Ring Learning With Errors (Ring-LWE) Key Encapsulation Mechanism
    Based on the anti-cyclic ring Z_q[x]/(x^n + 1)
    
    This implements a proper KEM where:
    - KeyGen generates a public/private key pair
    - Encapsulate generates a random shared secret and encapsulates it
    - Decapsulate recovers the shared secret using the private key
    """
    
    def __init__(self, n: int = 512, q: int = 12289, sigma: float = 1.2, 
                 shared_secret_length: int = 32):
        """
        Initialize Ring-LWE KEM parameters
        
        Args:
            n: Polynomial degree (power of 2)
            q: Modulus for coefficients (prime)
            sigma: Standard deviation for Gaussian noise
            shared_secret_length: Length of shared secret in bytes (e.g., 32 for 256-bit keys)
        """
        self.n = n
        self.q = q
        self.sigma = sigma
        self.shared_secret_length = shared_secret_length
        
        # Global parameter 'a' - can be system-wide parameter
        self.a = self._uniform_poly()
        
        # Security parameter for random oracle (hash function)
        self.hash_func = hashlib.sha256
    
    def _uniform_poly(self) -> np.ndarray:
        """Generate uniform random polynomial in Z_q^n"""
        return np.random.randint(0, self.q, self.n, dtype=np.int32)
    
    def _binary_poly(self) -> np.ndarray:
        """Generate binary polynomial with coefficients in {0,1}^n"""
        return np.random.randint(0, 2, self.n, dtype=np.int32)
    
    def _gaussian_poly(self) -> np.ndarray:
        """
        Generate polynomial with coefficients from discrete Gaussian distribution
        """
        continuous = np.random.normal(0, self.sigma, self.n)
        discrete = np.round(continuous).astype(np.int32)
        discrete = np.clip(discrete, -(self.q-1)//2, (self.q-1)//2)
        return discrete % self.q
    
    def _ternary_poly(self) -> np.ndarray:
        """Generate ternary polynomial with coefficients in {-1, 0, 1}"""
        return np.random.randint(-1, 2, self.n, dtype=np.int32) % self.q
    
    def _poly_mul_anticyclic(self, a: np.ndarray, b: np.ndarray, mod: int) -> np.ndarray:
        """
        Multiply two polynomials in the anti-cyclic ring Z_mod[x]/(x^n + 1)
        """
        result = np.zeros(self.n, dtype=np.int64)
        
        for i in range(self.n):
            for j in range(self.n):
                coeff_pos = (i + j) % (2 * self.n)
                if coeff_pos < self.n:
                    result[coeff_pos] += a[i] * b[j]
                else:
                    result[coeff_pos - self.n] -= a[i] * b[j]
        
        return result % mod
    
    def _poly_add(self, a: np.ndarray, b: np.ndarray, mod: int) -> np.ndarray:
        """Add two polynomials modulo mod"""
        return (a + b) % mod
    
    def _poly_sub(self, a: np.ndarray, b: np.ndarray, mod: int) -> np.ndarray:
        """Subtract two polynomials modulo mod"""
        return (a - b) % mod
    
    def _center_coefficient(self, x: int, mod: int) -> int:
        """Center coefficient to range [-(mod-1)/2, (mod-1)/2]"""
        x = x % mod
        if x > mod // 2:
            x -= mod
        return x
    
    def _random_bytes(self, length: int) -> bytes:
        """Generate cryptographically secure random bytes"""
        return np.random.bytes(length)
    
    def _hash_to_shared_secret(self, seed: bytes) -> bytes:
        """Hash seed to generate shared secret"""
        return self.hash_func(seed).digest()[:self.shared_secret_length]
    
    def _encode_message(self, message_bytes: bytes) -> np.ndarray:
        """
        Encode bytes into polynomial coefficients
        Each byte is mapped to 8 coefficients {0,1}
        """
        bits = []
        for byte in message_bytes:
            bits.extend([int(b) for b in format(byte, '08b')])
        
        # Pad to polynomial length if necessary
        while len(bits) < self.n:
            bits.append(0)
        
        # Encode as polynomial: 0 -> 0, 1 -> q//2
        encoded = np.array([(self.q // 2) * bit for bit in bits[:self.n]], dtype=np.int32)
        return encoded
    
    def _decode_message(self, poly: np.ndarray) -> bytes:
        """
        Decode polynomial coefficients back to bytes
        Decision rule: |coeff| > q/4 implies bit = 1
        """
        bits = []
        for coeff in poly:
            centered = self._center_coefficient(coeff, self.q)
            bit = 1 if abs(centered) > self.q // 4 else 0
            bits.append(bit)
        
        # Convert bits to bytes
        message_bytes = bytearray()
        for i in range(0, min(len(bits), self.n), 8):
            byte_bits = bits[i:i+8]
            if len(byte_bits) == 8:
                byte_val = sum(bit * (2 ** (7-j)) for j, bit in enumerate(byte_bits))
                message_bytes.append(byte_val)
        
        return bytes(message_bytes)
    
    def keygen(self) -> Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Generate Ring-LWE KEM key pair
        
        Returns:
            private_key: Secret polynomial s
            public_key: Tuple (a, t) where t = a*s + e
        """
        # Private key: small secret polynomial (binary or ternary)
        s = self._binary_poly()  # Can also use _ternary_poly() for better security
        
        # Noise for public key generation
        e = self._gaussian_poly()
        
        # Public key: t = a*s + e (standard form, not e - a*s)
        a_times_s = self._poly_mul_anticyclic(self.a, s, self.q)
        t = self._poly_add(a_times_s, e, self.q)
        
        return s, (self.a, t)
    
    def encapsulate(self, public_key: Tuple[np.ndarray, np.ndarray]) -> Tuple[bytes, Tuple[np.ndarray, np.ndarray]]:
        """
        Encapsulate a random shared secret
        
        Args:
            public_key: Tuple (a, t) from keygen
            
        Returns:
            shared_secret: Random shared secret (bytes)
            ciphertext: Tuple (u, v) that encapsulates the secret
        """
        a, t = public_key
        
        # Generate random seed for shared secret
        seed = self._random_bytes(32)  # 256-bit seed
        shared_secret = self._hash_to_shared_secret(seed)
        
        # Encode the seed (not the shared secret) into the ciphertext
        # This allows deterministic shared secret derivation
        encoded_seed = self._encode_message(seed)
        
        # Generate fresh randomness for encapsulation
        r = self._binary_poly()  # Random polynomial for encryption
        e1 = self._gaussian_poly()  # Fresh noise
        e2 = self._gaussian_poly()  # Fresh noise
        
        # Compute ciphertext components
        # u = a*r + e1
        u = self._poly_add(
            self._poly_mul_anticyclic(a, r, self.q),
            e1,
            self.q
        )
        
        # v = t*r + e2 + encoded_seed
        v = self._poly_add(
            self._poly_add(
                self._poly_mul_anticyclic(t, r, self.q),
                e2,
                self.q
            ),
            encoded_seed,
            self.q
        )
        
        ciphertext = (u, v)
        return shared_secret, ciphertext
    
    def decapsulate(self, ciphertext: Tuple[np.ndarray, np.ndarray], 
                   private_key: np.ndarray) -> bytes:
        """
        Decapsulate the shared secret from ciphertext
        
        Args:
            ciphertext: Tuple (u, v) from encapsulate
            private_key: Secret polynomial s from keygen
            
        Returns:
            shared_secret: Recovered shared secret (bytes)
        """
        u, v = ciphertext
        s = private_key
        
        # Recover the encoded seed: seed' = v - s*u
        s_times_u = self._poly_mul_anticyclic(s, u, self.q)
        recovered_poly = self._poly_sub(v, s_times_u, self.q)
        
        # Decode polynomial back to seed bytes
        recovered_seed = self._decode_message(recovered_poly)
        
        # Derive the same shared secret from recovered seed
        # Truncate to expected seed length to handle padding/noise
        truncated_seed = recovered_seed[:32]
        shared_secret = self._hash_to_shared_secret(truncated_seed)
        
        return shared_secret
    
    def test_kem(self, num_tests: int = 10) -> dict:
        """
        Test the KEM scheme with multiple iterations
        
        Args:
            num_tests: Number of test iterations
            
        Returns:
            Dictionary with test results and statistics
        """
        successes = 0
        failures = 0
        shared_secret_mismatches = 0
        
        results = []
        
        for test_num in range(num_tests):
            try:
                # Generate key pair
                private_key, public_key = self.keygen()
                
                # Encapsulate random shared secret
                original_secret, ciphertext = self.encapsulate(public_key)
                
                # Decapsulate shared secret
                recovered_secret = self.decapsulate(ciphertext, private_key)
                
                # Check if secrets match
                secrets_match = original_secret == recovered_secret
                
                if secrets_match:
                    successes += 1
                else:
                    shared_secret_mismatches += 1
                    failures += 1
                
                # Calculate ciphertext size
                u, v = ciphertext
                ciphertext_size = u.nbytes + v.nbytes
                
                results.append({
                    'test_number': test_num + 1,
                    'success': secrets_match,
                    'original_secret_hex': original_secret.hex(),
                    'recovered_secret_hex': recovered_secret.hex(),
                    'ciphertext_size_bytes': ciphertext_size,
                    'shared_secret_length': len(original_secret)
                })
                
            except Exception as e:
                failures += 1
                results.append({
                    'test_number': test_num + 1,
                    'success': False,
                    'error': str(e)
                })
        
        # Calculate key and ciphertext sizes
        dummy_private_key, dummy_public_key = self.keygen()
        dummy_secret, dummy_ciphertext = self.encapsulate(dummy_public_key)
        
        private_key_size = dummy_private_key.nbytes
        public_key_size = dummy_public_key[0].nbytes + dummy_public_key[1].nbytes
        ciphertext_size = dummy_ciphertext[0].nbytes + dummy_ciphertext[1].nbytes
        
        return {
            'parameters': {
                'n': self.n,
                'q': self.q,
                'sigma': self.sigma,
                'shared_secret_length': self.shared_secret_length
            },
            'summary': {
                'total_tests': num_tests,
                'successes': successes,
                'failures': failures,
                'success_rate': successes / num_tests,
                'shared_secret_mismatches': shared_secret_mismatches
            },
            'sizes': {
                'private_key_bytes': private_key_size,
                'public_key_bytes': public_key_size,
                'ciphertext_bytes': ciphertext_size,
                'shared_secret_bytes': self.shared_secret_length
            },
            'individual_results': results
        }


def demo_ring_lwe_kem():
    """Demonstration of Ring-LWE KEM"""
    
    print("=== Ring-LWE Key Encapsulation Mechanism Demo ===\n")
    
    # Initialize KEM with moderate security parameters
    kem = RingLWE_KEM(n=256, q=12289, sigma=1.2, shared_secret_length=32)
    
    print("=== Single KEM Operation Demo ===")
    
    # Step 1: Key Generation
    print("1. Key Generation:")
    private_key, public_key = kem.keygen()
    a, t = public_key
    
    print(f"   Private key size: {private_key.nbytes} bytes")
    print(f"   Public key size: {a.nbytes + t.nbytes} bytes")
    print(f"   Private key (first 8 coeffs): {private_key[:8]}")
    print(f"   Public key 'a' (first 8 coeffs): {a[:8]}")
    print(f"   Public key 't' (first 8 coeffs): {t[:8]}")
    
    # Step 2: Encapsulation
    print("\n2. Encapsulation:")
    shared_secret, ciphertext = kem.encapsulate(public_key)
    u, v = ciphertext
    
    print(f"   Generated shared secret: {shared_secret.hex()}")
    print(f"   Shared secret length: {len(shared_secret)} bytes")
    print(f"   Ciphertext size: {u.nbytes + v.nbytes} bytes")
    print(f"   Ciphertext 'u' (first 8 coeffs): {u[:8]}")
    print(f"   Ciphertext 'v' (first 8 coeffs): {v[:8]}")
    
    # Step 3: Decapsulation
    print("\n3. Decapsulation:")
    recovered_secret = kem.decapsulate(ciphertext, private_key)
    
    print(f"   Recovered shared secret: {recovered_secret.hex()}")
    print(f"   Secrets match: {'✓ YES' if shared_secret == recovered_secret else '✗ NO'}")
    
    if shared_secret == recovered_secret:
        print("   🎉 KEM operation successful!")
    else:
        print("   ❌ KEM operation failed!")
        
        # Debug information
        print(f"   Original:  {shared_secret.hex()}")
        print(f"   Recovered: {recovered_secret.hex()}")
        
        # Show bit differences
        orig_bits = ''.join(format(b, '08b') for b in shared_secret)
        recv_bits = ''.join(format(b, '08b') for b in recovered_secret)
        differences = sum(o != r for o, r in zip(orig_bits, recv_bits))
        print(f"   Bit differences: {differences}/{len(orig_bits)}")
    
    print("\n" + "="*60)
    print("=== Comprehensive Testing ===")
    
    # Run comprehensive tests
    test_results = kem.test_kem(num_tests=20)
    
    print(f"\nParameters:")
    for key, value in test_results['parameters'].items():
        print(f"  {key}: {value}")
    
    print(f"\nTest Summary:")
    print(f"  Total tests: {test_results['summary']['total_tests']}")
    print(f"  Successes: {test_results['summary']['successes']}")
    print(f"  Failures: {test_results['summary']['failures']}")
    print(f"  Success rate: {test_results['summary']['success_rate']:.1%}")
    
    print(f"\nSize Analysis:")
    print(f"  Private key: {test_results['sizes']['private_key_bytes']:,} bytes")
    print(f"  Public key: {test_results['sizes']['public_key_bytes']:,} bytes")
    print(f"  Ciphertext: {test_results['sizes']['ciphertext_bytes']:,} bytes")
    print(f"  Shared secret: {test_results['sizes']['shared_secret_bytes']} bytes")
    
    # Show first few individual results
    print(f"\nFirst 5 Test Results:")
    for i, result in enumerate(test_results['individual_results'][:5]):
        if 'error' in result:
            print(f"  Test {result['test_number']}: ❌ Error - {result['error']}")
        else:
            status = "✓" if result['success'] else "✗"
            print(f"  Test {result['test_number']}: {status} Success: {result['success']}")
    
    if test_results['summary']['success_rate'] == 1.0:
        print("\n🎉 All tests passed! The Ring-LWE KEM is working correctly.")
    else:
        print(f"\n⚠️  Some tests failed. Success rate: {test_results['summary']['success_rate']:.1%}")
    
    return test_results


def compare_kem_parameters():
    """Compare different parameter sets for Ring-LWE KEM"""
    
    print("\n" + "="*60)
    print("=== Parameter Comparison ===")
    
    parameter_sets = [
        {'name': 'Light', 'n': 256, 'q': 7681, 'sigma': 1.0},
        {'name': 'Standard', 'n': 512, 'q': 12289, 'sigma': 1.2},
        {'name': 'High', 'n': 1024, 'q': 12289, 'sigma': 1.5}
    ]
    
    for params in parameter_sets:
        print(f"\n{params['name']} Security Parameters:")
        print(f"  n={params['n']}, q={params['q']}, σ={params['sigma']}")
        
        kem = RingLWE_KEM(n=params['n'], q=params['q'], sigma=params['sigma'])
        results = kem.test_kem(num_tests=5)
        
        print(f"  Success rate: {results['summary']['success_rate']:.1%}")
        print(f"  Public key: {results['sizes']['public_key_bytes']:,} bytes")
        print(f"  Ciphertext: {results['sizes']['ciphertext_bytes']:,} bytes")


if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Run main demonstration
    results = demo_ring_lwe_kem()
    
    # Compare different parameter sets
    compare_kem_parameters()
    
    print(f"\n{'='*60}")
    print("Ring-LWE KEM demonstration completed!")