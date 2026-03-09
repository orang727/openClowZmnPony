#!/bin/bash
# 防水知识每日学习脚本

cd /Users/zmnmini/.openclaw/workspace-expert

# 定义搜索函数
search_and_learn() {
    query="$1"
    source="$2"
    echo "=== 正在学习: $query [$source] ===" 
    python3 ~/.openclaw/workspace/skills/cn-search/search.py "$query" --engine baidu --count 5
}

# 搜索防水相关内容
echo "$(date '+%Y-%m-%d %H:%M:%S') 开始每日防水知识学习..."

# 1. 搜索防水专业内容
search_and_learn "建筑防水材料种类" "专业网站"
search_and_learn "屋面防水施工工艺" "专业网站"
search_and_learn "地下室防水技术规范" "国标规范"
search_and_learn "卫生间防水做法" "专业网站"
search_and_learn "外墙防水补漏方法" "专业网站"

# 2. 搜索专业品牌
search_and_learn "东方雨虹防水涂料" "品牌官网"
search_and_learn "科顺防水怎么样" "品牌官网"

# 3. 搜索热门平台内容
search_and_learn "防水补漏小知识" "小红书"
search_and_learn "防水施工效果" "抖音"
search_and_learn "屋面防水教学" "B站"

# 4. 搜索知乎专业问答
search_and_learn "防水涂料哪种好" "知乎"
search_and_learn "装修防水注意事项" "知乎"

# 5. 专利搜索
search_and_learn "防水涂料 专利" "专利"

echo "$(date '+%Y-%m-%d %H:%M:%S') 学习完成"

# 记录日志
echo "$(date '+%Y-%m-%d %H:%M:%S') 每日防水知识学习完成" >> memory/daily-learning.log
