# Grover's Algorithm Implementation Documentation

## 1. Grover Operator Construction

### 1.1 Grover Operator Property

```python
@property
def grover_operator(self) -> QuantumCircuit | None:
    """Get the Q operator, or Grover operator.
    
    If the Grover operator is not set, we try to build it from the A operator
    and objective_qubits. This only works if objective_qubits is a list of integers.
    
    Returns:
        The Grover operator, or None if neither the Grover operator nor the
        A operator is set.
    """
    if self._grover_operator is None:
        return GroverOperator(self.oracle, self.state_preparation)
    return self._grover_operator
```

#### Explanation

This property implements **lazy construction** of the Grover operator $\mathcal{Q}$, which is the core iterative component of Grover's quantum search algorithm.

**Algorithm breakdown:**

1. **Lazy initialization**: The Grover operator is only constructed when first accessed, not during `AmplificationProblem` initialization. This improves performance by avoiding unnecessary circuit construction.

2. **Conditional construction**: Checks if `_grover_operator` is already built:
   - If `None`: Creates a new `GroverOperator` instance using the oracle and state preparation
   - If exists: Returns the cached operator

3. **Input components**:
   - `self.oracle`: The phase oracle that marks solution states with a phase flip
   - `self.state_preparation`: The amplitude preparation operator (typically Hadamard gates for uniform superposition)

**Mathematical foundation:**

The Grover operator implements the unitary transformation:
$$\mathcal{Q} = -\mathcal{A}\mathcal{S}_0\mathcal{A}^{\dagger}\mathcal{S}_{\chi}$$

Where:
- $\mathcal{S}_{\chi}$: Phase oracle (reflection about marked states)
- $\mathcal{A}$: State preparation operator  
- $\mathcal{S}_0$: Zero reflection (reflection about $|0\rangle^{\otimes n}$)
- $\mathcal{A}^{\dagger}$: Inverse state preparation

**Physical interpretation:**

The Grover operator performs a **rotation in the 2D subspace** spanned by:
- $|\psi_{\text{good}}\rangle$: Superposition of all marked/solution states
- $|\psi_{\text{bad}}\rangle$: Superposition of all unmarked states

Each application of $\mathcal{Q}$ rotates the state vector closer to $|\psi_{\text{good}}\rangle$ by a fixed angle $\theta$, where $\sin^2(\theta/2) = M/N$ ($M$ = number of marked states, $N$ = total states).

**Usage pattern:**

```python
# Create amplification problem
oracle = PhaseOracle(expression='(A & B) | (C & D)')
problem = AmplificationProblem(oracle)

# Access Grover operator (triggers construction)
grover_op = problem.grover_operator

# Use in Grover algorithm iterations
for i in range(optimal_iterations):
    circuit.append(grover_op, qubits)
```

**Key advantages:**

1. **Memory efficiency**: Only constructs when needed
2. **Reusability**: Once built, can be reused multiple times
3. **Automatic composition**: Correctly combines oracle with diffusion operator
4. **Type safety**: Returns `QuantumCircuit` for direct circuit composition

The property ensures that accessing `problem.grover_operator` always returns a valid, ready-to-use quantum circuit implementing the complete Grover iteration.

# Grover Algorithm Implementation Documentation

## 2. Grover Algorithm Execution

### 2.1 Amplify Method

```python
def amplify(self, amplification_problem: AmplificationProblem) -> "GroverResult":
    """Run the Grover algorithm.

    Args:
        amplification_problem: The amplification problem.

    Returns:
        The result as a ``GroverResult``, where e.g. the most likely state can be queried
        as ``result.top_measurement``.

    Raises:
        ValueError: If sampler is not set.
        AlgorithmError: If sampler job fails.
        TypeError: If ``is_good_state`` is not provided and is required (i.e. when iterations
        is ``None`` or a ``list``)
    """
```

#### Explanation

This method implements the **main execution loop** of Grover's quantum search algorithm, iteratively applying the Grover operator with different iteration counts to find optimal solutions.

**Algorithm breakdown:**

### 2.1.1 Iteration Strategy Setup

```python
if isinstance(self._iterations, list):
    max_iterations = len(self._iterations)
    max_power = np.inf  # no cap on the power
    iterator: Iterator[int] = iter(self._iterations)
else:
    max_iterations = max(10, 2**amplification_problem.oracle.num_qubits)
    max_power = np.ceil(
        2 ** (len(amplification_problem.grover_operator.reflection_qubits) / 2)
    )
    iterator = self._iterations
```

**Two iteration modes:**

