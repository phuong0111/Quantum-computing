# Multiple Systems - Classical Information

## 1. Classical States via Cartesian Product

### 1.1 Two Systems
**Systems**: X (state set Σ), Y (state set Γ)
**Joint system**: (X,Y) with state set Σ × Γ

**Cartesian Product**: Σ × Γ = {(a,b) : a∈Σ and b∈Γ}

**Interpretation**: 
- (X,Y) in state (a,b) means X in state a AND Y in state b

### 1.2 Multiple Systems
**n systems**: X₀, X₁, ..., X_{n-1} with state sets Σ₀, Σ₁, ..., Σ_{n-1}
**Joint state set**: Σ_{n-1} × ... × Σ₀
**Qiskit convention**: Right-to-left ordering (X_{n-1},...,X₀)

### 1.3 String Representation
**Notation**: (a_{n-1},...,a₀) written as a_{n-1}...a₀

**Examples**:
- Two bits: {00, 01, 10, 11}
- Ten bits: 2¹⁰ = 1024 possible states
- State 0000000110: X₁=1, X₂=1, others=0

## 2. Ordering Convention

**Alphabetical ordering**: Left-to-right significance decreases
- {1,2,3} × {0,1} → (1,0), (1,1), (2,0), (2,1), (3,0), (3,1)
- Like decimal system: 00, 01, 10, 11

## 3. Probabilistic States (Multiple Systems)

### 3.1 Basic Definition
**Probabilistic state**: Assigns probability to each element of Cartesian product

**Example** (two bits):
- Pr((X,Y)=(0,0)) = 1/2
- Pr((X,Y)=(0,1)) = 0  
- Pr((X,Y)=(1,0)) = 0
- Pr((X,Y)=(1,1)) = 1/2

**Vector representation**: 
$$\begin{pmatrix} 1/2 \\ 0 \\ 0 \\ 1/2 \end{pmatrix}$$ ← (00, 01, 10, 11)

## 4. Independence

### 4.1 Definition
**Systems X and Y are independent** if:
Pr((X,Y)=(a,b)) = Pr(X=a) × Pr(Y=b) for all a,b

### 4.2 Vector Condition
**Independence**: |π⟩ = |φ⟩ ⊗ |ψ⟩ (product state)
where p_{ab} = q_a × r_b

**Example** (independent):
- |π⟩ = 1/6|00⟩ + 1/12|01⟩ + 1/2|10⟩ + 1/4|11⟩
- |φ⟩ = 1/4|0⟩ + 3/4|1⟩, |ψ⟩ = 2/3|0⟩ + 1/3|1⟩

### 4.3 Correlation
**Correlation = lack of independence**

**Example** (correlated):
- |π⟩ = 1/2|00⟩ + 1/2|11⟩
- Cannot write as |φ⟩ ⊗ |ψ⟩

## 5. Tensor Products

### 5.1 Definition
**Given**: |φ⟩ = Σ α_a|a⟩, |ψ⟩ = Σ β_b|b⟩

**Tensor product**: |φ⟩ ⊗ |ψ⟩ = Σ α_a β_b |ab⟩

**Alternative notation**: |φ⟩|ψ⟩ or |φ⊗ψ⟩

### 5.2 Matrix Form
$$\begin{pmatrix} α₁ \\ ⋮ \\ α_m \end{pmatrix} ⊗ \begin{pmatrix} β₁ \\ ⋮ \\ β_k \end{pmatrix} = \begin{pmatrix} α₁β₁ \\ ⋮ \\ α₁β_k \\ α₂β₁ \\ ⋮ \\ α_m β_k \end{pmatrix}$$

### 5.3 Key Properties
**Standard basis**: |a⟩ ⊗ |b⟩ = |ab⟩

**Bilinear**:
1. Linear in first argument: (|φ₁⟩ + |φ₂⟩) ⊗ |ψ⟩ = |φ₁⟩⊗|ψ⟩ + |φ₂⟩⊗|ψ⟩
2. Linear in second argument: |φ⟩ ⊗ (|ψ₁⟩ + |ψ₂⟩) = |φ⟩⊗|ψ₁⟩ + |φ⟩⊗|ψ₂⟩

**Scalar multiplication**: α|φ⟩ ⊗ |ψ⟩ = |φ⟩ ⊗ α|ψ⟩ = α(|φ⟩ ⊗ |ψ⟩)

### 5.4 Independence Condition
**Product state**: ⟨ab|π⟩ = ⟨a|φ⟩⟨b|ψ⟩

**Systems independent ↔ Joint state is product state**

## 6. Multiple Systems (n ≥ 3)

### 6.1 Tensor Products
**n-way tensor product**: |ψ⟩ = |φ_{n-1}⟩ ⊗ ... ⊗ |φ₀⟩

**Definition**: ⟨a_{n-1}...a₀|ψ⟩ = ⟨a_{n-1}|φ_{n-1}⟩...⟨a₀|φ₀⟩

**Recursive definition**: |φ_{n-1}⟩ ⊗ ... ⊗ |φ₀⟩ = |φ_{n-1}⟩ ⊗ (|φ_{n-2}⟩ ⊗ ... ⊗ |φ₀⟩)

### 6.2 Independence Types
**Mutually independent**: Joint state is product state
**Pairwise independent**: Each pair is independent (weaker condition)

### 6.3 General Properties
**Multilinear**: Linear in each argument separately
**Standard basis**: |a_{n-1}⟩ ⊗ ... ⊗ |a₀⟩ = |a_{n-1}...a₀⟩

## 7. Measurements of Multiple Systems

### 7.1 Complete Measurements
**Measuring all systems**: Standard single-system rules apply
- Joint state |ψ⟩ = ½|00⟩ + ½|11⟩
- Outcome 00 with probability ½, outcome 11 with probability ½
- Post-measurement state: |00⟩ or |11⟩

