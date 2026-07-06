# FODL Mock Exam 1 (generated 2026-07-06)

**Format matches the real exam:** 3 hours · no aid material · 3 questions · 105 points
(max grade 100 — the 5 extra points are slack, as in recent years).
Every claim proved in class or recitation may be used if cited precisely; anything else
must be proved. Novel setups — variants of real exam patterns (2020–2024), not copies.

Solutions & grading rubric: `mock_exam_01_solutions.md` — **do not open before attempting.**

---

## Question 1 (40 pts) — Maxout networks

For $k \in \mathbb{N}$, define the class of *single maxout units* of width $k$ over
scalar input:

$$\mathcal{M}_k := \Big\{\, h:\mathbb{R}\to\mathbb{R},\quad h(x) = \max_{i\in[k]} (w_i x + b_i) \;:\; w_i, b_i \in \mathbb{R} \,\Big\}$$

and the *difference class*

$$\mathcal{D}_k := \{\, h_1 - h_2 \;:\; h_1, h_2 \in \mathcal{M}_k \,\}.$$

1. **(10 pts)** Prove that every $h \in \mathcal{M}_k$ is convex, and is piecewise
   linear with at most $k$ pieces (maximal intervals on which $h$ is affine).

2. **(10 pts)** Prove that $\mathcal{M} := \bigcup_{k\in\mathbb{N}} \mathcal{M}_k$ is
   **not** universal with respect to the continuous functions on $[0,1]$: exhibit a
   continuous $f:[0,1]\to\mathbb{R}$ and a constant $c>0$ such that for every
   $k \in \mathbb{N}$ and every $h \in \mathcal{M}_k$,
   $\;\sup_{x\in[0,1]} |f(x)-h(x)| \ge c$.
   *Hint: what does convexity say at the midpoint of $[0,1]$?*

3. **(10 pts)** Prove that every piecewise linear $f:\mathbb{R}\to\mathbb{R}$ with $m$
   pieces belongs to $\mathcal{D}_m$. Conclude that
   $\mathcal{D} := \bigcup_k \mathcal{D}_k$ is universal with respect to
   $C([a,b])$ in the sup norm.
   *You may use without proof the theorem from class stating that piecewise linear
   functions are dense in $C([a,b])$ with respect to the sup norm.*
   *Hint: write $f$ as an affine function plus a sum of terms $c_i\,[x - t_i]_+$, and
   split by the sign of $c_i$.*

4. **(10 pts)** Let $g_L:[0,1]\to[0,1]$ be the sawtooth function from class, which is
   piecewise linear with $2^L$ pieces. Prove: if $g_L = h_1 - h_2$ on $[0,1]$ with
   $h_1 \in \mathcal{M}_{k_1}$, $h_2 \in \mathcal{M}_{k_2}$, then
   $k_1 + k_2 \ge 2^L + 1$.
   Conclude, in one or two sentences, what this says about the width of maxout
   networks of this form compared to the depth of ReLU networks (which express $g_L$
   with $O(L)$ layers of constant width, as shown in class).

---

## Question 2 (35 pts) — Gradient flow on asymmetric rank-1 factorization

Let $d \in \mathbb{N}_{\ge 2}$ and let $M \in \mathbb{R}^{d\times d}$, $M \neq 0$.
Define the loss

$$L : \mathbb{R}^d \times \mathbb{R}^d \to \mathbb{R}_{\ge 0}, \qquad
L(u,v) := \tfrac{1}{2}\, \|\, u v^\top - M \,\|_F^2 .$$

We run gradient flow: $\;\dot u(t) = -\nabla_u L(u(t),v(t))$,
$\;\dot v(t) = -\nabla_v L(u(t),v(t))$.

1. **(7 pts)** Prove that $L$ is not convex (as a function of the pair $(u,v)$).
   *Reminder: for a differentiable convex function, every critical point is a global
   minimum.*

2. **(10 pts)** Prove that the gradient flow dynamics take the form
   $$\dot u = -\,(v^\top v)\, u + M v, \qquad
     \dot v = -\,(u^\top u)\, v + M^\top u .$$

