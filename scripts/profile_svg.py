"""프로필 README에 쓰는 SVG를 라이트·다크 두 벌로 만든다.

    python3 scripts/profile_svg.py            # assets/에 생성 (GitHub API 필요)
    python3 scripts/profile_svg.py --static   # 애니메이션 없이 생성 (캡처 확인용)

TELEMETRY 수치는 GitHub GraphQL API에서 받는다. 토큰은 GITHUB_TOKEN 또는 GH_TOKEN 환경 변수에서 읽는다.
글꼴은 fonts/의 IBM Plex Mono·IBM Plex Sans KR(SIL OFL 1.1)에서 SVG마다 쓰인 글자만 잘라 WOFF2로 넣는다.
OFL의 예약 글꼴 이름("Plex")을 피하려고 잘라 낸 글꼴은 이름 정보를 지우고 다른 이름으로 부른다.
필요 패키지: fonttools, brotli
레이아웃 아이디어는 github.com/Sharann-del 프로필을 참고했고, 코드와 그림은 새로 작성했다.
"""
import argparse
import base64
import html
import io
import json
import os
import re
import urllib.request
from collections import OrderedDict
from datetime import date
from pathlib import Path

LOGIN = "isle-blu"
ROOT = Path(__file__).resolve().parent.parent
FONTS = [  # (CSS에서 부를 이름, 파일) — 앞에 있는 글꼴부터 글자를 찾는다
    ("ProfileMono", ROOT / "fonts" / "IBMPlexMono-Regular.ttf"),
    ("ProfileKR", ROOT / "fonts" / "IBMPlexSansKR-Regular.ttf"),
]
MONO = ('"ProfileMono", "ProfileKR", ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, "Liberation Mono", '
        '"D2Coding", "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", monospace')

THEMES = {
    "light": dict(ink="#1F2328", muted="#59636E", faint="#D0D7DE", accent="#1D4ED8", bar="#93B4F5"),
    "dark": dict(ink="#E6EDF3", muted="#9198A1", faint="#30363D", accent="#3B82F6", bar="#1E3A8A"),
}

STATIC = False


# ── 공통 ─────────────────────────────────────────────

def style(t):
    anim = "" if STATIC else """
    .draw { stroke-dasharray: 1200; stroke-dashoffset: 1200; animation: draw 1.2s cubic-bezier(.6,0,.2,1) forwards; }
    @keyframes draw { to { stroke-dashoffset: 0; } }
    .rise { opacity: 0; animation: rise .8s cubic-bezier(.2,.7,.2,1) forwards; }
    @keyframes rise { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
    .grow { transform-box: fill-box; transform-origin: bottom; transform: scaleY(0); animation: grow .7s cubic-bezier(.2,.7,.2,1) forwards; }
    @keyframes grow { to { transform: scaleY(1); } }
    .a1 { animation-delay: .1s } .a2 { animation-delay: .35s } .a3 { animation-delay: .6s } .a4 { animation-delay: .85s } .a5 { animation-delay: 1.1s }
    @media (prefers-reduced-motion: reduce) { .draw, .rise, .grow { animation: none; opacity: 1; stroke-dashoffset: 0; transform: none; } }"""
    return f"""<style>
    text {{ font-family: {MONO}; }}
    .ink {{ fill: {t['ink']}; }} .muted {{ fill: {t['muted']}; }} .accent {{ fill: {t['accent']}; }}{anim}
  </style>"""


_font_cache = {}


def subset_woff2(path, chars):
    """글꼴에서 chars에 해당하는 글자만 남긴 WOFF2를 base64로 돌려준다."""
    key = (path, chars)
    if key not in _font_cache:
        import logging
        from fontTools import subset
        from fontTools.ttLib import TTFont
        logging.getLogger("fontTools.subset").setLevel(logging.ERROR)
        font = TTFont(path)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.name_IDs = []          # 이름 정보 제거 (예약 글꼴 이름 회피)
        opts.layout_features = ["kern", "liga"]
        sub = subset.Subsetter(opts)
        sub.populate(text=chars)
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        _font_cache[key] = base64.b64encode(buf.getvalue()).decode()
    return _font_cache[key]


def font_faces(body):
    chars = "".join(sorted(set(html.unescape("".join(re.findall(r">([^<>]+)<", body))))))
    faces = []
    for name, path in FONTS:
        data = subset_woff2(str(path), chars)
        faces.append(f'@font-face {{ font-family: "{name}"; src: url(data:font/woff2;base64,{data}) format("woff2"); }}')
    return "\n    ".join(faces)


