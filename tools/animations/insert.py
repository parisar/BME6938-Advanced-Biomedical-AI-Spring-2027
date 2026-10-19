"""Insert each animation into its notebook, after the section it illustrates."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cells_a, cells_b

import pathlib
NB = str(pathlib.Path(__file__).resolve().parents[2] / 'lectures' / 'notebooks')
MARK = 'from matplotlib.animation import FuncAnimation'   # how an earlier run is recognised

def cell(kind, text):
    lines = text.split('\n')
    src = [l + '\n' for l in lines[:-1]] + [lines[-1]]
    c = {'cell_type': kind, 'metadata': {}, 'source': src}
    if kind == 'code':
        c['outputs'] = []; c['execution_count'] = None
    return c

total = 0
for mod in (cells_a, cells_b):
    for name, (after, md, code) in mod.CELLS.items():
        p = f'{NB}/{name}.ipynb'
        nb = json.load(open(p))
        # drop what a previous run of this script inserted, so it can be re-run
        keep, skip_next = [], False
        for c in nb['cells']:
            s = ''.join(c['source'])
            if MARK in s:
                if keep: keep.pop()            # also drop its markdown lead-in
                continue
            keep.append(c)
        nb['cells'] = keep
        nb['cells'][after + 1:after + 1] = [cell('markdown', md), cell('code', code)]
        json.dump(nb, open(p, 'w'), indent=1, ensure_ascii=False)
        open(p, 'a').write('\n')
        total += 1
        print(f'{name:42s} inserted after cell {after}, now {len(nb["cells"])} cells')
print(total, 'notebooks')
