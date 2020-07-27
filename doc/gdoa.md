# 梯度下降优化算法概览
梯度下降是最流行的优化算法, 尤其是在神经网络优化中得到了广泛应用. 当前的最好的深度学习框架的实现， 都包含了多种算法来优化梯度下降(参看Lasagne, Caffe, Keras的文档). 这些算法用于深度学习优化, 但是其实际使用的优缺点却很少被提及.

本文就是期望帮助你理解各种不同的梯度下降优化算法的行为, 以便更好的在深度学习实践中应用这些算法. 首先我们先回顾一下不同种类的梯度下降的方法， 然后总结一下在日常训练中遇到的困难， 接下来, 我们通过分析那些常用的梯度下降算法诞生的原因以及如何推导它们的更新规则(update rule)来介绍这些算法，同时我们也会简单展示下如何在并行/分布式系统中应用这些算法, 最后， 我们讨论下其他有益于优化梯度下降的策略.

梯度下降是通过目标函数($J(\theta)$)的梯度($\\nabla_{\theta} J(\theta)$)的相反方向更新模型参数($\theta \in R^d$)来最小化目标函数($J(\theta)$)的方法. 学习因子($\eta$)决定了我们到达最小值或者局部最小值的步长, 换句话说, 我们沿着目标函数所构建的曲面的斜坡下滑直至到达谷底. 如果你不熟悉梯度下降， 可以在[这里](https://cs231n.github.io/optimization-1/)找到相关介绍.

## 梯度下降分类
梯度下降大致可以分为三类， 他们的区别在于使用多少数据来计算目标函数的梯度. 根据训练集中样本的数量， 我们需要在参数迭代更新的精度和训练时长这两者间权衡取舍.

### 批量梯度下降(Batch Gradient Descent)
批量梯度下降会使用训练集中的所有样本来计算参数代价函数相对于模型参数($\theta$)的梯度.
$$
\theta = \theta - \eta \times \nabla_{\theta} J(\theta)
$$
因为批量梯度下降训练需要一次性计算所有样本，所以训练速度会非常慢，如果样本数量多的话， 一次行加载所有样本并计算需要非常大的内存， 通常不太具备实际上的可操作性， 而且即使有新的训练样本出现，批量梯度训练也无法实现在线训练.

实现的代码大致如下：
```
for i in range(nb_epochs):
  params_grad = evaluate_gradient(loss_function, data, params)
  params = params - learning_rate * params_grad
```

### 随机梯度下降(Stochastic Gradient Descent)

### 小批量梯度下降(Mini-batch Gradient Descent)

# Original Post
* https://ruder.io/optimizing-gradient-descent/ by SEBASTIAN RUDER
