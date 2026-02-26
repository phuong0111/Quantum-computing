# All Formulas from "Beating the Photon-Number-Splitting Attack in Practical Quantum Cryptography"

## Equation (1) - Dephased coherent state
$$\rho_{\mu} = \frac{1}{2\pi}\int_0^{2\pi} |\sqrt{\mu}e^{i\theta}\rangle\langle\sqrt{\mu}e^{i\theta}| d\theta = \sum_n P_n(\mu)|n\rangle\langle n|$$

**Symbol Definitions:**
- $\rho_{\mu}$ = density matrix of dephased coherent state with average photon number μ
- $\mu$ = average photon number (non-negative real number)
- $\theta$ = random phase parameter (0 to 2π)
- $|\sqrt{\mu}e^{i\theta}\rangle$ = coherent state with amplitude $\sqrt{\mu}e^{i\theta}$
- $P_n(\mu)$ = probability of having n photons in coherent state
- $|n\rangle$ = n-photon Fock state
- $n$ = photon number (non-negative integer)

**Additional formula:** $P_n(\mu) = e^{-\mu}\frac{\mu^n}{n!}$ (Poisson distribution)

## Equation (2) - Assumptions
$$\mu' > \mu; \quad \mu'e^{-\mu'} > \mu e^{-\mu}$$

**Symbol Definitions:**
- $\mu'$ = average photon number for second coherent state (larger than μ)
- $\mu$ = average photon number for first coherent state
- $e$ = Euler's number (≈ 2.718)

## Equation (3) - Convex form of coherent state ρ_μ
$$\rho_{\mu} = e^{-\mu}|0\rangle\langle 0| + \mu e^{-\mu}|1\rangle\langle 1| + c\rho_c$$

**Symbol Definitions:**
- $\rho_{\mu}$ = density matrix of dephased coherent state with average photon number μ
- $e^{-\mu}$ = probability coefficient for vacuum state
- $|0\rangle\langle 0|$ = vacuum state projector (zero photons)
- $\mu e^{-\mu}$ = probability coefficient for single-photon state
- $|1\rangle\langle 1|$ = single-photon state projector
- $c$ = probability coefficient for multiphoton component
- $\rho_c$ = normalized multiphoton mixed state (2+ photons)

**Additional formula:** $c = 1 - e^{-\mu} - \mu e^{-\mu} > 0$

## Equation (4) - Definition of ρ_c
$$\rho_c = \frac{1}{c}\sum_{n=2}^{\infty} P_n(\mu)|n\rangle\langle n|$$

**Symbol Definitions:**
- $\rho_c$ = normalized density matrix for multiphoton states (n ≥ 2)
- $c$ = normalization constant (total probability of multiphoton states)
- $P_n(\mu)$ = Poisson probability for n photons
- $|n\rangle\langle n|$ = n-photon Fock state projector
- $n$ = photon number (starting from 2)

## Equation (5) - Convex form of coherent state ρ_μ'
$$\rho_{\mu'} = e^{-\mu'}|0\rangle\langle 0| + \mu'e^{-\mu'}|1\rangle\langle 1| + c \frac{\mu'^2 e^{-\mu'}}{\mu^2 e^{-\mu}} \rho_c + d\rho_d$$

**Symbol Definitions:**
- $\rho_{\mu'}$ = density matrix of dephased coherent state with average photon number μ'
- $e^{-\mu'}$ = probability coefficient for vacuum state from μ' pulse
- $\mu'e^{-\mu'}$ = probability coefficient for single-photon state from μ' pulse
- $c \frac{\mu'^2 e^{-\mu'}}{\mu^2 e^{-\mu}}$ = probability coefficient for $\rho_c$ component in μ' pulse
- $d$ = probability coefficient for additional multiphoton component $\rho_d$
- $\rho_d$ = additional normalized density operator for higher-order multiphoton states

