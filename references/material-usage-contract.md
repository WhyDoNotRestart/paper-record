# 材料使用合同（Paper Record 3.1）

## 1. 材料使用不是“保存路径”

材料只有在它进入 Evidence、Claim、矩阵字段或报告/主题解释时，才算被使用。单独登记路径不能证明用途。

```text
Material → Evidence → Claim → Matrix field → Note/Report → Topic/Opportunity
```

审计必须同时检查正向和反向关系：

```text
材料台账中的 ID → 文件、Evidence、Claim 和消费者真实存在
报告/矩阵/主题中的 ID → 能回溯到材料台账和真实文件
```

## 2. 状态枚举

```text
core-argument
method
result
limitation
background
reproduction
context-only
unused-with-reason
unavailable
needs-review
```

## 3. 每个材料对象必须有

- 唯一 `material_id`；
- 批次内相对路径；
- 材料类型、来源和版本；
- 获取日期和 hash（适用时）；
- `usage_status`；
- 实际消费者文件；
- Evidence、Claim 或明确未使用理由；
- 报告段落、主题段落或 occurrence 定位；
- `render_status`（适用时）。

## 4. 不同材料的最低证据要求

### 图表、表格和公式

记录图/表/公式编号、PDF页码、图注、变量、实验条件、比较对象、直接观察、支持 Claim、矩阵字段、不能推出项、图片路径和证据卡路径。

### 数据

记录来源、版本、规模、时间、划分、预处理、许可、泄漏风险、支撑的结果和复现消费者。

### 代码

记录仓库/commit、依赖、硬件、运行命令、输出、许可、无法复现部分和实际复现报告消费者。

### 参考文献

按 occurrence 标记理论、方法、数据、基线、相关工作、背景、仅出现、冲突或待核验。记录出现位置、引用角色、支持的 Claim 和进入的报告段落。

## 5. 受控未使用状态

保存但未进入论证的材料必须写：

```text
context-only
```

或：

```text
unused-with-reason
```

并填写原因。未获得的 PDF、补充材料、代码或数据使用：

```text
unavailable
```

同时记录缺失影响。以上状态不能被计入“核心证据已使用”。

## 6. 验收底线

- 100% 材料有受控状态；
- 所有 `core-argument`、`method`、`result`、`limitation` 材料都有消费者和证据链；
- 所有 Evidence/Claim ID 都能解析；
- 所有报告中的核心 ID 都能回链到材料台账；
- 关键图表、数据、代码和参考文献 occurrence 不得只有路径、没有用途；
- 不能为了达到“全部使用”而强行把背景材料改写成结论证据。
