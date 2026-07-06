# Mock Exam 4 — solutions & grading rubric

**⚠️ Spoilers. Attempt `mock_exam_04.md` first.** Tutor: grade against this rubric;
verified numerically on 2026-07-06 (Q1: matrix-power identities and least-squares
realizability fits — misfit of the all-ones sequence by the anti-symmetric class
$\ge 1$ uniformly in $\omega$; Q2 flow on the part-4 dataset: $v^2 - \|w\|^2$ drift
$\sim 5\text{e-}6$ at Euler step $10^{-5}$, loss plateaus at exactly $0.5$;
Q3: Gaussian-KL Monte-Carlo agrees with $\|w\|^2/(2\sigma^2)$ to $10^{-3}$).

## Q1 — Linear RNNs: scalar state and anti-symmetric transitions (40)

**1. (10)** *Closed form (4 pts).* By induction on $t$:
$s_t(x) = \sum_{\tau=1}^{t} A^{t-\tau} B\, x_\tau$. Base: $s_1 = A s_0 + B x_1 =
A^0 B x_1$. Step: $s_t = A s_{t-1} + B x_t = \sum_{\tau \le t-1} A^{t-\tau} B x_\tau
+ A^0 B x_t$. Hence $h(x) = C^\top s_L(x) = \sum_{t=1}^{L} C^\top A^{L-t} B\, x_t$,
so $h$ realizes $a_t = C^\top A^{L-t} B$ and is a linear functional of $x$.
*Uniqueness (2 pts):* if $h(x) = \sum_t a_t x_t = \sum_t a'_t x_t$ for all $x$,
evaluate at $x = e_t$ to get $a_t = h(e_t) = a'_t$.
*Non-universality (4 pts):* $f(x) := x_1 x_2$ is continuous. Suppose $f \in
\mathcal{H}_d$ for some $d$; then $f(x) = \sum_t a_t x_t$ for some $a$. But
$f(e_1) = 0 \Rightarrow a_1 = 0$, $f(e_2) = 0 \Rightarrow a_2 = 0$, while
$f(e_1 + e_2) = 1 \ne a_1 + a_2 = 0$ — contradiction. Since $d$ was arbitrary,
$f \notin \mathcal{H}_d$ for every $d$. (Any correct witness earns full credit:
$x_1^2$ via homogeneity $f(2e_1) \ne 2f(e_1)$, $f \equiv 1$ via $h(0) = 0$, etc. —
but the non-membership must be *proved*, for all $d$ at once.)
Deduct 3 if the induction is skipped and the closed form just quoted (the exam asks
to prove it — in a\_2024 it was given, here it is the task); deduct 2 if
non-universality is argued only by "linear functions aren't all continuous
functions" without an explicit $f$ and proof.

**2. (9)** *($\subseteq$, 4 pts)* For $d = 1$ the weights are scalars
$A = \lambda$, $B = b$, $C = c$, and $a_t = c\, \lambda^{L-t} b =
(cb)\, \lambda^{L-t}$; take $p := cb$ (recall $\lambda^0 := 1$, also for
$\lambda = 0$).
*($\supseteq$, 4 pts)* Given $p, \lambda \in \mathbb{R}$, the hypothesis with
$A = \lambda$, $B = 1$, $C = p$ realizes $a_t = p\,\lambda^{L-t}$.
*Edge cases (1 pt):* $p = 0$ ⇒ zero sequence; $\lambda = 0$ ⇒ $(0, \dots, 0, p)$;
$\lambda < 0$ ⇒ alternating signs — all covered by the same two directions; no
extra case analysis needed, but the answer should show awareness that these are
included (e.g. by the $\lambda^0 = 1$ convention remark).
Common traps: proving only one direction of the set equality (cap at 4); writing
the geometric ratio in the wrong direction (the sequence is geometric *backwards*:
$a_t = \lambda\, a_{t+1}$, exponent grows as $t$ decreases).

