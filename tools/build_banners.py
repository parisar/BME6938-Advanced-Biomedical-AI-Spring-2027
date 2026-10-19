#!/usr/bin/env python3
"""Put the week banners into the repository READMEs.

The same artwork appears on the Canvas course map and at the top of each Canvas
module, so the repository and Canvas look like one course rather than two.

What this writes:
  lectures/README.md          a visual course map, then the existing index table
  lectures/weekNN/README.md   that week's banner under the heading

The top-level README's banner is written by gen.py, which owns that file.
Run this after gen.py, and again whenever a week's title or links change.
"""
import json, os, re, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROW = re.compile(r'^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$')
# the index table's topic cell is sometimes a link to the week folder
LINKED = re.compile(r'^\[(.*)\]\((week\d+)/\)$')


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
                    'raw_topic': topic, 'slides': slides, 'clips': clips,
                    'nb': nb, 'line': line})
    return out


def links(r):
    """The one line of links under a banner: slides, clips, notebook, Colab."""
    parts = []
    # the slides cell is either "[PDF](...)" or "[1-1](...) · [1-2](...)"
    s = r['slides'].replace('[PDF]', '[Slides (PDF)]')
    if s:
        parts.append(s if '·' not in s else 'Slides: ' + s)
    if r['clips']:
        parts.append(r['clips'])
    if r['nb']:
        parts.append(r['nb'])
    return ' · '.join(parts)


def main():
    alt = json.load(open(os.path.join(R, 'assets/banners/alt.json')))
    path = os.path.join(R, 'lectures/README.md')
    md = open(path, encoding='utf-8').read()
    rs = rows(md)
    if not rs:
        sys.exit('no week rows found in lectures/README.md')

    # Everything this script writes starts at the first banner, the "## Index"
    # heading or the table, whichever comes first. Keeping only what precedes it
    # makes a second run replace its own output rather than append to it.
    lines = md.splitlines()
    cut = next(i for i, l in enumerate(lines)
               if '/assets/banners/' in l or l.startswith('## Index') or l.startswith('|'))
    head = '\n'.join(lines[:cut]).rstrip()          # title and intro paragraph
    tail = md.rsplit('|\n', 1)[1].strip()           # the note after the table
    table = [l for l in lines if l.startswith('|')]

    out = [head, '']
    for r in rs:
        wk = f"{r['wk']:02d}"
        # The alt text names the destination, which is what a link's image should
        # say; the motif is decoration and does not belong in it.
        out += [f"[![Week {r['wk']}: {r['topic']}](../assets/banners/week{wk}.png)]"
                f"(week{wk}/)", '', links(r), '']
    out += ['## Index', '', *table, '', tail, '']
    open(path, 'w', encoding='utf-8').write('\n'.join(out))
    print(f'lectures/README.md: {len(rs)} weeks')

    n = 0
    for r in rs:
        wk = f"{r['wk']:02d}"
        p = os.path.join(R, f'lectures/week{wk}/README.md')
        if not os.path.exists(p):
            continue
        lines = open(p, encoding='utf-8').read().splitlines()
        # drop a banner written by an earlier run, then insert under the heading
        lines = [l for l in lines if '/assets/banners/' not in l]
        i = next(j for j, l in enumerate(lines) if l.startswith('# ')) + 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        banner = f'![{alt.get(str(r["wk"]), "")}](../../assets/banners/week{wk}.png)'
        lines[i:i] = [banner, '']
        open(p, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
        n += 1
    print(f'{n} week READMEs')


main()
