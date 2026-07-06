# FODL Mock Exam 2 (generated 2026-07-06)

**Format matches the real exam:** 3 hours · no aid material · 3 questions · 105 points
(max grade 100 — the 5 extra points are slack, as in recent years).
Every claim proved in class or recitation may be used if cited precisely; anything else
must be proved. Novel setups — variants of real exam patterns (2020–2024), not copies.

Solutions & grading rubric: `mock_exam_02_solutions.md` — **do not open before attempting.**

---

## Question 1 (40 pts) — Product-pooling networks and matrix rank

Let $M \in \mathbb{N}_{\ge 2}$ and consider functions on the two-dimensional grid,
$f : [M] \times [M] \to \mathbb{R}$ (the $N = 2$ case of the discrete input spaces from
class). Identify each such function with its lookup table — the matrix
$F \in \mathbb{R}^{M \times M}$ defined by $F_{d_1, d_2} := f(d_1, d_2)$.

For a width $R \in \mathbb{N}$, consider the shallow product-pooling network from class
(one-hot representation $\to$ $1{\times}1$ conv of width $R$, locally connected $\to$
global product pooling $\to$ linear output). On input $(d_1, d_2)$, hidden unit
$r \in [R]$ computes $\langle \varphi^r, \mathbf{e}^{d_1} \rangle \cdot
\langle \psi^r, \mathbf{e}^{d_2} \rangle$ with filters
$\varphi^r, \psi^r \in \mathbb{R}^M$, and the output layer has weights
$c \in \mathbb{R}^R$:

$$h(d_1, d_2) \;=\; \sum_{r=1}^{R} c_r \, \langle \varphi^r, \mathbf{e}^{d_1} \rangle
\, \langle \psi^r, \mathbf{e}^{d_2} \rangle \;=\; \sum_{r=1}^{R} c_r \,
\varphi^r_{d_1} \, \psi^r_{d_2},$$

i.e., the realized matrix is $F_h = \sum_{r=1}^R c_r \, \varphi^r (\psi^r)^\top$ (a CP
decomposition with $R$ terms). Define the hypothesis class, as a set of matrices,

$$\mathcal{H}_R := \Big\{ \sum_{r=1}^{R} c_r \, \varphi^r (\psi^r)^\top \;:\;
c \in \mathbb{R}^R, \;\; \varphi^r, \psi^r \in \mathbb{R}^M \Big\}
\;\subseteq\; \mathbb{R}^{M \times M}.$$

1. **(10 pts)** Prove that
   $$\mathcal{H}_R = \big\{ F \in \mathbb{R}^{M \times M} : \operatorname{rank}(F) \le R \big\}.$$
   Both inclusions must be proven.
   *Reminder (may be used as known from linear algebra): for $A, B$ of the same size,
   $\operatorname{rank}(A + B) \le \operatorname{rank}(A) + \operatorname{rank}(B)$.*
   *Hint: for the inclusion $\supseteq$, expand the columns of $F$ in a basis of its
   column space.*

2. **(10 pts)** Recall that a hypothesis class of functions on $[M] \times [M]$ is
   *universal* if it can realize **any** function, i.e., under the identification
   above, if it equals $\mathbb{R}^{M \times M}$. Prove that $\mathcal{H}_R$ is
   universal **if and only if** $R \ge M$. Specifically:
   (i) for $R \ge M$, prove $\mathcal{H}_R = \mathbb{R}^{M \times M}$, and give an
   explicit assignment of $\{c_r, \varphi^r, \psi^r\}_{r=1}^{M}$ realizing an
   arbitrary given $F$ with width exactly $M$;
   (ii) for $R < M$, exhibit a concrete matrix not in $\mathcal{H}_R$, with proof.

