#!/usr/bin/env python3
"""Build the AI Agent Incident Tracker site.

Reads every YAML file in incidents/, validates required fields, and writes:
  docs/index.html      — browsable, filterable static page (GitHub Pages)
  docs/incidents.json  — machine-readable dataset for anyone to build on

No LLMs, no API keys, no external services. Run: python build_site.py
"""
from __future__ import annotations

import html
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

REQUIRED = ["id", "date", "title", "system", "vendor", "category", "status", "failure_mode", "impact", "sources"]


def load_incidents() -> list[dict]:
    items, errors = [], []
    for f in sorted(Path("incidents").glob("*.yml")) + sorted(Path("incidents").glob("*.yaml")):
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
            missing = [k for k in REQUIRED if not data.get(k)]
            if missing:
                errors.append(f"{f.name}: missing {', '.join(missing)}")
                continue
            data["_file"] = f.name
            items.append(data)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{f.name}: {exc}")
    if errors:
        print("VALIDATION ERRORS:\n  " + "\n  ".join(errors), file=sys.stderr)
        raise SystemExit(1)
    items.sort(key=lambda x: str(x["date"]), reverse=True)
    return items


def esc(v) -> str:
    return html.escape(str(v).strip())


def card(it: dict) -> str:
    lessons = "".join(f"<li>{esc(l)}</li>" for l in it.get("lessons", []))
    sources = " · ".join(
        f'<a href="{esc(s)}" target="_blank" rel="noopener">source {i + 1}</a>'
        for i, s in enumerate(it.get("sources", []))
    )
    return f"""
    <article class="card" data-category="{esc(it['category'])}" data-vendor="{esc(it['vendor'])}">
      <div class="meta"><span class="tag">{esc(it['category'])}</span>
        <span class="mono">{esc(it['date'])} · {esc(it['id'])}</span></div>
      <h2>{esc(it['title'])}</h2>
      <div class="mono sub">{esc(it['system'])} — {esc(it['vendor'])} · status: {esc(it['status'])}</div>
      <p><strong>Failure mode.</strong> {esc(it['failure_mode'])}</p>
      <p><strong>Impact.</strong> {esc(it['impact'])}</p>
      {f'<p><strong>Autonomy.</strong> {esc(it["autonomy"])}</p>' if it.get('autonomy') else ''}
      {f'<div><strong>Lessons</strong><ul>{lessons}</ul></div>' if lessons else ''}
      <div class="sources">{sources}</div>
    </article>"""


def build(items: list[dict]) -> str:
    cats = sorted({it["category"] for it in items})
    buttons = '<button class="f on" data-f="all">All</button>' + "".join(
        f'<button class="f" data-f="{esc(c)}">{esc(c)}</button>' for c in cats
    )
    cards = "".join(card(it) for it in items)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Agent Incident Tracker</title>
<style>
  :root {{ --bg:#F2F3F1; --panel:#fff; --ink:#10151F; --soft:#4A5160; --line:#D7DAD5; --accent:#2038D6; --amber:#B26A00; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.55 -apple-system,'Segoe UI',Helvetica,Arial,sans-serif; }}
  .mono {{ font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace; }}
  .shell {{ max-width:880px; margin:0 auto; padding:0 20px 64px; }}
  header {{ border-bottom:3px solid var(--ink); padding:28px 0 14px; }}
  .stamp {{ font-size:11px; letter-spacing:.14em; color:var(--soft); display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; }}
  h1 {{ font-size:clamp(30px,6vw,44px); letter-spacing:-.03em; margin:6px 0 2px; }}
  .lede {{ color:var(--soft); font-size:14px; padding-bottom:10px; }}
  .filters {{ margin:20px 0; }}
  .f {{ font-family:ui-monospace,Menlo,monospace; font-size:11px; padding:6px 12px; border:1px solid var(--line); background:transparent; color:var(--soft); cursor:pointer; margin:0 6px 6px 0; }}
  .f.on {{ background:var(--accent); border-color:var(--accent); color:#fff; }}
  .card {{ background:var(--panel); border:1px solid var(--line); padding:18px 20px; margin-bottom:12px; }}
  .meta {{ display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap; font-size:11px; }}
  .tag {{ font-family:ui-monospace,Menlo,monospace; font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--amber); }}
  .meta .mono {{ color:var(--soft); }}
  .card h2 {{ font-size:18px; margin:6px 0 4px; letter-spacing:-.01em; }}
  .sub {{ font-size:12px; color:var(--soft); margin-bottom:10px; }}
  .card p {{ margin:0 0 8px; font-size:14px; }}
  .card ul {{ margin:4px 0 8px; padding-left:20px; font-size:14px; }}
  .sources a {{ color:var(--accent); font-weight:600; text-decoration:none; font-size:13px; }}
  a:focus-visible, button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
  footer {{ margin-top:32px; font-size:12px; color:var(--soft); }}
  footer a {{ color:var(--accent); }}
</style></head>
<body><div class="shell">
<header>
  <div class="stamp mono"><span>OPEN DATASET // COMMUNITY MAINTAINED</span><span>BUILT {stamp}</span></div>
  <h1>AI Agent Incident Tracker</h1>
  <div class="lede">A structured, sourced record of real-world AI agent failures — destructive actions, prompt-injection exploits, and agentic supply-chain compromises. {len(items)} incidents. Add one via pull request.</div>
</header>
<div class="filters">{buttons}</div>
{cards}
<footer>Dataset: <a href="incidents.json">incidents.json</a> · Contribute: add a YAML file to <span class="mono">incidents/</span> — see the repo README. Entries marked "user-reported" reflect public accounts, not confirmed forensics.</footer>
</div>
<script>
  document.querySelectorAll('.f').forEach(b => b.addEventListener('click', () => {{
    document.querySelectorAll('.f').forEach(x => x.classList.remove('on'));
    b.classList.add('on');
    const f = b.dataset.f;
    document.querySelectorAll('.card').forEach(c => {{
      c.style.display = (f === 'all' || c.dataset.category === f) ? '' : 'none';
    }});
  }}));
</script>
</body></html>"""


def main() -> int:
    items = load_incidents()
    out = Path("docs")
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(build(items), encoding="utf-8")

    def clean(it: dict) -> dict:
        d = {k: v for k, v in it.items() if not k.startswith("_")}
        if isinstance(d.get("date"), date):
            d["date"] = d["date"].isoformat()
        return d

    (out / "incidents.json").write_text(
        json.dumps([clean(i) for i in items], indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Built docs/index.html and docs/incidents.json ({len(items)} incidents).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
