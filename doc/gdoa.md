# 梯度下降优化算法概览
```
本文翻译自SEBASTIAN RUDER的An overview of gradient descent optimization algorithms
```
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
因为批量梯度下降训练需要一次性计算所有样本，所以训练速度会非常慢，如果样本数量多的话， 一次性加载所有样本并计算需要非常大的内存， 通常不太具备实际上的可操作性， 而且即使有新的训练样本出现，批量梯度训练也无法实现在线训练.

实现的代码大致如下：
```
for i in range(nb_epochs):
  params_grad = evaluate_gradient(loss_function, data, params)
  params = params - learning_rate * params_grad
```
给定训练次数， 每次训练我们都通过对损失函数求导， 来计算模型参数的梯度矢量.  需要强调的是， 当前的深度学习框架都已经提供了高效的求导方法， 但是如果你是自己实现损失函数求导的话， 则需要对计算所得的梯度进行校验， [这里](https://cs231n.github.io/neural-networks-3/) 提供了一些关于梯度校验的有效的实践方法。 接下来， 梯度和学习因子决定了模型参数将被如何更新. 如果损失函数是凸函数的话， 批量梯度下降会收敛于最优解， 如果不是， 则会收敛于局部最优解.

### 随机梯度下降(Stochastic Gradient Descent)
随机梯度下降跟批量梯度下降不同的是， 它会根据每个样本($x^i, y^i$)计算梯度并且更新模型参数:
$$
\theta = \theta - \eta \times \nabla_{\theta}J(\theta;x^i;y^i)
$$
在训练集样本比较多的情形下， 通常会存在比较多的相似样本， 批量梯度下降需要计算所有样本才能去更新参数， 这样势必存在冗余计算， 而随机梯度下降则相反， 每个样本的计算都会导致参数更新， 这样就大大消除了计算冗余. 因此随机梯度下降的训练速度通常都比批量梯度下降快的多， 也可以被用于在线训练.

随机梯度下降每次更新参数的幅度变化比较大， 这会导致目标函数出现剧烈震荡, 如图一所示:
![image](https://ruder.io/content/images/2016/09/sgd_fluctuation.png)
图一

与批量梯度下降会是参数收敛于局部最优解相比， 随机梯度下降更容易是参数调整时跳出局部最优， 可能会选择更好的局部最优， 但是这也将使收敛过程变得极度复杂， 因为随机梯度下降可能会持续调整过量.  虽然如此， 我们已经可以证明当我们缓慢调低学习因子， 随机梯度下降将表现出于批量梯度下降相似的收敛特性， 即：如果损失函数是凸函数的话， 批量梯度下降会收敛于最优解， 如果不是， 则会收敛于局部最优解.

实现的代码大致如下, 需要注意的是 我们每次新阶段训练开始的时候， 都会随机打乱样本的顺序.
```
for i in range(nb_epochs):
  np.random.shuffle(data)
  for example in data:
    params_grad = evaluate_gradient(loss_function, example, params)
    params = params - learning_rate * params_grad
```

### 小批量梯度下降(Mini-batch Gradient Descent)
小批量梯度下降结合了批量梯度下降和随机梯度下降的优点， 这种方法会计算每一个小批量的样本的梯度并且更新模型参数：
$$
\theta = \theta - \eta \times \nabla_{\theta}J(\theta;x^{i:i+n};y^{i:i+n})
$$
这种方法， a)减小的每次模型参数更新的幅度， 这样更容易是收敛趋于稳定， b)有效利用当代深度学习框架所提供的高度优化的矩阵运算来提升梯度计算效率, 小批量梯度每次迭代的样本数大多在50～256左右，可以根据不同的场景选择不同的样本数. 小批量梯度下降是训练神经网络最常用的算法， 通常也被直接称为随机梯度下降. 为了描述方便， 下文中我们会省略参数$x^{i:i+n}$和$y^{i:i+n}$.
实现的代码大致如下：
```
for i in range(nb_epochs):
    np.random.shuffle(data)
    for batch in get_batches(data, batch_size=50):
        params_grad = evaluate_gradient(loss_function, batch, params)
        params = params - learning_rate * params_grad
```

### 梯度下降面临的挑战
然而小批量梯度训练依然无法保证良好的收敛性， 我们依然面临着下面的挑战：
* 选择一个合适的学习因子是非常困难的， 过小会导致收敛速度过慢， 过大会阻碍收敛， 导致模型参数在最优解周围震荡， 甚至偏离最优解.
* 为了解决学习因子的选择问题， 我们引入了学习因子调度的方法，类似退火算法(annealing), 大致的思路是按照预先设定好的步骤或者根据两个相邻阶段训练目标函数变化低于某个给定阈值的时候减小学习因子， 不过这种做法需要预先设定好调度的规则， 无法根据训练样本的特征做适应性调整.
* 另外， 学习因子会作用于所有的模型参数， 如果我们的训练样本是稀疏的， 样本的不同特征的出现率差异较大， 我们也许不希望所有的模型参数以同样的步长来更新， 而是希望出现概率低的特征以大步长来更新参数， 显然普通的训练方法无法满足这一要求.
* 神经网络的误差函数常常是高度非凸， 所以还有一个关键的点是如何避免陷入局部最优. Dauphin等人还指出， 这个困难经常出现在鞍点(saddle points)， 而非局部最优点. 所谓鞍点， 就是在一个纬度上是递减的， 而另一纬度是递增的， 这种鞍点周围的点通常都是误差平稳的， 也就是梯度接近于零.  随机梯度下降难以从这些点跳出.

## 梯度下降优化算法

### Momentum

### Nesterov accelerated gradient

### Adagrad

### Adadelta

### RMSprop

### Adam

### AdaMax

### Nadam

### AMSGrad

## Additional strategies for optimizing SGD


# 原文(Original Post)
* https://ruder.io/optimizing-gradient-descent/ by SEBASTIAN RUDER
