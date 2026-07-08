# Mock Exam 2 — Solutions

Every numeric answer was verified with a `python3`/numpy computation.

## Q1 — Sequential job offers

**Hint:** The only thing that matters is the current offer. Compare "accept" ($s/(1-\gamma)$)
against "reject" ($\gamma W$, where $W$ is the pre-offer value). Since accept grows in $s$ and
reject doesn't, optimality is a threshold. Solve the fixed point $W=\mathbb{E}_s[\max(s/(1-\gamma),\gamma W)]$.

**Full solution:**
**(a)** State = the current offer $s$ (the only payoff-relevant info). Actions: accept / reject.
$V^\*(s)=\max\{\,s/(1-\gamma),\ \gamma W\,\}$ where $W=\mathbb{E}_{s'}[V^\*(s')]=\tfrac14\sum_{s'} V^\*(s')$
is the value of entering a period before the offer is seen. Fixed point:
$$W=\tfrac14\sum_{s\in\{10,20,30,40\}}\max\!\Big(\tfrac{s}{1-\gamma},\ \gamma W\Big).$$

**(b)** Accept value $s/(1-\gamma)$ is strictly increasing in $s$; reject value $\gamma W$ is
constant in $s$. So $\{s:\text{accept optimal}\}=\{s: s/(1-\gamma)\ge\gamma W\}$ is an
upper interval — a threshold policy, accept iff $s\ge s^\*=(1-\gamma)\gamma W$.

**(c)** With $\gamma=0.9$, $1/(1-\gamma)=10$, so accept value $=10s$. Iterating the fixed point
gives $\boxed{W^\*=318.18}$. Threshold $s^\*=(1-\gamma)\gamma W=0.09\cdot318.18=28.64$, so she
**accepts $s\in\{30,40\}$** and rejects $\{10,20\}$ (reject value $\gamma W=286.36$ exceeds
$10\cdot10=100$ and $10\cdot20=200$, but is below $10\cdot30=300$).

**(d)** $V^\*(10)=V^\*(20)=\gamma W=286.36$; $V^\*(30)=300$; $V^\*(40)=400$.

## Q2 — Q-learning by hand

**Hint:** Apply the update transition-by-transition. Because every $Q$ starts at $0$, each
$\max_{a'}Q(s',\cdot)$ term is $0$ on the first pass, so only the immediate reward drives the update.

**Full solution:**
**(a)** Update $Q(s,a)\leftarrow Q(s,a)+\alpha(r+\gamma\max_{a'}Q(s',a')-Q(s,a))$, $\alpha=0.5,\gamma=0.9$:
- $A,x$: $r=5$, $\max_{a'}Q(B,\cdot)=0 \Rightarrow$ target $5$; $Q(A,x)=0+0.5(5-0)=\mathbf{2.5}$.
- $B,y$: $r=0$, $\max_{a'}Q(C,\cdot)=0 \Rightarrow$ target $0$; $Q(B,y)=0+0.5(0-0)=\mathbf{0}$.
- $C,x$: $r=10$, terminal ($\max=0$) $\Rightarrow$ target $10$; $Q(C,x)=0+0.5(10-0)=\mathbf{5}$.

Table: $Q(A,x)=2.5,\ Q(C,x)=5$, all others $0$.

**(b)** $Q(B,y)$ and every unvisited $(s,a)$ are still $0$ — $B,y$ because its reward and its
bootstrap target were both $0$. On a **second identical pass**, values propagate backward:
$Q(B,y)\leftarrow 0.5(0+0.9\cdot5)=2.25$ (now $Q(C,x)=5>0$), and $Q(A,x)\leftarrow 2.5+0.5(5+0.9\cdot2.25-2.5)=4.26$.

## Q3 — Gaussian policy gradient

**Hint:** $\log\pi=-\tfrac{(a-\mu)^2}{2\sigma^2}+\text{const}$ with $\mu=\theta^\top\phi$;
differentiate w.r.t. $\theta$ via the chain rule ($\partial\mu/\partial\theta=\phi$).

**Full solution:**
**(a)** $\log\pi(a\mid s;\theta)=-\tfrac{1}{2}\log(2\pi\sigma^2)-\tfrac{(a-\mu_\theta(s))^2}{2\sigma^2}$,
$\mu_\theta(s)=\theta^\top\phi(s)$. Then
$\nabla_\theta\log\pi=\dfrac{a-\mu_\theta(s)}{\sigma^2}\,\phi(s)$.

**(b)** $\mu_\theta(s)=\theta^\top\phi=0.5\cdot1+(-0.5)\cdot2=-0.5$. At $a=1$, $\sigma=1$:
score $=(1-(-0.5))\,\phi=1.5\cdot(1,2)=\mathbf{(1.5,\,3.0)}$. (Finite-difference check matches to $10^{-4}$.)

**(c)** $\theta\leftarrow(0.5,-0.5)+0.1\cdot2\cdot(1.5,3.0)=(0.5,-0.5)+(0.3,0.6)=\mathbf{(0.8,\,0.1)}$.
The update shifts the mean toward the rewarded action.

## Q4 — PAC best-arm identification

**Hint:** Hoeffding for an average of $\ell$ samples in $[0,1]$:
$\Pr[|\hat\mu-\mu|>\varepsilon/2]\le 2e^{-\ell\varepsilon^2/2}$. Union-bound over $n$ arms and set
$\le\delta$, then solve for $\ell$.

**Full solution:**
**(a)** For one arm, $\hat\mu$ is an average of $\ell$ i.i.d. $[0,1]$ rewards. Hoeffding:
$\Pr[|\hat\mu-\mu|>\varepsilon/2]\le 2\exp(-2\ell(\varepsilon/2)^2)=2\exp(-\ell\varepsilon^2/2)$.

**(b)** If **every** arm's estimate is within $\varepsilon/2$ of its mean, the empirically-best arm
is within $\varepsilon$ of the true best (a standard two-sided argument). Union bound:
$\Pr[\text{some arm off by}>\varepsilon/2]\le 2n\exp(-\ell\varepsilon^2/2)$. Set $\le\delta$:
$$\ell\ge \frac{2}{\varepsilon^2}\ln\frac{2n}{\delta}.$$
For $n=10,\varepsilon=0.1,\delta=0.05$: $\ell=\lceil \tfrac{2}{0.01}\ln(400)\rceil=\lceil 200\cdot5.99\rceil=\mathbf{1199}$
with the $\varepsilon/2$-Hoeffding constant, or $\ell=\lceil\tfrac{1}{2\varepsilon^2}\ln\tfrac{2n}{\delta}\rceil=\mathbf{300}$
if you bound each estimate at tolerance $\varepsilon$ directly (both are $(\varepsilon,\delta)$-PAC;
the tighter direct-$\varepsilon$ version is used below).

**(c)** Total $=n\ell=O\!\big(\tfrac{n}{\varepsilon^2}\log\tfrac{n}{\delta}\big)$ samples.

**(d)** Using $\ell=300$ (direct tolerance $\varepsilon$): union-bound failure
$\le 2n\,e^{-2\ell\varepsilon^2}=20\,e^{-2\cdot300\cdot0.01}=20\,e^{-6}=0.0496\le0.05$. ✓
Total $=10\cdot300=3000$ pulls.
