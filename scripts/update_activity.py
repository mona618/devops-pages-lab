"""Publish recent public GitHub events inside the README activity markers."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START = "<!--START_SECTION:activity-->"
END = "<!--END_SECTION:activity-->"
USER = "mona618"
REPOSITORY = "mona618/devops-pages-lab"


def github_json(path: str) -> list[dict]:
    token = os.environ.get("GH_TOKEN", "")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "devops-pages-lab-activity-updater",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com{path}", headers=headers)
    try:
        with urlopen(request, timeout=20) as response:
            result = json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"GitHub public API returned HTTP {error.code} for {path}") from error
    if not isinstance(result, list):
        raise RuntimeError(f"Expected a list from GitHub public API: {path}")
    return result


def event_line(event: dict) -> str | None:
    repository = event.get("repo", {}).get("name", "")
    if not repository or not repository.startswith(f"{USER}/"):
        return None
    kind = event.get("type", "")
    payload = event.get("payload", {})
    date = str(event.get("created_at", ""))[:10]
    repo_url = f"https://github.com/{repository}"
    if kind == "PushEvent":
        head = payload.get("head", "")
        link = f"{repo_url}/commit/{head}" if head else repo_url
        action = "pushed a public commit"
    elif kind == "CreateEvent":
        link = repo_url
        action = f"created a public {payload.get('ref_type', 'repository')}"
    elif kind == "PullRequestEvent":
        pr = payload.get("pull_request", {})
        link = pr.get("html_url", repo_url)
        action = f"{payload.get('action', 'updated')} a pull request"
    elif kind == "IssuesEvent":
        issue = payload.get("issue", {})
        link = issue.get("html_url", repo_url)
        action = f"{payload.get('action', 'updated')} an issue"
    elif kind == "ReleaseEvent":
        release = payload.get("release", {})
        link = release.get("html_url", repo_url)
        action = "published a release"
    else:
        return None
    return f"- {date} · {action} in [{repository}]({link})"


def recent_lines() -> tuple[list[str], str]:
    events = github_json(f"/users/{USER}/events/public?per_page=30")
    lines = []
    seen = set()
    for event in events:
        line = event_line(event)
        if line and line not in seen:
            lines.append(line)
            seen.add(line)
        if len(lines) == 8:
            break
    if lines:
        return lines, "public user events"

    # New repositories may take time to appear in the public events feed.
    commits = github_json(f"/repos/{REPOSITORY}/commits?per_page=8")
    for commit in commits:
        sha = commit.get("sha", "")
        message = commit.get("commit", {}).get("message", "").splitlines()[0]
        date = commit.get("commit", {}).get("committer", {}).get("date", "")[:10]
        if sha and message:
            safe_message = message.replace("[", "\\[").replace("]", "\\]")
            lines.append(f"- {date} · {safe_message} ([{sha[:7]}](https://github.com/{REPOSITORY}/commit/{sha}))")
    if not lines:
        raise RuntimeError("No verifiable public events or commits were returned")
    return lines, "public repository commits (feed fallback)"


def main() -> None:
    original = README.read_text(encoding="utf-8")
    if original.count(START) != 1 or original.count(END) != 1:
        raise RuntimeError("Expected exactly one pair of activity markers")
    lines, source = recent_lines()
    body = "\n".join(lines)
    updated = original[: original.index(START) + len(START)] + "\n" + body + "\n" + original[original.index(END) :]
    README.write_text(updated, encoding="utf-8")
    print(f"PASS: refreshed {len(lines)} activity entries from {source}")
    print(f"Updated at {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()

