# Deutsch-Jozsa Problem and Hadamard Gate Analysis

## 1. Problem Statement

Given a **black box quantum oracle** that implements a function:
$$f: \{0,1\}^n \to \{0,1\}$$

The function is guaranteed to be either:

- **Constant**: Returns 0 for all inputs OR returns 1 for all inputs
- **Balanced**: Returns 1 for exactly half the inputs and 0 for the other half

**Task**: Determine whether the function is **constant** or **balanced** using the oracle.

**Classical Complexity**: Classical algorithms require up to $2^{n-1} + 1$ evaluations in the worst case.

## 2. Quantum Oracle Implementation

The quantum oracle operates as:
$$U_f |x\rangle|y\rangle = |x\rangle|y \oplus f(x)\rangle$$

Where:

- $|x\rangle$: Input register (n qubits)
- $|y\rangle$: Output register (1 qubit)
- $\oplus$: XOR operation

## 3. Hadamard Gate Foundation

### 3.1 Matrix Representation

$$H = \begin{pmatrix}
\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} \\
\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}
\end{pmatrix}$$

### 3.2 Action on Basis States

**Individual transformations:**
$$H|0\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle$$
$$H|1\rangle = \frac{1}{\sqrt{2}}|0\rangle - \frac{1}{\sqrt{2}}|1\rangle$$

### 3.3 General Formula

These can be unified into a single expression:
$$H|a\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}(-1)^a|1\rangle = \frac{1}{\sqrt{2}} \sum_{b \in \{0,1\}} (-1)^{ab}|b\rangle$$

**Verification:**
- For $a = 0$: $(-1)^0 = 1 \rightarrow H|0\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle$ ✓
- For $a = 1$: $(-1)^1 = -1 \rightarrow H|1\rangle = \frac{1}{\sqrt{2}}|0\rangle - \frac{1}{\sqrt{2}}|1\rangle$ ✓

### 3.4 Significance

This compact formula $H|a\rangle = \frac{1}{\sqrt{2}} \sum_{b \in \{0,1\}} (-1)^{ab}|b\rangle$ is crucial because:
- **Generalizable**: Extends naturally to multiple qubits
- **Phase encoding**: The $(-1)^{ab}$ terms capture essential phase relationships
- **Algorithmic insight**: Enables mathematical analysis of quantum interference patterns

### 3.5 Multi-Qubit Hadamard Transform

Now suppose that instead of just a single qubit we have $n$ qubits, and a Hadamard operation is performed on each. The combined operation on the $n$ qubits is described by the tensor product $H \otimes \cdots \otimes H$ ($n$ times), which we write as $H^{\otimes n}$ for succinctness and clarity. Using the formula from above, followed by expanding and then simplifying, we can express the action of this combined operation on the standard basis states of $n$ qubits like this:

$$H^{\otimes n}|x_{n-1}\cdots x_1 x_0\rangle = (H|x_{n-1}\rangle) \otimes \cdots \otimes (H|x_0\rangle)$$

$$= \left(\frac{1}{\sqrt{2}}\sum_{y_{n-1} \in \Sigma}(-1)^{x_{n-1}y_{n-1}}|y_{n-1}\rangle\right) \otimes \cdots \otimes \left(\frac{1}{\sqrt{2}}\sum_{y_0 \in \Sigma}(-1)^{x_0 y_0}|y_0\rangle\right)$$

$$= \frac{1}{\sqrt{2^n}}\sum_{y_{n-1}\cdots y_0 \in \Sigma^n}(-1)^{x_{n-1}y_{n-1} + \cdots + x_0 y_0}|y_{n-1}\cdots y_0\rangle$$

Here, by the way, we're writing binary strings of length $n$ as $x_{n-1}\cdots x_0$ and $y_{n-1}\cdots y_0$, following the same numbering convention used in Qiskit.

### 3.6 Deutsch-Jozsa Algorithm Analysis

This formula provides us with a useful tool for analyzing the quantum circuit above. After the first layer of Hadamard gates is performed, the state of the $n+1$ qubits (including the leftmost/bottom qubit, which is treated separately from the rest) is:

$$(H|1\rangle)(H^{\otimes n}|0\cdots 0\rangle) = |-\rangle \otimes \frac{1}{\sqrt{2^n}}\sum_{x_{n-1}\cdots x_0 \in \Sigma^n}|x_{n-1}\cdots x_0\rangle$$

When the $U_f$ operation is performed, this state is transformed into:

$$|-\rangle \otimes \frac{1}{\sqrt{2^n}}\sum_{x_{n-1}\cdots x_0 \in \Sigma^n}(-1)^{f(x_{n-1}\cdots x_0)}|x_{n-1}\cdots x_0\rangle$$

through exactly the same phase kick-back phenomenon that we saw in the analysis of Deutsch's algorithm.

Then the second layer of Hadamard gates is performed, which (by the same formula as above) transforms this state into:

$$|-\rangle \otimes \frac{1}{\sqrt{2^n}}\sum_{x_{n-1}\cdots x_0 \in \Sigma^n}\sum_{y_{n-1}\cdots y_0 \in \Sigma^n}(-1)^{f(x_{n-1}\cdots x_0) + x_{n-1}y_{n-1} + \cdots + x_0 y_0}|y_{n-1}\cdots y_0\rangle$$

This expression looks somewhat complicated, and little can be concluded about the probabilities to obtain different measurement outcomes without more information about the function $f$.

Fortunately, we just need to know the probability that every one of the measurement outcomes is $0$ — because that's the probability that the algorithm determines that $f$ is constant — and this probability has a simple formula.

$$\left|\frac{1}{\sqrt{2^n}}\sum_{x_{n-1}\cdots x_0 \in \Sigma^n}(-1)^{f(x_{n-1}\cdots x_0)}\right|^2 = \begin{cases}
1 & \text{if } f \text{ is constant} \\
0 & \text{if } f \text{ is balanced}
\end{cases}$$

In greater detail, if $f$ is constant, then either $f(x_{n-1}\cdots x_0) = 0$ for every string $x_{n-1}\cdots x_0$, in which case the value of the sum is $2^n$, or $f(x_{n-1}\cdots x_0) = 1$ for every string $x_{n-1}\cdots x_0$, in which case the value of the sum is $-2^n$. Dividing by $\sqrt{2^n}$ and taking the square of the absolute value yields $1$.

If, on the other hand, $f$ is balanced, then $f$ takes the value $0$ on half of the strings $x_{n-1}\cdots x_0$ and the value $1$ on the other half, so the $+1$ terms and $-1$ terms in the sum cancel and we're left with the value $0$.

So, we conclude that the algorithm operates correctly provided that the promise is fulfilled.
