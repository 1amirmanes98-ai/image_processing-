# Mock Exam 2 — solutions & grading rubric

**⚠️ Spoilers. Attempt `mock_exam_02.md` first.** Tutor: grade against this rubric;
verified numerically on 2026-07-06 (Q1.3: rank-$R$ error of $I_M$ $= M{-}R$ exactly for
$M \in \{3,5,8\}$, GD from random init never beats it; Q2: ODE vs spectral solution
agree to 1e-15, kernel components frozen to 1e-14, time-varying decay bound holds with
ratio $\le 0.9973$; Q3: Monte-Carlo $R(\mathcal{H}_B \circ S)$ $\approx$ 0.40–0.48 of
the Massart bound for $(d,N) \in \{(5,10),(20,15),(3,40)\}$).

## Q1 — Product-pooling networks and matrix rank (40)

**1. (10)** ($\subseteq$, 4 pts) Each term $c_r \varphi^r (\psi^r)^\top$ has rank
$\le 1$: every column is a multiple of $\varphi^r$ (1 pt). By the reminder
(subadditivity of rank), $\operatorname{rank}\big(\sum_{r=1}^R c_r \varphi^r
(\psi^r)^\top\big) \le \sum_r 1 = R$ (3 pts).
($\supseteq$, 6 pts) Let $\operatorname{rank}(F) = k \le R$. Pick a basis
$u_1, \dots, u_k$ of the column space of $F$ and expand column $j$:
$F_{:,j} = \sum_{i=1}^k \beta_{ij} u_i$. Setting $\psi^i := (\beta_{i1}, \dots,
\beta_{iM})^\top$ gives, entrywise,
$\big(\sum_{i=1}^k u_i (\psi^i)^\top\big)_{pj} = \sum_i (u_i)_p \beta_{ij} = F_{pj}$,
i.e. $F = \sum_{i=1}^k u_i (\psi^i)^\top$. Take $c_i = 1$, $\varphi^i = u_i$ for
$i \le k$ and $c_i = 0$ for $k < i \le R$ (padding), so $F \in \mathcal{H}_R$
(the $k = 0$ case $F = 0$: all $c_r = 0$). Alternative full credit: SVD
$F = \sum_{i=1}^k \sigma_i u_i v_i^\top$ with $c_i = \sigma_i$. Deduct 2 if the padding
to width exactly $R$ / absorbing scalars is never addressed; deduct all 6 if
$\supseteq$ is only asserted ("rank $\le R$ means $R$ outer products") without a
construction.

**2. (10)** (i) (5 pts) Any $F \in \mathbb{R}^{M \times M}$ has
$\operatorname{rank}(F) \le M$ (at most $M$ columns) $\le R$, so by part 1
$F \in \mathcal{H}_R$ (2 pts). Explicit width-$M$ assignment (3 pts): $c_i = 1$,
$\varphi^i = \mathbf{e}^i$, $\psi^i = (F_{i,1}, \dots, F_{i,M})^\top$ ($i$-th row);
then $\sum_{i=1}^M \mathbf{e}^i (\psi^i)^\top$ has $(p, j)$ entry $F_{pj}$, so it
equals $F$. (Remark, not required: the class construction for universality — Prop 5,
Lecture 2 — uses $M^N = M^2$ one-hot terms; for $N = 2$ the rank argument shows $M$
terms suffice, and by (ii) no fewer can serve all targets.)
(ii) (5 pts) Take $I_M$: its columns $\mathbf{e}^1, \dots, \mathbf{e}^M$ are linearly
independent, so $\operatorname{rank}(I_M) = M$ (2 pts; invertibility /
$\det I_M = 1 \neq 0$ also fine). If $R < M$, part 1 gives $I_M \notin \mathcal{H}_R$
(2 pts). Hence $\mathcal{H}_R \ne \mathbb{R}^{M \times M}$, and combining (i)+(ii):
universal iff $R \ge M$ (1 pt for the explicit conclusion). Any other matrix accepted
**with** a full-rank proof.

