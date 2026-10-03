# 福娃内容中台系统 - API参考文档

## 概述

- **Base URL**: `http://localhost:8000`
- **API文档**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI规范**: `http://localhost:8000/openapi.json`
- **认证方式**: Bearer Token (JWT)

---

## 认证模块

### 1. 用户注册

**POST** `/api/auth/register`

**请求体**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "full_name": "string"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "string",
    "email": "string",
    "full_name": "string",
    "is_creator": false,
    "created_at": "2026-09-18T00:00:00"
  }
}
```

### 2. 用户登录

**POST** `/api/auth/login`

**请求体** (form-data):
```
username: string
password: string
```

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "is_creator": true
  }
}
```

### 3. 获取当前用户

**GET** `/api/auth/me`

**请求头**:
```
Authorization: Bearer <token>
```

**响应**:
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "full_name": "string",
  "is_creator": true,
  "created_at": "2026-09-18T00:00:00"
}
```

### 4. 初始化创建者

**POST** `/api/auth/init-creator`

**请求体**:
```json
{
  "creator_name": "string",
  "password": "string"
}
```

**响应**:
```json
{
  "success": true,
  "message": "创建者初始化成功",
  "data": {
    "creator_name": "string",
    "is_creator": true
  }
}
```

---

## 数据模块

### 选题管理

#### 获取选题列表

**GET** `/api/data/topics`

**查询参数**:
- `page` (int, 默认1): 页码
- `page_size` (int, 默认20): 每页数量
- `keyword` (str): 关键词搜索
- `status` (str): 状态筛选

**响应**:
```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}
```

#### 创建选题

**POST** `/api/data/topics`

**请求体**:
```json
{
  "title": "string",
  "description": "string",
  "category": "string",
  "tags": ["string"],
  "status": "draft",
  "priority": "medium"
}
```

#### 获取选题详情

**GET** `/api/data/topics/{item_id}`

#### 更新选题

**PUT** `/api/data/topics/{item_id}`

#### 删除选题

**DELETE** `/api/data/topics/{item_id}`

---

### 脚本管理

#### 获取脚本列表

**GET** `/api/data/scripts`

#### 创建脚本

**POST** `/api/data/scripts`

**请求体**:
```json
{
  "title": "string",
  "topic_id": 1,
  "content": "string",
  "script_type": "口播",
  "duration": 60,
  "status": "draft"
}
```

#### 获取/更新/删除脚本

- **GET** `/api/data/scripts/{item_id}`
- **PUT** `/api/data/scripts/{item_id}`
- **DELETE** `/api/data/scripts/{item_id}`

---

### 直播复盘

#### 获取直播复盘列表

**GET** `/api/data/live-reviews`

#### 创建直播复盘

**POST** `/api/data/live-reviews`

**请求体**:
```json
{
  "live_date": "2026-09-18",
  "anchor_name": "string",
  "account_name": "string",
  "platform": "抖音",
  "total_gmv": 161477.00,
  "total_orders": 781,
  "avg_order_value": 206.80,
  "peak_viewers": 150,
  "avg_watch_time": 68,
  "conversion_rate": 4.32,
  "interaction_rate": 3.99,
  "exposure_rate": 3.9,
  "remark": "string",
  "report_content": "string"
}
```

#### 获取/更新/删除直播复盘

- **GET** `/api/data/live-reviews/{item_id}`
- **PUT** `/api/data/live-reviews/{item_id}`
- **DELETE** `/api/data/live-reviews/{item_id}`

---

### 投放数据

#### 获取投放数据列表

**GET** `/api/data/ad-dashboards`

#### 创建投放数据

**POST** `/api/data/ad-dashboards`

**请求体**:
```json
{
  "date": "2026-09-18",
  "platform": "抖音",
  "account_name": "string",
  "anchor_name": "string",
  "total_cost": 10000.00,
  "total_exposure": 1000000,
  "total_clicks": 50000,
  "click_rate": 5.0,
  "conversion_count": 1000,
  "conversion_rate": 2.0,
  "roi": 3.5,
  "remark": "string"
}
```

#### 获取/更新/删除投放数据

- **GET** `/api/data/ad-dashboards/{item_id}`
- **PUT** `/api/data/ad-dashboards/{item_id}`
- **DELETE** `/api/data/ad-dashboards/{item_id}`

---

### 主播管理

#### 获取主播列表

**GET** `/api/data/anchors`

#### 创建主播

**POST** `/api/data/anchors`

**请求体**:
```json
{
  "name": "string",
  "nickname": "string",
  "platform": "抖音",
  "account_name": "string",
  "phone": "string",
  "email": "string",
  "status": "active",
  "uv_value": 100.00,
  "remark": "string"
}
```

#### 获取/更新/删除主播

- **GET** `/api/data/anchors/{item_id}`
- **PUT** `/api/data/anchors/{item_id}`
- **DELETE** `/api/data/anchors/{item_id}`

---

### 一键清空数据

**POST** `/api/data/clear-all`

**请求头**:
```
Authorization: Bearer <creator_token>
```

**请求体**:
```json
{
  "password": "creator_password"
}
```

**响应**:
```json
{
  "success": true,
  "message": "所有数据已清空"
}
```

> ⚠️ 此操作不可恢复，仅创建者可执行。

---

## 文件模块

### 上传文件

**POST** `/api/files/upload`

**Content-Type**: `multipart/form-data`

**参数**:
- `file` (file, 必填): 上传的文件
- `category` (str): 文件分类
- `description` (str): 文件描述

**响应**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "filename": "example.pdf",
    "original_name": "example.pdf",
    "file_size": 1024000,
    "file_type": "application/pdf",
    "file_path": "/uploads/example.pdf",
    "category": "文档",
    "uploaded_at": "2026-09-18T00:00:00"
  }
}
```