**3. (9)** *Inclusion (2 pts):* zero-padding — given scalar weights
$(\lambda, b, c)$, take $A' = \begin{pmatrix} \lambda & 0 \\ 0 & 0 \end{pmatrix}$,
$B' = (b, 0)^\top$, $C' = (c, 0)^\top$; then $C'^\top A'^{k} B' = c \lambda^k b$
for all $k \ge 0$, so the same function is realized and
$\mathcal{H}_1 \subseteq \mathcal{H}_2$.
*Three-term identity (3 pts):* if $a_t = p \lambda^{L-t}$ then for
$2 \le t \le L-1$: $a_{t+1} a_{t-1} = p\lambda^{L-t-1} \cdot p\lambda^{L-t+1} =
p^2 \lambda^{2(L-t)} = a_t^2$ (holds also when $p = 0$ or $\lambda = 0$).
*Witness (3 pts):* $a_t := 1 + 2^{L-t}$. Realizable with $d = 2$: take
$A = \mathrm{diag}(1, 2)$, $B = C = (1, 1)^\top$, so $C^\top A^{L-t} B =
1 \cdot 1^{L-t} + 1 \cdot 2^{L-t}$ — a sum of two geometric sequences with distinct
ratios.
*Violation & conclusion (1 pt):* at $t = L-1$ (valid since $L \ge 3$):
$a_L a_{L-2} = 2 \cdot 5 = 10 \neq 9 = 3^2 = a_{L-1}^2$, so $a \notin
\mathcal{S}_1$ by the identity. Hence $\mathcal{S}_1 \subsetneq \mathcal{S}_2$,
i.e. $\mathcal{H}_1 \subsetneq \mathcal{H}_2$.
(Alternative full-credit witnesses: any non-geometric sum of two geometrics, e.g.
the arithmetic sequence $a_t = L - t$ via the Jordan block
$\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$, or a\_2024's alternating
$(\dots, 1, 0, 1)$ pattern — the witness must be *verified* realizable in
$\mathcal{H}_2$ by explicit weights, and its non-realizability in $\mathcal{H}_1$
proved.) Trap: checking the identity at $t = 1$ or $t = L$ (not covered by the
lemma); asserting "not geometric, hence not in $\mathcal{S}_1$" without invoking
part 2 or the identity.

**4. (12)**
**a. (3)** $A^\top = -A$ forces $A_{11} = -A_{11} = 0$, $A_{22} = 0$, and
$A_{21} = -A_{12}$, so $A = \omega J$ with $\omega := A_{12}$ (1 pt). Direct
computation gives $J^2 = -I_2$, hence $J^3 = -J$, $J^4 = I_2$, and
$J^{k+4} = J^k$ — period 4. The identity $J^k = \cos(\tfrac{k\pi}{2}) I_2 +
\sin(\tfrac{k\pi}{2}) J$ holds for $k = 0, 1, 2, 3$ by inspection
($I, J, -I, -J$), and both sides are $4$-periodic in $k$, so it holds for all
$k \in \mathbb{N}_0$ (2 pts; induction on $k$ equally fine). Deduct 1 if verified
only for $k \le 3$ with no periodicity/induction argument extending it.

**b. (5)** *($\subseteq$, 3 pts)* For $A = \omega J$: scalars commute with
matrices, so $A^k = \omega^k J^k$, and with $k := L - t$,
$$a_{L-k} = C^\top A^k B = \omega^k\, C^\top J^k B
= \omega^k \Big( \cos(\tfrac{k\pi}{2})\, C^\top B +
\sin(\tfrac{k\pi}{2})\, C^\top J B \Big),$$
which is the stated form with $\alpha := C^\top B$, $\beta := C^\top J B$ (for
$k = 0$, $\omega^0 = 1$ holds also when $\omega = 0$).
*($\supseteq$, 2 pts)* Given $(\omega, \alpha, \beta)$, take $A := \omega J$,
$B := e_1$, $C := (\alpha, -\beta)^\top$: then $C^\top B = \alpha$ and, since
$J e_1 = (0, -1)^\top$, $C^\top J B = (-\beta)(-1) = \beta$; by the forward
computation this realizes the required sequence. Traps: treating $A^{L-t}$ as the
matrix exponential $e^{(L-t)A}$ (a rotation by *angle* $(L-t)\omega$) — it is a
matrix **power**: rotation by $(L-t) \cdot 90°$ scaled by $\omega^{L-t}$, so the
sequence is a period-4 sign-patterned *geometric* sequence, not a bounded
sinusoid; forgetting to show *every* pair $(\alpha, \beta)$ is attainable in the
converse.

