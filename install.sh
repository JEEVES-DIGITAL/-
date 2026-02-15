#!/bin/bash

# Jeeves OS 安装脚本
# 支持: Ubuntu 22.04+, Debian 12+, Raspberry Pi OS

set -e

JEEVES_VERSION="0.1.0"
JEEVES_DIR="/opt/jeeves-os"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查root权限
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "请使用 root 权限运行此脚本 (sudo)"
        exit 1
    fi
}

# 检查系统要求
check_requirements() {
    print_info "检查系统要求..."
    
    # 检查架构
    ARCH=$(uname -m)
    if [[ "$ARCH" != "x86_64" && "$ARCH" != "aarch64" && "$ARCH" != "armv7l" ]]; then
        print_error "不支持的架构: $ARCH"
        exit 1
    fi
    
    # 检查内存
    MEM_TOTAL=$(free -m | awk '/^Mem:/{print $2}')
    if [[ $MEM_TOTAL -lt 2048 ]]; then
        print_warn "内存小于 2GB，可能会影响性能"
    fi
    
    # 检查磁盘空间
    DISK_AVAIL=$(df -m / | awk 'NR==2 {print $4}')
    if [[ $DISK_AVAIL -lt 10240 ]]; then
        print_error "可用磁盘空间不足 10GB"
        exit 1
    fi
    
    print_info "系统检查通过"
}

# 安装依赖
install_dependencies() {
    print_info "安装依赖..."
    
    apt-get update
    apt-get install -y \
        curl \
        wget \
        git \
        jq \
        docker.io \
        docker-compose \
        ffmpeg \
        usbutils
    
    # 启动 Docker
    systemctl enable docker
    systemctl start docker
    
    print_info "依赖安装完成"
}

# 下载 Jeeves OS
download_jeeves() {
    print_info "下载 Jeeves OS ${JEEVES_VERSION}..."
    
    if [[ -d "$JEEVES_DIR" ]]; then
        print_warn "检测到已存在的安装，将更新..."
        rm -rf "$JEEVES_DIR"
    fi
    
    mkdir -p "$JEEVES_DIR"
    cd "$JEEVES_DIR"
    
    # 下载最新版本
    curl -fsSL "https://github.com/jeeves-os/jeeves-core/releases/download/v${JEEVES_VERSION}/jeeves-os-${JEEVES_VERSION}.tar.gz" | tar -xz --strip-components=1
    
    print_info "下载完成"
}

# 初始化配置
init_config() {
    print_info "初始化配置..."
    
    cd "$JEEVES_DIR"
    
    # 创建必要的目录
    mkdir -p config data logs
    
    # 生成随机密码
    DB_PASSWORD=$(openssl rand -base64 32)
    
    # 创建环境变量文件
    cat > .env <<EOF
# Jeeves OS 环境配置
JEEVES_VERSION=${JEEVES_VERSION}
TZ=Asia/Shanghai

# 数据库
DB_PASSWORD=${DB_PASSWORD}
POSTGRES_USER=jeeves
POSTGRES_DB=jeeves

# Frigate
FRIGATE_PASSWORD=$(openssl rand -base64 16)

# 模式 (production/development)
JEEVES_MODE=production
EOF
    
    print_info "配置已生成: $JEEVES_DIR/.env"
}

# 拉取模型
pull_models() {
    print_info "下载本地AI模型 (这可能需要几分钟)..."
    
    # 启动 ollama 容器临时下载模型
    docker run --rm -v ollama-data:/root/.ollama ollama/ollama:latest pull phi4
    docker run --rm -v ollama-data:/root/.ollama ollama/ollama:latest pull nomic-embed-text
    
    print_info "模型下载完成"
}

# 启动服务
start_services() {
    print_info "启动 Jeeves OS 服务..."
    
    cd "$JEEVES_DIR"
    docker-compose up -d
    
    # 等待服务启动
    print_info "等待服务启动..."
    sleep 10
    
    # 检查健康状态
    if docker-compose ps | grep -q "Up"; then
        print_info "服务启动成功!"
    else
        print_error "服务启动失败，请检查日志: docker-compose logs"
        exit 1
    fi
}

# 创建系统服务
create_systemd_service() {
    print_info "创建系统服务..."
    
    cat > /etc/systemd/system/jeeves-os.service <<EOF
[Unit]
Description=Jeeves OS - Your AI Home Manager
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=${JEEVES_DIR}
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable jeeves-os.service
    
    print_info "系统服务已创建"
}

# 显示完成信息
show_completion() {
    IP=$(hostname -I | awk '{print $1}')
    
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║              🎉 Jeeves OS 安装成功!                         ║"
    echo "║                                                            ║"
    echo "╠════════════════════════════════════════════════════════════╣"
    echo "║                                                            ║"
    echo "║  🌐 Web 界面: http://${IP}:8123                            ║"
    echo "║                                                            ║"
    echo "║  📊 默认登录:                                              ║"
    echo "║     用户名: admin                                          ║"
    echo "║     密码:   admin123                                       ║"
    echo "║                                                            ║"
    echo "║  ⚙️  管理命令:                                             ║"
    echo "║     查看状态: sudo systemctl status jeeves-os              ║"
    echo "║     重启服务: sudo systemctl restart jeeves-os             ║"
    echo "║     查看日志: cd ${JEVEES_DIR} && docker-compose logs -f   ║"
    echo "║                                                            ║"
    echo "║  📖 文档: https://docs.jeeves-os.com                       ║"
    echo "║  💬 社区: https://discord.gg/jeeves-os                     ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
}

# 主函数
main() {
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║           🏠 Jeeves OS 安装程序 v${JEEVES_VERSION}                     ║"
    echo "║                    你的开源AI家庭管家                       ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    check_root
    check_requirements
    install_dependencies
    download_jeeves
    init_config
    pull_models
    start_services
    create_systemd_service
    show_completion
}

# 运行主函数
main "$@"
