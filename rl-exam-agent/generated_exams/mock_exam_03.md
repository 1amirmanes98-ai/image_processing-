# Mock Exam 3 — Reinforcement Learning

generated 2026-07-08 · 3 hours · one A4 double-sided aid sheet + calculator · 4 questions · 100 points

Standard-template mock, with problems adapted from the course exercise booklet: Q1 Planning
(a stopping-game MDP with a slick invariant), Q2 Learning (TD(λ) with eligibility traces),
Q3 Approximation (a multi-step Bellman operator), Q4 Bandits (successive-elimination regret).

## Question 1 (30 pts) — The red-card game

A shuffled deck has $b$ black and $r$ red cards. Cards are revealed one at a time. At any
moment (before a card is revealed) you may **stop** and bet that the *next* card is **red**;
you win if it is. You must bet before the deck runs out. You see the colors of already-revealed
cards.

**(a) [8 pts]** Model this as a finite-horizon MDP: state, actions, reward, and horizon.

**(b) [14 pts]** Let $W(b,r)$ be the optimal winning probability with $b$ black and $r$ red
cards remaining. Write its Bellman equation, and **prove by induction on $b+r$ that
$W(b,r) = \dfrac{r}{b+r}$** — i.e. stopping *now* is already optimal, so **every** policy wins
with the same probability.

**(c) [8 pts]** Evaluate $W(2,3)$. What does the result say about clever "wait for a good moment"
strategies?

## Question 2 (20 pts) — TD(λ) with eligibility traces

Run **TD(λ)** with accumulating eligibility traces on the episode
$s_1 \to s_2 \to s_3 \to \text{terminal}$, with every transition reward $= 1$. Use $\gamma = 1$,
$\lambda = 0.5$, step size $\alpha = 0.5$, all $V(s) = 0$ and all traces $e(s) = 0$ initially.

At each step: $\delta = r + \gamma V(s') - V(s)$; increment $e(s)\mathrel{+}=1$; then for **all**
states $V(x)\mathrel{+}=\alpha\,\delta\,e(x)$ and decay $e(x)\mathrel{*}=\gamma\lambda$.

**(a) [14 pts]** Carry out the three steps, showing $\delta$ and the full $V$ vector after each.

**(b) [6 pts]** Give the final $V(s_1), V(s_2), V(s_3)$ and explain why states visited earlier
end up with larger values than plain TD(0) would give after one episode.

## Question 3 (20 pts) — A two-step Bellman operator

For a fixed policy $\pi$ with transition matrix $P$ and reward vector $r$, define the two-step
policy-evaluation operator
$$ (T^{\pi,2} v) = r + \gamma P r + \gamma^2 P^2 v. $$

**(a) [10 pts]** Prove $T^{\pi,2}$ is a **$\gamma^2$-contraction** in the max-norm, and hence has
a unique fixed point. Show that fixed point is $V^\pi$ (the ordinary value of $\pi$).

**(b) [10 pts]** Take $\gamma = 0.9$, $r = (1, 2, 0)^\top$, and
$P = \begin{pmatrix} 0.5 & 0.5 & 0\\ 0 & 0.5 & 0.5\\ 0 & 0 & 1\end{pmatrix}$
(state 3 absorbing). Compute $V^\pi = (I-\gamma P)^{-1} r$, confirm it is the fixed point of
$T^{\pi,2}$, and report the empirical contraction ratio you would observe.

## Question 4 (30 pts) — Successive elimination regret

Consider a stochastic $K$-armed bandit with rewards in $[0,1]$, a unique best arm, and gaps
$\Delta_i = \mu^\star - \mu_i > 0$ for each suboptimal arm $i$. **Successive elimination**
pulls all surviving arms equally and eliminates an arm once its upper confidence bound drops
below the best surviving lower confidence bound (Hoeffding confidence widths).

**(a) [10 pts]** Show that, with high probability, a suboptimal arm $i$ is eliminated after
being pulled $O\!\big(\tfrac{1}{\Delta_i^2}\log T\big)$ times. (State the Hoeffding width you use.)

**(b) [10 pts]** Conclude that the total (gap-dependent) regret is
$O\!\big(\sum_{i:\Delta_i>0} \tfrac{1}{\Delta_i}\log T\big)$.

**(c) [10 pts]** For $T = 10^5$ and a suboptimal arm with $\Delta_i = 0.2$, give the approximate
number of pulls of that arm and its contribution to the regret (use the constant $8$ in the
$\tfrac{8}{\Delta_i^2}\log T$ pull bound).
