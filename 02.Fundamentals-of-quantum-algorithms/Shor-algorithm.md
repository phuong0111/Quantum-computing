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