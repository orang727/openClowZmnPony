#!/bin/bash
# Surge 发布前自动检查脚本
# 用法：./surge-check.sh /path/to/project

set -e

PROJECT_DIR="$1"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Surge 发布前检查"
echo "=================="
echo "项目目录：$PROJECT_DIR"
echo ""

ERRORS=0
WARNINGS=0

# 1. 检查目录是否存在
echo -n "1. 检查目录存在性 ... "
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${GREEN}✅ 通过${NC}"
else
    echo -e "${RED}❌ 失败 - 目录不存在${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 2. 检查 index.html 是否存在
echo -n "2. 检查 index.html ... "
if [ -f "$PROJECT_DIR/index.html" ]; then
    echo -e "${GREEN}✅ 通过${NC}"
else
    echo -e "${RED}❌ 失败 - index.html 不存在${NC}"
    echo -e "${YELLOW}   提示：Surge 需要 index.html 作为入口文件${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 3. 检查 index.html 大小
if [ -f "$PROJECT_DIR/index.html" ]; then
    echo -n "3. 检查 index.html 大小 ... "
    SIZE=$(wc -c < "$PROJECT_DIR/index.html")
    if [ "$SIZE" -gt 100 ]; then
        echo -e "${GREEN}✅ 通过 ($SIZE bytes)${NC}"
    else
        echo -e "${YELLOW}⚠️  警告 - 文件太小 ($SIZE bytes)${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# 4. 检查 index.html 内容
if [ -f "$PROJECT_DIR/index.html" ]; then
    echo -n "4. 检查 index.html 内容 ... "
    if grep -q "<!DOCTYPE html>" "$PROJECT_DIR/index.html" 2>/dev/null; then
        echo -e "${GREEN}✅ 通过 (HTML5 文档)${NC}"
    elif grep -q "<html" "$PROJECT_DIR/index.html" 2>/dev/null; then
        echo -e "${GREEN}✅ 通过 (HTML 文档)${NC}"
    else
        echo -e "${YELLOW}⚠️  警告 - 可能不是有效的 HTML 文件${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# 5. 检查其他常见文件
echo -n "5. 检查其他文件 ... "
FILE_COUNT=$(find "$PROJECT_DIR" -type f | wc -l)
if [ "$FILE_COUNT" -gt 1 ]; then
    echo -e "${GREEN}✅ 通过 (共 $FILE_COUNT 个文件)${NC}"
else
    echo -e "${YELLOW}⚠️  警告 - 目录中只有 index.html${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# 6. 检查文件权限
echo -n "6. 检查文件可读性 ... "
if [ -r "$PROJECT_DIR/index.html" ]; then
    echo -e "${GREEN}✅ 通过${NC}"
else
    echo -e "${RED}❌ 失败 - index.html 不可读${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 总结
echo ""
echo "=================="
echo "检查结果:"
echo "  错误：$ERRORS"
echo "  警告：$WARNINGS"
echo ""

if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}❌ 发布前检查失败，请修复错误后再发布${NC}"
    echo ""
    echo "建议操作:"
    echo "  1. 确保 index.html 存在于项目目录"
    echo "  2. 确保 index.html 有正确的 HTML 内容"
    echo "  3. 重新运行检查：$0 $PROJECT_DIR"
    exit 1
elif [ "$WARNINGS" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  存在警告，但可以继续发布${NC}"
    read -p "是否继续发布？(y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ]; then
        echo "❌ 取消发布"
        exit 1
    fi
else
    echo -e "${GREEN}✅ 所有检查通过，可以安全发布${NC}"
fi

echo ""
echo "准备发布..."
