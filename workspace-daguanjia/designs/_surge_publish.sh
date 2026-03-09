#!/bin/bash
# Surge 发布脚本 - 防水智能报价系统 UI 设计

DESIGN_DIR="/Users/zmnmini/.openclaw/workspace-daguanjia/designs"
SURGE_PROJECT="waterproof-quote-ui-design"

cd "$DESIGN_DIR"

# 创建 Surge 项目目录
mkdir -p ./surge-publish
cd ./surge-publish

# 复制所有 PNG 图片
cp ../S1-pencil-final.png ./S1-locations.png
cp ../S2-upload.png ./S2-upload.png
cp ../S3-ai-analysis.png ./S3-ai-analysis.png
cp ../waterproof-quote-full.png ./design-fullview.png

# 创建 index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>防水智能报价系统 - UI 设计</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 1200px; margin: 0 auto; padding: 40px 20px; background: #f5f5f5; }
        h1 { text-align: center; color: #1e40af; margin-bottom: 40px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(375px, 1fr)); gap: 40px; justify-items: center; }
        .card { background: white; border-radius: 16px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .card h3 { text-align: center; color: #1f2937; margin-bottom: 16px; }
        .card img { width: 375px; height: auto; border-radius: 12px; }
        .full-width { grid-column: 1 / -1; }
        .info { background: #dbeafe; padding: 20px; border-radius: 12px; margin-bottom: 40px; }
        .info h2 { color: #1e40af; margin-bottom: 12px; }
        .info p { color: #1e40af; line-height: 1.6; }
    </style>
</head>
<body>
    <h1>🏠 防水智能报价系统 - UI 设计</h1>
    
    <div class="info">
        <h2>📋 设计说明</h2>
        <p><strong>PRD 版本:</strong> v2.3 | <strong>设计日期:</strong> 2026-03-09 | <strong>设计工具:</strong> Pencil MCP</p>
        <p><strong>设计风格:</strong> 蓝色系专业风格 | <strong>目标尺寸:</strong> 375×812 (移动端)</p>
        <p><strong>核心流程:</strong> S1 位置选择 → S2 图片上传 → S3 AI 分析 → S4 方案推荐 → S5 价格显示 → S6 留资下单</p>
    </div>
    
    <div class="grid">
        <div class="card">
            <h3>S1 漏点位置选择</h3>
            <img src="S1-locations.png" alt="S1 位置选择">
        </div>
        <div class="card">
            <h3>S2 上传现场图片</h3>
            <img src="S2-upload.png" alt="S2 图片上传">
        </div>
        <div class="card">
            <h3>S3 AI 智能分析</h3>
            <img src="S3-ai-analysis.png" alt="S3 AI 分析">
        </div>
        <div class="card full-width">
            <h3>完整设计长图</h3>
            <img src="design-fullview.png" alt="完整设计" style="width:100%;max-width:1200px">
        </div>
    </div>
    
    <div style="text-align:center;margin-top:40px;color:#6b7280">
        <p>设计交付完成 | 防水智能报价系统 v2.3</p>
    </div>
</body>
</html>
EOF

echo "✅ Surge 发布目录已准备"
ls -lh