def svg(t, height, label, body):
    css = style(t).replace("<style>", "<style>\n    " + font_faces(body), 1)
    return (f'<svg viewBox="0 0 1000 {height}" fill="none" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{label}">\n  {css}\n{body}</svg>\n')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── 헤더와 섹션 구분선 ───────────────────────────────

def header(t):
    return svg(t, 300, "양덕관 Deokkwan Yang — 백엔드 개발자", f"""
  <g class="rise a1">
    <text class="muted" x="0" y="28" font-size="14" letter-spacing="2">BACKEND ENGINEER — PROFILE Nº 001</text>
    <text class="muted" x="1000" y="28" font-size="14" letter-spacing="2" text-anchor="end">GITHUB / ISLE-BLU</text>
  </g>
  <line class="draw a1" x1="0" y1="46" x2="1000" y2="46" stroke="{t['faint']}"/>
  <text class="ink rise a2" x="-4" y="150" font-size="76">양덕관</text>
  <text class="muted rise a2" x="252" y="150" font-size="26">Deokkwan Yang</text>
  <text class="muted rise a3" x="0" y="196" font-size="20" letter-spacing="1">Java · Spring · CI/CD · Monitoring</text>
  <line class="draw a3" x1="0" y1="232" x2="1000" y2="232" stroke="{t['faint']}"/>
  <g class="rise a4">
    <text class="muted" x="0" y="270" font-size="14" letter-spacing="2">STATUS</text>
    <text class="accent" x="100" y="270" font-size="18">신입 백엔드 포지션 구직 중</text>
  </g>
""")


SECTIONS = [
    ("s01", "01", "기술 스택", "DAILY TOOLS"),
    ("s02", "02", "요즘 하는 일", "IN PROGRESS"),
    ("s03", "03", "프로젝트", "SELECTED WORK"),
    ("s04", "04", "활동 지표", "LAST 12 MONTHS"),
    ("s05", "05", "연표", "SO FAR"),
]


def section(t, num, name, note):
    return svg(t, 90, f"{num} — {name}", f"""
  <g class="rise a1">
    <text class="accent" x="-2" y="56" font-size="48" letter-spacing="-1">{num}</text>
    <text class="ink" x="86" y="54" font-size="20" letter-spacing="0">— {name}</text>
    <text class="muted" x="1000" y="54" font-size="14" letter-spacing="2" text-anchor="end">{note}</text>
  </g>
  <line class="draw a2" x1="0" y1="80" x2="1000" y2="80" stroke="{t['faint']}"/>
""")


# ── FIG.01 활동 지표 ─────────────────────────────────

QUERY = """query($login: String!) { user(login: $login) { contributionsCollection {
  totalCommitContributions totalPullRequestContributions totalPullRequestReviewContributions totalIssueContributions
  contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }"""


def fetch_stats():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN 또는 GH_TOKEN 환경 변수가 필요합니다.")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        body = json.load(res)
    if "errors" in body:
        raise SystemExit(f"GraphQL 오류: {body['errors']}")
    c = body["data"]["user"]["contributionsCollection"]
    months = OrderedDict()
    for week in c["contributionCalendar"]["weeks"]:
        for d in week["contributionDays"]:
            months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["contributionCount"]
    return dict(
        commits=c["totalCommitContributions"],
        prs=c["totalPullRequestContributions"],
        reviews=c["totalPullRequestReviewContributions"],
        issues=c["totalIssueContributions"],
        total=c["contributionCalendar"]["totalContributions"],
        months=list(months.items())[-12:],
    )


