# Mock Exam 1 — Solutions

All numeric answers below were verified with a `python3`/numpy computation.

## Q1 — Machine maintenance MDP

**(a)** $S=\{W,B\}$. Actions: $A(W)=\{\text{run},\text{service}\}$, $A(B)=\{\text{repair}\}$.
Rewards: $R(W,\text{run})=10$, $R(W,\text{service})=4$, $R(B,\text{repair})=-3$.
Transitions: $P(W\mid W,\text{run})=0.7,\ P(B\mid W,\text{run})=0.3$; $P(W\mid W,\text{service})=1$;
$P(W\mid B,\text{repair})=1$. Objective: maximize $\mathbb{E}\sum_{t\ge0}\gamma^t r_t$, $\gamma=0.9$.

**(b)**
$$V^*(W)=\max\Big\{\,10+\gamma\big(0.7\,V^*(W)+0.3\,V^*(B)\big),\ \ 4+\gamma V^*(W)\,\Big\},\qquad
V^*(B)=-3+\gamma V^*(W).$$

**(c)** Value iteration from $V_0\equiv0$:
- **Iter 1:** $Q(W,\text{run})=10+0.9(0)=10$, $Q(W,\text{service})=4+0.9(0)=4\Rightarrow V_1(W)=10$ (greedy = **run**).
  $Q(B,\text{repair})=-3+0.9(0)=-3\Rightarrow V_1(B)=-3$.
- **Iter 2:** $Q(W,\text{run})=10+0.9(0.7\cdot10+0.3\cdot(-3))=10+0.9(6.1)=15.49$,
  $Q(W,\text{service})=4+0.9\cdot10=13\Rightarrow V_2(W)=15.49$ (greedy = **run**).
  $Q(B,\text{repair})=-3+0.9\cdot10=6\Rightarrow V_2(B)=6$.

(For reference, iteration 3 gives $V_3(W)=21.38$; the sequence increases monotonically to $V^*$.)

**(d)** With $\pi(W)=\text{run},\ \pi(B)=\text{repair}$ the value solves
$$V(W)=10+0.9\big(0.7V(W)+0.3V(B)\big),\qquad V(B)=-3+0.9V(W).$$
Substituting the second into the first: $V(W)=10+0.63V(W)+0.27(-3+0.9V(W))$, i.e.
$V(W)(1-0.63-0.243)=10-0.81\Rightarrow 0.127\,V(W)=9.19\Rightarrow \boxed{V^*(W)=72.36}$, and
$\boxed{V^*(B)=-3+0.9\cdot72.36=62.13}$. Check in $W$: run $=10+0.9(0.7\cdot72.36+0.3\cdot62.13)=72.36$
vs service $=4+0.9\cdot72.36=69.13$; run wins, consistent with $\pi^*(W)=\text{run}$.

## Q2 — TD(0) vs first-visit MC

