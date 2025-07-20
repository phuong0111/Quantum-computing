# Shor's Algorithm Implementation Documentation

## 1. Quantum Fourier Transform Helper Functions

### 1.1 Angle Calculation for Fourier Space Addition

```python
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
```

#### Explanation

This function computes the rotation angles required to encode an integer `a` into the quantum Fourier basis for quantum addition circuits.

**Algorithm breakdown:**

1. **Binary representation**: Converts integer `a` to little-endian binary format where the least significant bit comes first. This ordering matches how qubits are typically indexed in quantum circuits.

2. **Angle accumulation**: For each qubit position `i`, calculates its rotation angle by summing contributions from all lower-indexed qubits `j ≤ i`. Each bit `j` that equals '1' contributes `2^(-(i-j))` to the angle.

3. **Mathematical formula**: Implements $\text{angles}[i] = \pi \times \sum_{j=0}^{i} \text{bit}[j] \times 2^{-(i-j)}$ for all $j$ from 0 to $i$.

4. **Derivation**: In the QFT, encoding integer $a = \sum_{j=0}^{n-1} \text{bit}[j] \times 2^j$ requires phase rotations. For qubit $i$, the phase contribution becomes $\phi[i] = 2\pi \times \sum_{j=0}^{i} \text{bit}[j] \times 2^{-(i-j)}$. The algorithm computes this with $\pi$ scaling for implementation efficiency.

4. **Physical meaning**: The resulting angles represent phase rotations that, when applied to qubits in superposition, encode the binary representation of `a` in the Fourier domain where addition becomes a simple phase accumulation operation.

**Example**: For `a=5` (binary `1010` in little-endian) and `n=4`:
- Qubit 0: `angles[0] = 1 × 2^0 = 1` → `π` radians
- Qubit 1: `angles[1] = 1 × 2^(-1) + 0 × 2^0 = 0.5` → `0.5π` radians  
- Qubit 2: `angles[2] = 1 × 2^(-2) + 0 × 2^(-1) + 1 × 2^0 = 1.25` → `1.25π` radians

These angles are then used as parameters for quantum rotation gates in the addition circuit.

---

## 2. Modular Arithmetic Operations

### 2.1 Controlled Modular Multiplication

```python
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
    
    # Forward multiplication: b = (a * x) mod N
    circuit.append(qft, b_qreg)
    for i in range(n):
        append_adder(modulo_adder, a, i)
    circuit.append(iqft, b_qreg)
    
    # Conditional swap: if ctrl=1, swap x and b
    for i in range(n):
        circuit.cswap(ctrl_qreg, x_qreg[i], b_qreg[i])
    
    # Inverse multiplication: uncompute auxiliary register
    circuit.append(qft, b_qreg)
    a_inv = pow(a, -1, mod=N) if sys.version_info >= (3, 8) else self.modinv(a, N)
    modulo_adder_inv = modulo_adder.inverse()
    for i in reversed(range(n)):
        append_adder(modulo_adder_inv, a_inv, i)
    circuit.append(iqft, b_qreg)
    
    return circuit.to_instruction()
```

#### Explanation

This function implements controlled modular multiplication $|x\rangle \rightarrow |ax \bmod N\rangle$ when the control qubit is $|1\rangle$, which is essential for Shor's quantum period finding.

**Algorithm breakdown:**

1. **Quantum registers setup**:
   - `ctrl_qreg`: Control qubit that enables/disables the operation
   - `x_qreg`: Input register containing value $x$
   - `b_qreg`: Auxiliary register for computation (n+1 qubits for overflow)
   - `flag_qreg`: Additional control for modular addition

2. **Forward multiplication**: Computes $b = (a \times x) \bmod N$ using repeated modular addition:
   $b = \sum_{i=0}^{n-1} x_i \times (a \times 2^i \bmod N) \bmod N$
   Each bit $x_i$ of the input controls addition of $(a \times 2^i) \bmod N$

