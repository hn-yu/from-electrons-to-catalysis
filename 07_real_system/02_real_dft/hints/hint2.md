# 提示 2：原始日志与整理表各自负责什么

CSV 便于重新计算吸附能；GPAW txt 用来核对 SCF、电子展宽、基组设置和所采用的能量定义。

优化日志中的 force-consistent free energy 可能与 ASE 默认 extrapolated energy 不同。所有相减项必须统一约定。

修改电子展宽不是给吸附体系加了热力学熵，有限温自由能仍需要单独的振动与储库处理。
