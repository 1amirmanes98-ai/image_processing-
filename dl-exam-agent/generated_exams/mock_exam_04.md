# FODL Mock Exam 4 (generated 2026-07-06)

**Format matches the real exam:** 3 hours · no aid material · 3 questions · 105 points
(max grade 100 — the 5 extra points are slack, as in recent years).
Every claim proved in class or recitation may be used if cited precisely; anything else
must be proved. Novel setups — variants of real exam patterns (2020–2024), not copies.

Solutions & grading rubric: `mock_exam_04_solutions.md` — **do not open before attempting.**

---

## Question 1 (40 pts) — Linear RNNs: scalar state and anti-symmetric transitions

Fix $L \in \mathbb{N}_{\ge 3}$. For $d \in \mathbb{N}$, a *linear RNN hypothesis* with
state dimension $d$ receives a sequence of $L$ real numbers
$x = (x_1, \dots, x_L) \in \mathbb{R}^L$ and outputs $h(x) \in \mathbb{R}$ via

$$s_0(x) = 0 \in \mathbb{R}^d, \qquad
  \forall t \in [L]:\; s_t(x) = A\, s_{t-1}(x) + B\, x_t, \qquad
  h(x) = C^\top s_L(x),$$

with weights $A \in \mathbb{R}^{d \times d}$ (the *transition matrix*) and
$B, C \in \mathbb{R}^d$. Denote by $\mathcal{H}_d$ the class of all such hypotheses.
Throughout, $A^0 := I_d$ (in particular $\lambda^0 := 1$ for scalars, including
$\lambda = 0$). Say that $h$ *realizes the coefficient sequence*
$a = (a_1, \dots, a_L) \in \mathbb{R}^L$ if $h(x) = \sum_{t=1}^{L} a_t x_t$ for every
$x \in \mathbb{R}^L$.

1. **(10 pts)** Prove that every $h \in \mathcal{H}_d$ with weights $A, B, C$
   realizes the coefficient sequence

   $$a_t = C^\top A^{L-t} B, \qquad t \in [L],$$

   and that this is the *only* coefficient sequence $h$ realizes. Conclude that
   $\mathcal{H}_d$ is not universal with respect to the set of continuous functions:
   exhibit a continuous $f : \mathbb{R}^L \to \mathbb{R}$ such that
   $f \notin \mathcal{H}_d$ for every $d \in \mathbb{N}$, and prove it.
   *Hint:* consider a product of coordinates.

   By part 1, $\mathcal{H}_d$ is identified with the set of coefficient sequences it
   realizes: $\;\mathcal{S}_d := \{a \in \mathbb{R}^L : \text{some } h \in
   \mathcal{H}_d \text{ realizes } a\}$.

2. **(9 pts)** *Scalar state.* Prove that

   $$\mathcal{S}_1 \;=\; \Big\{\, a \in \mathbb{R}^L \;:\; \exists\, p, \lambda \in
   \mathbb{R} \;\; \text{s.t.} \;\; \forall t \in [L]:\; a_t = p\, \lambda^{L-t}
   \,\Big\},$$

   i.e. exactly the sequences that are geometric when read backwards from $a_L = p$
   with ratio $\lambda$ (both directions of the set equality must be proved; note the
   admissible degenerate patterns: $p = 0$ gives the zero sequence, $\lambda = 0$
   gives $(0, \dots, 0, p)$, and $\lambda < 0$ gives alternating signs).

3. **(9 pts)** Prove that $\mathcal{H}_1$ is strictly contained in $\mathcal{H}_2$
   (equivalently $\mathcal{S}_1 \subsetneq \mathcal{S}_2$).
   *Hint:* first show that every $a \in \mathcal{S}_1$ satisfies
   $a_{t+1}\, a_{t-1} = a_t^2$ for every $t \in \{2, \dots, L-1\}$. Which sequences
   realizable with $d = 2$ violate this?

4. **(12 pts)** *Anti-symmetric transitions.* Denote by
   $\mathcal{H}_2^{anti} \subseteq \mathcal{H}_2$ the sub-class of hypotheses whose
   transition matrix is anti-symmetric, $A^\top = -A$, and by
   $\mathcal{S}_2^{anti}$ the corresponding set of coefficient sequences. Let
   $J := \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$.

   a. **(3 pts)** Show that every anti-symmetric $A \in \mathbb{R}^{2 \times 2}$
      equals $\omega J$ for some $\omega \in \mathbb{R}$, and prove that for every
      $k \in \mathbb{N}_0$

      $$J^k \;=\; \cos\!\Big(\frac{k\pi}{2}\Big)\, I_2 \;+\;
        \sin\!\Big(\frac{k\pi}{2}\Big)\, J$$

      (in particular the powers of $J$ cycle with period $4$:
      $I_2, J, -I_2, -J, I_2, \dots$). Note that $A^{L-t}$ is a matrix **power**,
      not a matrix exponential.

   b. **(5 pts)** Prove the characterization

      $$\mathcal{S}_2^{anti} \;=\; \Big\{\, a \in \mathbb{R}^L \;:\; \exists\,
      \omega, \alpha, \beta \in \mathbb{R} \;\; \text{s.t.} \;\;
      \forall k \in \{0, \dots, L-1\}:\;
      a_{L-k} = \omega^k \Big( \alpha \cos\!\Big(\frac{k\pi}{2}\Big) +
      \beta \sin\!\Big(\frac{k\pi}{2}\Big) \Big) \Big\}$$

      — geometric sequences carrying the period-$4$ sign pattern
      $(\alpha, \beta, -\alpha, -\beta, \alpha, \dots)$ when read backwards from
      $a_L$ (both directions must be proved).

   c. **(4 pts)** Exhibit a coefficient sequence realizable by $\mathcal{H}_2$ —
      in fact even by $\mathcal{H}_1$ — that is **not** realizable by
      $\mathcal{H}_2^{anti}$, and prove both claims. Conclude that
      $\mathcal{H}_2^{anti} \subsetneq \mathcal{H}_2$.
      *Hint:* how are $a_t$ and $a_{t-2}$ related for sequences in
      $\mathcal{S}_2^{anti}$?