3. **(8 pts)** Prove that the *imbalance* $\;\|u(t)\|^2 - \|v(t)\|^2\;$ is constant
   along the flow.

4. **(10 pts)** Suppose now $M = \lambda\, x y^\top$ with $\lambda > 0$ and
   $\|x\| = \|y\| = 1$, and initialize $u(0) = \alpha x$, $v(0) = \alpha y$ with
   $0 < \alpha < \sqrt{\lambda}$. Show that $u(t) = a(t)\,x$, $v(t) = a(t)\,y$ solves
   the flow, where $a(t)$ satisfies $\dot a = \lambda a - a^3$, $a(0)=\alpha$; prove
   that $a(t)^2 \to \lambda$ monotonically as $t \to \infty$; and conclude that
   $L(u(t), v(t)) \to 0$.
   *You may assume without proof that the gradient flow ODE has a unique solution.*

---

## Question 3 (30 pts) — Generalization for ternary sparse predictors

Let $\mathcal{X} \subseteq \mathbb{R}^d$ be an input space, $\mathcal{Y}$ a label
space, $D$ an (unknown) distribution over $\mathcal{X}\times\mathcal{Y}$, and
$S = \{(x_n, y_n)\}_{n=1}^N$ an i.i.d. sample. Consider the hypothesis class of
*ternary linear predictors*

$$\mathcal{H} := \{\, h_w(x) = w^\top x \;:\; w \in \{-1, 0, +1\}^d \,\},$$

and a loss $\ell : \mathbb{R}\times\mathcal{Y} \to [0,1]$. As usual,
$L_D(h) := \mathbb{E}_{(x,y)\sim D}[\ell(h(x),y)]$ and
$L_S(h) := \frac1N \sum_{n=1}^N \ell(h(x_n), y_n)$.

*Reminder (Hoeffding, may be used as a black box): if $A_1,\dots,A_N$ are i.i.d.
random variables bounded in $[0,1]$, then for every $\epsilon \ge 0$,*
$$P\Big( \big| \tfrac1N \textstyle\sum_{n} A_n - \mathbb{E}[A_1] \big| \ge \epsilon \Big) \le 2\exp(-2N\epsilon^2).$$

1. **(8 pts)** Prove that with probability at least $1-\delta$ over the sample,
   $$\forall h \in \mathcal{H}: \quad L_D(h) - L_S(h) \;\le\; \sqrt{\frac{d\ln 3 + \ln(2/\delta)}{2N}}.$$

2. **(10 pts)** For $k \in \{0,1,\dots,d\}$ let
   $\mathcal{H}_k := \{ h_w \in \mathcal{H} : \|w\|_0 \le k \}$ (at most $k$ nonzero
   coordinates). Prove that $|\mathcal{H}_k| \le (2d+1)^k$, and deduce that for each
   fixed $k$, with probability at least $1-\delta$,
   $$\forall h \in \mathcal{H}_k: \quad L_D(h) - L_S(h) \;\le\;
   \sqrt{\frac{k\ln(2d+1) + \ln(2/\delta)}{2N}}.$$

3. **(7 pts)** Derive a bound that holds *simultaneously for all
   $k \in \{0,\dots,d\}$*: with probability at least $1-\delta$,
   $$\forall k,\; \forall h \in \mathcal{H}_k: \quad L_D(h) - L_S(h) \;\le\; \Delta(N, \delta, k)$$
   with $\Delta$ increasing in $k$ and $\lim_{N\to\infty}\Delta(N,\delta,k) = 0$ for
   every fixed $k$ and $\delta$. Write $\Delta$ explicitly.

4. **(5 pts)** Suppose $d$ is huge ($d \gg N$), so the bound of part 1 is vacuous —
   yet gradient-based training empirically finds solutions that generalize. Explain,
   in at most five sentences and using the concept of implicit regularization from
   class, under what circumstances the bound of part 3 is meaningful in this regime
   and why this resolves the apparent contradiction.
