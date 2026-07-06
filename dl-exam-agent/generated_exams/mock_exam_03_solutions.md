# Mock Exam 3 — solutions & grading rubric

**⚠️ Spoilers. Attempt `mock_exam_03.md` first.** Tutor: grade against this rubric;
verified numerically on 2026-07-06 (Q1: exact breakpoint propagation — $g^{\circ k}$
has $2^k+2$ pieces with slopes $\pm 2^k$, and $(w+1)^L$ was never violated on random
deep nets; Q2: zero coordinates stay exactly $0$ along the flow, 1D trajectory
increases to $1$ with final loss $\sim 10^{-28}$, Jensen violation
$L(1/2)=49/128 > 1/4$; Q3: grid cover size/radius checked for $d\le3$, bound $\to 0$).

## Q1 — Linear pieces of deep ReLU networks (40)

**1. (8)** Let $c_0=-\infty<c_1<\dots<c_{q-1}<c_q=\infty$ delimit the pieces of $g$
and let $d_1<\dots<d_{p-1}$ be the breakpoints of $f$. Fix $j\in[q]$ and write
$g(x)=\alpha x+\beta$ on $I_j:=[c_{j-1},c_j]$.
- If $\alpha\ne0$: for $x\in I_j$, $f\circ g$ can fail to be affine only where
  $\alpha x+\beta\in\{d_1,\dots,d_{p-1}\}$, i.e. at the $\le p-1$ preimages
  $(d_i-\beta)/\alpha$. These split $I_j$ into $\le p$ subintervals; on each, $g$ maps
  into a single piece of $f$, so $f\circ g$ = affine $\circ$ affine = affine.
- If $\alpha=0$: $f\circ g$ is constant on $I_j$ — one piece.

$f\circ g$ is continuous (composition of continuous functions), and the constructed
partition has $\le pq$ intervals; the minimal count (Def. 1) is no larger, so
$f\circ g$ is PWL with $\le pq$ pieces.
*Credit:* 3 restriction to one affine piece of $g$; 3 preimage count $\le p-1$ per
interval incl. the $\alpha=0$ case; 2 assembling (continuity + minimality of Def. 1).
*Traps:* claiming pieces add ($p+q$); forgetting the constant ($\alpha=0$) case;
counting breakpoints of $f$ instead of their preimages under the affine map.

**2. (4)** $h(x)=\sum_{i=1}^{w} v_i\,[u_i x+b_i]_+ + b^{(2)}$. A neuron with
$u_i\ne0$ is affine on both sides of $\tau_i:=-b_i/u_i$ (its only possible
breakpoint); a neuron with $u_i=0$ is constant. Off the set
$T:=\{\tau_i: u_i\ne0\}$, $|T|\le w$, every neuron is locally affine, hence so is $h$
(a linear combination plus constant). Sorting $T$ delimits $\le w+1$ intervals on
which $h$ is affine; $h$ is continuous $\Rightarrow$ PWL with $\le w+1$ pieces.
*Credit:* 2 one breakpoint per neuron incl. $u_i=0$; 2 union + count.
*Trap:* asserting *exactly* $w+1$ (coinciding $\tau_i$'s or zero output weights give
fewer) — the claim is an upper bound.

**3. (8)** *Claim (induction on $k=0,1,\dots,L$):* there is a finite
$B_k\subset\mathbb R$ with $|B_k|\le(w+1)^k-1$ such that every layer-$k$ post-activation
neuron, as a function of the input $x$ (layer $0$ := the input itself), is affine on
each closed interval delimited by consecutive points of $B_k$.
- *Base:* $B_0=\emptyset$, $|B_0|=0=(w+1)^0-1$.
- *Step:* the layer-$(k{+}1)$ pre-activations $z_1,\dots,z_w$ are affine combinations
  of layer-$k$ neurons, hence affine on each of the $\le(w+1)^k$ intervals delimited
  by $B_k$. Fix such an interval $I$: each $z_j$ is affine on $I$, so $[z_j]_+$ is
  affine on $I$ except possibly at one point (an affine function changes sign at most
  once on an interval; if it has constant sign or is identically $0$ there is no new
  point) — the same counting as in sub-parts 1–2. So layer $k{+}1$ creates at most $w$
  new breakpoints per interval:
  $$|B_{k+1}| \le |B_k| + w\big(|B_k|+1\big) = (w+1)|B_k| + w
  \le (w+1)\big((w+1)^k-1\big)+w = (w+1)^{k+1}-1\,.$$
