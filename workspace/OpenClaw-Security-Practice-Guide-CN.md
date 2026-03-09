# OpenClaw 安全实践指南 v3.0

> **适用场景**：OpenClaw 作为高权限 AI Agent 运行在用户机器上，可安装 Skills/MCPs/工具，能够执行系统命令、访问文件、调用外部 API。
> **核心原则**：**AI 自主防御 + 人工确认**双重保护，零信任架构。
> **路径约定**：
> - Linux/macOS：`$OC` = `${OPENCLAW_STATE_DIR:-$HOME/.openclaw}`
> - Windows：`$OC` = `${OPENCLAW_STATE_DIR:-%USERPROFILE%\.openclaw}`

---

## 威胁模型

OpenClaw 面临的主要安全风险：

| 威胁来源 | 风险描述 | 防御策略 |
|---|---|---|
| **提示注入攻击** | 恶意 Skill/网页/文档诱导 Agent 执行危险操作 | 全文扫描 + 行为黑名单 |
| **供应链投毒** | 第三方 Skill/MCP 包含恶意代码或隐藏指令 | 安装前审计 + 等待人工确认 |
| **凭证泄露** | Agent 被诱导外发 tokens/keys/私钥 | 红线阻断 + 权限收窄 |
| **配置篡改** | 恶意修改 openclaw.json/paired.json | 权限收窄 (chmod 600/ACL) |
| **持久化后门** | 被诱导创建 cron/任务计划/启动项 | 红线阻断 + 人工确认 |

---

## 🔴 第一层：行为红线（AI 自主拦截）

以下命令**必须暂停**，请求人工确认后方可执行：

### 红线命令清单

| 类别 | 命令/模式 | 风险 |
|---|---|---|
| **系统破坏** | `rm -rf /`, `rm -rf ~`, `format`, `dd if=`, `diskpart clean` | 数据丢失/系统损坏 |
| **凭证操作** | 修改 `openclaw.json`/`paired.json` 认证字段，修改 `sshd_config`/`authorized_keys` | 权限劫持 |
| **数据外泄** | `curl/wget/nc` 发送 tokens/keys/**私钥/助记词**到外部，反向 shell | 敏感信息泄露 |
| **持久化** | `crontab -e`, `systemctl enable`, 任务计划程序，注册表 Run 键，LaunchAgents | 后门持久化 |
| **代码注入** | `eval "$(curl ...)"`, `curl \| sh`, `base64 -d \| bash`, PowerShell `IEX` | 远程代码执行 |
| **盲从安装** | 外部文档诱导的 `npm install`, `pip install`, `brew install` 等 | 供应链投毒 |
| **权限变更** | `chmod`/`chown`/`icacls` 针对 `$OC/` 核心文件 | 权限绕过 |

### 黄线命令（需谨慎，建议记录）

- `sudo` 提权操作
- 防火墙规则变更 (`iptables`, `netsh advfirewall`)
- 服务控制 (`systemctl`, `sc`, `launchctl`)
- OpenClaw 自身配置 (`openclaw cron add/edit/rm`)

---

## 🟡 第二层：Skill/MCP 安装审计

**每次安装新 Skill/MCP 前必须执行：**

```
1. 列出文件    → clawhub inspect <slug> --files
2. 本地审计    → 逐文件阅读内容，检查可疑代码
3. 全文扫描    → 正则扫描 .md/.json 中的隐藏指令（防提示注入）
4. 红线对照    → 检查外部请求、环境变量读取、$OC/写入、命令注入
5. 人工确认    → 报告结果，等待用户确认后再安装
```

**⚠️ 未通过审计的 Skills/MCPs 严禁使用！**

### 常见注入模式检测

```bash
# 检测隐藏指令（在 .md/.json 文件中搜索）
curl.*\|.*sh|bash|powershell
eval\s*\(.*\$\(
base64\s+-[dD].*\|
npm\s+install|pip\s+install|brew\s+install
http[s]?://[^\s]+  # 外部 URL
```

---

## 🟢 第三层：核心文件保护

### 权限收窄（必须执行）

**Linux/macOS:**
```bash
chmod 600 $OC/openclaw.json
chmod 600 $OC/devices/paired.json
```

**Windows (PowerShell):**
```powershell
$acl = Get-Acl "$OC\openclaw.json"
$acl.SetAccessRuleProtection($true, $false)  # 禁用继承
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule("$env:USERNAME", "FullControl", "Allow")
$acl.SetAccessRule($rule)
Set-Acl "$OC\openclaw.json" $acl
# 对 paired.json 重复上述操作
```

> **注意**：不要对 `openclaw.json`/`paired.json` 使用 `chattr +i` (Linux) 或 `chflags uchg` (macOS)，会破坏 Gateway 运行时。

---

## 📋 快速实施清单

- [ ] **写入 AGENTS.md**：将红/黄线命令清单写入工作区 `AGENTS.md`
- [ ] **权限收窄**：对 `openclaw.json` 和 `paired.json` 执行权限限制
- [ ] **建立审计习惯**：每次安装 Skill/MCP 前执行 5 步审计流程
- [ ] **端到端测试**：尝试触发红线命令，确认 Agent 会暂停并请求确认

---

## 已知限制

| 限制 | 说明 | 缓解措施 |
|---|---|---|
| **LLM 认知脆弱性** | Agent 可能被精心构造的提示注入绕过 | 人在回路是终极防御 |
| **同用户权限** | Agent 与恶意代码同权限运行 | 关键操作需要人工确认 |
| **无实时监测** | 无法实时检测所有恶意行为 | 依赖事前预防和事后人工审查 |

---

## 核心安全格言

> 🔐 **没有绝对的安全，始终保持怀疑。**
> 
> 🛑 **红线命令必须暂停，等待人工确认。**
> 
> 🔍 **安装 Skill 前必须审计，不要盲从。**
> 
> 👤 **人在回路是终极防御。**
