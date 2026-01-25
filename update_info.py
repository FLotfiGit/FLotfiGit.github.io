#!/usr/bin/env python3
"""
Generate git repository update information for Jekyll site.
This script generates a YAML file with git info that can be included in Jekyll layouts.
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path

def get_git_info():
    """Get git repository information."""
    try:
        # Get current branch
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True
        ).strip()
        
        # Get last commit hash
        commit_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True
        ).strip()
        
        # Get last commit message
        commit_msg = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%s"],
            text=True
        ).strip()
        
        # Get last commit date
        commit_date = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%ai"],
            text=True
        ).strip()
        
        # Get remote URL
        remote_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            text=True
        ).strip()
        
        # Check if repository is dirty
        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            text=True
        ).strip()
        is_dirty = bool(status)
        
        # Get ahead/behind info
        ahead_behind = subprocess.check_output(
            ["git", "rev-list", "--left-right", "--count", "HEAD...@{u}"],
            text=True,
            stderr=subprocess.DEVNULL
        ).strip().split() if subprocess.run(
            ["git", "rev-parse", "@{u}"],
            capture_output=True
        ).returncode == 0 else ["0", "0"]
        
        return {
            "branch": branch,
            "commit_hash": commit_hash,
            "commit_msg": commit_msg,
            "commit_date": commit_date,
            "remote_url": remote_url,
            "is_dirty": is_dirty,
            "ahead": ahead_behind[0] if len(ahead_behind) > 0 else "0",
            "behind": ahead_behind[1] if len(ahead_behind) > 1 else "0",
            "updated_at": datetime.now().isoformat()
        }
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        return None

def save_git_info_yaml(git_info):
    """Save git info as YAML in _data directory."""
    data_dir = Path("_data")
    data_dir.mkdir(exist_ok=True)
    
    git_info_file = data_dir / "git_info.yml"
    
    with open(git_info_file, "w") as f:
        f.write("# Auto-generated git repository information\n")
        f.write(f"branch: {git_info['branch']}\n")
        f.write(f"commit_hash: {git_info['commit_hash']}\n")
        f.write(f"commit_msg: {git_info['commit_msg']}\n")
        f.write(f"commit_date: '{git_info['commit_date']}'\n")
        f.write(f"remote_url: {git_info['remote_url']}\n")
        f.write(f"is_dirty: {str(git_info['is_dirty']).lower()}\n")
        f.write(f"ahead: {git_info['ahead']}\n")
        f.write(f"behind: {git_info['behind']}\n")
        f.write(f"updated_at: '{git_info['updated_at']}'\n")
    
    print(f"✓ Git info saved to {git_info_file}")

def save_git_info_json(git_info):
    """Save git info as JSON in assets directory."""
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    git_info_file = assets_dir / "git_info.json"
    
    with open(git_info_file, "w") as f:
        json.dump(git_info, f, indent=2)
    
    print(f"✓ Git info saved to {git_info_file}")

if __name__ == "__main__":
    print("Generating git repository update information...")
    git_info = get_git_info()
    
    if git_info:
        save_git_info_yaml(git_info)
        save_git_info_json(git_info)
        print("\n📊 Repository Info:")
        print(f"  Branch: {git_info['branch']}")
        print(f"  Last Commit: {git_info['commit_hash']} - {git_info['commit_msg']}")
        print(f"  Date: {git_info['commit_date']}")
        print(f"  Status: {'Modified' if git_info['is_dirty'] else 'Clean'}")
    else:
        print("✗ Failed to generate git info")