**Additional formula:** $d = 1 - e^{-\mu'} - \mu'e^{-\mu'} - c \frac{\mu'^2 e^{-\mu'}}{\mu^2 e^{-\mu}} \ge 0$

## Equation (6) - Asymptotic condition
$$s_{\rho}(\mu) = s_{\rho}(\mu')$$

**Symbol Definitions:**
- $s_{\rho}(\mu)$ = counting rate (detection probability) for quantum state ρ from class $Y_{\mu}$
- $s_{\rho}(\mu')$ = counting rate for the same quantum state ρ from class $Y_{\mu'}$
- $\rho$ = arbitrary quantum state
- This equation states that asymptotically, Eve treats identical states the same regardless of which class they come from

## Equation (7) - Definition of Δ
$$\Delta = c \frac{s_c}{S_{\mu}}$$

**Symbol Definitions:**
- $\Delta$ = fraction of counts caused by multiphoton pulses in class $Y_{\mu}$ (security parameter)
- $c$ = probability of multiphoton component in coherent state μ
- $s_c$ = counting rate (detection probability) for multiphoton mixed state $\rho_c$
- $S_{\mu}$ = overall counting rate for all pulses in class $Y_{\mu}$

## Equation (8) - Counting rate for ρ_μ'
$$S_{\mu'} = e^{-\mu'}s_0 + \mu'e^{-\mu'}s_1 + c \frac{\mu'^2 e^{-\mu'}}{\mu^2 e^{-\mu}} s_c + ds_d$$

**Symbol Definitions:**
- $S_{\mu'}$ = overall counting rate for all pulses in class $Y_{\mu'}$
- $e^{-\mu'}$ = probability coefficient for vacuum component
- $s_0$ = counting rate for vacuum state (dark count rate)
- $\mu'e^{-\mu'}$ = probability coefficient for single-photon component
- $s_1$ = counting rate for single-photon state
- $c \frac{\mu'^2 e^{-\mu'}}{\mu^2 e^{-\mu}}$ = probability coefficient for $\rho_c$ component
- $s_c$ = counting rate for multiphoton mixed state $\rho_c$
- $d$ = probability coefficient for $\rho_d$ component
- $s_d$ = counting rate for additional multiphoton mixed state $\rho_d$

## Equation (9) - First inequality for s_c
$$cs_c \le \frac{\mu^2 e^{-\mu}}{\mu'^2 e^{-\mu'}} (S_{\mu'} - e^{-\mu'}s_0 - \mu'e^{-\mu'}s_1)$$

