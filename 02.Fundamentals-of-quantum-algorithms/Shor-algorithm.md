# The Order-Finding Problem

## Basic Number Theory

To explain the order-finding problem and how it can be solved using phase estimation, we begin with some basic number theory concepts.

For any positive integer $N$, define the set $\mathbb{Z}_N$ as:

$$\mathbb{Z}_N = \{0, 1, \ldots, N-1\}$$

For example:
- $\mathbb{Z}_1 = \{0\}$
- $\mathbb{Z}_2 = \{0, 1\}$ 
- $\mathbb{Z}_3 = \{0, 1, 2\}$

We can perform arithmetic operations on $\mathbb{Z}_N$ (addition and multiplication) by always taking results modulo $N$. This keeps us within the set and turns $\mathbb{Z}_N$ into a **ring**.

For example, in $\mathbb{Z}_7$:
$$3 \cdot 5 = 15 \equiv 1 \pmod{7}$$

## The Group $\mathbb{Z}_N^*$

Among the $N$ elements of $\mathbb{Z}_N$, the elements $a \in \mathbb{Z}_N$ that satisfy $\gcd(a,N) = 1$ are special:

$$\mathbb{Z}_N^* = \{a \in \mathbb{Z}_N : \gcd(a,N) = 1\}$$

Under multiplication, $\mathbb{Z}_N^*$ forms an **abelian group**. A fundamental property is that for any element $a \in \mathbb{Z}_N^*$, repeatedly multiplying $a$ by itself will eventually yield $1$.

### Example with $N = 21$

$$\mathbb{Z}_{21}^* = \{1, 2, 4, 5, 8, 10, 11, 13, 16, 17, 19, 20\}$$

The smallest powers that give $1$ are:
- $1^1 = 1$
- $8^2 = 1$ 
- $16^3 = 1$
- $2^6 = 1$
- $10^6 = 1$
- $17^6 = 1$
- $4^3 = 1$
- $11^6 = 1$
- $19^6 = 1$
- $5^6 = 1$
- $13^2 = 1$
- $20^2 = 1$

## The Order-Finding Problem

**Problem Statement:**
- **Input:** Positive integers $N$ and $a$ satisfying $\gcd(N,a) = 1$
- **Output:** The smallest positive integer $r$ such that $a^r \equiv 1 \pmod{N}$

This number $r$ is called the **order** of $a$ modulo $N$.

## Connection to Phase Estimation

Consider the operation on a quantum system whose classical states correspond to $\mathbb{Z}_N$:

$$M_a |x\rangle = |ax \bmod N\rangle \quad \text{for each } x \in \mathbb{Z}_N$$

### Example: $N = 15$, $a = 2$

$$\begin{align}
M_2|0\rangle &= |0\rangle & M_2|5\rangle &= |10\rangle & M_2|10\rangle &= |5\rangle \\
M_2|1\rangle &= |2\rangle & M_2|6\rangle &= |12\rangle & M_2|11\rangle &= |7\rangle \\
M_2|2\rangle &= |4\rangle & M_2|7\rangle &= |14\rangle & M_2|12\rangle &= |9\rangle \\
M_2|3\rangle &= |6\rangle & M_2|8\rangle &= |1\rangle & M_2|13\rangle &= |11\rangle \\
M_2|4\rangle &= |8\rangle & M_2|9\rangle &= |3\rangle & M_2|14\rangle &= |13\rangle
\end{align}$$

## Properties of $M_a$

The operation $M_a$ is **unitary** when $\gcd(a,N) = 1$ because:
1. It's a permutation of basis states (hence a permutation matrix)
2. It's invertible: $M_{a^{-1}} M_a = M_1 = I$

## Eigenvectors and Eigenvalues

### First Eigenvector

$$|ψ_0\rangle = \frac{|1\rangle + |a\rangle + \cdots + |a^{r-1}\rangle}{\sqrt{r}}$$

This has eigenvalue $1$ because:

$$M_a|ψ_0\rangle = \frac{|a\rangle + \cdots + |a^{r-1}\rangle + |a^r\rangle}{\sqrt{r}} = \frac{|a\rangle + \cdots + |a^{r-1}\rangle + |1\rangle}{\sqrt{r}} = |ψ_0\rangle$$