---

## Question 2 (35 pts) — Gradient flow on a single ReLU neuron

Let $D, N \in \mathbb{N}$ and let $\{(x_n, y_n)\}_{n=1}^{N} \subset \mathbb{R}^D
\times \mathbb{R}$ be a training set. Consider a network consisting of a single ReLU
neuron,

$$h_{w,v}(x) := v\, \big[ w^\top x \big]_+, \qquad w \in \mathbb{R}^D,\;
v \in \mathbb{R},$$

where $[z]_+ := \max\{z, 0\}$, and the squared-loss objective

$$\mathcal{L}(w, v) := \frac{1}{2} \sum_{n=1}^{N}
\big( v\,[w^\top x_n]_+ - y_n \big)^2 .$$

Gradient flow is run over $\mathcal{L}$:
$\;\dot w(t) = -\nabla_w \mathcal{L}(w(t), v(t))$,
$\;\dot v(t) = -\frac{\partial}{\partial v} \mathcal{L}(w(t), v(t))$.
Throughout, use the convention $\frac{d}{dz}[z]_+ := \mathbb{1}[z > 0]$ (so the
derivative at $z = 0$ is $0$); as in class, you may assume the flow exists, is
unique and differentiable, and that the non-differentiability of the ReLU does not
"disturb". Denote the residuals $r_n(t) := v(t)\,[w(t)^\top x_n]_+ - y_n$.

1. **(8 pts)** Derive the gradient flow equations: prove that

   $$\dot v(t) = -\sum_{n=1}^{N} r_n(t)\, \big[ w(t)^\top x_n \big]_+ ,
   \qquad
   \dot w(t) = -\, v(t) \sum_{n=1}^{N} r_n(t)\,
   \mathbb{1}\big[ w(t)^\top x_n > 0 \big]\, x_n .$$

2. **(9 pts)** *Balancedness.* Prove that along the flow

   $$\frac{d}{dt} \Big( v(t)^2 - \| w(t) \|^2 \Big) = 0 .$$

   *Hint:* $z \cdot \mathbb{1}[z > 0] = [z]_+$ for every $z \in \mathbb{R}$.

3. **(8 pts)** *Sign preservation.* Assume $v(0)^2 > \|w(0)\|^2$. Prove that
   $v(t) \neq 0$ for every $t \ge 0$, and that $v(t)$ has the same sign as $v(0)$
   for every $t \ge 0$. (Justify carefully why $v(t)^2$ is bounded away from zero —
   note that only the *difference* $v^2 - \|w\|^2$ is conserved, not $v^2$ itself.)

4. **(10 pts)** *An unreachable infimum.* Set $D = 1$, $N = 1$ and
   $(x_1, y_1) = (1, -1)$, i.e.

   $$\mathcal{L}(w, v) = \tfrac{1}{2} \big( v\,[w]_+ + 1 \big)^2, \qquad
   w, v \in \mathbb{R}.$$

   (i) Show that $\inf_{w,v} \mathcal{L}(w, v) = 0$ and that the infimum is
   attained (exhibit a global minimizer; note its $v$ is negative).
   (ii) Assume the initialization satisfies $v(0) > |w(0)|$. Prove that

   $$\forall t \ge 0: \quad \mathcal{L}\big(w(t), v(t)\big) \;\ge\; \tfrac{1}{2}.$$

   (iii) Conclude that gradient flow over ReLU networks does **not** always converge
   to the global infimum of the loss, and contrast this in one sentence with the
   convergence guarantee proved in class for gradient flow over *linear* neural
   networks (Lecture 4).
   *Hint:* use part 3.

---

## Question 3 (30 pts) — PAC-Bayes with Gaussian priors and posteriors