3. **(10 pts)** Prove that for every $R \in \{0, 1, \dots, M-1\}$:
   $$\min_{F \in \mathcal{H}_R} \big\| F - I_M \big\|_F^2 \;=\; M - R,$$
   and exhibit a matrix attaining the minimum. Conclude: with the distance from class
   $D(h, \bar h) := \|F_h - F_{\bar h}\|_F$, if a width-$R$ network satisfies
   $D(h, \mathrm{identity\ table}) \le \epsilon$ (where the target function is
   $f(d_1, d_2) = \mathbb{1}[d_1 = d_2]$, i.e., $F = I_M$), then $R \ge M - \epsilon^2$.
   *Reminder (Eckart–Young–Mirsky, may be used as stated in class): let
   $A \in \mathbb{R}^{m_1 \times m_2}$ with singular values
   $\sigma_1(A) \ge \dots \ge \sigma_{\min\{m_1, m_2\}}(A) \ge 0$. For any
   $r \in \{0, 1, \dots, \min\{m_1, m_2\}\}$:*
   $$\min_{W \in \mathbb{R}^{m_1 \times m_2},\; \operatorname{rank}(W) \le r}
   \|W - A\|_F^2 \;=\; \sum\nolimits_{i=r+1}^{\min\{m_1, m_2\}} \sigma_i(A).$$

4. **(10 pts)** Assume now the weight-sharing constraint $\psi^r = \varphi^r$ for all
   $r \in [R]$ (the same filter applied at both grid locations — the *convolutional*
   case from class), and denote the resulting class by
   $$\mathcal{H}^{\mathrm{sym}}_R := \Big\{ \sum_{r=1}^{R} c_r \,
   \varphi^r (\varphi^r)^\top : c \in \mathbb{R}^R, \; \varphi^r \in \mathbb{R}^M \Big\}.$$
   (i) Prove that $\bigcup_{R \in \mathbb{N}} \mathcal{H}^{\mathrm{sym}}_R =
   \{ F \in \mathbb{R}^{M \times M} : F^\top = F \}$ (all symmetric matrices), and that
   width $R = M$ already suffices: $\mathcal{H}^{\mathrm{sym}}_M = \{F : F^\top = F\}$.
   (ii) Suppose the output weights are additionally constrained to be non-negative:
   $c_r \ge 0$ for all $r$. Characterize the class of matrices expressible with
   arbitrary width, and prove your characterization.
   *You may use the spectral theorem for real symmetric matrices as known from linear
   algebra.*

---

## Question 2 (35 pts) — Prediction dynamics under a (time-varying) kernel

Let $\{(x_n, y_n)\}_{n=1}^N \subseteq \mathbb{R}^d \times \mathbb{R}$ be a training set
and $y := [y_1, \dots, y_N]^\top \in \mathbb{R}^N$. For a differentiable model
$f(w, x)$ ($w$ = weights) trained by gradient flow on the $\ell_2$ loss, let
$u(t) \in \mathbb{R}^N$ hold the train predictions at time $t$:
$u_n(t) := f(w(t), x_n)$. Recall from class that $u(t)$ obeys
$\dot u(t) = -H(t)\,(u(t) - y)$ with $H(t)$ positive semidefinite (PSD). This question
studies these dynamics.

1. **(8 pts)** *Linear model.* Fix a feature map $\phi : \mathbb{R}^d \to \mathbb{R}^k$
   and let $f(w, x) = \phi(x)^\top w$ with $w \in \mathbb{R}^k$. Let
   $\Phi \in \mathbb{R}^{N \times k}$ be the matrix whose $n$-th row is
   $\phi(x_n)^\top$, so that $u = \Phi w$, and run gradient flow
   $\dot w(t) = -\nabla \ell(w(t))$ on
   $$\ell(w) = \tfrac{1}{2} \| \Phi w - y \|^2.$$
   Prove: (i) $\dot u(t) = -H \, (u(t) - y)$ where $H := \Phi \Phi^\top$ is constant in
   time; (ii) $H$ is symmetric PSD, with entries
   $(H)_{n, n'} = \langle \phi(x_n), \phi(x_{n'}) \rangle$.

