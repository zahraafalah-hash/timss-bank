# Attach the geometry figures from geo_svg.py to the suggested questions in data/similar.json.
# Safe to re-run: matching is by question text, and only the svg (plus the listed wording fixes) changes.
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import geo_svg as G

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'data', 'similar.json')
store = json.load(open(path, encoding='utf-8'))
figs = G.build()
done = 0
for key, items in store['items'].items():
    if not key.startswith('math'):
        continue
    for q in items:
        q['q'] = G.SIM_FIX.get(q['q'], q['q'])
        if q['q'] in G.EXPLAIN_FIX:
            q['explain'] = G.EXPLAIN_FIX[q['q']]
        if q['q'] in figs:
            q['svg'] = figs[q['q']]
            done += 1
json.dump(store, open(path, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(f'{done} questions now have a figure ({len(figs)} distinct figures)')
