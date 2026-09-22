# 提示 1：归一化不要破坏原始位移

切线要归一化，但弹簧需要两侧真实间距。

```python
forward = path[i+1] - path[i]
backward = path[i] - path[i-1]
tangent = candidate.copy()
tangent /= np.linalg.norm(tangent)
```

若对与 forward 共用内存的数组原地归一化，会把弹簧的一侧长度错误变成 1。保留原始位移并单独构造切线。
