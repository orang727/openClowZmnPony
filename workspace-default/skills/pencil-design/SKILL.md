---
name: pencil-design
description: AI 设计工具。使用 Pencil MCP 生成 UI 设计、页面原型、组件设计。当用户提到设计、UI、原型、画图、界面等需求时使用此技能。
---

# Pencil Design 技能

通过 mcporter CLI 调用 Pencil.dev MCP Server 进行 AI 驱动的 UI/UX 设计。

## 调用方式

所有 Pencil 工具通过 `mcporter call pencil.<工具名>` 调用：

```bash
mcporter call pencil.<tool_name> key:value key2:value2
```

JSON 参数使用 `--args`：
```bash
mcporter call pencil.<tool_name> --args '{"key": "value"}'
```

## 可用工具（14 个）

### 1. get_editor_state - 获取编辑器状态（每次任务开始时先调用）
```bash
mcporter call pencil.get_editor_state include_schema:false
```

### 2. open_document - 打开或新建设计文件
```bash
mcporter call pencil.open_document filePathOrNew:new
mcporter call pencil.open_document filePathOrNew:/path/to/file.pen
```

### 3. get_guidelines - 获取设计规范
可用 topic: code / table / tailwind / landing-page / slides / design-system / mobile-app / web-app
```bash
mcporter call pencil.get_guidelines topic:web-app
mcporter call pencil.get_guidelines topic:mobile-app
```

### 4. get_style_guide_tags - 获取所有风格标签
```bash
mcporter call pencil.get_style_guide_tags
```

### 5. get_style_guide - 根据标签获取风格指南
```bash
mcporter call pencil.get_style_guide --args '{"tags": ["modern", "minimal", "webapp"]}'
```

### 6. batch_design - 执行设计操作（核心工具，每次最多 25 个操作）
```bash
mcporter call pencil.batch_design --args '{"filePath": "new", "operations": "screen=I(\"document\", {\"type\": \"frame\", \"name\": \"Login Page\", \"width\": 1440, \"height\": 900, \"fill\": \"#FFFFFF\"})"}'
```

操作语法：
- `foo=I("parent", { ... })` — 插入节点
- `baz=C("nodeid", "parent", {...})` — 复制节点
- `foo2=R("nodeid1/nodeid2", {...})` — 替换节点
- `U(foo+"/nodeid", {...})` — 更新节点
- `D("nodeid")` — 删除节点
- `M("nodeid", "parent", 2)` — 移动节点
- `G("nodeid", "ai", "描述")` — AI 生成图片
- `G("nodeid", "stock", "关键词")` — Unsplash 图片

### 7. batch_get - 读取设计文件内容
```bash
mcporter call pencil.batch_get --args '{"filePath": "designs/page.pen"}'
mcporter call pencil.batch_get --args '{"filePath": "designs/page.pen", "patterns": [{"reusable": true}], "readDepth": 2}'
```

### 8. get_screenshot - 截图验证设计效果
```bash
mcporter call pencil.get_screenshot --args '{"filePath": "designs/page.pen", "nodeId": "nodeId123"}'
```

### 9. get_variables / set_variables - 管理变量和主题
### 10. snapshot_layout - 检查布局结构
### 11. find_empty_space_on_canvas - 查找画布空白区域
### 12. search_all_unique_properties - 搜索节点属性
### 13. replace_all_matching_properties - 批量替换属性

## 设计交互流程

1. `mcporter call pencil.get_editor_state include_schema:false` — 了解当前状态
2. `mcporter call pencil.open_document filePathOrNew:new` — 如无打开文件则新建
3. `mcporter call pencil.get_guidelines topic:web-app` — 获取设计规范
4. `mcporter call pencil.get_style_guide_tags` — 获取风格标签
5. `mcporter call pencil.get_style_guide --args '{"tags": [...]}'` — 选择风格
6. `mcporter call pencil.batch_design --args '{...}'` — 生成设计
7. `mcporter call pencil.get_screenshot --args '{...}'` — 截图验证，发送给用户
8. 根据用户反馈重复步骤 6-7 修改

## 前置条件

- Pencil.app 必须正在运行
- mcporter 已全局安装且配置了 pencil server（~/.mcporter/mcporter.json）
