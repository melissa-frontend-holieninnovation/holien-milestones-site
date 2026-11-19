"""Build the static SenditGo roadmap and its versioned, offline-readable snapshot."""

import csv
from collections import Counter
from datetime import date
from html import escape
from pathlib import Path

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parent
START = date(2026, 11, 23)
END = date(2027, 3, 31)
DAYS = (END - START).days + 1
MONTHS = (
    (START, 'Nov'), (date(2026, 12, 1), 'Dec'), (date(2027, 1, 1), 'Jan'),
    (date(2027, 2, 1), 'Feb'), (date(2027, 3, 1), 'Mar'),
)
STREAMS = {
    'au': ('AU requests and reliability', 'New features, priority fixes and operating rules', '#1464a5'),
    'fleet': ('Fleet Web V2', 'Navigation, setup, order lookup and Insight', '#365bb4'),
    'app': ('Driver App V2', 'Shared foundation, core journey and later native modules', '#285d90'),
    'ops': ('Dispatch and Roster', 'Daily Run Sheets, assignment and operational changes', '#22746b'),
    'data': ('Analytics and reporting', 'GA4 events, BigQuery exports and operational metrics', '#775189'),
    'docs': ('User manuals', 'English and Traditional Chinese guidance for released flows', '#9a5d2c'),
    'qa': ('AU validation and release', 'Acceptance criteria, integration, field pilot and rollout', '#356b50'),
}
GATES = [
    ('30 Nov', 'Triage and staff', 'Confirm owners for priority fixes and reconcile the feature backlog.'),
    ('18 Dec', 'Approve the baseline', 'Review Web IA and driver prototypes with AU. Set API rules and staff both tracks.'),
    ('29 Jan', 'Demonstrate core flows', 'Create and assign an order on Web. Walk from Home to an accepted route on App.'),
    ('26 Feb', 'Verify the full journey', 'Test dispatch, scanning, proof and offline recovery across Web, API and native builds.'),
    ('31 Mar', 'Decide and roll out', 'Use AU pilot results, telemetry and manuals to decide each track’s release.'),
]
CONDITIONAL = {'M02', 'M03', 'M09', 'M11', 'M12', 'M13', 'M15', 'W18'}
LINKS = {
    'F01': '41a89adbb34d80ef8429ea19231c9b96', 'F02': '41b89adbb34d80e3814dff6fdf1327f3',
    'F03': '41b89adbb34d81f691f5d60f46fe081d', 'W09': '3fa89adbb34d81719424fc6183ccfaf2',
    'W15': '40089adbb34d81dfa17afd603079cc92', 'W14': '41289adbb34d811fb003eab86f879bc8',
    'W16': '3fc89adbb34d81bdbe0fc60a269ec396', 'B01': '41b89adbb34d805d8830d8f1dfc1af08',
    'B09': '41c89adbb34d8079a2dbcc721b008088', 'B10': '41c89adbb34d807a9227e918596d0824',
    'B11': '41489adbb34d81158793e2774c569461', 'G01': '41389adbb34d81acbef5c58e73bd4dfa',
}
GROUP_LINKS = {
    'au': '41289adbb34d8140b908c84c0f8da9d4', 'fleet': '41189adbb34d812e8e40d641a33727a2',
    'ops': '41989adbb34d81fc81baf83bcfe1f10a', 'app': '3fe89adbb34d814aa5e7e2140982c8e0',
    'data': '41389adbb34d81acbef5c58e73bd4dfa', 'docs': '3fa89adbb34d81beab90e8575d17c571',
    'qa': '41989adbb34d813f9c33d30ba6eee48d',
}


def label(day):
    return f'{day.day} {day:%b}'


def notion(page):
    return f'https://app.notion.com/p/{page}'


def fraction(day):
    return (day - START).days / DAYS


