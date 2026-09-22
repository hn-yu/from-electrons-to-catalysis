# 安装、计算资源与数据约定

使用 Python 3.11+。参考环境为 Python 3.11.13；`requirements-lock.txt` 保存实际安装版本。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[quantum,reference,test]'
```

基础依赖 NumPy/SciPy/ASE 处理数组、线性代数和结构；`quantum` 添加 PySCF；`reference` 添加 Cantera、PyMBAR 和 YAML 导出工具；`test` 添加 pytest。Cantera 与 PyMBAR 在对应项目中实际参与独立求解，不能省略后仍宣称已完成比对。

## GPAW

周期新计算需要 GPAW 25.7 与 PAW 数据。按照 [官方安装文档](https://gpaw.readthedocs.io/install.html) 准备 C 编译器、BLAS 与匹配版本的 LibXC。实际参考使用 GPAW 25.7.0，本仓库限制为 `<26`。

```bash
python -m pip install -e '.[periodic]'
```

非标准库路径可用自定义 GPAW 构建配置；以下占位路径需要替换：

```python
# gpaw-config.py
compiler = 'gcc'
mpi = False
libraries = ['xc', 'blas']
include_dirs = ['/path/to/libxc/include']
library_dirs = ['/path/to/libxc/lib', '/path/to/blas/lib']
runtime_library_dirs = library_dirs
```

```bash
GPAW_CONFIG=/absolute/path/gpaw-config.py python -m pip install 'gpaw==25.7.0' gpaw-data
```

头文件与共享库版本必须匹配，静态库需要位置无关代码。本集群参考构建使用 PySCF 随包提供的匹配 LibXC 和系统 BLAS；这些机器路径不写死在课程代码中。

## Slurm

`scripts/slurm.sh` 使用 intel96 分区、4 CPU、12 GB、2 小时。这里的 GPAW 为串行构建配 CPU 线程，无需 GPU。其他集群应按其 MPI/GPAW 安装调整。复杂构建、计算及完整测试均在计算节点执行。

```bash
sbatch scripts/slurm.sh scripts/run_all.py --tiers core quantum periodic
sbatch scripts/slurm.sh -m pytest -q
```

上面的 `periodic` 是 DFT 数据分析项目层级，不自动启动新 DFT。实际新计算明确加 `--calculate`：

```bash
sbatch scripts/slurm.sh 03_electronic_structure/06_periodic/run.py --calculate --output runs/new-Al
sbatch scripts/slurm.sh 07_real_system/02_real_dft/run.py --calculate --output runs/new-H-Cu
```

表面案例也可单独执行：

```bash
sbatch --array=0-7 scripts/slurm.sh scripts/slab_task.py \
  --input 07_real_system/02_real_dft/input --output runs/H-Cu-cases
```

数组每项根据 cases.csv 读取对应目录的 POSCAR/EXTXYZ/calculator.toml，输出独立 energies.csv 和软件日志。它不会自动把未完成任务标记为完成，也不会复用旧 JSON 缓存。默认完整 runner 会重新执行所列案例；若只需一个案例，使用数组范围或 `--index`。

## 从结构重新生成教学数据

RHF 的默认学生路径从文本积分开始。改变坐标、基组或电荷后，先生成新积分，再运行与独立比对：

```bash
sbatch scripts/slurm.sh 03_electronic_structure/03_rhf/prepare_integrals.py
sbatch scripts/slurm.sh 03_electronic_structure/03_rhf/run.py
sbatch scripts/slurm.sh 03_electronic_structure/03_rhf/compare.py
```

上面三条有前后依赖，实际提交时等待前一步完成，或用 `--dependency=afterok:JOBID` 串联。水 Hessian 的 `prepare_hessian.py` 同样是先用 PySCF 生成可检查的真实矩阵，`run.py` 再完成质量加权与 ASE 对比。

改变动力学状态能量表后，显式运行对应项目的 `make_mechanism.py` 更新 Cantera YAML，检查变更，再求解。两套不同输入不应期待给出一致结果。

## 单位和输出

- 分子坐标：Å；周期结构：CIF/POSCAR 自带晶胞与坐标约定。
- AO 积分、SCF 能量：Hartree；电子结构 Hessian：Hartree/bohr²；质量：u。
- 通用能量：eV；力：eV/Å；温度：K；气体输入压力：bar。
- Cantera YAML：m、kmol、s，活化能 J/kmol；气体标准压力 1 bar。
- 二维势使用明确的模型坐标；MD 的谐振子扫描使用约化单位，原子积分器对照使用 ASE 内部时间单位并另报 fs。

主结果为 report.txt、DAT/CSV、优化坐标与软件日志。附属 result.json 保存输入与代码文件哈希、软件版本、启动 HEAD 和 Slurm 作业号。工作树未提交时，以实际源文件哈希为准。

GPAW 能量相减一致使用 ASE 默认 extrapolated electronic energy。优化器日志中的 force-consistent free energy 不可混入参考。电子展宽与有限温热化学不同；后者需要 RRHO、储库与必要的构型统计。

SCF/优化/NEB/WHAM 未达到求解停止条件会报错；目标观测量不满足物理收敛容限则保留测量和失败判断。缺库会报错，不会将 GPAW 请求替换为 EMT。
