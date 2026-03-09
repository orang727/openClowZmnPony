# 🚀 Surge 快速部署指南

## ⚠️ 当前状态

Surge 需要登录验证才能部署。

---

## 🔑 登录方式（2 选 1）

### 方式 1：命令行登录（推荐）

**步骤**:

1. **打开终端**

2. **运行登录命令**
```bash
surge login
```

3. **输入邮箱**
- 输入您的邮箱地址（或注册新账号）
- 按 Enter

4. **检查邮箱**
- Surge 会发送登录链接到您的邮箱
- 点击邮件中的链接完成登录

5. **返回终端，重新运行部署**
```bash
cd /Users/zmnmini/.openclaw/workspace-daguanjia/memory/projects/防水智能报价工具
npx surge ./项目完整看板.html --domain waterproof-complete-dashboard-20260308.surge.sh
```

---

### 方式 2：使用 Surge Token（自动化）

**步骤**:

1. **获取 Surge Token**
- 访问：https://surge.sh/login
- 登录后获取 token

2. **设置环境变量**
```bash
export SURGE_TOKEN="your_token_here"
```

3. **部署**
```bash
cd /Users/zmnmini/.openclaw/workspace-daguanjia/memory/projects/防水智能报价工具
npx surge ./项目完整看板.html --domain waterproof-complete-dashboard-20260308.surge.sh
```

---

## 🎯 快速操作流程

```bash
# 1. 登录（首次）
surge login
# → 检查邮箱，点击登录链接

# 2. 部署
cd /Users/zmnmini/.openclaw/workspace-daguanjia/memory/projects/防水智能报价工具
npx surge ./项目完整看板.html --domain waterproof-complete-dashboard-20260308.surge.sh

# 3. 完成！
# → 访问：https://waterproof-complete-dashboard-20260308.surge.sh
```

---

## ✅ 部署成功后

访问看板：
```
https://waterproof-complete-dashboard-20260308.surge.sh
```

---

## 🔄 后续更新

修改看板后重新部署（无需重新登录）：

```bash
cd /Users/zmnmini/.openclaw/workspace-daguanjia/memory/projects/防水智能报价工具
npx surge ./项目完整看板.html --domain waterproof-complete-dashboard-20260308.surge.sh
```

---

## 💡 提示

- Surge 登录凭证会保存在 `~/.surge` 文件
- 下次部署无需重新登录
- Token 长期有效，除非手动清除

---

**请先执行 `surge login` 完成登录，然后重新运行部署命令**！🫡
