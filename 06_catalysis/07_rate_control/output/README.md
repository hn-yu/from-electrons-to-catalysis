# 输出说明

本项目通过单独扰动过渡态并重新求稳态，量化每一步对整体速率的控制程度，检验“最高局部势垒就是决速步”的直觉。

## 应先读什么、回答什么

并排读局部势垒、DRC、Cantera 差值与扰动步长结果，再看中间体扰动引起的覆盖度变化。完成后应能准确说出“保持了什么、改变了什么、重新求了什么”，并识别净 TOF 接近零时对数响应的局限。

## 用于理解这些结果的背景

局部势垒决定从某个状态出发有多快，但整体通量还取决于该状态有多少人口、逆反应多强，以及其他步骤如何补充或消耗它。因此只把势垒排成一列，通常不足以确定提升哪个步骤最能加快催化。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [Cantera-coverages.dat](Cantera-coverages.dat)
- [Cantera-elementary_rates_s^-1.dat](Cantera-elementary_rates_s^-1.dat)
- [Cantera_degree_of_rate_control.dat](Cantera_degree_of_rate_control.dat)
- [forward_barriers_eV.dat](forward_barriers_eV.dat)
- [own_steady_state-coverages.dat](own_steady_state-coverages.dat)
- [own_steady_state-elementary_rates_s^-1.dat](own_steady_state-elementary_rates_s^-1.dat)
- [own_steady_state-forward_s^-1.dat](own_steady_state-forward_s^-1.dat)
- [own_steady_state-reverse_s^-1.dat](own_steady_state-reverse_s^-1.dat)
- [perturbations.csv](perturbations.csv)
- [report.txt](report.txt)
- [response-degree_of_rate_control.dat](response-degree_of_rate_control.dat)
- [response-reaction_orders_A_B.dat](response-reaction_orders_A_B.dat)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
