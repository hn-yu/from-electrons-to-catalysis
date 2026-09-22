# 01 · 先写计算备忘录，再申请资源

在申请一组 DFT 作业前，明确这笔计算将改变哪个判断。案例是高覆盖度 H/Cu(111) 的吸附符号。

## 这个项目应该自己完成什么

本项目要求**手写推理、量纲检查和可否定的判断**。引用前面计算项目的成熟软件结果；不把讨论题包装成返回 true/false 的脚本。必要算术可以使用 NumPy，电子结构、采样与动力学仍由对应项目的软件完成。

## 输入案例

- [calculator.toml](input/calculator.toml)
- [clean.POSCAR](input/clean.POSCAR)
- [fcc.POSCAR](input/fcc.POSCAR)


$$E_{ads}=E_{slab+H}-E_{slab}-\frac12E_{H_2},\qquad\theta_H=N_H/N_{surface\ sites}.$$

输入给出基准 clean/fcc POSCAR 与 calculator.toml。基准为 1×1×3，一个 H 即 1 ML。电子结构模型是中性、真空、PBE，不含溶剂、电位或有限温构型熵。


## 作业步骤

1. 按原子坐标核对层数、横向胞和覆盖度；列出固定原子。
2. 写一句可检验的问题、一个目标观测量、误差容限和最便宜的否定实验。
3. 分别列出数值误差与物理模型失效，不把软件设置清单当作研究问题。
4. 估算要算哪些独立参考，说明如何在 Slurm 分配资源与保存日志。

将回答写入自己的 `runs/01_calculation_memo/answer.md`，保留输入数据、公式、计算出的数值与结论范围。先完成回答，再查看 [参考分析](output/answer.md)。历史回答保存在 output/previous-answer.md；其中事前预测与事后测量不能互换身份。

## 提示

[逐步提示](hints/README.md) 给出三个具体推理环节。完整课程的 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md) 解释哪些工作应交给库。
