---
name: youguo-content-hub
description: "福娃内容中台系统——一站式内容生产全流程管理平台。覆盖选题、脚本创作、对标拆解、拍摄素材、成片管理、AI视频生成、直播复盘、投放端、主播管理、数据大屏等32+业务板块。前端采用纯HTML+IndexedDB（黑金科技风+紫色科技风数据大屏），后端采用FastAPI+SQLAlchemy+SQLite/PostgreSQL。支持本地部署、Docker容器化、云平台部署，兼容手机/电脑自适应。适用于内容团队、MCN机构、品牌自播、短视频运营等场景。"
---

# 福娃内容中台系统

## 概述

福娃内容中台系统是一套覆盖内容生产全流程的可交互Web应用，对标云视频管家等行业标杆产品，集成151+专业Skill，提供从选题到发布、从数据到复盘的一站式解决方案。

## 核心能力

### 🎯 32+业务板块

| 分类 | 板块 |
|---|---|
| **内容生产** | 选题管理、脚本创作、对标拆解脚本、对标视频拆解、对标视频库 |
| **素材管理** | 拍摄素材库、成片库、成片视频拆解分析 |
| **AI创作** | AI视频生成、AI视频提示词专业版、即梦提示词工坊、人物九视图、AI-Vlog编导 |
| **直播运营** | 主播管理中心、直播复盘、直播排班、主播GMV排行榜 |
| **投放管理** | 投放端、引流视频排行榜、广告消耗分析 |
| **数据中心** | 业务中控大屏、账号数据复盘、内容生产总览 |
| **协作管理** | SOP协作中心、账号内容自动发布、智能分析中心 |
| **系统管理** | 技能中心、行业对标中心、创建者授权管理、系统设置 |

### 📊 数据大屏特性

- **总GMV**：中心圆形仪表盘 + 5平台环绕（抖音/视频号/小红书/快手/TikTok）
- **总消耗**：千川消耗汇总 + 8大投放渠道细分
- **内容生产**：拍摄素材/AI生成/视频剪辑/视频发布/发布平台 5指标环绕
- **主播排行榜**：Top10主播，金/银/铜徽章，GMV进度条，UV参考排序
- **引流视频排行榜**：Top10引流视频，按消耗降序
- **视频曝光排行榜**：Top10视频，按曝光量降序
- **时间维度**：每日/每周/每月/90天切换
- **自动刷新**：每30秒自动汇总所有板块数据

### 🤖 AI能力集成

- **爆款深度拆解v2.0**：十维诊断系统（基础四关B1-B4 + 进阶六关A1-A6）
- **奇点选题宇宙**：内容元宇宙方法论，三层金字塔（原子×母版×奇点）
- **即梦2.5九维控场**：五大提示词公式、九个控场维度、11种转场技巧
- **人物九视图**：3×3网格角色设定，七件套角色设定
- **AI-Vlog编导**：6种Vlog类型，分镜脚本自动生成

### 🌐 全平台支持（5大内容平台 + 8大投放渠道）

**内容平台（5大）**：
- 抖音 / 小红书 / 视频号 / 快手 / TikTok

**投放渠道（8大）**：
- 巨量千川（抖音）
- 磁力金牛（快手）
- 腾讯ADQ（视频号）
- 微信豆（视频号）
- 薯条（小红书）
- 聚光（小红书）
- 磁力智投（快手）
- TikTok Ads（海外）

---

### ☁️ 云端数据同步

- **21个存储模块**完整同步（文件/选题/脚本/素材/成片/AI生成/发布/直播/投放等）
- **跨设备数据共享**：手机、电脑、平板登录同一账号即可同步
- **用户数据隔离**：每个用户只能看到和同步自己账号的数据
- **自动备份**：云端数据自动备份，防止数据丢失

---

### 🔐 权限管理

- **创建者授权机制**：首次使用设置创建者密码
- **数据清零权限**：仅创建者可执行一键清零
- **密码验证**：敏感操作需输入创建者密码
- **数据安全**：所有数据本地存储，支持导出备份