**3. (10)** Singular values of $I_M$ (2 pts): $I_M^\top I_M = I_M$ has all eigenvalues
$1$, so $\sigma_i(I_M) = 1$ for all $i$ (or: $I_M = I \cdot I \cdot I$ is an SVD).
Applying part 1 and then EYM as stated (4 pts):
$$\min_{F \in \mathcal{H}_R} \|F - I_M\|_F^2
= \min_{\operatorname{rank}(W) \le R} \|W - I_M\|_F^2
= \sum\nolimits_{i=R+1}^{M} \sigma_i(I_M) = M - R.$$
(The class-printed EYM has $\sigma_i(A)$ where the classical statement has
$\sigma_i(A)^2$; here all $\sigma_i = 1$, so both give $M - R$ — no penalty either
way, but wrong handling of general $\sigma_i^2$ elsewhere would be an error.)
Explicit minimizer (2 pts): $F^\star = \sum_{i=1}^R \mathbf{e}^i (\mathbf{e}^i)^\top$
(rank $R$, and $\|F^\star - I_M\|_F^2 = \#\{\text{deleted ones}\} = M - R$); any
$\sum_{i=1}^R w_i w_i^\top$ with orthonormal $w_i$ works. Conclusion (2 pts): every
$h \in \mathcal{H}_R$ has $D(h, \mathrm{identity}) = \|F_h - I_M\|_F \ge
\sqrt{M - R}$, so $D \le \epsilon \Rightarrow M - R \le \epsilon^2 \Rightarrow
R \ge M - \epsilon^2$. (This is Lecture 2 §2.5 with $M^{N/2} \to M$.)

**4. (10)** (i) (6 pts) ($\subseteq$, 2 pts): $\big(c_r \varphi^r
(\varphi^r)^\top\big)^\top = c_r \varphi^r (\varphi^r)^\top$ and sums of symmetric
matrices are symmetric — for **every** width $R$, so the union is contained in the
symmetric matrices. ($\supseteq$, 4 pts): $F$ symmetric $\Rightarrow$ spectral theorem
gives $F = \sum_{i=1}^M \lambda_i v_i v_i^\top$ with orthonormal $v_i$ and real
$\lambda_i$; take $c_i = \lambda_i$, $\varphi^i = v_i$, so
$F \in \mathcal{H}^{\mathrm{sym}}_M$. Negative eigenvalues are absorbed by the sign of
$c_i$ — the step where $c \in \mathbb{R}^R$ (not $\ge 0$) is essential; both the union
claim and $\mathcal{H}^{\mathrm{sym}}_M = \{F : F^\top = F\}$ follow. (Mirrors the
$N = 2$ symmetric characterization of Exam 2020 Moed B, Q1.)
(ii) (4 pts) Claim: expressible $=$ the PSD matrices
$\{F : F^\top = F, \; x^\top F x \ge 0 \; \forall x\}$ (1 pt for the correct
characterization). ($\subseteq$, 1.5 pts): symmetry as before, and
$x^\top \big(\sum_r c_r \varphi^r (\varphi^r)^\top\big) x = \sum_r c_r
\langle \varphi^r, x \rangle^2 \ge 0$ since $c_r \ge 0$. ($\supseteq$, 1.5 pts): $F$
PSD $\Rightarrow$ symmetric with all $\lambda_i \ge 0$; the spectral construction of
(i) now has $c_i = \lambda_i \ge 0$. Trap: answering "matrices with non-negative
entries" — 0 pts for the characterization.

## Q2 — Prediction dynamics under a (time-varying) kernel (35)

**1. (8)** Gradient (3 pts): $\ell(w) = \frac12 (\Phi w - y)^\top (\Phi w - y)$; the
directional derivative along $\delta$ is $(\Phi \delta)^\top (\Phi w - y) =
\delta^\top \Phi^\top (\Phi w - y)$, so $\nabla \ell(w) = \Phi^\top (\Phi w - y)$
(must be derived, not quoted). Dynamics (3 pts): $u = \Phi w \Rightarrow
\dot u = \Phi \dot w = -\Phi \Phi^\top (\Phi w - y) = -H (u - y)$ with
$H = \Phi \Phi^\top$, which does not depend on $t$ (or on $w$). Properties (2 pts):
$H^\top = (\Phi \Phi^\top)^\top = H$; $v^\top H v = \|\Phi^\top v\|^2 \ge 0$; and
$(H)_{n,n'} = (\text{row } n)(\text{row } n')^\top = \langle \phi(x_n),
\phi(x_{n'}) \rangle$ — the Gram/kernel matrix. (Remark: this is Lemma 1 of Lecture 5
in the constant-Jacobian case $\frac{\partial f}{\partial w} = \phi(x)$, which is why
$H(t) \equiv H(0)$ here exactly.)

**2. (10)** (i) (6 pts) Let $q_n(t) := \langle v_n, u(t) - y \rangle$. Then
$\dot q_n = \langle v_n, \dot u \rangle = -\langle v_n, H (u - y) \rangle =
-\langle H v_n, u - y \rangle = -\lambda_n q_n$, using $H^\top = H$ and
$H v_n = \lambda_n v_n$ (3 pts). Hence $\frac{d}{dt}\big( e^{\lambda_n t} q_n(t) \big)
= e^{\lambda_n t} (\lambda_n q_n + \dot q_n) = 0$, so $e^{\lambda_n t} q_n(t) \equiv
q_n(0)$, i.e. $q_n(t) = e^{-\lambda_n t} q_n(0)$ (2 pts; the exponential-multiplier
trick avoids dividing by $q_n$ — dividing without treating $q_n = 0$ loses 1 pt).
Since $\{v_n\}$ is an orthonormal basis, $u(t) - y = \sum_n q_n(t) v_n$, giving the
displayed expansion (1 pt). No uniqueness-of-solution assumption is needed — the
argument applies to any solution.
(ii) (4 pts) $\lambda_n > 0 \Rightarrow |q_n(t)| = e^{-\lambda_n t} |q_n(0)| \to 0$ at
rate $\lambda_n$; $\lambda_n = 0 \Rightarrow q_n(t) = q_n(0)$ for all $t$ (1.5 pts).
For symmetric PSD $H$, $\ker H = \operatorname{span}\{v_n : \lambda_n = 0\}$ (writing
$v = \sum a_n v_n$: $Hv = \sum \lambda_n a_n v_n = 0$ iff $a_n = 0$ whenever
$\lambda_n > 0$) (1 pt). Hence $u(t) - y \to \sum_{n : \lambda_n = 0} q_n(0) v_n =
P_{\ker H}(u(0) - y)$, which vanishes iff $u(0) - y \perp \ker H$; when $H \succ 0$,
$\ker H = \{0\}$ and $u(t) \to y$ always, with $\|u(t) - y\| \le
e^{-\lambda_{\min} t} \|u(0) - y\|$ (1.5 pts).

**3. (10)** Differentiate the squared norm (3 pts): with $e(t) := u(t) - y$,
$$\tfrac{d}{dt} \|e(t)\|^2 = 2 \langle e(t), \dot e(t) \rangle
= -2 \, e(t)^\top H(t) \, e(t).$$
PSD floor (3 pts): $H(t) \succeq \lambda I_N$ means $e^\top (H(t) - \lambda I) e \ge
0$, i.e. $e^\top H(t) e \ge \lambda \|e\|^2$, so
$\frac{d}{dt}\|e\|^2 \le -2\lambda \|e\|^2$. Integrating factor (2 pts):
$g(t) := e^{2\lambda t} \|e(t)\|^2$ has $g'(t) = e^{2\lambda t}\big(
\frac{d}{dt}\|e\|^2 + 2\lambda \|e\|^2 \big) \le 0$, so $g(t) \le g(0)$, i.e.
$\|e(t)\|^2 \le e^{-2\lambda t} \|e(0)\|^2$. Time bound (2 pts): $\ell(t) =
\frac12 \|e(t)\|^2 \le \frac12 e^{-2\lambda t} \|e(0)\|^2 \le \epsilon$ once
$e^{2\lambda t} \ge \frac{\|e(0)\|^2}{2\epsilon}$, i.e. for all
$t \ge \frac{1}{2\lambda} \ln \frac{\|u(0) - y\|^2}{2 \epsilon}$ (if
$\|e(0)\|^2 \le 2\epsilon$ the log is $\le 0$ and the claim is trivial). Traps: writing
$e(t) = e^{-\int_0^t H} e(0)$ (invalid — $H(t)$ at different times need not commute;
that is the point of the sub-part); differentiating $\|e\|$ instead of $\|e\|^2$
(non-differentiable at 0); using an eigenbasis of "the" $H$ (it changes with $t$).

**4. (7)** Model answer (four sentences): "The equation
$\dot u = -H(t)(u - y)$ is exact for any architecture, and in the ultra-wide regime
the $1/\sqrt{n}$ output scaling makes every neuron's weights move only
$O(1/\sqrt{n})$ during training ($\|w_r(t) - w_r(0)\| \le 2cmt/\sqrt{n}$, Lecture 5
Prop 2), so the Jacobian — hence the Gram matrix — is nearly frozen:
$\|H(t) - H(0)\|_{\mathrm{spectral}} \le 4cm^3 t / \sqrt{n} \to 0$ as
$n \to \infty$ ('lazy training'). Moreover, at initialization $H(0)$ concentrates
around a deterministic NTK Gram matrix $H^*$ (Hoeffding + union bound, Lecture 5
Prop 1, $n \gtrsim m^4/\epsilon^2$). Therefore for large width the true dynamics are
approximately the constant-kernel linear system of part 2 — equivalently part 3
applies with $\lambda$ slightly below $\lambda_{\min}(H^*)$. Consequently, if
$H^* \succ 0$, the training loss of the (non-convex) problem converges to zero — a
global minimum — at an exponential rate set by the NTK spectrum."
Rubric: 2 pts lazy-weights/kernel-stability mechanism ($O(1/\sqrt n)$ movement, Prop
2); 2 pts concentration at init $H(0) \approx H^*$ (Prop 1); 2 pts implication —
approximately linear dynamics, exponential convergence to **zero** loss when
$\lambda_{\min}(H^*) > 0$; 1 pt naming the regime (NTK / lazy training) or the
global-minimum-despite-non-convexity point. Content over length, but −1 if
substantially over four sentences.

## Q3 — Rademacher complexity of ℓ1-bounded linear predictors (30)

**1. (8)** Definition (2 pts): $R(A) = \frac{1}{N} \, \mathbb{E}_{\sigma}\big[
\sup_{a \in A} \sum_{n=1}^N \sigma_n a_n \big]$ with $\sigma_1, \dots, \sigma_N$
i.i.d., $\Pr(\sigma_n = \pm 1) = \frac12$ (as in Lecture 6 Def 1 / the Rademacher
recitation). Dual-norm step (3 pts): for any $v$,
$\langle w, v \rangle \le \sum_j |w_j| |v_j| \le \|v\|_\infty \|w\|_1 \le B
\|v\|_\infty$; conversely $w^\star = B \operatorname{sign}(v_{j^\star})
\mathbf{e}^{j^\star}$ with $j^\star \in \operatorname{argmax}_j |v_j|$ satisfies
$\|w^\star\|_1 = B$ and $\langle w^\star, v \rangle = B |v_{j^\star}| = B
\|v\|_\infty$; hence $\sup_{\|w\|_1 \le B} \langle w, v \rangle = B \|v\|_\infty$
(a maximum, attained at a scaled signed coordinate vector). Assembly (3 pts):
$$R(\mathcal{H}_B \circ S) = \frac1N \mathbb{E}_\sigma \Big[ \sup_{\|w\|_1 \le B}
\sum_n \sigma_n \langle w, x_n \rangle \Big] = \frac1N \mathbb{E}_\sigma \Big[
\sup_{\|w\|_1 \le B} \big\langle w, \sum_n \sigma_n x_n \big\rangle \Big]
= \frac{B}{N} \, \mathbb{E}_\sigma \Big\| \sum_n \sigma_n x_n \Big\|_\infty,$$
where the middle equality is linearity of the inner product and the last applies the
dual-norm step pointwise per realization of $\sigma$ (that per-$\sigma$ application
must be visible).

**2. (8)** Construction of $V$ (3 pts): for $j \in [d]$ let $v^j := (x_{1,j}, \dots,
x_{N,j})^\top \in \mathbb{R}^N$ (the $j$-th coordinate of the sample along the $N$
examples) and $V := \{ +v^j, -v^j : j \in [d] \}$, so $|V| \le 2d$. Rewriting (2 pts):
$$\Big\| \sum\nolimits_n \sigma_n x_n \Big\|_\infty = \max_{j \in [d]} \Big|
\sum\nolimits_n \sigma_n x_{n,j} \Big| = \max_{j} \big| \langle \sigma, v^j \rangle
\big| = \max_{v \in V} \langle \sigma, v \rangle,$$
the $\pm$ pair absorbing the absolute value. Norm bound (1 pt):
$\|v^j\|_2^2 = \sum_n x_{n,j}^2 \le N$ since $|x_{n,j}| \le \|x_n\|_\infty \le 1$.
Massart (1 pt): $\mathbb{E}_\sigma \max_{v \in V} \langle \sigma, v \rangle \le
\sqrt{N} \cdot \sqrt{2 \ln(2d)}$. Combine with part 1 (1 pt):
$R(\mathcal{H}_B \circ S) \le \frac{B}{N} \sqrt{2 N \ln(2d)} = B \sqrt{2\ln(2d)/N}$.
Traps: applying Massart to the infinite ball $\{w\}$ directly (0 for that step);
forgetting the $\pm$ doubling ($\ln d$ instead of $\ln(2d)$: −1); norm bound $N$
instead of $\sqrt{N}$.

**3. (7)** Contraction + part 2 (3 pts): $R(\ell \circ \mathcal{H}_B \circ S) \le
\rho \, R(\mathcal{H}_B \circ S) \le \rho B \sqrt{2 \ln(2d)/N}$. Plug into the quoted
recitation theorem for the class $\mathcal{H}_B$ (3 pts): w.p. $\ge 1 - \delta$,
$\forall h \in \mathcal{H}_B$: $L_D(h) - L_S(h) \le 2\rho B \sqrt{2\ln(2d)/N} +
3\sqrt{2\ln(4/\delta)/N}$; rearrange (1 pt). Note the bound depends on the data only
through the support assumption $\|x\|_\infty \le 1$, and on dimension only through
$\ln(2d)$. (The lecture-notes version of the theorem has constant 4 in place of the
recitation's 3 — either quoted form accepted if used consistently.)

**4. (7)** Union step (3 pts): for $j \in \{0, 1, 2, \dots\}$ apply part 3 to
$\mathcal{H}_{2^j}$ with $\delta_j := \delta 2^{-(j+1)}$; since $\sum_{j \ge 0}
\delta_j = \delta$, a union bound gives that w.p. $\ge 1 - \delta$ **all** the events
hold simultaneously: $\forall j, \forall h \in \mathcal{H}_{2^j}$:
$L_D - L_S \le 2\rho \, 2^j \sqrt{2\ln(2d)/N} + 3\sqrt{2(\ln(4/\delta) +
(j+1)\ln 2)/N}$, using $\ln(4/\delta_j) = \ln(4/\delta) + (j+1)\ln 2$. A
non-summable choice of $\delta_j$ gets at most 1 of these 3 pts.
Instantiation (3 pts): given $w$, set $j(w) := 0$ if $\|w\|_1 \le 1$, else
$j(w) := \lceil \log_2 \|w\|_1 \rceil$. Then (a) $2^{j(w)} \ge \|w\|_1$, so
$h_w \in \mathcal{H}_{2^{j(w)}}$; (b) $2^{j(w)} \le \max\{1, 2\|w\|_1\} = B(w)$
(for $\|w\|_1 > 1$: $2^{\lceil \log_2 \|w\|_1 \rceil} < 2^{\log_2 \|w\|_1 + 1} =
2\|w\|_1$); (c) $(j(w)+1)\ln 2 = \ln(2 \cdot 2^{j(w)}) \le \ln(2B(w))$. Both terms of
the bound are increasing in $2^j$ and in the log argument, so substituting the upper
bounds (b), (c) yields the stated inequality — the monotonicity remark must appear.
Conclusion (1 pt), expected content: the bound scales linearly with $\|w\|_1$ but only
logarithmically with $d$, so it favors predictors of small $\ell_1$ norm (effectively
sparse ones) and remains meaningful even when $d \gg N$; it therefore explains
generalization exactly when gradient training's implicit bias selects such low-norm
solutions — generalization as a property of the algorithm–class pair (Lectures 6–7,
same weighting pattern as the norm-adaptive bound of Exam 2021 Moed B, Q3).

## Grading notes
- Total 105; per-part partial credit as marked. Hints used during attempt: −20% of
  that sub-part.
- Common traps to check: Q1.1 proving only one inclusion, or asserting the
  $\supseteq$ construction; Q1.2 not proving $\operatorname{rank}(I_M) = M$; Q1.3
  skipping $\sigma_i(I_M) = 1$ or omitting an attaining matrix; Q1.4(ii) "non-negative
  entries" instead of PSD; Q2.1 quoting $\nabla\ell$ without derivation; Q2.2 dividing
  by $q_n$ without handling zeros; Q2.3 using $e^{-\int H}$ or a fixed eigenbasis for
  time-varying $H(t)$; Q3.1 missing the attainment point or the per-$\sigma$
  application of duality; Q3.2 Massart on an infinite set, or $\ln d$ vs $\ln(2d)$;
  Q3.4 non-summable $\delta_j$ or unjustified replacement of $2^j$ by $B(w)$.
