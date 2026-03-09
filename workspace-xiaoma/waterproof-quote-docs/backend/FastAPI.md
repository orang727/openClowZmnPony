# 防水补漏智能报价器 - 后端 FastAPI 接口代码

## 项目结构

```
waterproof-quote-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 入口
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   ├── models/                 # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── quote.py
│   │   ├── order.py
│   │   └── config.py
│   ├── schemas/                # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── quote.py
│   │   ├── order.py
│   │   └── config.py
│   ├── api/                    # API 路由
│   │   ├── __init__.py
│   │   ├── quote.py
│   │   ├── upload.py
│   │   ├── order.py
│   │   └── config.py
│   └── services/               # 业务逻辑
│       ├── __init__.py
│       ├── quote_service.py
│       ├── order_service.py
│       ├── ai_service.py
│       └── rule_engine.py
├── requirements.txt
└── .env
```

---

## 1. 入口文件 main.py

```python
"""
防水补漏智能报价器 - FastAPI 入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import quote, upload, order, config
from app.database import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="防水补漏智能报价API",
    description="防水补漏智能报价后端服务",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(quote.router, prefix="/api", tags=["报价"])
app.include_router(upload.router, prefix="/api", tags=["上传"])
app.include_router(order.router, prefix="/api", tags=["工单"])
app.include_router(config.router, prefix="/api", tags=["配置"])

@app.get("/")
def root():
    return {"message": "防水补漏智能报价API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

---

## 2. 配置管理 config.py

```python
"""
配置管理
"""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # 数据库
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/waterproof_quote"
    
    # 对象存储
    OSS_ACCESS_KEY: str = ""
    OSS_SECRET_KEY: str = ""
    OSS_BUCKET: str = ""
    OSS_ENDPOINT: str = ""
    
    # AI 配置
    AI_BASE_URL: str = "https://api.minimax.chat/v1"
    AI_API_KEY: str = ""
    AI_MODEL: str = "minimax"
    
    # 服务配置
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
```

---

## 3. 数据库连接 database.py

```python
"""
数据库连接
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 4. 数据模型 models/quote.py

```python
"""
报价请求模型
"""
from sqlalchemy import Column, BigInteger, String, Text, JSON, DateTime, DECIMAL
from sqlalchemy.sql import func
from app.database import Base

class QuoteRequest(Base):
    """报价请求表"""
    __tablename__ = "quote_requests"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(String(64), nullable=False, index=True, comment="用户ID")
    location_type = Column(String(32), nullable=False, comment="漏点位置")
    floor_level = Column(String(16), nullable=True, comment="楼层")
    house_age = Column(String(16), nullable=True, comment="房龄")
    area_range = Column(String(16), nullable=True, comment="面积段")
    description = Column(Text, nullable=True, comment="问题描述")
    images = Column(JSON, nullable=True, comment="图片URL数组")
    severity = Column(String(16), nullable=True, comment="严重程度: light/normal/severe")
    severity_reason = Column(Text, nullable=True, comment="AI分析说明")
    status = Column(String(16), default="pending", comment="状态: pending/analyzed/ordered")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
```

---

## 5. 数据模型 models/order.py

```python
"""
工单模型
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, DECIMAL, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Order(Base):
    """工单表"""
    __tablename__ = "orders"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_no = Column(String(32), unique=True, nullable=False, comment="工单编号")
    request_id = Column(BigInteger, nullable=False, index=True, comment="报价请求ID")
    user_id = Column(String(64), nullable=False, index=True, comment="用户ID")
    chosen_plan_id = Column(BigInteger, nullable=False, comment="选择的方案ID")
    final_price_min = Column(DECIMAL(10, 2), nullable=True, comment="最终报价下限")
    final_price_max = Column(DECIMAL(10, 2), nullable=True, comment="最终报价上限")
    status = Column(String(16), default="new", comment="状态: new/assigned/in_progress/completed/cancelled")
    remark = Column(Text, nullable=True, comment="备注")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

