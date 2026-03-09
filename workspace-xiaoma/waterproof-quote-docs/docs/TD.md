# 防水补漏智能报价器 - 技术开发文档 (TD)

**文档版本**：v1.0  
**创建日期**：2026-03-05  
**技术栈**：Vue3 + Vant + FastAPI + MySQL

---

## 一、系统架构

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        小程序宿主                                │
│  ┌─────────────────┐                                            │
│  │   WebView H5   │ ◄─── user_id / token 参数                  │
│  └────────┬────────┘                                            │
└───────────┼─────────────────────────────────────────────────────┘
            │ HTTP/HTTPS
            ▼
┌───────────────────────────────────────────────────────────────────┐
│                      后端服务 (Python FastAPI)                     │
│                                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  用户模块    │  │  报价模块    │  │  工单模块               │  │
│  │  /session   │  │  /quote     │  │  /order                │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    规则引擎 & 报价计算                        │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                 AI 图像分析服务                              │  │
│  └─────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
            │                    │
            ▼                    ▼
    ┌───────────────┐    ┌───────────────┐
    │   MySQL      │    │  对象存储     │
    │  (数据库)    │    │ (OSS/COS)    │
    └───────────────┘    └───────────────┘
```

### 1.2 技术选型

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | Vue 3 + TypeScript | 响应式框架 |
| UI组件 | Vant 4 | 移动端组件库 |
| 构建工具 | Vite | 快速构建 |
| 路由 | Vue Router 4 | 页面路由 |
| 网络 | Axios | HTTP 请求 |
| 后端 | Python FastAPI | 高性能 API 框架 |
| 数据库 | MySQL 8.0 | 关系型数据库 |
| 对象存储 | 阿里云 OSS / 腾讯云 COS | 图片存储 |
| AI 服务 | 可配置 | minimax / OpenAI / 自研 |

---

## 二、数据库设计

### 2.1 数据库表结构

#### 2.1.1 报价请求表 (quote_requests)

```sql
CREATE TABLE `quote_requests` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` VARCHAR(64) NOT NULL COMMENT '用户ID',
  `location_type` VARCHAR(32) NOT NULL COMMENT '漏点位置',
  `floor_level` VARCHAR(16) DEFAULT NULL COMMENT '楼层',
  `house_age` VARCHAR(16) DEFAULT NULL COMMENT '房龄',
  `area_range` VARCHAR(16) DEFAULT NULL COMMENT '面积段',
  `description` TEXT COMMENT '问题描述',
  `images` JSON COMMENT '图片URL数组',
  `severity` VARCHAR(16) DEFAULT NULL COMMENT '严重程度: light/normal/severe',
  `severity_reason` TEXT COMMENT 'AI分析说明',
  `status` VARCHAR(16) DEFAULT 'pending' COMMENT '状态: pending/analyzed/ordered',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_status` (`status`),
  INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='报价请求表';
```

#### 2.1.2 施工方案表 (construction_plans)

```sql
CREATE TABLE `construction_plans` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `plan_code` VARCHAR(32) NOT NULL COMMENT '方案编码',
  `name` VARCHAR(128) NOT NULL COMMENT '方案名称',
  `description` TEXT COMMENT '方案描述',
  `location_types` JSON COMMENT '适用位置列表',
  `severity_levels` JSON COMMENT '适用严重程度列表',
  `base_price_min` DECIMAL(10,2) DEFAULT NULL COMMENT '基准价下限',
  `base_price_max` DECIMAL(10,2) DEFAULT NULL COMMENT '基准价上限',
  `duration` VARCHAR(32) DEFAULT NULL COMMENT '预计工期',
  `tags` JSON COMMENT '标签列表',
  `sort_order` INT DEFAULT 0 COMMENT '排序',
  `is_active` TINYINT DEFAULT 1 COMMENT '是否启用',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_plan_code` (`plan_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='施工方案表';
```

#### 2.1.3 工单表 (orders)

```sql
CREATE TABLE `orders` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `order_no` VARCHAR(32) NOT NULL COMMENT '工单编号',
  `request_id` BIGINT NOT NULL COMMENT '报价请求ID',
  `user_id` VARCHAR(64) NOT NULL COMMENT '用户ID',
  `chosen_plan_id` BIGINT NOT NULL COMMENT '选择的方案ID',
  `final_price_min` DECIMAL(10,2) DEFAULT NULL COMMENT '最终报价下限',
  `final_price_max` DECIMAL(10,2) DEFAULT NULL COMMENT '最终报价上限',
  `status` VARCHAR(16) DEFAULT 'new' COMMENT '状态: new/assigned/in_progress/completed/cancelled',
  `remark` TEXT COMMENT '备注',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  INDEX `idx_request_id` (`request_id`),
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='工单表';
```

#### 2.1.4 系统配置表 (system_config)

```sql
CREATE TABLE `system_config` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `config_key` VARCHAR(64) NOT NULL COMMENT '配置键',
  `config_value` TEXT COMMENT '配置值',
  `description` VARCHAR(256) DEFAULT NULL COMMENT '说明',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_config_key` (`config_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';
