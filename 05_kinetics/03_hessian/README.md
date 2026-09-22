# 从 Cartesian Hessian 到正常振动：曲率、质量和虚频

一个优化器返回“受力很小”，只能说明势能一阶导数接近零。最低点、过渡态和高阶鞍点都可能满足这个条件。区分它们需要二阶导数；把曲率转换为振动频率还需要质量与单位。

本项目从真实 H₂O 坐标和 Cartesian Hessian 出发。你将得到 9 个模式，辨认 3 个内部振动以及 6 个近零的整体平移/转动模式，并与 ASE 的独立分析核对。

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

$$
E(\mathbf R_0+\mathbf u)=E_0+
\underbrace{\nabla E_0^T\mathbf u}_{\text{驻点处为零}}+
\frac12\mathbf u^TH\mathbf u+O(u^3),
\qquad H_{ij}=\frac{\partial^2E}{\partial R_i\partial R_j}.
$$

若有力接口 $F_i=-\partial E/\partial R_i$，用

$$
H_{ij}\approx-\frac{F_i(\mathbf R+h\mathbf e_j)-F_i(\mathbf R-h\mathbf e_j)}{2h}.
$$

注意负号：最小值附近的恢复力导数为负，而势能曲率为正。对 Morse 最低点有解析结果 $H=2Da^2$，可检查符号与差分误差。

## 第二步：由运动方程导出质量加权

线性化运动满足

$$
M\ddot{\mathbf u}=-H\mathbf u.
$$

设 $\mathbf u=\mathbf a e^{i\omega t}$，得到广义本征问题 $H\mathbf a=\omega^2M\mathbf a$。令 $\mathbf q=M^{1/2}\mathbf a$：

$$
\widetilde H=M^{-1/2}HM^{-1/2},\qquad
\widetilde H\mathbf q=\omega^2\mathbf q.
$$

因此每个矩阵元除以 $\sqrt{m_im_j}$。每个**原子**的质量应重复三次，而不是循环重复整段质量列表。对角化后，质量加权向量 q 与真实位移 a 不同：$\mathbf a=M^{-1/2}\mathbf q$。见 [提示 2](hints/hint2.md)。

## 第三步：把本征值转换为 cm⁻¹

先把输入的 Hartree/bohr² 转成 eV/Å²。若本征值 $\lambda$ 的数值单位是 eV/(Å²·u)，则

$$
\omega=\sqrt{\lambda\frac{1.602176634\times10^{-19}\ \mathrm{J/eV}}
{10^{-20}\ \mathrm{m^2/\mathring A^2}\;1.66053906660\times10^{-27}\ \mathrm{kg/u}}},
\qquad\widetilde\nu=\frac{\omega}{2\pi c}.
$$

$c$ 使用 cm/s 时，$\widetilde\nu$ 就是 cm⁻¹。少了 $2\pi$，得到的是把角频率误作普通频率的错误答案。质量整体乘 4 时，频率应减半，这是独立于软件的检查。

## 第四步：理解零模与负模

孤立非线性分子有 3 个整体平移与 3 个整体转动自由度，因此有 $3N-6$ 个内部振动；线性分子只有两个独立整体转动，所以是 $3N-5$。

- $\lambda>0$：局部恢复力，对应实振动。
- $\lambda<0$：沿该方向能量下降，对应虚频。
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
