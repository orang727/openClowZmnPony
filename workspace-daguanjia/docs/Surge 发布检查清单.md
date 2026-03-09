# Surge 发布检查清单

> **目的**: 避免 404 错误，确保每次发布都能正常访问  
> **适用范围**: 所有 Surge 发布操作

---

## ✅ 发布前检查（必须）

### 1. 文件检查

- [ ] **index.html 存在** - Surge 入口文件（最重要！）
- [ ] 文件内容正确 - 不是空白或错误内容
- [ ] 相关文件完整 - CSS/JS/图片等依赖文件

### 2. 目录结构检查

```
project-folder/
├── index.html          # ✅ 必须存在
├── styles.css          # 可选
├── script.js           # 可选
└── images/             # 可选
```

### 3. index.html 验证

```bash
# 检查文件是否存在
ls -la project-folder/index.html

# 检查文件大小（应该 > 0）
wc -c project-folder/index.html

# 快速查看内容
head -20 project-folder/index.html
```

---

## 🚀 发布步骤

### 标准流程

```bash
# 1. 进入项目目录
cd /path/to/project

# 2. 确认 index.html 存在
ls -la index.html

# 3. 发布到 Surge
surge . your-domain.surge.sh
```

### 使用发布脚本（推荐）

```bash
# 自动检查并发布
bash ~/.openclaw/workspace-daguanjia/scripts/surge-publish.sh /path/to/project domain-name.surge.sh
```

---

## ❌ 常见问题

### 问题 1: 404 Not Found

**原因**: 缺少 `index.html` 文件

**解决**:
```bash
# 检查文件
ls -la index.html

# 如果不存在，创建或复制
cp source-file.html index.html

# 重新发布
surge . domain.surge.sh
```

### 问题 2: 内容不是最新的

**原因**: 发布了旧版本文件

**解决**:
```bash
# 清理旧文件
rm -rf project-folder/*

# 复制新文件
cp new-files/* project-folder/

# 确认 index.html
ls -la project-folder/index.html

# 重新发布
surge . domain.surge.sh
```

### 问题 3: Surge 缓存问题

**原因**: Surge CDN 缓存了旧版本

**解决**:
```bash
# 使用 --force 强制刷新
surge . domain.surge.sh --force
```

---

## 📋 发布后验证

### 1. 立即访问测试

```bash
# 使用 curl 测试
curl -I https://domain.surge.sh

# 应该返回 HTTP/1.1 200 OK
```

### 2. 浏览器测试

- [ ] 打开链接能正常访问
- [ ] 页面内容正确
- [ ] 样式和脚本正常加载
- [ ] 图片正常显示

### 3. 移动端测试（如适用）

- [ ] 在手机上访问正常
- [ ] 响应式布局正常
- [ ] 触摸交互正常

---

## 🎯 最佳实践

### 1. 使用版本化域名

```bash
# v1 版本
surge . project-v1.surge.sh

# v2 版本
surge . project-v2.surge.sh

# final 版本
surge . project-final.surge.sh
```

### 2. 发布前本地测试

```bash
# 使用 Python 快速启动本地服务器
cd project-folder
python3 -m http.server 8080

# 浏览器访问 http://localhost:8080 测试
```

### 3. 保留发布记录

创建 `RELEASE.md` 记录每次发布：

```markdown
# 发布记录

## v2.0 - 2026-03-09
- 域名：project-v2.surge.sh
- 更新内容：xxx
- 发布人：xxx
```

---

## 🔧 自动化脚本

### 一键发布脚本

```bash
#!/bin/bash
# save as: publish.sh

PROJECT_DIR="$1"
DOMAIN="$2"

# 检查 index.html
if [ ! -f "$PROJECT_DIR/index.html" ]; then
    echo "❌ 错误：缺少 index.html"
    exit 1
fi

# 发布
cd "$PROJECT_DIR" && surge . "$DOMAIN"
```

---

## 📞 快速排查

如果发布后 404，按顺序检查：

1. ✅ `index.html` 是否存在？
2. ✅ `index.html` 是否有内容？
3. ✅ 发布目录是否正确？
4. ✅ 域名是否拼写正确？
5. ✅ Surge 账户是否正常？

---

> **最后更新**: 2026-03-09  
> **维护人**: 大管家
