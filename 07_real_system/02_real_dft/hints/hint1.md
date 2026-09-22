# 提示 1：原生输入应该足以重建计算

仅记录 cutoff 和 kpts 不够。还需要原子坐标、晶胞、元素、电子模型与约束。

本项目把这些分别写入 POSCAR/EXTXYZ 与 calculator.toml，cases.csv 建立对应关系。

打开一个 case，不依赖 Python 中硬编码的构造器，手动核对它能否代表所声称的层数与覆盖度。
