# 02 · 用真实 PBE 计算回答一个有限问题

本项目用真实 GPAW/PBE 数据检验一个具体的 H/Cu(111) 吸附假设，并保留从原生结构、软件日志到误差判断的完整证据。

## 背景：为什么需要这一步

前面在解析模型上可以用已知答案判断算法。真实材料没有这样的通用标准答案，需要用结构核对、独立参考、软件收敛和参数扫描逐层建立可信度。本项目把这些步骤合在同一个有限问题上，而不是把“调用 DFT 成功”作为终点。

初始 bringup 计算的作用是确认输入和工作流能运行，并暴露主导误差。最小可运行设置不必已经足以发表；若它的失败能指向下一轮更有价值的计算，同样构成有用结果。关键是公开保留失败的容限和原始证据。

本项目复用表面章节的真实能量档案，重点转为研究判断与可追溯执行。默认分析已有数据，显式 --calculate 才从当前 POSCAR/EXTXYZ 重新进行 PBE 计算，两种运行回答的问题应在报告中区分清楚。

## 开始前需要理解的概念

- **PBE / PAW**：分别是交换关联近似与电子结构表示方法，本项目通过 GPAW 使用。
- **单点与几何优化**：前者固定坐标计算能量/力，后者继续移动原子至规定受力条件。
- **bringup**：用较小设置调通真实软件与数据流，并识别需要继续检验的部分。
- **可追溯结果**：结构、参数、日志、能量参考和分析对应同一组明确输入。
- **收敛失败**：目标量对设置变化超过预定容限，是需要解释和延伸的证据。

## 本次任务：从什么得到什么

从 cases.csv 定位基准与七个变体的完整结构和参数，独立重算 energies.csv 中的吸附能。审核 0.05 eV 容限、覆盖度和厚度影响。若执行新计算，用 Slurm 调用 --calculate，保存 GPAW 原始日志、优化轨迹和最终结构，再重新进行同一项审核。

## 先用一个小例子走通思路

三层基准吸附能约 +0.04560 eV，四层约 −0.30182 eV。因此当前数据已经否定“这套基准在厚度上达到 0.05 eV 容限”的声明；不能因四层数值看起来更合理就跳过继续收敛。

另外保存的 native-poscar-check 是从当前结构执行的单点，最大力约 1.67 eV/Å。它证明了原生结构可以进入 GPAW 并返回能量/力，但尚未证明该结构为吸附驻点。

## 实现边界

**直接用 ASE/GPAW** 的周期 PAW/PBE、优化器和结构文件；**手写**反应参考、误差预算和下一轮计算设计。默认分析已执行数据；新计算用 `--calculate`，绝不静默退回 EMT。

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

`cases.csv` 指向基准与七个单因素变体，每个目录给出完整坐标和 calculator.toml；`energies.csv` 保存每套独立计算的 clean/H₂/adsorbed 总能量。

```math
\Delta E_{ads}=E[H/Cu(111)]-E[Cu(111)]-\frac12E[H_2].
```

基准是 1×1×3、一个 H、1 ML、250 eV、3×3×1 k 点。它是一套 bringup 起点，不是已收敛表面模型。

```math
\epsilon_q=|\Delta E_{ads}(q_{refined})-\Delta E_{ads}(q_{base})|.
```

既定容限是 0.05 eV；对已执行变体检验这个声明，不把失败的容限在结果出现后悄悄放宽。

## 从公式到程序

1. 先读本节 calculation memo 和 blind prediction，区分历史事前记录与现在已经知道的数值。
2. 检查每个 POSCAR 的原子数、层数、晶胞、真空与 Selective dynamics；H₂ 参考使用独立分子盒。
3. 默认运行完成表格分析；执行 `sbatch scripts/slurm.sh 07_real_system/02_real_dft/run.py --calculate --output runs/new-real-dft` 则真正运行全部案例。
4. 新运行保存 GPAW 原始 txt、优化日志和 relaxed.extxyz，停止条件失败会报错。
5. 写出数据支持的有限结论，并优先补计算厚度失败的轴。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 07_real_system/02_real_dft/run.py --output runs/02_real_dft
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 基准吸附能 +0.04560 eV；四层约 −0.30182 eV，说明当前吸附符号对 slab 厚度不稳定。
- 2×2×3、单 H 变成 0.25 ML，结果约 −0.08851 eV。将其同时标为覆盖度变化，不能仅称为“超胞误差”。
- 提出保持覆盖度与底部约束一致的 4/5/6 层后续计划，并事前定义平台判据。
- 当前数据不能支持可靠位点排序、有限温 TOF 或实验活性结论；列出每个推断还缺哪种信息。

## 分步提示与资料

[GPAW 安装与文档](https://gpaw.readthedocs.io/)；本仓库 [安装说明](../../INSTALL.md)。

## 原生结构接口检查

[output/native-poscar-check](output/native-poscar-check) 是直接从当前 fcc.POSCAR 新执行的 PBE 单点，保留软件原始日志与带能量/力的 EXTXYZ。最大力约 1.67 eV/Å，未作几何优化，因此仅验证输入和软件接口，不能充当吸附驻点或收敛证据。

## 完成后应能解释什么

先读每个 case 的结构/参数与原始总能，再读收敛差值和结论。完成后应能独立复核报告，并将“接口已通”“几何已优化”“目标量已收敛”“物理模型适用”分别对应到实际证据。

## 与前后项目的关系

前置是 [计算备忘录](../01_calculation_memo/README.md)，新计算的预测先记录于 [预测项目](../03_blind_prediction/README.md)。下一项分析任务是 [bringup 复盘](../04_bringup_analysis/README.md)。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
