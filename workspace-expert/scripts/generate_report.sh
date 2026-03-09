#!/bin/bash
# 防水知识每日汇报生成

cd /Users/zmnmini/.openclaw/workspace-expert

# 获取今日日期
TODAY=$(date '+%Y-%m-%d')

# 统计学习次数
LEARNING_COUNT=$(grep -c "正在学习" memory/learning.log 2>/dev/null || echo "0")

# 生成汇报内容
REPORT="📚 防水知识学习日报
📅 日期: $TODAY

✅ 今日学习: $LEARNING_COUNT 次"

# 获取学习内容
CONTENT=$(grep "正在学习" memory/learning.log 2>/dev/null | tail -5)

if [ -n "$CONTENT" ]; then
    REPORT="$REPORT

📖 学习内容:"
    while IFS= read -r line; do
        REPORT="$REPORT
- $line"
    done <<< "$CONTENT"
fi

REPORT="$REPORT

💧 持续学习中..."

# 保存汇报
echo "$REPORT" > memory/daily_report.txt

echo "$REPORT"
