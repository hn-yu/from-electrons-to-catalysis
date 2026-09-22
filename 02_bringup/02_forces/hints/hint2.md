# 提示 2：把标量力还原成笛卡尔力

链式法则给出 $\partial r/\partial\mathbf R_2=\hat{\mathbf r}_{12}$。

```python
direction = (positions[1] - positions[0]) / r
forces[1] = radial_force * direction
forces[0] = -forces[1]
```

检查 $\sum_i\mathbf F_i=0$。交换原子顺序不改变能量，但会交换两行力。若计算 $r=0$，方向没有定义，应当明确拒绝重叠原子。
