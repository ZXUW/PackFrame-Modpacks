from __future__ import annotations

import json
import os
import pathlib
import shutil
import stat
import subprocess
import tempfile
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOKEN = os.environ.get("GITEE_TOKEN", "").strip()
GITEE_OWNER = os.environ.get("GITEE_OWNER", "zxuw").strip()
INDEX_REPO = "PackFrame-Modpacks"
API = "https://gitee.com/api/v5"


def gitee_request(method: str, path: str, payload: dict | None = None):
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={
            "Authorization": "token " + TOKEN,
            "Content-Type": "application/json",
            "User-Agent": "PackFrame-Mirror",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode() or "{}")
    except urllib.error.HTTPError as error:
        if error.code in (400, 409, 422):
            return None
        raise


def ensure_repo(name: str):
    gitee_request("POST", "/user/repos", {
        "name": name,
        "private": False,
        "auto_init": False,
        "description": "PackFrame modpack mirror",
    })


def raw_base(name: str) -> str:
    return f"https://gitee.com/{GITEE_OWNER}/{name}/raw/main"


def git(*args: str, cwd: pathlib.Path | None = None):
    try:
        subprocess.run(["git", *args], check=True, cwd=cwd)
    except subprocess.CalledProcessError as error:
        raise SystemExit(f"git {args[0] if args else ''} failed") from error


def remove_git(path: pathlib.Path):
    for root, _, files in os.walk(path):
        for name in files:
            try:
                os.chmod(os.path.join(root, name), stat.S_IWRITE)
            except OSError:
                pass
    shutil.rmtree(path)

def push_repo(path: pathlib.Path, name: str, message: str):
    ensure_repo(name)
    git("init", "-b", "main", cwd=path)
    git("config", "user.name", "PackFrame Mirror", cwd=path)
    git("config", "user.email", "packframe@example.invalid", cwd=path)
    git("add", "-A", cwd=path)
    git("commit", "-m", message, cwd=path)
    url = f"https://oauth2:{TOKEN}@gitee.com/{GITEE_OWNER}/{name}.git"
    git("push", "--force", url, "HEAD:main", cwd=path)


def rewrite_pack(repo_dir: pathlib.Path, name: str):
    manifest_path = repo_dir / "pack.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    base = raw_base(name)
    image = manifest.get("image", "images/cover.png")
    for candidate in ("images/cover.jpg", "images/cover-small.png"):
        if (repo_dir / candidate).exists():
            image = candidate
            break
    manifest["image"] = base + "/" + str(image).lstrip("/")
    if manifest.get("configFiles"):
        manifest["configBaseUrl"] = base + "/config"
    archive = str(manifest.get("modsArchive") or "").strip()
    if archive and "://" not in archive:
        manifest["modsArchive"] = base + "/" + archive.lstrip("/")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def mirror_pack(entry: dict, work: pathlib.Path):
    if not entry.get("file"):
        return
    repo = str(entry.get("repo") or "").strip()
    if "/" not in repo:
        raise SystemExit(f"invalid pack repo: {repo!r}")
    name = repo.rsplit("/", 1)[1]
    target = work / name
    git("clone", "--depth", "1", f"https://github.com/{repo}.git", str(target))
    remove_git(target / ".git")
    rewrite_pack(target, name)
    push_repo(target, name, "Mirror from GitHub")


def mirror_index(work: pathlib.Path):
    target = work / INDEX_REPO
    shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git"))
    index_path = target / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8-sig"))
    for entry in index.get("packs", []):
        repo = str(entry.get("repo") or "")
        name = repo.rsplit("/", 1)[-1]
        ref = entry.get("ref") or "main"
        manifest = entry.get("manifest") or "pack.json"
        entry["giteeFile"] = f"https://gitee.com/{GITEE_OWNER}/{name}/raw/{ref}/{manifest}"
        if entry.get("file"):
            entry["file"] = f"https://raw.githubusercontent.com/{repo}/{ref}/{manifest}"
        pack_path = target / "packs" / (str(entry.get("id", "")) + ".json")
        if pack_path.exists():
            pack = json.loads(pack_path.read_text(encoding="utf-8-sig"))
            pack["giteeFile"] = entry["giteeFile"]
            if entry.get("file"):
                pack["file"] = entry["file"]
            else:
                pack.pop("file", None)
            pack_path.write_text(
                json.dumps(pack, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    push_repo(target, INDEX_REPO, "Mirror index from GitHub")


def main():
    if not TOKEN:
        raise SystemExit("GITEE_TOKEN is not set")
    index = json.loads((ROOT / "index.json").read_text(encoding="utf-8-sig"))
    with tempfile.TemporaryDirectory(prefix="packframe-gitee-") as temp:
        work = pathlib.Path(temp)
        for entry in index.get("packs", []):
            mirror_pack(entry, work)
        mirror_index(work)
    print("Gitee mirror complete")


if __name__ == "__main__":
    main()
