#!/usr/bin/env python3
"""
Fleet Commander - Modern Edition
Extends classic fleet_ops.py with GitHub Actions and Gemini automation integration
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional

# Auto-detect environment (same as classic)
if "com.termux" in os.environ.get("PREFIX", ""):
    DEVICE_NAME = "Pixel 8a (Mobile)"
    ROOT_DIR = "/storage/emulated/0/pixel8a/unexusi/"
else:
    DEVICE_NAME = "Laptop (Base)"
    ROOT_DIR = "/home/sauron/Q/runexusiam/"

# Try to import GitPython
try:
    from git import Repo, GitCommandError
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    print("⚠️  GitPython not available - running in limited mode")

class FleetRepo:
    """Represents a single repository in the fleet"""

    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(path)
        self.repo = None
        self.status = self._get_status()

    def _get_status(self) -> Dict:
        """Get repository status"""
        if not GIT_AVAILABLE:
            return {"error": "GitPython not available"}

        try:
            self.repo = Repo(self.path)

            # Get branch info
            try:
                branch = self.repo.active_branch.name
            except:
                branch = "DETACHED"

            # Check for changes
            dirty = self.repo.is_dirty(untracked_files=True)

            # Get remote status
            ahead = 0
            behind = 0
            try:
                origin = self.repo.remotes.origin
                origin.fetch()
                local_branch = self.repo.active_branch
                remote_branch = local_branch.tracking_branch()

                if remote_branch:
                    ahead = sum(1 for _ in self.repo.iter_commits(f'{remote_branch.name}..{local_branch.name}'))
                    behind = sum(1 for _ in self.repo.iter_commits(f'{local_branch.name}..{remote_branch.name}'))
            except:
                pass

            return {
                "branch": branch,
                "dirty": dirty,
                "ahead": ahead,
                "behind": behind,
                "health": self._calculate_health(dirty, ahead, behind)
            }
        except Exception as e:
            return {"error": str(e)}

    def _calculate_health(self, dirty: bool, ahead: int, behind: int) -> str:
        """Calculate repository health status"""
        if dirty:
            return "DIRTY"
        elif ahead > 0:
            return "AHEAD"
        elif behind > 0:
            return "BEHIND"
        else:
            return "SYNCED"

    def sync(self, message: str = "Auto-sync via Fleet Commander") -> Dict:
        """Sync repository (commit, pull, push)"""
        results = []

        if not GIT_AVAILABLE or not self.repo:
            return {"error": "Git not available"}

        try:
            # Commit if dirty
            if self.status.get("dirty"):
                self.repo.git.add(all=True)
                self.repo.index.commit(message)
                results.append("✅ Committed local changes")

            # Pull if behind
            if self.status.get("behind", 0) > 0:
                origin = self.repo.remotes.origin
                origin.pull()
                results.append("✅ Pulled from remote")

            # Push if ahead or was dirty
            if self.status.get("ahead", 0) > 0 or self.status.get("dirty"):
                origin = self.repo.remotes.origin
                origin.push()
                results.append("✅ Pushed to remote")

            if not results:
                results.append("✨ Already synced")

            return {"success": True, "actions": results}

        except Exception as e:
            return {"error": str(e)}

    def to_dict(self) -> Dict:
        """Export as dictionary for JSON output"""
        return {
            "name": self.name,
            "path": self.path,
            "status": self.status
        }


class FleetCommander:
    """Main fleet management system"""

    def __init__(self, root_dir: str = ROOT_DIR):
        self.root_dir = Path(root_dir)
        self.repos: List[FleetRepo] = []
        self._scan_repos()

    def _scan_repos(self):
        """Scan for git repositories in root directory"""
        if not self.root_dir.exists():
            print(f"⚠️  Directory not found: {self.root_dir}")
            return

        for item in sorted(self.root_dir.iterdir()):
            if item.is_dir() and (item / ".git").exists():
                try:
                    repo = FleetRepo(str(item))
                    self.repos.append(repo)
                except Exception as e:
                    print(f"⚠️  Error loading {item.name}: {e}")

    def status(self, format: str = "human") -> str:
        """Get fleet status"""
        if format == "json":
            return json.dumps({
                "device": DEVICE_NAME,
                "root_dir": str(self.root_dir),
                "repos": [r.to_dict() for r in self.repos]
            }, indent=2)

        # Human-readable format
        lines = []
        lines.append(f"\n🌍 FLEET COMMANDER - {DEVICE_NAME}")
        lines.append(f"Sector: {self.root_dir}\n")

        if not self.repos:
            lines.append("No repositories found")
        else:
            for i, repo in enumerate(self.repos, 1):
                health = repo.status.get("health", "UNKNOWN")
                branch = repo.status.get("branch", "unknown")

                icons = {
                    "SYNCED": "✅",
                    "DIRTY": "⚠️ ",
                    "AHEAD": "⬆️ ",
                    "BEHIND": "⬇️ "
                }
                icon = icons.get(health, "❓")

                lines.append(f"{i}. {icon} {repo.name:<20} [{branch}] | {health}")

        return "\n".join(lines)

    def sync_all(self, message: str = "Auto-sync via Fleet Commander") -> Dict:
        """Sync all repositories"""
        results = {}

        for repo in self.repos:
            print(f"\n⚙️  Syncing {repo.name}...")
            result = repo.sync(message)
            results[repo.name] = result

            if "error" in result:
                print(f"   ❌ Error: {result['error']}")
            else:
                for action in result.get("actions", []):
                    print(f"   {action}")

        return results

    def triage(self) -> Dict:
        """Triage fleet - identify repos needing attention"""
        needs_attention = []

        for repo in self.repos:
            health = repo.status.get("health")
            if health in ["DIRTY", "BEHIND"]:
                needs_attention.append({
                    "name": repo.name,
                    "health": health,
                    "status": repo.status
                })

        return {
            "total_repos": len(self.repos),
            "needs_attention": len(needs_attention),
            "repos": needs_attention
        }


def main():
    parser = argparse.ArgumentParser(description="Fleet Commander - Modern Edition")
    parser.add_argument("command",
                       choices=["status", "sync", "triage"],
                       help="Command to execute")
    parser.add_argument("--format",
                       choices=["human", "json"],
                       default="human",
                       help="Output format")
    parser.add_argument("--message", "-m",
                       default="Auto-sync via Fleet Commander",
                       help="Commit message for sync")

    args = parser.parse_args()

    fleet = FleetCommander()

    if args.command == "status":
        print(fleet.status(format=args.format))

    elif args.command == "sync":
        results = fleet.sync_all(message=args.message)
        if args.format == "json":
            print(json.dumps(results, indent=2))

    elif args.command == "triage":
        results = fleet.triage()
        if args.format == "json":
            print(json.dumps(results, indent=2))
        else:
            print(f"\n🔍 Fleet Triage Results")
            print(f"Total repos: {results['total_repos']}")
            print(f"Needs attention: {results['needs_attention']}")

            if results['repos']:
                print("\nRepositories needing attention:")
                for repo in results['repos']:
                    print(f"  - {repo['name']}: {repo['health']}")


if __name__ == "__main__":
    main()
