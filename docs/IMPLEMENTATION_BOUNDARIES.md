# 哪些自己写，哪些交给成熟软件

学习目标决定实现边界。调用一个线性代数例程，并不会绕过 SCF 的学习目标；把整个 SCF 交给 `RHF.kernel()`，却会绕过。反过来，周期 DFT 项目的目标是设计与判断收敛实验，不是重新实现 PBE 或赝势。

下表中的“手写”指学生应实现、解释并能够修改的部分；NumPy 数组、BLAS/LAPACK、文件读取、绘图等基础设施都可使用。标为“比对”的项目必须保留独立路径，不能把同一个函数调用两次称为验证。

| 项目 | 学生手写 | 直接使用 | 验证对象与控制条件 |
|---|---|---|---|
| 单位与尺度 | 量纲分组、换算和 kBT | ASE/CODATA 常数 | 正反换算、已知尺度；不重写常数数据库 |
| Morse 能量与力 | 势函数、解析导数、差分检查 | ASE 坐标 I/O、MorsePotential | 相同 D、a、r0 的能量和 Cartesian force |
| 差分失效 | 步长扫描与误差分析 | 数组运算 | 解析导数作为基准；库数值差分不是独立真值 |
| 一维薛定谔 | 网格、边界条件、离散 Hamiltonian、归一化 | SciPy 对称本征求解 | 箱/振子解析谱、网格收敛；不手写 LAPACK |
| LCAO | 对称正交化和 H→H′→C 的变换 | NumPy eigh；SciPy generalized eigh 作参照 | 本征值、Hc−ESc、CᵀSC；向量允许整体相位差 |
| RHF | 密度、J/K、Fock、能量、SCF/DIIS | PySCF 产生 AO 积分；RHF 作独立参照 | 同几何、基组、电荷、自旋下的 S/X/D/F、电子数、总能量 |
| HF 失效 | 实验设计、误差归因 | PySCF RHF/UHF、spin_square | 伸键、自旋与基组扫描；不另造 UHF 积分程序 |
| DFT 对比 | 相同条件下比较方法并解释 | PySCF HF/LDA/PBE/B3LYP/FCI | 区分模型误差与数值误差；不手写 XC 泛函 |
| 周期 EOS | 构造收敛实验、单位与拟合判断 | ASE 结构、GPAW PBE、ASE EOS | 晶格常数和体模量；控制 k 点、截断能、展宽、体积网格 |
| 配分函数 | Z/p/U/F/S 与简并计数 | SciPy logsumexp | 显式能级求和及高低温极限；不是套热化学黑箱 |
| 分子热化学 | RRHO 各项与参考态合并 | PySCF 结构/梯度/Hessian；ASE IdealGasThermo 对照 | 同坐标、频率、对称数、自旋、T、p 的 ZPE/H/S/G |
| 化学势 | μ°+kBT ln(p/p°)、反应计量 | 表格 I/O | 标准态、压力斜率和自由能变号；无须另造 EOS 库 |
| 表面相图 | E−Nμ 与 lower envelope | ASE 读取结构；本例为明确合成状态能量 | 同面积、同参考；比较交叉点并辨认省略的熵 |
| 优化器 | 最速下降、回溯、力收敛判据 | SciPy BFGS 作对照；真实原子用 ASE | 同起点/势；比较盆地、终态梯度，而非迭代数 |
| MD | velocity Verlet 的两个半步 | ASE VelocityVerlet 作对照；势和 I/O 可用 ASE | 同质量、初态、时间单位；比较轨迹与能量误差 |
| Hessian | 力差分、质量加权、模式分析 | PySCF 解析 Hessian、ASE VibrationsData 作参照 | 同矩阵与质量；比较频率、零模、负模与子空间 |
| NEB | 切向量、真力/弹簧力投影、收敛 | ASE NEB/FIRE 作参照；后续原子路径使用 ASE | 相同端点、图像数、弹簧与势；不要求路径逐位相同 |
| TST | Eyring/Arrhenius、速率↔等待时间 | 物理常数、表格/绘图 | 零势垒、指数比率、温度极限；无须包一层反应器 |
| slab/吸附/真实 DFT | 问题、结构选择、参考能与收敛审计 | ASE 读 POSCAR/优化/约束；GPAW 电子结构 | 真正的 adsorption-energy 差；不能用 EMT 的收敛代替 DFT |
| umbrella | 简单采样器、WHAM 自洽方程 | PyMBAR 作独立重加权参照 | 相同窗口/轨迹、偏置、T；比较自由能形状、重叠、相关性 |
| MEP/FES | 最小化与边缘化的推导 | SciPy quadrature 作独立积分 | 加性常数对齐后比较；不把不同热力学对象硬凑成一样 |
| 反应网络 | 化学计量、质量作用式、详细平衡 | Cantera 加载原生 mechanism.yaml | kf/kr 和气体标准浓度；不把 1/s 与体积反应率混用 |
| 微动力学 | RHS、位点约束、稳态、TOF/反应级数 | SciPy stiff ODE；Cantera 独立表面动力学 | 同机制/标准态/T/分压/位点密度的覆盖度与 TOF |
| 速率控制 | 保持详细平衡的 TS 扰动及差分 | 已验证的求解器；Cantera rate multiplier 对照 | 比较 DRC；移动 TS 与改中间体能是两种不同实验 |
| 思考与检查点 | 推理、量级估计、反证实验、计算备忘录 | 上述结果与文献 | 不用一个返回布尔值的脚本冒充科学判断 |

## 每个可编程项目的阅读顺序

1. README 先说明要回答的问题、已有输入、公式及符号，再给实现步骤。
2. 先看每步的概念提示，再看索引/单位提示，最后看小段代码与中间数值。
3. `run.py` 是可运行的参考解；需要时 `prepare_*.py` 生成可独立读取的数据，`compare.py`/软件驱动提供另一条路径。
4. 对照 `output/report.txt`、矩阵和 CSV，而不只看一个最终小数或“tests passed”。
5. 解释一次受控失败：改变一个物理或数值假设，说明哪个观测会首先暴露它。

## 数据文件与软件输入

分子使用 XYZ；周期结构使用 CIF/POSCAR；积分与 Hessian 使用有明确维度、指标和单位的文本；轨迹、能级与能量扫描使用 CSV/DAT；Cantera 使用其原生 YAML。控制参数可以放在 TOML，但坐标、矩阵和数据表必须作为实际输入被读取。

旧版 JSON 运行记录仅用于追溯已经发生的计算。它们不是新版作业的输入界面，也不是学生应背诵的文件格式。
