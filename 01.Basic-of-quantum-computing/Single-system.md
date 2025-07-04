# Part 1: Classical States and Probability Vectors

## 1. Classical States
- **System X**: Has finite classical states (configurations that can be recognized)
- **Classical state set Σ**: Finite, nonempty set of possible states

### Examples:
- **Bit**: Σ = {0,1}
- **Die**: Σ = {1,2,3,4,5,6}  
- **Fan**: Σ = {high, medium, low, off}

## 2. Probabilistic States
When knowledge is uncertain, we use **probability vectors**:

### Example (Bit):
Pr(X=0) = 3/4, Pr(X=1) = 1/4

Vector representation:
```
(3/4)
(1/4)
```

## Probability Vector Properties:
1. All entries ≥ 0
2. Sum of entries = 1

**Symbol**: Column vector with probabilities for each classical state

## 3. Measuring Probabilistic States

**Measurement**: Looking at system and recognizing its classical state without ambiguity

### What happens when we measure:
- We see only one classical state (not the probabilistic state)
- Our knowledge changes → probabilistic state updates
- New state becomes **standard basis vector**

### Standard Basis Vectors (Ket notation):
- **|a⟩**: "ket a" - certainty that system is in state a
- Has 1 for state a, 0 for all others

### Examples:
**Bit**: |0⟩ = (1,0), |1⟩ = (0,1)

**Any probability vector** can be written as:
(3/4, 1/4) = 3/4|0⟩ + 1/4|1⟩

### Coin Example:
- Before looking: (1/2, 1/2) = 1/2|heads⟩ + 1/2|tails⟩  
- After seeing tails: |tails⟩ = (0,1)

**Key Point**: Measurement changes knowledge, not the system itself

## 4. Classical Operations

### 4.1 Deterministic Operations
**Function f: Σ → Σ** transforms each state a to f(a)

**Bit functions** (Σ = {0,1}):
- f₁: constant 0 (00→0, 11→0)  
- f₂: identity (00→0, 11→1)
- f₃: NOT (00→1, 11→0)
- f₄: constant 1 (00→1, 11→1)

**Matrix representation**: M|a⟩ = |f(a)⟩
- Each column has exactly one 1, rest are 0s

**Examples**:
- M₂ = $\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$ (identity)
<br/>
- M₃ = $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ (NOT)

### 4.2 Dirac Notation (Bra-Ket)
- **|a⟩**: "ket a" (column vector)
  - Standard basis vector: 1 for state a, 0 for others
  - Example: |0⟩ = $\begin{pmatrix} 1 \\ 0 \end{pmatrix}$, |1⟩ = $\begin{pmatrix} 0 \\ 1 \end{pmatrix}$

- **⟨a|**: "bra a" (row vector)  
  - Row version of |a⟩
  - Example: ⟨0| = (1 0), ⟨1| = (0 1)

- **⟨a|b⟩**: "bracket" (inner product)
  - = 1 if a=b, 0 if a≠b
  - Example: ⟨0|0⟩ = 1, ⟨0|1⟩ = 0

- **|b⟩⟨a|**: "outer product" (matrix)
  - Creates matrix with 1 at position (b,a), 0 elsewhere
  - Example: |0⟩⟨1| = $\begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$

**Matrix form**: M = Σ |f(a)⟩⟨a|

### 4.3 Probabilistic Operations
**Stochastic matrices**: columns are probability vectors
1. All entries ≥ 0
2. Each column sums to 1

**Example**: Bit operation that flips state 1 randomly
Matrix: (1 1/2; 0 1/2)

### 4.4 Composition
**Sequential operations**: M₂M₁ (apply M₁ first, then M₂)
- Order matters: M₂M₁ ≠ M₁M₂
- Result is also stochastic

# Part 2: Quantum Information

## 5. Quantum State Vectors
**Properties**:
1. Entries are complex numbers
2. Sum of absolute values squared = 1 (unit vector)

**Euclidean norm**: ||v|| = √(Σ|αₖ|²) = 1

## 6. Qubit States
**Qubit**: quantum system with classical states {0,1}

