# 06 · 周期边界、体积与状态方程

拟合出一个晶格常数并不难；困难的是确认曲线反映的是材料的压缩响应，而不是 k 点和基组误差。

## 实现边界

**直接用 ASE/GPAW** 读取 CIF、求平面波 PAW/PBE 能量并用 ASE EquationOfState 拟合。**手写**原胞归一化、体积扫描和收敛设计；不重写平面波 DFT。默认先分析既有真实 PBE 表，`--calculate` 才启动新计算。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [Al.cif](input/Al.cif)
- [control.toml](input/control.toml)
- [eos.csv](input/eos.csv)
- [lattice_scan.csv](input/lattice_scan.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


`Al.cif` 给出真实原胞及坐标。`lattice_scan.csv` 指定 a，`eos.csv` 给出已执行 GPAW 的每原子 $V,E$；`control.toml` 指定新计算的截断能、k 点与展宽。

面心立方的每原子体积是 $V=a^3/4$。压力和体模量来自能量曲率：

$$P=-\frac{dE}{dV},\qquad B=V\frac{d^2E}{dV^2}\bigg|_{V_0}.$$

三阶 Birch–Murnaghan 表达式令 $\eta=(V_0/V)^{2/3}$：

$$E(V)=E_0+\frac{9V_0B_0}{16}\{B'_0(\eta-1)^3+(\eta-1)^2(6-4\eta)\}.$$

这里 $B'_0=(dB/dP)_0$ 无量纲。eV/Å³ 到 GPa 需要单位转换，不能把拟合输出直接当 GPa。


## 从公式到程序

1. 对 eos.csv 按 scenario 分组，分别拟合相同物理形式，保存 a₀ 和 B。
2. 检查拟合最低点位于体积采样区间内部，曲率为正。
3. 新计算使用 `run.py --calculate`：读取 CIF，按 a/a_initial 同时缩放晶胞和坐标；每个体积独立调用 GPAW。
4. 查看 output/gpaw-Al-a4.06.txt 的原始 GPAW 日志，确认电子能量约定与收敛状态。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 03_electronic_structure/06_periodic/run.py --output runs/06_periodic
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 分别增加 k 点与平面波截断，比较 a₀ 和 B；曲率通常比极小值位置更敏感。
- 基准 k=4 的 a₀ 约 4.04768 Å；已有 k=6、8 延伸结果约为 4.04205、4.03817 Å。不能因为一条曲线光滑就结束收敛。
- 改用仅压缩或仅拉伸的体积点，观察外推如何影响拟合；补点应围绕实际极小值。
- 在 Slurm 中运行新曲线：`sbatch scripts/slurm.sh 03_electronic_structure/06_periodic/run.py --calculate --output runs/new-Al`。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[ASE EOS](https://ase-lib.org/ase/eos.html)；[GPAW 平面波模式](https://gpaw.readthedocs.io/documentation/basic.html)。

## 从当前 CIF 新执行的例子

[output/native-cif-dft](output/native-cif-dft) 保存了从当前 Al.cif 和 lattice_scan.csv 新运行的 GPAW 曲线、原始 txt 与 eos.csv，a₀≈4.047757 Å、B≈79.944 GPa。它与默认历史表采用不同采样点；比较拟合差时要把体积网格也列为条件。