Since $a^r = 1$, each state $|a^k\rangle$ shifts to $|a^{k+1}\rangle$, and $|a^{r-1}\rangle$ cycles back to $|1\rangle$.

### Additional Eigenvectors

For any $j \in \{0, \ldots, r-1\}$:

$$|ψ_j\rangle = \frac{1}{\sqrt{r}} \sum_{k=0}^{r-1} ω_r^{-jk} |a^k\rangle$$

where $ω_r = e^{2πi/r}$.

This is an eigenvector with eigenvalue $ω_r^j$:

$$M_a|ψ_j\rangle = ω_r^j |ψ_j\rangle$$

### Verification

$$M_a|ψ_j\rangle = \sum_{k=0}^{r-1} ω_r^{-jk} M_a|a^k\rangle = \sum_{k=0}^{r-1} ω_r^{-jk} |a^{k+1}\rangle$$

Reindexing and using the periodicity properties:

$$= ω_r^j \sum_{k=0}^{r-1} ω_r^{-jk} |a^k\rangle = ω_r^j |ψ_j\rangle$$

The eigenvalues $ω_r^j = e^{2πij/r}$ encode the order $r$ in their phases, making this problem amenable to **quantum phase estimation**!

# Order Finding Through Phase Estimation

## Implementation of $M_a$

To solve the order-finding problem for a given choice of $a \in \mathbb{Z}_N^*$, we apply the phase-estimation procedure to the operation $M_a$.

For implementation, we need to efficiently construct quantum circuits for $M_a$, $M_{a^2}$, $M_{a^4}$, $M_{a^8}$, and so on.

### Binary Encoding

We use binary notation to encode numbers between $0$ and $N-1$. The number of bits needed is:

$$n = \lceil \lg(N-1) \rceil = \lfloor \log_2(N-1) \rfloor + 1$$

For example, if $N = 21$, we have $n = 5$ bits.

### Precise Definition of $M_a$

The $n$-qubit operation $M_a$ is defined as:

$$M_a |x\rangle = \begin{cases}
|ax \bmod N\rangle & \text{if } 0 \leq x < N \\
|x\rangle & \text{if } N \leq x < 2^n
\end{cases}$$

### Circuit Construction for $M_a$

We can build a quantum circuit for $M_a$ with cost $O(n^2)$ using the following three-step process:

1. **Step 1:** Build a circuit for 
   $$|x\rangle |y\rangle \mapsto |x\rangle |y \oplus f_a(x)\rangle$$
   where 
   $$f_a(x) = \begin{cases}
   ax \bmod N & \text{if } 0 \leq x < N \\
   x & \text{if } N \leq x < 2^n
   \end{cases}$$

2. **Step 2:** Swap the two $n$-qubit systems using $n$ swap gates

3. **Step 3:** Build a circuit for 
   $$|x\rangle |y\rangle \mapsto |x\rangle |y \oplus f_{a^{-1}}(x)\rangle$$

The complete transformation is:
$$|x\rangle |0^n\rangle \xrightarrow{\text{step 1}} |x\rangle |f_a(x)\rangle \xrightarrow{\text{step 2}} |f_a(x)\rangle |x\rangle \xrightarrow{\text{step 3}} |f_a(x)\rangle |0^n\rangle$$

### Powers of $M_a$

For $M_{a^2}$, $M_{a^4}$, $M_{a^8}$, etc., we use the same method but replace $a$ with $a^2$, $a^4$, $a^8$, etc., as elements of $\mathbb{Z}_N^*$.

The key insight is that we compute $b = a^k \in \mathbb{Z}_N^*$ **classically** and then use the circuit for $M_b$, rather than iterating the circuit for $M_a$ $k$ times.

Powers are computed using **modular exponentiation**:
- We need power-of-2 powers: $a^2, a^4, \ldots, a^{2^{m-1}} \in \mathbb{Z}_N^*$
- Obtained by iteratively squaring $m-1$ times
- Each squaring can be performed by a Boolean circuit of size $O(n^2)$

## Solution with a Convenient Eigenvector

### Using $|\psi_1\rangle$

Suppose we run phase estimation on $M_a$ using the eigenvector $|\psi_1\rangle$. The corresponding eigenvalue is:

