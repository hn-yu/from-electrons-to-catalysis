# 01 · 从势能表组装薛定谔算符

能级是边界条件、离散化和物理势共同决定的。你需要分清网格误差与有限计算盒误差，而不只是获得几个本征值。

## 实现边界

**手写**二阶导数离散、Hamiltonian 组装、归一化和收敛实验；**直接用 SciPy** 对称三对角本征求解器；**比对解析解**无限深方势阱与谐振子。数值线性代数不是本项目要重新实现的目标。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [box.dat](input/box.dat)
- [control.toml](input/control.toml)
- [double_well.dat](input/double_well.dat)
- [finite_well.dat](input/finite_well.dat)
- [harmonic.dat](input/harmonic.dat)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


四个 DAT 文件每行是 `x_bohr V_Hartree`，给出均匀内部网格。两端外侧各一个步长处施加 $\psi=0$。

原子单位下 $\hbar=m_e=1$：

$$-\frac12\psi''(x)+V(x)\psi(x)=E\psi(x),$$
$$H_{ii}=\frac1{h^2}+V_i,\qquad H_{i,i\pm1}=-\frac1{2h^2}.$$

求解器返回的向量满足 $\sum_i|c_i|^2=1$；连续概率要求 $h\sum_i|\psi_i|^2=1$，所以 $\psi_i=c_i/\sqrt h$。

盒长为 $L=(n+1)h$。无限深阱解析能级 $E_j=j^2\pi^2/(2L^2)$；$V=x^2/2$ 的无限域谐振子 $E_j=j+1/2$。


## 从公式到程序

1. 读 x 与 V，检验网格均匀。DAT 中的势是计算输入，改变文件必须改变 Hamiltonian。
2. 建立对角和次对角，交给 `eigh_tridiagonal`；只求所需低能态。
3. 输出波函数、归一化和解析误差。检查节点数是否随能级顺序增加。
4. 分别固定 L 加密网格、固定 h 扩大 L，解释两种收敛曲线。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 03_electronic_structure/01_schrodinger/run.py --output runs/01_schrodinger
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 将谐振子盒长减半，观察高激发态先受到边界影响。
- 对双阱逐渐提高中央势垒，预测最低两个态的能量劈裂变化；波函数奇偶性比仅看能量更有解释力。
- 有限阱里 E>0 的态仍被计算盒离散化，不能都叫“分子束缚态”。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[SciPy eigh_tridiagonal](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh_tridiagonal.html)。
