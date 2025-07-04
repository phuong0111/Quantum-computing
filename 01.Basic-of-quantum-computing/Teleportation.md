# Explicit Quantum Teleportation Analysis

Let's work through the complete teleportation protocol using the state **|ψ⟩ = α|0⟩ + β|1⟩**.

## Initial Setup (Time |π₀⟩)

### Starting states:
- **Qubit Q**: α|0⟩ + β|1⟩ (to be teleported)
- **Bell pair (A,B)**: |φ⁺⟩ = (1/√2)(|00⟩ + |11⟩)

### Combined initial state:
|π₀⟩ = |φ⁺⟩ ⊗ (α|0⟩ + β|1⟩)

= (1/√2)(|00⟩ + |11⟩) ⊗ (α|0⟩ + β|1⟩)

= **(α|000⟩ + α|110⟩ + β|001⟩ + β|111⟩)/√2**

## Step 1: Alice's CNOT Gate (Time |π₁⟩)

Apply CNOT(Q,A) - Q controls, A target:

**CNOT transformations**:
- |000⟩ → |000⟩ (Q=0, don't flip A)
- |110⟩ → |110⟩ (Q=0, don't flip A)
- |001⟩ → |011⟩ (Q=1, flip A)
- |111⟩ → |101⟩ (Q=1, flip A)

**After CNOT**:
|π₁⟩ = **(α|000⟩ + α|110⟩ + β|011⟩ + β|101⟩)/√2**

## Step 2: Alice's Hadamard Gate (Time |π₂⟩)

Apply H to qubit Q:

**Hadamard transformations**:
- H|0⟩ = (1/√2)(|0⟩ + |1⟩) = |+⟩
- H|1⟩ = (1/√2)(|0⟩ - |1⟩) = |−⟩

**After H on Q**:
|π₂⟩ = (α|00⟩|+⟩ + α|11⟩|+⟩ + β|01⟩|−⟩ + β|10⟩|−⟩)/√2

**Expanding |+⟩ and |−⟩**:
= (α|000⟩ + α|001⟩ + α|110⟩ + α|111⟩ + β|010⟩ - β|011⟩ + β|100⟩ - β|101⟩)/(2)

**Reorganizing by AQ measurement outcomes**:
|π₂⟩ = **(1/2)[(α|0⟩ + β|1⟩)|00⟩ + (α|0⟩ - β|1⟩)|01⟩ + (α|1⟩ + β|0⟩)|10⟩ + (α|1⟩ - β|0⟩)|11⟩]**

## Step 3: Alice's Measurements & Bob's Corrections

### Case 1: Alice measures (a,b) = (0,0)
**Probability**: ||(1/2)(α|0⟩ + β|1⟩)||² = (|α|² + |β|²)/4 = **1/4**

**Post-measurement state**: (α|0⟩ + β|1⟩)|00⟩

**Bob's action**: Do nothing (I gate)

**Final state of B**: **α|0⟩ + β|1⟩** ✓

### Case 2: Alice measures (a,b) = (0,1)  
**Probability**: ||(1/2)(α|0⟩ - β|1⟩)||² = (|α|² + |β|²)/4 = **1/4**

**Post-measurement state**: (α|0⟩ - β|1⟩)|01⟩

**Bob's action**: Apply Z gate
- Z(α|0⟩ - β|1⟩) = α|0⟩ - β(-|1⟩) = α|0⟩ + β|1⟩

**Final state of B**: **α|0⟩ + β|1⟩** ✓

### Case 3: Alice measures (a,b) = (1,0)
**Probability**: ||(1/2)(α|1⟩ + β|0⟩)||² = (|α|² + |β|²)/4 = **1/4**

**Post-measurement state**: (α|1⟩ + β|0⟩)|10⟩

**Bob's action**: Apply X gate  
- X(α|1⟩ + β|0⟩) = α|0⟩ + β|1⟩

**Final state of B**: **α|0⟩ + β|1⟩** ✓

### Case 4: Alice measures (a,b) = (1,1)
**Probability**: ||(1/2)(α|1⟩ - β|0⟩)||² = (|α|² + |β|²)/4 = **1/4**

**Post-measurement state**: (α|1⟩ - β|0⟩)|11⟩

**Bob's action**: Apply ZX gate
- X(α|1⟩ - β|0⟩) = α|0⟩ - β|1⟩
- Z(α|0⟩ - β|1⟩) = α|0⟩ + β|1⟩

**Final state of B**: **α|0⟩ + β|1⟩** ✓

## Key Results

### Perfect Teleportation
In **all four cases**, Bob's qubit B ends up in the exact original state **α|0⟩ + β|1⟩**

### Equal Probabilities  
Each measurement outcome has probability **1/4**, independent of α and β

### No Cloning
- Original qubit Q is destroyed (becomes |b⟩)
- Alice's qubit A becomes |a⟩ 
- Only one copy of α|0⟩ + β|1⟩ exists (now in B)

### Resources Used
- **1 e-bit** (Bell pair) consumed
- **2 classical bits** transmitted  
- **1 qubit** perfectly transmitted

**Conclusion**: Quantum teleportation successfully transfers the state α|0⟩ + β|1⟩ from Alice to Bob using entanglement and classical communication!


## Bob Already Has α and β (Just "Scrambled")

### Bob's Qubit States (Before Classical Communication):

| Alice's measurement | Bob's actual state | Status |
|-------------------|-------------------|--------|
| (0,0) | α\|0⟩ + β\|1⟩ | ✓ Perfect! |
| (0,1) | α\|0⟩ - β\|1⟩ | Wrong sign on β |
| (1,0) | α\|1⟩ + β\|0⟩ | Positions swapped |
| (1,1) | α\|1⟩ - β\|0⟩ | Both swapped AND wrong sign |

### Bob's Dilemma
🤔 **Problem**: "I have some scrambled version of α|0⟩ + β|1⟩, but I don't know which scrambling!"

### Classical Bits = "Unscrambling Instructions"

| Alice sends (a,b) | Bob's instruction |
|------------------|------------------|
| (0,0) | "Correct state - do nothing!" |
| (0,1) | "Wrong sign on β - apply Z!" |
| (1,0) | "Swapped positions - apply X!" |
| (1,1) | "Both problems - apply XZ!" |

### Key Insight
- **Quantum information doesn't travel** - it gets distributed through entanglement
- **Bob already has α,β** - just in scrambled form (sign changes, position swaps)
- **Classical bits = decoder key** to unscramble what Bob already has
- **No faster-than-light communication**, but perfect quantum state transfer

**Bottom line**: The α,β coefficients are already at Bob's location through entanglement - they just need the right classical "unscrambling instructions"!

# Teleportation with Entangled Input (General Case)

## Setup: Q is Entangled with External System R

### Initial entangled state:
**Q-R system**: α|0⟩_Q|γ₀⟩_R + β|1⟩_Q|γ₁⟩_R

Where:
- |γ₀⟩, |γ₁⟩ are unit vectors (any quantum states of system R)
- α, β are complex coefficients with |α|² + |β|² = 1
- **Any** two-qubit entangled state can be written this way

### Complete initial state:
|π₀⟩ = |φ⁺⟩_BA ⊗ (α|0⟩_Q|γ₀⟩_R + β|1⟩_Q|γ₁⟩_R)

**Expanded**:
= (α|0⟩_B|γ₀⟩_R|00⟩_AQ + α|1⟩_B|γ₀⟩_R|10⟩_AQ + β|0⟩_B|γ₁⟩_R|01⟩_AQ + β|1⟩_B|γ₁⟩_R|11⟩_AQ)/√2

## Protocol Steps (Same as Before)

### After CNOT(Q,A):
|π₁⟩ = (α|0⟩_B|γ₀⟩_R|00⟩_AQ + α|1⟩_B|γ₀⟩_R|10⟩_AQ + β|0⟩_B|γ₁⟩_R|11⟩_AQ + β|1⟩_B|γ₁⟩_R|01⟩_AQ)/√2

### After Hadamard on Q:
|π₂⟩ = **(1/2)[(α|0⟩_B|γ₀⟩_R + β|1⟩_B|γ₁⟩_R)|00⟩_AQ + (α|0⟩_B|γ₀⟩_R - β|1⟩_B|γ₁⟩_R)|01⟩_AQ + (α|1⟩_B|γ₀⟩_R + β|0⟩_B|γ₁⟩_R)|10⟩_AQ + (α|1⟩_B|γ₀⟩_R - β|0⟩_B|γ₁⟩_R)|11⟩_AQ]**

## Bob's Corrections (Same Logic)

| Alice's measurement | Bob's (B,R) state before correction | Bob applies | Final (B,R) state |
|-------------------|-----------------------------------|-------------|------------------|
| (0,0) | α\|0⟩\|γ₀⟩ + β\|1⟩\|γ₁⟩ | I | **α\|0⟩\|γ₀⟩ + β\|1⟩\|γ₁⟩** ✓ |
| (0,1) | α\|0⟩\|γ₀⟩ - β\|1⟩\|γ₁⟩ | Z | **α\|0⟩\|γ₀⟩ + β\|1⟩\|γ₁⟩** ✓ |
| (1,0) | α\|1⟩\|γ₀⟩ + β\|0⟩\|γ₁⟩ | X | **α\|0⟩\|γ₀⟩ + β\|1⟩\|γ₁⟩** ✓ |
| (1,1) | α\|1⟩\|γ₀⟩ - β\|0⟩\|γ₁⟩ | XZ | **α\|0⟩\|γ₀⟩ + β\|1⟩\|γ₁⟩** ✓ |

## Final Result

**Perfect entanglement transfer**: α|0⟩|γ₀⟩ + β|1⟩|γ₁⟩

- **B is now entangled with R** exactly as Q was originally
- **All correlations preserved** - R doesn't even "know" the switch happened
- **|γ₀⟩ and |γ₁⟩ "come along for the ride"** - unchanged throughout

## Key Insights

### 1. Perfect Quantum Channel
Teleportation implements a **perfect, noiseless quantum channel**:
- **Input**: Q entangled with R
- **Output**: B entangled with R (identical relationship)

### 2. Universal Property
If teleportation works for **any single qubit**, it automatically works for **any entangled qubit**:
- The protocol acts like **identity operation** on the quantum state
- External entanglements are **automatically preserved**

### 3. No Special Cases Needed
- **Same protocol** works for isolated qubits AND entangled qubits
- **Same classical communication** (just 2 bits)
- **Same success probability** (deterministic after corrections)

## Applications

This general property makes teleportation incredibly powerful:
- **Quantum networks**: Move qubits while preserving network entanglement
- **Distributed computing**: Relocate qubits without breaking quantum algorithms
- **Error correction**: Move logical qubits between physical locations
- **Quantum internet**: Maintain end-to-end entanglement across hops

**Bottom line**: Teleportation is truly a **perfect quantum communication channel** - it works exactly the same whether the qubit is isolated or maximally entangled!