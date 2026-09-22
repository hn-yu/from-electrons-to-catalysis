# 提示 2：稳定计算与物理零点

可减去最小能量再求指数，最后把零点加回 F 和 U。更一般地使用

```python
logw = np.log(g) - E / kBT
logZ = logsumexp(logw)
p = np.exp(logw - logZ)
```

熵可以由 $(U-F)/T$ 得到，也可由 $-k_B\sum_i p_i\ln(p_i/g_i)$ 核对。后式中的 $g_i$ 不能遗漏。
