# 01 · 收敛一个可解释的表面观测量

本项目用有限厚度的周期薄板代表 Cu(111) 表面，围绕 H 吸附能设计收敛实验，判断这个表面模型是否足够可靠。

## 背景：为什么需要这一步

真实晶体表面在横向延伸，在垂直方向一侧是固体、另一侧是环境。周期电子结构程序通常在三个方向都重复晶胞，因此采用 slab：保留有限原子层，加入真空把相邻重复薄板分开。层数、真空和底部约束都会影响这个近似。

表面研究关心的是反应或吸附的能量差，而不是单个体系的巨大总能。清洁表面、含吸附物表面和气体参考必须采用一致的能量约定和适当数值设置；某些误差在相减时抵消，另一些则会保留。

收敛计划应直接检验目标观测量。增加 k 点、截断能或 slab 厚度后，吸附能是否进入预先要求的容限？横向扩大晶胞时还要检查覆盖度是否同时改变，因为改变实际吸附密度是一项物理实验，不能只当成数值精度提高。

## 开始前需要理解的概念

- **slab**：带真空的有限层周期表面模型。
- **Cu(111)**：FCC 铜的一种晶面方向，括号中的整数为晶面指标。
- **固定层**：用原子约束近似体相支撑，约束方案属于模型定义。
- **吸附能**：这里以半个 H₂ 为 H 的参考，负值表示对应电子能反应放热。
- **单因素扫描**：相对基准只改变一个设置，便于定位差异来源。

## 本次任务：从什么得到什么

cases.csv 为每个变体指定独立的 clean/fcc POSCAR、H₂ EXTXYZ 与 calculator.toml。默认读取真实 PBE energies.csv，手写吸附能与相对基准差，按 0.05 eV 容限审核。需要新增证据时才用 --calculate 经 ASE/GPAW 在 Slurm 上重算所有列出的案例。

## 先用一个小例子走通思路

当前三层基准约为 +0.0456 eV，四层约为 −0.3018 eV，差约 −0.3474 eV。既超过 0.05 eV 容限，又改变符号，所以不能从基准宣称吸附必然吸热。

1×1 表面胞放一个 H 是 1 ML；2×2 放一个 H 是 0.25 ML。即使软件参数完全一致，这两项也在比较不同覆盖度，因此其差异不能全部归为“超胞数值误差”。

## 实现边界

**直接用 GPAW/PBE 与 ASE** 做电子结构、结构读写和优化；**手写**能量差、单因素收敛与覆盖度核对。默认分析真实计算表；`--calculate` 对 cases.csv 中每套 POSCAR 重新计算。

## 输入与物理模型

- [baseline/H2.extxyz](input/baseline/H2.extxyz)
- [baseline/calculator.toml](input/baseline/calculator.toml)
- [baseline/clean.POSCAR](input/baseline/clean.POSCAR)
- [baseline/fcc.POSCAR](input/baseline/fcc.POSCAR)
- [cases.csv](input/cases.csv)
- [control.toml](input/control.toml)
- [cutoff_eV-0/H2.extxyz](input/cutoff_eV-0/H2.extxyz)
- [cutoff_eV-0/calculator.toml](input/cutoff_eV-0/calculator.toml)
- [cutoff_eV-0/clean.POSCAR](input/cutoff_eV-0/clean.POSCAR)
- [cutoff_eV-0/fcc.POSCAR](input/cutoff_eV-0/fcc.POSCAR)
- [energies.csv](input/energies.csv)
- [fixed_layers-0/H2.extxyz](input/fixed_layers-0/H2.extxyz)

完整清单与单位见 [input/README.md](input/README.md)。

输入 `cases.csv` 的每行指向一个独立目录，包含 clean.POSCAR、fcc.POSCAR、H2.extxyz 和 calculator.toml。数据源见 DATA_SOURCE.md。

```math
E_{ads}=E_{slab+H}-E_{slab}-\frac12E_{H_2},
```

```math
\delta_j=E_{ads}(q_j)-E_{ads}(q_0).
```

$q_j$ 是只改变一项的计算设置。截断能、k 点、真空、层数、固定层和电子展宽分别扫描，不能拿不同设置的 clean 与 adsorbed 能量相减。

1×1 表面胞中一个 H 是 1 ML；2×2 中一个 H 是 0.25 ML。横向扩胞同时改变覆盖度，因此该轴不单是数值收敛。

## 从公式到程序

1. 读每个 case 的总能量三元组，自己重新计算 Eads。
2. 输出相对基准变化，并与事先指定的 0.05 eV 阈值比较。
3. 对变化大的轴解释可能物理来源；继续增加该轴，而不是用其他轴的小差异抵消它。
4. 新计算命令为 `sbatch scripts/slurm.sh 06_catalysis/01_slab/run.py --calculate --output runs/new-slab`，会执行输入表全部 case。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 06_catalysis/01_slab/run.py --output runs/01_slab
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 已有 1×1×3 基准 Eads 约 +0.0456 eV；增加到四层变为约 −0.3018 eV，厚度差约 0.35 eV，远超阈值。
- 将每个 case 的三个参考能都打印，检查总能量是否虽然变化很大，但差值发生抵消。
- 下一轮保持覆盖度固定增加层数，事前指定何种平台趋势足以改变当前“未收敛”的判断。

## 分步提示与资料

[GPAW 表面计算](https://gpaw.readthedocs.io/tutorialsexercises/structureoptimization/surface/surface.html)；[ASE 约束](https://ase-lib.org/ase/constraints.html)。

## 完成后应能解释什么

先从每个 case 的三个总能独立重算 Eads，再查看各轴变化和结构条件。完成后应能指出当前最大未解决差异及下一轮优先计算，并说明为什么其他轴变化小不能抵消厚度轴失败。

## 与前后项目的关系

需要 [周期计算](../../03_electronic_structure/06_periodic/README.md) 和 [化学势](../../04_thermodynamics/03_chemical_potential/README.md) 的参考态概念；下一项 [吸附位点](../02_adsorption/README.md) 比较相同表面上不同局部结构。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
