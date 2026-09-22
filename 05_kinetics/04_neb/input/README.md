# 输入说明

本项目在两个已知稳定状态之间寻找最低能量路径，手写 NEB 的切线和力投影，并与 ASE 的路径优化比较。

## 这些输入用于哪项任务

先优化 endpoints.dat 的二维 Müller–Brown 端点，手写插值、切线、力投影和松弛，随后用 ASE NEB/FIRE 处理同一问题。原子扩展读取 fcc/hcp EXTXYZ，由 ASE 与 EMT 完成 Cu/H 路径，学习实际结构和约束如何进入流程。

## 阅读文件前先核对一个具体例子

若仅对每个中间 image 使用普通真实力，所有点都会趋向两端或中间的局部极小值，山口附近反而可能没有点。弹簧维持间距，但它的垂直分量又会把弯曲通道拉成捷径，所以需要投影。

当前二维模型势垒约 1.056 eV，而原子 EMT 流程示例约 0.0095 eV。它们来自不同势函数和坐标定义，不能把后者当成真实 H/Cu 的 DFT 扩散势垒。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [endpoints.dat](endpoints.dat)

两行 x y，二维 NEB 起止初猜；先分别优化。

## [fcc.extxyz](fcc.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

## [hcp.extxyz](hcp.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
