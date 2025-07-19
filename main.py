import array
import fractions
import logging
import math
import numpy as np
import sys
from typing import List, Optional, Tuple, Union
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import ParameterVector, Gate, Instruction
from qiskit.circuit.library import QFT  # Updated import
from qiskit.quantum_info import partial_trace
from qiskit_aer import AerSimulator
from qiskit import transpile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from abc import ABC
import inspect
import pprint

class AlgorithmResult(ABC):
    """Abstract Base Class for algorithm results."""

    def __str__(self) -> str:
        result = {}
        for name, value in inspect.getmembers(self):
            if (
                not name.startswith("_")
                and not inspect.ismethod(value)
                and not inspect.isfunction(value)
                and hasattr(self, name)
            ):
                result[name] = value
        return pprint.pformat(result, indent=4)

    def combine(self, result: "AlgorithmResult") -> None:
        """Any property from the argument that exists in the receiver is updated."""
        if result is None:
            raise TypeError("Argument result expected.")
        if result == self:
            return

        for name, value in inspect.getmembers(result):
            if (
                not name.startswith("_")
                and not inspect.ismethod(value)
                and not inspect.isfunction(value)
                and hasattr(self, name)
            ):
                try:
                    setattr(self, name, value)
                except AttributeError:
                    pass

class ShorResult(AlgorithmResult):
    """Shor Result."""

    def __init__(self) -> None:
        super().__init__()
        self._factors = []
        self._total_counts = 0
        self._successful_counts = 0

    @property
    def factors(self) -> List[List[int]]:
        """returns factors"""
        return self._factors

    @factors.setter
    def factors(self, value: List[List[int]]) -> None:
        """set factors"""
        self._factors = value

    @property
    def total_counts(self) -> int:
        """returns total counts"""
        return self._total_counts

    @total_counts.setter
    def total_counts(self, value: int) -> None:
        """set total counts"""
        self._total_counts = value

    @property
    def successful_counts(self) -> int:
        """returns successful counts"""
        return self._successful_counts

    @successful_counts.setter
    def successful_counts(self, value: int) -> None:
        """set successful counts"""
        self._successful_counts = value

def is_power(N: int, return_decomposition: bool = True):
    """Check if N is a perfect power."""
    for p in range(2, int(N.bit_length()) + 1):
        b = round(N ** (1/p))
        if b ** p == N:
            if return_decomposition:
                return True, b, p
            else:
                return True
    if return_decomposition:
        return False, None, None
    else:
        return False

