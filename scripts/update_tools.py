#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Profile 工具掃描與更新腳本
自動掃描所有倉庫並更新工具列表
"""

import os
import re
import sys
from datetime import datetime
from typing import List, Dict

try:
    from github import Github
    import requests
except ImportError:
    print("📦 安裝必要的依賴...")
    os.system("pip install PyGithub requests")
    from github import Github
    import requests


def get_tools_list(github_token: str, username: str) -> List[Dict]:
    """
    掃描所有倉庫並提取工具資訊
    
    Args:
        github_token: GitHub Personal Access Token
        username: GitHub 用戶名
    
    Returns:
        工具列表
    """
    g = Github(github_token)
    user = g.get_user(username)
    
    tools = []
    
    print(f"\n{'='*60}")
    print(f"🔍 掃描用戶 {username} 的倉庫...")
    print(f"{'='*60}\n")
    
    for repo in user.get_repos():
        # 跳過 Profile 倉庫本身
        if repo.name == username:
            continue
        
        print(f"📂 檢查倉庫: {repo.name}")
        
        # 檢查是否有 HTML 文件（小工具的標誌）
        has_html = False
        tool_files = []
        
        try:
            contents = repo.get_contents("")
            for content in contents:
                if content.name.endswith(('.HTML', '.html', '.htm')):
                    has_html = True
                    tool_files.append(content.name)
                    print(f"   ✓ 找到工具文件: {content.name}")
        except Exception as e:
            print(f"   ⚠️  無法讀取內容: {e}")
            continue
        
        # 檢查是否啟用 GitHub Pages
        pages_url = None
        try:
            # 嘗試獲取 Pages 資訊
            pages = repo.get_pages_build()
            pages_url = f"https://{username}.github.io/{repo.name}/"
            print(f"   ✓ Pages URL: {pages_url}")
        except:
            # 如果沒有 Pages，使用倉庫 URL
            pages_url = repo.html_url
            print(f"   ℹ️  使用倉庫 URL: {pages_url}")
        
        if has_html or tool_files:
            # 獲取倉庫語言
            languages = repo.get_languages()
            main_language = max(languages, key=languages.get) if languages else 'HTML'
            
            tool_info = {
                'name': repo.name,
                'description': repo.description or '實用小工具',
                'url': pages_url,
                'repo_url': repo.html_url,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'language': main_language,
                'updated': repo.updated_at.strftime('%Y-%m-%d'),
                'files': tool_files,
                'topics': list(repo.get_topics())
            }
            tools.append(tool_info)
            print(f"   ✅ 已添加工具: {repo.name}\n")
    
    print(f"{'='*60}")
    print(f"✅ 共找到 {len(tools)} 個工具")
    print(f"{'='*60}\n")
    
    return tools


def generate_tools_markdown(tools: List[Dict]) -> str:
    """
    生成工具列表的 Markdown
    
    Args:
        tools: 工具列表
    
    Returns:
        Markdown 格式的工具列表
    """
    if not tools:
        return """
<table>
<tr>
<td align="center">

### 🔧 暫無工具

目前還沒有可用的工具，敬請期待！

[![提交建議](https://img.shields.io/badge/💡_提交建議-9C27B0?style=for-the-badge)](https://github.com/abc214315/abc214315/issues)

</td>
</tr>
</table>
"""
    
    lines = []
    
    # 開始表格
    lines.append("\n<table>")
    
    # 每行 3 個工具
    for i in range(0, len(tools), 3):
        lines.append("<tr>")
        
        # 處理當前行的工具（最多 3 個）
        row_tools = tools[i:i+3]
        
        for tool in row_tools:
            # 提取工具顯示名稱
            display_name = tool['name'].replace('-', ' ').replace('_', ' ').title()
            
            # 如果有 HTML 文件，列出它們
            files_info = ""
            if tool['files']:
                files_list = ' '.join([f"`{f}`" for f in tool['files'][:3]])  # 最多顯示 3 個
                files_info = f"\n\n**📄 文件**: {files_list}"
            
            # 主題標籤
            topics_info = ""
            if tool['topics']:
                topics_badges = ' '.join([f"`{t}`" for t in tool['topics'][:3]])
                topics_info = f"\n\n{topics_badges}"
            
            cell = f"""
<td align="center" width="33%">

### 🔧 {display_name}

<img src="https://img.icons8.com/fluency/96/000000/code.png" width="80px" />

{tool['description']}{files_info}{topics_info}

[![使用工具](https://img.shields.io/badge/🚀_立即使用-4CAF50?style=for-the-badge)]({tool['url']})
[![查看源碼](https://img.shields.io/badge/📦_源碼-2196F3?style=for-the-badge)]({tool['repo_url']})

⭐ {tool['stars']} | 🍴 {tool['forks']} | 💻 {tool['language']}

📅 更新: {tool['updated']}

</td>
"""
            lines.append(cell)
        
        # 如果該行不足 3 個，填充空單元格
        for _ in range(3 - len(row_tools)):
            lines.append('<td width="33%"></td>')
        
        lines.append("</tr>")
    
    lines.append("</table>\n")
    
    # 統計資訊
    total_stars = sum(tool['stars'] for tool in tools)
    total_forks = sum(tool['forks'] for tool in tools)
    
    lines.append(f"\n**📊 統計**: {len(tools)} 個工具 | ⭐ {total_stars} Stars | 🍴 {total_forks} Forks")
    
    # 更新時間
    update_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    lines.append(f"\n*🕐 最後更新: {update_time}*\n")
    
    return '\n'.join(lines)


def update_readme(tools_content: str, readme_path: str = 'README.md') -> None:
    """
    更新 README 文件
    
    Args:
        tools_content: 工具列表內容
        readme_path: README 文件路徑
    """
    print(f"📖 讀取 {readme_path}...")
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ 錯誤: 找不到 {readme_path}")
        sys.exit(1)
    
    # 替換工具列表部分
    start_marker = '<!-- TOOLS_LIST:START -->'
    end_marker = '<!-- TOOLS_LIST:END -->'
    
    if start_marker not in content or end_marker not in content:
        print(f"⚠️  警告: README 中找不到標記 {start_marker} 或 {end_marker}")
        print("請確保 README.md 中包含這些標記")
        return
    
    pattern = r'<!-- TOOLS_LIST:START -->.*?<!-- TOOLS_LIST:END -->'
    replacement = f'{start_marker}\n{tools_content}\n{end_marker}'
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ {readme_path} 更新成功！\n")


def main():
    """主函數"""
    github_token = os.getenv('GITHUB_TOKEN')
    username = os.getenv('GITHUB_ACTOR', 'abc214315')
    
    if not github_token:
        print("❌ 錯誤: 未設置 GITHUB_TOKEN 環境變量")
        print("請在 GitHub Actions 中設置 secrets.GITHUB_TOKEN")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🚀 開始更新工具儀表板")
    print("="*60)
    
    try:
        # 獲取工具列表
        tools = get_tools_list(github_token, username)
        
        # 生成 Markdown
        tools_content = generate_tools_markdown(tools)
        
        # 更新 README
        update_readme(tools_content)
        
        print("="*60)
        print("✅ 儀表板更新完成！")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