---

## 6. Pydantic 模型 schemas/quote.py

```python
"""
报价请求/响应模型
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BuildingInfo(BaseModel):
    """建筑信息"""
    floor_level: Optional[str] = None
    house_age: Optional[str] = None
    area_range: Optional[str] = None

class QuoteRequest(BaseModel):
    """报价请求"""
    user_id: str = "anonymous"
    location_type: str
    building_info: Optional[BuildingInfo] = None
    description: Optional[str] = None
    images: List[str]

class Plan(BaseModel):
    """施工方案"""
    plan_id: int
    plan_code: str
    name: str
    description: str
    tags: List[str]
    duration: str
    price_min: float
    price_max: float

class QuoteResponse(BaseModel):
    """报价响应"""
    request_id: str
    severity: str
    severity_label: str
    severity_reason: str
    plans: List[Plan]

class ConfirmRequest(BaseModel):
    """确认方案请求"""
    request_id: str
    plan_id: int

class ConfirmResponse(BaseModel):
    """确认方案响应"""
    order_id: str
    order_no: str
    status: str
```

---

## 7. AI 服务 services/ai_service.py

```python
"""
AI 图像分析服务
"""
import json
import requests
from typing import Dict, Any
from app.config import settings

class AIService:
    """AI 分析服务"""
    
    def __init__(self):
        self.base_url = settings.AI_BASE_URL
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL
    
    def analyze_severity(
        self, 
        images: List[str], 
        location_type: str, 
        description: str = ""
    ) -> Dict[str, Any]:
        """
        分析图片，返回严重程度
        
        Args:
            images: 图片URL列表
            location_type: 漏点位置
            description: 用户描述
            
        Returns:
            {
                "severity": "light|normal|severe",
                "reason": "分析说明"
            }
        """
        # 构造 Prompt
        prompt = self._build_prompt(location_type, description)
        
        # 调用 AI API（这里以 OpenAI 格式为例）
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一个专业的防水补漏专家，请根据用户提供的图片和分析信息，判断漏水严重程度。"
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                *[
                                    {"type": "image_url", "image_url": {"url": img}}
                                    for img in images[:3]  # 最多3张
                                ]
                            ]
                        }
                    ],
                    "max_tokens": 500
                },
                timeout=30
            )
            
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # 解析返回结果
            return self._parse_response(content)
            
        except Exception as e:
            # AI 调用失败，返回默认结果
            return {
                "severity": "normal",
                "reason": "AI分析暂时不可用，返回默认评估结果"
            }
    
    def _build_prompt(self, location_type: str, description: str) -> str:
        """构造提示词"""
        location_map = {
            "bathroom": "卫生间",
            "kitchen": "厨房",
            "balcony": "阳台",
            "roof": "屋顶",
            "outer_wall": "外墙",
            "bay_window": "飘窗",
            "other": "其他位置"
        }
        location = location_map.get(location_type, location_type)
        
        prompt = f"""请分析以下防水补漏情况：
- 漏点位置：{location}
- 用户描述：{description or "无"}

请根据图片判断漏水严重程度，只返回以下JSON格式：
{{"severity": "light" 或 "normal" 或 "severe", "reason": "简短说明"}}

light: 轻微（局部渗水，面积小）
normal: 普通（有一定渗水范围）
severe: 严重（大面积渗水、滴水、结构受损）"""
        return prompt
    
    def _parse_response(self, content: str) -> Dict[str, Any]:
        """解析 AI 返回内容"""
        try:
            # 尝试提取 JSON
            data = json.loads(content)
            return {
                "severity": data.get("severity", "normal"),
                "reason": data.get("reason", "根据图片分析得出")
            }
        except:
            # 解析失败，尝试正则匹配
            import re
            severity_match = re.search(r'"severity"\s*:\s*"(\w+)"', content)
            reason_match = re.search(r'"reason"\s*:\s*"([^"]+)"', content)
            
            severity = severity_match.group(1) if severity_match else "normal"
            reason = reason_match.group(1) if reason_match else "根据图片分析得出"
            
            return {"severity": severity, "reason": reason}

# 导出单例
ai_service = AIService()
```

