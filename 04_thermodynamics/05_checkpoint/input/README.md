# 输入说明

本项目把电子能、振动和气体储库项整理成一份不会漏算或重复计数的反应自由能账本。

## 这些输入用于哪项任务

读取 thermochemistry.csv，为气相分子写 H/S/G 分项，再写吸附反应的 ΔG。用 600 K 的压力变化和 CO₂/H₂O 模式计数检查自己的账本，提交带公式、数值与近似范围的 answer.md。

## 阅读文件前先核对一个具体例子

如果使用 $\mu_{gas}=E_{gas}+ZPE_{gas}+\Delta H_{gas}-TS_{gas}$，则在吸附自由能中减去 μgas 时，气体 ZPE 已经被减去一次；再单独减 ZPEgas 会重复计数。

600 K 时压力提高十倍，单个理想气体粒子的 μ 增加约 0.11905 eV。反应消耗一个气体粒子时，反应自由能降低这个量；若反应产生两个，压力贡献则增加两倍这个量。

## 案例材料

- [questions.md](questions.md)
- [thermochemistry.csv](thermochemistry.csv)

先读 questions.md，再用其余材料支持自己的推理。正文的小例子帮助核对概念和量纲；自己的结论应引用具体数据或公式。

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
