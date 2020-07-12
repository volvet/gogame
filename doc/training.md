# Training Efficiently with Adaptive Gradients

## Learning Rate Schedules
  Learning rate schedules seek to adjust learning rate during training by reducing the learning rate according to a pre-defined schedule. The Common learning schedules including time-based decay, step decay and exponential decay.
  
### Constant Learning Rate
  Constant learning rate is the default learning rate schedule in SGD Optimizer in Keras. Momentum and decay rate are both set to zero by default.
  
### Time-Based Decay
  The mathematical form of time-based decay is ```lr=lr0/(1+kt), where lr, k are hyperparameters and t is the iteration number```.
  
### Step Decay
  Step decay schedule drops the learning rate by a factor every few epochs. The methematical form of stop decay is
  ```
  lr = lr0 * drop^floor(epoch/epochs_drop)
  ```
### Exponential Decay
  The exponential decay has the methematical form is ```lr = lr0*e^(-kt), where k are hyperparameters and t is the ineration number```.

### Momentum
  

## Reference
* https://towardsdatascience.com/learning-rate-schedules-and-adaptive-learning-rate-methods-for-deep-learning-2c8f433990d1
* https://cnl.salk.edu/~schraudo/teach/NNcourse/momrate.html
