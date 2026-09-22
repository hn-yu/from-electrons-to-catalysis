# 04 · 让 Hartree–Fock 暴露自己的近似

SCF 收敛只说明方程被求解了。拉伸 H₂、改变 O₂ 自旋和增加基函数，分别能揭露哪一种误差？

## 实现边界

本项目**直接用 PySCF RHF/UHF**。上一项目已经手写过 RHF，此处手写的是受控实验和物理诊断：能量差、自旋污染、基组与方法误差的拆分。不要再写一个不完整 UHF 当作成熟参考。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [H2_0.74.xyz](input/H2_0.74.xyz)
- [H2_1.50.xyz](input/H2_1.50.xyz)
- [H2_2.00.xyz](input/H2_2.00.xyz)
- [H2_3.00.xyz](input/H2_3.00.xyz)
- [H2_5.00.xyz](input/H2_5.00.xyz)
- [O2.xyz](input/O2.xyz)
- [control.toml](input/control.toml)
- [geometries.csv](input/geometries.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


`geometries.csv` 指向不同键长的 H₂ XYZ，键长重新从坐标读取；`O2.xyz` 是另一组自旋实验，不能混入 H₂ 拉伸曲线。

RHF 强制 $\phi_i^\alpha=\phi_i^\beta$；UHF 允许两套空间轨道独立变化。因此同一基组和电子数下，UHF 的变分空间包含 RHF。

$$E_{\rm UHF}\le E_{\rm RHF}\quad\text{（若找到相应最低驻点）}.$$

纯自旋态应满足 $\langle\hat S^2\rangle=S(S+1)$。解离极限的破缺对称 UHF H₂ 常得到约 1，而纯单重态应为 0；降低能量不等于恢复正确的自旋波函数。

PySCF 的 `spin` 是 $N_\alpha-N_\beta=2S$，不是多重度 $2S+1$。初始密度会决定是否保持或打破空间对称。


## 从公式到程序

1. 固定 STO-3G，对每个 H₂ 坐标同时运行 RHF 和破缺对称初猜的 UHF，保存能量、S²、收敛状态。
2. 对同一 O₂ 几何做 spin=0 和 spin=2 的 UHF；解释哪一个是三重态设置。
3. 固定第一帧 H₂ 几何，依次用控制文件指定的基组做 RHF。输出不同实验到不同 CSV。
4. 将“电子迭代失败”“错误驻点”“方法近似失效”分别举一个例子。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 03_electronic_structure/04_break_hf/run.py --output runs/04_break_hf
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 给拉伸 H₂ 的 UHF 使用对称初猜，观察它是否一直停在 RHF 型解；初猜不是无关紧要的技术细节。
- 在 3 Å 处比较 RHF/UHF 和 S²。解释为什么能量改善与自旋污染可以同时出现。
- 基组增大能改善变分能量，但不会自动加入缺失的多行列式关联。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[PySCF SCF 用户指南](https://pyscf.org/user/scf.html)。
