# 梯度下降优化算法概览
```
本文翻译自SEBASTIAN RUDER的An overview of gradient descent optimization algorithms
```
梯度下降是最流行的优化算法, 尤其是在神经网络优化中得到了广泛应用. 当前流行的深度学习框架都包含了多种算法来优化梯度下降(参看Lasagne, Caffe, Keras的文档). 这些算法用于深度学习优化, 但是其实际使用的优缺点却很少被提及.

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
下文我们会概述深度学习中常用的梯度下降优化算法.  不过我们不会讨论不适合在高维数据集中运算的算法， 比如跟牛顿法类似的二阶法.
### Momentum
随机梯度下降很难越过峡谷， 峡谷是指在某一维度上的表面弯曲程度远超过其他维度的区域， 在局部最优点周围常能见到这种情形.   遇到这种情形的时候， 随机梯度下降会在峡谷震荡， 艰难的到达局部最优的谷底. 如图二所示.

![Image](https://ruder.io/content/images/2015/12/without_momentum.gif)
图二

Momentum 就是针对这种场景的应对方法， 它可以加速随机梯度下降在有价值的方向上的快速下降， 并且抑制无效的震荡， 如图三所示.

![Image](https://ruder.io/content/images/2015/12/with_momentum.gif)
图三

Momentum做到这一点仅仅引入了一个部分$\gamma$的上一次更新矢量到当前的更新矢量， 用公式来描述:
$$
v_t = \gamma \times v_{t-1} + \eta \times \nabla_{\theta}J(\theta)
$$
$$
\theta = \theta - v_t
$$
注意： 某些实现可能会交换等式的正负号.  $\gamma$ 通常取值为$0.9$或相近的值.
想象一下， 当你把一个球从山顶上往下扔， 这个球在滚下来的过程中会累积动量， 变的越来越快， 直到到达最终速度为止， 这边的最终速度可以理解为空气存在阻力， 数学意义上表示为$\gamma \lt 1$. 同样的事情也发生在我们的模型参数更新过程, 如果参数更新的方向一致， Monmentum会增大更新的幅度， 反正则会减小更新幅度， 作为结果， 我们可以更快的收敛和有效减少震荡. 
### Nesterov 加速梯度下降
但是， 当一个球滚下山的时候， 如果只是盲目沿着斜率方向滚动， 是不能让人满意的.  我们希望这个球可以更智能， 能知道它所要去的地方， 可以在斜率重新上升前就知道要减速.

Nesterov 加速梯度下降(NAG)就是可以给予momentum预知的能力, 我们知道$\gamma v_{t-1}$会用来更新模型参数$\theta$, 计算$\theta - \gamma \times v_{t-1}$可以得到下一时刻模型参数的近似值(这个梯度在momentum方法计算梯度时是被忽略了). 这也是对未来我们的模型参数将要被如何更新的估计. 于是我们可以使用未来估计的模型参数值， 而不是当前的模型参数值来更有效的计算梯度. 用公式来描述:
$$
v_t = \gamma \times v_{t-1} + \eta \times \nabla_{\theta}J(\theta - \gamma \times v_{t-1})
$$
$$
\theta = \theta - v_t
$$
跟momentum方法相似, $\gamma$的值被预设为$0.9$左右, momentum方法先计算当前梯度（图四中的小的蓝色矢量)然后再向累计的梯度（图四中的大的蓝色矢量)方向前进一大步. 而Nesterov加速梯度下降则先向累计梯度(棕色矢量)方向前进一大步， 然后再根据当前梯度做矫正(红色矢量). 结果形成一次NAG更新(绿色矢量). 这个具有预见性的更新防止我们更新过快, 从而使算法的灵敏度提升. 尤其是在RNN的训练中可以显著提升效率.

