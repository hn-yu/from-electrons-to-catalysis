# 05 · 从势能面到结构、路径和时间尺度

这一章研究状态之间怎样变化。给定可靠的能量和力，我们分别做结构优化、经典动力学、振动分析、路径搜索和单步速率估计，理解每种算法回答的不同问题。

## 同一个势能面上的五种任务

优化沿能量下降寻找驻点；动力学用质量和动量推进 Newton 方程；Hessian 分析驻点附近的曲率；NEB 寻找两个状态之间的低能通道；TST 用自由能势垒估计跨越事件率。

```math
\mathbf F=-\nabla E,\qquad
M\ddot{\mathbf R}=\mathbf F,\qquad
H_{ij}=\frac{\partial^2E}{\partial R_i\partial R_j}.
```

这三个式子分别涉及一阶导数、运动方程和二阶导数。它们共享底层势能，却需要不同输入和检查。优化步数没有真实时间意义，MD 轨迹也不保证自动找到最有代表性的反应路径。

## 进入本章前

先掌握 [能量与力](../02_bringup/02_forces/README.md) 和 [有限差分](../02_bringup/03_finite_differences/README.md)，能理解梯度、矩阵本征值与基本微分方程。到 TST 前，再读 [自由能背景](../04_thermodynamics/README.md)，以区分 ΔE‡ 和 ΔG‡。

| 项目 | 要解决的具体问题 | 主要核对 |
|---|---|---|
| [优化](01_optimizer/README.md) | 从初始点进入哪个局部盆地？ | 自写回溯与 SciPy BFGS 的终点/残余力 |
| [Velocity Verlet](02_dynamics/README.md) | 给定初态后轨迹怎样随时间演化？ | 守恒量、稳定步长与 ASE 完整轨迹 |
| [Hessian 与正常振动](03_hessian/README.md) | 驻点稳定吗，各协同运动有多快？ | 质量加权、模式计数与 ASE 频率 |
| [NEB](04_neb/README.md) | 两个状态之间经过什么能量山口？ | 路径残余力、image 间距与 ASE NEB |
| [TST](05_tst/README.md) | 给定自由能势垒对应多长等待？ | 单位、对数斜率和速率倍率 |
| [检查点](06_checkpoint/README.md) | 每一步究竟支持到哪项判断？ | 依据真实模式表和反例审查推断 |

## 两个可以先手算的判断

二维势 E=x²−y² 在原点受力为零，但一方向升高、另一方向降低，因此是鞍点。这说明优化报告中的小力不能替代 Hessian 分类。

600 K 时，0.1 eV 的势垒变化使 TST 速率乘约 0.145：

```math
\frac{k_{new}}{k_{old}}=\exp\left[-\frac{0.1\ \mathrm{eV}}{k_BT}\right].
```

这说明一个“看起来很小”的路径能量误差也可能显著影响时间预测。真实速率还需要自由能修正和传输系数，不能将模型 NEB 的电子势垒直接包装为实验速率。

## 分工和交付

自己实现回溯、Verlet、Hessian 后处理与 NEB 投影；对角化、生产级优化/轨迹管理和电子结构导数使用成熟库。水分子解析 Hessian 来自 PySCF，后处理由自己与 ASE 独立比较；原子 EMT 路径仅用于工作流练习。

交付应有优化/动力学轨迹、完整模式谱或路径图，以及它们支持的结构和时间判断。下一章 [催化](../06_catalysis/README.md) 加入表面状态、自由能采样和网络人口。[课程首页](../README.md) · [实现边界](../docs/IMPLEMENTATION_BOUNDARIES.md)