- *Conclusion:* the output is an affine combination of layer-$L$ neurons, hence affine
  on each of the $\le(w+1)^L$ intervals delimited by $B_L$; $h$ is continuous
  $\Rightarrow$ PWL with $\le(w+1)^L$ pieces. Sanity: $L=1$ recovers sub-part 2 and
  Prop. 1's $B+1$.

*Credit:* 2 a correct inductive statement over a **common** breakpoint set/partition
for all neurons of a layer; 4 the step ($\le w$ new breakpoints per interval and the
recursion $(w+1)|B_k|+w$); 2 base + output layer + conclusion.
*Traps:* per-neuron piece bookkeeping without a shared partition (pieces of a sum
were bounded by products, or doubling per neuron) yields $(2w)^L$-type bounds — a
*correct* proof of such a weaker exponential bound earns at most 4/8; forgetting that
the output layer adds no breakpoints.

**4. (4)** *Lemma:* at a strict local extremum $x^*$, a PWL $h$ must have a
breakpoint. Otherwise $x^*$ lies in the open interior of a piece $[c_{i-1},c_i]$ of a
minimal partition, so $h$ is affine on a neighborhood of $x^*$; a (constant or
non-constant) affine function has no strict local extremum — contradiction. (2 pts)

By the given structure, each interior grid point $x_j=j\,2^{-L}$,
$j\in[2^L-1]$, is a strict local extremum: the slopes on the two adjacent intervals
are $(-1)^{j-1}2^L$ and $(-1)^{j}2^L$ — opposite signs — so locally
$g^{\circ L}(x)=g^{\circ L}(x_j)-2^L|x-x_j|$ (a strict peak) for odd $j$, and
$g^{\circ L}(x_j)+2^L|x-x_j|$ (a strict valley) for even $j$. Hence every minimal
partition contains the $2^L-1$ points
$x_1,\dots,x_{2^L-1}$ among its $c_i$'s, so $P-1\ge2^L-1$, i.e. $g^{\circ L}$ has at
least $2^L$ pieces. (2 pts) (In fact it has exactly $2^L+2$, counting the two constant
tails — matches Lecture 2's count $2+2^L$ for an $(L{+}1)$-layer sawtooth.)
*Traps:* counting monotone segments/"swings" between values $0$ and $1$ only forces
$\approx2^{L-1}$ pieces (a single affine piece can serve a whole swing) — the
extremum-must-be-a-breakpoint argument is what gives $2^L$; using a non-minimal
partition to *lower*-bound $P$ (Def. 1 is a minimum — one must show every valid
partition is large).

**5. (6)** (i) If $h\in\mathcal N_{B,1}$ and $h\equiv g^{\circ L}$: by sub-part 2, $h$
has $\le B+1$ pieces; being the same function as $g^{\circ L}$ it has $\ge 2^L$ pieces
(sub-part 4). Hence $B+1\ge2^L$, i.e. $B\ge2^L-1$. (3 pts)
(ii) If $h\in\mathcal N_{w,L'}$ and $h\equiv g^{\circ L}$: by sub-part 3,
$(w+1)^{L'}\ge2^L$; taking $\ln$: $L'\ge L\ln2/\ln(w+1)$. (2 pts)
Sentence (1 pt), e.g.: since $g^{\circ L}\in\mathcal N_{3,L}$ (3L hidden neurons),
replacing depth by width costs exponentially (width $\ge2^L-1$ at depth 1), whereas
replacing width by depth costs only a logarithmic factor — depth is exponentially more
efficient for this family (cf. Lecture 2, Prop. 2 / Telgarsky).
*Trap:* quoting the wrong direction of Prop. 1 (realizable-with-$\le B$-pieces vs.
realized-has-$\le B+1$-pieces).

**6. (10)** *Representation (4 pts).* Let $a$ := slope of $f$ on $(-\infty,t_1]$ and
$b$ := its intercept there (so $f(x)=ax+b$ for $x\le t_1$); let $a_j$ denote the slope
of $f$ on the $j$-th piece and set $c_i:=a_{i+1}-a_i$ (slope jumps). Define
$\varphi(x):=ax+b+\sum_{i=1}^{p-1}c_i[x-t_i]_+$. Then: $\varphi=f$ on
$(-\infty,t_1]$; on the interior of the $(j{+}1)$-st piece $(t_j,t_{j+1})$,
$\varphi'=a+\sum_{i\le j}c_i=a_1+\sum_{i=1}^{j}(a_{i+1}-a_i)=a_{j+1}=f'$ (telescoping).
So $\psi:=f-\varphi$ is continuous, vanishes on the first piece, and has zero
derivative on the interior of every piece $\Rightarrow$ $\psi$ is constant on each
piece, and by continuity the constants glue to $0$ across the breakpoints
$\Rightarrow$ $f\equiv\varphi$.
*Realization (3 pts).* $ax+b=a[x]_+-a[-x]_+ +b$, so
$$f(x)= a[x]_+ - a[-x]_+ + \sum\nolimits_{i=1}^{p-1}c_i[x-t_i]_+ + b$$
is a one-hidden-layer ReLU network with $(p-1)+2=p+1$ neurons and output bias $b$:
$f\in\mathcal N_{p+1,1}$. (Remark: writing $ax+b=a[x-t_1]_+-a[t_1-x]_+ +(at_1+b)$ and
merging the two $[x-t_1]_+$ terms gives width $p$ — the sharp constant of Prop. 1;
$p+1$ earns full credit.)
*Universality (3 pts).* Given continuous $f$ and $\epsilon>0$: by Lemma 1 (cited)
there is a PWL $g$ with $d(f,g)<\epsilon$; by the above $g$ is realized **exactly** by
some $h\in\mathcal N_{B,1}$ ($B$ = #pieces of $g$ + 1), so
$d(f,h)=d(f,g)<\epsilon$.
*Traps:* dropping the $ax+b$ term ($\sum_i c_i[x-t_i]_+$ vanishes left of $t_1$, so it
cannot match a general $f$); concluding $f\equiv\varphi$ from equal slopes without
gluing the piecewise constants via continuity and the anchor on the first piece;
forgetting that the affine term costs two neurons.

## Q2 — Gradient flow on a cubic reparameterization of linear regression (35)

**1. (7)** $L(z)=\frac12\sum_{n=1}^N\big(\sum_{j=1}^d X_{nj}z_j^3-y_n\big)^2$. By the
chain rule,
$$\frac{\partial L}{\partial z_i}
=\sum_{n=1}^N\Big(\sum_j X_{nj}z_j^3-y_n\Big)\cdot X_{ni}\cdot 3z_i^2
=3z_i^2\,\big(X^\top r\big)_i\,,\qquad r:=Xz^{\odot3}-y\,,$$
i.e. $\nabla L(z)=3\,z^{\odot2}\odot(X^\top r)$, and gradient flow is
$\dot z=-3\,z^{\odot2}\odot(X^\top r)$. (Equivalent full-credit route: directional
derivative with $(z+su)^{\odot3}=z^{\odot3}+3s\,z^{\odot2}\odot u+O(s^2)$, then
$\frac{d}{ds}L(z+su)\big|_{s=0}=\langle X(3z^{\odot2}\odot u),r\rangle
=\langle u,\,3z^{\odot2}\odot(X^\top r)\rangle$, using
$\langle a\odot b,c\rangle=\langle b,a\odot c\rangle$.)
*Credit:* 4 a genuine derivation (indices or directional); 3 correct vector assembly.
*Traps:* missing the factor $3$; $X r$ instead of $X^\top r$; sign of $r$.

**2. (10)** Fix $i$ with $z_i(0)=0$ and let $z(\cdot)$ be the (assumed unique)
solution. Define the continuous function $a(t):=-3\big(X^\top r(t)\big)_i$ along the
trajectory. Then $\psi(t):=z_i(t)$ satisfies the scalar ODE
$$\dot\psi(t)=a(t)\,\psi(t)^2\,,\qquad \psi(0)=0\,,$$
whose right-hand side is continuous in $t$ and continuously differentiable in $\psi$.
The zero function is a solution; by the granted scalar uniqueness (Picard–Lindelöf),
it is *the* solution, so $z_i(t)=\psi(t)=0$ for all $t\ge0$. (6 pts. Alternative full
credit: solve the flow of the reduced objective on the coordinates of
$\operatorname{supp}(z_0)$, extend by zeros, verify the extension solves the full ODE
— every zero coordinate has identically zero derivative — and invoke uniqueness of the
full flow.)
Consequently $\operatorname{supp}(z(t))\subseteq\operatorname{supp}(z_0)$, and since
$w(t)=z(t)^{\odot3}$ has the same support,
$\operatorname{supp}(w(t))\subseteq\operatorname{supp}(z_0)$ for all $t$ (and for any
limit point). (2 pts)
Implicit-regularization sentence (2 pts), e.g.: without any explicit penalty, the
optimizer–parameterization pair constrains the reachable minimizers — here gradient
flow implicitly controls the *sparsity* ($\ell_0$-support) of the learned predictor,
never exceeding the support of the initialization; this is implicit regularization in
the sense of Lecture 7 (simple = sparse, rather than min-$\ell_2$-norm / max-margin).
*Traps:* "the derivative at $0$ is $0$, hence it never moves" — first-order reasoning
at a single time proves nothing without uniqueness (e.g. $\dot\psi=3\psi^{2/3}$,
$\psi(0)=0$ has both $\psi\equiv0$ and $\psi=t^3$: RHS vanishes at $0$ but is not
Lipschitz); circular use of $z_i\equiv0$ to prove $\dot z_i\equiv0$.

**3. (8)** $L(z)=\frac12(z^3-1)^2$, $L'(z)=3z^2(z^3-1)$; critical points $z\in\{0,1\}$.
$L(1)=0$ is the global minimum while $L(0)=\frac12>0$, so $z=0$ is a critical point
that is not a global minimum; by the reminder, $L$ is not convex. (5 pts. Alternative
full credit: explicit chord violation, e.g.
$L\big(\tfrac{0+1}{2}\big)=\tfrac12(\tfrac18-1)^2=\tfrac{49}{128}>\tfrac14
=\tfrac{L(0)+L(1)}{2}$.)
Degeneracy (3 pts): $L''(z)=15z^4-6z$, so $L''(0)=0$ — no negative curvature at the
origin; indeed $L(z)-L(0)=-z^3+\tfrac12 z^6$ changes sign at $0$, so the origin is a
saddle-type critical point with a *vanishing* Hessian, exactly the flat, non-strict
degeneracy that Prop. 3 of Lecture 3 exhibits at the origin of depth-$\ge3$ linear
networks (here $w=z^3$ plays the role of a depth-3 diagonal network) — the reason a
landscape argument fails and sub-part 4 analyzes the trajectory instead.
*Traps:* checking only $L''$ at one point to "prove" non-convexity ($L''(0)=0$ alone
does not disprove convexity — must exhibit a non-global critical point or a chord
violation); claiming $z=0$ is a local maximum (it is neither a max nor a min).

**4. (10)** The flow is $\dot z=-L'(z)=-3z^2(z^3-1)=:\varphi(z)$.
- *Sign (2 pts):* for $z\in(0,1)$: $z^2>0$ and $z^3-1<0$, so $\varphi(z)>0$.
- *Confinement (3 pts):* $\hat z\equiv1$ solves the ODE ($\varphi(1)=0$). If
  $z(t^*)=1$ for some finite $t^*$, two distinct solutions pass through the point
  $(t^*,1)$, contradicting uniqueness; hence $z(t)\ne1$ for all $t$. Let
  $T:=\sup\{t\ge0: z(s)\in(0,1)\ \forall s\in[0,t]\}$. On $[0,T)$, $\dot z>0$, so $z$
  is strictly increasing and $z(t)\in[\alpha,1)$. If $T<\infty$, continuity gives
  $z(T)\in[\alpha,1]\setminus(0,1)=\{1\}$ — contradiction. So $T=\infty$: for all
  $t\ge0$, $z$ is strictly increasing with $\alpha\le z(t)<1$.
- *Limit is an equilibrium (3 pts):* monotone + bounded $\Rightarrow$
  $z(t)\uparrow z_\infty\in(\alpha,1]$. By continuity
  $\dot z(t)=\varphi(z(t))\to\varphi(z_\infty)$. If $\varphi(z_\infty)=c>0$, then
  $\dot z\ge c/2$ for all large $t$, whence $z(t)\to\infty$ — contradicting
  boundedness. So $\varphi(z_\infty)=0$.
- *Identification (2 pts):* the equilibria are $z\in\{0,1\}$; since
  $z_\infty>\alpha>0$, $z_\infty=1$. By continuity of $L$,
  $L(z(t))=\tfrac12(z(t)^3-1)^2\to L(1)=0$.

*Traps:* "$z$ stays below 1 because $\dot z=0$ there" without invoking uniqueness (a
barrier needs the constant-solution/uniqueness argument); asserting "the limit of
gradient flow is a critical point" without justification — a precise citation of the
recitation result that proves it (Recitation: Optimization Exercises 1, P5) earns
full credit per the front-matter rules; forgetting to rule out $z_\infty=0$.

## Q3 — Generalization via a cover of the parameter ball (30)

**1. (7)** *One dimension (4 pts):* let $k:=\lceil1/\epsilon\rceil$ and
$$T:=\big\{\min(-1+2\epsilon j,\ 1)\ :\ j=0,1,\dots,k\big\}\subseteq[-1,1]\,,\qquad
|T|\le k+1\,.$$
Covering: the uncapped grid points $-1+2\epsilon j$ have spacing $2\epsilon$ and reach
$-1+2\epsilon k\ge1$; hence every $\alpha\in[-1,1]$ is within $\epsilon$ of some
uncapped grid point $\gamma$. If $\gamma\le1$ then $\gamma\in T$; if $\gamma>1$ then
$1=\min(\gamma,1)\in T$ and $|\alpha-1|<|\alpha-\gamma|\le\epsilon$ (as
$\alpha\le1<\gamma$). Either way $\alpha$ is within $\epsilon$ of a point of $T$.
*Product (3 pts):* set $C_\epsilon:=T^d\subseteq\mathcal B$; then
$|C_\epsilon|=|T|^d\le(\lceil1/\epsilon\rceil+1)^d$, and for $w\in\mathcal B$ choosing
$\tilde w$ coordinatewise gives
$\|w-\tilde w\|_\infty=\max_i|w_i-\tilde w_i|\le\epsilon$.
*Traps:* grid spacing $\epsilon$ instead of $2\epsilon$ (a radius-$\epsilon$ ball
covers an interval of length $2\epsilon$) gives $\sim(2/\epsilon)^d$ points and
misses the required size; cover points falling outside $[-1,1]^d$ (the statement
requires $C_\epsilon\subseteq\mathcal B$ — clamp or shift).

**2. (8)** Fix $\tilde w\in C_\epsilon$ — a *data-independent* hypothesis (the cover
is built before seeing $S$; this is what legitimizes Hoeffding). The random variables
$A_n:=\ell(h_{\tilde w}(x_n),y_n)$, $n\in[N]$, are i.i.d. (functions of the i.i.d.
$(x_n,y_n)$), bounded in $[0,1]$, with $\mathbb E[A_1]=L_D(\tilde w)$ and
$\frac1N\sum_nA_n=L_S(\tilde w)$. (3 pts)
Hoeffding with $t:=\Delta_\epsilon(N,\delta)$ and $K:=\lceil1/\epsilon\rceil+1$:
$$P\big(|L_S(\tilde w)-L_D(\tilde w)|\ge t\big)\le2\exp(-2Nt^2)
=2\exp\big(-d\ln K-\ln(2/\delta)\big)=\delta\,K^{-d}\,. \quad(2\text{ pts})$$
Union bound over $C_\epsilon$ ($|C_\epsilon|\le K^d$): the probability that *some*
$\tilde w\in C_\epsilon$ violates the bound is $\le|C_\epsilon|\cdot\delta K^{-d}\le\delta$;
on the complement, all $\tilde w\in C_\epsilon$ satisfy it simultaneously. (3 pts)
*Traps:* applying Hoeffding to a sample-dependent $w$ (the entire point of the cover
is to avoid that); dropping the factor $2$ (two-sided bound) from $\ln(2/\delta)$;
treating $|C_\epsilon|=K^d$ as exact — only $\le$ is available, which is fine since
the failure bound is increasing in the class size.

**3. (8)** Let $w\in\mathcal B$ and pick $\tilde w\in C_\epsilon$ with
$\|w-\tilde w\|_\infty\le\epsilon$ (sub-part 1). Pointwise, for every $(x,y)$:
$|\ell(h_w(x),y)-\ell(h_{\tilde w}(x),y)|\le\rho\|w-\tilde w\|_\infty\le\rho\epsilon$.
(2 pts) Averaging over the sample and over $D$ respectively:
$$|L_S(w)-L_S(\tilde w)|\le\rho\epsilon\,,\qquad
|L_D(w)-L_D(\tilde w)|=\big|\mathbb E[\ell_w-\ell_{\tilde w}]\big|
\le\mathbb E\big|\ell_w-\ell_{\tilde w}\big|\le\rho\epsilon\,. \quad(3\text{ pts})$$
On the single event of sub-part 2 (probability $\ge1-\delta$, independent of which $w$
we consider), for **every** $w\in\mathcal B$ simultaneously:
$$L_D(w)-L_S(w)=\underbrace{\big[L_D(w)-L_D(\tilde w)\big]}_{\le\rho\epsilon}
+\underbrace{\big[L_D(\tilde w)-L_S(\tilde w)\big]}_{\le\Delta_\epsilon(N,\delta)}
+\underbrace{\big[L_S(\tilde w)-L_S(w)\big]}_{\le\rho\epsilon}
\le\Delta_\epsilon(N,\delta)+2\rho\epsilon\,. \quad(3\text{ pts})$$
*Traps:* paying only one $\rho\epsilon$ (both the population and the empirical side
transfer); re-applying probability per $w$ (the event must be fixed once — this is
what "uniform" means); Jensen is not even needed, just $|\mathbb E[\cdot]|\le\mathbb E|\cdot|$.

**4. (7)** Choose $\epsilon:=\min\big\{1,\ \tfrac{1}{\rho\sqrt N}\big\}\in(0,1]$.
(3 pts for any valid explicit choice + explicit bound.) For $N\ge1/\rho^2$ this gives
$2\rho\epsilon=2/\sqrt N$ and
$$\Delta(N,\delta)=
\sqrt{\frac{d\,\ln\!\big(\lceil\rho\sqrt N\rceil+1\big)+\ln(2/\delta)}{2N}}
\;+\;\frac{2}{\sqrt N}\,.$$
Vanishing (4 pts): $\lceil\rho\sqrt N\rceil+1\le\rho\sqrt N+2$, so the first term is
$\le\sqrt{\big(d\ln(\rho\sqrt N+2)+\ln(2/\delta)\big)/(2N)}\to0$ as $N\to\infty$
(since $\ln N/N\to0$ and $d,\rho,\delta$ are fixed), and $2/\sqrt N\to0$. Altogether
$\Delta(N,\delta)=O\Big(\sqrt{d\ln(\rho N+2)/N}+\sqrt{\ln(2/\delta)/N}\Big)
\xrightarrow[N\to\infty]{}0$.
(Any $\epsilon(N)\in(0,1]$ with $\rho\epsilon(N)\to0$ and $d\ln(1/\epsilon(N))/N\to0$
— e.g. $\epsilon=1/\sqrt N$ — earns full credit provided the limit is proved, not
asserted.)
*Traps:* leaving $\epsilon$ in the final bound; choosing $\epsilon$ constant (the
$2\rho\epsilon$ term then does not vanish); ignoring the constraint $\epsilon\le1$
for small $N$ (handled by the $\min$, or by stating the bound for $N$ large enough).

## Grading notes
- Total 105; per-part partial credit as marked. Hints used during the attempt: −20%
  of that sub-part.
- Common traps to check: Q1.1 additive piece counting; Q1.3 no common partition
  (weaker $(2w)^L$-type bound caps at half credit); Q1.4 swing-counting instead of the
  strict-extremum argument; Q1.6 missing affine term or ungrounded $f\equiv\varphi$;
  Q2.1 quoting the gradient without derivation; Q2.2 zero-preservation without a
  uniqueness argument; Q2.4 barrier at $1$ or "limit is an equilibrium" asserted
  without proof; Q3.1 cover of the wrong radius/size or points outside the ball;
  Q3.2 Hoeffding on a data-dependent hypothesis or missing union bound; Q3.3 a single
  $\rho\epsilon$; Q3.4 non-vanishing or non-explicit $\epsilon$.
- Cross-references for review after grading: Q1 ↔ Lecture 2 §1 (Prop. 1, Prop. 2,
  Lemma 1); Q2 ↔ Lecture 3 (Prop. 3), Lecture 7 (implicit regularization) and the
  gradient-flow recitation; Q3 ↔ Lecture 6 §2.1 and Exam 2023 Moed A Q3 (function-class
  covering — compare the two discretizations).