![Image](https://ruder.io/content/images/2016/09/nesterov_update_vector.png)
图四

[这里](https://cs231n.github.io/neural-networks-3/)有对NAG的另一种解释. Ilya Sutskever 在他的博士论文中给出了更加详细的说明.
现在我们已经有能力根据误差函数的斜率来更新我们的模型参数并且加速SGD的训练过程了. 不过我们希望更进一步， 希望梯度下降算法可以根据模型参数重要程度的不同做出有针对性的更新.

### Adagrad
Adagrad 可以基于模型参数特征来自适应调整学习因子, 对于出现频率高的特征采用较大的学习因子, 对于出现频率低的特征采用较大的学习因子. 因此， 它非常使用处理稀疏样本集. Dean等人在google工作期间发现adagrad可以有效的提升SGD的鲁棒性, 并将adagrad应用于大规模神经网络的训练, 比如从Youtube视频中识别猫. 此外, Pennington等人采用adagrad来训练GloVe词嵌入(GloVe word embedding)， 低频的词要比高频的词需要更大的学习因子.

我们之前的训练都是使用相同的学习因子$\eta$来更新模型参数. Adagrad则会针对不同的参数$\theta_{i}$， 选择不同的学习因子.  为了描述简单， 我们使用$g_t$来表示在阶段$t$时的梯度， 用$g_{t,i}$来表示目标函数在阶段$t$时对参数$\theta_i$的偏导数.
$$
g_{t,i} = \nabla_{\theta}J(\theta_{t,i})
$$
则, SGD针对参数$\theta_i$在阶段$t$时刻的更新为:
$$
\theta_{t+1,i} = \theta_{t,i} - \eta \times g_{t,i}
$$
Adagrad会根据不同的参数采用不同的学习因子, 即修改SGD过程中的学习因子, 用公式来描述:
$$
\theta_{t+1,i} = \theta_{t,i} - \frac{\eta}{\sqrt{G_{t,ii}+\epsilon}} . g_{t,i}
$$
其中， $G_t \in R^{d \times d}$ 是一个对角矩阵, 其对角线上的每一个元素$i$是到阶段$t$为止, 所有梯度$\theta_i$的平方和.  $\epsilon$是为了避免除零的平滑项，通常取值$1e-8$. 有趣的是， 如果没有开方操作， adagrad的性能会变的很差.

我们也可以把上式写成矩阵-矢量乘:
$$
\theta_{t+1,i} = \theta_{t} - \frac{\eta}{\sqrt{G_{t}+\epsilon}} \odot g_{t}
$$
Adagrad主要的优点在于无需手动调整学习因子$\eta$, 多数情况下学习因子初始被设置为$0.01$就可以了.

Adagrad的缺点是: 它的分母跟历史梯度的平方和相关， 这个值会在训练过程中持续增加， 从而学习因子持续变小最终变成无限小， 训练过程也难以为继. 下面的算法就旨在解决这个问题.

### Adadelta
Adadelta是adagrad算法的扩展，  它寻求解决学习因子单调递减的问题.  跟adagrad算法需要求历史所有梯度的平方和不同， adadelta将球平方和的窗口限制为某个固定值$w$. 为了避免在训练过程中需要持续保存$w$个历史梯度值,  adadelta寻求一种更为高效的做法， 令$E_t$为阶段$t$的梯度平方的均值， 它仅被$\gamma$和前一阶段的均值$E_{t-1}$所决定($\gamma$类似momentum).

$$
E_t = \gamma E_{t-1} + (1 - \gamma)g^2_t
$$

$\gamma$的值大致可以设置为$0.9$左右.  为简化起见， 我们可以把SGD的参数更新矢量记为$\Delta \theta_t$：
$$
\Delta \theta_t = - \eta \cdot g_t
$$
$$
\theta_{t+1} = \theta_t + \Delta \theta_t
$$
在Adggrad, 则此公式更新为:
$$
\Delta \theta_t = - \frac{\eta}{\sqrt{G_t + \epsilon}} \odot g_t
$$
用$E_t$来替换对角矩阵$G_t$
$$
\Delta \theta_t = - \frac{\eta}{\sqrt{E_t + \epsilon}}g_t
$$
可见分母可以被视为梯度的均方根， 于是上式可以写为:
$$
\Delta \theta_t = - \frac{\eta}{RMS[g]_t}g_t
$$

作者指出， 上式中各个部分的计算单位不一致，  参数更新公式必须跟参数有相同的计算单位. 为了解决这个问题，作者定义了：
$$
E(\Delta \theta^2) = \gamma E(\Delta \theta^2)_{t-1} + (1 - \gamma) \Delta \theta^2_t
$$
于是:
$$
RMS[\Delta \theta]_t = \sqrt{E[\Delta \theta^2]_t + \epsilon}
$$

由于 $RMS[\Delta \theta]_{t}$

是未知量, 所以用前一次的 $RMS$ 来模拟. 这样就可以用

$RMS[\Delta \theta]_{t-1}$

来替换$\eta$, 最终， adadelta更新公式可以写为:
$$
\Delta \theta_t = - \frac{RMS[\Delta \theta]_{t-1}}{RMS[g]_t} \cdot g_t
$$

$$
\theta_{t+1} = \theta_t + \Delta \theta_t
$$
使用adadelta，我们无需指定学习因子， 因为她已经在更新公式中被消去了.

### RMSprop
RMSprop是未公开发表的自适应调整学习因子的算法, 是由Geoff Hinton 提出. [Lecture slides lec6](http://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf)

RMSProp和Adadelta是在相同的时间被独立研究出来的， 其目的都是为了解决Adagrad的学习因子递减至无限小的问题. RMSProp实际上等价于Adadelta最早被提出时的样子.
$$
E_t = 0.9E_{t-1} + 0.1g^2_t
$$
$$
\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{E_t + \epsilon}}
$$
RMSProp将学习因子除以梯度的均方根(指数衰减), Hinton建议$\eta$的值为$0.9$, $\epsilon$的值为$0.001$

### Adam
Adaptive Moment Estimation(Adam) 是另一种可以根据参数特征自适应调整学习因子的算法.   除了像Adadelta和RMSprop那样需要保存一个指数衰减的历史平方梯度$v_t$, Adam还需要保存另一个指数衰减的历史梯度$m_t$， 有点像momentum.  Momentum可以在小球滚下斜坡时被观察到， Adam的行为就像一个重球, 带有不可忽视的摩檫力， 它倾向于在收敛到平坦的错误表面(error surface).  用数学公式来表示:
$$
m_t = \beta_1 m_{t-1} + (1 - \beta_1)g_t
$$
$$
v_t = \beta_2 v_{t-1} + (1 - \beta_2)g^2_t
$$

$m_t$ 和 $v_t$分别是梯度的一阶矩和二阶矩. 正如算法的名字， 当 $m_t$ 和 $v_t$初始为0， Adam的作者观察到它们都会偏向于零. 尤其在初始时和衰减率比较小的时候($\beta_1$和$\beta_2$都接近于1)
可以通过偏向矫正(bias-corrected)一阶矩和二阶矩的方法来抵消这个问题:
$$
\hat{m_t} = \frac{m_t}{1-\beta^t_1}
$$

$$
\hat{v_t} = \frac{v_t}{1-\beta^t_2}
$$
于是, Adam算法的公式表示为：
$$
\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v+t}} + \epsilon}\hat{m_t}
$$
作者建议$\beta_1$和$\beta_2$的取值为0.9和0.999, $\epsilon$的取值为$10^{-8}$.  在实际的训练中, Adam表现出了良好的性能.

