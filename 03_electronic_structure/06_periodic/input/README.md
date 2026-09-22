# 输入说明

本项目用周期 Al 晶体的能量—体积曲线提取平衡晶格常数和体模量，并检验数值设置是否足以支撑这些材料性质。

## 这些输入用于哪项任务

先读取真实 GPAW 计算留下的 eos.csv，按 scenario 分组，用 ASE EquationOfState 拟合并比较 a₀、B。然后检查 Al.cif 与 lattice_scan.csv 如何定义一个新的体积扫描。默认命令只分析已有数据；带 --calculate 才从当前 CIF 启动新的 GPAW 电子结构计算，应提交 Slurm。

## 阅读文件前先核对一个具体例子

FCC 常规晶胞含四个原子。若 $a=4$ Å，则每原子体积为 $a^3/4=16$ Å³；把 64 Å³ 与每原子能量配对，会直接破坏归一化。

已有 k=4、6、8 数据给出的 a₀ 约为 4.04768、4.04205、4.03817 Å。即使每条拟合曲线都很平滑，晶格常数仍随采样改变。体模量依赖二阶导数，因此还应单独检查其变化，不能从 a₀ 稳定推断 B 必然稳定。

## [Al.cif](Al.cif)

晶体 CIF，含晶胞、空间群与原子分数坐标，由 ASE 读取。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [eos.csv](eos.csv)

已执行 PBE 体积扫描，体积 Å³/atom、能量 eV/atom，按 scenario 分组拟合。

```csv
scenario,a_A,volume_A3_atom,energy_eV_atom
baseline,3.9,14.829749999999995,-3.6316234020775098
baseline,3.98,15.761198000000002,-3.677592775719872
```

## [lattice_scan.csv](lattice_scan.csv)

逗号分隔表；第一行为字段与单位，数值不可脱离列名解释。

```csv
a_A
3.8
3.9
```

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