2. **(10 pts)** *Constant kernel.* Suppose $\dot u(t) = -H (u(t) - y)$ for a constant
   symmetric PSD $H \in \mathbb{R}^{N \times N}$; by the spectral theorem write
   $H = \sum_{n=1}^N \lambda_n v_n v_n^\top$ with $\{v_n\}_{n=1}^N$ orthonormal and
   $\lambda_n \ge 0$.
   (i) Prove that for every $n \in [N]$ and $t \ge 0$:
   $$\langle v_n, u(t) - y \rangle = e^{-\lambda_n t} \, \langle v_n, u(0) - y \rangle,
   \qquad \text{hence} \qquad
   u(t) - y = \sum_{n=1}^{N} e^{-\lambda_n t} \, \langle v_n, u(0) - y \rangle \, v_n.$$
   *Hint: differentiate $e^{\lambda_n t} \langle v_n, u(t) - y \rangle$.*
   (ii) Deduce the convergence behavior per eigenvalue: components of $u(t) - y$ along
   eigenvectors with $\lambda_n > 0$ decay to zero exponentially (at rate $\lambda_n$),
   while components along eigenvectors with $\lambda_n = 0$ remain **constant** for all
   $t$. Conclude that $\lim_{t \to \infty} \big( u(t) - y \big) = P_{\ker H}
   \big( u(0) - y \big)$ (orthogonal projection onto the kernel of $H$), and that
   $u(t) \to y$ if and only if $u(0) - y \perp \ker(H)$ — in particular, whenever $H$
   is non-singular.

3. **(10 pts)** *Time-varying kernel.* Assume now only that $H(t)$ is symmetric for
   every $t \ge 0$, continuous in $t$, and that there exists $\lambda > 0$ with
   $H(t) \succeq \lambda I_N$ for all $t \ge 0$ (i.e., $H(t) - \lambda I_N$ is PSD).
   Prove:
   $$\forall t \ge 0: \qquad \| u(t) - y \|^2 \;\le\; e^{-2 \lambda t} \,
   \| u(0) - y \|^2,$$
   and deduce that the loss $\ell(t) := \tfrac{1}{2}\|u(t) - y\|^2$ satisfies
   $\ell(t) \le \epsilon$ for every
   $t \ge \frac{1}{2\lambda} \ln\big( \frac{\|u(0) - y\|^2}{2\epsilon} \big)$.
   *Hint: show that $g(t) := e^{2\lambda t} \, \|u(t) - y\|^2$ is non-increasing. Note
   that no closed-form solution of the ODE is available here — for time-varying $H(t)$
   you may not simply write $e^{-\int H}$.*

4. **(7 pts)** *Ultra-wide networks.* In **at most four sentences**: for an ultra-wide
   non-linear network (the regime studied in class), why does $H(t)$ remain close to
   its value at initialization throughout training, and what does this imply for the
   convergence of the training loss? Refer to the relevant quantitative results from
   class (no proofs needed).

---

## Question 3 (30 pts) — Rademacher complexity of ℓ1-bounded linear predictors

Let $d, N \in \mathbb{N}$. Let $\mathcal{X} \subseteq \{x \in \mathbb{R}^d :
\|x\|_\infty \le 1\}$ be an input space (all inputs have entries in $[-1, 1]$),
$\mathcal{Y}$ a label space, $D$ an unknown distribution over
$\mathcal{X} \times \mathcal{Y}$, and $S = \{(x_n, y_n)\}_{n=1}^N$ an i.i.d. sample.
For $B > 0$ define the class of $\ell_1$-bounded linear predictors

$$\mathcal{H}_B := \big\{ h_w : x \mapsto \langle w, x \rangle \;:\;
w \in \mathbb{R}^d, \; \|w\|_1 \le B \big\},
\qquad \|w\|_1 = \sum\nolimits_{j=1}^d |w_j|, \quad
\|v\|_\infty = \max\nolimits_{j \in [d]} |v_j|.$$

Let $\ell : \mathcal{Y} \times \mathbb{R} \to [0, 1]$ be a loss which is
$\rho$-Lipschitz in its second argument, and let $L_D, L_S$ denote the population and
empirical losses, as usual. For a class $\mathcal{H}$ write
$\mathcal{H} \circ S := \{ (h(x_1), \dots, h(x_N)) : h \in \mathcal{H} \}
\subseteq \mathbb{R}^N$ and
$\ell \circ \mathcal{H} \circ S := \{ (\ell(y_1, h(x_1)), \dots, \ell(y_N, h(x_N))) :
h \in \mathcal{H} \}$.

