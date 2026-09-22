# 04 · 把真实力与弹簧力放在正确方向

本项目在两个已知稳定状态之间寻找最低能量路径，手写 NEB 的切线和力投影，并与 ASE 的路径优化比较。

## 背景：为什么需要这一步

知道反应物和产物的最低能结构，并不知道它们之间要经过多高的山口。直线插值只是连接端点的初始猜测，可能穿过强排斥区。普通结构优化又会把中间点都拉向附近极小值，无法自动保留整条连接路径。

弹性带方法用一串构型副本（images）表示路径。NEB，即 nudged elastic band，通过投影让真实势能的力主要调整路径形状，让人工弹簧主要维持沿路径的间距。两种力的职责不同；如果混用方向，会导致拐角被弹簧拉直或 images 堆积到谷底。

最低能量路径 MEP 描述势能面上的几何通道。它不是一条带真实时间的动力学轨迹，也没有自动包含路径周围大量构型的熵。得到候选山口后，还需要 Hessian 和连接方向检查才能加强过渡态判断。

## 开始前需要理解的概念

- **端点**：已优化并在路径计算中固定的初态和终态。
- **image**：路径上一个完整构型的副本，不是单个原子或时间帧。
- **切线与垂直分量**：区分沿路径方向与改变路径形状的方向。
- **MEP**：最低能量路径，路径上的垂直真实力为零。
- **climbing image**：专门驱动最高能 image 靠近鞍点的改进，不等于任意一条路径的全局最优保证。

## 本次任务：从什么得到什么

先优化 endpoints.dat 的二维 Müller–Brown 端点，手写插值、切线、力投影和松弛，随后用 ASE NEB/FIRE 处理同一问题。原子扩展读取 fcc/hcp EXTXYZ，由 ASE 与 EMT 完成 Cu/H 路径，学习实际结构和约束如何进入流程。

## 先用一个小例子走通思路

若仅对每个中间 image 使用普通真实力，所有点都会趋向两端或中间的局部极小值，山口附近反而可能没有点。弹簧维持间距，但它的垂直分量又会把弯曲通道拉成捷径，所以需要投影。

当前二维模型势垒约 1.056 eV，而原子 EMT 流程示例约 0.0095 eV。它们来自不同势函数和坐标定义，不能把后者当成真实 H/Cu 的 DFT 扩散势垒。

## 实现边界

**手写后比对**二维势上的 NEB 切线、力投影和松弛，与 **ASE NEB/FIRE** 对照。原子扩展直接读 EXTXYZ 并用 ASE climbing-image NEB；示例 EMT 只演示流程，不能当作真实 H/Cu 扩散预测。

## 输入与物理模型

- [control.toml](input/control.toml)
- [endpoints.dat](input/endpoints.dat)
- [fcc.extxyz](input/fcc.extxyz)
- [hcp.extxyz](input/hcp.extxyz)

`endpoints.dat` 给出二维模型的两个初始点；先各自优化。`fcc.extxyz`、`hcp.extxyz` 给出 Cu/H 原子路径的两端，底层模型固定整个 Cu 衬底。

对于中间 image i，切线单位向量 $\hat\tau_i$ 沿当前路径。NEB 力为

```math
\mathbf F_i^{NEB}=\mathbf F_i-(\mathbf F_i\cdot\hat\tau_i)\hat\tau_i+k(|\mathbf R_{i+1}-\mathbf R_i|-|\mathbf R_i-\mathbf R_{i-1}|)\hat\tau_i.
```

第一项让路径在垂直方向靠近 MEP，第二项维持 image 间距。沿路径最高能 image 给出离散势垒；climbing image 则反转真实力的切向分量以靠近鞍点。

二维 Müller–Brown 势缩放为教学 eV，坐标不是 Å。原子部分的 Å/eV 则由 ASE 处理，二者不能混成同一个物理势垒。

## 从公式到程序

1. 优化端点并冻结；线性插值内部 image。
2. 依据局部能量排序构造改进切线；分别计算真力垂直分量和弹簧平行分量。
3. 自写 NEB 与 ASE 使用相同端点、image 数、弹簧与停止阈值，输出路径和势垒差。
4. 原子扩展直接读取 fcc/hcp EXTXYZ，先优化端点，再运行 ASE climbing-image NEB 并保存所有 image。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 05_kinetics/04_neb/run.py --output runs/04_neb
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 二维基准势垒约 1.056 eV，当前自写/ASE 差约 0.00032 eV。加倍 image 数，分开观察离散峰值误差与力收敛误差。
- 若错误地保留真实力的切向分量，images 会往极小值聚集；画 image 间距比看一个势垒数更容易诊断。
- 原子 EMT 示例势垒约 0.0095 eV。解释为什么这个数不能用于发表 H/Cu 的实际扩散率。
- 用 Hessian 验证候选鞍点是否恰有一个相关负曲率方向；NEB 收敛本身不是完整过渡态验证。

## 分步提示与资料

[ASE NEB](https://ase-lib.org/ase/neb.html)。

## 完成后应能解释什么

把路径坐标、image 间距、NEB 残余力和能量剖面一起读，再比较手写与 ASE 的势垒。完成后应能解释三种误差：路径尚未松弛、images 太稀、底层势能模型不适用。

## 与前后项目的关系

前置是 [优化](../01_optimizer/README.md) 与 [Hessian](../03_hessian/README.md)；[TST](../05_tst/README.md) 把指定自由能势垒转为时间尺度，[MEP 与自由能](../../06_catalysis/04_mep_fes/README.md) 解释还缺少的熵。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
