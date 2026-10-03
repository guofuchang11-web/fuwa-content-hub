# 福娃内容中台系统 - 多平台部署指南

## 📦 部署文件清单

| 文件 | 用途 | 部署平台 |
|---|---|---|
| `index.html` | 应用主文件（压缩版，587KB） | 所有静态平台 |
| `netlify.toml` | Netlify 部署配置（SPA 路由 + 安全头） | Netlify |
| `_redirects` | Netlify 前端路由重定向 | Netlify |
| `vercel.json` | Vercel 部署配置 | Vercel |
| `.github/workflows/deploy.yml` | GitHub Pages 自动部署工作流 | GitHub Pages |
| `.nojekyll` | 禁用 Jekyll 处理 | GitHub Pages |
| `404.html` | SPA 路由回退页面 | GitHub Pages |
| `docker-compose.yml` | Docker 一键部署（前端+后端） | 自有服务器 |
| `nginx.conf` | Nginx 前端配置 | 自有服务器 |
| `backend/Dockerfile` | 后端 Docker 镜像 | 自有服务器 |

---

## 🚀 平台一：Netlify 部署（推荐，免费）

### 方式一：拖拽部署（最简单）

1. 访问 https://app.netlify.com/drop
2. 将 `deploy/` 目录下的所有文件 + `index.html` 拖拽到页面
3. 等待部署完成，获得 `https://xxx.netlify.app` 域名

### 方式二：Git 持续部署

1. 将代码推送到 GitHub
2. 访问 https://app.netlify.com/start
3. 选择你的 GitHub 仓库
4. 配置：
   - Build command: 留空
   - Publish directory: `.`
5. 点击 Deploy，自动部署

### 方式三：CLI 部署

```bash
# 安装 Netlify CLI
npm install -g netlify-cli

# 登录
netlify login

# 初始化并部署
cd deploy
netlify init
netlify deploy --prod
```

---

## ▲ 平台二：Vercel 部署（推荐，免费）

### 方式一：Git 部署

1. 将代码推送到 GitHub
2. 访问 https://vercel.com/new
3. 导入你的 GitHub 仓库
4. 配置：
   - Framework Preset: Other
   - Build Command: 留空
   - Output Directory: `.`
5. 点击 Deploy，自动部署

### 方式二：CLI 部署

```bash
# 安装 Vercel CLI
npm install -g vercel

# 登录
vercel login

# 部署
cd deploy
vercel --prod
```

---

## 🐙 平台三：GitHub Pages 部署（免费）

### 自动部署（推荐）

1. 将代码推送到 GitHub 仓库的 `main` 分支
2. 确保 `.github/workflows/deploy.yml` 文件存在
3. 进入仓库 Settings → Pages
4. Source 选择 "GitHub Actions"
5. 每次 push 到 main 分支会自动部署
6. 访问 `https://你的用户名.github.io/仓库名/`

### 手动部署

```bash
# 创建 gh-pages 分支
git checkout --orphan gh-pages

# 复制文件
cp ../index.html .
cp .nojekyll .
cp 404.html .

# 提交并推送
git add .
git commit -m "deploy: 福娃内容中台系统"
git push origin gh-pages

# 开启 Pages
# Settings → Pages → Source: gh-pages branch
```

---

## 🐳 平台四：Docker 部署（自有服务器）

### 一键启动（前端 + 后端）

```bash
cd deploy

# 启动所有服务
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 访问地址

- 前端：http://localhost:8080
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

### 仅启动后端

```bash
cd ../backend

# 构建镜像
docker build -t youguo-backend .

# 运行容器
docker run -d \
  --name youguo-backend \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/uploads:/app/uploads \
  youguo-backend
```

---

## 🌐 平台五：Nginx 静态部署（自有服务器）

```bash
# 1. 安装 Nginx
sudo apt install nginx

# 2. 复制前端文件
sudo mkdir -p /var/www/youguo
sudo cp ../index.html /var/www/youguo/

