---
name: douyin
description: 抖音视频信息获取工具。解析抖音视频链接获取视频详情。当用户提供抖音视频链接时使用此技能。
---

# 抖音视频信息获取技能

## 使用场景

当用户需要获取抖音视频信息时使用：
- 解析抖音分享链接
- 获取视频标题、作者、播放量等信息
- 获取视频封面和播放地址

## 使用方法

脚本路径：`C:\Users\Administrator\.openclaw\workspace\skills\douyin\douyin.py`

### 获取视频信息

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\douyin\douyin.py info <视频链接>
```

支持的链接格式：
- 短链接：`https://v.douyin.com/xxxxx/`
- 完整链接：`https://www.douyin.com/video/7329515945095608615`

示例：
```bash
python C:\Users\Administrator\.openclaw\workspace\skills\douyin\douyin.py info "https://v.douyin.com/iRNBho5t/"
```

### 检查配置状态

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\douyin\douyin.py status
```

## 功能限制

由于抖音严格的反爬虫机制：
- 关键词搜索功能不可用
- 视频详情 API 需要签名验证
- 部分功能依赖 douyin-tiktok-scraper 库

## 依赖安装

```bash
pip install douyin-tiktok-scraper requests
```

## Cookie 配置（可选）

配置 Cookie 可能提高成功率：

1. 浏览器登录 douyin.com
2. F12 → Network → 复制 Cookie
3. 创建 `config.json`：

```json
{
  "cookie": "完整的Cookie字符串"
}
```

## 注意事项

- 抖音反爬虫机制严格，解析可能失败
- 建议使用短链接进行解析
- 遵守抖音使用条款
