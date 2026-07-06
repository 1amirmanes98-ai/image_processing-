# FODL Mock Exam 3 (generated 2026-07-06)

**Format matches the real exam:** 3 hours · no aid material · 3 questions · 105 points
(max grade 100 — the 5 extra points are slack, as in recent years).
Every claim proved in class or recitation may be used if cited precisely; anything else
must be proved. Novel setups — variants of real exam patterns (2020–2024), not copies.

Solutions & grading rubric: `mock_exam_03_solutions.md` — **do not open before attempting.**

---

## Question 1 (40 pts) — Linear pieces of deep ReLU networks

Throughout this question networks have one-dimensional input and output
($\mathcal X = \mathcal Y = \mathbb R$) and ReLU activation $[z]_+ := \max\{0,z\}$,
applied entrywise by $\sigma(\cdot)$.

*Reminder (Lecture 2, Def. 1):* a continuous $h:\mathbb R\to\mathbb R$ is **piecewise
linear (PWL)** if there exist $-\infty =: c_0 < c_1 < \dots < c_{P-1} < c_P := \infty$
such that $h$ is affine on each $[c_{i-1}, c_i]$; the **number of linear pieces** of $h$
is the *minimal* $P$ for which this holds. For a minimal partition, the points
$c_1,\dots,c_{P-1}$ are called the *breakpoints* of $h$ (the points where its affine
formula genuinely changes).

For $w, L \in \mathbb N$, let $\mathcal N_{w,L}$ denote the class of functions computed
by fully connected ReLU networks with $L$ hidden layers, each of width at most $w$:

$$\mathcal N_{w,L} := \Big\{\, x \mapsto W^{(L+1)}\sigma\big(W^{(L)}\sigma(\cdots\sigma(W^{(1)}x + \mathbf b^{(1)})\cdots) + \mathbf b^{(L)}\big) + b^{(L+1)} \,\Big\},$$

