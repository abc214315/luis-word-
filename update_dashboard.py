#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Branch Dashboard Updater
================================
自動更新 GitHub Profile README 中的分支活動儀表板

Author: abc214315
License: MIT
Version: 2.0.0
"""

import os
import re
import sys
from datetime import datetime
from typing import List, Dict, Optional
import logging

# 嘗試導入 PyGithub
try:
    from github import Github, GithubException
except ImportError:
    print("❌ Error: PyGithub not installed")
    print("💡 Run: pip install PyGithub")
    sys.exit(1)

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class BranchDashboardUpdater:
    """
    分支儀表板更新器
    
    負責從 GitHub API 獲取分支資訊並更新 README.md
    """
    
    def __init__(self, token: str, repo_name: str):
        """
        初始化更新器
        
        Args:
            token (str): GitHub Personal Access Token
            repo_name (str): 倉庫名稱，格式為 'owner/repo'
        """
        self.token = token
        self.repo_name = repo_name
        self.github = None
        self.repo = None
        
   def connect(self) -> bool:
    """
    連接到 GitHub API
    
    Returns:
        bool: 連接成功返回 True，失敗返回 False
    """
    try:
        logger.info("🔍 正在連接到 GitHub API...")
        self.github = Github(self.token)
        
        # 獲取目標倉庫
        logger.info(f"📦 正在獲取倉庫: {self.repo_name}")
        self.repo = self.github.get_repo(self.repo_name)
        logger.info(f"✅ 倉庫已找到: {self.repo.full_name}")
        
        # 顯示倉庫基本資訊
        logger.info(f"   ├─ 星標數: {self.repo.stargazers_count}")
        logger.info(f"   ├─ Fork 數: {self.repo.forks_count}")
        logger.info(f"   └─ 開放問題: {self.repo.open_issues_count}")
        
        return True
        
    except GithubException as e:
        logger.error(f"❌ GitHub API 錯誤: {e.status} - {e.data.get('message', 'Unknown error')}")
        return False
    except Exception as e:
        logger.error(f"❌ 連接錯誤: {str(e)}")
        return False
    
    def fetch_branches(self, limit: int = 15) -> List[Dict]:
        """
        獲取分支資訊
        
        Args:
            limit (int): 最多獲取的分支數量，默認 15
            
        Returns:
            List[Dict]: 分支資訊列表，每個元素包含分支的詳細資訊
        """
        try:
            logger.info("🌿 正在獲取分支列表...")
            branches = list(self.repo.get_branches())
            total_branches = len(branches)
            logger.info(f"✅ 找到 {total_branches} 個分支")
            
            if total_branches == 0:
                logger.warning("⚠️  倉庫中沒有分支")
                return []
            
            branch_data = []
            processed_count = 0
            
            # 處理每個分支
            for branch in branches[:limit]:
                try:
                    commit = branch.commit
                    
                    # 獲取提交訊息的第一行（標題）
                    commit_message = commit.commit.message.split('\n')[0]
                    
                    # 處理過長的提交訊息
                    max_length = 60
                    if len(commit_message) > max_length:
                        commit_title = commit_message[:max_length - 3] + "..."
                    else:
                        commit_title = commit_message
                    
                    # 轉義 Markdown 特殊字符
                    commit_title = self._escape_markdown(commit_title)
                    
                    # 獲取作者資訊
                    author = commit.commit.author.name
                    if len(author) > 20:
                        author = author[:17] + "..."
                    
                    # 格式化日期
                    date = commit.commit.author.date.strftime('%Y-%m-%d')
                    
                    # 提交連結資訊
                    commit_url = commit.html_url
                    commit_sha = commit.sha[:7]
                    
                    # 組裝分支資訊
                    branch_info = {
                        'name': branch.name,
                        'title': commit_title,
                        'author': author,
                        'date': date,
                        'url': commit_url,
                        'sha': commit_sha
                    }
                    
                    branch_data.append(branch_info)
                    processed_count += 1
                    logger.info(f"   ✓ [{processed_count}/{min(limit, total_branches)}] 已處理: {branch.name}")
                    
                except Exception as e:
                    logger.warning(f"   ⚠️  處理分支 '{branch.name}' 時出錯: {str(e)}")
                    continue
            
            logger.info(f"✅ 成功處理 {len(branch_data)} 個分支")
            return branch_data
            
        except Exception as e:
            logger.error(f"❌ 獲取分支時出錯: {str(e)}")
            return []
    
    def generate_table(self, branches: List[Dict]) -> str:
        """
        生成 Markdown 表格
        
        Args:
            branches (List[Dict]): 分支資訊列表
            
        Returns:
            str: 格式化的 Markdown 表格字符串
        """
        logger.info("📝 正在生成 Markdown 表格...")
        
        # 表格標題行
        lines = [
            "| 🌿 Branch | 📝 Latest Commit | 👤 Author | ⏰ Time | 🔗 Link |",
            "|-----------|------------------|-----------|---------|---------|"
        ]
        
        # 添加每個分支的資料行
        for branch in branches:
            line = (
                f"| `{branch['name']}` | "
                f"{branch['title']} | "
                f"{branch['author']} | "
                f"{branch['date']} | "
                f"[`{branch['sha']}`]({branch['url']}) |"
            )
            lines.append(line)
        
        # 添加更新時間戳記
        update_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        lines.append(f"\n*🕐 Last updated: {update_time}*")
        
        table_content = '\n'.join(lines)
        logger.info(f"✅ 表格生成完成，共 {len(branches)} 行資料")
        
        return table_content
    
    def update_readme(self, table_content: str, readme_path: str = 'README.md') -> bool:
        """
        更新 README 文件
        
        Args:
            table_content (str): 要插入的表格內容
            readme_path (str): README 文件路徑，默認為 'README.md'
            
        Returns:
            bool: 更新成功返回 True，沒有變更或失敗返回 False
        """
        try:
            logger.info(f"📖 正在讀取 {readme_path}...")
            
            # 檢查文件是否存在
            if not os.path.exists(readme_path):
                logger.error(f"❌ 找不到 {readme_path} 文件")
                return False
            
            # 讀取 README 內容
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # 檢查必要的標記是否存在
            start_marker = '<!-- BRANCH_ACTIVITY:START -->'
            end_marker = '<!-- BRANCH_ACTIVITY:END -->'
            
            if start_marker not in readme_content:
                logger.error(f"❌ README 中找不到起始標記: {start_marker}")
                return False
            
            if end_marker not in readme_content:
                logger.error(f"❌ README 中找不到結束標記: {end_marker}")
                return False
            
            # 使用正則表達式替換內容
            logger.info("✏️  正在更新 README 內容...")
            pattern = r'<!-- BRANCH_ACTIVITY:START -->.*?<!-- BRANCH_ACTIVITY:END -->'
            replacement = f'{start_marker}\n{table_content}\n{end_marker}'
            
            updated_content = re.sub(
                pattern,
                replacement,
                readme_content,
                flags=re.DOTALL
            )
            
            # 檢查是否有實際變更
            if updated_content == readme_content:
                logger.info("ℹ️  內容沒有變更，無需更新")
                return False
            
            # 寫入更新後的內容
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            logger.info("✅ README 更新成功！")
            return True
            
        except Exception as e:
            logger.error(f"❌ 更新 README 時出錯: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def _escape_markdown(text: str) -> str:
        """
        轉義 Markdown 特殊字符
        
        Args:
            text (str): 原始文本
            
        Returns:
            str: 轉義後的文本
        """
        # 需要轉義的特殊字符
        special_chars = {
            '|': '\\|',
            '[': '\\[',
            ']': '\\]',
            '(': '\\(',
            ')': '\\)',
            '<': '&lt;',
            '>': '&gt;',
        }
        
        for char, escaped in special_chars.items():
            text = text.replace(char, escaped)
        
        return text


def validate_environment() -> tuple:
    """
    驗證環境變數
    
    Returns:
        tuple: (token, repo_name) 或 (None, None) 如果驗證失敗
    """
    logger.info("🔍 正在驗證環境變數...")
    
    token = os.environ.get('GITHUB_TOKEN')
    repo_name = os.environ.get('REPO_NAME')
    
    errors = []
    
    if not token:
        errors.append("GITHUB_TOKEN 環境變數未設置")
    
    if not repo_name:
        errors.append("REPO_NAME 環境變數未設置")
    elif '/' not in repo_name:
        errors.append(f"REPO_NAME 格式錯誤: '{repo_name}' (應為 'owner/repo')")
    
    if errors:
        for error in errors:
            logger.error(f"❌ {error}")
        return None, None
    
    logger.info("✅ 環境變數驗證通過")
    logger.info(f"   ├─ Token: {'*' * 20}...{token[-4:]}")
    logger.info(f"   └─ Repo: {repo_name}")
    
    return token, repo_name


def main():
    """
    主函數
    
    執行流程:
    1. 驗證環境變數
    2. 連接到 GitHub API
    3. 獲取分支資訊
    4. 生成 Markdown 表格
    5. 更新 README 文件
    """
    logger.info("=" * 60)
    logger.info("🚀 GitHub Branch Dashboard Updater")
    logger.info("=" * 60)
    
    try:
        # 步驟 1: 驗證環境變數
        token, repo_name = validate_environment()
        if not token or not repo_name:
            logger.error("💥 環境變數驗證失敗，程式退出")
            sys.exit(1)
        
        # 步驟 2: 創建更新器並連接
        logger.info("\n" + "─" * 60)
        updater = BranchDashboardUpdater(token, repo_name)
        
        if not updater.connect():
            logger.error("💥 連接 GitHub API 失敗，程式退出")
            sys.exit(1)
        
        # 步驟 3: 獲取分支資訊
        logger.info("\n" + "─" * 60)
        branches = updater.fetch_branches(limit=15)
        
        if not branches:
            logger.warning("⚠️  沒有獲取到分支資訊")
            logger.info("💡 請確認倉庫中至少有一個分支")
            sys.exit(1)
        
        # 步驟 4: 生成表格
        logger.info("\n" + "─" * 60)
        table_content = updater.generate_table(branches)
        
        # 步驟 5: 更新 README
        logger.info("\n" + "─" * 60)
        if updater.update_readme(table_content):
            logger.info("\n" + "=" * 60)
            logger.info("🎉 儀表板更新完成！")
            logger.info("=" * 60)
            sys.exit(0)
        else:
            logger.info("\n" + "=" * 60)
            logger.info("ℹ️  沒有需要更新的內容")
            logger.info("=" * 60)
            sys.exit(0)
        
    except KeyboardInterrupt:
        logger.info("\n⚠️  操作被用戶中斷")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n💥 發生未預期的錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
