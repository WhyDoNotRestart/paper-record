# 主张—证据—材料模型

## 三层对象

```text
Material：PDF、全文、图表、表格、公式、数据、代码、SI、参考文献
Evidence：材料中可定位的事实、观察、数字或限制
Claim：作者主张、结构化转述或本次综合推论
```

## 最小关系

```text
Material → Evidence → Claim → Matrix field → Report/Topic/Gap/Asset
```

## Claim记录

每条Claim必须有ID、owner（author / structured-restatement / synthesis）、文本、Evidence ID、定位、支持字段、置信度和边界。不能从Material直接跳到结论；不能把推论伪装成作者原话。

## Evidence强度

- `direct`：正文、图表、公式、附录或结论直接支持；
- `partial`：只支持表述的一部分；
- `contextual`：只提供背景；
- `conflicting`：材料之间存在冲突；
- `unverified`：当前无法核验。

图表数字必须保留条件和比较对象；低置信材料不能升级成高置信结论。
