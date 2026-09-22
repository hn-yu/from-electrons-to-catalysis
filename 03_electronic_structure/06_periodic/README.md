# 06 · 周期边界、体积与状态方程

本项目用周期 Al 晶体的能量—体积曲线提取平衡晶格常数和体模量，并检验数值设置是否足以支撑这些材料性质。

## 背景：为什么需要这一步

孤立分子的坐标可以放在开放空间中；晶体则由晶胞沿晶格方向无限重复。周期边界让有限输入代表宏观材料，但电子态也必须满足相应的平移对称性。Bloch 描述把问题分成不同波矢 k 的电子态，实际计算用有限 k 点对布里渊区积分进行近似。

平面波是周期问题方便的基函数。截断能决定保留多少平面波，k 点密度决定周期电子态采样有多细；两者控制不同数值误差。GPAW 用 PAW 方法处理原子附近的电子结构细节，本项目直接使用成熟实现，学习如何设置和检验计算。

材料受压时总能随体积变化。曲线最低点给出零外压平衡体积，曲率说明压缩有多困难，即体模量。拟合一条光滑曲线只能压缩数据，不能消除数据自身的 k 点、基组或体积采样误差。

## 开始前需要理解的概念

- **原胞与常规晶胞**：同一晶体的不同描述；比较能量和体积时必须统一到每原子或同一晶胞。
- **晶格常数 a**：本例是面心立方常规晶胞的边长，不能直接当作每原子体积的立方根。
- **k 点**：倒空间的数值积分采样，不是实空间原子数。
- **截断能**：限制平面波动能的上限，与最终总能数值不是同一个量。
- **状态方程 EOS**：用参数化 E(V) 表达压缩响应；B 的单位是压力。

## 本次任务：从什么得到什么

先读取真实 GPAW 计算留下的 eos.csv，按 scenario 分组，用 ASE EquationOfState 拟合并比较 a₀、B。然后检查 Al.cif 与 lattice_scan.csv 如何定义一个新的体积扫描。默认命令只分析已有数据；带 --calculate 才从当前 CIF 启动新的 GPAW 电子结构计算，应提交 Slurm。

## 先用一个小例子走通思路

FCC 常规晶胞含四个原子。若 $a=4$ Å，则每原子体积为 $a^3/4=16$ Å³；把 64 Å³ 与每原子能量配对，会直接破坏归一化。

已有 k=4、6、8 数据给出的 a₀ 约为 4.04768、4.04205、4.03817 Å。即使每条拟合曲线都很平滑，晶格常数仍随采样改变。体模量依赖二阶导数，因此还应单独检查其变化，不能从 a₀ 稳定推断 B 必然稳定。

## 实现边界

**直接用 ASE/GPAW** 读取 CIF、求平面波 PAW/PBE 能量并用 ASE EquationOfState 拟合。**手写**原胞归一化、体积扫描和收敛设计；不重写平面波 DFT。默认先分析既有真实 PBE 表，`--calculate` 才启动新计算。

## 输入与物理模型

- [Al.cif](input/Al.cif)
- [control.toml](input/control.toml)
- [eos.csv](input/eos.csv)
- [lattice_scan.csv](input/lattice_scan.csv)

`Al.cif` 给出真实原胞及坐标。`lattice_scan.csv` 指定 a，`eos.csv` 给出已执行 GPAW 的每原子 $V,E$；`control.toml` 指定新计算的截断能、k 点与展宽。

面心立方的每原子体积是 $V=a^3/4$。压力和体模量来自能量曲率：

```math
P=-\frac{dE}{dV},\qquad B=V\frac{d^2E}{dV^2}\bigg|_{V_0}.
```

三阶 Birch–Murnaghan 表达式令 $\eta=(V_0/V)^{2/3}$：

```math
E(V)=E_0+\frac{9V_0B_0}{16}\{B'_0(\eta-1)^3+(\eta-1)^2(6-4\eta)\}.
```

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

## 分步提示与资料

[ASE EOS](https://ase-lib.org/ase/eos.html)；[GPAW 平面波模式](https://gpaw.readthedocs.io/documentation/basic.html)。

## 从当前 CIF 新执行的例子

[output/native-cif-dft](output/native-cif-dft) 保存了从当前 Al.cif 和 lattice_scan.csv 新运行的 GPAW 曲线、原始 txt 与 eos.csv，a₀≈4.047757 Å、B≈79.944 GPa。它与默认历史表采用不同采样点；比较拟合差时要把体积网格也列为条件。

## 完成后应能解释什么

先读拟合的 a₀/B，再回到原始 E(V) 点、scenario 设置和 GPAW 日志，确认极小值在采样区间内。完成后应能说明曲线以什么单位、按多少原子归一化，以及下一笔计算应增加 k 点、截断能还是体积点。

## 与前后项目的关系

承接 [DFT](../05_dft/README.md)；[电子结构检查点](../07_checkpoint/README.md) 总结数值与模型误差。周期几何和收敛设计会在 [表面 slab](../../06_catalysis/01_slab/README.md) 中继续使用。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
