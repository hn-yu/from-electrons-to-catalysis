# 提示 1：Metropolis 接受的是总有偏能量

窗口 k 的接受概率为

$$a=\min\{1,\exp[-\beta((U'+W_k')-(U+W_k))]\}.$$

```python
if np.log(rng.random()) < -(new_energy-old_energy)/kBT:
    point = proposal
```

漏掉偏置的能量差却保留偏置重加权，会双重改变错误的分布。先对单窗口检查采样均值和方差。
