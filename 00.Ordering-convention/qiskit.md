# Qiskit Qubit Ordering Conventions

## Visual Circuit Representation

In Qiskit circuit diagrams:
- **Top wire** = **Rightmost qubit** in state notation
- **Bottom wire** = **Leftmost qubit** in state notation

```
q[1] ——————— (top wire, rightmost in |q₁q₀⟩)
q[0] ——————— (bottom wire, leftmost in |q₁q₀⟩)
```

## Index Ordering

**Least Significant Bit (LSB) = Lowest Index**
- `q[0]` is the least significant bit
- `q[1]` is more significant than `q[0]`
- `q[n-1]` is the most significant bit

## State Notation Examples

### 2-Qubit System
```
Circuit:        State Notation:
q[1] ———        |q₁q₀⟩
q[0] ———        
```

**Examples:**
- `|00⟩`: q[1]=0, q[0]=0
- `|01⟩`: q[1]=0, q[0]=1  
- `|10⟩`: q[1]=1, q[0]=0
- `|11⟩`: q[1]=1, q[0]=1

### 3-Qubit System
```
Circuit:        State Notation:
q[2] ———        |q₂q₁q₀⟩
q[1] ———        
q[0] ———        
```

## Binary Value Mapping

The binary value represented by the qubits follows standard binary notation:
```
|q₂q₁q₀⟩ = q₂×2² + q₁×2¹ + q₀×2⁰
```

**Examples:**
- `|000⟩` = 0×4 + 0×2 + 0×1 = 0
- `|001⟩` = 0×4 + 0×2 + 1×1 = 1
- `|010⟩` = 0×4 + 1×2 + 0×1 = 2
- `|101⟩` = 1×4 + 0×2 + 1×1 = 5

## Important Notes

1. **Reading Order**: When reading state vectors, read from left to right, but remember that leftmost corresponds to highest-indexed qubit
2. **Tensor Products**: `|ψ⟩ = |q₁⟩ ⊗ |q₀⟩` where q[1] is written first
3. **Matrix Ordering**: State vectors and density matrices follow this same convention

## Common Confusion Points

- **Circuit vs. Math**: The top wire in circuits corresponds to the rightmost position in mathematical notation
- **Index vs. Significance**: Lower index means lower significance (opposite of some other conventions)
- **Tensor Product Order**: The order in tensor products follows the state notation, not the circuit visual order