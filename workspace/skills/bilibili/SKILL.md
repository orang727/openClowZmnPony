---
name: bilibili
description: B站视频信息获取工具。获取视频详情、评论、下载地址等。当用户提供B站视频链接或BV号时使用此技能。
---

# B站视频信息获取技能

## 使用场景

当用户需要获取 B站（哔哩哔哩）视频的以下信息时使用：
- 视频基本信息（标题、描述、播放量、点赞等）
- 视频评论
- UP主信息
- 视频下载地址

## 使用方法

脚本路径：`C:\Users\Administrator\.openclaw\workspace\skills\bilibili\bilibili.py`

### 获取视频信息

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\bilibili\bilibili.py info <BV号或视频链接>
```

示例：
```bash
python C:\Users\Administrator\.openclaw\workspace\skills\bilibili\bilibili.py info BV1uv411q7Mv
```

### 获取视频评论

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\bilibili\bilibili.py comments <BV号> [--count 20]
```

### 获取视频下载地址

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\bilibili\bilibili.py download <BV号>
```

### 登录B站（获取完整评论需要）

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\bilibili\bilibili.py login
```

执行后会显示二维码，用户使用B站APP扫码登录，凭据会自动保存到 `config.json`。

### 检查登录状态

```bash
python C:\Users\Administrator\.openclaw\workspace\skills\bilibili\bilibili.py status
```

## 返回格式

JSON 格式输出，包含请求的视频信息。

## 注意事项

- 支持 BV号 和完整视频链接
- 部分功能可能需要登录（评论等）
- 视频下载地址有时效性
- 遵守B站使用条款，不要滥用
