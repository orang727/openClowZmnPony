---
name: zhihu
description: 知乎内容获取工具。搜索知乎、获取热门回答、问题详情等。当用户需要知乎内容时使用此技能。
---

# 知乎内容获取技能

## 使用场景

当用户需要获取知乎内容时使用：
- 搜索知乎内容（需要配置 Cookie）
- 获取今日/本月热门回答
- 获取问题详情
- 获取问题下的回答列表

## 使用方法

脚本路径：`C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py`

### 搜索知乎（需要 Cookie）

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py search "关键词" [--type general|question|answer|article|user] [--count 10]
```

示例：
```bash
# 综合搜索
python C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py search "Python" --count 5

# 搜索用户
python C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py search "张三" --type user
```

### 获取热门回答

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py hot [--type day|month] [--count 10]
```

示例：
```bash
# 获取今日热门
python C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py hot --type day --count 5

# 获取本月热门
python C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py hot --type month
```

### 获取问题详情

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py question <问题ID或URL>
```

示例：
```bash
python C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py question 19550225
python C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py question "https://www.zhihu.com/question/19550225"
```

### 获取问题的回答列表

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py answers <问题ID> [--count 10] [--sort vote|time]
```

### 检查配置状态

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\zhihu\zhihu.py status
```

## 功能限制

- 搜索功能需要配置 Cookie
- Cookie 有效期有限，过期需重新获取

## Cookie 配置

搜索功能需要登录 Cookie：

1. 浏览器登录 zhihu.com
2. F12 → Application → Cookies
3. 获取以下 Cookie 值：
   - `z_c0`（必需）
   - `_xsrf`
   - `d_c0`
4. 创建 `config.json`：

```json
{
  "cookie": "z_c0=xxx; _xsrf=xxx; d_c0=xxx"
}
```

## 依赖安装

```bash
pip install zhihuapi requests
```

## 返回示例

```json
{
  "success": true,
  "data": {
    "type": "hot_day",
    "count": 5,
    "answers": [
      {
        "answer_id": 123456,
        "question": {
          "id": 789,
          "title": "问题标题",
          "url": "https://www.zhihu.com/question/789"
        },
        "author": {
          "name": "作者名"
        },
        "voteup_count": 1000,
        "content_preview": "回答内容预览..."
      }
    ]
  }
}
```

## 注意事项

- zhihuapi 使用知乎的内部 API
- 请求频率不宜过高
- 遵守知乎使用条款