3. **Conditional swap**: Uses controlled-SWAP gates to exchange $x$ and $b$ registers only when control qubit is $|1\rangle$

4. **Inverse computation**: Uncomputes the auxiliary register by performing inverse multiplication with $a^{-1} \bmod N$, ensuring the computation is reversible and leaves no garbage qubits

**Mathematical foundation**: 
The operation implements the unitary $U_a|x\rangle = |ax \bmod N\rangle$. The controlled version applies this transformation only when the control qubit is in state $|1\rangle$:
$\text{CMULT}_a|c\rangle|x\rangle = |c\rangle|x \oplus c \cdot (ax \bmod N)\rangle$

### 2.2 How Controlled Multiplication Uses Double-Controlled Addition

The `_controlled_multiple_mod_N` method implements modular multiplication by decomposing it into a series of modular additions using the **shift-and-add** algorithm.

#### Mathematical Foundation

To compute $(a \times x) \bmod N$, we use the binary representation of $x$:
$x = \sum_{i=0}^{n-1} x_i \times 2^i$

Therefore:
$a \times x = a \times \sum_{i=0}^{n-1} x_i \times 2^i = \sum_{i=0}^{n-1} x_i \times (a \times 2^i)$

And modulo N:
$(a \times x) \bmod N = \left(\sum_{i=0}^{n-1} x_i \times (a \times 2^i \bmod N)\right) \bmod N$

#### Implementation Strategy

```python
def append_adder(adder: QuantumCircuit, constant: int, idx: int):
    partial_constant = (pow(2, idx, N) * constant) % N  # Compute (a × 2^i) mod N
    angles = self._get_angles(partial_constant, n + 1)  # Get rotation angles
    bound = adder.assign_parameters({angle_params: angles})  # Bind angles to circuit
    circuit.append(bound, [*ctrl_qreg, x_qreg[idx], *b_qreg, *flag_qreg])
```

**Step-by-step process:**

1. **For each bit position i** in the input register $x$:
   - Compute `partial_constant = (a × 2^i) mod N`
   - Use `_get_angles()` to compute rotation angles for this constant
   - Apply `_double_controlled_phi_add_mod_N` with two controls:
     - **Control 1**: Main control qubit (enables entire multiplication)
     - **Control 2**: Bit $x_i$ (determines if this term is added)

2. **Double control logic**:
   ```
   If (main_control = |1⟩) AND (x_bit[i] = |1⟩):
       Add (a × 2^i) mod N to auxiliary register
   Else:
       Do nothing
   ```

#### Concrete Example: $(2 \times 3) \bmod 7$

**Parameters**: $a=2, x=3, N=7, n=3$

**Input decomposition**: $x = 3 = |011⟩ = 1 \times 2^0 + 1 \times 2^1 + 0 \times 2^2$

**Addition sequence**:

1. **i=0**: $x_0 = 1$
   - `partial_constant = (2 × 2^0) mod 7 = 2 mod 7 = 2`
   - `angles = _get_angles(2, 4)` → rotation angles for adding 2
   - **Double control**: main_ctrl=|1⟩ AND x[0]=|1⟩ → **Execute addition**
   - Result: auxiliary += 2

2. **i=1**: $x_1 = 1$ 
   - `partial_constant = (2 × 2^1) mod 7 = 4 mod 7 = 4`
   - `angles = _get_angles(4, 4)` → rotation angles for adding 4
   - **Double control**: main_ctrl=|1⟩ AND x[1]=|1⟩ → **Execute addition**
   - Result: auxiliary += 4 → auxiliary = (2 + 4) mod 7 = 6

3. **i=2**: $x_2 = 0$
   - `partial_constant = (2 × 2^2) mod 7 = 8 mod 7 = 1`
   - **Double control**: main_ctrl=|1⟩ AND x[2]=|0⟩ → **Skip addition**
   - Result: auxiliary unchanged