**c. (4)** *Sign constraint (2 pts):* let $a \in \mathcal{S}_2^{anti}$ with
parameters $(\omega, \alpha, \beta)$. For any $k \in \{0, \dots, L-3\}$ (so both
positions $L-k$ and $L-k-2$ lie in $[L]$), using $\cos(\theta + \pi) =
-\cos\theta$ and $\sin(\theta + \pi) = -\sin\theta$:
$$a_{L-k-2} = \omega^{k+2} \Big( \alpha \cos\tfrac{(k+2)\pi}{2} +
\beta \sin\tfrac{(k+2)\pi}{2} \Big)
= -\,\omega^2\, \omega^{k} \Big( \alpha \cos\tfrac{k\pi}{2} +
\beta \sin\tfrac{k\pi}{2} \Big) = -\,\omega^2\, a_{L-k} .$$
Hence $a_{t-2} = -\omega^2 a_t$ and so $a_t\, a_{t-2} = -\omega^2 a_t^2 \le 0$ for
every $t \in \{3, \dots, L\}$: entries two steps apart can never both be strictly
positive.
*Witness (2 pts):* the all-ones sequence $a = (1, 1, \dots, 1)$. It lies in
$\mathcal{S}_1$ ($p = 1, \lambda = 1$ in part 2), hence in $\mathcal{S}_2$ by
part 3's inclusion (or directly: $A = I_2$, $B = C = e_1$). It is not in
$\mathcal{S}_2^{anti}$: $a_L a_{L-2} = 1 > 0$ contradicts the sign constraint
(uses $L \ge 3$); equivalently, $\alpha = a_L = 1$ and $a_{L-2} = -\omega^2 \alpha
= 1$ force $\omega^2 = -1$, impossible over $\mathbb{R}$. Hence
$\mathcal{H}_2^{anti} \subsetneq \mathcal{H}_2$.
*(Remark, not required: $\mathcal{H}_2^{anti}$ and $\mathcal{H}_1$ are
incomparable — for $L = 3$, $(\omega, \alpha, \beta) = (1, 1, 0)$ gives
$(-1, 0, 1) \in \mathcal{S}_2^{anti} \setminus \mathcal{S}_1$ since
$a_2^2 = 0 \ne -1 = a_1 a_3$. Contrast with a\_2024 Q1(4): symmetric transitions
add nothing over diagonal ones, while anti-symmetric transitions genuinely
restrict — over $\mathbb{R}$ they cannot even realize constant sequences.)*
Trap: proving only non-realizability and forgetting to *prove* the witness is
realizable by $\mathcal{H}_2$ (both claims are asked).

## Q2 — Gradient flow on a single ReLU neuron (35)

**1. (8)** Write $\mathcal{L}(w, v) = \tfrac12 \sum_n r_n^2$ with
$r_n = v [w^\top x_n]_+ - y_n$. Chain rule (4 pts for $v$, 4 pts for $w$):
$$\frac{\partial \mathcal{L}}{\partial v} = \sum_n r_n\, [w^\top x_n]_+ ,
\qquad
\nabla_w \mathcal{L} = \sum_n r_n\, v\, \mathbb{1}[w^\top x_n > 0]\, x_n ,$$
using the stated convention $\frac{d}{dz}[z]_+ = \mathbb{1}[z > 0]$ (which also
covers $w^\top x_n = 0$). Negating gives the flow equations. Full marks require an
actual derivation (chain rule made explicit), not just quoting the answer; deduct
2 for a missing factor $v$ in $\dot w$ or a sign error; using
$\mathbb{1}[z \ge 0]$ contradicts the stated convention (deduct 1 unless carried
consistently and flagged).