1. **(8 pts)** State the definition of the (empirical) Rademacher complexity $R(A)$ of
   a set $A \subseteq \mathbb{R}^N$, as given in class, and prove:
   $$R(\mathcal{H}_B \circ S) \;=\; \frac{B}{N} \; \mathbb{E}_{\sigma}
   \Big[ \Big\| \sum\nolimits_{n=1}^{N} \sigma_n x_n \Big\|_\infty \Big].$$
   *Hint: first prove that for every $v \in \mathbb{R}^d$,
   $\sup_{\|w\|_1 \le B} \langle w, v \rangle = B \|v\|_\infty$, and identify a point
   where the supremum is attained.*

2. **(8 pts)** Prove:
   $$R(\mathcal{H}_B \circ S) \;\le\; B \sqrt{\frac{2 \ln(2d)}{N}}.$$
   *Reminder (Massart's lemma, may be used as a black box): for any finite set
   $V \subset \mathbb{R}^N$ and $\sigma_1, \dots, \sigma_N$ i.i.d. uniform on
   $\{\pm 1\}$:*
   $$\mathbb{E}_{\sigma} \Big[ \max_{v \in V} \langle \sigma, v \rangle \Big] \;\le\;
   \Big( \max_{v \in V} \|v\|_2 \Big) \sqrt{2 \ln |V|}.$$
   *Hint: write $\|\sum_n \sigma_n x_n\|_\infty$ as a maximum of
   $\langle \sigma, v \rangle$ over a set of $2d$ vectors built from the coordinates of
   the sample.*

3. **(7 pts)** Derive: for every fixed $B > 0$ and $\delta \in (0, 1)$, with
   probability at least $1 - \delta$ over $S$:
   $$\forall h \in \mathcal{H}_B: \qquad L_D(h) \;\le\; L_S(h) \;+\;
   2 \rho B \sqrt{\frac{2 \ln(2d)}{N}} \;+\; 3 \sqrt{\frac{2 \ln(4/\delta)}{N}}.$$
   *Reminder (Rademacher generalization bound, proved in recitation): for any
   hypothesis class $\mathcal{H}$ and $\delta \in (0,1)$, w.p. $\ge 1 - \delta$ over
   $S \sim D^N$:*
   $$\forall h \in \mathcal{H}: \quad L_D(h) - L_S(h) \;\le\;
   2 R(\ell \circ \mathcal{H} \circ S) + 3 \sqrt{\frac{2 \ln(4/\delta)}{N}}.$$
   *Reminder (contraction, may be used as a black box): if $\ell(y, \cdot)$ is
   $\rho$-Lipschitz for every $y \in \mathcal{Y}$, then
   $R(\ell \circ \mathcal{H} \circ S) \le \rho \cdot R(\mathcal{H} \circ S)$.*

4. **(7 pts)** Prove an **adaptive** version holding for all norms simultaneously: with
   probability at least $1 - \delta$ over $S$, for **every** $w \in \mathbb{R}^d$ (no
   norm restriction), with $B(w) := \max\{ 1, \, 2\|w\|_1 \}$:
   $$L_D(h_w) \;\le\; L_S(h_w) \;+\; 2 \rho \, B(w) \sqrt{\frac{2 \ln(2d)}{N}}
   \;+\; 3 \sqrt{\frac{2 \big( \ln(4/\delta) + \ln(2 B(w)) \big)}{N}}.$$
   *Hint: apply part 3 to the classes $\mathcal{H}_{2^j}$, $j = 0, 1, 2, \dots$, with
   confidence levels $\delta_j := \delta \cdot 2^{-(j+1)}$.*
   Conclude in one or two sentences: which predictors does this bound favor, and why is
   it relevant to generalization of gradient-trained models when $d \gg N$ (recall the
   implicit-regularization discussion from class)?
