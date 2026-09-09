#!/usr/bin/env python3
import csv
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.github.com"
ORG = "CSC-17-01"
SOURCE_REPOSITORY = "TrangLe1912/csc4007-hello-nlp-starter"
REPO_PREFIX = "csc4007-hello-nlp"
ROSTER = Path(__file__).with_name("khmt17-01-roster.csv")


def api(method, path, token, body=None, accepted=(200,)):
    url = f"{API}{path}"
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "CSC4007-class-distributor",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8")
            parsed = json.loads(payload) if payload else {}
            if response.status not in accepted:
                raise RuntimeError(f"HTTP {response.status}: {parsed}")
            return response.status, parsed
    except urllib.error.HTTPError as error:
        payload = error.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(payload)
            message = parsed.get("message", payload)
        except json.JSONDecodeError:
            message = payload
        if error.code in accepted:
            return error.code, {"message": message}
        raise RuntimeError(f"HTTP {error.code}: {message}") from error


def load_roster():
    with ROSTER.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"student_id", "full_name", "github_username"}
    if not rows or not required.issubset(rows[0]):
        raise RuntimeError("Roster thiếu cột bắt buộc")
    seen_ids, seen_users = set(), set()
    for row in rows:
        for key in required:
            row[key] = row[key].strip()
            if not row[key]:
                raise RuntimeError(f"Roster có giá trị trống: {row}")
        user_key = row["github_username"].lower()
        if row["student_id"] in seen_ids or user_key in seen_users:
            raise RuntimeError(f"Roster có MSSV hoặc username trùng: {row}")
        seen_ids.add(row["student_id"])
        seen_users.add(user_key)
    return rows


def run(command, cwd=None, env=None):
    subprocess.run(command, cwd=cwd, env=env, check=True)


def publish_assignment(repo, token):
    excluded_prefix = ".github/classroom/"
    excluded_files = {".github/workflows/distribute-khmt17-01.yml"}
    tracked = subprocess.run(
        ["git", "ls-files", "-z"], check=True, capture_output=True
    ).stdout.decode("utf-8").split("\0")
    assignment_files = [
        path for path in tracked
        if path and not path.startswith(excluded_prefix) and path not in excluded_files
    ]
    if not assignment_files:
        raise RuntimeError("Không tìm thấy file bài tập để phát")

    with tempfile.TemporaryDirectory(prefix="csc4007-") as temp_dir:
        target = Path(temp_dir) / "assignment"
        target.mkdir()
        for relative in assignment_files:
            source = Path(relative)
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        run(["git", "init", "-b", "main"], cwd=target)
        run(["git", "config", "user.name", "CSC4007 Class Distributor"], cwd=target)
        run(["git", "config", "user.email", "noreply@dnu.edu.vn"], cwd=target)
        run(["git", "add", "."], cwd=target)
        run(["git", "commit", "-m", "Initial CSC4007 assignment"], cwd=target)

        askpass = Path(temp_dir) / "git-askpass.sh"
        askpass.write_text(
            '#!/bin/sh\ncase "$1" in\n  *Username*) printf "%s\\n" "x-access-token" ;;\n  *) printf "%s\\n" "$CLASSROOM_PAT" ;;\nesac\n',
            encoding="utf-8",
        )
        askpass.chmod(askpass.stat().st_mode | stat.S_IXUSR)
        push_env = os.environ.copy()
        push_env.update({
            "CLASSROOM_PAT": token,
            "GIT_ASKPASS": str(askpass),
            "GIT_TERMINAL_PROMPT": "0",
        })
        run(
            ["git", "push", f"https://github.com/{ORG}/{repo}.git", "HEAD:main"],
            cwd=target,
            env=push_env,
        )


def escape(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def write_summary(results, dry_run):
    lines = [
        f"## {'Chạy thử' if dry_run else 'Kết quả phát bài'} – KHMT 17-01",
        "",
        "| MSSV | Sinh viên | GitHub | Repository | Kết quả |",
        "|---|---|---|---|---|",
    ]
    for item in results:
        lines.append(
            "| {student_id} | {full_name} | @{github_username} | [{repo}](https://github.com/{org}/{repo}) | {status} |".format(
                org=ORG, **{key: escape(value) for key, value in item.items()}
            )
        )
    summary = "\n".join(lines) + "\n"
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(summary)
    print(summary)


def main():
    if os.getenv("GITHUB_REPOSITORY") != SOURCE_REPOSITORY:
        raise RuntimeError(f"Workflow chỉ được chạy tại {SOURCE_REPOSITORY}")
    token = os.getenv("CLASSROOM_PAT", "").strip()
    if not token:
        raise RuntimeError("Thiếu Actions secret CLASSROOM_PAT")
    dry_run = os.getenv("DRY_RUN", "true").lower() == "true"
    rows = load_roster()
    results = []

    for row in rows:
        username = row["github_username"]
        repo = f"{REPO_PREFIX}-{row['student_id']}"
        result = {**row, "repo": repo, "status": ""}
        try:
            quoted_user = urllib.parse.quote(username, safe="")
            api("GET", f"/users/{quoted_user}", token, accepted=(200,))
            repo_path = f"/repos/{ORG}/{repo}"
            existing = None
            try:
                _, existing = api("GET", repo_path, token, accepted=(200,))
                repo_exists = True
            except RuntimeError as error:
                if not str(error).startswith("HTTP 404:"):
                    raise
                repo_exists = False

            if dry_run:
                result["status"] = "Đã tồn tại; sẽ kiểm tra lời mời" if repo_exists else "Sẵn sàng tạo, chép bài và mời"
            else:
                if not repo_exists:
                    api(
                        "POST",
                        f"/orgs/{ORG}/repos",
                        token,
                        body={
                            "name": repo,
                            "description": f"CSC4007 – KHMT 17-01 – {row['student_id']} – {row['full_name']}",
                            "private": True,
                            "has_issues": True,
                            "has_projects": False,
                            "has_wiki": False,
                            "auto_init": False,
                        },
                        accepted=(201,),
                    )
                    publish_assignment(repo, token)
                    time.sleep(1)
                elif not existing.get("default_branch"):
                    publish_assignment(repo, token)
                status, _ = api(
                    "PUT",
                    f"/repos/{ORG}/{repo}/collaborators/{quoted_user}",
                    token,
                    body={"permission": "push"},
                    accepted=(201, 204),
                )
                result["status"] = "Đã tạo, chép bài và gửi lời mời" if not repo_exists and status == 201 else (
                    "Đã gửi lời mời" if status == 201 else "Đã có quyền truy cập"
                )
        except Exception as error:
            result["status"] = f"LỖI: {error}"
        results.append(result)

    write_summary(results, dry_run)
    failures = [item for item in results if item["status"].startswith("LỖI:")]
    if failures:
        print(f"Có {len(failures)} lỗi; xem bảng Summary.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