1. **Custom iteration list**: When `_iterations` is a list of specific iteration counts
   - Uses each value from the provided list
   - No theoretical limit on iteration count

2. **Automatic iteration strategy**: When `_iterations` is an iterator/generator
   - **Max iterations**: $\max(10, 2^n)$ where $n$ is number of oracle qubits
   - **Max power**: $\lceil 2^{m/2} \rceil$ where $m$ is number of reflection qubits
   - **Theoretical foundation**: Optimal Grover iterations ≈ $\frac{\pi}{4}\sqrt{2^n/M}$ where $M$ is number of solutions

### 2.1.2 Main Search Loop

```python
for _ in range(max_iterations):  # iterate at most to the max number of iterations
    # get next power and check if allowed
    power = next(iterator)
    
    if power > max_power:
        break
    
    iterations.append(power)  # store power
    
    # sample from [0, power) if specified
    if self._sample_from_iterations:
        power = algorithm_globals.random.integers(power)
```

**Iteration control:**
- **Power selection**: Gets next iteration count from iterator
- **Boundary check**: Stops if power exceeds theoretical optimum
- **Random sampling**: Optionally samples random iteration count ∈ [0, power) for robustness

### 2.1.3 Quantum Circuit Execution

```python
if self._sampler is not None:
    qc = self.construct_circuit(amplification_problem, power, measurement=True)
    job = self._sampler.run([qc])
    
    try:
        results = job.result()
    except Exception as exc:
        raise AlgorithmError("Sampler job failed.") from exc
    
    num_bits = len(amplification_problem.objective_qubits)
    circuit_results: dict[str, Any] | Statevector | np.ndarray = {
        np.binary_repr(k, num_bits): v for k, v in results.quasi_dists[0].items()
    }
    top_measurement, max_probability = max(
        circuit_results.items(), key=lambda x: x[1]
    )
```

**Execution steps:**

1. **Circuit construction**: Creates quantum circuit with `power` Grover operator applications
2. **Quantum execution**: Runs circuit on quantum sampler (simulator or hardware)
3. **Result processing**: 
   - Converts measurement outcomes to binary strings
   - Extracts most probable measurement outcome
   - Records probability distribution

**Mathematical operation**: Applies $\mathcal{Q}^{\text{power}}|\psi_0\rangle$ where:
- $\mathcal{Q}$: Grover operator
- $|\psi_0\rangle$: Initial uniform superposition
- **power**: Number of Grover iterations

### 2.1.4 Solution Validation

```python
# is_good_state arg must be provided if iterations arg is not an integer
if (
    self._iterations_arg is None or isinstance(self._iterations_arg, list)
) and amplification_problem.is_good_state is None:
    raise TypeError("An is_good_state function is required with the provided oracle")

# only check if top measurement is a good state if an is_good_state arg is provided
oracle_evaluation = amplification_problem.is_good_state(top_measurement)

if oracle_evaluation is True:
    break  # we found a solution
```

**Solution verification:**
- **Good state check**: Validates if measured state satisfies the search criteria
- **Early termination**: Stops search once valid solution is found
- **Efficiency**: Avoids unnecessary iterations when solution is discovered

### 2.1.5 Result Compilation

```python
result.iterations = iterations
result.top_measurement = top_measurement
result.assignment = amplification_problem.post_processing(top_measurement)
result.oracle_evaluation = oracle_evaluation
result.circuit_results = all_circuit_results
result.max_probability = max_probability

return result
```

**Output components:**
- **iterations**: List of iteration counts attempted
- **top_measurement**: Most probable bit string measured
- **assignment**: Post-processed solution (maps bits to variable names)
- **oracle_evaluation**: Boolean indicating if solution is valid
- **circuit_results**: Complete probability distributions from each run
- **max_probability**: Highest measurement probability achieved

**Usage example:**
```python
# Setup
oracle = PhaseOracle(expression='(A & B) | (C & D)')
problem = AmplificationProblem(oracle)
grover = Grover(sampler=Sampler())

# Execute
result = grover.amplify(problem)

# Access results
print(f"Solution: {result.top_measurement}")
print(f"Variable assignment: {result.assignment}")
print(f"Success probability: {result.max_probability}")
```

**Key advantages:**
1. **Adaptive search**: Tries multiple iteration counts for robustness
2. **Early termination**: Stops when valid solution found
3. **Complete results**: Returns full probability distributions and metadata
4. **Error handling**: Robust exception handling for quantum execution failures

The method implements a sophisticated search strategy that balances theoretical optimality with practical robustness for finding solutions to Boolean satisfiability problems.