---

## 8. 规则引擎 services/rule_engine.py

```python
"""
规则引擎 - 报价计算
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.quote import QuoteRequest
from app.models.order import ConstructionPlan

class RuleEngine:
    """规则引擎"""
    
    # 价格系数
    FLOOR_MULTIPLIERS = {
        "low": 1.0,
        "mid": 1.1,
        "high": 1.2
    }
    
    HOUSE_AGE_MULTIPLIERS = {
        "0_5": 1.0,
        "5_10": 1.2,
        "10_plus": 1.3
    }
    
    AREA_MULTIPLIERS = {
        "lt_50": 1.0,
        "50_100": 1.3,
        "gt_100": 1.5
    }
    
    def match_plans(
        self,
        db: Session,
        location_type: str,
        severity: str,
        floor_level: str = None,
        house_age: str = None,
        area_range: str = None
    ) -> List[Dict[str, Any]]:
        """
        匹配施工方案
        
        Args:
            db: 数据库会话
            location_type: 漏点位置
            severity: 严重程度
            floor_level: 楼层
            house_age: 房龄
            area_range: 面积段
            
        Returns:
            方案列表（含计算后的价格）
        """
        # 查询适用的方案
        plans = db.query(ConstructionPlan).filter(
            ConstructionPlan.is_active == 1
        ).all()
        
        # 过滤适用方案
        matched = []
        for plan in plans:
            # 检查位置是否适用
            location_types = plan.location_types or []
            if location_type not in location_types and "*" not in location_types:
                continue
            
            # 检查严重程度是否适用
            severity_levels = plan.severity_levels or []
            if severity not in severity_levels and "*" not in severity_levels:
                continue
            
            # 计算价格
            price_min = float(plan.base_price_min or 0)
            price_max = float(plan.base_price_max or 0)
            
            # 应用系数
            multiplier = self._calculate_multiplier(floor_level, house_age, area_range)
            price_min = round(price_min * multiplier)
            price_max = round(price_max * multiplier)
            
            matched.append({
                "plan_id": plan.id,
                "plan_code": plan.plan_code,
                "name": plan.name,
                "description": plan.description,
                "tags": plan.tags or [],
                "duration": plan.duration,
                "price_min": price_min,
                "price_max": price_max
            })
        
        # 按价格排序
        matched.sort(key=lambda x: x["price_min"])
        
        return matched[:3]  # 最多返回3个方案
    
    def _calculate_multiplier(
        self, 
        floor_level: str = None, 
        house_age: str = None, 
        area_range: str = None
    ) -> float:
        """计算价格系数"""
        multiplier = 1.0
        
        if floor_level:
            multiplier *= self.FLOOR_MULTIPLIERS.get(floor_level, 1.0)
        
        if house_age:
            multiplier *= self.HOUSE_AGE_MULTIPLIERS.get(house_age, 1.0)
        
        if area_range:
            multiplier *= self.AREA_MULTIPLIERS.get(area_range, 1.0)
        
        return multiplier

# 导出单例
rule_engine = RuleEngine()
```

---

## 9. 报价服务 services/quote_service.py

