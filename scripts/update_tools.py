#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
from datetime import datetime

try:
    from github import Github
except ImportError:
    print("Installing PyGithub...")
    os.system("pip install PyGithub")
    from github import Github

def get_tools_list(github_token, username):
    """掃描所有倉庫並提取工具資訊"""
    g = Github(github_token)
    user = g.get_user(username)
    
    tools = []
    
    print(f"🔍 掃描用戶 {username} 的倉庫...")
    
    for repo in user.get_repos():
        # 跳過 Profile 倉庫本身
        if repo.name == username:
            continue
        
        print(f"   檢查倉庫: {repo.name}")
        
        # 檢查是否有 HTML 文件（小工具的標誌）
        has_html = False
        tool_files = []
        
        try:
            contents = repo.get_contents("")
            for content in contents:
                if content.name.endswith('.HTML') or content.name.endswith('.html'):
                    has_html = True
                    tool_files.append(content.name)
                    print(f"      ✓ 找到工具文件: {content.name}")
        except:
            continue
        
        # 檢查是否啟用 GitHub Pages
        pages_url = None
        try:
            # 嘗試獲取 Pages 資訊
            pages_url = f"https://{username}.github.io/{repo.name}/"
            print(f"      ✓ Pages URL: {pages_url}")
        except:
            pages_url = repo.html_url
        
        if has_html or tool_files:
            tool_info = {
                'name': repo.name,
                'description': repo.description or '實用小工具',
                'url': pages_url,
                'repo_url': repo.html_url,
                'stars': repo.stargazers_count,
                'language': repo.language or 'HTML',
                'updated': repo.updated_at.strftime('%Y-%m-%d'),
                'files': tool_files
            }
            tools.append(tool_info)
            print(f"   ✅ 已添加工具: {repo.name}")
    
    print(f"\n✅ 共找到 {len(tools)} 個工具\n")
    return tools

def generate_tools_markdown(tools):
    """生成工具列表的 Markdown"""
    if not tools:
        return "*目前還沒有工具*"
    
    lines = []
    
    # 標題
    lines.append("### 🎯 線上工具集\n")
    
    # 為每個工具生成卡片
    for i, tool in enumerate(tools, 1):
        # 提取工具顯示名稱
        display_name = tool['name'].replace('-', ' ').replace('_', ' ').title()
        
        # 如果有 HTML 文件，列出它們
        files_info = ""
        if tool['files']:
            files_list = ', '.join([f"`{f}`" for f in tool['files']])
            files_info = f"\n**📄 文件**: {files_list}"
        
        card = f"""
<div align="center">

#### {i}. 🔧 {display_name}

{tool['description']}

{files_info}

[![使用工具](https://img.shields.io/badge/🚀_立即使用-4CAF50?style=for-the-badge)]({tool['url']})
[![查看源碼](https://img.shields.io/badge/📦_查看源碼-2196F3?style=for-the-badge)]({tool['repo_url']})

⭐ Stars: {tool['stars']} | 💻 語言: {tool['language']} | 📅 更新: {tool['updated']}

---

</div>
"""
        lines.append(card)
    
    # 統計資訊
    lines.append(f"\n**📊 統計**: 共 {len(tools)} 個工具")
    
    # 更新時間
    update_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    lines.append(f"\n*🕐 最後更新: {update_time}*\n")
    
    return '\n'.join(lines)

def update_readme(tools_content, readme_path='README.md'):
    """更新 README 文件"""
    print(f"📖 讀取 {readme_path}...")
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替換工具列表部分
    start_marker = '<!-- TOOLS_LIST:START -->'
    end_marker = '<!-- TOOLS_LIST:END -->'
    
    pattern = r'<!-- TOOLS_LIST:START -->.*?<!-- TOOLS_LIST:END -->'
    replacement = f'{start_marker}\n{tools_content}\n{end_marker}'
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ {readme_path} 更新成功！\n")

def main():
    github_token = os.getenv('GITHUB_TOKEN')
    username = os.getenv('GITHUB_ACTOR', 'abc214315')
    
    if not github_token:
        print("❌ 錯誤: 未設置 GITHUB_TOKEN")
        sys.exit(1)
    
    print("=" * 60)
    print("🚀 開始更新工具儀表板")
    print("=" * 60)
    
    # 獲取工具列表
    tools = get_tools_list(github_token, username)
    
    # 生成 Markdown
    tools_content = generate_tools_markdown(tools)
    
    # 更新 README
    update_readme(tools_content)
    
    print("=" * 60)
    print("✅ 儀表板更新完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
