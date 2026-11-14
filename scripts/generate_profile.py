#!/usr/bin/env python3
"""Generate self-contained SVG cards using GitHub's public REST API.

No third-party statistics service is used. The workflow's GITHUB_TOKEN is
used only for API authentication/rate-limit headroom; no PAT is required.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path

USERNAME = os.getenv("GITHUB_USERNAME", "m-arslan009")
TOKEN = os.getenv("GITHUB_TOKEN", "")
OUT = Path("assets")
OUT.mkdir(exist_ok=True)

BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
TEXT = "#e6edf3"
MUTED = "#8b949e"
BLUE = "#58a6ff"
GREEN = "#3fb950"
PURPLE = "#bc8cff"
ORANGE = "#d29922"

def api(path: str):
    url = "https://api.github.com" + path
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-dashboard-generator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))

def svg_start(title: str, subtitle: str, width=1000, height=260):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        f'<rect width="{width}" height="{height}" rx="18" fill="{BG}"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="17" fill="none" stroke="{BORDER}"/>',
        f'<text x=" thirty " y="40" fill="{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="21" font-weight="700">{escape(title)}</text>'.replace('x=" thirty "', 'x="30"'),
        f'<text x="30" y="65" fill="{MUTED}" font-family="Segoe UI,Arial,sans-serif" font-size="12">{escape(subtitle)}</text>',
    ]

def write_svg(name, parts):
    parts.append("</svg>")
    (OUT / name).write_text("\n".join(parts), encoding="utf-8")

def card(x, y, w, h, label, value, accent):
    return [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>',
        f'<rect x="{x}" y="{y}" width="4" height="{h}" rx="2" fill="{accent}"/>',
        f'<text x="{x+18}" y="{y+29}" fill="{MUTED}" font-family="Segoe UI,Arial,sans-serif" font-size="12">{escape(label.upper())}</text>',
        f'<text x="{x+18}" y="{y+67}" fill="{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="29" font-weight="700">{escape(str(value))}</text>',
    ]

def main():
    user = api(f"/users/{urllib.parse.quote(USERNAME)}")
    repos = api(f"/users/{urllib.parse.quote(USERNAME)}/repos?per_page=100&sort=updated")
    events = api(f"/users/{urllib.parse.quote(USERNAME)}/events/public?per_page=100")

    public_repos = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    forks = sum(r.get("forks_count", 0) for r in repos)
    languages = Counter()
    for repo in public_repos:
        lang = repo.get("language")
        if lang:
            languages[lang] += 1

    now = datetime.now(timezone.utc)
    recent_events = []
    for event in events:
        try:
            when = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00"))
            if (now - when).days <= 30:
                recent_events.append(event)
        except (KeyError, ValueError):
            pass

    # Main dashboard
    p = svg_start("ENGINEERING DASHBOARD", f"@{USERNAME}  •  PUBLIC REPOSITORY SNAPSHOT  •  UPDATED {now:%Y-%m-%d UTC}", height=210)
    metrics = [
        ("Public repositories", user.get("public_repos", 0), BLUE),
        ("Followers", user.get("followers", 0), PURPLE),
        ("Stars received", stars, GREEN),
        ("Forks received", forks, ORANGE),
    ]
    x_positions = [30, 270, 510, 750]
    for x, (label, value, accent) in zip(x_positions, metrics):
        p += card(x, 90, 220, 90, label, value, accent)
    write_svg("dashboard.svg", p)

    # Languages by repository count, not code bytes: clear and reproducible.
    p = svg_start("LANGUAGE FOOTPRINT", "Primary language declared by each non-fork public repository", height=300)
    top = languages.most_common(7)
    if not top:
        p.append(f'<text x="30" y="125" fill="{MUTED}" font-family="Segoe UI,Arial,sans-serif" font-size="15">No public repository language data available yet.</text>')
    else:
        max_count = max(v for _, v in top) or 1
        palette = [BLUE, PURPLE, GREEN, ORANGE, "#f778ba", "#79c0ff", "#d2a8ff"]
        for i, (lang, count) in enumerate(top):
            y = 105 + i * 26
            p.append(f'<text x="30" y="{y+13}" fill="{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="13">{escape(lang)}</text>')
            p.append(f'<rect x="210" y="{y}" width="650" height="13" rx="6" fill="{PANEL}"/>')
            p.append(f'<rect x="210" y="{y}" width="{max(4, 650*count/max_count):.1f}" height="13" rx="6" fill="{palette[i % len(palette)]}"/>')
            p.append(f'<text x="885" y="{y+12}" fill="{MUTED}" font-family="Segoe UI,Arial,sans-serif" font-size="12">{count} repos</text>')
    write_svg("languages.svg", p)

    # Recent public event sample; events API is not a complete contribution ledger.
    p = svg_start("RECENT PUBLIC ACTIVITY", "Public GitHub events observed in the last 30 days (GitHub Events API)", height=250)
    counts = Counter(e.get("type", "Other").replace("Event", "") for e in recent_events)
    if not counts:
        p.append(f'<text x="30" y="125" fill="{MUTED}" font-family="Segoe UI,Arial,sans-serif" font-size="15">No recent public events returned by GitHub.</text>')
    else:
        top_events = counts.most_common(5)
        max_count = max(v for _, v in top_events) or 1
        for i, (kind, count) in enumerate(top_events):
            y = 100 + i * 28
            p.append(f'<text x="30" y="{y+13}" fill="{TEXT}" font-family="Segoe UI,Arial,sans-serif" font-size="13">{escape(kind)}</text>')
            p.append(f'<rect x="260" y="{y}" width="560" height="13" rx="6" fill="{PANEL}"/>')
            p.append(f'<rect x="260" y="{y}" width="{max(4, 560*count/max_count):.1f}" height="13" rx="6" fill="{BLUE}"/>')
            p.append(f'<text x="850" y="{y+12}" fill="{MUTED}" font-family="Segoe UI,Arial,sans-serif" font-size="12">{count}</text>')
    write_svg("activity.svg", p)

    print(f"Generated dashboard for {USERNAME}: {len(repos)} repositories returned, {len(recent_events)} recent public events.")

if __name__ == "__main__":
    main()