```python
"""
报价服务
"""
import uuid
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.quote import QuoteRequest
from app.services.ai_service import ai_service
from app.services.rule_engine import rule_engine

class QuoteService:
    """报价服务"""
    
    SEVERITY_LABELS = {
        "light": "轻微",
        "normal": "普通",
        "severe": "严重"
    }
    
    def create_quote(
        self,
        db: Session,
        user_id: str,
        location_type: str,
        building_info: Dict[str, Any],
        description: str,
        images: list
    ) -> Dict[str, Any]:
        """
        创建报价
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            location_type: 漏点位置
            building_info: 建筑信息
            description: 问题描述
            images: 图片列表
            
        Returns:
            报价结果
        """
        # 生成请求ID
        request_id = f"req_{uuid.uuid4().hex[:12]}"
        
        # 保存报价请求
        quote_request = QuoteRequest(
            user_id=user_id,
            location_type=location_type,
            floor_level=building_info.get("floor_level"),
            house_age=building_info.get("house_age"),
            area_range=building_info.get("area_range"),
            description=description,
            images=images,
            status="pending"
        )
        db.add(quote_request)
        db.commit()
        db.refresh(quote_request)
        
        # 调用 AI 分析严重程度
        ai_result = ai_service.analyze_severity(
            images=images,
            location_type=location_type,
            description=description
        )
        
        severity = ai_result["severity"]
        severity_reason = ai_result["reason"]
        
        # 更新报价请求
        quote_request.severity = severity
        quote_request.severity_reason = severity_reason
        quote_request.status = "analyzed"
        db.commit()
        
        # 匹配施工方案
        plans = rule_engine.match_plans(
            db=db,
            location_type=location_type,
            severity=severity,
            floor_level=building_info.get("floor_level"),
            house_age=building_info.get("house_age"),
            area_range=building_info.get("area_range")
        )
        
        return {
            "request_id": request_id,
            "severity": severity,
            "severity_label": self.SEVERITY_LABELS.get(severity, "普通"),
            "severity_reason": severity_reason,
            "plans": plans
        }

# 导出单例
quote_service = QuoteService()
```

---

## 10. API 路由 api/quote.py

```python
"""
报价接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.quote import QuoteRequest, QuoteResponse, ConfirmRequest, ConfirmResponse
from app.services.quote_service import quote_service
from app.services.order_service import order_service

router = APIRouter()

@router.post("/quote/estimate", response_model=QuoteResponse)
def estimate_quote(
    request: QuoteRequest,
    db: Session = Depends(get_db)
):
    """
    提交报价请求，返回严重程度和方案
    """
    result = quote_service.create_quote(
        db=db,
        user_id=request.user_id,
        location_type=request.location_type,
        building_info=request.building_info.dict() if request.building_info else {},
        description=request.description or "",
        images=request.images
    )
    
    return result

@router.get("/quote/result/{request_id}", response_model=QuoteResponse)
def get_quote_result(
    request_id: str,
    db: Session = Depends(get_db)
):
    """
    查询报价结果
    """
    # TODO: 从数据库查询已有结果
    raise HTTPException(status_code=404, detail="Not implemented")

@router.post("/quote/confirm", response_model=ConfirmResponse)
def confirm_quote(
    request: ConfirmRequest,
    db: Session = Depends(get_db)
):
    """
    确认方案，生成工单
    """
    result = order_service.create_order(
        db=db,
        request_id=request.request_id,
        plan_id=request.plan_id
    )
    
    return result
```

---

## 11. API 路由 api/upload.py

```python
"""
上传接口
"""
import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.config import settings

router = APIRouter()

# 本地存储目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片
    """
    # 验证文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")
    
    # 验证文件大小 (8MB)
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    
    if size > 8 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 8MB)")
    
    # 生成文件名
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    # 保存文件
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    
    # 返回 URL（实际项目中应该是 OSS/COS 的 URL）
    url = f"/uploads/{filename}"
    
    return {"url": url}
```

---

## 12. API 路由 api/order.py

```python
"""
工单接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderResponse
from app.services.order_service import order_service

router = APIRouter()

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    """
    查询工单详情
    """
    order = order_service.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order
```

---

## 13. 依赖安装 requirements.txt

```
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.25
pymysql==1.1.0
python-multipart==0.0.6
pydantic==2.5.3
pydantic-settings==2.1.0
requests==2.31.0
python-dotenv==1.0.0
```

---

## 14. 启动服务

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后，访问 `http://localhost:8000/docs` 可查看 API 文档。