```

### 2.2 初始数据

#### 施工方案初始数据

```sql
INSERT INTO `construction_plans` (`plan_code`, `name`, `description`, `location_types`, `severity_levels`, `base_price_min`, `base_price_max`, `duration`, `tags`, `sort_order`) VALUES
('plan_standard_bathroom_light', '标准局部防水修复', '对渗水区域进行开槽、基层处理、防水涂刷2遍，并恢复表面。', '["bathroom", "kitchen", "balcony"]', '["light", "normal"]', 800.00, 1200.00, '约0.5-1天', '["标准型", "性价比高"]', 1),
('plan_enhanced_bathroom_severe', '加强型整体防水翻新', '对整个区域进行整体防水翻新，适合渗水点较多或老化严重的情况。', '["bathroom", "kitchen", "balcony"]', '["severe"]', 1500.00, 2200.00, '约1-2天', '["加强型", "更长寿命"]', 2),
('plan_roof_light', '屋顶局部修补', '针对屋顶局部裂缝进行修补，做防水处理。', '["roof"]', '["light"]', 600.00, 1000.00, '约0.5天', '["经济型"]', 3),
('plan_roof_severe', '屋顶整体防水', '对整个屋顶进行防水处理，新做防水层。', '["roof"]', '["normal", "severe"]', 2000.00, 5000.00, '约2-3天', '["加强型"]', 4),
('plan_wall_light', '外墙局部防水', '针对外墙裂缝进行修补防水处理。', '["outer_wall"]', '["light"]', 500.00, 800.00, '约0.5天', '["经济型"]', 5),
('plan_wall_severe', '外墙整体防水', '对外墙整体做防水涂料处理。', '["outer_wall"]', '["normal", "severe"]', 1500.00, 3000.00, '约1-2天', '["加强型"]', 6);
```

---

## 三、API 接口设计

### 3.1 接口概览

| 模块 | 接口路径 | 方法 | 说明 |
|------|----------|------|------|
| 用户 | `/api/session/verify` | GET | 校验用户身份 |
| 上传 | `/api/upload/image` | POST | 上传图片 |
| 报价 | `/api/quote/estimate` | POST | 提交报价请求 |
| 报价 | `/api/quote/result/{request_id}` | GET | 查询报价结果 |
| 工单 | `/api/quote/confirm` | POST | 确认方案生成工单 |
| 工单 | `/api/orders/{order_id}` | GET | 查询工单详情 |
| 配置 | `/api/config` | GET | 获取配置 |
| 配置 | `/api/config` | POST | 保存配置 |

### 3.2 详细接口定义

#### 3.2.1 用户会话校验

**请求**
```
GET /api/session/verify
Query: user_id, token
```

**响应**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "user_id": "user_123",
    "nickname": "张三",
    "phone": "13800138000"
  }
}
```

#### 3.2.2 图片上传

**请求**
```
POST /api/upload/image
Content-Type: multipart/form-data
Body: file (二进制)
```

**响应**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "url": "https://xxx.oss.com/images/2026/03/05/xxx.jpg"
  }
}
```

#### 3.2.3 提交报价请求

**请求**
```
POST /api/quote/estimate
Content-Type: application/json
```

```json
{
  "user_id": "user_123",
  "location_type": "bathroom",
  "building_info": {
    "floor_level": "high",
    "house_age": "5_10",
    "area_range": "50_100"
  },
  "description": "地面和墙角有渗水",
  "images": [
    "https://xxx.oss.com/images/1.jpg",
    "https://xxx.oss.com/images/2.jpg"
  ]
}
```

**响应**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "request_id": "req_123",
    "severity": "normal",
    "severity_label": "普通",
    "severity_reason": "根据图片渗水面积和水痕深浅，判断为日常使用导致的局部防水老化。",
    "plans": [
      {
        "plan_id": 1,
        "plan_code": "plan_standard_bathroom_light",
        "name": "标准局部防水修复",
        "description": "对渗水区域进行开槽、基层处理、防水涂刷2遍，并恢复表面。",
        "tags": ["标准型", "性价比高"],
        "duration": "约0.5-1天",
        "price_min": 800,
        "price_max": 1200
      },
      {
        "plan_id": 2,
        "plan_code": "plan_enhanced_bathroom_severe",
        "name": "加强型整体防水翻新",
        "description": "对整个区域进行整体防水翻新。",
        "tags": ["加强型", "更长寿命"],
        "duration": "约1-2天",
        "price_min": 1500,
        "price_max": 2200
      }
    ]
  }
}
```

#### 3.2.4 确认方案生成工单

**请求**
```
POST /api/quote/confirm
Content-Type: application/json
```

```json
{
  "request_id": "req_123",
  "plan_id": 1
}
```

