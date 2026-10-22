#!/usr/bin/env python3
"""Build the GitHub Pages site: a home page and one page per week.

GitHub will not play a video from a README. A relative path does not render, and
raw.githubusercontent.com serves .mp4 as application/octet-stream so the browser
downloads it. Pages serves the same files from the same repository with the right
content type, so an ordinary <video> element works, and with it the <track> that
finally puts the WebVTT captions in front of a viewer.

The site is served from the root of the default branch, not from docs/, so that the
clips stay where they are and nothing is duplicated. Each week page therefore lives
at lectures/weekNN/index.html, beside the clips it plays.

    python tools/build_site.py

Everything comes from files that already exist: the index table in lectures/README.md,
each week's clips.json, the transcripts for the clip titles, the banners, and the
schedule table in README.md for the papers. There is no second copy to keep in sync.
"""
import glob, html, json, os, re, subprocess, sys

try:
    import markdown                                         # pip install markdown
except ImportError:                                         # the site still builds, minus the doc pages
    markdown = None

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROW = re.compile(r'^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$')
LINKED = re.compile(r'^\[(.*)\]\((week\d+)/\)$')
MDLINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
E = html.escape


def md_links(cell, prefix=''):
    """The markdown links in one table cell, as (text, href) with relative hrefs prefixed."""
    out = []
    for text, href in MDLINK.findall(cell or ''):
        if not href.startswith('http'):
            href = prefix + href
        out.append((text, href))
    return out


def index_rows():
    """Week number, topic, slides and notebook, from the index table in lectures/README.md."""
    rows = {}
    for line in open(f'{R}/lectures/README.md', encoding='utf-8'):
        m = ROW.match(line)
        if not m or not m.group(1).isdigit():
            continue
        wk, topic, slides, clips, nb = m.groups()
        t = LINKED.match(topic)
        rows[int(wk)] = {'topic': t.group(1) if t else topic, 'slides': slides, 'nb': nb}
    return rows


SCHED = re.compile(r'^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$')


def schedule_papers():
    """The Thursday papers of each week, from the schedule table in the top-level README.

    That table has four columns, not the five of the lectures index, so it needs its
    own pattern: matching it with the five-column one silently returns no papers.
    """
    out = {}
    for line in open(f'{R}/README.md', encoding='utf-8'):
        m = SCHED.match(line)
        if not m or not m.group(1).isdigit():
            continue
        wk, _topic, papers, _project = m.groups()
        out[int(wk)] = md_links(papers.replace('<br>', ' '))
    return out


def duration(path):
    """Length of an mp4 in seconds, or None when ffprobe is not available."""
    try:
        s = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                            '-of', 'csv=p=0', path], capture_output=True, text=True).stdout
        return float(s.strip())
    except Exception:
        return None


def mmss(sec):
    if sec is None:
        return ''
    m, s = divmod(int(round(sec)), 60)
    return f'{m} min {s:02d} s' if m else f'{s} s'


def clips_of(wk):
    """Every clip of a week: its title, its two versions, its captions and its transcript."""
    d = f'{R}/lectures/week{wk:02d}'
    man = f'{d}/clips.json'
    if not os.path.exists(man):
        return []
    out = []
    for c in json.load(open(man, encoding="utf-8"))["clips"]:
        o = c['output']
        nar = f'clips/narrated/{o}-narrated.mp4'
        vtt = f'clips/narrated/{o}-narrated.vtt'
        sil = f'clips/silent/{o}.mp4'
        tr = f'clips/transcripts/{o}.md'
        title = o
        if os.path.exists(f'{d}/{tr}'):                      # the H1 is the title drawn in the clip
            first = open(f'{d}/{tr}', encoding='utf-8').readline().strip()
            title = first.lstrip('# ').strip() or title
        out.append({
            'title': title,
            'narrated': nar if os.path.exists(f'{d}/{nar}') else None,
            'vtt': vtt if os.path.exists(f'{d}/{vtt}') else None,
            'silent': sil if os.path.exists(f'{d}/{sil}') else None,
            'transcript': tr if os.path.exists(f'{d}/{tr}') else None,
            'secs': duration(f'{d}/{nar}') if os.path.exists(f'{d}/{nar}') else None,
        })
    return out


