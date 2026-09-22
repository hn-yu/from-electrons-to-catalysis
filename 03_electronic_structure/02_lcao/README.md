# 02 · 非正交基组中的本征问题

同一个矩阵为什么在非正交基中不能直接当作普通 Hamiltonian 对角化？本项目为下一步 AO 基组 SCF 建立代数基础。

## 实现边界

**手写后比对**对称正交化、变换与残差；NumPy 提供普通对称本征求解器；SciPy `eigh(H,S)` 走独立广义本征路径。不要手写通用本征算法。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [control.toml](input/control.toml)
- [hamiltonian.dat](input/hamiltonian.dat)
- [overlap.dat](input/overlap.dat)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


`hamiltonian.dat` 为 Hartree，`overlap.dat` 无量纲，均是完整方阵。基函数重叠 $S_{\mu\nu}=\langle\chi_\mu|\chi_\nu\rangle$。

$$Hc=\varepsilon Sc,\quad c^TSc=1.$$

对称正交化为

$$S=UsU^T,\quad X=Us^{-1/2}U^T,\quad X^TSX=I,$$
$$H'=X^THX,\quad H'c'=\varepsilon c',\quad c=Xc'.$$

Rayleigh 商是 $c^THc/(c^TSc)$，不是 $c^THc/(c^Tc)$。若 S 含极小本征值，$s^{-1/2}$ 会放大误差；这对应近线性相关的基函数。


## 从公式到程序

1. 检查 H、S 对称，S 正定，输出其最小本征值。
2. 构造 X 并输出 XᵀSX；在正交基中对角化 H′ 后变换回原 AO 基。
3. 同时运行 SciPy 的广义求解器，比较能量及 `H C - S C diag(e)` 残差。
4. 保存 X、C 和 CᵀSC 三个矩阵，使下一项目可以逐项核对。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 03_electronic_structure/02_lcao/run.py --output runs/02_lcao
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 把 S 错当单位矩阵，定量比较能量变化；矩阵形状不报错不表示物理正确。
- 逐渐使两个基函数接近线性相关，观察 X 的元素和残差。
- 对基函数做可逆线性组合，同时变换 H 和 S。能级应保持不变，系数会变。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[SciPy 广义对称本征问题](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh.html)。
