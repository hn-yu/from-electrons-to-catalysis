# 提示 1：径向导数的负号

先对中间变量求导：$dz/dr=-az$。所以

$$\frac{dE}{dr}=2D(1-z)az.$$

力再加一个负号。$r>r_e$ 时 $0<z<1$，$F_r<0$，指向缩短键长。

```python
z = np.exp(-alpha * (r - re))
radial_force = -2 * depth * alpha * z * (1 - z)
```

用短键、平衡键和长键各一个点检查符号，不能只比较绝对值。
