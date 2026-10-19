"""Execute each animation cell on its own and report that it renders."""
import sys, os, importlib, matplotlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
matplotlib.use('Agg')

mod = importlib.import_module(sys.argv[1])
ok = True
for name, (idx, md, code) in mod.CELLS.items():
    ns = {}
    try:
        exec(compile(code, name, 'exec'), ns)
        h = ns.get('HTML')
        html = ns['ani'].to_jshtml(fps=8)
        frames = ns['ani'].save_count if hasattr(ns['ani'], 'save_count') else '?'
        print(f'ok   {name:42s} {len(html)/1024:7.0f} KB of HTML')
    except Exception as e:
        ok = False
        import traceback; traceback.print_exc()
        print(f'FAIL {name}: {e}')
sys.exit(0 if ok else 1)