**响应**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_id": "order_456",
    "order_no": "WO202603050001",
    "status": "created"
  }
}
```

#### 3.2.5 查询工单详情

**请求**
```
GET /api/orders/{order_id}
```

**响应**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_id": "order_456",
    "order_no": "WO202603050001",
    "status": "new",
    "request_id": "req_123",
    "location_type": "bathroom",
    "severity": "normal",
    "chosen_plan": {
      "plan_id": 1,
      "name": "标准局部防水修复",
      "price_min": 800,
      "price_max": 1200
    },
    "created_at": "2026-03-05 10:30:00"
  }
}
```

#### 3.2.6 获取/保存配置

**GET /api/config**

**响应**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "agent_base_url": "https://api.minimax.chat/v1",
    "agent_api_key": "sk-xxx",
    "agent_model": "minimax",
    "agent_prompt": "你是一个防水补漏专家..."
  }
}
```

**POST /api/config**

```json
{
  "agent_base_url": "https://api.minimax.chat/v1",
  "agent_api_key": "sk-xxx",
  "agent_model": "minimax",
  "agent_prompt": "你是一个防水补漏专家..."
}
```

---

## 四、核心业务逻辑

### 4.1 报价计算逻辑

```
输入: location_type, severity, floor_level, house_age, area_range

1. 根据 location_type + severity 查询适用的施工方案
2. 获取方案的 base_price_min 和 base_price_max
3. 根据楼层系数调整价格:
   - 低层: 1.0
   - 中层: 1.1
   - 高层: 1.2
4. 根据房龄系数调整价格:
   - 0-5年: 1.0
   - 5-10年: 1.2
   - 10年以上: 1.3
5. 根据面积系数调整价格:
   - <50㎡: 1.0
   - 50-100㎡: 1.3
   - >100㎡: 1.5

最终价格 = 基准价格 * 楼层系数 * 房龄系数 * 面积系数
```

### 4.2 AI 分析逻辑

```
输入: images[], location_type, description

1. 构造 Prompt:
   - 角色: 防水补漏专家
   - 任务: 分析图片判断漏水严重程度
   - 输出格式: JSON { severity, reason }
2. 调用 AI API (配置中的 base_url + key + model)
3. 解析返回结果
4. 返回 severity (light/normal/severe) + reason
```

---

## 五、前端目录结构

```
waterproof-quote-h5/
├── src/
│   ├── api/
│   │   └── quote.ts          # API 封装
│   ├── assets/
│   │   └── main.css         # 全局样式
│   ├── components/
│   │   ├── LocationPicker.vue
│   │   ├── PlanCard.vue
│   │   └── ImageUploader.vue
│   ├── router/
│   │   └── index.ts         # 路由配置
│   ├── utils/
│   │   ├── upload.ts        # 图片上传工具
│   │   └── index.ts         # 通用工具
│   ├── views/
│   │   ├── QuotePage.vue    # 报价首页
│   │   └── ResultPage.vue   # 结果页
│   ├── App.vue
│   └── main.ts
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

---

## 六、后端目录结构

```
waterproof-quote-backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── quote.py     # 报价接口
│   │   │   ├── upload.py    # 上传接口
│   │   │   ├── order.py    # 工单接口
│   │   │   └── config.py   # 配置接口
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py        # 配置管理
│   │   ├── database.py     # 数据库连接
│   │   └── security.py     # 安全模块
│   ├── models/             # SQLAlchemy 模型
│   │   ├── quote.py
│   │   ├── order.py
│   │   └── config.py
│   ├── schemas/            # Pydantic 模型
│   │   ├── quote.py
│   │   ├── order.py
│   │   └── config.py
│   ├── services/           # 业务逻辑
│   │   ├── quote_service.py
│   │   ├── order_service.py
│   │   ├── ai_service.py
│   │   └── rule_engine.py
│   ├── utils/
│   │   └── file_utils.py
│   └── main.py
├── alembic/               # 数据库迁移
├── requirements.txt
└── .env.example
```

---

## 七、部署配置

### 7.1 环境变量 (.env)

```
# 数据库
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/waterproof_quote

# 对象存储
OSS_ACCESS_KEY=xxx
OSS_SECRET_KEY=xxx
OSS_BUCKET=xxx
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com

# AI 配置 (默认)
AI_BASE_URL=https://api.minimax.chat/v1
AI_API_KEY=sk-xxx
AI_MODEL=minimax

# 服务配置
DEBUG=True
SECRET_KEY=your-secret-key
```

### 7.2 Docker 部署 (可选)

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://db:3306/waterproof_quote
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: waterproof_quote

  frontend:
    build: ./frontend
    ports:
      - "80:80"
```

---

## 八、附录

### 8.1 枚举值定义

| 枚举 | 值 | 说明 |
|------|-----|------|
| location_type | bathroom, kitchen, balcony, roof, outer_wall, bay_window, other | 漏点位置 |
| floor_level | low, mid, high | 楼层 |
| house_age | 0_5, 5_10, 10_plus | 房龄 |
| area_range | lt_50, 50_100, gt_100 | 面积段 |
| severity | light, normal, severe | 严重程度 |
| quote_status | pending, analyzed, ordered | 报价状态 |
| order_status | new, assigned, in_progress, completed, cancelled | 工单状态 |

### 8.2 变更日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0 | 2026-03-05 | 初始版本 |
