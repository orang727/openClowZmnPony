---
name: waterproof-monitor
description: 防水补漏数据监控分析。用于每天自动获取抖音、小红书平台上"防水补漏"相关内容，分析受欢迎程度和评论，并生成报告推送给用户。当用户需要监控防水补漏行业数据、分析社交媒体热点、或设置定时数据报告时触发此技能。
---

# 防水补漏数据监控技能

## 技能状态
- **状态**: 暂存（网络问题待解决）
- **创建时间**: 2026-03-01

## 功能概述
自动获取抖音、小红书平台上"防水补漏"相关内容，分析受欢迎程度（点赞、收藏、分享）和评论热点，生成每日报告并推送给用户。

## 当前配置

### 数据源
- **搜索API**: Brave Search API
- **API Key**: BSAP3xm4s10rblwH8cJF8H2wfyKxze8（已配置，但网络不通）

### 飞书Bitable（备用方案）
- **App**: 防水补漏数据监控
- **Token**: PX8DbSiayabwgps8b5NcisNwnoc
- **链接**: https://my.feishu.cn/base/PX8DbSiayabwgps8b5NcisNwnoc

### 字段结构
| 字段 | 类型 |
|------|------|
| 平台 | 单选（小红书/抖音）|
| 日期 | 日期时间 |
| 点赞数 | 数字 |
| 收藏数 | 数字 |
| 评论数 | 数字 |
| 分享数 | 数字 |
| 链接 | URL |

## 搜索关键词
- 防水补漏
- 防水施工
- 房屋漏水
- 卫生间防水
- 屋顶防水

## 启用步骤

### 方案1: 恢复 Brave Search（需要网络）
1. 确认机器可以访问 api.search.brave.com
2. 重启 Gateway 让 BRAVE_API_KEY 生效
3. 测试 web_search 功能
4. 设置每日定时任务

### 方案2: 使用飞书Bitable（稳定）
1. 用户每天导出小红书/抖音数据到表格
2. 读取 Bitable 数据进行分析
3. 生成报告推送给用户

## 输出
- 每日摘要报告
- 发送至飞书 DM

## 相关文件
- 任务配置: memory/data-task.md
- 心跳任务: HEARTBEAT.md