**2. (9)** Setup (3 pts):
$\frac{d}{dt}(v^2 - \|w\|^2) = 2 v \dot v - 2 w^\top \dot w$. Substitute part 1
(3 pts):
$$2 v \dot v = -2 \sum_n r_n\, v\, [w^\top x_n]_+ , \qquad
2 w^\top \dot w = -2 v \sum_n r_n\, \mathbb{1}[w^\top x_n > 0]\,(w^\top x_n).$$
Homogeneity identity (3 pts): $z\,\mathbb{1}[z > 0] = [z]_+$ for all $z$ (check
$z > 0$ and $z \le 0$ separately; equality at $z = 0$ is $0 = 0$ under the
convention), so the two expressions coincide and the derivative vanishes. Hence
$v(t)^2 - \|w(t)\|^2 \equiv v(0)^2 - \|w(0)\|^2$. This is the single-neuron case
of the balancedness conservation law (Lecture 4, Lemma 1; cf. 2022 exams Q2).
Trap: treating $w^\top \dot w$ as anything other than the inner product; invoking
balancedness from class without deriving it in this setting (the derivation is the
question).

**3. (8)** Let $c_0 := v(0)^2 - \|w(0)\|^2 > 0$. Key inequality (3 pts): by
part 2, for every $t \ge 0$
$$v(t)^2 = \|w(t)\|^2 + c_0 \ \ge\ c_0 > 0$$
(since $\|w(t)\|^2 \ge 0$) — the conserved quantity lower-bounds $v^2$ even though
$v^2$ itself is not conserved. Hence $v(t) \ne 0$ for all $t$ (2 pts; in
particular $v(0) \ne 0$ since $v(0)^2 > \|w(0)\|^2 \ge 0$). Sign preservation
(3 pts): $v(\cdot)$ is continuous (differentiable by assumption); if
$\mathrm{sign}\, v(t_2) \ne \mathrm{sign}\, v(t_1)$ for some $t_1 < t_2$, the
intermediate value theorem yields $t^* \in (t_1, t_2)$ with $v(t^*) = 0$ —
contradiction. So $\mathrm{sign}\, v(t) = \mathrm{sign}\, v(0)$ for all $t \ge 0$.
Note this is *simpler* than the balanced case ($v(0)^2 = \|w(0)\|^2$, b\_2022 Q2c),
which needs an integrating-factor argument; here strict imbalance gives the
uniform bound $|v(t)| \ge \sqrt{c_0}$ for free. Traps: claiming $v^2$ constant;
skipping continuity/IVT ("$v$ can't jump" must be justified by continuity of the
flow); circular use of part 4.

**4. (10)** *(i) (3 pts)* $\mathcal{L} \ge 0$ always, and at $(w, v) = (1, -1)$:
$v[w]_+ = -1 = y_1$, so $\mathcal{L}(1, -1) = 0$. Hence
$\inf \mathcal{L} = 0$, attained — only with $v < 0$ (need $v[w]_+ = -1 < 0$).
*(ii) (5 pts)* $v(0) > |w(0)| \ge 0$ implies $v(0) > 0$ and
$v(0)^2 > w(0)^2$ (1 pt — spell this out). By part 3, $v(t) > 0$ for all $t$
(2 pts). Then $v(t)[w(t)]_+ \ge 0$, so the residual satisfies
$v(t)[w(t)]_+ + 1 \ge 1$, giving (2 pts)
$$\mathcal{L}(w(t), v(t)) = \tfrac12 \big( v(t)[w(t)]_+ + 1 \big)^2 \ \ge\
\tfrac12 = \tfrac12 y_1^2 .$$
*(iii) (2 pts)* Gradient flow stays at loss $\ge \tfrac12 > 0 = \inf \mathcal{L}$
forever, so it does not converge to the global infimum — the output weight's sign
is trapped by conservation. Contrast: for linear neural networks, gradient flow
from a balanced initialization whose end-to-end matrix has a deficiency margin
provably converges to the global minimum at a linear rate (Lecture 4, Thm 2);
a single ReLU neuron already breaks any such unconditional guarantee.
*(Numerically: $w(t)$ crosses $0$ in finite time, after which both gradients
vanish and the flow freezes with $\mathcal{L} = \tfrac12$ exactly — matches the
bound; stating this is not required.)*
Traps: exhibiting a minimizer with $v > 0$ (impossible — check!); proving
$\mathcal{L} \to \tfrac12$ instead of the required $\mathcal{L} \ge \tfrac12$
(more than needed, fine if correct); contrasting with the wrong class result
(the relevant class theorem is linear-network convergence, not saddle
avoidance).

