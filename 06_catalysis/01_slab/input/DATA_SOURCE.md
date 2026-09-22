# 已执行计算的数据来源

能量表从本仓库既有 `07_real_system/02_real_dft/output/result.json` 导出；原始完整记录保存在 output 的归档中。
这是既有 GPAW/PBE 计算的数据分析输入，不能把运行分析脚本说成重新做过 DFT。

`cases.csv` 的每一行对应独立的 slab、H2 和 slab+H 计算。
每个子目录的 POSCAR/EXTXYZ 是该配置的起始结构，`calculator.toml` 指定软件参数。
新计算关闭点群对称，旧数据部分保留了起始点群，故两者的松弛轨迹可能不同；需要重新比较最终结构。
能量来自 ASE 默认的 extrapolated energy；不能混用 force-consistent free energy。
