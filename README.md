# From Electrons to Catalysis

从原子坐标出发，学习电子能量怎样经过自由能、反应路径与状态人口，最终连接到催化观测量。每一层都要回答三个问题：**公式中的对象是什么，程序如何计算它，什么证据能说明结果可信。**

教学组织参考 [ProgrammingProjects](https://github.com/hn-yu/ProgrammingProjects)：给出可检查的坐标、积分或数据表，分步推导，保存中间矩阵与数值，再通过渐进提示完成实现。这里的公式、讲解和练习针对本课程重新编写。

## 哪些应该自己写

| 学习对象 | 自己完成 | 成熟工具与独立核对 |
|---|---|---|
| 能量与力、LCAO、RHF | 导数、正交化、密度/Fock/能量/DIIS | ASE 势、SciPy 广义本征、PySCF RHF；积分直接由 PySCF 生成 |
| 振动、热化学 | Hessian 索引与质量加权、RRHO 分项 | PySCF 梯度/Hessian；ASE 模式与 IdealGasThermo |
| 优化、MD、NEB | 回溯、Verlet、切线与力投影 | SciPy BFGS、ASE VelocityVerlet/NEB |
| 自由能与反应网络 | WHAM、质量作用、详细平衡、速率控制 | PyMBAR FES、Cantera 原生 YAML 与表面动力学 |
| 分子/周期 DFT | 问题定义、参考态、收敛实验与结果解释 | 直接使用 PySCF、ASE/GPAW，不重写生产级电子结构软件 |

[逐项目实现边界](docs/IMPLEMENTATION_BOUNDARIES.md) 说明每次对照固定什么、检验什么。线性代数、结构读写、PAW、通用刚性求解器由成熟库提供；同一物理问题上自己实现的教学核心再与独立路径比较。

## 先完整走过一个例子

推荐从 [RHF 项目](03_electronic_structure/03_rhf/README.md) 开始：

1. 读 H₂/HeH⁺/LiH/H₂O 的 **XYZ** 和基组/电荷表。
2. 从带指标的 **DAT 积分**恢复 S、T、V 与双电子积分；核对八重对称和电子数。
3. 根据正文推导 X、D、J、K、F 和总能；完成 SCF，保存每一步矩阵和残差。
4. 独立运行 PySCF，逐项比对；用六份提示定位因子 2、积分指标或能量双计错误。

随后用 [水分子 Hessian 项目](05_kinetics/03_hessian/README.md) 完成另一个完整例子：真实优化坐标与 9×9 Hessian → 质量加权 → 刚体/内部模式 → ASE 对照 → 同位素与负曲率实验。

## 安装与运行

使用 Python 3.11+。完整安装和 GPAW 编译要求见 [INSTALL.md](INSTALL.md)。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[quantum,reference,test]'
```

在本 Slurm 集群上，计算与完整测试提交作业；按本机环境调整 scripts/slurm.sh 的分区与资源：

```bash
sbatch scripts/slurm.sh 03_electronic_structure/03_rhf/run.py --output runs/rhf
sbatch scripts/slurm.sh 03_electronic_structure/03_rhf/compare.py
sbatch scripts/slurm.sh 05_kinetics/03_hessian/run.py --output runs/vibrations
sbatch scripts/slurm.sh scripts/run_all.py --tiers core quantum periodic
sbatch scripts/slurm.sh -m pytest -q
```

`--input` 接收包含科学文件的**目录**，`--output` 指定新结果目录。输入使用 XYZ/EXTXYZ、CIF/POSCAR、DAT、CSV 与 Cantera YAML；TOML 只放控制参数。主输出是 report.txt、矩阵、轨迹、表格和软件原始日志，JSON 仅作附属审计记录。

DFT 项目默认分析仓库已执行的 PBE 数据。只有 `--calculate` 才调用 GPAW 进行新计算：

```bash
sbatch scripts/slurm.sh 03_electronic_structure/06_periodic/run.py --calculate --output runs/new-Al
sbatch scripts/slurm.sh 07_real_system/02_real_dft/run.py --calculate --output runs/new-H-Cu
```

学生先依据公式完成自己的实现，再使用 run.py 与共享核心作为参考解。每个 README 给出受控实验；hints 分步展开推导与排错。书面项目提供具体案例、公式和参考分析。

## 如何使用结果

算法一致与物理可信需要分别论证。自写 RHF 与 PySCF 一致不修复 RHF 的解离近似；WHAM 与 PyMBAR 一致不证明隐藏变量采样充分；GPAW 作业完成也不证明 slab 收敛。

真实 H/Cu 示例目前的三层与四层吸附能差约 0.35 eV，超过事先设定的 0.05 eV。它保留为一次失败的收敛假设，用于设计下一轮实验。旧输入、输出与预测保存在各项目 output 的历史文件中，新文档不改变历史预测的时间身份。

## 课程项目

| 项目 | 学习入口 |
|---|---|
| [01_intro/01_hamiltonian](01_intro/01_hamiltonian/README.md) | 01 · 从坐标写出电子—核 Hamiltonian |
| [01_intro/02_emulation](01_intro/02_emulation/README.md) | 02 · 用模拟器调通流程，再明确换模型 |
| [01_intro/03_prediction_log](01_intro/03_prediction_log/README.md) | 03 · 把预测写成可以被结果改变的判断 |
| [02_bringup/01_units](02_bringup/01_units/README.md) | 01 · 让单位在公式两边闭合 |
| [02_bringup/02_forces](02_bringup/02_forces/README.md) | 02 · 从两原子坐标到一致的能量和力 |
| [02_bringup/03_finite_differences](02_bringup/03_finite_differences/README.md) | 03 · 为什么更小的差分步长反而更差 |
| [03_electronic_structure/01_schrodinger](03_electronic_structure/01_schrodinger/README.md) | 01 · 从势能表组装薛定谔算符 |
| [03_electronic_structure/02_lcao](03_electronic_structure/02_lcao/README.md) | 02 · 非正交基组中的本征问题 |
| [03_electronic_structure/03_rhf](03_electronic_structure/03_rhf/README.md) | 从 AO 积分到 restricted Hartree–Fock：自己完成一次 SCF |
| [03_electronic_structure/04_break_hf](03_electronic_structure/04_break_hf/README.md) | 04 · 让 Hartree–Fock 暴露自己的近似 |
| [03_electronic_structure/05_dft](03_electronic_structure/05_dft/README.md) | 05 · 同一有限基组里的 HF、DFT 与 FCI |
| [03_electronic_structure/06_periodic](03_electronic_structure/06_periodic/README.md) | 06 · 周期边界、体积与状态方程 |
| [03_electronic_structure/07_checkpoint](03_electronic_structure/07_checkpoint/README.md) | 07 · 电子结构结果的四层核对 |
| [04_thermodynamics/01_partition](04_thermodynamics/01_partition/README.md) | 01 · 从能级表到自由能 |
| [04_thermodynamics/02_molecular_thermochemistry](04_thermodynamics/02_molecular_thermochemistry/README.md) | 02 · 从分子坐标到气相 Gibbs 自由能 |
| [04_thermodynamics/03_chemical_potential](04_thermodynamics/03_chemical_potential/README.md) | 03 · 压力通过化学势改变吸附方向 |
| [04_thermodynamics/04_surface_phase](04_thermodynamics/04_surface_phase/README.md) | 04 · 用巨势比较不同覆盖度 |
| [04_thermodynamics/05_checkpoint](04_thermodynamics/05_checkpoint/README.md) | 05 · 电子能、自由能与储库的检查点 |
| [05_kinetics/01_optimizer](05_kinetics/01_optimizer/README.md) | 01 · 优化的是驻点，还是你希望的结构 |
| [05_kinetics/02_dynamics](05_kinetics/02_dynamics/README.md) | 02 · 用能量误差检验 Velocity Verlet |
| [05_kinetics/03_hessian](05_kinetics/03_hessian/README.md) | 从 Cartesian Hessian 到正常振动：曲率、质量和虚频 |
| [05_kinetics/04_neb](05_kinetics/04_neb/README.md) | 04 · 把真实力与弹簧力放在正确方向 |
| [05_kinetics/05_tst](05_kinetics/05_tst/README.md) | 05 · 势垒如何变成时间尺度 |
| [05_kinetics/06_checkpoint](05_kinetics/06_checkpoint/README.md) | 06 · 从力到速率，哪一步证明了什么 |
| [06_catalysis/01_slab](06_catalysis/01_slab/README.md) | 01 · 收敛一个可解释的表面观测量 |
| [06_catalysis/02_adsorption](06_catalysis/02_adsorption/README.md) | 02 · 吸附位点竞争与参考态 |
| [06_catalysis/03_umbrella](06_catalysis/03_umbrella/README.md) | 03 · 从有偏轨迹恢复自由能 |
| [06_catalysis/04_mep_fes](06_catalysis/04_mep_fes/README.md) | 04 · 最低能量路径为什么不是自由能路径 |
| [06_catalysis/05_reaction_network](06_catalysis/05_reaction_network/README.md) | 05 · 从状态能量构造满足详细平衡的网络 |
| [06_catalysis/06_microkinetics](06_catalysis/06_microkinetics/README.md) | 06 · 覆盖度与基元速率共同决定 TOF |
| [06_catalysis/07_rate_control](06_catalysis/07_rate_control/README.md) | 07 · 用扰动代替“最高势垒就是决速步”的直觉 |
| [06_catalysis/08_checkpoint](06_catalysis/08_checkpoint/README.md) | 08 · 从一个势垒到催化观测量 |
| [07_real_system/01_calculation_memo](07_real_system/01_calculation_memo/README.md) | 01 · 先写计算备忘录，再申请资源 |
| [07_real_system/02_real_dft](07_real_system/02_real_dft/README.md) | 02 · 用真实 PBE 计算回答一个有限问题 |
| [07_real_system/03_blind_prediction](07_real_system/03_blind_prediction/README.md) | 03 · 保留真正的事前与事后记录 |
| [07_real_system/04_bringup_analysis](07_real_system/04_bringup_analysis/README.md) | 04 · 失败的收敛假设怎样产生下一步 |
| [07_real_system/05_advisor_defense](07_real_system/05_advisor_defense/README.md) | 05 · 对“算一个 NEB 就证明迁移”进行答辩 |

[原课程大纲](COURSE_OUTLINE.md) · [实现边界](docs/IMPLEMENTATION_BOUNDARIES.md) · [安装说明](INSTALL.md)