$$\omega_r = e^{2\pi i \cdot 1/r}$$

That is, $\omega_r = e^{2\pi i \theta}$ for $\theta = 1/r$.

### Phase Estimation Result

With $m$ control qubits, we obtain a number $y \in \{0, \ldots, 2^m - 1\}$. We take $y/2^m$ as our estimate for $\theta = 1/r$.

To find $r$, we compute:
$$\left\lfloor \frac{2^m}{y} + \frac{1}{2} \right\rfloor$$

### Example

Let $r = 6$ and $m = 5$ control bits. The best 5-bit approximation to $1/r = 1/6$ is $5/32$.

If we obtain $y = 5$:
$$\frac{2^m}{y} = \frac{32}{5} = 6.4$$

Rounding gives $6$, which is correct.

### Precision Requirements

To distinguish $1/r$ from nearby fractions like $1/(r+1)$, we need:

$$\left| \frac{y}{2^m} - \frac{1}{r} \right| < \frac{1}{2r(r+1)}$$

Since we don't know $r$ beforehand, we use $r < N$ and require:

$$\left| \frac{y}{2^m} - \frac{1}{r} \right| \leq \frac{1}{2N^2}$$

Taking $m = 2\lceil \lg(N) \rceil + 1$ ensures sufficient precision.

## General Solution

### Using Arbitrary Eigenvectors

If we use eigenvector $|\psi_k\rangle$ instead of $|\psi_1\rangle$, phase estimation gives an approximation:

$$\frac{y}{2^m} \approx \frac{k}{r}$$

### Continued Fractions Algorithm

**Fact:** Given an integer $N \geq 2$ and a real number $\alpha \in (0,1)$, there is at most one choice of integers $u, v \in \{0, \ldots, N-1\}$ with $v \neq 0$ and $\gcd(u,v) = 1$ satisfying:

$$\left| \alpha - \frac{u}{v} \right| < \frac{1}{2N^2}$$

The continued fractions algorithm finds $u$ and $v$, giving us $\frac{u}{v} = \frac{k}{r}$ in lowest terms.

### Multiple Samples Strategy

- Run the algorithm several times to get different values $k/r$
- The denominators $v$ divide $r$
- Take the **least common multiple** of all observed denominators
- This gives $r$ with high probability

### Using $|1\rangle$ Instead of Eigenvectors

Key insight: We don't need to prepare specific eigenvectors! Instead, we use:

$$|1\rangle = \frac{1}{\sqrt{r}} \sum_{k=0}^{r-1} |\psi_k\rangle$$

This gives the same measurement statistics as choosing $k \in \{0, \ldots, r-1\}$ uniformly at random.

### Final State After Phase Estimation

When using $|1\rangle$, after the inverse QFT we get:

$$\frac{1}{\sqrt{r}} \sum_{k=0}^{r-1} |\psi_k\rangle |\gamma_k\rangle$$

where

$$|\gamma_k\rangle = \frac{1}{\sqrt{2^m}} \sum_{y=0}^{2^m-1} \sum_{x=0}^{2^m-1} e^{2\pi i x(k/r - y/2^m)} |y\rangle$$

Measurement of the top $m$ qubits yields an approximation $y/2^m$ to $k/r$ where $k$ is chosen uniformly at random.

## Total Cost Analysis

### Quantum Circuit Cost
- Each controlled-unitary $M_{a^k}$: $O(n^2)$
- Number of controlled-unitaries: $m = O(n)$
- Total controlled-unitary cost: $O(n^3)$
- Hadamard gates: $O(n)$
- Inverse QFT: $O(n^2)$

**Total quantum cost: $O(n^3)$**

### Classical Preprocessing Cost
- Computing powers $a^k$ in $\mathbb{Z}_N$ for $k = 2, 4, 8, \ldots, 2^{m-1}$
- Continued fractions algorithm
- **Total classical cost: $O(n^3)$**

### Overall Complexity
The order-finding algorithm has **polynomial complexity** $O(n^3)$ where $n = O(\log N)$, making it efficient for large $N$.

This polynomial scaling is crucial for Shor's factoring algorithm, as it provides an exponential speedup over known classical methods for integer factorization.