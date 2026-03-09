#!/bin/bash
# Surge 发布标准化脚本
# 用途：确保每次发布都包含 index.html，避免 404 问题

set -e

PROJECT_DIR="$1"
DOMAIN="$2"

echo "🚀 Surge 发布脚本"
echo "================"
echo "项目目录：$PROJECT_DIR"
echo "域名：$DOMAIN"
echo ""

# 检查目录是否存在
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ 错误：目录不存在 - $PROJECT_DIR"
    exit 1
fi

# 检查是否有 index.html
if [ ! -f "$PROJECT_DIR/index.html" ]; then
    echo "⚠️  警告：目录中没有 index.html 文件"
    echo ""
    echo "可选操作："
    echo "1. 创建空白 index.html"
    echo "2. 从其他文件生成 index.html"
    echo "3. 取消发布"
    echo ""
    read -p "请选择 (1/2/3): " choice
    
    case $choice in
        1)
            cat > "$PROJECT_DIR/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>项目发布</title>
</head>
<body>
    <h1>项目已发布</h1>
    <p>请上传 index.html 文件</p>
</body>
</html>
EOF
            echo "✅ 已创建空白 index.html"
            ;;
        2)
            echo "请指定源文件路径："
            read SOURCE_FILE
            cp "$SOURCE_FILE" "$PROJECT_DIR/index.html"
            echo "✅ 已复制 $SOURCE_FILE 到 index.html"
            ;;
        3)
            echo "❌ 取消发布"
            exit 1
            ;;
        *)
            echo "❌ 无效选择"
            exit 1
            ;;
    esac
fi

# 检查 index.html 内容
echo ""
echo "📄 index.html 信息："
ls -lh "$PROJECT_DIR/index.html"
echo ""

# 确认发布
read -p "确认发布到 $DOMAIN ? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ 取消发布"
    exit 1
fi

# 执行发布
echo ""
echo "🚀 开始发布..."
cd "$PROJECT_DIR"
surge . "$DOMAIN"

echo ""
echo "✅ 发布完成！"
echo "访问链接：https://$DOMAIN"