CSS = '''/* Written by tools/build_site.py. The palette matches the week banners, which are
   light artwork, so the site is light as well rather than following the system theme. */
:root{--uf:#0021A5;--orange:#FA4616;--ink:#11161f;--muted:#5a6474;--line:#e2e6ed;--bg:#f7f8fa;--card:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.6 "Inter",-apple-system,"Segoe UI",system-ui,sans-serif}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}
header{background:var(--card);border-bottom:1px solid var(--line);padding:18px 0}
header .wrap{display:flex;gap:18px;align-items:baseline;flex-wrap:wrap}
header a{color:var(--muted);text-decoration:none;font-size:.92rem}
header a:hover,header a[aria-current]{color:var(--uf)}
header .brand{font-weight:600;color:var(--ink);font-size:1rem}
main{padding:26px 0 70px}
h1{font-size:1.5rem;letter-spacing:-.01em;margin:0 0 6px}
h2{font-size:1.1rem;margin:2.1em 0 .6em}
p{margin:.6em 0}
a{color:var(--uf)}
.lede{color:var(--muted);margin-bottom:1.4em}
img.banner{width:100%;height:auto;display:block;border-radius:10px;border:1px solid var(--line);margin-bottom:22px}
a.weeklink{display:block;margin-bottom:14px}
a.weeklink img{width:100%;height:auto;display:block;border-radius:10px;border:1px solid var(--line)}
a.weeklink:hover img{border-color:var(--uf)}
.meta{color:var(--muted);font-size:.9rem;margin:-8px 0 20px}
.clip{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:0 0 18px}
.clip h3{margin:0 0 4px;font-size:1.02rem}
.clip .sub{color:var(--muted);font-size:.87rem;margin:0 0 10px}
video{width:100%;height:auto;display:block;border-radius:8px;background:#000}
.row{display:flex;gap:16px;flex-wrap:wrap;font-size:.9rem;margin-top:10px}
table{border-collapse:collapse;width:100%;font-size:.94rem;margin:.6em 0}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:var(--card);font-weight:600}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:.86rem;padding:18px 0 40px}
@media(max-width:600px){.wrap{padding:0 16px}}
'''

REPO = 'https://github.com/parisar/BME6938-Advanced-Biomedical-AI-Spring-2027'

# Every entry here has to resolve to an HTML page. Pointing one at a .md file or at a
# directory gives the reader raw markdown or a file listing, because .nojekyll stops
# GitHub rendering markdown and nothing serves an index for a bare folder.
NAV = ('<header><div class="wrap"><span class="brand">Advanced Biomedical AI</span>'
       '<a href="{root}index.html">Weeks</a>'
       '<a href="{root}syllabus/index.html">Syllabus</a>'
       '<a href="{root}papers/index.html">Reading list</a>'
       '<a href="{root}presentations/index.html">Paper sessions</a>'
       '<a href="{root}project/index.html">Term project</a>'
       f'<a href="{REPO}">Repository &#8599;</a>'
       '</div></header>')

FOOT = ('<footer><div class="wrap">BME 6938, University of Florida, Spring 2027. '
        'Taught by Dr. Parisa Rashidi.<br>The narration in the clips is an AI-generated voice. '
        'Captions are provided for every narrated clip.</div></footer>')


