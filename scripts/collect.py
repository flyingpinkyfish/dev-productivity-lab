"""Snapshot GitHub delivery data and probe the deployed app."""

import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}"
TOKEN = os.environ["GITHUB_TOKEN"]
APP_URL = os.environ.get("APP_URL", "").rstrip("/")
OUT = Path("data_out")


def get(url):
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def pages(path):
    items = []
    page = 1
    sep = "&" if "?" in path else "?"
    while True:
        batch = get(f"{API}/{path}{sep}per_page=100&page={page}")
        if isinstance(batch, dict):
            batch = batch.get("workflow_runs", [])
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def collect_prs():
    rows = []
    for pr in pages("pulls?state=all"):
        number = pr["number"]
        detail = get(f"{API}/pulls/{number}")
        commits = get(f"{API}/pulls/{number}/commits?per_page=100")
        reviews = get(f"{API}/pulls/{number}/reviews")
        first = commits[0]["commit"]["author"]["date"] if commits else None
        rows.append(
            {
                "number": number,
                "title": pr["title"],
                "labels": [label["name"] for label in pr["labels"]],
                "created_at": pr["created_at"],
                "first_commit_at": first,
                "merged_at": pr["merged_at"],
                "closed_at": pr["closed_at"],
                "commits": detail["commits"],
                "additions": detail["additions"],
                "deletions": detail["deletions"],
                "changed_files": detail["changed_files"],
                "reviews": len(reviews),
                "merge_commit_sha": pr["merge_commit_sha"],
            }
        )
    return rows


def collect_runs():
    rows = []
    for run in pages("actions/runs"):
        rows.append(
            {
                "id": run["id"],
                "name": run["name"],
                "event": run["event"],
                "branch": run["head_branch"],
                "sha": run["head_sha"],
                "status": run["status"],
                "conclusion": run["conclusion"],
                "created_at": run["created_at"],
                "run_started_at": run["run_started_at"],
                "updated_at": run["updated_at"],
            }
        )
    return rows


def probe():
    if not APP_URL:
        return None
    started = time.monotonic()
    try:
        with urllib.request.urlopen(f"{APP_URL}/health", timeout=90) as response:
            code = response.status
    except urllib.error.HTTPError as error:
        code = error.code
    except OSError:
        code = None
    return {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": code,
        "seconds": round(time.monotonic() - started, 2),
    }


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "prs.json").write_text(json.dumps(collect_prs(), indent=2))
    (OUT / "runs.json").write_text(json.dumps(collect_runs(), indent=2))
    result = probe()
    if result:
        (OUT / "probe.json").write_text(json.dumps(result))


if __name__ == "__main__":
    main()
