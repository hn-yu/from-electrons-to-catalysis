# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

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
