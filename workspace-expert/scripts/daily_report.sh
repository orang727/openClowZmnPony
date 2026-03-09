#!/bin/bash
# 防水知识每日汇报脚本

cd /Users/zmnmini/.openclaw/workspace-expert

echo "=== 每日防水知识学习汇报 ===" 
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 统计学习次数
learning_count=$(grep -c "正在学习" memory/learning.log 2>/dev/null || echo "0")
echo "今日学习次数: $learning_count"

# 显示今日学习内容
echo ""
echo "--- 今日学习记录 ---"
tail -20 memory/learning.log 2>/dev/null

echo ""
echo "=== 汇报完成 ==="
