# 06 · 从表面状态到持续催化通量

这一章把前面的电子结构、热力学与动力学连接到表面催化：先定义可信状态，再求相应统计和速率，最后研究覆盖度如何决定整体响应。

## 为什么一个吸附能或一个势垒不够

催化剂提供反应通道，改变达到平衡的速度，而不改变给定反应和条件下的平衡常数。持续非零产物通量需要反应物与产物储库提供驱动力；表面各状态的占据由所有吸附、转化和脱附过程共同决定。

因此需要三组互相连接的证据。结构和收敛计算定义候选状态；自由能描述温度下的相对统计权重；反应网络把速率与覆盖度耦合。这里的几组教学模型分别隔离这些问题，不将抽象网络的 TOF 说成 H/Cu 的实际活性。

## 本章的三条支线

| 项目 | 先解决的缺口 | 关键输入与方法 |
|---|---|---|
| [slab 收敛](01_slab/README.md) | 有限薄板能否代表目标表面？ | POSCAR/EXTXYZ 与真实 PBE 能量；直接用 ASE/GPAW |
| [吸附位点](02_adsorption/README.md) | 状态身份和位点排序是否可靠？ | 四个位点结构、最终坐标与共同参考 |
| [伞形采样](03_umbrella/README.md) | 稀有区域如何得到充分数据？ | 窗口表 → Metropolis 轨迹 → 自写 WHAM/PyMBAR |
| [MEP 与 FES](04_mep_fes/README.md) | 最低能路径为何缺少横向熵？ | 同一二维势的解析与 SciPy 积分 |
| [反应网络](05_reaction_network/README.md) | 正逆速率怎样与热力学一致？ | 状态/过渡态 CSV 与 Cantera 原生 YAML |
| [微观动力学](06_microkinetics/README.md) | 人口如何把单步速率变成 TOF？ | 质量作用、稳态方程、BDF 与 Cantera |
| [速率控制](07_rate_control/README.md) | 改哪个过渡态最影响整体速率？ | 保持中间体不变的受控扰动与独立对照 |
| [检查点](08_checkpoint/README.md) | 不同层次结果能否组成一致解释？ | 实际通量报告和缺失证据审查 |

结构支线需要 [周期 DFT](../03_electronic_structure/06_periodic/README.md)，采样支线需要 [配分函数](../04_thermodynamics/01_partition/README.md)，网络支线需要 [化学势](../04_thermodynamics/03_chemical_potential/README.md) 与 [TST](../05_kinetics/05_tst/README.md)。可以按这三条支线补先修知识，再在检查点汇合。

## 一个最小催化循环

```math
A(g)+*\rightleftharpoons A*\rightleftharpoons B*\rightleftharpoons B(g)+*.
```

星号是表面空位，A* 与 B* 是占据态。吸附需要气体和空位，转化需要 A*，脱附需要 B*；因此任一步的速率常数都不能单独决定总通量。

```math
\dot{\boldsymbol\theta}=S\mathbf r,\qquad
\theta_*+\theta_A+\theta_B=1.
```

本串联循环稳态时各步净通量相等，但可以都不为零。示例在 600 K 的表面大多被 A* 占据，说明覆盖度会强烈影响哪些事件真正发生。改变条件后必须重新求人口，不能只替换一个 Arrhenius 指数。

## 怎样读本章的计算结果

真实 PBE 表面例子当前厚度差约 0.35 eV，尚未达到 0.05 eV 容限；约 7 meV 的 fcc/hcp 位点差也需要进一步收敛检验。伞形模型即使两个重加权软件一致，隐藏坐标仍可能未平衡。网络算例则是抽象 A/B 异构化，其参数用于方法理解。

交付应能明确每组数据的模型、状态和标准态，并解释一项覆盖度或速率变化。最后进入 [真实体系研究练习](../07_real_system/README.md)，把这些检查转化为计算决策。[课程首页](../README.md) · [上一章：动力学](../05_kinetics/README.md)