def page(title, body, root, desc=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>
{NAV.format(root=root)}
<main><div class="wrap">
{body}
</div></main>
{FOOT}
</body>
</html>
'''


DOC_DIRS = {'papers': 'Reading list', 'project': 'Term project',
            'presentations': 'Paper sessions', 'syllabus': 'Syllabus'}


def rendered_md():
    """Every markdown file the site turns into a page, as repo-relative path -> output path.

    A folder's README.md becomes its index.html; anything else keeps its name. The map is
    built before any rendering so that links between these files can be rewritten.
    """
    out = {}
    for d in DOC_DIRS:
        if not os.path.isdir(f'{R}/{d}'):
            continue
        for f in sorted(os.listdir(f'{R}/{d}')):
            if f.endswith('.md'):
                out[f'{d}/{f}'] = f'{d}/' + ('index.html' if f == 'README.md' else f[:-3] + '.html')
    for t in sorted(glob.glob(f'{R}/lectures/week*/clips/transcripts/*.md')):
        rel = os.path.relpath(t, R)
        out[rel] = rel[:-3] + '.html'
    return out


def rewrite_links(body, src_rel, pages):
    """Point every link at something a browser can show.

    A link to a .md file renders as raw text in the browser, because .nojekyll stops
    GitHub rendering markdown. So: a .md we render becomes its .html, the repository
    README becomes the site home, and anything else we do not publish becomes a link
    to the file on GitHub.
    """
    here = os.path.dirname(src_rel)
    up = os.path.relpath(R, os.path.join(R, here)) if here else '.'

    def fix(m):
        href = m.group(1)
        if href.startswith(('http', 'mailto:', '#')):
            return m.group(0)
        base, _, frag = href.partition('#')
        if not base.endswith('.md'):
            return m.group(0)
        tgt = os.path.normpath(os.path.join(here, base)).replace(os.sep, '/')
        if tgt in pages:
            new = os.path.relpath(os.path.join(R, pages[tgt]),
                                  os.path.join(R, here)).replace(os.sep, '/')
        elif tgt == 'README.md':
            new = f'{up}/index.html'.lstrip('./') or 'index.html'
        else:
            new = f'{REPO}/blob/main/{tgt}'
        return f'href="{new}{"#" + frag if frag else ""}"'

    return re.sub(r'href="([^"]+)"', fix, body)


def doc_pages():
    """Render the document folders and the clip transcripts into real pages."""
    if markdown is None:
        print('markdown not installed: skipping the document pages', file=sys.stderr)
        return 0
    pages = rendered_md()
    made = 0
    for rel, out in pages.items():
        body = markdown.markdown(open(f'{R}/{rel}', encoding='utf-8').read(),
                                 extensions=['tables', 'sane_lists'])
        body = rewrite_links(body, rel, pages)
        depth = out.count('/')
        root = '../' * depth
        title = DOC_DIRS.get(out.split('/')[0], 'Transcript')
        open(f'{R}/{out}', 'w', encoding='utf-8').write(
            page(f'{title} | Advanced Biomedical AI', body, root,
                 f'{title} for BME 6938 Advanced Biomedical AI, Spring 2027.'))
        made += 1

    # A folder with no README has no index, so the nav entry pointing at it 404s.
    for d, title in DOC_DIRS.items():
        idx = f'{R}/{d}/index.html'
        if f'{d}/README.md' in pages or not os.path.isdir(f'{R}/{d}'):
            continue                                         # it has a README, which is its index
        items = sorted((v for k, v in pages.items() if k.startswith(d + '/')))
        li = ''.join(
            f'<li><a href="{os.path.basename(v)}">'
            f'{E(os.path.basename(v)[:-5].replace("_", " ").capitalize())}</a></li>'
            for v in items)
        open(idx, 'w', encoding='utf-8').write(
            page(f'{title} | Advanced Biomedical AI',
                 f'<h1>{E(title)}</h1><ul>{li}</ul>', '../',
                 f'{title} for BME 6938 Advanced Biomedical AI, Spring 2027.'))
        made += 1
    return made


def main():
    rows, papers = index_rows(), schedule_papers()
    alt = json.load(open(f'{R}/assets/banners/alt.json', encoding='utf-8'))
    os.makedirs(f'{R}/assets', exist_ok=True)
    open(f'{R}/assets/site.css', 'w', encoding='utf-8').write(CSS)
    open(f'{R}/.nojekyll', 'w').write('')                    # or Jekyll hides lectures/_shared

    # ---------------------------------------------------------------- week pages
    made = []
    for wk in sorted(rows):
        d = f'{R}/lectures/week{wk:02d}'
        if not os.path.isdir(d):
            continue
        r = rows[wk]
        clips = clips_of(wk)
        b = [f'<img class="banner" src="../../assets/banners/week{wk:02d}.png" '
             f'alt="{E(alt.get(str(wk), ""))}">',
             f'<h1>Week {wk}: {E(r["topic"])}</h1>']

        # Slides on one line and code on the next, because they are different
        # errands. "PDF" said the file format rather than what the file is.
        def line(label, cell, relabel=None):
            got = [(relabel(t) if relabel else t,
                    h.replace('../../lectures/week', '../week'))
                   for t, h in md_links(cell, '../../lectures/')]
            if not got:
                return None
            return (f'<p class="meta"><strong>{label}</strong> ' +
                    ' &middot; '.join(f'<a href="{E(h)}">{E(t)}</a>' for t, h in got) + '</p>')

        # Decks are labelled by their number, 1-1 and 1-2 in Week 1, 6-1 in Week 6.
        # The index table calls a lone deck "PDF", which names the file format rather
        # than the thing, so the number is taken from the filename instead.
        def deck_no(t):
            m = re.match(r'(\d+-\d+)', t)
            return m.group(1) if m else t
        for ln in (line('Slides', r['slides'],
                        relabel=lambda t: deck_no(t) if t != 'PDF' else
                                deck_no(os.path.basename(
                                    md_links(r['slides'])[0][1]).split('-slides')[0])),
                   line('Code', r['nb'],
                        relabel=lambda t: 'Notebook' if t.lower().endswith('notebook') else t)):
            if ln:
                b.append(ln)

        if papers.get(wk):
            b.append('<h2>Papers for Thursday</h2><ul>' +
                     ''.join(f'<li><a href="{E(h)}">{E(t)}</a></li>' for t, h in papers[wk]) +
                     '</ul>')

        if clips:
            b.append('<h2>Animation clips</h2>')
            b.append('<p class="lede">Each clip comes in two versions. The narrated version has an '
                     'AI-generated voice and captions; turn them on with the CC button. The silent '
                     'version is the same animation with its on-screen captions only.</p>')
            for c in clips:
                parts = [f'<div class="clip"><h3>{E(c["title"])}</h3>']
                # Length only. An earlier version printed the number of on-screen
                # captions here, which read as the number of subtitle cues and is not:
                # a long narration segment is split across several cues.
                parts.append(f'<p class="sub">{mmss(c["secs"])}</p>' if c['secs'] else '')
                if c['narrated']:
                    track = (f'<track kind="captions" src="{E(c["vtt"])}" srclang="en" '
                             f'label="English" default>' if c['vtt'] else '')
                    parts.append(f'<video controls preload="metadata" '
                                 f'src="{E(c["narrated"])}">{track}'
                                 f'Your browser cannot play this video. '
                                 f'<a href="{E(c["narrated"])}">Download it instead.</a></video>')
                extra = []
                if c['silent']:
                    extra.append(f'<a href="{E(c["silent"])}">Silent version</a>')
                if c['transcript']:
                    extra.append(f'<a href="{E(c["transcript"][:-3])}.html">Transcript</a>')
                if c['vtt']:
                    extra.append(f'<a href="{E(c["vtt"])}">Captions (.vtt)</a>')
                if extra:
                    parts.append('<div class="row">' + ''.join(extra) + '</div>')
                parts.append('</div>')
                b.append(''.join(parts))

        b.append(f'<h2>Everything for this week</h2><p>'
                 f'<a href="{REPO}/tree/main/lectures/week{wk:02d}">'
                 f'The Week {wk} folder in the repository &#8599;</a>, with the animation '
                 f'sources, the slides and the session guide.</p>')
        open(f'{d}/index.html', 'w', encoding='utf-8').write(
            page(f'Week {wk}: {r["topic"]} | Advanced Biomedical AI', '\n'.join(b), '../../',
                 f'Week {wk} of BME 6938: {r["topic"]}. Animation clips with captions, '
                 f'slides, notebook and papers.'))
        made.append((wk, r['topic'], len(clips)))

    # ---------------------------------------------------------------- home page
    h = ['<img class="banner" src="assets/banners/course-banner.png" alt="">',
         '<h1>Advanced Biomedical AI (BME 6938)</h1>',
         '<p class="lede">University of Florida, Spring 2027. A graduate course on current '
         'research in biomedical AI: modern LLM architectures, post-training and reasoning, '
         'self-supervised learning, foundation models for imaging, EHR and physiological time '
         'series, multimodal models, retrieval and agentic systems, generative models, clinical '
         'evaluation and deployment.</p>',
         '<p>Every week below has its animation clips, playable here with captions, alongside the '
         'slides and a reference notebook. The course repository has the sources for all of it.</p>',
         '<h2>Weeks</h2>']
    for wk, topic, n in made:
        h.append(f'<a class="weeklink" href="lectures/week{wk:02d}/index.html">'
                 f'<img src="assets/banners/week{wk:02d}.png" '
                 f'alt="Week {wk}: {E(topic)}"></a>')
    open(f'{R}/index.html', 'w', encoding='utf-8').write(
        page('Advanced Biomedical AI (BME 6938), Spring 2027', '\n'.join(h), '',
             'Graduate course on current research in biomedical AI at the University of Florida. '
             'Animation clips with captions, slides and notebooks.'))

    docs = doc_pages()
    total = sum(n for _, _, n in made)
    print(f'index.html, {len(made)} week pages, {docs} document pages, {total} clips')


main()