Let $\mathcal{X}$ be an input space and $\mathcal{Y}$ an output space, let $D$ be an
(unknown) distribution over $\mathcal{X} \times \mathcal{Y}$, and let
$S = \{(x_n, y_n)\}_{n=1}^{N}$ be a training set of $N \ge 2$ examples drawn i.i.d.
from $D$. Hypotheses are parametrized by $\theta \in \mathbb{R}^d$:
$\mathcal{H} = \{ h_\theta : \theta \in \mathbb{R}^d \}$ (an arbitrary architecture),
and distributions over $\mathcal{H}$ are identified with distributions over
$\mathbb{R}^d$. The loss $\ell : \mathcal{Y} \times \mathcal{Y} \to [0, 1]$ is
bounded; $L_D(h) := \mathbb{E}_{(x,y) \sim D}[\ell(h(x), y)]$ and
$L_S(h) := \frac{1}{N} \sum_{n=1}^N \ell(h(x_n), y_n)$. For a distribution $Q$ over
$\mathbb{R}^d$ write $L_D(Q) := \mathbb{E}_{\theta \sim Q}[L_D(h_\theta)]$ and
$L_S(Q) := \mathbb{E}_{\theta \sim Q}[L_S(h_\theta)]$.

*Reminder (PAC-Bayes bound, as proved in class):* let $P$ be a prior distribution
over $\mathcal{H}$, **chosen independently of the sample $S$**, and let
$\delta \in (0,1)$. Then with probability at least $1 - \delta$ over $S$,
simultaneously for **every** distribution $Q$ over $\mathcal{H}$ (including
$S$-dependent ones):

$$L_D(Q) - L_S(Q) \;\le\; \sqrt{\frac{KL(Q \| P) + \ln\!\big(\frac{2N}{\delta}\big)}
{2(N-1)}} .$$

*Reminder (Gaussians and KL):* $N(\mu, \sigma^2 I_d)$ has density
$p(\theta) = (2\pi\sigma^2)^{-d/2} \exp\!\big( -\|\theta - \mu\|^2 / (2\sigma^2)
\big)$, and $KL(Q \| P) := \mathbb{E}_{\theta \sim Q}\big[ \ln \frac{q(\theta)}
{p(\theta)} \big]$ for densities $q, p$ of $Q, P$.

1. **(8 pts)** Prove that for every $w \in \mathbb{R}^d$ and $\sigma^2 > 0$:

   $$KL\Big( N(w, \sigma^2 I_d) \,\Big\|\, N(0, \sigma^2 I_d) \Big) \;=\;
   \frac{\|w\|^2}{2\sigma^2} .$$

2. **(7 pts)** Fix $\sigma^2 > 0$ and the prior $P := N(0, \sigma^2 I_d)$ *before*
   seeing the data, train on $S$, and let $w_S \in \mathbb{R}^d$ denote the learned
   weights. Derive: with probability at least $1 - \delta$ over $S$, for **every**
   $w \in \mathbb{R}^d$ — in particular for $w = w_S$ —

   $$L_D\big( N(w, \sigma^2 I_d) \big) \;\le\;
   L_S\big( N(w, \sigma^2 I_d) \big) +
   \sqrt{\frac{\frac{\|w\|^2}{2\sigma^2} + \ln\!\big(\frac{2N}{\delta}\big)}
   {2(N-1)}} .$$

   Explain in one or two sentences (i) why it is legitimate that $w_S$ depends on
   $S$, and (ii) to which predictor the guarantee applies (is it $h_{w_S}$ itself?).

3. **(10 pts)** A friend proposes the shortcut $P := N(w_S, \sigma^2 I_d)$ and
   $Q := N(w_S, \sigma^2 I_d)$, so that $KL(Q \| P) = 0$ and the reminder "yields"
   the bound $L_D(Q) - L_S(Q) \le \sqrt{\ln(2N/\delta) / (2(N-1))}$ — tiny for large
   $N$, with no dependence on $\|w_S\|$ whatsoever.

   a. **(5 pts)** Explain precisely why this is invalid: name the hypothesis of the
      theorem that is violated, and identify which step of the proof given in class
      breaks when $P$ depends on $S$ (state what that step needs and why it fails).

   b. **(5 pts)** The legitimate way to *adapt the prior's scale* to the data: fix
      $\sigma_0^2 > 0$ and, for every $j \in \mathbb{N}_0 = \{0, 1, 2, \dots\}$, set
      $P_j := N(0,\, 2^j \sigma_0^2\, I_d)$ and $\delta_j := \delta \cdot 2^{-(j+1)}$.
      Prove: with probability at least $1 - \delta$ over $S$, simultaneously for
      every $j \in \mathbb{N}_0$ and every distribution $Q$,

      $$L_D(Q) - L_S(Q) \;\le\; \sqrt{\frac{KL(Q \| P_j) +
      \ln\!\big(\frac{2N}{\delta}\big) + (j+1)\ln 2}{2(N-1)}} ,$$

      and write the resulting bound for $Q_j := N(w_S,\, 2^j \sigma_0^2\, I_d)$
      (using part 1), noting that $j$ may now be chosen *after* seeing the data.

4. **(5 pts)** In at most four sentences, explain why the bound of part 2 favors
   solutions lying at **flat minima** and having **low parameter norm**, and connect
   this to the discussion from class on which properties of trained networks a
   meaningful generalization bound should depend.
