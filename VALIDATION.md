# 验证对象、结果与限制

本次重做的重点是把公式、科学输入、中间数据与独立参考连起来。下面记录实际运行的证据；教学质量还需要通过项目中的推导和受控实验判断，不能由测试数量替代。

## 自己实现后与成熟工具比较

| 对象 | 独立路径 | 实际观察 |
|---|---|---|
| Morse 能量/力 | ASE MorsePotential，匹配参数与截断 | 径向及笛卡尔力在浮点精度内一致 |
| LCAO | 自己正交化；SciPy generalized eigh | 本征值、度量归一化与残差一致 |
| RHF | 文本 AO 积分上的自写 SCF；从 XYZ 新运行 PySCF | H₂、HeH⁺、LiH、H₂O 能量差 <10⁻¹² Hartree；电子数、D、F 也核对 |
| 水的振动 | 自写质量加权；ASE VibrationsData | 内部频率约 2169.851、4139.636、4390.673 cm⁻¹；差 <2×10⁻⁵ cm⁻¹ |
| RRHO | 自写 H/S/G；ASE IdealGasThermo | 四个分子 G 的差约 10⁻⁷ eV；同几何/频率/标准态 |
| 优化 | 自写 Armijo 下降；SciPy BFGS | 比较各起点的驻点、能量与力，不比较迭代数 |
| Verlet | 自写积分器；ASE VelocityVerlet | 同势、质量、初态、内部时间单位，最大轨迹差约 4×10⁻¹⁵ Å |
| NEB | 自写投影；ASE NEB/FIRE | 模型势垒约 1.056244 eV，两者差约 0.000320 eV |
| WHAM | 自写分箱自洽；PyMBAR FES | 同轨迹形状 RMS 差约 0.000053/0.000149 eV，分别为一维/二维 |
| 表面稳态 | 自写质量作用方程；Cantera 原生 YAML | 多个 T/p 点的覆盖度与净通量一致；600 K 基准 TOF≈752320.86 s⁻¹ |
| 速率控制 | 过渡态能量差分；Cantera 正逆共同倍率 | Xi≈(0.02558,0.00294,0.97148)，差分误差内一致 |

相同输入上的软件对照检查实现。RHF 近似、RRHO 范围、采样遍历性和机制完整性是额外问题，正文专门给出反例。

## 真实结构与 GPAW

Slurm 705355 从 `Al.cif` 重新生成 PBE 体积扫描；新曲线拟合 a₀≈4.047757 Å、B≈79.944 GPa。扫描点与历史曲线不同，所以不要求拟合参数逐位一致。新 GPAW 日志、能量表与记录位于周期项目 output/native-cif-dft。

Slurm 705354 直接读取 H/Cu 基准 `fcc.POSCAR`，执行 PBE 单点并核对坐标/晶胞保持原输入。能量约 −11.985586 eV；最大允许自由度力约 1.66949 eV/Å，明确是**未松弛单点接口检查**，不作为吸附能或驻点结果。文件位于真实 DFT 项目 output/native-poscar-check。

主吸附案例分析先前实际执行的 PBE 数据，能量三元组导出为 CSV，各 case 提供完整起始结构与软件参数。保留已有原始软件日志和历史记录；新的 `--calculate` 驱动关闭点群对称，旧数据部分保留初始对称，故重新优化路径可能不同。

三层→四层的吸附能变化约 0.35 eV，超过既定 0.05 eV。这一失败保留；新接口、更多提示和测试通过都没有消除它。横向单 H 扩胞同时改变覆盖度，也明确单独解释。

## 运行与审计

- 705334：PySCF 从四组 XYZ 生成带指标的真实 AO 文本积分。
- 705335：PySCF 优化水并生成 9×9 笛卡尔 Hessian。
- 705344/705345：原生文件入口的核心/分子案例；含 ASE、PyMBAR、Cantera 对照。
- 705360：再次独立检查 XYZ/积分/电子数及 RHF 总能、密度、Fock 矩阵。
- 705362：所有计算项目通过公开 run.py 入口重新运行；周期/表面默认模式为已执行 PBE 数据分析。
- 705363：当前完整测试，含修改 XYZ 会改变力及输入哈希、独立 Cantera 温压点、积分与真实坐标匹配。

`python scripts/check_projects.py` 检查所有项目的原生输入、输出及源码文件 SHA-256，并检查当前 README/hints 的本地链接。报告中记录实际源文件哈希、启动 HEAD、软件版本和作业号；工作树尚未提交时，不把 HEAD 误称为源文件的完整身份。

```bash
sbatch scripts/slurm.sh -m pytest -q
python scripts/check_projects.py
sbatch scripts/slurm.sh scripts/run_all.py --tiers core quantum periodic
```

GitHub Actions 安装 quantum/reference/test 依赖，运行数值测试和原生输入审计。CI 不安装 GPAW 编译栈，新 DFT 已在 Slurm 单独执行。此前计算与预测的验证历史保存在 [PREVIOUS_VALIDATION.md](docs/PREVIOUS_VALIDATION.md)。
