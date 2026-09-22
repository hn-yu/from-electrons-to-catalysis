# 提示 3：接口契约包含单位

能量是总能还是每原子能？力是 eV/Å 还是 Hartree/bohr？受约束分量是否被清零？

这三项都不由 Python 数组形状保证。

把它们写在 input/README、输出列名和 Calculator 边界处，比在发生错误后猜测转换因子更可靠。
