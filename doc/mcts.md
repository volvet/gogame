# Monte Carlo Tree Search

Monte Carlo Tree Search is a method for finding optimal decisions in a given domain by taking random samples in the decision space and building a search tree according to the result.

A tree is built in an incremental and asymmetric manner. For each iteration of the algorithm, a tree policy is used to find the most urgent node of the current tree. The tree policy attempt to balance considerations of exploration and exploitation. 

A great benefit of MCTS is that the values of intermediate state do not have to be evauated as for depth-limited minimax search, which greatly reduce the amount of domain knowledge required. Only the value of the terminal state at the end of each simulation is required.

## Combinatorial Games
Games with two players that are zero-sum, perfect information, deterministic, decrete and sequential are described as *combinational games*.

## AI in Real Games
* **Minimax** attempts to minimize the opponent's maximum reward at each state,  and this is the traditional search approach for two-player combinatorial games. The search is typically stopped prematurely and a value function used to estimate the outcome of the game, and the $\alpha$-$\beta$ heuristic is typically used to prune the gtree.
* **Expectimax** generalies minimax to stochastic games in which the transitions from state to state are probabilistic.
* **Miximax** is similiar to single-player expectimax and is used primarily in games of imperfect information.

## Monte Carlo Methods
* Q-value
$$
Q(s, a) = \frac{1}{N(s, a)}\sum_{i=1}^{N(s)}\Pi_i(s,a)z_i
$$
Where $N(s, a)$ is the number of times action $a$ has been selected from state $s$.
      $N(s)$ is the number of times a game has been playout though state $s$.
      $z_i$ is the result $i$th simulcation playout from state $s$.
      $\Pi_i(s,a)$ is 1 if action $a$ is selected from the state $s$ on the $i$th simulcation from state $s$ or $0$ otherwise.


## Bandit Based Methods
* Regret
$$
R_N = \mu^*n - \mu_j \sum_{j=1}^KE[T_j(n)]
$$

* Upper Confidence Bouinds(UCB)
$$
UCB = \overline X_j + \sqrt{\frac{2\lnn}{n_j}
$$

## Reference
* A Survey of Monte Carlo Tree Search Mothods,   by Cameron Browne, etc.
