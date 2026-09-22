# 从 Cartesian Hessian 到正常振动：曲率、质量和虚频

本项目从真实水分子坐标和二阶导数矩阵得到正常振动，解释曲率如何判断结构稳定性，以及质量如何把曲率变成频率。

## 背景：为什么需要这一步

最大力很小只说明一阶导数接近零。在山谷底部和山口鞍点，一阶导数都可能为零；区别在于向各方向轻推后，能量是升高还是降低。Hessian 是所有坐标二阶导数组成的矩阵，记录这种局部曲率与不同位移之间的耦合。

原子振动通常不是某个原子沿某个轴单独运动，而是多个原子按固定比例协同运动。将驻点附近的能量展开到二阶，并代入 Newton 方程，可以得到正常模式的本征问题。质量不同意味着同一恢复力产生不同加速度，所以不能直接把 Hessian 的普通本征值开方当作频率。

本项目使用 PySCF 生成的水分子解析 Hessian，自己完成可检查的质量加权和单位转换，再与 ASE 对照。另用低维势的力差分检查 Hessian 构造和驻点分类，将电子结构软件的工作与后处理的工作分开。

## 开始前需要理解的概念

- **Cartesian Hessian**：3N×3N 二阶导数矩阵，包含所有原子和笛卡尔方向的耦合。
- **正常模式**：在线性近似下可独立振动的协同位移方向。
- **质量加权**：把 H a=ω²M a 转成普通对称本征问题。
- **波数 cm⁻¹**：光谱常用频率单位，与角频率相差 2π 和光速的换算。
- **零模与虚频**：零模常来自刚体运动，负曲率对应虚频；必须结合位移形状判断。

## 本次任务：从什么得到什么

读取 H2O_optimized.xyz、masses.dat 和 9×9 hessian.dat，核对原子顺序和 Hartree/bohr² 单位，构造质量加权矩阵并求完整九个模式。将同一矩阵和质量交给 ASE VibrationsData，核对频率；用 stationary_guesses.dat 继续练习最低点与鞍点分类。

## 先用一个小例子走通思路

单个质量 m 接弹簧 k 时，$\omega=\sqrt{k/m}$；质量变为四倍，频率减半而势能曲线不变。多原子体系的质量加权正是这个关系的矩阵形式。

水有九个笛卡尔自由度，其中六个是整体平移/转动，余下三个是内部振动。真实有限精度矩阵中的六个零模可能略带正负号；把所有负号直接取绝对值，会同时掩盖真正不稳定的模式。

## 实现边界

| 自己写 | 直接用 | 手写后比对 |
|---|---|---|
| 力的中心差分、矩阵索引、质量加权、频率换算、最低点/鞍点判断 | PySCF 优化结构并计算解析 Hessian；ASE 读 XYZ；NumPy eigh | 将同一个 Hessian 与同一组质量交给 ASE VibrationsData，核对频率 |

不要求重新实现 PySCF 的解析二阶电子响应。它提供真实矩阵，供你验证自己的后处理；Morse/Müller–Brown 的力差分则检验二阶导数构造。

## 输入及坐标顺序

- [H2O_optimized.xyz](input/H2O_optimized.xyz)：RHF/STO-3G 优化后的 Cartesian 坐标，单位 Å。
- [hessian.dat](input/hessian.dat)：9×9 实矩阵，单位 Hartree/bohr²。
- [masses.dat](input/masses.dat)：三个原子的质量，单位 u，顺序必须与 XYZ 相同。
- [stationary_guesses.dat](input/stationary_guesses.dat)：二维势的最低点和鞍点初猜，用于独立的驻点分类练习。

矩阵索引的顺序是 $(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)$。PySCF 原始 Hessian 的维度是 `(atom, atom, Cartesian, Cartesian)`，不能直接 `reshape(9,9)`。应先变成 `(atom, Cartesian, atom, Cartesian)` 再 reshape。见 [提示 1](hints/hint1.md)。

## 第一步：从能量展开得到 Hessian

在驻点 $\mathbf R_0$ 附近，令位移为 $\mathbf u$：

```math
E(\mathbf R_0+\mathbf u)=E_0+
\underbrace{\nabla E_0^T\mathbf u}_{\text{驻点处为零}}+
\frac12\mathbf u^TH\mathbf u+O(u^3),
\qquad H_{ij}=\frac{\partial^2E}{\partial R_i\partial R_j}.
```

若有力接口 $F_i=-\partial E/\partial R_i$，用

```math
H_{ij}\approx-\frac{F_i(\mathbf R+h\mathbf e_j)-F_i(\mathbf R-h\mathbf e_j)}{2h}.
```

注意负号：最小值附近的恢复力导数为负，而势能曲率为正。对 Morse 最低点有解析结果 $H=2Da^2$，可检查符号与差分误差。

## 第二步：由运动方程导出质量加权

线性化运动满足

