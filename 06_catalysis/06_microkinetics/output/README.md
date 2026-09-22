# 输出说明

本项目将基元反应速率与表面覆盖度耦合，求稳态周转频率，并解释温度和压力响应为什么不能仅由某个单步势垒判断。

## 应先读什么、回答什么

先核对覆盖度和为 1、各步净通量相等，再读温压扫描中的 TOF、反应级数和表观活化能。完成后应能用人口变化解释曲线，并区分初态影响的暂态与固定储库下的最终稳态。

## 用于理解这些结果的背景

一个反应步骤即使速率常数很大，也需要相应反应物真的存在。例如表面转化的事件率与 A* 覆盖度相乘；吸附则需要气体和空位同时存在。网络中每一步都在改变下一步可用的状态人口，所以必须一起求解。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [Cantera-coverages.dat](Cantera-coverages.dat)
- [Cantera-elementary_rates_s^-1.dat](Cantera-elementary_rates_s^-1.dat)
- [integration-coverages.csv](integration-coverages.csv)
- [integration-time_s.dat](integration-time_s.dat)
- [own_steady_state-coverages.dat](own_steady_state-coverages.dat)
- [own_steady_state-elementary_rates_s^-1.dat](own_steady_state-elementary_rates_s^-1.dat)
- [own_steady_state-forward_s^-1.dat](own_steady_state-forward_s^-1.dat)
- [own_steady_state-reverse_s^-1.dat](own_steady_state-reverse_s^-1.dat)
- [report.txt](report.txt)
- [response-degree_of_rate_control.dat](response-degree_of_rate_control.dat)
- [response-reaction_orders_A_B.dat](response-reaction_orders_A_B.dat)
- [steady_state-coverages.dat](steady_state-coverages.dat)
- [steady_state-elementary_rates_s^-1.dat](steady_state-elementary_rates_s^-1.dat)
- [steady_state-forward_s^-1.dat](steady_state-forward_s^-1.dat)
- [steady_state-reverse_s^-1.dat](steady_state-reverse_s^-1.dat)
- [sweep-0-coverages.dat](sweep-0-coverages.dat)
- [sweep-0-elementary_rates_s^-1.dat](sweep-0-elementary_rates_s^-1.dat)
- [sweep-0-forward_s^-1.dat](sweep-0-forward_s^-1.dat)
- [sweep-0-reverse_s^-1.dat](sweep-0-reverse_s^-1.dat)
- [sweep-1-coverages.dat](sweep-1-coverages.dat)
- [sweep-1-elementary_rates_s^-1.dat](sweep-1-elementary_rates_s^-1.dat)
- [sweep-1-forward_s^-1.dat](sweep-1-forward_s^-1.dat)
- [sweep-1-reverse_s^-1.dat](sweep-1-reverse_s^-1.dat)
- [sweep-10-coverages.dat](sweep-10-coverages.dat)
- [sweep-10-elementary_rates_s^-1.dat](sweep-10-elementary_rates_s^-1.dat)
- [sweep-10-forward_s^-1.dat](sweep-10-forward_s^-1.dat)
- [sweep-10-reverse_s^-1.dat](sweep-10-reverse_s^-1.dat)
- [sweep-11-coverages.dat](sweep-11-coverages.dat)
- [sweep-11-elementary_rates_s^-1.dat](sweep-11-elementary_rates_s^-1.dat)
- [sweep-11-forward_s^-1.dat](sweep-11-forward_s^-1.dat)
- [sweep-11-reverse_s^-1.dat](sweep-11-reverse_s^-1.dat)
- [sweep-12-coverages.dat](sweep-12-coverages.dat)
- [sweep-12-elementary_rates_s^-1.dat](sweep-12-elementary_rates_s^-1.dat)
- [sweep-12-forward_s^-1.dat](sweep-12-forward_s^-1.dat)
- [sweep-12-reverse_s^-1.dat](sweep-12-reverse_s^-1.dat)
- [sweep-13-coverages.dat](sweep-13-coverages.dat)
- [sweep-13-elementary_rates_s^-1.dat](sweep-13-elementary_rates_s^-1.dat)
- [sweep-13-forward_s^-1.dat](sweep-13-forward_s^-1.dat)
- [sweep-13-reverse_s^-1.dat](sweep-13-reverse_s^-1.dat)
- [sweep-14-coverages.dat](sweep-14-coverages.dat)
- [sweep-14-elementary_rates_s^-1.dat](sweep-14-elementary_rates_s^-1.dat)
- [sweep-14-forward_s^-1.dat](sweep-14-forward_s^-1.dat)
- [sweep-14-reverse_s^-1.dat](sweep-14-reverse_s^-1.dat)
- [sweep-15-coverages.dat](sweep-15-coverages.dat)
- [sweep-15-elementary_rates_s^-1.dat](sweep-15-elementary_rates_s^-1.dat)
- [sweep-15-forward_s^-1.dat](sweep-15-forward_s^-1.dat)
- [sweep-15-reverse_s^-1.dat](sweep-15-reverse_s^-1.dat)
- [sweep-2-coverages.dat](sweep-2-coverages.dat)
- [sweep-2-elementary_rates_s^-1.dat](sweep-2-elementary_rates_s^-1.dat)
- [sweep-2-forward_s^-1.dat](sweep-2-forward_s^-1.dat)
- [sweep-2-reverse_s^-1.dat](sweep-2-reverse_s^-1.dat)
- [sweep-3-coverages.dat](sweep-3-coverages.dat)
- [sweep-3-elementary_rates_s^-1.dat](sweep-3-elementary_rates_s^-1.dat)
- [sweep-3-forward_s^-1.dat](sweep-3-forward_s^-1.dat)
- [sweep-3-reverse_s^-1.dat](sweep-3-reverse_s^-1.dat)
- [sweep-4-coverages.dat](sweep-4-coverages.dat)
- [sweep-4-elementary_rates_s^-1.dat](sweep-4-elementary_rates_s^-1.dat)
- [sweep-4-forward_s^-1.dat](sweep-4-forward_s^-1.dat)
- [sweep-4-reverse_s^-1.dat](sweep-4-reverse_s^-1.dat)
- [sweep-5-coverages.dat](sweep-5-coverages.dat)
- [sweep-5-elementary_rates_s^-1.dat](sweep-5-elementary_rates_s^-1.dat)
- [sweep-5-forward_s^-1.dat](sweep-5-forward_s^-1.dat)
- [sweep-5-reverse_s^-1.dat](sweep-5-reverse_s^-1.dat)
- [sweep-6-coverages.dat](sweep-6-coverages.dat)
- [sweep-6-elementary_rates_s^-1.dat](sweep-6-elementary_rates_s^-1.dat)
- [sweep-6-forward_s^-1.dat](sweep-6-forward_s^-1.dat)
- [sweep-6-reverse_s^-1.dat](sweep-6-reverse_s^-1.dat)
- [sweep-7-coverages.dat](sweep-7-coverages.dat)
- [sweep-7-elementary_rates_s^-1.dat](sweep-7-elementary_rates_s^-1.dat)
- [sweep-7-forward_s^-1.dat](sweep-7-forward_s^-1.dat)
- [sweep-7-reverse_s^-1.dat](sweep-7-reverse_s^-1.dat)
- [sweep-8-coverages.dat](sweep-8-coverages.dat)
- [sweep-8-elementary_rates_s^-1.dat](sweep-8-elementary_rates_s^-1.dat)
- [sweep-8-forward_s^-1.dat](sweep-8-forward_s^-1.dat)
- [sweep-8-reverse_s^-1.dat](sweep-8-reverse_s^-1.dat)
- [sweep-9-coverages.dat](sweep-9-coverages.dat)
- [sweep-9-elementary_rates_s^-1.dat](sweep-9-elementary_rates_s^-1.dat)
- [sweep-9-forward_s^-1.dat](sweep-9-forward_s^-1.dat)
- [sweep-9-reverse_s^-1.dat](sweep-9-reverse_s^-1.dat)
- [sweep.csv](sweep.csv)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
