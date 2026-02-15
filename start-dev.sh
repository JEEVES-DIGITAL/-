#!/bin/bash

# 基维斯OS 一键开发环境启动脚本
# 用于快速搭建本地开发环境

set -e

JEEVES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔════════════════════════════════════════════════════════╗"
echo "║         🏠 基维斯OS (Jeeves OS) 开发环境启动             ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

cd "$JEEVES_DIR"

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 请先安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ 请先安装 Docker Compose"
    exit 1
fi

# 创建必要目录
echo "📁 创建必要目录..."
mkdir -p config data logs

# 复制示例配置（如果不存在）
if [[ ! -f ".env" ]]; then
    echo "⚙️  创建默认配置..."
    cat > .env <<EOF
# Jeeves OS 开发环境配置
JEEVES_VERSION=0.1.0-dev
TZ=Asia/Shanghai
JEEVES_MODE=development
DEBUG=true

# 数据库（开发环境使用简单密码）
DB_PASSWORD=jeeves
POSTGRES_USER=jeeves
POSTGRES_DB=jeeves_dev

# Frigate
FRIGATE_PASSWORD=jeeves
EOF
fi

echo "🚀 启动开发环境..."
docker-compose -f docker-compose.dev.yml up -d

echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
echo ""
echo "📊 服务状态:"
docker-compose -f docker-compose.dev.yml ps

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                  ✅ 开发环境已启动                       ║"
echo "╠════════════════════════════════════════════════════════╣"
echo "║                                                        ║"
echo "║  🌐 服务地址:                                          ║"
echo "║     Jeeves Core: http://localhost:8123                 ║"
echo "║     PostgreSQL:  localhost:5432                        ║"
echo "║     Redis:       localhost:6379                        ║"
echo "║     Ollama:      http://localhost:11434                ║"
echo "║                                                        ║"
echo "║  📋 常用命令:                                          ║"
echo "║     查看日志: docker-compose -f docker-compose.dev.yml ║"
echo "║               logs -f                                  ║"
echo "║     停止服务: docker-compose -f docker-compose.dev.yml ║"
echo "║               down                                     ║"
echo "║     重启服务: docker-compose -f docker-compose.dev.yml ║"
echo "║               restart                                  ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
