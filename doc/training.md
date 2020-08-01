# Training Efficiently with Adaptive Gradients

## Learning Rate Schedules
  Learning rate schedules seek to adjust learning rate during training by reducing the learning rate according to a pre-defined schedule. The Common learning schedules including time-based decay, step decay and exponential decay.  

### Decay and Momentum in SGD
  If $w$ is a paramter vector that you want to update, $\partial w$ is the current gradient computed for $w$, if the last update you used is $u$, then the next update will be as follow:
$$
  w = w - \alpha(\gamma u + (1+\gamma)\partial w)
$$
  
### Adagrad and Adadelta

$$
E[g^2]_t = E[g^2]_{t-1}
$$

## Reference
* https://ruder.io/optimizing-gradient-descent/
