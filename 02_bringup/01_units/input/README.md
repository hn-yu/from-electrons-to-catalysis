# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [conversions.csv](conversions.csv)

逗号分隔表；第一行为字段与单位，数值不可脱离列名解释。

```csv
value,from_unit,to_unit
1,eV,kJ/mol
1,Hartree,eV
```

## [temperatures.csv](temperatures.csv)

逗号分隔表；第一行为字段与单位，数值不可脱离列名解释。

```csv
T_K
300
600
```
