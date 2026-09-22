# 02 · 从分子坐标到气相 Gibbs 自由能

电子能量本身不能回答室温气体反应是否有利。平移、转动、振动和标准压力分别在自由能中贡献什么？

## 实现边界

**直接用 PySCF** 优化所需梯度与解析 Hessian，ASE 处理结构和惯性矩；**手写 RRHO** 各配分函数与 H/S/G；再用 **ASE IdealGasThermo 独立比对**。不手写分子积分和电子结构 Hessian。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [CO.xyz](input/CO.xyz)
- [CO2.xyz](input/CO2.xyz)
- [H2.xyz](input/H2.xyz)
- [H2O.xyz](input/H2O.xyz)
- [control.toml](input/control.toml)
- [molecules.csv](input/molecules.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


H₂、CO、CO₂、H₂O 坐标来自 XYZ；`molecules.csv` 明确线性分类、旋转对称数和电子自旋。计算先用 RHF/STO-3G 优化几何，再取内部振动频率；这组数据是方法练习而非高精度实验热化学。

$$q_{\rm trans}=\left(\frac{2\pi mk_BT}{h^2}\right)^{3/2}\frac{k_BT}{p},$$
$$q_{\rm rot}^{\rm linear}=\frac{8\pi^2Ik_BT}{\sigma h^2},\quad q_{\rm rot}^{\rm nonlinear}=\frac{\sqrt\pi}{\sigma}\prod_{a=1}^3\left(\frac{8\pi^2I_ak_BT}{h^2}\right)^{1/2}.$$

$\sigma$ 防止将不可区分的转动构型重复计数。H₂ 为 2、CO 为 1、CO₂ 为 2、水为 2。

$$H=E_{\rm elec}+U_{\rm vib}+(5/2+d_{\rm rot})k_BT,\quad G=H-TS,$$

线性分子 $d_{\rm rot}=1$，非线性为 $3/2$；$5/2$ 包括平移内能 $3/2$ 与理想气体的 pV 项 1。振动项含 ZPE。


## 从公式到程序

1. 从 XYZ 读几何，检查能量和梯度的单位：PySCF 梯度为 Hartree/bohr，优化坐标为 Å。
2. 优化后分析 Hessian，去掉刚体自由度；线性分子有 3N−5 个内部振动，非线性有 3N−6 个。
3. 计算质量、惯性矩、各配分函数，输出 electronic/ZPE/thermal H/S/G 分项。
4. 将相同几何、频率、温度、压力和对称数传给 ASE；输出 G_error，并保存优化后的 XYZ。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 04_thermodynamics/02_molecular_thermochemistry/run.py --output runs/02_molecular_thermochemistry
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 把水的对称数从 2 改为 1，预测 ΔG=−kBT ln2；不要将它当能量计算误差。
- 将压力提高 10 倍，G 增加 kBT ln10，H 在此理想模型下不变。
- 故意把很小的刚体频率当振动加入，观察熵异常增大；“频率都是实数”仍不足以证明模式分类正确。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[ASE thermochemistry](https://ase-lib.org/ase/thermochemistry/thermochemistry.html)；[PySCF Hessian](https://pyscf.org/user/grad.html)。
