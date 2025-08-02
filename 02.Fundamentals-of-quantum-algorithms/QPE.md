I'll explain exactly how the inverse QFT transforms the "before" state to the "after" state.

## The Inverse QFT Operation

The inverse QFT is defined as:
$$\text{QFT}^{-1}_{2^m} = \frac{1}{\sqrt{2^m}} \sum_{x,y=0}^{2^m-1} \omega_{2^m}^{-xy} |y⟩⟨x|$$

Note the **negative sign** in the exponent compared to the forward QFT.

## Step-by-Step Transformation

### Starting State (before inverse QFT):
$$|\psi⟩ \otimes \frac{1}{\sqrt{2^m}} \sum_{x=0}^{2^m-1} e^{2\pi i x\theta} |x⟩$$

### Applying the Inverse QFT:
The inverse QFT only acts on the second register (the m-qubit register), so:

$$|\psi⟩ \otimes \left(\text{QFT}^{-1}_{2^m} \cdot \frac{1}{\sqrt{2^m}} \sum_{x=0}^{2^m-1} e^{2\pi i x\theta} |x⟩\right)$$

### Substituting the QFT^(-1) definition:
$$|\psi⟩ \otimes \left(\frac{1}{\sqrt{2^m}} \sum_{x,y=0}^{2^m-1} \omega_{2^m}^{-xy} |y⟩⟨x| \cdot \frac{1}{\sqrt{2^m}} \sum_{x'=0}^{2^m-1} e^{2\pi i x'\theta} |x'⟩\right)$$

### Using the orthogonality ⟨x|x'⟩ = δ_{x,x'}:
$$|\psi⟩ \otimes \frac{1}{2^m} \sum_{x,y=0}^{2^m-1} \omega_{2^m}^{-xy} \cdot e^{2\pi i x\theta} |y⟩$$

### Substituting ω_{2^m} = e^{2πi/2^m}:
$$|\psi⟩ \otimes \frac{1}{2^m} \sum_{x,y=0}^{2^m-1} e^{-2\pi i xy/2^m} \cdot e^{2\pi i x\theta} |y⟩$$

### Combining the exponentials:
$$|\psi⟩ \otimes \frac{1}{2^m} \sum_{y=0}^{2^m-1} \sum_{x=0}^{2^m-1} e^{2\pi i x(\theta - y/2^m)} |y⟩$$

## Key Steps in the Transformation:

1. **QFT^(-1) acts as a linear operator**: It transforms each basis state |x⟩ into a superposition over all |y⟩ states

2. **Phase accumulation**: Each |x⟩ contributes to every |y⟩ with amplitude proportional to ω_{2^m}^{-xy}

3. **Interference**: The original phase e^{2πixθ} from each |x⟩ interferes with the QFT transformation phases

4. **Result**: The final amplitude for each |y⟩ is the sum over all x of the combined phase factors

## The Physical Meaning:

The transformation essentially **"decodes" the phase information**:
- **Before**: Phase θ was encoded in the relative phases between different |x⟩ states
- **After**: This phase information is converted into probability amplitudes for different |y⟩ outcomes
- **Peak probability**: Occurs when y/2^m ≈ θ, where the phase factors e^{2πix(θ - y/2^m)} ≈ 1 and add constructively

This is why measuring the final state gives us an estimate of θ encoded in the binary representation of the measurement outcome y.