### AdaMax
Adam中的$v_t$的更新规则有点像基于$g_t$的$l_2$范数:
$$
v_t = \beta_2 v_{t-1} + (1 - \beta_2)|g_t|^2
$$
我们可以推广此式为$l_p$范数, Adam的作者也把$\beta_2$参数化(parameterize)为$\beta_2^p$
$$
v_t = \beta_2^p v_{t-1} + (1 - \beta_2^p)|g_t|^p
$$
通常高$p$范数($p \gt 2$)不是平稳的， 所以实践上常用$l1$和$l2$范数. 但是$l \infty$范数却通常是平稳的, 所以作者提出了AdamMax算法, 为了避免混乱， 用$u_t$来描述$l \infty$的$v_t$:
$$
u_t = \beta_2^{\infty} v_{t-1} + (1 - \beta_2^{\infty})|g_t|^{\infty} = max(\beta_2 \cdot v_{t-1}, |g_t|)
$$
于是， AdaMax的更新规则为:
$$
\theta_{t+1} = \theta_{t} - \frac{\eta}{u_t}\hat{m_t}
$$
因为$u_t$是个取最大值的操作结果， 所以AdaMax解决了偏向零的问题. 实践中, 建议的取值为: $\eta = 0.002, \beta_1 = 0.9, \beta_2 = 0.999$ 

### Nadam
TODO

### AMSGrad
TODO

### Visualization of algorithms
TODO

## Additional strategies for optimizing SGD
TODO


# 原文(Original Post)
* https://ruder.io/optimizing-gradient-descent/ by SEBASTIAN RUDER