## 技术栈

### 前端
- **框架**：纯HTML + 原生JavaScript（无框架依赖）
- **存储**：IndexedDB（浏览器本地数据库）
- **样式**：CSS3（黑金科技风 + 紫色科技风数据大屏）
- **响应式**：手机/平板/电脑自适应
- **文件大小**：约666KB（单文件自包含）

### 后端
- **Web框架**：FastAPI 0.104.1
- **ASGI服务器**：Uvicorn 0.24.0
- **ORM**：SQLAlchemy 2.0.23
- **数据验证**：Pydantic 2.5.2
- **认证**：JWT + bcrypt
- **数据库**：SQLite（默认）/ MySQL / PostgreSQL
- **API端点**：32个（RESTful风格）
- **API文档**：Swagger UI（自动生成）

## 快速开始

### 方式一：纯前端运行（推荐，零配置）

```bash
# 1. 进入前端目录
cd assets

# 2. 启动本地HTTP服务器
python3 -m http.server 8080

# 3. 浏览器访问
open http://localhost:8080/index.html
```

或直接用浏览器打开 `assets/index.html` 文件。

### 方式二：前后端完整部署

```bash
# 1. 启动后端服务
cd backend
pip install -r requirements.txt
python main.py
# 后端运行在 http://localhost:8000

# 2. 启动前端
cd ../assets
python3 -m http.server 8080
# 前端运行在 http://localhost:8080

# 3. API文档访问
open http://localhost:8000/docs
```

### 方式三：Docker部署

```bash
# 构建后端镜像
cd backend
docker build -t youguo-backend .

# 运行后端容器
docker run -d \
  --name youguo-backend \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/uploads:/app/uploads \
  youguo-backend

# 前端使用Nginx托管
docker run -d \
  --name youguo-frontend \
  -p 8080:80 \
  -v $(pwd)/../assets:/usr/share/nginx/html \
  nginx:alpine
```

## 目录结构

```
youguo-content-hub/
├── SKILL.md                    # 本文件
├── README.md                   # 项目说明
├── assets/                     # 前端应用
│   └── index.html              # 单文件应用（666KB）
├── backend/                    # 后端服务
│   ├── main.py                 # FastAPI主入口
│   ├── requirements.txt        # Python依赖
│   ├── app/
│   │   ├── api/                # API路由（auth/data/files/ai/dashboard）
│   │   ├── core/               # 核心配置（config/database）
│   │   ├── models/             # 数据模型（12张表）
│   │   └── services/           # 业务服务（auth_service）
│   ├── data/                   # 数据库文件目录
│   └── uploads/                # 文件上传目录
├── references/                 # 参考文档
│   ├── deployment-guide.md     # 部署指南
│   ├── api-reference.md        # API参考文档
│   └── user-manual.md          # 用户手册
└── scripts/                    # 工具脚本
    ├── install.sh              # 一键安装脚本
    ├── start.sh                # 启动脚本
    ├── stop.sh                 # 停止脚本
    └── backup.sh               # 数据备份脚本
```

## API模块说明

### 认证模块（/api/auth）
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户
- `POST /api/auth/init-creator` - 初始化创建者

### 数据模块（/api/data）
- 选题管理（topics）
- 脚本管理（scripts）
- 直播复盘（live-reviews）
- 投放数据（ad-dashboards）
- 主播管理（anchors）
- 一键清空数据（clear-all，需创建者授权）

### 文件模块（/api/files）
- 文件上传（支持37+格式）
- 批量上传
- 文件下载
- 文件删除
- 文件列表

### AI模块（/api/ai）
- AI对话
- 生成脚本
- 爆款视频拆解
- 生成视频提示词
- AI记录列表

### 数据大屏模块（/api/dashboard）
- 总览数据（总GMV/总消耗/内容生产/视频曝光）
- 主播GMV排行榜
- 引流视频排行榜
- 视频曝光排行榜
- 系统统计