where $W^{(1)}\in\mathbb R^{w,1}$, $W^{(l)}\in\mathbb R^{w,w}$ for $2\le l\le L$,
$W^{(L+1)}\in\mathbb R^{1,w}$, and biases of matching dimensions. (In the notation of
Lecture 2, $\mathcal N_{w,1} = \mathcal H_w$, and $\mathcal N_{w,L}$ is the deep class
$\bar{\mathcal H}_{\bar B = w}$ with $L+1$ layers in the lecture's layer counting.)

1. **(8 pts)** *(Composition lemma.)* Let $f, g:\mathbb R\to\mathbb R$ be PWL with $p$
   and $q$ linear pieces, respectively. Prove that $f\circ g$ is PWL with at most
   $p\cdot q$ linear pieces.
   *Hint: on a maximal interval on which $g$ is affine, at which points can
   $f\circ g$ fail to be affine?*

2. **(4 pts)** *(Shallow upper bound.)* Prove that every $h\in\mathcal N_{w,1}$ is PWL
   with at most $w+1$ pieces. (This is one direction of Prop. 1 from Lecture 2, whose
   proof was deferred to Home Assignment 2 — give a full proof here.)

3. **(8 pts)** *(Deep upper bound.)* Prove by induction on $L$: every
   $h\in\mathcal N_{w,L}$ is PWL with at most $(w+1)^L$ pieces.
   *Hint: show by induction on the layer index $k$ that there is a set of at most
   $(w+1)^k - 1$ points outside of which ALL neurons of layer $k$ (as functions of the
   network input $x$) are simultaneously locally affine. For the inductive step, bound
   the number of new breakpoints the ReLUs of layer $k+1$ can create inside each
   existing interval, exactly as in the counting of sub-parts 1–2: an affine function
   changes sign at most once on an interval.*

4. **(4 pts)** *(The sawtooth has many pieces.)* Let
   $g(x) = [2x]_+ - [4x-2]_+ + [2x-2]_+$ be the tent function from class and
   $g^{\circ L}$ its $L$-fold composition. You may use without proof (Lecture 2,
   §1.4): $g^{\circ L}\in\mathcal N_{3,L}$, and on $[0,1]$ the function $g^{\circ L}$
   is affine on each interval $[(j-1)2^{-L},\, j\,2^{-L}]$, $j\in\{1,\dots,2^L\}$, with
   slope $(-1)^{j-1}\, 2^L$ (the sawtooth with $2^{L-1}$ teeth).
   Prove that $g^{\circ L}$ has at least $2^L$ linear pieces.
   *Hint: show first that at a strict local extremum a PWL function must have a
   breakpoint.*

5. **(6 pts)** *(Depth–width tradeoff.)* Conclude from sub-parts 2–4:
   - if $h\in\mathcal N_{B,1}$ satisfies $h \equiv g^{\circ L}$, then
     $B \ge 2^L - 1$;
   - more generally, if $h\in\mathcal N_{w,L'}$ satisfies $h \equiv g^{\circ L}$, then
     $(w+1)^{L'} \ge 2^L$, i.e. $L' \ge L\cdot\frac{\ln 2}{\ln(w+1)}$.

   State in one sentence what this pair of facts says about trading depth for width.

6. **(10 pts)** *(Universality nonetheless.)*
   - **(7 pts)** Prove: every PWL $f:\mathbb R\to\mathbb R$ with $p \ge 2$ pieces and
     breakpoints $t_1 < \dots < t_{p-1}$ can be written as
     $$f(x) = a x + b + \sum\nolimits_{i=1}^{p-1} c_i\,[x - t_i]_+$$
     for suitable $a, b, c_1,\dots,c_{p-1}\in\mathbb R$, and conclude that
     $f \in \mathcal N_{p+1,\,1}$ (exact realization on all of $\mathbb R$; the case
     $p=1$ is contained in this for the empty sum). Do not cite Prop. 1 of Lecture 2 —
     its deferred proof is what you are asked to reproduce.
     *Hint: choose $a, b$ to match $f$ on its leftmost piece and $c_i$ to match the
     slope jumps; then compare derivatives piece by piece. Recall
     $\alpha x = \alpha[x]_+ - \alpha[-x]_+$.*
   - **(3 pts)** Conclude that one-hidden-layer ReLU networks of unbounded width are
     universal in the sense of Lecture 2: for every continuous
     $f:\mathbb R\to\mathbb R$ and every $\epsilon > 0$ there exist $B\in\mathbb N$
     and $h\in\mathcal N_{B,1}$ with
     $d(f,h) := \int_0^1 |f(x)-h(x)|\,dx < \epsilon$.
     *You may use without proof Lemma 1 from Lecture 2: for every continuous $f$ and
     $\epsilon>0$ there exists a PWL $g$ with $d(f,g)<\epsilon$.*

---

## Question 2 (35 pts) — Gradient flow on a cubic reparameterization of linear regression

Let $X \in \mathbb R^{N\times d}$ be a data matrix whose rows are training instances,
and let $y \in \mathbb R^N$ hold the labels. For $z\in\mathbb R^d$ denote by
$z^{\odot 3} := (z_1^3,\dots,z_d^3)^\top$ and $z^{\odot 2} := (z_1^2,\dots,z_d^2)^\top$
the elementwise powers, and by $u \odot v$ the elementwise (Hadamard) product. We fit a
linear predictor $w \in \mathbb R^d$ to the data, but *reparameterize* each weight as a
cube, $w = z^{\odot 3}$, and minimize over $z$:

$$L : \mathbb R^d \to \mathbb R_{\ge 0}\,,\qquad L(z) := \tfrac12\,\big\|\, X z^{\odot 3} - y \,\big\|^2 .$$

We minimize $L(\cdot)$ with gradient flow: $\dot z(t) = -\nabla L(z(t))$, initialized
at $z(0) = z_0 \in \mathbb R^d$. You may assume without proof that this ODE admits a
unique solution $z:[0,\infty)\to\mathbb R^d$; you may also use without proof that a
scalar ODE $\dot\psi(t) = F(t,\psi(t))$ whose right-hand side is continuous in $t$ and
continuously differentiable in $\psi$ has at most one solution per initial condition
(Picard–Lindelöf). Denote $\operatorname{supp}(v) := \{i\in[d] : v_i \neq 0\}$.

1. **(7 pts)** Prove that the gradient flow takes the form
   $$\dot z(t) = -3\, z(t)^{\odot 2} \odot \big( X^\top r(t) \big)\,, \qquad
   r(t) := X z(t)^{\odot 3} - y\,,$$
   i.e. derive $\nabla L(z) = 3\, z^{\odot 2} \odot \big(X^\top (X z^{\odot 3} - y)\big)$
   (an actual derivation — via partial derivatives with indices or via directional
   derivatives — not a verification of dimensions).

2. **(10 pts)** Prove: if $z_i(0) = 0$ for some coordinate $i \in [d]$, then
   $z_i(t) = 0$ for all $t \ge 0$. Conclude that
   $\operatorname{supp}\!\big(z(t)^{\odot 3}\big) \subseteq \operatorname{supp}(z_0)$
   for every $t\ge0$ — gradient flow can only reach predictors supported on the
   initially nonzero coordinates. Finally, explain in one sentence why this is an
   instance of *implicit regularization* in the sense of Lecture 7 (which complexity
   measure of the predictor is implicitly controlled, and by what).

3. **(8 pts)** Consider the instance $d = N = 1$, $X = (1)$, $y = (1)$, so that
   $L(z) = \tfrac12 (z^3-1)^2$. Prove that $L$ is **not** convex, and show that the
   critical point at $z = 0$ is degenerate: $L''(0) = 0$, i.e. there is no negative
   curvature there (the analogue, for this cubic model, of the non-strict saddles at
   the origin of linear networks of depth $\ge 3$ — Lecture 3, Prop. 3).
   *Reminder: for a differentiable convex function, every critical point is a global
   minimum.*

4. **(10 pts)** Same instance as sub-part 3, with initialization
   $z(0) = \alpha \in (0,1)$. Prove that $z(t)$ is strictly increasing with
   $\lim_{t\to\infty} z(t) = 1$, and conclude that $\lim_{t\to\infty} L(z(t)) = 0$.
   *Hint: analyze the sign of $\dot z$ on $(0,1)$; show the trajectory can never reach
   $1$ (consider the constant solution $\hat z \equiv 1$ and uniqueness); use that a
   monotone bounded trajectory converges, and show that its limit must be an
   equilibrium of the flow.*

---

## Question 3 (30 pts) — Generalization via a cover of the parameter ball

Let $\mathcal X$ be an input space, $\mathcal Y$ a label space, $D$ an (unknown)
distribution over $\mathcal X\times\mathcal Y$, and $S = \{(x_n,y_n)\}_{n=1}^N$ a
training sample drawn i.i.d. from $D$. Consider a parametric family of predictors
$\{h_w\}_{w\in\mathcal B}$ indexed by the parameter ball
$$\mathcal B := [-1,1]^d = \{\, w\in\mathbb R^d : \|w\|_\infty \le 1 \,\}\,, \qquad
\|v\|_\infty := \max\nolimits_{i\in[d]} |v_i|\,,$$
and a loss $\ell$ satisfying $\ell(h_w(x),y) \in [0,1]$ for every $w\in\mathcal B$ and
$(x,y)\in\mathcal X\times\mathcal Y$. Assume the loss is **$\rho$-Lipschitz in the
parameters**, uniformly over the data: for some $\rho > 0$,
$$\forall\, (x,y)\in\mathcal X\times\mathcal Y\,,\ \forall\, w, w'\in\mathcal B:\qquad
\big|\ell(h_w(x),y) - \ell(h_{w'}(x),y)\big| \;\le\; \rho\,\|w - w'\|_\infty\,.$$
Denote $L_D(w) := \mathbb E_{(x,y)\sim D}\big[\ell(h_w(x),y)\big]$ and
$L_S(w) := \frac1N \sum_{n=1}^N \ell(h_w(x_n),y_n)$.

(Unlike the covering argument from class, which discretizes a class of *functions*,
here you will discretize the *parameter space* directly.)

1. **(7 pts)** Let $\epsilon \in (0,1]$. Prove that there exists a finite set
   $C_\epsilon \subseteq \mathcal B$ such that
   $$\text{(i)}\quad |C_\epsilon| \;\le\; \big(\lceil 1/\epsilon\rceil + 1\big)^d
   \qquad\text{and}\qquad
   \text{(ii)}\quad \forall\, w\in\mathcal B\ \ \exists\, \tilde w\in C_\epsilon:\ \
   \|w - \tilde w\|_\infty \le \epsilon\,.$$
   (Such a $C_\epsilon$ is called an $\epsilon$-cover of $\mathcal B$ in the
   $\ell_\infty$ norm. Both properties must be proved.)

2. **(8 pts)** Prove: for every $\delta\in(0,1)$, with probability at least $1-\delta$
   over the sample $S$,
   $$\forall\, \tilde w \in C_\epsilon:\qquad
   \big|L_D(\tilde w) - L_S(\tilde w)\big| \;\le\;
   \Delta_\epsilon(N,\delta) := \sqrt{\frac{d\,\ln\!\big(\lceil 1/\epsilon\rceil + 1\big) + \ln(2/\delta)}{2N}}\,.$$
   *Reminder (Hoeffding, may be used as a black box): if $A_1,\dots,A_N$ are i.i.d.
   random variables bounded in $[0,1]$, then for every $t \ge 0$,*
   $$P\Big(\Big|\tfrac1N \textstyle\sum_{n=1}^N A_n - \mathbb E[A_1]\Big| \ge t\Big)
   \;\le\; 2\exp(-2Nt^2)\,.$$

3. **(8 pts)** Prove: for every $\delta\in(0,1)$, with probability at least $1-\delta$
   over the sample $S$,
   $$\forall\, w \in \mathcal B:\qquad
   L_D(w) - L_S(w) \;\le\; \Delta_\epsilon(N,\delta) + 2\rho\epsilon\,.$$
   (Note the quantifier: a single event of probability $\ge 1-\delta$ on which the
   bound holds simultaneously for **all** $w$ in the ball.)

4. **(7 pts)** The two terms in sub-part 3 pull in opposite directions as functions of
   $\epsilon$. Choose $\epsilon$ as an explicit function of $N$ and $\rho$ (with
   $\epsilon\in(0,1]$), state the resulting bound $\Delta(N,\delta)$ explicitly (no
   $\epsilon$ remaining), and prove that $\Delta(N,\delta) \xrightarrow[N\to\infty]{} 0$
   for every fixed $d$, $\rho$ and $\delta$.