### 批量上传

**POST** `/api/files/batch-upload`

**Content-Type**: `multipart/form-data`

**参数**:
- `files` (files, 必填): 多个文件
- `category` (str): 文件分类

### 下载文件

**GET** `/api/files/{file_id}`

**响应**: 文件流（自动下载）

### 删除文件

**DELETE** `/api/files/{file_id}`

### 获取文件列表

**GET** `/api/files/list`

**查询参数**:
- `page` (int): 页码
- `page_size` (int): 每页数量
- `category` (str): 分类筛选
- `keyword` (str): 关键词搜索

---

## AI模块

### AI对话

**POST** `/api/ai/chat`

**请求体**:
```json
{
  "message": "string",
  "conversation_id": "string",
  "model": "deepseek"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "response": "string",
    "conversation_id": "string"
  }
}
```

### 生成脚本

**POST** `/api/ai/generate-script`

**请求体**:
```json
{
  "topic": "string",
  "script_type": "口播",
  "duration": 60,
  "style": "string",
  "reference": "string"
}
```

### 爆款视频拆解

**POST** `/api/ai/breakdown`

**请求体**:
```json
{
  "video_url": "string",
  "video_title": "string",
  "analysis_type": "full"
}
```

### 生成视频提示词

**POST** `/api/ai/generate-video-prompt`

**请求体**:
```json
{
  "description": "string",
  "style": "string",
  "duration": 5,
  "model": "seedance2.5"
}
```

### 获取AI记录列表

**GET** `/api/ai/records`

---

## 数据大屏模块

### 获取总览数据

**GET** `/api/dashboard/overview`

**查询参数**:
- `time_range` (str): `daily` / `weekly` / `monthly` / `90days`
- `start_date` (str): 开始日期
- `end_date` (str): 结束日期

**响应**:
```json
{
  "success": true,
  "data": {
    "total_gmv": {
      "value": 1000000.00,
      "platforms": {
        "抖音": 500000.00,
        "视频号": 300000.00,
        "小红书": 150000.00,
        "快手": 50000.00
      }
    },
    "total_cost": {
      "value": 100000.00,
      "platforms": {}
    },
    "content_production": {
      "materials_count": 100,
      "ai_generated_count": 50,
      "edited_count": 80,
      "published_count": 70,
      "platforms": {}
    },
    "video_exposure": {
      "total": 10000000,
      "platforms": {}
    }
  }
}
```

### 获取主播排行榜

**GET** `/api/dashboard/anchor-ranking`

**查询参数**:
- `time_range` (str): 时间范围
- `limit` (int): 返回数量，默认10

**响应**:
```json
{
  "success": true,
  "data": [
    {
      "rank": 1,
      "anchor_name": "string",
      "gmv": 500000.00,
      "uv_value": 200.00,
      "orders": 1000,
      "avg_order_value": 500.00
    }
  ]
}
```

### 获取引流视频排行榜

**GET** `/api/dashboard/traffic-videos`

**查询参数**:
- `time_range` (str): 时间范围
- `limit` (int): 返回数量，默认10

### 获取视频曝光排行榜

**GET** `/api/dashboard/exposure-videos`

**查询参数**:
- `time_range` (str): 时间范围
- `limit` (int): 返回数量，默认10

### 获取系统统计

**GET** `/api/dashboard/system-stats`

**响应**:
```json
{
  "success": true,
  "data": {
    "total_users": 100,
    "total_topics": 500,
    "total_scripts": 300,
    "total_materials": 1000,
    "total_videos": 200,
    "total_live_reviews": 50,
    "total_ad_records": 80,
    "total_files": 500,
    "storage_used": "1.2GB",
    "storage_total": "8880TB"
  }
}
```

---

## 系统端点

### 根路径

**GET** `/`

返回系统信息和API端点列表。

### 健康检查

**GET** `/health`

**响应**:
```json
{
  "status": "healthy",
  "timestamp": "2026-09-18T00:00:00",
  "version": "1.0.0"
}
```

---

## 错误响应格式

所有错误响应遵循以下格式：

```json
{
  "success": false,
  "error": "错误类型",
  "detail": "详细错误信息",
  "code": 400
}
```

### 常见错误码

| 状态码 | 说明 |
|---|---|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 422 | 验证失败 |
| 500 | 服务器内部错误 |

---

## 认证使用示例

### cURL

```bash
# 登录获取token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=123456" | jq -r .access_token)

# 使用token访问受保护接口
curl -s http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Python

```python
import requests

# 登录
response = requests.post(
    "http://localhost:8000/api/auth/login",
    data={"username": "admin", "password": "123456"}
)
token = response.json()["access_token"]

# 访问受保护接口
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/api/auth/me", headers=headers)
print(response.json())
```

### JavaScript

```javascript
// 登录
const response = await fetch("http://localhost:8000/api/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: "username=admin&password=123456"
});
const { access_token } = await response.json();

// 访问受保护接口
const userResponse = await fetch("http://localhost:8000/api/auth/me", {
  headers: { "Authorization": `Bearer ${access_token}` }
});
const user = await userResponse.json();
```

---

## 数据格式约定

### 金额
- 单位：元（人民币）
- 精度：小数点后两位
- 示例：`161477.00`

### 数量
- 单位：个
- 示例：`781`

### 百分比
- 单位：%
- 精度：小数点后两位
- 示例：`4.32`

### 日期时间
- 格式：ISO 8601
- 示例：`2026-09-18T00:00:00`

### 平台枚举
- `抖音`
- `视频号`
- `小红书`
- `快手`