def fig_telemetry(t, s):
    counters = [("COMMITS", s["commits"]), ("PULL REQUESTS", s["prs"]),
                ("REVIEWS", s["reviews"]), ("ISSUES", s["issues"])]
    parts = [f"""
  <text class="muted rise a1" x="0" y="20" font-size="14" letter-spacing="2">FIG. 01</text>
  <text class="muted rise a1" x="1000" y="20" font-size="14" letter-spacing="2" text-anchor="end">UPDATED {date.today():%Y.%m.%d}</text>"""]
    for i, (label, value) in enumerate(counters):
        x, y = (i % 2) * 190, 96 + (i // 2) * 110
        parts.append(f"""
  <g class="rise a{i + 1}">
    <text class="ink" x="{x}" y="{y}" font-size="52" letter-spacing="-1">{value:,}</text>
    <text class="muted" x="{x}" y="{y + 28}" font-size="14" letter-spacing="2">{label}</text>
  </g>""")
    # 월별 기여 막대
    cx0, cw, base, top = 440, 560, 300, 100
    months = s["months"]
    peak = max(v for _, v in months) or 1
    step = cw / len(months)
    bw = step * 0.62
    parts.append(f"""
  <text class="muted rise a1" x="{cx0}" y="56" font-size="14" letter-spacing="2">CONTRIBUTIONS / MONTH</text>
  <text class="accent rise a1" x="1000" y="56" font-size="14" letter-spacing="0" text-anchor="end">{s['total']:,} total</text>
  <line class="draw a1" x1="{cx0}" y1="{base}" x2="1000" y2="{base}" stroke="{t['faint']}"/>""")
    for i, (ym, v) in enumerate(months):
        h = (base - top) * v / peak
        x = cx0 + i * step + (step - bw) / 2
        is_peak = v == peak
        fill = t["accent"] if is_peak else t["bar"]
        parts.append(f"""
  <rect class="grow a{min(i // 3 + 1, 5)}" x="{x:.1f}" y="{base - h:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{fill}"/>
  <text class="muted" x="{x + bw / 2:.1f}" y="{base + 24}" font-size="14" text-anchor="middle">{int(ym[5:])}</text>""")
        if is_peak:
            parts.append(f"""
  <text class="accent rise a5" x="{x + bw / 2:.1f}" y="{base - h - 10:.1f}" font-size="14" text-anchor="middle">{v}</text>""")
    return svg(t, 340, "활동 지표: 최근 12개월 커밋, PR, 리뷰, 이슈 수와 월별 기여", "".join(parts) + "\n")


# ── FIG.02 연표 ──────────────────────────────────

EVENTS = [
    ("2021.03", "GitHub 시작", "first repositories"),
    ("2026.08", "Showmoa", "CTO · data sync"),
    ("2026.10", "test moa", "realtime chat"),
    ("2026.11", "Pawmento", "infra · CI"),
    ("NOW", "구직 중", "junior backend"),
]


def fig_timeline(t):
    y = 110
    xs = [20, 230, 420, 610, 980]
    parts = [f"""
  <text class="muted rise a1" x="0" y="20" font-size="14" letter-spacing="2">FIG. 02</text>
  <line class="draw a1" x1="20" y1="{y}" x2="980" y2="{y}" stroke="{t['faint']}"/>
  <g class="rise a2">
    <line x1="128" y1="{y - 10}" x2="120" y2="{y + 10}" stroke="{t['muted']}"/>
    <line x1="138" y1="{y - 10}" x2="130" y2="{y + 10}" stroke="{t['muted']}"/>
  </g>"""]
    for i, ((when, title, sub), x) in enumerate(zip(EVENTS, xs)):
        last = i == len(EVENTS) - 1
        anchor = "end" if last else "start"
        tx = x if last else x - 2
        dot = (f'<circle cx="{x}" cy="{y}" r="9" fill="{t["accent"]}"/>' if last
               else f'<circle cx="{x}" cy="{y}" r="6" fill="{t["ink"]}"/>')
        parts.append(f"""
  <g class="rise a{min(i + 1, 5)}">
    {dot}
    <text class="{'accent' if last else 'muted'}" x="{tx}" y="{y - 26}" font-size="14" letter-spacing="0" text-anchor="{anchor}">{when}</text>
    <text class="{'accent' if last else 'ink'}" x="{tx}" y="{y + 40}" font-size="17" text-anchor="{anchor}">{esc(title)}</text>
    <text class="muted" x="{tx}" y="{y + 64}" font-size="14" text-anchor="{anchor}">{esc(sub)}</text>
  </g>""")
    return svg(t, 200, "연표: 2021 GitHub 시작, 2026 Showmoa, test moa, Pawmento, 지금 신입 백엔드 구직 중", "".join(parts) + "\n")


# ── 실행 ─────────────────────────────────────────────

def main():
    global STATIC
    ap = argparse.ArgumentParser()
    ap.add_argument("--static", action="store_true", help="애니메이션 없이 생성")
    ap.add_argument("--out", default=str(ROOT / "assets"), help="출력 폴더")
    args = ap.parse_args()
    STATIC = args.static
    stats = fetch_stats()
    out = Path(args.out)
    for mode, t in THEMES.items():
        d = out if mode == "light" else out / "dark"
        d.mkdir(parents=True, exist_ok=True)
        (d / "header.svg").write_text(header(t))
        for fname, num, name, note in SECTIONS:
            (d / f"{fname}.svg").write_text(section(t, num, name, note))
        (d / "fig-telemetry.svg").write_text(fig_telemetry(t, stats))
        (d / "fig-timeline.svg").write_text(fig_timeline(t))
    print(f"생성 완료: {out} (commits={stats['commits']}, total={stats['total']})")


if __name__ == "__main__":
    main()
