# Mock Exam 1 — solutions & grading rubric

**⚠️ Spoilers. Attempt `mock_exam_01.md` first.** Tutor: grade against this rubric;
verified numerically on 2026-07-06 (Q2 flow: loss → 1e-27, imbalance drift ~1e-14).

## Q1 — Maxout networks (40)

**1. (10)** Convexity (4 pts): each $x \mapsto w_i x + b_i$ is convex; a pointwise max
of convex functions is convex (sup of any family of convex functions is convex — cite
or prove via epigraph/inequality in two lines). Piece count (6 pts): let
$I_j := \{x : h(x) = w_j x + b_j\}$ ordered by slope. Two affine functions cross at
most once, and by convexity the active (max) index has nondecreasing slope in $x$;
hence each of the $k$ affines is active on at most one interval ⇒ at most $k$ maximal
affine pieces. Deduct 3 if "at most k pieces" argued only by "k lines ⇒ k pieces"
without using convexity/ordering (k lines can cross k(k−1)/2 times in general).

**2. (10)** Take $f(x) = -x^2$, $c = 1/8$. For any convex $h$:
$h(1/2) \le \tfrac{h(0)+h(1)}{2}$. Let $\epsilon := \sup_{[0,1]}|f-h|$. Then
$h(1/2) \ge f(1/2) - \epsilon = -\tfrac14 - \epsilon$ and
$\tfrac{h(0)+h(1)}{2} \le \tfrac{f(0)+f(1)}{2} + \epsilon = -\tfrac12 + \epsilon$.
Combining: $-\tfrac14 - \epsilon \le -\tfrac12 + \epsilon \Rightarrow \epsilon \ge \tfrac18$.
(3 pts choosing a strictly concave target + convexity obstruction idea; 7 pts the
quantitative argument. Any strictly concave $f$ with the same midpoint computation is
fine.)

**3. (10)** Any PWL $f$ with $m$ pieces (breakpoints $t_1<\dots<t_{m-1}$) can be
written $f(x) = ax + b + \sum_{i=1}^{m-1} c_i [x - t_i]_+$ where $c_i$ = slope jumps
(4 pts; this representation was used in class/hw). Split
$P(x) := ax+b+\sum_{c_i>0} c_i[x-t_i]_+$ and $Q(x) := \sum_{c_i<0} (-c_i)[x-t_i]_+$:
both are convex PWL with at most $m$ pieces, and $f = P - Q$. Each convex PWL with
$\le m$ pieces is a max of its $\le m$ affine pieces, hence in $\mathcal{M}_m$ (3 pts
— this converse-of-part-1 step must be stated, not assumed). Universality: PWL dense
in $C([a,b])$ (given) and $\mathcal{D} \supseteq$ PWL ⇒ dense (3 pts).

**4. (10)** $h_1 - h_2$ has breakpoints only where $h_1$ or $h_2$ has one:
$\le (k_1 - 1) + (k_2 - 1)$ breakpoints ⇒ at most $k_1 + k_2 - 1$ pieces (6 pts).
$g_L$ has $2^L$ pieces ⇒ $k_1 + k_2 - 1 \ge 2^L$ (2 pts). Conclusion (2 pts): width
of this maxout form must be exponential in $L$ while ReLU depth achieves it linearly —
a depth-separation statement (cf. Lecture 2 / Telgarsky).

## Q2 — Asymmetric rank-1 factorization (35)

**1. (7)** $\nabla_u L = (uv^\top - M)v$, $\nabla_v L = (uv^\top - M)^\top u$; at
$(0,0)$ both vanish, so it's a critical point with $L(0,0) = \tfrac12\|M\|_F^2 > 0$.
Taking the top singular triplet $(\sigma_1, p, q)$ of $M$ and $(u,v) = (\sqrt\epsilon\, p, \sqrt\epsilon\, q)$
gives $L < L(0,0)$ for small $\epsilon>0$ (expand: cross term $-\epsilon\sigma_1$
dominates $\epsilon^2/2$). So $(0,0)$ is a non-global critical point ⇒ by the
reminder, $L$ is not convex. (Alternative full credit: restrict to a line through two
points violating the chord inequality, computed explicitly.)

**2. (10)** Expand $L(u,v) = \tfrac12\langle uv^\top - M, uv^\top - M\rangle$ and
differentiate: for a perturbation $\delta u$,
$D_u L[\delta u] = \langle uv^\top - M, \delta u\, v^\top \rangle = \delta u^\top (uv^\top - M) v$
⇒ $\nabla_u L = (uv^\top - M) v = (v^\top v) u - M v$; symmetrically
$\nabla_v L = (uv^\top - M)^\top u = (u^\top u) v - M^\top u$. Negate for the flow.
(Full marks require an actual derivation — index computation or directional
derivative — not just quoting the answer.)

