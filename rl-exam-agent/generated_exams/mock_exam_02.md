# Mock Exam 2 — Reinforcement Learning

generated 2026-07-08 · 3 hours · one A4 double-sided aid sheet + calculator · 4 questions · 100 points

Standard-template mock, with problems adapted from the course exercise booklet:
Q1 Planning (optimal stopping), Q2 Learning (Q-learning by hand), Q3 Approximation
(policy gradient), Q4 Bandits (PAC best-arm). Try each fully before the hint or solution.

## Question 1 (30 pts) — Sequential job offers (optimal stopping)

Each period an unemployed engineer receives one job offer with salary $s$ drawn uniformly
from $\{10, 20, 30, 40\}$ (independently each period). If she **accepts** salary $s$, she
earns $s$ every period forever after — a value of $s/(1-\gamma)$ — and the process stops.
If she **rejects**, she waits one period (no reward) and draws a fresh offer next period.
The discount factor is $\gamma = 0.9$.

**(a) [8 pts]** Model this as an MDP / optimal-stopping problem: give the state, the two
actions, and the Bellman optimality equation. Let $W$ denote the value of *entering a period
before the offer is revealed*; write the fixed-point equation $W$ satisfies.

**(b) [10 pts]** Argue that the optimal policy is a **threshold** policy (accept iff
$s \ge s^\*$), and explain briefly why (monotonicity of the accept-vs-reject comparison in $s$).

**(c) [8 pts]** Solve for $W$ and the acceptance set. Which offers does she accept?

**(d) [4 pts]** Give $V^\*(s)$ for each $s \in \{10,20,30,40\}$.

## Question 2 (20 pts) — Q-learning by hand

An agent runs **Q-learning** ($\alpha = 0.5$, $\gamma = 0.9$, all $Q$ initialized to $0$) on
states $\{A, B, C\}$ with actions $\{x, y\}$. It observes the single trajectory

$$A \xrightarrow{\,x,\ r=5\,} B \xrightarrow{\,y,\ r=0\,} C \xrightarrow{\,x,\ r=10\,} \text{terminal}.$$

**(a) [14 pts]** Apply the Q-learning update
$Q(s,a) \leftarrow Q(s,a) + \alpha\big(r + \gamma \max_{a'} Q(s',a') - Q(s,a)\big)$ to each
transition in order. Show each update and give the resulting $Q$-table.

**(b) [6 pts]** Which entries are still $0$, and why? What would change on a second identical
pass through the trajectory?

## Question 3 (20 pts) — Gaussian policy gradient (continuous action)

A continuous-action policy is Gaussian, $\pi(a\mid s;\theta) = \mathcal{N}\!\big(a;\ \mu_\theta(s),\ \sigma^2\big)$
with mean $\mu_\theta(s) = \theta^\top \phi(s)$ and fixed $\sigma = 1$. Take
$\phi(s) = (1, 2)^\top$ and $\theta = (0.5, -0.5)^\top$.

**(a) [8 pts]** Derive the score $\nabla_\theta \log \pi(a\mid s;\theta)$.

**(b) [6 pts]** Compute $\mu_\theta(s)$ and evaluate the score at the sampled action $a = 1$.

**(c) [6 pts]** With observed return $G = 2$ and step size $\eta = 0.1$, perform one REINFORCE
update $\theta \leftarrow \theta + \eta\, G\, \nabla_\theta \log\pi(a\mid s;\theta)$; give the new $\theta$.

## Question 4 (30 pts) — PAC best-arm identification

You have $n = 10$ arms with unknown means in $[0,1]$. You want to output an arm whose mean is
within $\varepsilon = 0.1$ of the best, with failure probability at most $\delta = 0.05$
(an $(\varepsilon,\delta)$-PAC guarantee). The algorithm: **pull each arm $\ell$ times, then
output the arm with the highest empirical mean.**

**(a) [8 pts]** Using Hoeffding's inequality, bound the probability that a single arm's
empirical mean deviates from its true mean by more than $\varepsilon/2$.

**(b) [10 pts]** Via a union bound over all $n$ arms, choose $\ell$ so the algorithm is
$(\varepsilon,\delta)$-PAC. Give the smallest such $\ell$ (a formula, then a number).

**(c) [6 pts]** State the total sample complexity, and its $O(\cdot)$ dependence on
$n,\varepsilon,\delta$.

**(d) [6 pts]** Verify your $\ell$ makes the union-bound failure probability $\le \delta$
for $n=10,\varepsilon=0.1,\delta=0.05$.
