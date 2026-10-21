#!/usr/bin/env python3
"""Put the course banners into the repository READMEs.

The same artwork appears on the Canvas course map and at the top of each Canvas
module, so the repository and Canvas look like one course rather than two.

What this writes:
  README.md                   a "Course map" section: every week as its banner,
                              linking into lectures/
  lectures/weekNN/README.md   that week's banner under the heading

The map is built from the index table in lectures/README.md, which stays the
plain table it has always been. The top-level README's own banner is written by
gen.py, which owns the rest of that file.

Run after gen.py, and again whenever a week's title or links change. Running it
twice changes nothing.
"""
import json, os, re, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROW = re.compile(r'^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$')
LINKED = re.compile(r'^\[(.*)\]\((week\d+)/\)$')
LINK = re.compile(r'\]\((?!https?:)([^)]+)\)')      # a relative link in a table cell
HEAD = '## Course map'
# the map goes between these two headings of README.md
AFTER, BEFORE = '## How the course works', '## Where things are'


def rows(md):
    """The week rows of the index table in lectures/README.md."""
    out = []
    for line in md.splitlines():
        m = ROW.match(line)
        if not m or not m.group(1).isdigit():
            continue
        wk, topic, slides, clips, nb = m.groups()
        t = LINKED.match(topic)
        out.append({'wk': int(wk), 'topic': t.group(1) if t else topic,
                    'slides': slides, 'clips': clips, 'nb': nb})
    return out


def links(r):
    """The line of links under a banner: slides, clips, notebook, Colab.

    The cells come from lectures/README.md, so their relative links are rewritten
    to work from the repository root.
    """
    parts = []
    s = r['slides'].replace('[PDF]', '[Slides (PDF)]')
    if s:
        parts.append(s if '·' not in s else 'Slides: ' + s)
    if r['clips']:
        parts.append(r['clips'])
    if r['nb']:
        parts.append(r['nb'])
    return LINK.sub(lambda m: f'](lectures/{m.group(1)})', ' · '.join(parts))


def main():
    alt = json.load(open(os.path.join(R, 'assets/banners/alt.json')))
    rs = rows(open(os.path.join(R, 'lectures/README.md'), encoding='utf-8').read())
    if not rs:
        sys.exit('no week rows found in lectures/README.md')

    block = [HEAD, '',
             'Every week of the course. Click a week for its slides, clips, and notebook.', '']
    for r in rs:
        wk = f"{r['wk']:02d}"
        # The alt names where the link goes, which is what a linked image should
        # say; the drawing itself is decoration and does not belong in it.
        block += [f"[![Week {r['wk']}: {r['topic']}](assets/banners/week{wk}.png)]"
                  f"(lectures/week{wk}/)", '', links(r), '']

    p = os.path.join(R, 'README.md')
    md = open(p, encoding='utf-8').read()
    if HEAD in md:                                   # replace the section in place
        md = re.sub(re.escape(HEAD) + r'.*?(?=' + re.escape(BEFORE) + ')',
                    '\n'.join(block), md, flags=re.S)
    else:
        md = md.replace(BEFORE, '\n'.join(block) + BEFORE, 1)
    open(p, 'w', encoding='utf-8').write(md)
    print(f'README.md: course map, {len(rs)} weeks')

    n = 0
    for r in rs:
        wk = f"{r['wk']:02d}"
        q = os.path.join(R, f'lectures/week{wk}/README.md')
        if not os.path.exists(q):
            continue
        lines = [l for l in open(q, encoding='utf-8').read().splitlines()
                 if '/assets/banners/' not in l]     # drop an earlier run's banner
        i = next(j for j, l in enumerate(lines) if l.startswith('# ')) + 1
        j = i
        while j < len(lines) and not lines[j].strip():
            j += 1
        # Replace the blank run under the heading rather than skipping past it. Skipping is
        # what made this script add one blank line on every run: dropping the previous
        # banner above left its blank line behind, and the new banner brought another.
        lines[i:j] = ['', f'![{alt.get(str(r["wk"]), "")}](../../assets/banners/week{wk}.png)', '']
        open(q, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
        n += 1
    print(f'{n} week READMEs')


main()