**3. (8)** $\tfrac{d}{dt}(\|u\|^2 - \|v\|^2) = 2u^\top \dot u - 2v^\top \dot v
= 2[-(v^\top v)(u^\top u) + u^\top M v] - 2[-(u^\top u)(v^\top v) + v^\top M^\top u] = 0$,
since $u^\top M v = v^\top M^\top u$ (scalar transpose). This is the balancedness
conservation law (Lecture 4) specialized to rank-1.

**4. (10)** Ansatz (4 pts): plug $u = a x$, $v = a y$ into part 2's ODE:
$\dot u = (-a^3 + \lambda a)x$ (using $\|y\|=1$, $y^\top y = 1$, $Mv = \lambda a x$),
similarly for $v$; so the ansatz satisfies the flow with $\dot a = \lambda a - a^3$,
and by assumed uniqueness it IS the solution. Convergence (4 pts): for
$0 < a < \sqrt\lambda$, $\dot a = a(\lambda - a^2) > 0$ and $a$ is bounded above by
$\sqrt\lambda$ (cannot cross the equilibrium: $\dot a = 0$ there); monotone + bounded
⇒ $a(t) \to a_\infty$ with $a_\infty(\lambda - a_\infty^2) = 0$ and
$a_\infty \ge \alpha > 0$ ⇒ $a_\infty = \sqrt\lambda$. Conclusion (2 pts):
$uv^\top = a^2 xy^\top \to \lambda xy^\top = M$, so $L \to 0$.

## Q3 — Ternary sparse predictors (30)

**1. (8)** $|\mathcal{H}| \le 3^d$ (2 pts). Fix $h$: the $\ell(h(x_n),y_n)$ are i.i.d.
in $[0,1]$ with mean $L_D(h)$; Hoeffding with
$\epsilon = \sqrt{(d\ln3 + \ln(2/\delta))/(2N)}$ gives failure prob
$\le 2\exp(-2N\epsilon^2) = 2 e^{-d\ln 3}\,\delta/2 = \delta\,3^{-d}$ (3 pts). Union
bound over $\le 3^d$ hypotheses ⇒ total failure $\le \delta$ (3 pts).

**2. (10)** Counting (5 pts): a $w$ with $\|w\|_0 \le k$ is specified by a $k$-tuple
over the alphabet $\{(i, s) : i \in [d], s \in \{\pm1\}\} \cup \{\text{null}\}$ of
size $2d+1$ (positions of nonzeros with signs, padded with nulls); the map from
tuples onto $\mathcal{H}_k$ is surjective ⇒ $|\mathcal{H}_k| \le (2d+1)^k$. (Also
accept $\sum_{j\le k}\binom{d}{j}2^j \le (2d+1)^k$ shown by binomial theorem:
$\sum_{j\le k}\binom{k}{j}(2d)^j = (2d+1)^k$ needs $\binom{d}{j}\le\binom{k}{j}d^j/j!\dots$
— any correct route.) Bound (5 pts): identical Hoeffding + union argument with
$3^d \to (2d+1)^k$.

**3. (7)** Allocate $\delta_k := \delta \cdot 2^{-(k+1)}$ (or $\frac{\delta}{(k+1)(k+2)}$;
any summable-to-$\le\delta$ scheme). Apply part 2 per $k$ with $\delta_k$ and union
over $k$: with prob $\ge 1-\sum_k \delta_k \ge 1-\delta$,
$$\forall k, \forall h \in \mathcal{H}_k: \; L_D - L_S \le
\Delta(N,\delta,k) = \sqrt{\frac{k \ln(2d+1) + (k+1)\ln 2 + \ln(2/\delta)}{2N}}.$$
Increasing in $k$ ✓, $\to 0$ as $N\to\infty$ ✓ (must be stated). This is the SRM /
"black box" weighting pattern (Lecture 6; 2024 exams Q3).

**4. (5)** Expected content: uniform convergence over all of $\mathcal{H}$ is hopeless
($d \gg N$), but the *algorithm* does not return arbitrary $h$ — if GD's implicit
regularization biases it toward sparse solutions ($k_{\text{eff}} \ll d$, analogous
to min-norm/low-rank biases from class), then the returned $h$ lies in a small
$\mathcal{H}_{k_{\text{eff}}}$, and part 3's bound applies *to it* with the small
effective $k$ — without knowing $k$ in advance. Generalization is then a property of
the algorithm-class pair, not the class alone (Zhang et al. narrative, Lectures 6–7).
Full credit needs: (i) bound depends on returned $h$'s sparsity; (ii) simultaneity
over $k$ is what makes this legitimate; (iii) explicit use of "implicit
regularization/bias".

## Grading notes
- Total 105; per-part partial credit as marked. Hints used during attempt: −20% of
  that sub-part.
- Common traps to check: Q1.1 piece-count without convexity; Q1.3 missing the
  "convex PWL ⇒ max of affines" converse; Q2.2 quoting gradients without derivation;
  Q2.4 not invoking uniqueness for the ansatz; Q3.1 missing the union bound step or
  wrong $\epsilon$ inversion; Q3.3 non-summable $\delta_k$.
