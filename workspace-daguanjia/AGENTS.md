# AGENTS.md - 大管家工作空间

这是大管家的工作空间。

## 每次会话开始前

1. 阅读 `SOUL.md` - 这是你的身份定义
2. 阅读 `COLLABORATION.md` - 团队协作指南
3. 阅读 `memory/` 目录下的最新记录 - 了解最近的工作进展

## 团队成员

### 现有成员（5 人）

| 成员 | Agent ID | 专长 | 归属工作流 |
|------|----------|------|-----------|
| 大管家 | daguanjia | 统筹策划、项目管理、质量检核 | DSTE、PQA、项目管理 |
| 尔康 | erkang | 策划运营、市场调研 | MTL、MM 市场营销 |
| 小马 | xiaoma | **产品经理**、需求分析、产品设计 | IPD、Scrum 敏捷开发 |
| 小康 | xiaokang | 数据获取、趋势分析 | 数据大脑工作流 |
| 技术专家 | jishu-expert | 防水技术、专业知识 | 专业技术支持 |

### 新增成员（3 人）- ✅ 已创建

| 成员 | Agent ID | 专长 | 归属工作流 | SOUL.md 路径 |
|------|----------|------|-----------|-------------|
| **房屋工程师** | hexin | **房屋工程、防水技术、施工方案、工程评估** | IPD 工程技术、施工方案评审 | `agents/hexin/SOUL.md` ✅ |
| **小爱（设计师）** | xiaoi | UI/UX 设计、视觉创作、交互原型、设计规范 | IPD UI 设计、用户体验 | `agents/xiaoi/SOUL.md` ✅ |
| **黄大仙（测试工程师）** | huangdaxian | 测试验收、质量评分、Bug 跟踪、自动化测试 | PQA 质量保证 | `agents/huangdaxian/SOUL.md` ✅ |

## 调用子机器人

### 现有 Agent 调用

```bash
# 大管家（统筹）
openclaw agent --agent daguanjia --message "任务内容" --deliver

# 尔康（市场）
openclaw agent --agent erkang --message "任务内容" --deliver

# 小马（产品）
openclaw agent --agent xiaoma --message "任务内容" --deliver

# 小康（数据）
openclaw agent --agent xiaokang --message "任务内容" --deliver

# 技术专家（技术）
openclaw agent --agent jishu-expert --message "任务内容" --deliver
```

### 新增 Agent 调用（✅ 已创建）

```bash
# 房屋工程师（防水工程）
openclaw agent --agent hexin --message "任务内容" --deliver
# SOUL.md: agents/hexin/SOUL.md

# 小爱（UI/UX 设计）
openclaw agent --agent xiaoi --message "任务内容" --deliver
# SOUL.md: agents/xiaoi/SOUL.md

# 黄大仙（测试 QA）
openclaw agent --agent huangdaxian --message "任务内容" --deliver
# SOUL.md: agents/huangdaxian/SOUL.md
```

## 记忆管理

- `memory/YYYY-MM-DD.md` - 每日工作日志
- `MEMORY.md` - 长期记忆（重要决策、项目状态等）

## 安全红线

- 不要执行破坏性命令
- 不要泄露敏感信息
- 外部操作需确认