## Q3 — PAC-Bayes with Gaussian priors and posteriors (30)

**1. (8)** With $q, p$ the densities of $Q := N(w, \sigma^2 I_d)$,
$P := N(0, \sigma^2 I_d)$: the normalizations $(2\pi\sigma^2)^{-d/2}$ cancel
(2 pts), and
$$\ln \frac{q(\theta)}{p(\theta)} =
\frac{ -\|\theta - w\|^2 + \|\theta\|^2 }{2\sigma^2}
= \frac{ 2\langle \theta, w\rangle - \|w\|^2 }{2\sigma^2}$$
(3 pts). Taking $\mathbb{E}_{\theta \sim Q}$ with
$\mathbb{E}_Q[\theta] = w$ (3 pts):
$$KL(Q \| P) = \frac{2\|w\|^2 - \|w\|^2}{2\sigma^2} = \frac{\|w\|^2}{2\sigma^2}.$$
Also full credit: instantiating the general Gaussian-KL formula from class
(Lecture 6, Lem 1) with $\Sigma_0 = \Sigma_1 = \sigma^2 I_d$ —
$\tfrac12(d + \|w\|^2/\sigma^2 - d + \ln 1) = \|w\|^2/(2\sigma^2)$ — provided all
four terms are computed, not asserted. Trap: sign error in the exponent
difference; leaving second moments uncancelled (if expanded separately:
$\mathbb{E}_Q\|\theta\|^2 = \|w\|^2 + d\sigma^2$ and
$\mathbb{E}_Q\|\theta - w\|^2 = d\sigma^2$, difference again $\|w\|^2$ — fine).

**2. (7)** *Instantiation (3 pts):* $P = N(0, \sigma^2 I_d)$ is chosen
independently of $S$, so the reminder applies; its conclusion holds on a single
probability-$(1-\delta)$ event *simultaneously for all* $Q$ — in particular for
the whole family $\{ N(w, \sigma^2 I_d) : w \in \mathbb{R}^d \}$. Plugging
part 1's $KL = \|w\|^2 / (2\sigma^2)$ gives the stated bound for every $w$ at
once, hence for $w = w_S$.
*(i) Legitimacy (2 pts):* the quantifier "$\forall Q$" sits *inside* the
high-probability event — the event does not depend on $Q$ — so the posterior may
be chosen after seeing $S$; only the prior must be data-independent. (No union
bound over $w$ is needed, and none would work over an uncountable family.)
*(ii) (2 pts):* the guarantee is for the *stochastic ("noisy") predictor*: draw
$\theta \sim N(w_S, \sigma^2 I_d)$ and predict with $h_\theta$ — it bounds
$L_D(Q)$, not $L_D(h_{w_S})$; bounding the latter requires an additional argument
(course caveat, Lecture 6).
Trap: re-invoking the theorem per $w$ with fresh $\delta$'s and union-bounding;
claiming the bound holds for $h_{w_S}$ itself.

**3a. (5)** *Violated hypothesis (2 pts):* the prior must be **chosen
independently of $S$** ("fixed before the data"); $P = N(w_S, \sigma^2 I_d)$ is a
function of $S$, so the theorem simply does not cover it — its probability
statement is over draws of $S$ *for a fixed $P$*.
*Broken proof step (3 pts):* the class proof bounds
$\mathbb{E}_S\big[ e^{f(S)} \big]$, $f(S) := \sup_Q \big[ 2(N-1)\,
\mathbb{E}_{\theta \sim Q}[\Delta(\theta)^2] - KL(Q\|P) \big]$ with
$\Delta(\theta) := L_D(h_\theta) - L_S(h_\theta)$, via change of measure
$f(S) \le \ln \mathbb{E}_{\theta \sim P}\big[ e^{2(N-1)\Delta(\theta)^2} \big]$,
then **swaps** $\mathbb{E}_S$ and $\mathbb{E}_{\theta \sim P}$ — valid only
because $P$ is independent of $S$ — and applies Hoeffding to the i.i.d. losses of
each **fixed** $\theta$ to get
$\mathbb{E}_S[e^{2(N-1)\Delta(\theta)^2}] \le 2N$, finishing with Markov. With
$P = P(S)$ the swap is illegal, and Hoeffding cannot be applied to hypotheses
*selected using $S$*: training concentrates $P(S)$ precisely on $\theta$ whose
empirical loss is atypically small relative to $L_D$, so
$\mathbb{E}_S \mathbb{E}_{\theta \sim P(S)}[e^{2(N-1)\Delta(\theta)^2}]$ need not
be $\le 2N$ and the failure probability is no longer $\le \delta$. The "free"
$KL = 0$ bound is the same fallacy as reading generalization off the training
loss (cf. the data-dependent-prior pitfall discussed in class). Grade: naming the
violated hypothesis alone earns 2; the remaining 3 require pointing at the
independence-based swap / fixed-$h$ Hoeffding step, not a generic "overfitting"
remark.

