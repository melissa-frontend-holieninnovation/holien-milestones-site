"""Render the portfolio Gantt with the shared SenditGo dates and package details."""

from datetime import date, timedelta
from html import escape
from textwrap import shorten

# Original portfolio palette: blue for SenditGo, vermilion for Sterling.
BLUES = ('#007fff', '#006ad2', '#003df2')
LEFT = 174
SCALE = 10


def render(rows, streams, gates, start, end, conditional):
    def x(day):
        return LEFT + (day - start).days * SCALE

    width = x(end) + SCALE + 12
    bottom = 134
    backgrounds = []
    grid = []
    content = []
    week = start
    while week <= end:
        grid.append(f'<text x="{x(week)+3}" y="42" font-size="10" fill="#4b5563">{week:%d %b}</text>')
        week += timedelta(days=7)
    for offset in range((end - start).days + 1):
        day = start + timedelta(days=offset)
        if day == start or day.day == 1:
            grid.append(f'<text x="{x(day)+3}" y="19" font-size="12" font-weight="700">{day:%b %Y}</text>')
    content.append('<text x="16" y="42" font-size="12" font-weight="700">SenditGo</text>')
    content.append('<text x="16" y="74" font-size="12" font-weight="700">◆ Milestone targets</text>')
    for gate, (_, name, desc) in zip(('2026-11-30', '2026-12-18', '2027-01-29', '2027-02-26', '2027-03-31'), gates):
        day = date.fromisoformat(gate)
        pos = x(day) + SCALE // 2
        anchor = 'end' if day == end else 'middle'
        content.append(f'<g class="checkpoint"><title>{day:%d %b} · {escape(name)}. {escape(desc)}</title><path d="M{pos} 52 l6 6 -6 6 -6 -6z" fill="#e53e65"/><text x="{pos}" y="78" text-anchor="{anchor}" font-size="11" font-weight="600">{day:%d %b}</text><text x="{pos}" y="91" text-anchor="{anchor}" font-size="10" fill="#536170">{escape(name)}</text></g>')
    content.append(f'<text x="16" y="114" font-size="12" font-weight="700">Ongoing AU feedback</text><rect x="{LEFT}" y="96" width="{width-LEFT-12}" height="27" rx="7" fill="#006ad2"/><text x="{LEFT+9}" y="114" fill="#fff" font-size="12" font-weight="600">AU feedback intake and weekly triage · 23 Nov – 31 Mar</text>')
    for index, (key, (name, _, _)) in enumerate(streams.items()):
        items = sorted((r for r in rows if r['stream'] == key), key=lambda r: (r['start'], r['finish'], r['id']))
        track_ends: list[date] = []
        top = bottom
        color = BLUES[index % len(BLUES)]
        for item in items:
            begin, finish = (date.fromisoformat(item[k]) for k in ('start', 'finish'))
            track = next((i for i, previous in enumerate(track_ends) if previous < begin), len(track_ends))
            if track == len(track_ends):
                track_ends.append(finish)
            else:
                track_ends[track] = finish
            y = top + 7 + track * 32
            length = ((finish - begin).days + 1) * SCALE - 3
            code = item['id']
            full = f"{code} · {item['work']}"
            text = shorten(full, width=max(7, (length - 17) // 7), placeholder='…')
            tip = f'{full} | {begin:%d %b %Y} – {finish:%d %b %Y} | {item["planned outcome"]}'
            edge = ' stroke="#163b74" stroke-dasharray="4 3" stroke-width="2"' if code in conditional else ''
            if edge:
                tip += ' | Conditional on approval or additional capacity.'
            content.append(f'<g class="feature"><title>{escape(tip)}</title><a href="index.html#{code}" aria-label="{escape(tip)}"><rect x="{x(begin)}" y="{y}" width="{length}" height="26" rx="7" fill="{color}"{edge}/><text x="{x(begin)+7}" y="{y+17}" font-size="11" font-weight="600" fill="#fff">{escape(text)}</text></a></g>')
        bottom = top + 12 + len(track_ends) * 32
        backgrounds.append(f'<rect y="{top}" width="{width}" height="{bottom-top}" fill="{("#dcecff", "#ebf5ff")[index % 2]}"/><rect y="{top}" width="7" height="{bottom-top}" fill="{color}"/>')
        lane_labels = {'au': 'AU requests and fixes', 'data': 'Analytics and reporting', 'qa': 'AU validation and release'}
        content.append(f'<text x="16" y="{top+23}" font-size="12" font-weight="700" fill="#12457b">{escape(lane_labels.get(key, name))}</text>')
    for offset in range((end - start).days + 1):
        day = start + timedelta(days=offset)
        if day.weekday() == 0 or day.day == 1:
            stroke = '#b5c6d7' if day.day == 1 else '#d5e0ec'
            grid.append(f'<line x1="{x(day)}" x2="{x(day)}" y1="47" y2="{bottom}" stroke="{stroke}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{bottom+2}" viewBox="0 0 {width} {bottom+2}" font-family="Inter,Helvetica,Arial,sans-serif" fill="#182737" aria-labelledby="chart-title chart-desc">
<title id="chart-title">SenditGo milestones · November 2026 to March 2027</title><desc id="chart-desc">Weekly Gantt in seven lanes. Diamonds mark the five proposed monthly checkpoints. Dashed outlines indicate conditional packages. Each feature links to its scope and ticket details.</desc>
<rect width="100%" height="100%" fill="white"/>{''.join(backgrounds)}{''.join(grid)}{''.join(content)}</svg>'''
