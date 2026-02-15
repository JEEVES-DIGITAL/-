#!/bin/bash

# GitHub 仓库初始化脚本
# 用于创建 jeeves-os 组织的所有仓库

set -e

ORG_NAME="jeeves-os"
REPOS=(
    "jeeves-core:AI大脑核心服务"
    "jeeves-hub:设备接入与自动化中枢"
    "jeeves-nodes:边缘节点固件"
    "jeeves-box:硬件设计与镜像"
    "jeeves-app:移动端应用"
    "jeeves-docs:文档中心"
    "jeeves-website:官网"
)

# 检查 GitHub CLI
check_gh() {
    if ! command -v gh &> /dev/null; then
        echo "请先安装 GitHub CLI: https://cli.github.com/"
        exit 1
    fi
    
    if ! gh auth status &> /dev/null; then
        echo "请先登录 GitHub CLI: gh auth login"
        exit 1
    fi
}

# 创建组织
create_org() {
    echo "检查组织 $ORG_NAME..."
    if gh api "orgs/$ORG_NAME" &> /dev/null; then
        echo "组织已存在: $ORG_NAME"
    else
        echo "请手动创建组织: https://github.com/organizations/new"
        echo "组织名: $ORG_NAME"
        exit 1
    fi
}

# 创建仓库
create_repo() {
    local repo_info=$1
    local repo_name=$(echo $repo_info | cut -d':' -f1)
    local repo_desc=$(echo $repo_info | cut -d':' -f2)
    local full_name="$ORG_NAME/$repo_name"
    
    echo "创建仓库: $full_name"
    
    if gh api "repos/$full_name" &> /dev/null; then
        echo "  仓库已存在，跳过"
        return
    fi
    
    gh repo create "$full_name" \
        --public \
        --description "$repo_desc" \
        --homepage "https://jeeves-os.com"
    
    # 添加 topics
    gh api "repos/$full_name/topics" \
        --method PUT \
        --input - <<< '{"names":["home-automation","ai","smart-home","iot","open-source"]}' \
        --silent
    
    echo "  ✅ 创建成功"
}

# 设置保护规则
setup_protection() {
    local repo_name=$1
    local full_name="$ORG_NAME/$repo_name"
    
    echo "设置分支保护: $full_name"
    
    gh api "repos/$full_name/branches/main/protection" \
        --method PUT \
        --input - <<< '{
            "required_status_checks": null,
            "enforce_admins": false,
            "required_pull_request_reviews": {
                "required_approving_review_count": 1
            },
            "restrictions": null
        }' \
        --silent 2>/dev/null || echo "  ⚠️  跳过分支保护设置"
}

# 主函数
main() {
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║         Jeeves OS GitHub 仓库初始化脚本                  ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    
    check_gh
    create_org
    
    echo "开始创建仓库..."
    echo ""
    
    for repo in "${REPOS[@]}"; do
        create_repo "$repo"
        repo_name=$(echo $repo | cut -d':' -f1)
        setup_protection "$repo_name"
        echo ""
    done
    
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║                  ✅ 初始化完成                          ║"
    echo "╠════════════════════════════════════════════════════════╣"
    echo "║                                                        ║"
    echo "║  组织地址: https://github.com/$ORG_NAME                ║"
    echo "║                                                        ║"
    echo "║  接下来:                                               ║"
    echo "║  1. 上传初始代码到 jeeves-core                         ║"
    echo "║  2. 设置 Actions CI/CD                                 ║"
    echo "║  3. 邀请团队成员                                       ║"
    echo "║                                                        ║"
    echo "╚════════════════════════════════════════════════════════╝"
}

main "$@"
