# 福娃内容中台系统 - 部署指南

## 目录

1. [本地部署](#本地部署)
2. [Docker部署](#docker部署)
3. [云平台部署](#云平台部署)
4. [数据库配置](#数据库配置)
5. [Nginx反向代理](#nginx反向代理)
6. [HTTPS配置](#https配置)
7. [性能优化](#性能优化)
8. [监控与日志](#监控与日志)

---

## 本地部署

### 前置要求

- Python 3.8+
- pip3
- 现代浏览器（Chrome/Firefox/Safari/Edge）

### 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd youguo-content-hub

# 2. 一键安装
bash scripts/install.sh

# 3. 启动服务
bash scripts/start.sh

# 4. 访问应用
# 前端: http://localhost:8080
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/docs
```

### 手动安装

```bash
# 后端
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# 前端（另开终端）
cd assets
python3 -m http.server 8080
```

---

## Docker部署

### 后端Docker部署

```bash
cd backend

# 构建镜像
docker build -t youguo-backend:latest .

# 运行容器
docker run -d \
  --name youguo-backend \
  --restart always \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/uploads:/app/uploads \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=sqlite:///./data/content_hub.db \
  youguo-backend:latest

# 查看日志
docker logs -f youguo-backend

# 健康检查
curl http://localhost:8000/health
```

### 前端Docker部署

```bash
# 使用Nginx托管前端
docker run -d \
  --name youguo-frontend \
  --restart always \
  -p 8080:80 \
  -v $(pwd)/assets:/usr/share/nginx/html:ro \
  nginx:alpine
```

### Docker Compose（推荐）

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: youguo-backend
    restart: always
    ports:
      - "8000:8000"
    volumes:
      - ./backend/data:/app/data
      - ./backend/uploads:/app/uploads
    environment:
      - SECRET_KEY=change-me-in-production
      - DATABASE_URL=sqlite:///./data/content_hub.db
      - DEBUG=False
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    image: nginx:alpine
    container_name: youguo-frontend
    restart: always
    ports:
      - "8080:80"
    volumes:
      - ./assets:/usr/share/nginx/html:ro
    depends_on:
      - backend

  postgres:
    image: postgres:15-alpine
    container_name: youguo-postgres
    restart: always
    environment:
      POSTGRES_DB: youguo
      POSTGRES_USER: youguo
      POSTGRES_PASSWORD: change-me
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

启动：

```bash
docker-compose up -d
```

---

## 云平台部署

### 1. Render（推荐，有免费套餐）

1. 注册 [Render](https://render.com) 账号
2. 点击 "New +" → "Web Service"
3. 连接GitHub仓库
4. 配置：
   - Runtime: Python
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python main.py`
5. 添加环境变量
6. 点击 Create

### 2. Railway

1. 注册 [Railway](https://railway.app) 账号
2. 安装CLI：`npm i -g @railway/cli`
3. 登录：`railway login`
4. 初始化：`railway init`
5. 添加PostgreSQL数据库：`railway add`
6. 部署：`railway up`

### 3. Fly.io（推荐，有香港节点）

1. 注册 [Fly.io](https://fly.io) 账号
2. 安装CLI：`curl -L https://fly.io/install.sh | sh`
3. 登录：`fly auth login`
4. 进入backend目录：`cd backend`
5. 初始化：`fly launch`
6. 选择区域：`hkg`（香港）
7. 部署：`fly deploy`

### 4. Vercel（前端）

1. 注册 [Vercel](https://vercel.com) 账号
2. 安装CLI：`npm i -g vercel`
3. 登录：`vercel login`
4. 部署：`cd assets && vercel --prod`

### 5. 阿里云函数计算（国内推荐）

1. 注册阿里云账号并开通函数计算
2. 安装Serverless Devs：`npm install @serverless-devs/s -g`
3. 配置账号：`s config add`
4. 初始化：`s init start-fc3-python -d my-fc`
5. 部署：`cd my-fc && s deploy`

---

## 数据库配置

### SQLite（默认，无需配置）

```python
DATABASE_URL = "sqlite:///./data/content_hub.db"
```

### PostgreSQL

```bash
# 安装依赖
pip install psycopg2-binary

# 设置环境变量
export DATABASE_URL="postgresql://user:password@localhost:5432/youguo"
```

### MySQL

```bash
# 安装依赖
pip install pymysql

# 设置环境变量
export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/youguo"
```

---

## Nginx反向代理

### 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        root /path/to/youguo-content-hub/assets;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API文档
    location /docs {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }

    # 健康检查
    location /health {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

---

## HTTPS配置

### 使用Let's Encrypt（免费）

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期（已内置）
sudo certbot renew --dry-run
```

### 使用Cloudflare

1. 注册Cloudflare账号
2. 添加域名
3. 修改DNS为Cloudflare提供的nameserver
4. 开启SSL/TLS（Flexible/Full/Full Strict）
5. 开启Always Use HTTPS

---

## 性能优化

### 后端优化

1. **使用Gunicorn/Uvicorn Workers**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **启用数据库连接池**
   ```python
   engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
   ```

3. **启用响应缓存**
   - 使用Redis缓存频繁查询的数据

### 前端优化

1. **启用Gzip压缩**（Nginx）
   ```nginx
   gzip on;
   gzip_types text/plain text/css application/json application/javascript;
   ```

2. **启用浏览器缓存**
   ```nginx
   location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

3. **使用CDN**
   - 将静态资源部署到CDN

---

## 监控与日志

### 日志查看

```bash
# 后端日志
tail -f /tmp/youguo-backend.log

# Docker日志
docker logs -f youguo-backend

# 系统日志
journalctl -u youguo-backend -f
```

### 健康检查

```bash
# 健康检查端点
curl http://localhost:8000/health

# 系统信息
curl http://localhost:8000/
```

### 进程管理（Systemd）

创建 `/etc/systemd/system/youguo-backend.service`：

```ini
[Unit]
Description=福娃内容中台系统后端
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/youguo-content-hub/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启用并启动：

```bash
sudo systemctl enable youguo-backend
sudo systemctl start youguo-backend
sudo systemctl status youguo-backend
```

---

## 故障排查

### 服务无法启动

1. 检查端口是否被占用：`netstat -tlnp | grep 8000`
2. 检查依赖是否安装：`pip list | grep fastapi`
3. 查看错误日志：`tail -f /tmp/youguo-backend.log`

### 数据库连接失败

1. 检查数据库服务是否运行
2. 检查连接字符串是否正确
3. 检查防火墙是否允许数据库端口

### 前端无法访问后端

1. 检查CORS配置
2. 检查后端服务是否运行
3. 检查API地址配置是否正确

### 上传文件失败

1. 检查上传目录权限
2. 检查文件大小限制
3. 检查磁盘空间

---

## 安全建议

1. **修改默认SECRET_KEY**
   ```bash
   export SECRET_KEY=$(openssl rand -hex 32)
   ```

2. **启用HTTPS**
   - 所有生产环境必须使用HTTPS

3. **限制文件上传类型和大小**
   - 在Nginx或应用层配置

4. **定期备份数据**
   ```bash
   # 添加定时任务
   0 2 * * * /path/to/scripts/backup.sh
   ```

5. **更新依赖**
   ```bash
   pip list --outdated
   pip install --upgrade -r requirements.txt
   ```
