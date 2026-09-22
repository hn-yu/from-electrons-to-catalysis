# 05 · 同一有限基组里的 HF、DFT 与 FCI

“哪个方法的能量最低”与“哪个方法更准确”为什么不是同一个问题？用最小的 H₂ 拉伸问题检验这种直觉。

## 实现边界

**直接用 PySCF** 的 RKS、积分网格与 FCI；不手写交换关联泛函、PAW 或生产级积分。**手写**统一几何与基组的比较、误差定义和近似解释。FCI 是有限基组基准，不是完备基组实验真值。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [H2_0.74.xyz](input/H2_0.74.xyz)
- [H2_2.50.xyz](input/H2_2.50.xyz)
- [O2.xyz](input/O2.xyz)
- [control.toml](input/control.toml)
- [geometries.csv](input/geometries.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


每帧 XYZ 分别求 HF、LDA/VWN、PBE、B3LYP 和 FCI。RKS 固定为闭壳层自旋限制形式，基组与坐标相同。

$$E_{\rm KS}[n]=T_s[n]+\int v_{\rm ext}n\,d\mathbf r+E_H[n]+E_{xc}[n]+E_{NN}.$$

$T_s$ 为非相互作用动能，$E_H$ 是经典电子库仑能；所有遗漏的交换和关联近似进入 $E_{xc}$。不同泛函不满足相互之间的变分排序。

同一基组 Hamiltonian 的全组态相互作用满足

$$E_{\rm FCI}\le E_{\rm HF},\qquad E_c^{\rm basis}=E_{\rm FCI}-E_{\rm HF}.$$

DFT 近似能量偶尔低于 FCI 并不违反 FCI 对其自身 Hamiltonian 的变分界，因为两者能量泛函不同。


## 从公式到程序

1. 从 geometries.csv 读 XYZ；对所有方法使用同一套输入坐标和 basis。
2. 保存每个 SCF 的收敛状态，DFT 网格 level=3，输出结果 CSV。
3. 逐帧计算 HF−FCI 和 DFT−FCI；另画相对最低点的势能曲线，区分绝对能量偏移与曲线形状。
4. 解释为什么简单提高 DFT 网格密度不能修复限制自旋解离的静态关联问题。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 03_electronic_structure/05_dft/run.py --output runs/05_dft
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 先提高积分网格，再更换泛函，两次实验分别讨论数值误差与模型误差。
- 拉伸时检查曲线形状，不能只根据平衡键长附近一个点给所有方法排名。
- 改用更大基组之前估计 FCI 行列式数：组合数增长解释了为什么真实表面不能照搬这个求解器。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[PySCF DFT](https://pyscf.org/user/dft.html) 与 [FCI](https://pyscf.org/user/ci.html)。
