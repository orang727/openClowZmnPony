---
name: cn-search
description: 国内网络搜索工具。当 web_search 不可用时，使用此技能通过百度/Bing 进行搜索。支持中英文搜索查询。
---

# 国内搜索技能

## 使用场景

当用户需要搜索网络信息，但 `web_search` 工具因网络原因不可用时，使用此技能。

## 使用方法

运行搜索脚本：

```bash
python ~/.openclaw/workspace/skills/cn-search/search.py "搜索关键词" [--engine baidu|bing] [--count 5]
```

### 参数

- `query`: 搜索关键词（必需）
- `--engine`: 搜索引擎，可选 `baidu`（默认）或 `bing`
- `--count`: 返回结果数量，默认 5

### 示例

```bash
# 使用百度搜索
python ~/.openclaw/workspace/skills/cn-search/search.py "防水补漏 小红书"

# 使用 Bing 搜索
python ~/.openclaw/workspace/skills/cn-search/search.py "Python教程" --engine bing --count 10
```

## 返回格式

JSON 格式的搜索结果列表：

```json
{
  "query": "搜索词",
  "engine": "baidu",
  "results": [
    {
      "title": "标题",
      "url": "链接",
      "snippet": "摘要"
    }
  ]
}
```

## 注意事项

- 此技能仅在国内网络环境下使用
- 搜索结果来自百度/Bing，可能受搜索引擎限制
- 如果 web_search 可用，优先使用 web_search
