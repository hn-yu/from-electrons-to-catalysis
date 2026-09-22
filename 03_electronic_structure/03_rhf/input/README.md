# 输入说明

本项目为给定核坐标和有限基组求闭壳层分子的 Hartree–Fock 基态近似。你将自己完成电子密度与平均场相互决定的 SCF 循环，并从同一物理输入独立运行 PySCF 核对。

## 这些输入用于哪项任务

完成四个坐标明确的小案例：H₂、HeH⁺、LiH 和 H₂O。它们逐步增加不对称性、基函数数和占据轨道数，避免只在过于对称的 H₂ 上误以为循环已经正确。

实际数据流是“XYZ 与基组 → PySCF AO 积分 → 自写 X/D/J/K/F/能量迭代 → 矩阵和残差 → 独立 PySCF 比较”。默认 run.py 从附带积分开始；修改坐标后需先生成新积分。compare.py 专门检查坐标和积分仍然匹配。

## 阅读文件前先核对一个具体例子

H₂/STO-3G 有两个 AO、两个电子和一个双占据 MO，因此 S、h、D、F 都是 2×2，ERI 是 2×2×2×2。密度中占据贡献乘 2，电子数应满足 $\mathrm{Tr}(DS)=2$。

在高度对称的 H₂ 中，第一次猜测可能就接近最终轨道；这不能充分检验一般 SCF 的密度更新。水有七个 AO、十个电子，必须选五个占据 MO，因而更容易暴露占据、交换指标和迭代错误。下面的每一步都能在这些小矩阵中逐项核对。

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

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