# 3. 复制 Nginx 配置
sudo cp nginx.conf /etc/nginx/conf.d/youguo.conf

# 4. 测试配置
sudo nginx -t

# 5. 重启 Nginx
sudo systemctl restart nginx

# 6. 访问
# http://your-server-ip
```

---

## 🔧 后端部署配置

### 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./data/content_hub.db` | 数据库连接地址 |
| `SECRET_KEY` | `youguo-secret-key` | JWT 签名密钥（生产环境必须修改） |
| `ALGORITHM` | `HS256` | JWT 算法 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Token 有效期（分钟） |
| `STORAGE_MAX_SIZE` | `8880TB` | 存储容量显示 |
| `MAX_UPLOAD_SIZE` | `8880TB` | 单文件上传上限 |

### 数据库切换

**SQLite（默认，无需配置）**
```
DATABASE_URL=sqlite:///./data/content_hub.db
```

**MySQL**
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/youguo
```

**PostgreSQL**
```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/youguo
```

---

## 📊 部署平台对比

| 平台 | 免费额度 | 自定义域名 | SSL | 持续部署 | 后端支持 | 推荐指数 |
|---|---|---|---|---|---|---|
| **Netlify** | 100GB流量/月 | ✅ | ✅ 自动 | ✅ | ❌ 需单独部署 | ⭐⭐⭐⭐⭐ |
| **Vercel** | 100GB流量/月 | ✅ | ✅ 自动 | ✅ | ✅ Serverless | ⭐⭐⭐⭐⭐ |
| **GitHub Pages** | 无限流量 | ✅ | ✅ 自动 | ✅ Actions | ❌ | ⭐⭐⭐⭐ |
| **Cloudflare Pages** | 无限流量 | ✅ | ✅ 自动 | ✅ | ✅ Workers | ⭐⭐⭐⭐⭐ |
| **Docker** | 取决于服务器 | ✅ | 需配置 | ❌ | ✅ 完整 | ⭐⭐⭐⭐ |
| **Nginx** | 取决于服务器 | ✅ | 需配置 | ❌ | ✅ 完整 | ⭐⭐⭐ |

---

## ✅ 部署后检查清单

- [ ] 前端页面可正常访问
- [ ] 页面标题显示"福娃内容中台系统"
- [ ] 侧边栏导航可正常切换
- [ ] 数据上传功能正常
- [ ] 数据保存到 IndexedDB（前端模式）
- [ ] 后端 API 健康检查正常（如部署后端）
- [ ] API 文档可访问（如部署后端）
- [ ] 移动端适配正常
- [ ] HTTPS 证书有效（如配置域名）

---

## 🔄 更新部署

### Netlify/Vercel（Git 模式）
```bash
git add .
git commit -m "update: 更新内容"
git push origin main
# 自动触发重新部署
```

### GitHub Pages
```bash
git push origin main
# GitHub Actions 自动部署
```

### Docker
```bash
cd deploy
docker-compose down
docker-compose pull  # 如果使用远程镜像
docker-compose up -d --build
```

---

## 🆘 常见问题

**Q: 部署后页面空白？**
A: 检查浏览器控制台，通常是路径问题。确保 index.html 在根目录，且 SPA 路由配置正确。

**Q: 刷新页面 404？**
A: SPA 路由回退配置缺失。Netlify 检查 `_redirects`，Vercel 检查 `vercel.json` 的 rewrites，GitHub Pages 需要 `404.html`。

**Q: 后端 API 连接失败？**
A: 检查后端服务是否启动，端口是否正确，CORS 是否配置允许前端域名。

**Q: 数据上传失败？**
A: 前端模式下数据存储在浏览器 IndexedDB，清除浏览器数据会丢失。建议定期导出备份。

**Q: 如何绑定自定义域名？**
A: Netlify/Vercel/GitHub Pages 都支持在设置中添加自定义域名，然后在域名服务商添加 CNAME 记录。
