# 案例与问题

相同的 ASE 接口可以挂接 Morse、EMT 或 GPAW。接口相同究竟保证了什么，又没有保证什么？


统一接口提供 $E(\mathbf R)$ 和 $\mathbf F=-\nabla E$。数值优化、Verlet 和 NEB 可以复用，但换 calculator 会换势能面。

$$\delta E_{obs}=\delta E_{implementation}+\delta E_{numerical}+\delta E_{model}$$

这里只是误差来源的记账框架，不假定三项统计独立，也不意味着可直接加绝对值当置信区间。


1. 根据 input/contracts.csv，指定每个练习的手写部分、库部分与对照对象。
2. 列出能在 Morse/EMT 上发现的三种实现错误，以及必须在 GPAW 上检查的两种数值误差。
3. 写一个从模型势迁移到 DFT 的验收顺序，每一步说明检查的可观测量。
4. 解释为什么 EMT 与 PBE 吸附能接近不能自动校准整个势能面。