**Final result**: auxiliary = 6 = $(2 \times 3) \bmod 7$ ✓

#### Circuit Flow Integration

```python
# Forward multiplication phase
circuit.append(qft, b_qreg)
for i in range(n):
    append_adder(modulo_adder, a, i)  # Uses double-controlled addition
circuit.append(iqft, b_qreg)

# The modulo_adder is created as:
modulo_adder = self._double_controlled_phi_add_mod_N(
    angle_params, c_phi_add_N, iphi_add_N, qft, iqft
)
```

**Key insights:**

1. **Modular multiplication → Series of modular additions**: Each bit controls one addition
2. **Double control mechanism**: Precise control over which terms contribute
3. **QFT efficiency**: All additions happen in Fourier space for speed
4. **Automatic modular reduction**: Each addition properly handles overflow
5. **Reversible computation**: Can be undone for uncomputation phase

This elegant decomposition transforms the complex problem of quantum modular multiplication into manageable, controlled modular additions!

---

## 3. Advanced Modular Operations

### 3.1 Double-Controlled Modular Addition

```python
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
```

#### Explanation

This method implements **double-controlled modular addition**: $(b + a) \bmod N$ when both control qubits are $|1\rangle$. It's the core building block for modular multiplication.

**Algorithm breakdown:**

1. **Double-controlled addition**: 
   ```python
   cc_phi_add_a = self._phi_add_gate(angles).control(2)
   ```
   Adds value $a$ to register $b$ only when both controls are $|1\rangle$

2. **Overflow detection sequence**:
   ```python
   circuit.append(iphi_add_N, b_qreg)        # Subtract N
   circuit.append(iqft, b_qreg)              # Convert to computational basis  
   circuit.cx(b_qreg[-1], flag_qreg[0])      # Check if result ≥ N (overflow)
   circuit.append(qft, b_qreg)               # Back to Fourier basis
   ```

3. **Conditional correction**:
   ```python
   circuit.append(c_phi_add_N, [*flag_qreg, *b_qreg])  # Add N back if no overflow
   circuit.append(cc_iphi_add_a, [*ctrl_qreg, *b_qreg]) # Subtract original addition
   ```

4. **Flag reset and final correction**:
   ```python
   circuit.x(b_qreg[-1])                     # Flip MSB
   circuit.cx(b_qreg[-1], flag_qreg[0])      # Update flag
   circuit.x(b_qreg[-1])                     # Restore MSB
   circuit.append(cc_phi_add_a, [*ctrl_qreg, *b_qreg]) # Re-add if needed
   ```

**Mathematical operation**: Implements the conditional operation:
$\text{if } (ctrl_1 = 1) \land (ctrl_2 = 1): \quad b \leftarrow (b + a) \bmod N$

#### Usage in Controlled Multiplication

In the `_controlled_multiple_mod_N` method:

```python
modulo_adder = self._double_controlled_phi_add_mod_N(
    angle_params, c_phi_add_N, iphi_add_N, qft, iqft
)
```

**Integration pattern**:
- **First control**: From the main control qubit (enables/disables entire multiplication)
- **Second control**: From individual bits of the input $x$ register
- **Operation**: For each bit $x_i = 1$, add $(a \times 2^i) \bmod N$ to the result

**Example with parameters** $a=2, N=7, x=3$:
- Bit 0: $x_0 = 1 \rightarrow$ add $(2 \times 2^0) \bmod 7 = 2$
- Bit 1: $x_1 = 1 \rightarrow$ add $(2 \times 2^1) \bmod 7 = 4$ 
- Total: $(2 + 4) \bmod 7 = 6 = (2 \times 3) \bmod 7$ ✓

**Key insights**:
- **Modular arithmetic**: Automatically handles overflow using the flag qubit
- **Reversible computation**: Each addition can be undone for uncomputation
- **Quantum efficiency**: Uses QFT-based addition for logarithmic depth
- **Double control**: Enables precise control over when additions occur