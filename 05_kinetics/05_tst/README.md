# 05 · 势垒如何变成时间尺度

本项目用过渡态理论把自由能势垒转换为单步速率和等待时间，量化能垒误差对动力学预测的影响。

## 背景：为什么需要这一步

反应热力学有利并不意味着反应很快。体系可能长时间留在反应物盆地中，只有少量热涨落能到达连接产物的分割面。过渡态理论（TST）用反应物与分割面附近的相对统计权重，乘以通过该面的频率尺度，估计净向外的反应事件。

常用形式中的 kBT/h 是频率前因子，指数中的 ΔG‡ 是相对于反应物的自由能势垒。该描述假设反应物盆地能够近似平衡，并把反复穿越分割面等动力学效应留给传输系数 κ。这里取 κ=1，目的是先理解指数敏感性。

单步一阶速率常数的倒数给出平均等待时间。催化网络还受覆盖度、逆反应和其他步骤影响，所以不能把某个单步 k 直接称为整个表面的周转频率。

## 开始前需要理解的概念

- **过渡态与分割面**：把反应物区和产物区分开的局部区域；反应坐标方向不按稳定振动处理。
- **活化自由能 ΔG‡**：过渡态相对反应物的自由能差，包含所采用模型中的熵效应。
- **前因子**：具有速率单位的尺度，TST 与固定 Arrhenius 前因子有不同温度依赖。
- **传输系数 κ**：修正理想化穿越计数，本例固定为 1。
- **等待时间 τ**：对恒定一阶事件率为 1/k，不自动等于扩散或网络完成时间。

## 本次任务：从什么得到什么

从 temperatures.csv 与控制文件读取温度、势垒范围和 Arrhenius 前因子，自己实现 k 与 τ 的扫描，同时输出两种公式的对比。先在对数尺度验证斜率，再把时间换成秒、毫秒或微秒解释。

## 先用一个小例子走通思路

600 K 时 $k_BT\approx0.05170$ eV。势垒增加 0.1 eV，速率比为 $\exp(-0.1/0.05170)\approx0.145$，也就是约慢 6.9 倍。

因此“只差 0.1 eV”是否可接受，要由目标速率精度决定。若希望 600 K 下速率误差小于两倍，仅势垒误差预算就约为 $k_BT\ln2\approx0.0358$ eV，尚未包含前因子和模型误差。

## 实现边界

**手写** TST 与 Arrhenius 公式、单位、对数敏感性；不需要再引入反应求解软件。后续多步耦合交给手写质量作用方程与 Cantera，单步 TST 不能替代整个网络。

## 输入与物理模型

- [control.toml](input/control.toml)
- [temperatures.csv](input/temperatures.csv)

`temperatures.csv` 给出温度，控制文件给出势垒扫描和 Arrhenius 前因子。TST 使用自由能势垒：

```math
k_{TST}=\kappa\frac{k_BT}{h}\exp[-\Delta G^\ddagger/(k_BT)],\quad \tau=1/k.
```

$\kappa$ 是传输系数，此例为 1。作为对照，Arrhenius 为 $k=Ae^{-E_a/(k_BT)}$；如果取相同数值势垒，两者的差别来自前因子，但物理上的 $E_a$ 与 $\Delta G^\ddagger$ 并不天然相等。

```math
\delta\ln k=-\delta\Delta G^\ddagger/(k_BT).
```

这里时间尺度是单一一阶过程的平均等待时间。表面 TOF 还需要覆盖度和多步耦合，不能直接等同 k。

## 从公式到程序

1. 对每个温度与势垒计算 k 和 τ，保存 barrier-timescale.csv。
2. 同时计算固定前因子的 Arrhenius，明确两种势垒标签。
3. 用 ln k 对势垒的直线斜率验证实现，检查单位为 s⁻¹。
4. 将秒、毫秒与微秒标注在同一图上，用可观测窗口判断势垒范围。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 05_kinetics/05_tst/run.py --output runs/05_tst
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 600 K 下给势垒加 0.1 eV，速率应乘约 0.145；把这个比值与直接计算核对。
- 把 κ 从 1 改成 0.1，预测曲线平移，思考它与势垒偏移在哪一个温度下可混淆。
- 温度依赖的熵势垒会改变表观活化能；不要把 Arrhenius 图斜率机械称为电子 NEB 势垒。

## 分步提示与资料

常数与量纲约定见 [单位项目](../../02_bringup/01_units/README.md)。

## 完成后应能解释什么

读 barrier-timescale.csv 时同时看势垒单位、温度和速率标签，检查 ln k 的斜率与时间倒数。完成后应能把一个能量误差翻译成速率倍率，并列出从电子 NEB 势垒到自由能 TST 势垒需要的补充。

## 与前后项目的关系

连接 [NEB](../04_neb/README.md) 与 [热力学](../../04_thermodynamics/README.md)；[动力学检查点](../06_checkpoint/README.md) 审核这些连接，后续 [微观动力学](../../06_catalysis/06_microkinetics/README.md) 将单步速率耦合起来。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