**Examples**:
- |0⟩ = $\begin{pmatrix} 1 \\ 0 \end{pmatrix}$, |1⟩ = $\begin{pmatrix} 0 \\ 1 \end{pmatrix}$ (standard basis)
<br/>
- |+⟩ = $\frac{1}{\sqrt{2}}$|0⟩ + $\frac{1}{\sqrt{2}}$|1⟩ = $\begin{pmatrix} \frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} \end{pmatrix}$ (plus state)
<br/>
- |−⟩ = $\frac{1}{\sqrt{2}}$|0⟩ − $\frac{1}{\sqrt{2}}$|1⟩ (minus state)
<br/>
- $\frac{1+2i}{3}$|0⟩ − $\frac{2}{3}$|1⟩ (complex superposition)

**Superposition**: Linear combination of basis states

## 7. Dirac Notation for Quantum States
- **⟨ψ|**: Row vector (conjugate-transpose of |ψ⟩)
- **⟨a|ψ⟩**: Entry of |ψ⟩ corresponding to state a
- **|ψ⟩**: General quantum state vector

**Example**: If |ψ⟩ = $\frac{1+2i}{3}$|0⟩ − $\frac{2}{3}$|1⟩
Then ⟨ψ| = $\frac{1-2i}{3}$⟨0| − $\frac{2}{3}$⟨1|

## 8. General Quantum Systems
**Uniform superposition**: $\frac{1}{\sqrt{|Σ|}}$Σ|a⟩ (equal amplitude for all states)

**Advantage of Dirac notation**:
- No need to specify ordering of classical states
- Compact representation for large systems
- Handles indeterminate aspects

## 9. Measuring Quantum States

**Born Rule**: Probability of measuring classical state a = |⟨a|ψ⟩|²

### Examples:
**Plus state**: |+⟩ = $\frac{1}{\sqrt{2}}$|0⟩ + $\frac{1}{\sqrt{2}}$|1⟩
- Pr(0) = |⟨0|+⟩|² = |$\frac{1}{\sqrt{2}}$|² = $\frac{1}{2}$
- Pr(1) = |⟨1|+⟩|² = |$\frac{1}{\sqrt{2}}$|² = $\frac{1}{2}$

**Minus state**: |−⟩ = $\frac{1}{\sqrt{2}}$|0⟩ − $\frac{1}{\sqrt{2}}$|1⟩
- Same measurement probabilities as |+⟩!
- Pr(0) = Pr(1) = $\frac{1}{2}$

**Key insight**: |+⟩ and |−⟩ are distinguishable by operations, not measurements

## 10. Unitary Operations

**Unitary matrix U**: UU† = U†U = I
- U† = conjugate-transpose of U
- Preserves quantum state norm: ||U|ψ⟩|| = ||ψ⟩||
- Maps quantum states to quantum states

### 10.1 Pauli Operations (Single Qubit)
- **I** = $\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$ (identity)
<br/>
- **X** = $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ (bit flip/NOT)
  - X|0⟩ = |1⟩, X|1⟩ = |0⟩
<br/>
- **Z** = $\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$ (phase flip)
  - Z|0⟩ = |0⟩, Z|1⟩ = −|1⟩
<br/>
- **Y** = $\begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$

### 10.2 Hadamard Operation
**H** = $\begin{pmatrix} \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}} \end{pmatrix}$

**Key transformations**:
- H|0⟩ = |+⟩, H|1⟩ = |−⟩  
- H|+⟩ = |0⟩, H|−⟩ = |1⟩

**Distinguishes |+⟩ and |−⟩**: H then measure gives 0 or 1 with certainty

### 10.3 Phase Operations
**P_θ** = $\begin{pmatrix} 1 & 0 \\ 0 & e^{iθ} \end{pmatrix}$

**Special cases**:
- **S** = P_{π/2} = $\begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}$
<br/>
- **T** = P_{π/4} = $\begin{pmatrix} 1 & 0 \\ 0 & \frac{1+i}{\sqrt{2}} \end{pmatrix}$

### 10.4 Composition
**Sequential operations**: R = U₂U₁ (apply U₁ first, then U₂)

**Example**: R = HSH is a square root of NOT (R² = X)

### 10.5 Larger Systems
**Permutation matrices**: Rearrange basis states (both classical and quantum)
**Quantum Fourier Transform**: Key component in quantum algorithms