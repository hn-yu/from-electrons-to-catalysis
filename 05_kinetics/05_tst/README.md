# 05 · 势垒如何变成时间尺度

势垒从 0.8 eV 改到 0.9 eV，到底是“小变化”还是几个数量级？本项目把能量不确定性翻译成实验可见时间。

## 实现边界

**手写** TST 与 Arrhenius 公式、单位、对数敏感性；不需要再引入反应求解软件。后续多步耦合交给手写质量作用方程与 Cantera，单步 TST 不能替代整个网络。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [control.toml](input/control.toml)
- [temperatures.csv](input/temperatures.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


`temperatures.csv` 给出温度，控制文件给出势垒扫描和 Arrhenius 前因子。TST 使用自由能势垒：

$$k_{TST}=\kappa\frac{k_BT}{h}\exp[-\Delta G^\ddagger/(k_BT)],\quad \tau=1/k.$$

$\kappa$ 是传输系数，此例为 1。作为对照，Arrhenius 为 $k=Ae^{-E_a/(k_BT)}$；如果取相同数值势垒，两者的差别来自前因子，但物理上的 $E_a$ 与 $\Delta G^\ddagger$ 并不天然相等。

$$\delta\ln k=-\delta\Delta G^\ddagger/(k_BT).$$

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

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

常数与量纲约定见 [单位项目](../../02_bringup/01_units/README.md)。
