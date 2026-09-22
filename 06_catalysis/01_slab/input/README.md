# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

## [DATA_SOURCE.md](DATA_SOURCE.md)

模型、来源或输入约定说明。

## [baseline/H2.extxyz](baseline/H2.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

## [baseline/calculator.toml](baseline/calculator.toml)

GPAW/PBE backend、cutoff_eV、kpts、smearing_eV、fmax；长度 Å，力 eV/Å。

## [baseline/clean.POSCAR](baseline/clean.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [baseline/fcc.POSCAR](baseline/fcc.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [cases.csv](cases.csv)

逐案例目录及模型身份；结构文件必须与该行的设置、覆盖度/电荷对应。

```csv
scenario,parameter,value,directory,coverage_ML
baseline,baseline,baseline,baseline,1.0
cutoff_eV-0,cutoff_eV,300,cutoff_eV-0,1.0
```

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [cutoff_eV-0/H2.extxyz](cutoff_eV-0/H2.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

## [cutoff_eV-0/calculator.toml](cutoff_eV-0/calculator.toml)

GPAW/PBE backend、cutoff_eV、kpts、smearing_eV、fmax；长度 Å，力 eV/Å。

## [cutoff_eV-0/clean.POSCAR](cutoff_eV-0/clean.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [cutoff_eV-0/fcc.POSCAR](cutoff_eV-0/fcc.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [energies.csv](energies.csv)

已执行 PBE 总能量三元组；每行属于独立 scenario，eV。不可混用不同 scenario 的参考。

```csv
scenario,site,clean_eV,H2_eV,total_eV,force_max_eV_A,Hx_A,Hy_A,Hz_A
baseline,fcc,-9.357079982855794,-6.485204909265862,-12.554081054962252,0.045167236463648154,1.2766648181250455,0.7370808203183089,11.194583982585494
cutoff_eV-0,fcc,-9.684395505086954,-6.592309009364759,-12.927224393907512,0.02482551388360138,1.2763221862043155,0.7368827447860234,11.160829566241215
```

## [fixed_layers-0/H2.extxyz](fixed_layers-0/H2.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

## [fixed_layers-0/calculator.toml](fixed_layers-0/calculator.toml)

GPAW/PBE backend、cutoff_eV、kpts、smearing_eV、fmax；长度 Å，力 eV/Å。

## [fixed_layers-0/clean.POSCAR](fixed_layers-0/clean.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [fixed_layers-0/fcc.POSCAR](fixed_layers-0/fcc.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [kpts-0/H2.extxyz](kpts-0/H2.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

## [kpts-0/calculator.toml](kpts-0/calculator.toml)

GPAW/PBE backend、cutoff_eV、kpts、smearing_eV、fmax；长度 Å，力 eV/Å。

## [kpts-0/clean.POSCAR](kpts-0/clean.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [kpts-0/fcc.POSCAR](kpts-0/fcc.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [size-0/H2.extxyz](size-0/H2.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

## [size-0/calculator.toml](size-0/calculator.toml)

GPAW/PBE backend、cutoff_eV、kpts、smearing_eV、fmax；长度 Å，力 eV/Å。

## [size-0/clean.POSCAR](size-0/clean.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [size-0/fcc.POSCAR](size-0/fcc.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [size-1/H2.extxyz](size-1/H2.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

## [size-1/calculator.toml](size-1/calculator.toml)

GPAW/PBE backend、cutoff_eV、kpts、smearing_eV、fmax；长度 Å，力 eV/Å。

## [size-1/clean.POSCAR](size-1/clean.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [size-1/fcc.POSCAR](size-1/fcc.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [smearing_eV-0/H2.extxyz](smearing_eV-0/H2.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

## [smearing_eV-0/calculator.toml](smearing_eV-0/calculator.toml)

GPAW/PBE backend、cutoff_eV、kpts、smearing_eV、fmax；长度 Å，力 eV/Å。

## [smearing_eV-0/clean.POSCAR](smearing_eV-0/clean.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [smearing_eV-0/fcc.POSCAR](smearing_eV-0/fcc.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [vacuum_A-0/H2.extxyz](vacuum_A-0/H2.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

## [vacuum_A-0/calculator.toml](vacuum_A-0/calculator.toml)

GPAW/PBE backend、cutoff_eV、kpts、smearing_eV、fmax；长度 Å，力 eV/Å。

## [vacuum_A-0/clean.POSCAR](vacuum_A-0/clean.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [vacuum_A-0/fcc.POSCAR](vacuum_A-0/fcc.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。
