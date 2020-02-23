# Monte Carlo Tree Search

Monte Carlo Tree Search is a method for finding optimal decisions in a given domain by taking random samples in the decision space and building a search tree according to the result.

A tree is built in an incremental and asymmetric manner. For each iteration of the algorithm, a tree policy is used to find the most urgent node of the current tree. The tree policy attempt to balance considerations of exploration and exploitation. 

A great benefit of MCTS is that the values of intermediate state do not have to be evauated as for depth-limited minimax search, which greatly reduce the amount of domain knowledge required. Only the value of the terminal state at the end of each simulation is required.


## Reference
* A Survey of Monte Carlo Tree Search Mothods,   by Cameron Browne, etc.
