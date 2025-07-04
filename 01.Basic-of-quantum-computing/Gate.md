# Quantum Gates Reference

## Single-Qubit Gates

### 1. Identity Gate (I)
**Matrix**: $$I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$$

**Action**:
- I|0⟩ = |0⟩
- I|1⟩ = |1⟩

**Purpose**: Do nothing (placeholder operation)

### 2. Pauli-X Gate (X) - Bit Flip
**Matrix**: $$X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$$

**Action**:
- X|0⟩ = |1⟩
- X|1⟩ = |0⟩

**Purpose**: Flips qubit state (quantum NOT gate)
**Symbol**: ⊕ or X box

### 3. Pauli-Z Gate (Z) - Phase Flip  
**Matrix**: $$Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

**Action**:
- Z|0⟩ = |0⟩
- Z|1⟩ = -|1⟩

**Purpose**: Adds phase of -1 to |1⟩ state
**Symbol**: Z box

### 4. Pauli-Y Gate (Y)
**Matrix**: $$Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$$

**Action**:
- Y|0⟩ = i|1⟩
- Y|1⟩ = -i|0⟩

**Purpose**: Combination of bit flip and phase flip
**Symbol**: Y box

### 5. Hadamard Gate (H)
**Matrix**: $$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$

**Action**:
- H|0⟩ = |+⟩ = $$\frac{1}{\sqrt{2}}$$(|0⟩ + |1⟩)
- H|1⟩ = |−⟩ = $$\frac{1}{\sqrt{2}}$$(|0⟩ - |1⟩)

**Inverse property**: H|+⟩ = |0⟩, H|−⟩ = |1⟩

**Purpose**: Creates superposition states
**Symbol**: H box

### 6. Phase Gates

#### S Gate (Quarter Phase)
**Matrix**: $$S = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}$$

**Action**:
- S|0⟩ = |0⟩  
- S|1⟩ = i|1⟩

#### T Gate (Eighth Phase)
**Matrix**: $$T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & \frac{1+i}{\sqrt{2}} \end{pmatrix}$$

**Action**:
- T|0⟩ = |0⟩
- T|1⟩ = e^{iπ/4}|1⟩

#### General Phase Gate
**Matrix**: $$P_θ = \begin{pmatrix} 1 & 0 \\ 0 & e^{iθ} \end{pmatrix}$$

**Special cases**: I = P₀, Z = P_π, S = P_{π/2}, T = P_{π/4}

## Two-Qubit Gates

### 1. CNOT Gate (Controlled-X)
**Matrix**: $$\text{CNOT} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$$

**Action**:
- CNOT|00⟩ = |00⟩
- CNOT|01⟩ = |01⟩  
- CNOT|10⟩ = |11⟩
- CNOT|11⟩ = |10⟩

**Rule**: If control = 1, flip target; otherwise do nothing
**Symbol**: Control (●) connected to target (⊕)

### 2. Controlled-Z Gate (CZ)
**Matrix**: $$\text{CZ} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -1 \end{pmatrix}$$

**Action**:
- CZ|00⟩ = |00⟩
- CZ|01⟩ = |01⟩
- CZ|10⟩ = |10⟩  
- CZ|11⟩ = -|11⟩

**Rule**: If both qubits = 1, add phase -1; otherwise do nothing
**Symbol**: Control (●) connected to target (●)

### 3. SWAP Gate
**Matrix**: $$\text{SWAP} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

**Action**:
- SWAP|00⟩ = |00⟩
- SWAP|01⟩ = |10⟩
- SWAP|10⟩ = |01⟩
- SWAP|11⟩ = |11⟩

**Rule**: Exchange the states of two qubits
**Symbol**: ×——× (crossed lines)

## Three-Qubit Gates

### 1. Toffoli Gate (CCX) - Controlled-Controlled-X
**Action**: Flip target if both controls = 1

**Truth table**:
- CCX|000⟩ = |000⟩, CCX|001⟩ = |001⟩
- CCX|010⟩ = |010⟩, CCX|011⟩ = |011⟩  
- CCX|100⟩ = |100⟩, CCX|101⟩ = |101⟩
- CCX|110⟩ = |111⟩, CCX|111⟩ = |110⟩

**Symbol**: Two controls (●●) connected to target (⊕)

### 2. Fredkin Gate (CSWAP) - Controlled-SWAP
**Action**: SWAP two qubits if control = 1

**Symbol**: Control (●) connected to SWAP (×——×)

## General Controlled Gates

### Controlled-U Gate
**Structure**: CU = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ U

**Rule**: Apply U to target if control = 1; otherwise apply identity

**Examples**:
- **CNOT**: U = X
- **CZ**: U = Z  
- **CY**: U = Y
- **CH**: U = H

## Gate Properties

### Universal Gate Sets
1. **{H, T, CNOT}**: Computationally universal
2. **{H, S, T, CNOT}**: Common practical set
3. **Any universal set** can approximate any unitary operation

### Important Relationships
- **Self-inverse**: H² = I, X² = I, Y² = I, Z² = I
- **Commutation**: [X,Z] = 2iY (anticommute)
- **Phase relations**: S² = Z, T⁴ = I

### Circuit Identities
- **HXH = Z**: Hadamard conjugates X to Z
- **HZH = X**: Hadamard conjugates Z to X  
- **CNOT|+0⟩ = |Φ⁺⟩**: Creates Bell state

## Measurement
**Symbol**: ⌒ (meter/gauge icon)
**Action**: Projects qubit onto computational basis {|0⟩, |1⟩}
**Output**: Classical bit (0 or 1) based on Born rule probabilities