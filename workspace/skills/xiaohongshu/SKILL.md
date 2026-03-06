---
name: xiaohongshu
description: 小红书内容获取工具。获取推荐笔记列表。当用户需要小红书内容时使用此技能。
---

# 小红书内容获取技能

## 使用场景

当用户需要获取小红书（xiaohongshu）内容时使用：
- 获取首页推荐笔记
- 查看笔记标题、作者、点赞数等基本信息

## 使用方法

脚本路径：`C:\Users\Administrator\.openclaw\workspace\skills\xiaohongshu\xiaohongshu.py`

### 获取推荐笔记

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\xiaohongshu\xiaohongshu.py recommend [--count 10]
```

示例：
```bash
python C:\Users\Administrator\.openclaw\workspace\skills\xiaohongshu\xiaohongshu.py recommend --count 5
```

### 检查配置状态

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\xiaohongshu\xiaohongshu.py status
```

## Cookie 配置

需要配置小红书 Cookie 才能使用：

1. 浏览器登录 xiaohongshu.com
2. F12 → Network → 刷新页面 → 复制 Request Headers 中的 Cookie
3. 创建 `config.json`：

```json
{
  "cookie": "完整的Cookie字符串"
}
```

## 功能限制

由于小红书反爬虫机制，以下功能受限：
- 关键词搜索 API 不可用
- 笔记详情 API 不可用
- 仅支持获取首页推荐内容

## 返回示例

```json
{
  "success": true,
  "data": {
    "type": "recommend",
    "count": 3,
    "notes": [
      {
        "note_id": "xxx",
        "title": "笔记标题",
        "type": "normal",
        "cover": "封面图URL",
        "user": {
          "user_id": "xxx",
          "nickname": "用户昵称",
          "avatar": "头像URL"
        },
        "liked_count": "1.9万",
        "url": "https://www.xiaohongshu.com/explore/xxx"
      }
    ]
  }
}
```

## 注意事项

- Cookie 有效期有限，过期需重新获取
- 遵守小红书使用条款
- 请求频率不宜过高