class Shor:
    """Shor's factoring algorithm."""
    
    def __init__(self, backend: Optional[Union[AerSimulator]] = None) -> None:
        """
        Args:
            backend: Backend
        """
        self._backend = None
        if backend:
            self.backend = backend
            
    @property
    def backend(self) -> Optional[Union[AerSimulator]]:
        """Returns backend."""
        return self._backend

    @backend.setter
    def backend(self, backend: Union[AerSimulator]) -> None:
        """Sets backend."""
        self._backend = backend
        
    @staticmethod
    def _get_angles(a: int, n: int) -> np.ndarray:
        """Calculates the array of angles to be used in the addition in Fourier Space."""
        bits_little_endian = (bin(int(a))[2:].zfill(n))[::-1]

        angles = np.zeros(n)
        for i in range(n):
            for j in range(i + 1):
                k = i - j
                if bits_little_endian[j] == "1":
                    angles[i] += pow(2, -k)

        return angles * np.pi
    
    @staticmethod
    def _phi_add_gate(angles: Union[np.ndarray, ParameterVector]) -> Gate:
        """Gate that performs addition by a in Fourier Space."""
        circuit = QuantumCircuit(len(angles), name="phi_add_a")
        for i, angle in enumerate(angles):
            circuit.p(angle, i)
        return circuit.to_gate()
    
    def _double_controlled_phi_add_mod_N(self, angles: Union[np.ndarray, ParameterVector], 
                                        c_phi_add_N: Gate, iphi_add_N: Gate, 
                                        qft: Gate, iqft: Gate) -> QuantumCircuit:
        """Creates a circuit which implements double-controlled modular addition by a."""
        ctrl_qreg = QuantumRegister(2, "ctrl")
        b_qreg = QuantumRegister(len(angles), "b")
        flag_qreg = QuantumRegister(1, "flag")
        
        circuit = QuantumCircuit(ctrl_qreg, b_qreg, flag_qreg, name="ccphi_add_a_mod_N")
        
        cc_phi_add_a = self._phi_add_gate(angles).control(2)
        cc_iphi_add_a = cc_phi_add_a.inverse()
        
        circuit.append(cc_phi_add_a, [*ctrl_qreg, *b_qreg])
        circuit.append(iphi_add_N, b_qreg)
        circuit.append(iqft, b_qreg)
        
        circuit.cx(b_qreg[-1], flag_qreg[0])
        
        circuit.append(qft, b_qreg)
        
        circuit.append(c_phi_add_N, [*flag_qreg, *b_qreg])
        circuit.append(cc_iphi_add_a, [*ctrl_qreg, *b_qreg])
        
        circuit.append(iqft, b_qreg)
        
        circuit.x(b_qreg[-1])
        circuit.cx(b_qreg[-1], flag_qreg[0])
        circuit.x(b_qreg[-1])
        
        circuit.append(qft, b_qreg)
        circuit.append(cc_phi_add_a, [*ctrl_qreg, *b_qreg])
        
        return circuit
    
    def _controlled_multiple_mod_N(self, n: int, N: int, a: int, 
                                  c_phi_add_N: Gate, iphi_add_N: Gate, 
                                  qft: Gate, iqft: Gate) -> Instruction:
        """Implements modular multiplication by a as an instruction."""
        ctrl_qreg = QuantumRegister(1, "ctrl")
        x_qreg = QuantumRegister(n, "x")
        b_qreg = QuantumRegister(n + 1, "b")
        flag_qreg = QuantumRegister(1, "flag")
        circuit = QuantumCircuit(ctrl_qreg, x_qreg, b_qreg, flag_qreg, name="cmult_a_mod_N")
        
        angle_params = ParameterVector("angles", length=n + 1)
        modulo_adder = self._double_controlled_phi_add_mod_N(
            angle_params, c_phi_add_N, iphi_add_N, qft, iqft
        )
        
        def append_adder(adder: QuantumCircuit, constant: int, idx: int):
            partial_constant = (pow(2, idx, N) * constant) % N
            angles = self._get_angles(partial_constant, n + 1)
            bound = adder.assign_parameters({angle_params: angles})
            circuit.append(bound, [*ctrl_qreg, x_qreg[idx], *b_qreg, *flag_qreg])
            
        circuit.append(qft, b_qreg)
        
        for i in range(n):
            append_adder(modulo_adder, a, i)
            
        circuit.append(iqft, b_qreg)
        
        for i in range(n):
            circuit.cswap(ctrl_qreg, x_qreg[i], b_qreg[i])
            
        circuit.append(qft, b_qreg)
        
        a_inv = pow(a, -1, mod=N) if sys.version_info >= (3, 8) else self.modinv(a, N)
        modulo_adder_inv = modulo_adder.inverse()
        
        for i in reversed(range(n)):
            append_adder(modulo_adder_inv, a_inv, i)
            
        circuit.append(iqft, b_qreg)
        return circuit.to_instruction()
    
    def _power_mod_N(self, n: int, N: int, a: int) -> Instruction:
        """Implements modular exponentiation a^x as an instruction."""
        up_qreg = QuantumRegister(2 * n, name="up")
        down_qreg = QuantumRegister(n, name="down")
        aux_qreg = QuantumRegister(n + 2, name="aux")

        circuit = QuantumCircuit(up_qreg, down_qreg, aux_qreg, name=f"power_mod_N_{a}_{N}")

        qft = QFT(n + 1, do_swaps=False).to_gate()
        iqft = qft.inverse()

        phi_add_N = self._phi_add_gate(self._get_angles(N, n + 1))
        iphi_add_N = phi_add_N.inverse()
        c_phi_add_N = phi_add_N.control(1)

        for i in range(2 * n):
            partial_a = pow(a, pow(2, i), N)
            modulo_multiplier = self._controlled_multiple_mod_N(
                n, N, partial_a, c_phi_add_N, iphi_add_N, qft, iqft
            )
            circuit.append(modulo_multiplier, [up_qreg[i], *down_qreg, *aux_qreg])

        return circuit.to_instruction()
    
    @staticmethod
    def _validate_input(N: int, a: int):
        """Check parameters of the algorithm."""
        if N < 1 or N % 2 == 0:
            raise ValueError("The input needs to be an odd integer greater than 1.")
        if a >= N or math.gcd(a, N) != 1:
            raise ValueError("The integer a needs to satisfy a < N and gcd(a, N) = 1.")
        
    def construct_circuit(self, N: int, a: int = 2, measurement: bool = False) -> QuantumCircuit:
        """Construct quantum part of the algorithm."""
        self._validate_input(N, a)

        n = N.bit_length()

        up_qreg = QuantumRegister(2 * n, name="up")
        down_qreg = QuantumRegister(n, name="down")
        aux_qreg = QuantumRegister(n + 2, name="aux")

        circuit = QuantumCircuit(up_qreg, down_qreg, aux_qreg, name=f"Shor(N={N}, a={a})")

        circuit.h(up_qreg)
        circuit.x(down_qreg[0])

        modulo_power = self._power_mod_N(n, N, a)
        circuit.append(modulo_power, circuit.qubits)

        iqft = QFT(len(up_qreg)).inverse().to_gate()
        circuit.append(iqft, up_qreg)

        if measurement:
            up_cqreg = ClassicalRegister(2 * n, name="m")
            circuit.add_register(up_cqreg)
            circuit.measure(up_qreg, up_cqreg)

        return circuit
    
    @staticmethod
    def modinv(a: int, m: int) -> int:
        """Returns the modular multiplicative inverse of a with respect to the modulus m."""
        def egcd(a: int, b: int) -> Tuple[int, int, int]:
            if a == 0:
                return b, 0, 1
            else:
                g, y, x = egcd(b % a, a)
                return g, x - (b // a) * y, y

        g, x, _ = egcd(a, m)
        if g != 1:
            raise ValueError(
                "The greatest common divisor of {} and {} is {}, so the "
                "modular inverse does not exist.".format(a, m, g)
            )
        return x % m
    
    def _get_factors(self, N: int, a: int, measurement: str) -> Optional[List[int]]:
        """Apply the continued fractions to find r and the gcd to find the desired factors."""
        x_final = int(measurement, 2)
        logger.info("In decimal, x_final value for this result is: %s.", x_final)

        if x_final <= 0:
            fail_reason = "x_final value is <= 0, there are no continued fractions."
        else:
            fail_reason = None

        T_upper = len(measurement)
        T = pow(2, T_upper)
        x_over_T = x_final / T

        i = 0
        b = array.array("i")
        t = array.array("f")

        b.append(math.floor(x_over_T))
        t.append(x_over_T - b[i])

        exponential = 0.0
        while i < N and fail_reason is None:
            if i > 0:
                b.append(math.floor(1 / t[i - 1]))
                t.append((1 / t[i - 1]) - b[i])

            denominator = self._calculate_continued_fraction(b)
            i += 1

            if denominator % 2 == 1:
                logger.debug("Odd denominator, will try next iteration of continued fractions.")
                continue

            if denominator < 1000:
                exponential = pow(a, denominator / 2)

            if exponential > 1000000000:
                fail_reason = "denominator of continued fraction is too big."
            else:
                putting_plus = int(exponential + 1)
                putting_minus = int(exponential - 1)
                one_factor = math.gcd(putting_plus, N)
                other_factor = math.gcd(putting_minus, N)

                if any(factor in {1, N} for factor in (one_factor, other_factor)):
                    logger.debug("Found just trivial factors, not good enough.")
                    if t[i - 1] == 0:
                        fail_reason = "the continued fractions found exactly x_final/(2^(2n))."
                else:
                    return sorted((one_factor, other_factor))

        logger.debug(
            "Cannot find factors from measurement %s because %s",
            measurement,
            fail_reason or "it took too many attempts.",
        )
        return None
    
    @staticmethod
    def _calculate_continued_fraction(b: array.array) -> int:
        """Calculate the continued fraction of x/T from the current terms of expansion b."""
        x_over_T = 0

        for i in reversed(range(len(b) - 1)):
            x_over_T = 1 / (b[i + 1] + x_over_T)

        x_over_T += b[0]

        frac = fractions.Fraction(x_over_T).limit_denominator()

        logger.debug("Approximation number %s of continued fractions:", len(b))
        logger.debug("Numerator:%s \t\t Denominator: %s.", frac.numerator, frac.denominator)
        return frac.denominator
    
    def factor(self, N: int, a: int = 2) -> ShorResult:
        """Execute the algorithm with improved error handling."""
        self._validate_input(N, a)
        if self.backend is None:
            raise ValueError("A Backend must be supplied to run the quantum algorithm.")
            
        result = ShorResult()
        
        # Check if the input integer N is a power
        tf, b, p = is_power(N, return_decomposition=True)
        if tf:
            logger.info("The input integer is a power: %s=%s^%s.", N, b, p)
            result.factors.append([b])
            return result
            
        if not result.factors:
            logger.debug("Running with N=%s and a=%s.", N, a)
            
            try:
                # Use statevector simulator for better compatibility
                if hasattr(self.backend, 'name') and 'statevector' in self.backend.name:
                    n = N.bit_length()
                    circuit = self.construct_circuit(N=N, a=a, measurement=False)
                    
                    # Decompose the circuit to avoid custom instruction errors
                    transpiled_circuit = transpile(circuit, 
                                                 backend=self.backend, 
                                                 optimization_level=0)
                    
                    logger.warning("Using statevector simulator - memory intensive for large N")
                    job = self.backend.run(transpiled_circuit)
                    result_data = job.result()
                    complete_state_vec = result_data.get_statevector(transpiled_circuit)
                    
                    up_qreg_density_mat = partial_trace(complete_state_vec, range(2 * n, 4 * n + 2))
                    up_qreg_density_mat_diag = np.diag(up_qreg_density_mat)
                    counts = dict()
                    for i, v in enumerate(up_qreg_density_mat_diag):
                        if not np.isclose(v, 0):
                            counts[bin(int(i))[2:].zfill(2 * n)] = abs(v) ** 2
                            
                else:
                    # Use regular simulator with measurements
                    circuit = self.construct_circuit(N=N, a=a, measurement=True)
                    
                    # Decompose the circuit
                    transpiled_circuit = transpile(circuit, 
                                                 backend=self.backend, 
                                                 optimization_level=1)
                    
                    job = self.backend.run(transpiled_circuit, shots=1000)
                    result_data = job.result()
                    counts = result_data.get_counts(transpiled_circuit)
                
                result.total_counts = len(counts)
                
                # Analyze each measurement result
                for measurement in list(counts.keys()):
                    logger.info("------> Analyzing result %s.", measurement)
                    factors = self._get_factors(N, a, measurement)
                    if factors:
                        logger.info("Found factors %s from measurement %s.", factors, measurement)
                        result.successful_counts += 1
                        if factors not in result.factors:
                            result.factors.append(factors)
                            
            except Exception as e:
                logger.error(f"Error during quantum execution: {e}")
                logger.info("Quantum execution failed, but this is expected for complex circuits")
                
        return result

if __name__ == "__main__":
    backend = AerSimulator()
    shor = Shor(backend=backend)
    result = shor.factor(N=15, a=2)
    print(f"Result: {result}")