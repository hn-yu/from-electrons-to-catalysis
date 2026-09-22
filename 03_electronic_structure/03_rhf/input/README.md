# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

## [H2/eri.dat](H2/eri.dat)

1-based 唯一非零双电子积分：i j k l (ij|kl)，Hartree，八重对称恢复，未列项为零。

## [H2/molecule.xyz](H2/molecule.xyz)

核坐标，Å；电荷、自旋、基组见 cases.csv。

## [H2/pyscf_reference.dat](H2/pyscf_reference.dat)

独立 PySCF RHF 总能量，Hartree。改变坐标或基组后需重新生成。

## [H2/s.dat](H2/s.dat)

1-based 下三角 AO overlap：i j Sij，无量纲。

## [H2/system.dat](H2/system.dat)

nAO、电子数、核排斥能 Hartree，第一行三个数。

## [H2/t.dat](H2/t.dat)

1-based 下三角动能积分：i j Tij，Hartree。

## [H2/v.dat](H2/v.dat)

1-based 下三角电子—核吸引积分：i j Vij，Hartree。

## [H2O/eri.dat](H2O/eri.dat)

1-based 唯一非零双电子积分：i j k l (ij|kl)，Hartree，八重对称恢复，未列项为零。

## [H2O/molecule.xyz](H2O/molecule.xyz)

核坐标，Å；电荷、自旋、基组见 cases.csv。

## [H2O/pyscf_reference.dat](H2O/pyscf_reference.dat)

独立 PySCF RHF 总能量，Hartree。改变坐标或基组后需重新生成。

## [H2O/s.dat](H2O/s.dat)

1-based 下三角 AO overlap：i j Sij，无量纲。

## [H2O/system.dat](H2O/system.dat)

nAO、电子数、核排斥能 Hartree，第一行三个数。

## [H2O/t.dat](H2O/t.dat)

1-based 下三角动能积分：i j Tij，Hartree。

## [H2O/v.dat](H2O/v.dat)

1-based 下三角电子—核吸引积分：i j Vij，Hartree。

## [HeHplus/eri.dat](HeHplus/eri.dat)

1-based 唯一非零双电子积分：i j k l (ij|kl)，Hartree，八重对称恢复，未列项为零。

## [HeHplus/molecule.xyz](HeHplus/molecule.xyz)

核坐标，Å；电荷、自旋、基组见 cases.csv。

## [HeHplus/pyscf_reference.dat](HeHplus/pyscf_reference.dat)

独立 PySCF RHF 总能量，Hartree。改变坐标或基组后需重新生成。

## [HeHplus/s.dat](HeHplus/s.dat)

1-based 下三角 AO overlap：i j Sij，无量纲。

## [HeHplus/system.dat](HeHplus/system.dat)

nAO、电子数、核排斥能 Hartree，第一行三个数。

## [HeHplus/t.dat](HeHplus/t.dat)

1-based 下三角动能积分：i j Tij，Hartree。

## [HeHplus/v.dat](HeHplus/v.dat)

1-based 下三角电子—核吸引积分：i j Vij，Hartree。

## [LiH/eri.dat](LiH/eri.dat)

1-based 唯一非零双电子积分：i j k l (ij|kl)，Hartree，八重对称恢复，未列项为零。

## [LiH/molecule.xyz](LiH/molecule.xyz)

核坐标，Å；电荷、自旋、基组见 cases.csv。

## [LiH/pyscf_reference.dat](LiH/pyscf_reference.dat)

独立 PySCF RHF 总能量，Hartree。改变坐标或基组后需重新生成。

## [LiH/s.dat](LiH/s.dat)

1-based 下三角 AO overlap：i j Sij，无量纲。

## [LiH/system.dat](LiH/system.dat)

nAO、电子数、核排斥能 Hartree，第一行三个数。

## [LiH/t.dat](LiH/t.dat)

1-based 下三角动能积分：i j Tij，Hartree。

## [LiH/v.dat](LiH/v.dat)

1-based 下三角电子—核吸引积分：i j Vij，Hartree。

## [cases.csv](cases.csv)

逐案例目录及模型身份；结构文件必须与该行的设置、覆盖度/电荷对应。

```csv
case,geometry,basis,charge,spin
H2,H2/molecule.xyz,sto-3g,0,0
HeH+,HeHplus/molecule.xyz,sto-3g,1,0
```

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

修改 XYZ 后先运行 prepare_integrals.py，再运行 compare.py。run.py 的学生算法从文本积分求解；compare.py 会检查这些积分确实属于对应 XYZ。
