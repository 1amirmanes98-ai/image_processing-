# Mock Exam 1 — Reinforcement Learning

generated 2026-07-08 · 3 hours · one A4 double-sided aid sheet + calculator · 4 questions · 100 points

This mock follows the standard template of the course finals: Q1 Planning (model an
MDP and solve it), Q2 Learning (a model-free update by hand), Q3 Approximation (policy
gradient), Q4 Bandits (a regret bound). Try each question fully before opening its
solution.

## Question 1 (30 pts) — Machine maintenance: model the MDP and solve it

A machine is, each morning, in one of two states: **Working** ($W$) or **Broken** ($B$).
The discount factor is $\gamma = 0.9$.

- If the machine is **Working**, you choose one of two actions:
  - **run**: earn reward $10$; the machine stays $W$ with probability $0.7$ and breaks to
    $B$ with probability $0.3$.
  - **service**: earn reward $4$; the machine stays $W$ with probability $1$.
- If the machine is **Broken**, the only action is **repair**: reward $-3$, and the machine
  returns to $W$ with probability $1$.

The objective is to maximize the expected discounted return $\sum_{t\ge0}\gamma^t r_t$.

**(a) [8 pts]** Formalize the problem as an MDP: give $S$, $A$ (per state), the reward
function $R(s,a)$, and the transition kernel $P(s'\mid s,a)$.

**(b) [6 pts]** Write the Bellman optimality equations for $V^*(W)$ and $V^*(B)$.

**(c) [8 pts]** Run value iteration from $V_0\equiv 0$ for **two** iterations. Report
$V_1(W),V_1(B)$ and $V_2(W),V_2(B)$, and state the greedy action in $W$ at each iteration.

**(d) [8 pts]** It turns out the optimal policy is $\pi^*(W)=\text{run}$, $\pi^*(B)=\text{repair}$.
Solve the linear system for the value of this policy and report $V^*(W),V^*(B)$ to two
decimals. Confirm that in state $W$, **run** is at least as good as **service**.

## Question 2 (20 pts) — TD(0) versus Monte-Carlo on one episode

Consider a chain $s_1\to s_2\to s_3\to\text{terminal}$. You observe a **single episode** with
transition rewards
$$r(s_1\to s_2)=2,\qquad r(s_2\to s_3)=1,\qquad r(s_3\to\text{terminal})=5.$$
Use $\gamma=1$, step size $\alpha=0.5$, and initialize $V_0(s)=0$ for all states.

**(a) [10 pts]** Run **TD(0)** over the episode, updating the states in the order they are
visited ($s_1$, then $s_2$, then $s_3$). Show each update and give the resulting
$V(s_1),V(s_2),V(s_3)$.

**(b) [6 pts]** Compute the **first-visit Monte-Carlo** value estimates of $s_1,s_2,s_3$ from
this same episode.

**(c) [4 pts]** The two methods disagree after one episode. Explain why, in terms of
bootstrapping and bias.

## Question 3 (20 pts) — Policy gradient for a softmax policy

There are two actions $a_1,a_2$ with feature vectors $\phi(s,a_1)=(1,0)^\top$ and
$\phi(s,a_2)=(0,1)^\top$. The policy is the softmax
$$\pi(a\mid s;\theta)=\frac{e^{\theta^\top\phi(s,a)}}{\sum_{a'}e^{\theta^\top\phi(s,a')}},
\qquad \theta=(\theta_1,\theta_2)^\top.$$

**(a) [8 pts]** Show that the score function is
$\nabla_\theta \log\pi(a\mid s;\theta)=\phi(s,a)-\mathbb{E}_{a'\sim\pi(\cdot\mid s)}[\phi(s,a')]$.

**(b) [6 pts]** At $\theta=(0.5,\,0)^\top$, compute the action probabilities $\pi(\cdot\mid s)$
and the score $\nabla_\theta\log\pi(a_1\mid s)$.

**(c) [6 pts]** You sample action $a_1$ and observe return $G=3$. Perform one REINFORCE update
$\theta\leftarrow\theta+\eta\,G\,\nabla_\theta\log\pi(a_1\mid s)$ with step size $\eta=0.1$;
give the new $\theta$.

## Question 4 (30 pts) — Regret of explore-then-commit (2 arms)

Two arms give rewards in $[0,1]$ (hence $\tfrac12$-sub-Gaussian). Their means differ by a gap
$\Delta=\mu^\star-\mu_{\text{other}}>0$ (unknown to the algorithm). Over a horizon $T$, the
**explore-then-commit** algorithm pulls **each** arm $m$ times ($2m$ exploration pulls), then
commits to the arm with the higher empirical mean for all remaining $T-2m$ pulls. Regret is
$\mathrm{Reg}(T)=\sum_{t}(\mu^\star-\mu_{a_t})$.

**(a) [6 pts]** Show the exploration phase incurs regret exactly $m\Delta$.

**(b) [10 pts]** Using Hoeffding's inequality on the difference of the two empirical means,
show the probability of committing to the **wrong** arm is at most $\exp(-m\Delta^2/4)$.

**(c) [6 pts]** Conclude that $\mathrm{Reg}(T)\le m\Delta + T\,\Delta\,\exp(-m\Delta^2/4)$.

**(d) [8 pts]** Choose $m$ to (nearly) minimize this bound. Give the optimizing $m$ (up to
rounding) and show the resulting regret is $O\!\big(\tfrac{1}{\Delta}\log(T\Delta^2)\big)$.