## 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|---|---|---|
| `APP_NAME` | 福娃内容中台系统 | 应用名称 |
| `APP_VERSION` | 1.0.0 | 应用版本 |
| `HOST` | 0.0.0.0 | 监听地址 |
| `PORT` | 8000 | 监听端口 |
| `DEBUG` | True | 调试模式 |
| `DATABASE_URL` | sqlite:///./data/content_hub.db | 数据库连接 |
| `SECRET_KEY` | your-secret-key-change-me | JWT密钥 |
| `UPLOAD_DIR` | ./uploads | 上传目录 |
| `MAX_UPLOAD_SIZE` | 8880TB | 最大上传大小 |
| `CORS_ORIGINS` | ["*"] | 允许的跨域来源 |

### 前端配置

前端应用无需配置，打开即可使用。所有数据存储在浏览器IndexedDB中。

如需对接后端API，在系统设置中配置后端地址。

## 数据备份与恢复

### 备份

```bash
# 备份前端数据（浏览器导出）
# 在应用中：设置 → 数据管理 → 导出数据

# 备份后端数据库
cp backend/data/content_hub.db backup/content_hub_$(date +%Y%m%d).db

# 备份上传文件
tar -czf backup/uploads_$(date +%Y%m%d).tar.gz backend/uploads/
```

### 恢复

```bash
# 恢复前端数据（浏览器导入）
# 在应用中：设置 → 数据管理 → 导入数据

# 恢复后端数据库
cp backup/content_hub_20260101.db backend/data/content_hub.db

# 恢复上传文件
tar -xzf backup/uploads_20260101.tar.gz -C backend/
```

## 常见问题

### Q: 前端和后端有什么区别？
A: 前端是纯HTML应用，所有数据存储在浏览器本地，无需后端即可使用。后端提供API服务和数据库持久化，适合多用户协作和数据集中管理。

### Q: 支持哪些文件格式上传？
A: 支持37+种格式，包括文档（doc/docx/pdf/txt/md）、表格（xls/xlsx/csv）、图片（jpg/png/gif/webp/svg）、视频（mp4/mov/avi/mkv）、音频（mp3/wav/flac）、压缩包（zip/rar/7z）等。

### Q: 数据存储在哪里？
A: 前端模式下数据存储在浏览器IndexedDB中，清除浏览器数据会丢失。后端模式下数据存储在SQLite/PostgreSQL数据库中。

### Q: 如何重置所有数据？
A: 在系统设置中点击"一键清零所有数据"，需要输入创建者密码验证。此操作不可恢复，请先备份数据。

### Q: 支持多人协作吗？
A: 纯前端模式不支持多人协作（数据存储在各自浏览器）。部署后端服务后支持多用户注册登录和数据共享。

## 云平台部署

支持部署到以下平台，详细步骤请参考 `references/deployment-guide.md`：

- **Vercel** - 前端+Serverless API
- **Railway** - 全栈应用+数据库
- **Render** - 全栈应用（有免费套餐）
- **Fly.io** - Docker容器（有香港节点）
- **DigitalOcean** - VM/App Platform（有新加坡节点）
- **阿里云函数计算** - Serverless（国内访问快）
- **AWS Elastic Beanstalk** - 企业级PaaS
- **Azure App Service** - 企业级PaaS

## 版本历史

### v1.0.0 (2026-09-18)
- ✅ 32+业务板块完整实现
- ✅ 黑金科技风+紫色科技风数据大屏
- ✅ 151+专业Skill集成
- ✅ 前后端分离架构
- ✅ 创建者授权管理
- ✅ 手机/电脑自适应
- ✅ 37+文件格式支持
- ✅ 8880TB存储配置
- ✅ 数据自动汇总机制

## 许可证

MIT License

## 联系方式

- 项目地址：GitHub（见仓库链接）
- 问题反馈：GitHub Issues
- 技术支持：社区讨论
