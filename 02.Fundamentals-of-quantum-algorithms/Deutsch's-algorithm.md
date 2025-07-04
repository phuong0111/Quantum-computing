# Deutsch problem: Complete Analysis

## 1. Problem Statement

Given a **black box quantum oracle** that implements a function:

$$f: \{0,1\}^n \to \{0,1\}$$

- **Input**: $n$-bit binary values
- **Output**: Single bit (0 or 1) for each input

The function is guaranteed to be either:

- **Constant**: Returns 0 for all inputs OR returns 1 for all inputs
- **Balanced**: Returns 1 for exactly half the inputs and 0 for the other half

**Task**: Determine whether the function is **constant** or **balanced** using the oracle.

**Classical Complexity**: Classical algorithms require up to $2^{n-1} + 1$ evaluations in the worst case (deterministic) or still $2^{n-1} + 1$ for zero error (randomized). Best case is 2 queries if the function is balanced and first two outputs differ.

## 2. Quantum Oracle Implementation

For quantum circuits, classical query gates don't work because they would be **non-unitary** for some functions $f$. Instead, we use **unitary query gates** that operate on standard basis states as:

$$U_f |x\rangle|y\rangle = |x\rangle|y \oplus f(x)\rangle$$

Where:

- $|x\rangle$: Input register ($n$ qubits)
- $|y\rangle$: Output register (1 qubit)
- $\oplus$: XOR operation
- $f(x)$: Function evaluation

**Key Properties:**

- **Unitary**: $U_f$ is always reversible ($U_f^\dagger = U_f$)
- **Preserves input**: The $x$ register remains unchanged
- **Controlled output**: The $y$ register is flipped based on $f(x)$

## 3. Deutsch-Jozsa Quantum Circuit

The quantum circuit for Deutsch-Jozsa algorithm:

```graph
|0⟩ ——[H]——————[Uf]——————[H]——[📊] → { 0 f is constant
                                     { 1 f is balanced
|1⟩ ——[H]————————————————————————————
```

**Circuit Components:**

- **H**: Hadamard gates creating superposition
- **$U_f$**: Quantum oracle implementing function $f$
- **📊**: Measurement on top qubit

## 4. Algorithm Analysis

### 4.1 Initial State

$$|\psi_0\rangle = |1\rangle|0\rangle$$

### 4.2 After Initial Hadamards

$$|\psi_1\rangle = |-\rangle|+\rangle = \frac{1}{2}(|0\rangle-|1\rangle)|0\rangle + \frac{1}{2}(|0\rangle-|1\rangle)|1\rangle$$

### 4.3 After Oracle $U_f$

$$|\psi_2\rangle = \frac{1}{2}(|0\oplus f(0)\rangle-|1\oplus f(0)\rangle)|0\rangle + \frac{1}{2}(|0\oplus f(1)\rangle-|1\oplus f(1)\rangle)|1\rangle$$

Using the identity: $|0\oplus a\rangle-|1\oplus a\rangle = (-1)^a(|0\rangle-|1\rangle)$

$$|\psi_2\rangle = (-1)^{f(0)}|-\rangle\frac{|0\rangle + (-1)^{f(0)\oplus f(1)}|1\rangle}{2}$$

This simplifies to:

$$|\psi_2\rangle = \begin{cases}
(-1)^{f(0)}|-\rangle|+\rangle & \text{if } f(0)\oplus f(1) = 0 \text{ (constant)} \\
(-1)^{f(0)}|-\rangle|-\rangle & \text{if } f(0)\oplus f(1) = 1 \text{ (balanced)}
\end{cases}$$

### 4.4 After Final Hadamard
$$|\psi_3\rangle = \begin{cases}
(-1)^{f(0)}|-\rangle|0\rangle & \text{if } f \text{ is constant} \\
(-1)^{f(0)}|-\rangle|1\rangle & \text{if } f \text{ is balanced}
\end{cases}$$

**Measurement Result:**
- **0**: Function is constant
- **1**: Function is balanced

## 5. Phase Kickback Phenomenon

**Key Insight**: Although $U_f$ acts on the bottom qubit, the phase information "kicks back" to the top qubit due to entanglement.

**Mathematical Foundation:**
$$U_f(|-\rangle|a\rangle) = (X^{f(a)}|-\rangle)|a\rangle = (-1)^{f(a)}|-\rangle|a\rangle$$

This works because $X|-\rangle = -|-\rangle$ ($|-\rangle$ is an eigenvector of $X$ with eigenvalue $-1$).

## 6. Multi-Qubit Generalization

For $n$-qubit functions, the Deutsch-Jozsa algorithm extends naturally:

### 6.1 Initial State
$$|\psi_0\rangle = |0\rangle^{\otimes n}|1\rangle$$

### 6.2 After Initial Hadamards
$$|\psi_1\rangle = \frac{1}{\sqrt{2^n}}\sum_{x \in \{0,1\}^n} |x\rangle \otimes |-\rangle$$

### 6.3 After Oracle
$$|\psi_2\rangle = \frac{1}{\sqrt{2^n}}\sum_{x \in \{0,1\}^n} (-1)^{f(x)}|x\rangle \otimes |-\rangle$$

### 6.4 After Final Hadamards
Using the multi-qubit Hadamard transform:
$$H^{\otimes n}|x\rangle = \frac{1}{\sqrt{2^n}}\sum_{y \in \{0,1\}^n} (-1)^{x \cdot y}|y\rangle$$

The final state becomes:
$$|\psi_3\rangle = \frac{1}{2^n}\sum_{x \in \{0,1\}^n}\sum_{y \in \{0,1\}^n} (-1)^{f(x) + x \cdot y}|y\rangle \otimes |-\rangle$$

### 6.5 Measurement Analysis

The amplitude for measuring $|0\rangle^{\otimes n}$ is:
$$A_{00...0} = \frac{1}{2^n}\sum_{x \in \{0,1\}^n} (-1)^{f(x)}$$

This gives:
$$|A_{00...0}|^2 = \begin{cases}
1 & \text{if } f \text{ is constant} \\
0 & \text{if } f \text{ is balanced}
\end{cases}$$

## 7. Quantum Solution Summary

- **Single evaluation** of $f$ (compared to up to $2^{n-1} + 1$ classical evaluations)
- **Always correct** (no probability of error)
- **Exponential speedup** over classical approaches: $O(1)$ vs $O(2^n)$

## 8. Key Mathematical Tools

### 8.1 XOR Distributive Property
$$(s \cdot x) \oplus (y \cdot x) = (s \oplus y) \cdot x$$

### 8.2 Phase Factor Properties
$$(-1)^k = \begin{cases}
+1 & \text{if } k \text{ is even} \\
-1 & \text{if } k \text{ is odd}
\end{cases}$$

### 8.3 Hadamard Transform Formula
$$H^{\otimes n}|x\rangle = \frac{1}{\sqrt{2^n}}\sum_{y \in \{0,1\}^n} (-1)^{x \cdot y}|y\rangle$$

These mathematical foundations enable the quantum interference patterns that give the Deutsch-Jozsa algorithm its exponential advantage over classical approaches.
