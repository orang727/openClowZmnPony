#!/bin/bash
# 防水补漏每日监控脚本
# 执行时间: 每天早上6点

cd ~/.openclaw/workspace

# 搜索防水补漏相关内容
RESULT=$(python3 ~/.openclaw/workspace/skills/cn-search/search.py "防水补漏 小红书 抖音" --engine bing --count 10 2>/dev/null)

# 生成报告
REPORT="📊 防水补漏每日数据监控

**日期**: $(date '+%Y-%m-%d')

**搜索结果**:
$RESULT

---
由小康自动生成"

# 发送到飞书（通过 OpenClaw message）
echo "$REPORT"