def build():
    with (SOURCE / 'packages.tsv').open() as handle:
        rows = list(csv.DictReader(handle, delimiter='\t'))
    expected = {f'{prefix}{i:02}' for prefix, first, last in (
        ('F', 1, 4), ('W', 1, 18), ('M', 0, 16), ('B', 1, 12),
        ('G', 1, 6), ('D', 1, 6), ('Q', 1, 4)) for i in range(first, last + 1)}
    assert Counter(row['id'] for row in rows) == Counter(expected)
    groups = []
    svg = []
    y = 106
    sx, sw = 524, 720
    axis = ''.join(f'<span style="left:{fraction(day):.3%}">{name}</span>' for day, name in MONTHS)
    for key, (title, subtitle, color) in STREAMS.items():
        items = [r for r in rows if r['stream'] == key]
        svg.append(f'<rect x="0" y="{y-20}" width="1270" height="32" fill="#e9eff5"/><text x="22" y="{y+2}" font-weight="700">{escape(title)}</text>')
        y += 36
        body = []
        for item in items:
            code = item['id']
            start, finish = (date.fromisoformat(item[k]) for k in ('start', 'finish'))
            assert START <= start <= finish <= END
            left, width = fraction(start), (finish - start).days / DAYS + 1 / DAYS
            name = escape(item['work'])
            dates = f'{label(start)} – {label(finish)}'
            conditional = code in CONDITIONAL
            marker = '<small class="conditional">Conditional</small>' if conditional else ''
            page = notion(LINKS.get(code, GROUP_LINKS[key]))
            body.append(f'''<details class="package" id="{code}"><summary>
              <span class="code">{code}</span><span class="work">{name} {marker}</span>
              <span class="dates">{dates}</span><span class="track" aria-hidden="true"><i style="left:{left:.3%};width:{width:.3%}"></i></span></summary>
              <div class="detail"><p>{escape(item['planned outcome'])}</p><p><b>Dependency or decision</b> {escape(item['dependency or decision'])}</p><a href="{page}">Inventory source ↗</a></div></details>''')
            svg.append(f'<g><title>{code} · {name} · {dates}</title><text x="22" y="{y}" font-size="12">{code}　{name}</text><text x="393" y="{y}" font-size="11">{dates}</text><rect x="{sx+sw*left:.1f}" y="{y-9}" width="{sw*width:.1f}" height="8" rx="4" fill="{color}" opacity="{0.58 if conditional else 1}"/></g>')
            y += 23
        groups.append(f'''<details class="stream" style="--ink:{color}" {'open' if key == 'au' else ''}>
            <summary><span class="swatch"></span><span><strong>{title}</strong><span class="subtitle">{subtitle}</span></span>
            <span class="count">{len(items)} packages</span><span class="arrow" aria-hidden="true">⌄</span></summary>
            <div class="head"><span>Package</span><span>Window</span><span class="axis">{axis}</span></div>
            {''.join(body)}</details>''')
        y += 14
    assert sum(r['stream'] in STREAMS for r in rows) == len(rows)
    lines = ''.join(f'<path d="M {sx+sw*fraction(d):.1f} 78 V {y}" stroke="#d7e0e8"/><text x="{sx+sw*fraction(d)+3:.1f}" y="72" font-size="12">{m}</text>' for d, m in MONTHS)
    graphic = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1270 {y+10}" width="1270" height="{y+10}" font-family="Arial,sans-serif" fill="#162b40" role="img" aria-labelledby="title desc"><title id="title">SenditGo delivery roadmap</title><desc id="desc">23 November 2026 to 31 March 2027. Seven streams. Lighter bars indicate conditional packages. All dates are planning targets.</desc><rect width="100%" height="100%" fill="white"/><text x="22" y="32" font-size="24" font-weight="700">SenditGo delivery roadmap</text><text x="22" y="55" font-size="13">23 Nov 2026 – 31 Mar 2027 · Proposed windows · Lighter bars require approval or extra capacity</text>{lines}{''.join(svg)}</svg>'''
    gates = ''.join(f'<article><time>{dt}</time><h3>{title}</h3><p>{detail}</p></article>' for dt, title, detail in GATES)
    template = (SOURCE / 'template.html').read_text()
    for out, archive in [(ROOT, 'v1.5/'), (ROOT / 'v1.6', '../v1.5/')]:
        out.mkdir(exist_ok=True)
        html = template.replace('{{archive}}', archive).replace('{{gates}}', gates).replace('{{groups}}', '\n'.join(groups))
        (out / 'index.html').write_text(html)
        (out / 'jira-milestones.svg').write_text(graphic + '\n')


if __name__ == '__main__':
    build()
