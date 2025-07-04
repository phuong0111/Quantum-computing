# Tensor Product (A ⊗ B) Explanation

## Definition

**Tensor product** (A ⊗ B) is a mathematical operation that combines two matrices or vectors to create a larger structure.

## For Matrices

### General Form:
If A is m×m and B is n×n, then A ⊗ B is (mn)×(mn)

$$A \otimes B = \begin{pmatrix} a_{11}B & a_{12}B & \cdots & a_{1m}B \\ a_{21}B & a_{22}B & \cdots & a_{2m}B \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1}B & a_{m2}B & \cdots & a_{mm}B \end{pmatrix}$$

### Example (2×2 matrices):
$$A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}, \quad B = \begin{pmatrix} w & x \\ y & z \end{pmatrix}$$

$$A \otimes B = \begin{pmatrix} a \begin{pmatrix} w & x \\ y & z \end{pmatrix} & b \begin{pmatrix} w & x \\ y & z \end{pmatrix} \\ c \begin{pmatrix} w & x \\ y & z \end{pmatrix} & d \begin{pmatrix} w & x \\ y & z \end{pmatrix} \end{pmatrix} = \begin{pmatrix} aw & ax & bw & bx \\ ay & az & by & bz \\ cw & cx & dw & dx \\ cy & cz & dy & dz \end{pmatrix}$$

## For Vectors

### Column Vectors:
$$|a⟩ = \begin{pmatrix} a_1 \\ a_2 \end{pmatrix}, \quad |b⟩ = \begin{pmatrix} b_1 \\ b_2 \end{pmatrix}$$

$$|a⟩ \otimes |b⟩ = \begin{pmatrix} a_1 \begin{pmatrix} b_1 \\ b_2 \end{pmatrix} \\ a_2 \begin{pmatrix} b_1 \\ b_2 \end{pmatrix} \end{pmatrix} = \begin{pmatrix} a_1 b_1 \\ a_1 b_2 \\ a_2 b_1 \\ a_2 b_2 \end{pmatrix}$$

## Quantum Examples

### Basis States:
$$|0⟩ \otimes |0⟩ = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \otimes \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix} = |00⟩$$

$$|0⟩ \otimes |1⟩ = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \otimes \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix} = |01⟩$$

### Pauli Gates:
$$X \otimes I = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \otimes \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = \begin{pmatrix} 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \\ 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \end{pmatrix}$$

## Key Properties

### 1. **Distributive**:
$(A + B) \otimes C = A \otimes C + B \otimes C$

### 2. **Associative**:
$(A \otimes B) \otimes C = A \otimes (B \otimes C)$

### 3. **Mixed Product**:
$(A \otimes B)(C \otimes D) = (AC) \otimes (BD)$

### 4. **Not Commutative**:
$A \otimes B \neq B \otimes A$ (in general)

## Physical Meaning in Quantum

### 1. **Independent Systems**:
If system 1 is in state |ψ⟩ and system 2 is in state |φ⟩, the combined system is |ψ⟩ ⊗ |φ⟩

### 2. **Independent Operations**:
If gate A acts on qubit 1 and gate B acts on qubit 2, the combined operation is A ⊗ B

### 3. **No Entanglement**:
Product states |ψ⟩ ⊗ |φ⟩ represent **separable** (non-entangled) systems

## Operation on Product States

### Key Rule:
$(A \otimes B)(|ψ⟩ \otimes |φ⟩) = (A|ψ⟩) \otimes (B|φ⟩)$

### Example:
$(X \otimes H)(|0⟩ \otimes |0⟩) = (X|0⟩) \otimes (H|0⟩) = |1⟩ \otimes |+⟩$

## In CHSH Context

### Bell State Operations:
$(U_0 \otimes U_{\pi/8})|φ^+⟩$ means:
- **Apply $U_0$ to first qubit** of the Bell pair
- **Apply $U_{\pi/8}$ to second qubit** of the Bell pair
- **Simultaneously and independently**

### Why This Works:
- **Bell state** |φ⁺⟩ = (1/√2)(|00⟩ + |11⟩)
- **Tensor operation** acts on each component
- **Preserves entanglement structure** while rotating measurement basis

## Tensor vs Regular Product

### Regular Matrix Product (AB):
- **Requires compatible dimensions** (A: m×n, B: n×p → AB: m×p)
- **Combines matrices sequentially**
- **Represents composition** of operations

### Tensor Product (A ⊗ B):
- **Always possible** regardless of dimensions
- **Combines matrices in parallel**
- **Represents independent operations**

**Bottom line**: Tensor product A ⊗ B combines two mathematical objects to represent **independent, parallel operations** on separate parts of a composite quantum system!