```math
M\ddot{\mathbf u}=-H\mathbf u.
```

设 $\mathbf u=\mathbf a e^{i\omega t}$，得到广义本征问题 $H\mathbf a=\omega^2M\mathbf a$。令 $\mathbf q=M^{1/2}\mathbf a$：

```math
\widetilde H=M^{-1/2}HM^{-1/2},\qquad
\widetilde H\mathbf q=\omega^2\mathbf q.
```

因此每个矩阵元除以 $\sqrt{m_im_j}$。每个**原子**的质量应重复三次，而不是循环重复整段质量列表。对角化后，质量加权向量 q 与真实位移 a 不同：$\mathbf a=M^{-1/2}\mathbf q$。见 [提示 2](hints/hint2.md)。

## 第三步：把本征值转换为 cm⁻¹

先把输入的 Hartree/bohr² 转成 eV/Å²。若本征值 $\lambda$ 的数值单位是 eV/(Å²·u)，则

```math
\omega=\sqrt{\lambda\frac{1.602176634\times10^{-19}\ \mathrm{J/eV}}
{10^{-20}\ \mathrm{m^2/\mathring A^2}\;1.66053906660\times10^{-27}\ \mathrm{kg/u}}},
\qquad\widetilde\nu=\frac{\omega}{2\pi c}.
```

$c$ 使用 cm/s 时，$\widetilde\nu$ 就是 cm⁻¹。少了 $2\pi$，得到的是把角频率误作普通频率的错误答案。质量整体乘 4 时，频率应减半，这是独立于软件的检查。

## 第四步：理解零模与负模

孤立非线性分子有 3 个整体平移与 3 个整体转动自由度，因此有 $3N-6$ 个内部振动；线性分子只有两个独立整体转动，所以是 $3N-5$。

- $\lambda\gt 0$：局部恢复力，对应实振动。
- $\lambda\lt 0$：沿该方向能量下降，对应虚频。
- $\lambda\approx0$：可能是刚体运动，也可能是非常软的内部运动，必须检查本征向量。

有限精度、未充分优化的几何和离散导数会让零模略偏离零。本项目报告完整谱，不把小负数全部取绝对值，也不按“最小六个”盲目删掉真实不稳定方向。见 [提示 3](hints/hint3.md)。

## 第五步：与 ASE 对照

把**同一** eV/Å² Hessian、同一原子顺序、同一组质量传给 `VibrationsData.from_2d(atoms, H)`。ASE 独立完成质量加权和频率换算。比较模式频率；若存在简并，不逐列要求本征向量相同，而应比较它们张成的子空间。

这项比较验证后处理。它不能证明 RHF/STO-3G 的势能面足够准确，更不能把计算频率称为实验基准。验证 PySCF 二阶导数本身需要另一套力差分实验。

## 运行与输出

```bash
# 已提供坐标和 Hessian；改结构或电子方法后重新生成：
sbatch scripts/slurm.sh 05_kinetics/03_hessian/prepare_hessian.py
sbatch scripts/slurm.sh 05_kinetics/03_hessian/run.py
```

从 [report.txt](output/report.txt) 对照完整谱；[normal_modes.csv](output/normal_modes.csv) 同列给出手写与 ASE 结果；`mass_weighted_hessian.dat` 可检查每个元素；`eigenvectors.dat` 的每一列是一个质量加权模式。

## 受控修改与物理判断

1. 只把两个 H 的质量替换为 D 的质量，Hessian 不变。哪些频率下降最多？为什么这叫 Born–Oppenheimer 势能面上的同位素效应？
2. 交换 XYZ 中两个不同元素的位置顺序，却不交换 Hessian 的对应块，会出现怎样的“数值正常、物理错误”？
3. 在二维鞍点找出唯一负模，沿 $\pm\epsilon\mathbf q$ 分别移动并计算能量，确认两侧下降。这个方向是否连向你预期的两个盆地？
4. 若分子尚有明显残余力，为什么“有六个零模”的理想计数可能失真？

资料：[ASE vibrations](https://ase-lib.org/ase/vibrations/vibrations.html)、[PySCF Hessian 模块](https://pyscf.org/pyscf_api_docs/pyscf.hessian.html)。本项目的“坐标→矩阵→质量加权→频率”步骤参考 ProgrammingProjects 的振动分析组织方式。

## 完成后应能解释什么

先检查 mass_weighted_hessian.dat 的质量和坐标索引，再读 normal_modes.csv 的全谱与 ASE 差值，最后查看本征向量。完成后应能解释三个内部模式与六个近零模式的来源，并提出区分刚体误差和真实负曲率的检查。

## 与前后项目的关系

联系 [优化](../01_optimizer/README.md) 的驻点和 [动力学](../02_dynamics/README.md) 的振动；结果可送入 [分子热化学](../../04_thermodynamics/02_molecular_thermochemistry/README.md)，也用于 [NEB](../04_neb/README.md) 候选过渡态检验。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