**(a)** TD(0) update $V(s)\leftarrow V(s)+\alpha\big(r+\gamma V(s')-V(s)\big)$, in visit order:
- $s_1$: target $=2+V(s_2)=2$; $V(s_1)=0+0.5(2-0)=\mathbf{1.0}$.
- $s_2$: target $=1+V(s_3)=1$ (still $0$); $V(s_2)=0+0.5(1-0)=\mathbf{0.5}$.
- $s_3$: target $=5+V(\text{term})=5$; $V(s_3)=0+0.5(5-0)=\mathbf{2.5}$.

So after one episode TD(0) gives $V(s_1)=1.0,\ V(s_2)=0.5,\ V(s_3)=2.5$.

**(b)** First-visit MC uses the full return from each state ($\gamma=1$):
$G(s_1)=2+1+5=\mathbf{8}$, $G(s_2)=1+5=\mathbf{6}$, $G(s_3)=5=\mathbf{5}$. With one episode these
returns are the MC estimates.

**(c)** TD(0) **bootstraps**: each update uses the *current* estimate of the next state, which is
still $0$ after one pass, so the reward information has not yet propagated back — the values are
biased low and far from the true returns. MC uses the *actual* observed return, so after one
episode it already equals the true (sampled) return. TD is biased but low-variance and updates
online; MC is unbiased but high-variance. (True values here are $V(s_1)=8,V(s_2)=6,V(s_3)=5$;
TD converges to them over many episodes.)

## Q3 — Softmax policy gradient

**(a)** $\log\pi(a\mid s;\theta)=\theta^\top\phi(s,a)-\log\sum_{a'}e^{\theta^\top\phi(s,a')}$.
Differentiating, $\nabla_\theta\log\pi(a\mid s)=\phi(s,a)-\dfrac{\sum_{a'}e^{\theta^\top\phi(s,a')}\phi(s,a')}{\sum_{a'}e^{\theta^\top\phi(s,a')}}
=\phi(s,a)-\sum_{a'}\pi(a'\mid s)\phi(s,a')=\phi(s,a)-\mathbb{E}_{a'\sim\pi}[\phi(s,a')]$.

**(b)** Logits are $\theta^\top\phi(s,a_1)=0.5$, $\theta^\top\phi(s,a_2)=0$. So
$\pi(a_1)=\dfrac{e^{0.5}}{e^{0.5}+1}=\mathbf{0.6225}$, $\pi(a_2)=\mathbf{0.3775}$.
$\mathbb{E}_\pi[\phi]=0.6225(1,0)+0.3775(0,1)=(0.6225,0.3775)$, hence
$\nabla_\theta\log\pi(a_1\mid s)=(1,0)-(0.6225,0.3775)=\mathbf{(0.3775,\,-0.3775)}$.
(Finite-difference check confirms this to $10^{-4}$.)

**(c)** $\theta\leftarrow(0.5,0)+0.1\cdot3\cdot(0.3775,-0.3775)=(0.5,0)+(0.11325,-0.11325)
=\mathbf{(0.6133,\,-0.1133)}$. The update raises the probability of the rewarded action $a_1$.

## Q4 — Explore-then-commit regret

**(a)** During exploration each arm is pulled $m$ times. Pulling the optimal arm costs $0$ regret;
pulling the other arm costs $\Delta$ each. So exploration regret $=m\cdot\Delta$ exactly (the $m$
pulls of the sub-optimal arm), independent of what happens after.

**(b)** Let $\hat\mu_1,\hat\mu_2$ be the empirical means after $m$ pulls each. We commit wrongly iff
the empirical mean of the worse arm exceeds that of the best arm. The difference
$\hat\mu^\star-\hat\mu_{\text{other}}$ has mean $\Delta$ and, being a difference of two independent
$\tfrac12$-sub-Gaussian averages of $m$ samples, is $\sqrt{\tfrac{1}{2m}}$-sub-Gaussian, i.e.
variance proxy $\tfrac{1}{4m}+\tfrac{1}{4m}=\tfrac{1}{2m}$. Hoeffding gives
$\Pr[\hat\mu^\star-\hat\mu_{\text{other}}\le 0]\le\exp\!\Big(-\dfrac{\Delta^2}{2\cdot(1/(2m))\cdot 2}\Big)
=\exp(-m\Delta^2/4)$.

**(c)** If we commit correctly (prob $\ge 1-e^{-m\Delta^2/4}$) the commit phase adds $0$ regret;
if we commit wrongly (prob $\le e^{-m\Delta^2/4}$) each of the $\le T$ commit pulls costs $\le\Delta$.
Adding the exploration regret from (a):
$$\mathrm{Reg}(T)\le m\Delta + (T-2m)\Delta\,e^{-m\Delta^2/4}\le m\Delta+T\Delta\,e^{-m\Delta^2/4}.$$

**(d)** Balance the two terms: set the exponential tail so $T\,e^{-m\Delta^2/4}=O(1/\Delta)$-scale, i.e.
choose $m=\Big\lceil \dfrac{4}{\Delta^2}\log\!\big(\tfrac{T\Delta^2}{4}\big)\Big\rceil$. Then
$T\Delta e^{-m\Delta^2/4}\le \tfrac{4}{\Delta}$, and the exploration term is
$m\Delta=\tfrac{4}{\Delta}\log(\tfrac{T\Delta^2}{4})$, giving
$$\mathrm{Reg}(T)=O\!\Big(\tfrac{1}{\Delta}\log(T\Delta^2)\Big).$$
Numeric check at $T=10^5,\ \Delta=0.1$: the bound is minimized at $m^\star=2209$ (theory
$\tfrac{4}{\Delta^2}\log(\tfrac{T\Delta^2}{4})=2208.6$), giving regret $\approx 261$ — matching the
$\tfrac{4}{\Delta}\log(\tfrac{T\Delta^2}{4})\approx 221$ scaling (same order).
