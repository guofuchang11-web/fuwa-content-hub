# 福娃内容中台系统

> 一站式内容生产全流程管理平台 | 对标云视频管家 | 32+业务板块 | 151+专业Skill

![Version](https://img.shields.io/badge/version-1.0.0-gold)
![License](https://img.shields.io/badge/license-MIT-blue)
![Frontend](https://img.shields.io/badge/frontend-HTML%2BJS-orange)
![Backend](https://img.shields.io/badge/backend-FastAPI-green)
![Storage](https://img.shields.io/badge/storage-8880TB-purple)

## ✨ 系统特性

### 🎯 32+业务板块
- **内容生产**：选题、脚本、对标拆解、拍摄素材、成片管理
- **AI创作**：AI视频生成、即梦提示词工坊、人物九视图、AI-Vlog编导
- **直播运营**：主播管理、直播复盘、直播排班、GMV排行榜
- **投放管理**：投放端、引流视频排行、广告消耗分析
- **数据中心**：业务中控大屏、账号数据复盘、内容生产总览
- **协作管理**：SOP协作、自动发布、智能分析中心

### 📊 智能数据大屏
- 总GMV：中心圆形仪表盘 + 4平台环绕
- 总消耗：千川消耗汇总 + 平台细分
- 内容生产：5指标环绕（素材/生成/剪辑/发布/平台）
- 主播排行榜：Top10，金/银/铜徽章，UV参考排序
- 引流视频排行榜：Top10，按消耗降序
- 视频曝光排行榜：Top10，按曝光量降序
- 时间维度：每日/每周/每月/90天
- 自动刷新：每30秒自动汇总

### 🤖 AI能力集成
- 爆款深度拆解v2.0（十维诊断系统）
- 奇点选题宇宙（内容元宇宙方法论）
- 即梦2.5九维控场（五大公式+11种转场）
- 人物九视图（3×3网格角色设定）
- AI-Vlog编导（6种Vlog类型）

### 🔐 权限管理
- 创建者授权机制
- 数据清零仅创建者可执行
- 密码验证敏感操作
- 数据本地存储，支持导出备份

## 🚀 快速开始

### 方式一：纯前端运行（零配置）

```bash
# 直接用浏览器打开
open assets/index.html

# 或启动本地服务器
cd assets && python3 -m http.server 8080
# 访问 http://localhost:8080
```

### 方式二：前后端完整部署

```bash
# 一键安装
bash scripts/install.sh

# 启动服务
bash scripts/start.sh

# 访问
# 前端: http://localhost:8080
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/docs
```

### 方式三：Docker部署

```bash
# 后端
cd backend
docker build -t youguo-backend .
docker run -d -p 8000:8000 -v $(pwd)/data:/app/data youguo-backend

# 前端
docker run -d -p 8080:80 -v $(pwd)/assets:/usr/share/nginx/html nginx:alpine
```

## 📁 项目结构

```
youguo-content-hub/
├── SKILL.md                    # Skill说明文档
├── README.md                   # 项目说明（本文件）
├── assets/                     # 前端应用
│   └── index.html              # 单文件应用（666KB）
├── backend/                    # 后端服务
│   ├── main.py                 # FastAPI主入口
│   ├── requirements.txt        # Python依赖
│   ├── Dockerfile              # Docker配置
│   ├── app/
│   │   ├── api/                # API路由（5个模块）
│   │   ├── core/               # 核心配置
│   │   ├── models/             # 数据模型（12张表）
│   │   └── services/           # 业务服务
│   ├── data/                   # 数据库目录
│   └── uploads/                # 上传文件目录
├── references/                 # 参考文档
│   ├── deployment-guide.md     # 部署指南
│   ├── api-reference.md        # API参考
│   └── user-manual.md          # 用户手册
└── scripts/                    # 工具脚本
    ├── install.sh              # 一键安装
    ├── start.sh                # 启动服务
    ├── stop.sh                 # 停止服务
    └── backup.sh               # 数据备份
```

## 🛠️ 技术栈

| 层级 | 技术 | 版本 |
|---|---|---|
| 前端 | HTML + 原生JavaScript | - |
| 前端存储 | IndexedDB | - |
| 后端框架 | FastAPI | 0.104.1 |
| ASGI服务器 | Uvicorn | 0.24.0 |
| ORM | SQLAlchemy | 2.0.23 |
| 数据验证 | Pydantic | 2.5.2 |
| 认证 | JWT + bcrypt | - |
| 数据库 | SQLite / MySQL / PostgreSQL | - |

## 📡 API模块

| 模块 | 端点前缀 | 功能 |
|---|---|---|
| 认证 | `/api/auth` | 注册、登录、用户信息、创建者初始化 |
| 数据 | `/api/data` | 选题、脚本、直播复盘、投放数据、主播管理 |
| 文件 | `/api/files` | 上传、下载、删除、列表（37+格式） |
| AI | `/api/ai` | 对话、生成脚本、爆款拆解、视频提示词 |
| 数据大屏 | `/api/dashboard` | 总览、主播排行、引流视频、曝光视频 |

共 **32个API端点**，完整RESTful风格，自动生成Swagger文档。

## 🎨 界面风格

- **主应用**：黑金科技风（#0F0F0F背景 + #D4AF37金色点缀）
- **数据大屏**：紫色科技风（#0A0E27背景 + #7C3AED紫色点缀）
- **响应式**：手机/平板/电脑自适应
- **交互动画**：悬停效果、过渡动画、加载状态

## 💾 数据备份

```bash
# 一键备份
bash scripts/backup.sh

# 手动备份数据库
cp backend/data/content_hub.db backup.db

# 前端数据导出
# 应用内：设置 → 数据管理 → 导出数据
```

## 🌐 云平台部署

支持部署到以下平台：

- [Vercel](https://vercel.com) - 前端+Serverless
- [Railway](https://railway.app) - 全栈+数据库
- [Render](https://render.com) - 全栈（免费套餐）
- [Fly.io](https://fly.io) - Docker（香港节点）
- [DigitalOcean](https://digitalocean.com) - VM/App Platform
- [阿里云函数计算](https://www.aliyun.com/product/fc) - Serverless
- [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk) - 企业级PaaS
- [Azure App Service](https://azure.microsoft.com) - 企业级PaaS

详细部署步骤请参考 `references/deployment-guide.md`。

## 📝 更新日志

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
- ✅ Docker容器化支持
- ✅ 一键安装/启动/备份脚本

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系方式

- 项目地址：GitHub
- 问题反馈：GitHub Issues
