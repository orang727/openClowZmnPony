#!/bin/bash

# 防水智能报价工具 - 项目看板部署脚本
# 部署到 surge.sh

SOURCE_FILE="/Users/zmnmini/.openclaw/workspace-daguanjia/memory/projects/防水智能报价工具/项目完整看板.html"
DOMAIN="waterproof-complete-dashboard-20260308.surge.sh"

echo "🚀 开始部署项目看板到外网..."
echo "📄 源文件：$SOURCE_FILE"
echo "🌐 域名：$DOMAIN"

# 检查文件是否存在
if [ ! -f "$SOURCE_FILE" ]; then
    echo "❌ 文件不存在：$SOURCE_FILE"
    exit 1
fi

echo "✅ 文件存在，开始部署..."

# 使用 surge 部署
npx surge "$SOURCE_FILE" --domain "$DOMAIN"

if [ $? -eq 0 ]; then
    echo "✅ 部署成功！"
    echo "🌐 访问地址：https://$DOMAIN"
else
    echo "❌ 部署失败"
    echo "💡 请手动部署或检查 surge 登录状态"
fi
