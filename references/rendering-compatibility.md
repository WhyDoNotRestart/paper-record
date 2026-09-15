# 链接与渲染兼容规范（Paper Record 3.1）

## 目标

同一批次必须在普通 Markdown、Obsidian 和独立 HTML 预览中打开。文件存在不代表可以展示；每个本地目标必须依次通过：

```text
路径可解析 → 文件存在 → 文件类型有效 → 内容可解码 → 预览实际加载
```

## 推荐写法

```markdown
![FIG-01 方法流程](../../04-证据仓/P001--2024--paper/figures/P001--FIG-01--method.png)
[打开图表证据卡](../../04-证据仓/P001--2024--paper/figures/P001--FIG-01--evidence.md)
[打开原始PDF](../../04-证据仓/P001--2024--paper/source/P001--2024--paper.pdf)
[[03-逐篇精读/P001--2024--paper/02-深度说理报告]]
```

## 目标类型检查

- 图片：检查 PNG/JPEG/GIF/WebP/BMP/TIFF 内容可解码，SVG 至少包含有效 `<svg>` 根节点，并记录宽高；
- PDF：检查 `%PDF-` 文件头、可解析页数和页数大于零；
- Markdown/HTML：检查目标是文件而不是目录；
- Obsidian wikilink：允许省略 `.md`，但必须解析到批次内真实文件；
- 外部 URL：不参与本地文件检查，但要保留来源和访问日期。

## 三种渲染模式

```text
python scripts/render_markdown_preview.py --renderer markdown ...
python scripts/render_markdown_preview.py --renderer obsidian ...
python scripts/render_markdown_preview.py --renderer html ...
```

`html` 模式生成可打开的独立预览并检查本地资源；`markdown` 和 `obsidian` 模式验证相应语法的本地解析结果。三种结果分别记录，不能互相替代。

## 图表双入口

每个图、表、公式必须同时提供：

1. 可直接显示或打开的原始材料；
2. 文字证据卡，说明图注、变量、条件、支持的 Claim、矩阵字段和不能推出的结论。

图片不可解码、PDF 不可打开或证据卡缺失时，相关 Evidence 不能进入 `completed`。

## 禁止

- 链接目录；
- 使用盘符或机器绝对路径；
- 只在 YAML 中保存不可点击路径；
- 图片只嵌证据卡而不提供可显示图片；
- 依赖错误工作目录的 HTML 相对路径；
- 用“文件存在”代替媒体格式和实际渲染验证；
- 未验证就生成 Zotero URI。

## 验收记录

链接审计结果必须记录：源文件、语法、目标、目标类型、解析后的相对路径、是否存在、是否为目录、格式是否有效、媒体尺寸/页数、渲染器和状态。图片必须有至少一套 HTML 预览记录；PDF 必须有解析页数记录。
