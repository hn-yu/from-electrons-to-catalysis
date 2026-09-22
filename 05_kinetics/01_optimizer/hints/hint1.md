# 提示 1：力的方向与梯度的方向

下降沿 $-\nabla E$，而物理力恰好就是 $-\nabla E$。

```python
trial = x + step * force
```

如果把 `jac=force` 传给 SciPy，优化器会把力误认为梯度；应传 `jac=lambda x: -potential.force(x)`。

一个符号错误可能在初始点刚好是极小值时隐藏，所以必须从非驻点开始验证。