**3b. (5)** *Union over the grid (2 pts):* each $P_j$ is data-independent, so the
reminder applies to $(P_j, \delta_j)$; since
$\sum_{j \ge 0} \delta_j = \delta \sum_{j \ge 0} 2^{-(j+1)} = \delta$, the union
bound makes all conclusions hold simultaneously w.p. $\ge 1 - \delta$.
*Simultaneous bound (2 pts):* $\ln(2N/\delta_j) = \ln(2N/\delta) + (j+1)\ln 2$,
giving exactly the stated display, for all $j$ and all $Q$ at once — so $j$ (the
prior scale) may be selected after seeing $S$.
*Instantiation (1 pt):* by part 1 with variance $2^j \sigma_0^2$,
$KL(Q_j \| P_j) = \|w_S\|^2 / (2^{j+1} \sigma_0^2)$, so w.p. $\ge 1 - \delta$,
for every $j$:
$$L_D(Q_j) \le L_S(Q_j) + \sqrt{ \frac{ \frac{\|w_S\|^2}{2^{j+1}\sigma_0^2}
+ \ln\!\big(\tfrac{2N}{\delta}\big) + (j+1)\ln 2 }{ 2(N-1) } } ,$$
and one may pick the minimizing $j$ — adapting the scale within a factor 2 of any
target variance at only a logarithmic ($+ (j+1)\ln 2$) price. Trap: non-summable
$\delta_j$; forgetting to recompute the KL at variance $2^j\sigma_0^2$; letting
the *mean* of the prior depend on $w_S$ (that is exactly what part 3a forbids —
only the scale is tuned, through data-independent candidates).

**4. (5)** Model answer (within four sentences): the bound is small only if both
of its terms are small. $L_S(N(w_S, \sigma^2 I_d))$ is the training loss averaged
over Gaussian parameter noise, which stays close to $L_S(h_{w_S})$ exactly when
the minimum is **flat** — the loss is insensitive to perturbing the weights
(the flat-minima discussion from class, Lecture 6) — while the KL term
$\|w_S\|^2 / (2\sigma^2)$ is small exactly when the learned weights have **low
norm**. Thus PAC-Bayes rewards flat, low-norm solutions, and — unlike uniform
convergence or the norm-only Rademacher bound — it depends on both the learned
hypothesis and the sample, which is why the course singles it out as the bound
family that can in principle track the observed generalization phenomena.
(Larger $\sigma^2$ trades smaller KL against a wider noise ball; part 3b tunes
this legitimately.) Credit: 2 flatness ↔ noisy-training-loss term; 2 low norm ↔
KL term; 1 the tie to the class discussion. Deduct 1 if over four sentences.

## Grading notes
- Total 105; per-part partial credit as marked. Hints used during attempt: −20% of
  that sub-part.
- Common traps to check: Q1.1 closed form quoted without induction; Q1.2/Q1.4b only
  one direction of a characterization; Q1.3 witness not verified realizable in
  $\mathcal{H}_2$; Q1.4 matrix power confused with matrix exponential; Q2.1
  missing factor $v$; Q2.3 claiming $v^2$ (rather than the difference) conserved,
  or skipping the IVT step; Q2.4 wrong class result cited in the contrast; Q3.1
  exponent sign; Q3.2 spurious union bound over $w$; Q3.3a vague "overfitting"
  answer without naming the broken step; Q3.3b non-summable weights or stale KL.
