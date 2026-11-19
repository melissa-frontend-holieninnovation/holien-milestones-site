"""Build the static SenditGo roadmap and its versioned, offline-readable snapshot."""

import csv
from collections import Counter, defaultdict
from datetime import date, timedelta
from html import escape
from pathlib import Path

from timeline import render

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
    ('18–30 Nov 2026', 'Planning and prioritisation', 'Triage AU feedback, confirm feature priorities, reconcile the GA4 backlog and investigate critical App and Web bugs. Lock the executable backlog and dependencies.'),
    ('December 2026', 'UX and requirements', 'Approve Fleet Web IA and UX, validate core App prototypes with AU operators and agree API contracts and acceptance criteria. Freeze the first release slice before development.'),
    ('January 2027', 'Core development', 'Deliver Web dispatch and Create Order increments, the App design system, Home, Run Sheet and navigation, and critical GA4 events. Demonstrate usable slices with API readback.'),
    ('February 2027', 'Integration and testing', 'Integrate scan, POD and offline recovery. Complete and harden Web features, run cross-platform E2E and AU UAT, and update manuals. Verify outcomes on actual builds.'),
    ('March 2027', 'Release readiness', 'Close severe regressions, validate telemetry and manuals, and run the AU pilot. Decide go or hold for each track and stage approved rollouts.'),
]
CONDITIONAL = {'M02', 'M03', 'M09', 'M11', 'M12', 'M13', 'M15', 'W18'}
LINKS = {
    'F01': '41a89adbb34d80ef8429ea19231c9b96', 'F02': '41b89adbb34d80e3814dff6fdf1327f3',
    'F04': '41b89adbb34d800ebb6ceab1eeba4540', 'B02': '41789adbb34d805ab99df9a097e55bbd',
    'B12': '41789adbb34d8023a657ce69d2b98a07', 'F03': '41b89adbb34d81f691f5d60f46fe081d', 'W09': '3fa89adbb34d81719424fc6183ccfaf2',
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


def read_rows(filename):
    with (SOURCE / filename).open() as handle:
        return list(csv.DictReader(handle, delimiter='\t'))


def weekly_table():
    weeks = read_rows('weeks.tsv')
    assert [date.fromisoformat(w['monday']) for w in weeks] == [
        START + timedelta(weeks=i) for i in range((END - START).days // 7 + 1)]
    result = []
    for week in weeks:
        monday = date.fromisoformat(week['monday'])
        friday = min(monday + timedelta(days=4), END)
        flex = week['second slot']
        assert flex.startswith(('Bug · ', 'UX · ', 'Feature · '))
        cells = ''.join(f'<td>{escape(week[k])}</td>' for k in ('bug reserve', 'second slot', 'ux', 'feature'))
        result.append(f'<tr><th scope="row">{label(monday)} – {label(friday)}</th>{cells}</tr>')
    return ''.join(result)


def ticket_info(matches):
    kinds = {r['match'] for r in matches}
    category = next((k for k in ('direct', 'related', 'prior') if k in kinds), 'gap')
    titles = {'direct': 'Open ticket', 'related': 'Related open work', 'prior': 'Earlier ticket', 'gap': 'No direct open match'}
    parts = []
    for row in matches:
        url = notion(row['page'])
        parts.append(f'<li>{titles[row["match"]]} · <a href="{url}">#{row["ticket"]} {escape(row["scope"])}</a> · {escape(row["status"])}</li>')
    detail = '<ul class="ticket-list">' + ''.join(parts) + '</ul>' if parts else '<p>No directly matching open delivery ticket confirmed in Tasks. Check the source and agree scope at triage.</p>'
    return category, detail


def build():
    rows = read_rows('packages.tsv')
    tickets = defaultdict(list)
    for ticket in read_rows('tickets.tsv'):
        tickets[ticket['package']].append(ticket)
    register = defaultdict(list)
    expected = {f'{prefix}{i:02}' for prefix, first, last in (
        ('F', 1, 4), ('W', 1, 18), ('M', 0, 16), ('B', 1, 12),
        ('G', 1, 6), ('D', 1, 6), ('Q', 1, 4)) for i in range(first, last + 1)}
    assert Counter(row['id'] for row in rows) == Counter(expected)
    groups = []
    axis = ''.join(f'<span style="left:{fraction(day):.3%}">{name}</span>' for day, name in MONTHS)
    for key, (title, subtitle, color) in STREAMS.items():
        items = [r for r in rows if r['stream'] == key]
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
            category, ticket_detail = ticket_info(tickets[code])
            register[category].append(f'<li><a href="#{code}">{code} · {name}</a>{ticket_detail}</li>')
            body.append(f'''<details class="package" id="{code}"><summary>
              <span class="code">{code}</span><span class="work">{name} {marker}</span>
              <span class="dates">{dates}</span><span class="track" aria-hidden="true"><i style="left:{left:.3%};width:{width:.3%}"></i></span></summary>
              <div class="detail"><p>{escape(item['planned outcome'])}</p><p><b>Dependency or decision</b> {escape(item['dependency or decision'])}</p><a href="{page}">Inventory source ↗</a>{ticket_detail}</div></details>''')
        groups.append(f'''<details class="stream" style="--ink:{color}" {'open' if key == 'au' else ''}>
            <summary><span class="swatch"></span><span><strong>{title}</strong><span class="subtitle">{subtitle}</span></span>
            <span class="count">{len(items)} packages</span><span class="arrow" aria-hidden="true">⌄</span></summary>
            <div class="head"><span>Package</span><span>Window</span><span class="axis">{axis}</span></div>
            {''.join(body)}</details>''')
    assert sum(r['stream'] in STREAMS for r in rows) == len(rows)
    graphic = render(rows, STREAMS, GATES, START, END, CONDITIONAL)
    gates = ''.join(f'<article><time>{dt}</time><h3>{title}</h3><p>{detail}</p></article>' for dt, title, detail in GATES)
    names = {'direct': 'Direct open tickets', 'related': 'Related open tickets only', 'prior': 'Verified or earlier work only', 'gap': 'No direct ticket confirmed'}
    ticket_register = ''.join(
        f'<details class="register"><summary>{name} · {len(register[kind])} packages</summary><ul>{"".join(register[kind])}</ul></details>'
        for kind, name in names.items())
    weeks = weekly_table()
    template = (SOURCE / 'template.html').read_text()
    for out, archive in [(ROOT, 'v1.5/'), (ROOT / 'v1.8', '../v1.5/')]:
        out.mkdir(exist_ok=True)
        inline_chart = graphic.replace('href="index.html#', 'href="#')
        html = template.replace('{{timeline}}', inline_chart).replace('{{archive}}', archive).replace('{{weeks}}', weeks).replace('{{tickets}}', ticket_register).replace('{{gates}}', gates).replace('{{groups}}', '\n'.join(groups))
        (out / 'index.html').write_text(html)
        (out / 'jira-milestones.svg').write_text(graphic + '\n')


if __name__ == '__main__':
    build()
