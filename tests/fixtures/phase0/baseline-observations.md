# 阶段 0 基线失败复现

日期：2026-09-15  
分支：`codex/luban-paper-record-3.1`  
基线：`b7fc868`

## 复现命令与结果

### 1. 无效图片被误判为可用

```text
python scripts/check_links.py --root tests/fixtures/phase0/batch
```

结果：`passed=true`、`broken_count=0`。但 `04-证据仓/P001--2024--fixture/figures/invalid.png` 的内容是 `not-a-real-png`，不是可解码 PNG。

### 2. HTML 预览只检查路径，不检查媒体内容

```text
python scripts/render_markdown_preview.py --root tests/fixtures/phase0/batch --source 00-开始/entry.md --out tests/fixtures/phase0/batch/preview-before.html --report tests/fixtures/phase0/batch/preview-before.json
```

结果：`passed=true`、`broken_count=0`。同一份预览同时接受有效 PNG 和无效图片，说明当前渲染门禁无法证明图表实际可展示。

### 3. 材料使用审计无法识别最小 fixture 的材料关系

```text
python scripts/audit_material_usage.py --root tests/fixtures/phase0/batch
```

结果：`passed=false`、`material_count=0`，因为当前 fixture 没有材料台账；下一阶段需要让审计器区分“台账缺失”“材料未使用”“材料已使用但链路断裂”三种状态，而不是只给一个形式失败。

## 基线结论

当前门禁能够发现部分路径和目录错误，但不能证明图片/PDF真实可用，也不能证明材料实际进入 Claim、矩阵或主报告。阶段 1 和阶段 3 必须优先修复这两个静默失败面。
