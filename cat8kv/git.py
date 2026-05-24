from pathlib import Path
import shutil

from git import Actor, Repo

from cat8kv.config import GitConfig


def init_repo(config: GitConfig) -> Repo:
    config.repo_path.mkdir(parents=True, exist_ok=True)
    if (config.repo_path / ".git").exists():
        return Repo(config.repo_path)
    return Repo.init(config.repo_path)


def _has_changes(repo: Repo) -> bool:
    if not repo.head.is_valid():
        return len(repo.index.entries) > 0
    return bool(repo.index.diff("HEAD")) or bool(repo.untracked_files)


def sync(backups_dir: Path, config: GitConfig) -> None:
    repo = init_repo(config)
    author = Actor(config.committer_name, config.committer_email)

    for src in backups_dir.glob("*.json"):
        shutil.copy2(src, config.repo_path / src.name)

    repo.index.add([f.name for f in config.repo_path.glob("*.json")])

    if not _has_changes(repo):
        return

    repo.index.commit(
        "backup: update config",
        author=author,
        committer=author,
    )