**Symbol Definitions:**
- $cs_c$ = weighted counting rate for multiphoton component
- $\frac{\mu^2 e^{-\mu}}{\mu'^2 e^{-\mu'}}$ = scaling factor relating μ and μ' coherent states
- $(S_{\mu'} - e^{-\mu'}s_0 - \mu'e^{-\mu'}s_1)$ = counting rate attributed to multiphoton components in $S_{\mu'}$

## Equation (10) - Hwang's result
$$cs_c \le \frac{\mu^2 e^{-\mu}}{\mu'^2 e^{-\mu'}} (S_{\mu'} - e^{-\mu'}s_0) \le \frac{\mu^2 e^{-\mu}}{\mu'^2 e^{-\mu'}} S_{\mu'}$$

**Symbol Definitions:**
- This is a cruder bound obtained by setting $s_1 \ge 0$ (ignoring the single-photon contribution)
- All symbols same as previous equations
- The second inequality comes from dropping the $e^{-\mu'}s_0$ term

## Equation (11) - Counting rate constraint for ρ_μ
$$e^{-\mu}s_0 + \mu e^{-\mu}s_1 + cs_c = S_{\mu}$$

**Symbol Definitions:**
- This equation decomposes the total counting rate $S_{\mu}$ into its components
- $e^{-\mu}s_0$ = contribution from vacuum component
- $\mu e^{-\mu}s_1$ = contribution from single-photon component  
- $cs_c$ = contribution from multiphoton component
- All other symbols as defined previously

## Equation (12) - Lower bound for s_1
$$s_1 \ge S_{\mu} - e^{-\mu}s_0 - cs_c > 0$$

**Symbol Definitions:**
- $s_1$ = counting rate for single-photon state (must be positive)
- $S_{\mu} - e^{-\mu}s_0 - cs_c$ = remaining counting rate after subtracting vacuum and multiphoton contributions
- This provides a non-trivial lower bound for $s_1$

## Equation (13) - Final bound for Δ
$$\Delta \le \frac{\mu}{\mu'-\mu} \left(\frac{\mu'e^{\mu}}{\mu e^{\mu'}} \frac{S_{\mu'}}{S_{\mu}} - 1\right) + \frac{\mu e^{-\mu}s_0}{\mu' S_{\mu}}$$

**Symbol Definitions:**
- $\Delta$ = upper bound for fraction of multiphoton counts in class $Y_{\mu}$
- $\frac{\mu}{\mu'-\mu}$ = scaling factor depending on the difference between μ and μ'
- $\frac{\mu'e^{\mu}}{\mu e^{\mu'}}$ = exponential scaling factor
- $\frac{S_{\mu'}}{S_{\mu}}$ = ratio of observed counting rates
- $\frac{\mu e^{-\mu}s_0}{\mu' S_{\mu}}$ = correction term accounting for dark counts
- This is the main result providing a tight security bound

## Equation (14) - Verification limit
$$\Delta = \frac{\mu(e^{\mu'-\mu}-1)}{\mu'-\mu}\bigg|_{\mu'-\mu \to 0} = \mu$$

**Symbol Definitions:**
- Left side: exact expression for Δ in limit where μ' approaches μ
- $e^{\mu'-\mu}$ = exponential of the difference
- $\bigg|_{\mu'-\mu \to 0}$ = limit notation as μ' approaches μ
- Right side: limiting value equal to μ
- This shows the bound approaches the ideal case when there's no Eve

## Equation (15) - Upper bound for Δ'
$$\Delta' \le 1 - \left(1-\Delta - \frac{s_1 \mu e^{-\mu}}{S_{\mu}} - \frac{s_0 e^{-\mu}}{S_{\mu}}\right) \frac{S_{\mu} e^{-\mu'}}{S_{\mu'} e^{-\mu}} - \frac{s_0 e^{-\mu'}}{S_{\mu'}}$$

**Symbol Definitions:**
- $\Delta'$ = upper bound for fraction of multiphoton counts in class $Y_{\mu'}$
- $\left(1-\Delta - \frac{s_1 \mu e^{-\mu}}{S_{\mu}} - \frac{s_0 e^{-\mu}}{S_{\mu}}\right)$ = fraction of single-photon counts in class $Y_{\mu}$
- $\frac{S_{\mu} e^{-\mu'}}{S_{\mu'} e^{-\mu}}$ = scaling factor for transferring bounds between classes
- $\frac{s_0 e^{-\mu'}}{S_{\mu'}}$ = dark count contribution in class $Y_{\mu'}$

## Equation (16) - Statistical fluctuation constraint (first form)
$$e^{-\mu}s_0 + \mu e^{-\mu}s_1 + cs_c = S_{\mu}$$

**Symbol Definitions:**
- Same as Equation (11) - this is the constraint equation for the non-asymptotic case
- All symbols have same meanings as before

## Equation (17) - Statistical fluctuation constraint (second form)
$$c s'_c \le \frac{\mu^2 e^{-\mu}}{\mu'^2 e^{-\mu'}} \times (S_{\mu'} - \mu'e^{-\mu'}s'_1 - e^{-\mu'}s'_0)$$

**Symbol Definitions:**
- $s'_c$ = counting rate for $\rho_c$ from class $Y_{\mu'}$ (with statistical fluctuations)
- $s'_1$ = counting rate for single-photon state from class $Y_{\mu'}$ (with fluctuations)
- $s'_0$ = dark count rate from class $Y_{\mu'}$ (with fluctuations)
- Primed variables account for the fact that Eve might treat identical states slightly differently due to statistical fluctuations

## Equation (18) - Non-asymptotic bound with fluctuations
$$\mu' e^\mu (1-r_c)\frac{\mu-1}{\mu} \Delta \le \mu e^{\mu'} S_{\mu'}/S_{\mu} - \mu'e^{\mu'} + [(\mu'-\mu)s_0 + r_1s_1 + r_0s_0]/S_{\mu}$$

**Symbol Definitions:**
- $(1-r_c)$ = statistical fluctuation factor for multiphoton counting rate
- $r_c$ = relative fluctuation parameter for $s_c$
- $r_1$ = relative fluctuation parameter for $s_1$  
- $r_0$ = relative fluctuation parameter for $s_0$
- $\frac{\mu-1}{\mu}$ = correction factor
- $[(\mu'-\mu)s_0 + r_1s_1 + r_0s_0]/S_{\mu}$ = fluctuation correction terms
- This provides security bounds accounting for finite statistics

## Additional Key Relations

### Channel transmittance condition for PNS attack
$$\eta < \frac{1-e^{-\mu} - \mu e^{-\mu}}{\mu}$$

**Symbol Definitions:**
- $\eta$ = overall channel transmittance (including detection efficiency)
- $1-e^{-\mu} - \mu e^{-\mu}$ = probability of multiphoton pulses
- This condition determines when photon-number-splitting attacks become feasible

### Probability bound for statistical fluctuations
$$P(|s_{p,a}-s_{p,b}| > \delta_p) < \exp\left(-\frac{1}{2}\delta_p^2 N_0 / \bar{s}_p^2\right)$$

**Symbol Definitions:**
- $P(\cdot)$ = probability
- $s_{p,a}$ = counting rate for first subset of pulses
- $s_{p,b}$ = counting rate for second subset of pulses
- $\delta_p$ = deviation threshold
- $N_0$ = minimum number of pulses in either subset
- $\bar{s}_p$ = average counting rate
- $\exp(\cdot)$ = exponential function
- This gives the probability that statistical fluctuations exceed a threshold

### Statistical requirement for exponential certainty
$$\frac{\delta_p^2 N_0}{\bar{s}_p^2} = 100$$

**Symbol Definitions:**
- This equation sets the requirement for achieving exponential security
- The value 100 ensures very high confidence in the bounds

### Relative fluctuation
$$r_p = \frac{\delta_p}{\bar{s}_p} = \frac{10}{\sqrt{N_0}}$$

**Symbol Definitions:**
- $r_p$ = relative fluctuation (fractional deviation)
- $10$ = numerical constant for high-confidence bounds
- $\sqrt{N_0}$ = square root of minimum pulse number

### Real fraction of multiphoton counts (no Eve)
$$\Delta_{\text{real}} = 1-e^{-\mu}$$ (when $\eta \ll 1$)

**Symbol Definitions:**
- $\Delta_{\text{real}}$ = true fraction of multiphoton counts when there's no eavesdropper
- $1-e^{-\mu}$ = probability of having one or more photons
- $\eta \ll 1$ = condition of very lossy channel

## Additional Notation Explanations

### Class Definitions:
- $Y_{\mu}$ = class of pulses with average photon number μ
- $Y_{\mu'}$ = class of pulses with average photon number μ'  
- $Y_0$ = class of vacuum pulses

### Subscript Conventions:
- $\Delta_H$ = result using Hwang's method
- $\Delta_R$ = real/true value without eavesdropper
- $\Delta_{W1}, \Delta_{W2}$ = Wang's bounds for different conditions
- $N_{\mu,1}, N_{\mu,c}$ = number of single-photon and multiphoton pulses in class $Y_{\mu}$