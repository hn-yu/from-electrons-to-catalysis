# 提示 1：先把电子结构算在驻点上

振动展开以驻点为中心。若梯度仍大，刚体旋转和内振动容易数值混合。

```python
gradient_hartree_per_angstrom = gradient_hartree_per_bohr / 0.529177210903
```

这里是除以 bohr 的 Å 长度，不是乘。检查最终最大梯度和内部频率，优化器给出一个坐标不代表已经收敛。
