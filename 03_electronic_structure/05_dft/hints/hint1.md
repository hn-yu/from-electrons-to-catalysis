# 提示 1：统一比较对象

FCI 通常在 HF 轨道上构造 Hamiltonian，但允许占据同一有限空间中的全部相关行列式。

```python
hf = scf.RHF(mol).run()
e_fci = fci.FCI(hf).kernel()[0]
```

这里的电子数、核坐标、基组和核排斥能必须与 HF 完全相同。不同 basis 的 FCI 不能作为当前 basis 算法的逐位核对。