### 7.2 Partial Measurements
**Measuring subset of systems**: Affects remaining unmeasured systems

**Key principle**: Pr(X=a) = Σ_b Pr((X,Y)=(a,b))
- **Reduced/marginal state**: Probabilities for individual system
- **No faster-than-light signaling**: Measuring Y cannot affect X probabilities

### 7.3 Conditional Probabilities
**After measuring X=a**:
- Pr(Y=b|X=a) = Pr((X,Y)=(a,b))/Pr(X=a)
- **Normalization**: Divide by measurement probability

### 7.4 Vector Formulation
**Joint state**: |ψ⟩ = Σ p_{ab}|ab⟩

**Measuring X**:
1. **Probability**: Pr(X=a) = Σ_c p_{ac}
2. **Reduced state of X**: Σ_a (Σ_c p_{ac})|a⟩
3. **Conditional state of Y**: |π_a⟩ = (Σ_b p_{ab}|b⟩)/(Σ_c p_{ac})
4. **Post-measurement joint**: |a⟩ ⊗ |π_a⟩

### 7.5 Factorization Method
**Express as**: |ψ⟩ = |0⟩ ⊗ |φ₀⟩ + |1⟩ ⊗ |φ₁⟩
- **Measurement probabilities**: ||φᵢ⟩||²
- **Post-measurement states**: |i⟩ ⊗ |φᵢ⟩/||φᵢ⟩||

**Example**:
- |ψ⟩ = ½|0,1⟩ + 1/12|0,3⟩ + 1/12|1,1⟩ + ⅙|1,2⟩ + ⅙|1,3⟩
- = |0⟩ ⊗ (½|1⟩ + 1/12|3⟩) + |1⟩ ⊗ (1/12|1⟩ + ⅙|2⟩ + ⅙|3⟩)
- Pr(X=0) = 7/12, Pr(X=1) = 5/12

## 8. Operations on Multiple Systems

### 8.1 Joint Operations
**Stochastic matrices**: Rows/columns indexed by Σ × Γ

**Controlled-NOT** (X controls Y):
$\begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$

**Detailed Breakdown**

$$\begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix} \begin{pmatrix} |00⟩ \\ |01⟩ \\ |10⟩ \\ |11⟩ \end{pmatrix}$$

### Column 0 (Input |00⟩):
$$\begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix}$$ 
→ 1×|00⟩ + 0×|01⟩ + 0×|10⟩ + 0×|11⟩ = **|00⟩**

### Column 1 (Input |01⟩):  
$$\begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix}$$
→ 0×|00⟩ + 1×|01⟩ + 0×|10⟩ + 0×|11⟩ = **|01⟩**

### Column 2 (Input |10⟩):
$$\begin{pmatrix} 0 \\ 0 \\ 0 \\ 1 \end{pmatrix}$$
→ 0×|00⟩ + 0×|01⟩ + 0×|10⟩ + 1×|11⟩ = **|11⟩**

### Column 3 (Input |11⟩):
$$\begin{pmatrix} 0 \\ 0 \\ 1 \\ 0 \end{pmatrix}$$
→ 0×|00⟩ + 0×|01⟩ + 1×|10⟩ + 0×|11⟩ = **|10⟩**

## Summary of Transformations
- **|00⟩ → |00⟩** (Column 0 → result has "1" in row 0)
- **|01⟩ → |01⟩** (Column 1 → result has "1" in row 1)  
- **|10⟩ → |11⟩** (Column 2 → result has "1" in row 3)
- **|11⟩ → |10⟩** (Column 3 → result has "1" in row 2)

Action: |00⟩→|00⟩, |01⟩→|01⟩, |10⟩→|11⟩, |11⟩→|10⟩

### 8.2 Tensor Products of Matrices
**Definition**: M ⊗ N
- ⟨ac|M⊗N|bd⟩ = ⟨a|M|b⟩⟨c|N|d⟩
- (M⊗N)(|φ⟩⊗|ψ⟩) = (M|φ⟩) ⊗ (N|ψ⟩)

**Block structure**:
$M ⊗ N = \begin{pmatrix} α_{11}N & \cdots & α_{1m}N \\ \vdots & \ddots & \vdots \\ α_{m1}N & \cdots & α_{mm}N \end{pmatrix}$

### 8.3 Properties of Matrix Tensor Products
**Multiplicative**: (M₁⊗N₁)(M₂⊗N₂) = (M₁M₂) ⊗ (N₁N₂)
**Stochastic preservation**: M⊗N stochastic if M,N stochastic
**Identity operations**: M⊗I (apply M to first, do nothing to second)

### 8.4 Independent Operations
**Tensor products represent independence**:
- **States**: |φ⟩⊗|ψ⟩ (systems independent)
- **Operations**: M⊗N (operations independent)

**Example**:
- Apply probabilistic flip to X: $\begin{pmatrix} 1 & 1/2 \\ 0 & 1/2 \end{pmatrix}$
- Apply NOT to Y: $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$
- Joint operation: First matrix ⊗ Second matrix

### 8.5 Complex Operations
**Three-bit increment mod 8**:
- |000⟩→|001⟩, |001⟩→|010⟩, ..., |111⟩→|000⟩
- Matrix: Σₖ |k+1 mod 8⟩⟨k|

## Key Insights

1. **Partial measurements** create conditional states and update knowledge
2. **Tensor products** represent both independent states and operations  
3. **Factorization** simplifies partial measurement calculations
4. **Matrix tensor products** combine independent operations
5. **Stochastic properties** preserved under tensor products
6. **Physical consistency**: No faster-than-light signaling