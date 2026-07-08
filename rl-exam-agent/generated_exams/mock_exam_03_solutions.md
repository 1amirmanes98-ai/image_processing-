# Mock Exam 3 — Solutions

Every numeric answer was verified with a `python3`/numpy computation.

## Q1 — The red-card game

**Hint:** Guess the answer $W(b,r)=r/(b+r)$ and prove it by induction on $b+r$. For the
"continue" action, condition on the color of the discarded card and use the inductive
hypothesis — the two terms telescope back to $r/(b+r)$.

**Full solution:**
**(a)** State $=(b,r)$ = cards of each color remaining; actions = {stop-and-bet-red, reveal-one-and-continue};
reward $1$ iff you stop and the next card is red, else $0$; horizon $\le b+r$ (you must bet before the deck empties).

**(b)** Bellman equation:
$$W(b,r)=\max\Big\{\underbrace{\tfrac{r}{b+r}}_{\text{stop, bet red}},\ \underbrace{\tfrac{b}{b+r}W(b-1,r)+\tfrac{r}{b+r}W(b,r-1)}_{\text{reveal one card, then continue}}\Big\}.$$
**Claim** $W(b,r)=\tfrac{r}{b+r}$. Induction on $n=b+r$. Base $n=1$: $W(0,1)=1,\ W(1,0)=0$, both $=r/(b+r)$.
Step: assume it holds for $n-1$. The continue value is
$$\tfrac{b}{b+r}\cdot\tfrac{r}{(b-1)+r}+\tfrac{r}{b+r}\cdot\tfrac{r-1}{b+(r-1)}
=\tfrac{1}{b+r}\Big(\tfrac{br}{b+r-1}+\tfrac{r(r-1)}{b+r-1}\Big)=\tfrac{1}{b+r}\cdot\tfrac{r(b+r-1)}{b+r-1}=\tfrac{r}{b+r}.$$
So stop and continue give the **same** value $r/(b+r)$; the max is $r/(b+r)$, and every action is optimal. $\square$

**(c)** $W(2,3)=\tfrac{3}{5}=\mathbf{0.6}$ (numerically verified via DP over the $(b,r)$ grid, matching $r/(b+r)$ exactly). No strategy beats the naive "bet immediately" probability $r/(b+r)$: waiting for a "good moment" cannot help, because the revealed-card process is a martingale for the fraction of red remaining.

## Q2 — TD(λ) with eligibility traces

**Hint:** Keep a trace vector. At each step compute $\delta$, bump the current state's trace to
$1$, then update **every** state by $\alpha\delta e(x)$ and decay all traces by $\gamma\lambda=0.5$.

**Full solution:**
**(a)** $\gamma=1,\lambda=0.5\Rightarrow \gamma\lambda=0.5$; $\alpha=0.5$. Every $\delta=1+V(s')-V(s)$.
- **Step $s_1\to s_2$:** $\delta=1+0-0=1$. Traces: $e=(1,0,0)$. Update: $V=(0.5,0,0)$. Decay: $e=(0.5,0,0)$.
- **Step $s_2\to s_3$:** $\delta=1+0-0=1$. Bump $e_2$: $e=(0.5,1,0)$. Update: $V=(0.5+0.5\cdot0.5,\ 0+0.5\cdot1,\ 0)=(0.75,0.5,0)$. Decay: $e=(0.25,0.5,0)$.
- **Step $s_3\to\text{term}$:** $\delta=1+0-0=1$. Bump $e_3$: $e=(0.25,0.5,1)$. Update: $V=(0.75+0.5\cdot0.25,\ 0.5+0.5\cdot0.5,\ 0+0.5\cdot1)=(0.875,0.75,0.5)$.

**(b)** Final $V(s_1)=\mathbf{0.875},\ V(s_2)=\mathbf{0.75},\ V(s_3)=\mathbf{0.5}$. Plain TD(0) after
one episode would give $V(s_1)=0.5,V(s_2)=0.5,V(s_3)=0.5$ (each state only gets its own one-step
reward). The eligibility traces let the later rewards flow back to earlier states within the same
episode, so $s_1$ (visited first, then kept "eligible") accumulates credit from all three
$\delta$'s — hence the larger value.

## Q3 — A two-step Bellman operator

**Hint:** For contraction, subtract two applications: $T^{\pi,2}u-T^{\pi,2}v=\gamma^2P^2(u-v)$ and
$\|P^2 x\|_\infty\le\|x\|_\infty$ (rows of $P^2$ are probability vectors). For the fixed point,
note $V^\pi=r+\gamma P V^\pi$, apply twice.

**Full solution:**
**(a)** $T^{\pi,2}u-T^{\pi,2}v=\gamma^2 P^2(u-v)$. Since $P$ (hence $P^2$) is row-stochastic,
$\|P^2 x\|_\infty\le\|x\|_\infty$, so $\|T^{\pi,2}u-T^{\pi,2}v\|_\infty\le\gamma^2\|u-v\|_\infty$ —
a $\gamma^2$-contraction, unique fixed point by Banach. $V^\pi$ satisfies $V^\pi=r+\gamma PV^\pi$;
substituting once into itself, $V^\pi=r+\gamma P(r+\gamma PV^\pi)=r+\gamma Pr+\gamma^2P^2V^\pi=T^{\pi,2}V^\pi$.
So $V^\pi$ is the fixed point.

**(b)** $V^\pi=(I-\gamma P)^{-1}r=\mathbf{(4.7934,\ 3.6364,\ 0)}$. Iterating $T^{\pi,2}$ from $v=0$
converges to the same vector (verified). The observed contraction ratio
$\|T^{\pi,2}u-T^{\pi,2}w\|_\infty/\|u-w\|_\infty = 0.81 = \gamma^2$, exactly as proved.

## Q4 — Successive elimination regret

**Hint:** After $m$ pulls each, Hoeffding gives confidence width $\sqrt{\tfrac{2\log T}{m}}$ (up to
constants). Arm $i$ is safely eliminated once this width shrinks below $\Delta_i/2$, i.e.
$m=\Theta(\log T/\Delta_i^2)$. Each such pull costs $\Delta_i$ regret.

**Full solution:**
**(a)** On the "clean event" (all confidence intervals valid, prob $\ge 1-1/T$-ish by a union
bound), with $m$ pulls each arm's empirical mean is within $c_m=\sqrt{\tfrac{2\log T}{m}}$ of its
true mean. Once $c_m<\Delta_i/2$, the best arm's LCB exceeds arm $i$'s UCB, so $i$ is eliminated.
That threshold is $m=O\!\big(\tfrac{\log T}{\Delta_i^2}\big)$ pulls of arm $i$.

**(b)** Arm $i$ contributes regret (pulls)$\times\Delta_i=O\!\big(\tfrac{\log T}{\Delta_i^2}\big)\cdot\Delta_i
=O\!\big(\tfrac{\log T}{\Delta_i}\big)$. Summing over suboptimal arms:
$\mathrm{Reg}(T)=O\!\big(\sum_{i:\Delta_i>0}\tfrac{1}{\Delta_i}\log T\big)$ (plus the low-probability
"bad event" contributing $O(1)$).

**(c)** With the constant $8$: pulls $\approx\tfrac{8}{\Delta_i^2}\log T=\tfrac{8}{0.04}\ln(10^5)=200\cdot11.51=\mathbf{2303}$.
Regret contribution $=\Delta_i\times\text{pulls}=\tfrac{8}{\Delta_i}\log T=40\cdot11.51\approx\mathbf{460}$.
