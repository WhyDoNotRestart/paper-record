# 材料使用合同

## 1. 状态枚举

```text
core-argument  method  result  limitation  background
reproduction  context-only  unused-with-reason  unavailable  needs-review
```

## 2. 最小关系

```text
Material → Evidence → Claim → Matrix field → Note/Report
```

每个材料对象必须有：唯一ID、相对路径、来源/版本、获取日期、hash（适用时）、使用状态、实际消费者、Evidence或原因。

## 3. 图表、公式、数据、代码

- 图表：图号/表号、页码、图注、变量、条件、比较对象、关键观察、支持Claim、矩阵字段、不能推出项、图片和证据卡路径；
- 公式：符号、假设、本文作用、与方法/证明的关系、公式失效后果；
- 数据：来源、版本、规模、时间、划分、预处理、许可、泄漏风险、支撑结论；
- 代码：仓库/commit、依赖、硬件、运行命令、输出、许可和无法复现部分；
- 参考文献：按 occurrence 标记理论、方法、数据、基线、相关工作、背景、仅出现、冲突/待核验。

保存但未进入论证的材料必须写 `context-only` 或 `unused-with-reason` 和原因，不能计为已使用。
