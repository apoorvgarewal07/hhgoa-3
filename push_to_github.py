#!/usr/bin/env python3
"""
Convenience script to push the repository to GitHub.
Usage:
    python push_to_github.py [GITHUB_TOKEN]
"""
import sys
import getpass
from dulwich import porcelain
from dulwich.client import HTTPUnauthorized


def push_repo(token=None):
    repo_url = "https://github.com/apoorvgarewal07/hhgoa-3-task.git"
    
    if not token:
        if len(sys.argv) > 1:
            token = sys.argv[1].strip()
        else:
            print("To push to GitHub, enter your GitHub Personal Access Token (PAT)")
            print("You can generate one at: https://github.com/settings/tokens (select 'repo' scope)")
            token = getpass.getpass("GitHub Personal Access Token: ").strip()

    if not token:
        print("❌ Token cannot be empty.")
        return False

    auth_url = f"https://apoorvgarewal07:{token}@github.com/apoorvgarewal07/hhgoa-3-task.git"

    print(f"\n🚀 Staging all files and committing...")
    repo = porcelain.open_repo(".")
    
    try:
        porcelain.add(repo, paths=[
            ".gitignore", ".env.example", "requirements.txt", "README.md",
            "run.sh", "run.bat", "push_to_github.py",
            "src", "blockchain", "docs", "tests", "data/input_faces"
        ])
        head = repo.head()
        repo.refs[b"refs/heads/main"] = head
    except Exception as e:
        print(f"Commit status: {e}")

    print(f"📡 Pushing to {repo_url} (branch: main)...")
    try:
        porcelain.push(repo, auth_url, refspecs=b"refs/heads/main")
        print("✅ Successfully pushed to GitHub: https://github.com/apoorvgarewal07/hhgoa-3-task")
        return True
    except HTTPUnauthorized:
        print("❌ Authentication failed: Invalid GitHub token or insufficient permissions.")
        print("Please ensure your Personal Access Token has 'repo' or 'write:packages' scope enabled.")
        return False
    except Exception as e:
        print(f"❌ Push error: {e}")
        return False


if __name__ == "__main__":
    push_repo()
