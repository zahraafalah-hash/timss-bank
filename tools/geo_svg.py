# SVG figures for the geometry & area suggested questions.
# Each figure is drawn to scale from the question's own numbers, and is keyed by
# the exact question text so duplicates across grades share one drawing.
import math

FONT = 'Tahoma, Arial, sans-serif'
AR = str.maketrans('0123456789-.', '٠١٢٣٤٥٦٧٨٩−,')


def ar(x):
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    return str(x).translate(AR)


def deg(x):
    return ar(x) + '°'


# ---------- primitives (pixel coords, y down) ----------
def svg(body, w=420, h=280):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}" font-size="16">'
            f'<rect width="{w}" height="{h}" fill="white"/>{"".join(body)}</svg>')


def f(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


def P(pts):
    return ' '.join(f'{f(x)},{f(y)}' for x, y in pts)


def poly(pts, fill='none', sw=2, dash=False, stroke='black'):
    d = ' stroke-dasharray="6 4"' if dash else ''
    return f'<polygon points="{P(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{d}/>'


def line(a, b, sw=2, dash=False, stroke='black'):
    d = ' stroke-dasharray="6 4"' if dash else ''
    return f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def text(x, y, s, size=18, anchor='middle', weight=None, fill='black'):
    # direction="rtl" flips start/end, so callers keep meaning "start = text begins at x, going right".
    anchor = {'start': 'end', 'end': 'start'}.get(anchor, anchor)
    w = f' font-weight="{weight}"' if weight else ''
    return (f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" dominant-baseline="central" '
            f'font-size="{size}" fill="{fill}"{w} direction="rtl" unicode-bidi="embed">{s}</text>')


def dot(p, r=4, fill='black'):
    return f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="{r}" fill="{fill}"/>'


def circle(c, r, fill='none', sw=2, dash=False):
    d = ' stroke-dasharray="6 4"' if dash else ''
    return f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}" fill="{fill}" stroke="black" stroke-width="{sw}"{d}/>'


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, k):
    return (a[0] * k, a[1] * k)


def unit(v):
    n = math.hypot(*v)
    return (v[0] / n, v[1] / n)


def mid(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def centroid(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def side_label(a, b, s, inside, off=16, size=18):
    """Label the segment ab on the side away from the point `inside`, clear of the line."""
    m = mid(a, b)
    n = unit((-(b[1] - a[1]), b[0] - a[0]))
    if (inside[0] - m[0]) * n[0] + (inside[1] - m[1]) * n[1] > 0:
        n = mul(n, -1)
    tw, th = len(s) * 8.4 * size / 16, size * 1.15
    d = off - 4 + abs(n[0]) * tw / 2 + abs(n[1]) * th / 2
    return text(m[0] + n[0] * d, m[1] + n[1] * d, s, size)


def vlabel(v, s, inside, off=17, size=18):
    d = unit(sub(v, inside))
    return text(v[0] + d[0] * off, v[1] + d[1] * off, s, size, weight='bold')


def right_angle(v, p, q, s=13):
    u, w = unit(sub(p, v)), unit(sub(q, v))
    a, c = add(v, mul(u, s)), add(v, mul(w, s))
    b = add(a, mul(w, s))
    return f'<polyline points="{P([a, b, c])}" fill="none" stroke="black" stroke-width="1.5"/>'


def angle_arc(v, p, q, label=None, r=28, loff=None, size=17, arcs=1):
    a1 = math.atan2(p[1] - v[1], p[0] - v[0])
    a2 = math.atan2(q[1] - v[1], q[0] - v[0])
    d = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
    out = []
    for i in range(arcs):
        rr = r + i * 5
        s = add(v, (rr * math.cos(a1), rr * math.sin(a1)))
        e = add(v, (rr * math.cos(a2), rr * math.sin(a2)))
        out.append(f'<path d="M{f(s[0])},{f(s[1])} A{rr},{rr} 0 0 {1 if d > 0 else 0} {f(e[0])},{f(e[1])}" '
                   f'fill="none" stroke="black" stroke-width="1.5"/>')
    if label:
        am = a1 + d / 2
        lo = loff if loff is not None else r + 13 + max(0, 14 - abs(math.degrees(d)) / 4)
        out.append(text(v[0] + lo * math.cos(am), v[1] + lo * math.sin(am), label, size))
    return ''.join(out)


def ticks(a, b, n=1, L=7):
    m = mid(a, b)
    u = unit(sub(b, a))
    nrm = (-u[1], u[0])
    out = []
    for i in range(n):
        c = add(m, mul(u, (i - (n - 1) / 2) * 5))
        out.append(line(add(c, mul(nrm, L)), add(c, mul(nrm, -L)), sw=1.5))
    return ''.join(out)


def arrows(a, b, n=1):
    """Parallel marks (small chevrons) at the middle of ab."""
    m = mid(a, b)
    u = unit(sub(b, a))
    nrm = (-u[1], u[0])
    out = []
    for i in range(n):
        c = add(m, mul(u, i * 7))
        t1 = add(sub(c, mul(u, 7)), mul(nrm, 5))
        t2 = add(sub(c, mul(u, 7)), mul(nrm, -5))
        out.append(f'<polyline points="{P([t1, c, t2])}" fill="none" stroke="black" stroke-width="1.5"/>')
    return ''.join(out)


SHADE = '#cfe3ee'
CUT = 'url(#hatch)'
HATCH = ('<defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<line x1="0" y1="0" x2="0" y2="8" stroke="#888" stroke-width="2"/></pattern></defs>')


def fit(pts, w=420, h=280, pad=50, maxs=None):
    """Scale math points (y up) into the box; returns pixel points and the scale."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    sx = (w - 2 * pad) / max(1e-9, max(xs) - min(xs))
    sy = (h - 2 * pad) / max(1e-9, max(ys) - min(ys))
    s = min(sx, sy) if maxs is None else min(sx, sy, maxs)
    ox = (w - (max(xs) - min(xs)) * s) / 2 - min(xs) * s
    oy = (h - (max(ys) - min(ys)) * s) / 2 + max(ys) * s
    return [(ox + x * s, oy - y * s) for x, y in pts], s


def tri_sss(a, b, c):
    """Triangle with base a on the x axis, sides b (left) and c (right)."""
    x = (a * a + b * b - c * c) / (2 * a)
    return [(0, 0), (a, 0), (x, math.sqrt(max(0, b * b - x * x)))]


def tri_aa(base, A, B):
    """Triangle on a base with base angles A (left) and B (right), in degrees."""
    ta, tb = math.tan(math.radians(A)), math.tan(math.radians(B))
    x = base * tb / (ta + tb)
    return [(0, 0), (base, 0), (x, x * ta)]


# ---------- shared figure builders ----------
def triangle_fig(m, labels=(), angles=(), right=None, ticks_on=(), vnames=None, w=420, h=260, pad=55, extra=None):
    pts, s = fit(m, w, h, pad)
    c = centroid(pts)
    body = [poly(pts)]
    for i, j, t in labels:
        body.append(side_label(pts[i], pts[j], t, c))
    for v, t, *opt in angles:
        o = [pts[k] for k in range(3) if k != v]
        body.append(angle_arc(pts[v], o[0], o[1], t, **(opt[0] if opt else {})))
    if right is not None:
        o = [pts[k] for k in range(3) if k != right]
        body.append(right_angle(pts[right], o[0], o[1]))
    for i, j, n in ticks_on:
        body.append(ticks(pts[i], pts[j], n))
    if vnames:
        for k, nm in enumerate(vnames):
            body.append(vlabel(pts[k], nm, c))
    if extra:
        body.append(extra(pts, s))
    return svg(body, w, h)


def rect_fig(L, W, top=None, side=None, inner=None, w=420, h=250, ticks4=False, pad=60):
    pts, s = fit([(0, 0), (L, 0), (L, W), (0, W)], w, h, pad)
    c = centroid(pts)
    body = [poly(pts, fill=SHADE if inner else 'none')]
    for k in range(4):
        body.append(right_angle(pts[k], pts[k - 1], pts[(k + 1) % 4], 11))
    if top:
        body.append(side_label(pts[0], pts[1], top, c))
    if side:
        body.append(side_label(pts[1], pts[2], side, c))
    if inner:
        lines = inner.split('\n')
        for i, t in enumerate(lines):
            body.append(text(c[0], c[1] + (i - (len(lines) - 1) / 2) * 22, t, 18))
    if ticks4:
        for k in range(4):
            body.append(ticks(pts[k], pts[(k + 1) % 4]))
    return svg(body, w, h)


def para_fig(base, slant, height, labels, w=420, h=250, left_off=None, show_slant_label=True):
    off = math.sqrt(slant * slant - height * height) if left_off is None else left_off
    m = [(0, 0), (base, 0), (base + off, height), (off, height)]
    pts, s = fit(m, w, h, 60)
    c = centroid(pts)
    body = [poly(pts)]
    foot = (pts[3][0], pts[0][1])
    body.append(line(pts[3], foot, sw=1.5, dash=True))
    body.append(right_angle(foot, pts[3], pts[1], 10))
    body.append(side_label(pts[0], pts[1], labels['base'], c))
    if labels.get('slant'):
        body.append(side_label(pts[1], pts[2], labels['slant'], c))
    if labels.get('height'):
        body.append(text(foot[0] + 8, (pts[3][1] + foot[1]) / 2, labels['height'], 18, anchor='start'))
    body.append(arrows(pts[0], pts[1]) + arrows(pts[3], pts[2]))
    if labels.get('area'):
        body.append(text(c[0] + 20, c[1] - 6, labels['area'], 17))
    return svg(body, w, h)


def parallels(angle, given, ask, names=('م', 'ن'), w=420, h=260):
    """Two horizontal parallel lines cut by a transversal.
    `given`/`ask` are (line 0|1, quadrant) with quadrant in {'tr','tl','br','bl'}."""
    y1, y2 = 85, 185
    t = math.radians(angle)
    dx = (y2 - y1) / math.tan(t)
    p1, p2 = (210 + dx / 2, y1), (210 - dx / 2, y2)
    u = unit(sub(p1, p2))
    body = [line((40, y1), (380, y1)), line((40, y2), (380, y2)),
            line(add(p2, mul(u, -70)), add(p1, mul(u, 70))),
            arrows((290, y1), (300, y1)), arrows((290, y2), (300, y2)),
            text(395, y1, names[0], 17, weight='bold'), text(395, y2, names[1], 17, weight='bold')]
    # At either line the transversal makes `angle` in the tr/bl quadrants and 180 − angle in tl/br.
    gq = given[0][1]
    real = angle if gq in ('tr', 'bl') else 180 - angle
    assert given[1] == deg(real), (given, real)
    for (ln, qd), lab in (given, ask):
        v = p1 if ln == 0 else p2
        right, up = qd[1] == 'r', qd[0] == 't'
        a = add(v, (60 if right else -60, 0))
        b = add(v, mul(u, 60 if up else -60))
        body.append(angle_arc(v, a, b, lab, r=24))
    return svg(body, w, h)


class Grid:
    """Coordinate plane with axes, unit grid and Arabic tick numbers."""

    def __init__(self, x0, x1, y0, y1, w=420, h=300, pad=30, unit_px=None):
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        # Keep phone-friendly proportions: at most 34px a unit and about 320px tall.
        u = unit_px or min(34, (w - 2 * pad) / (x1 - x0), 300 / (y1 - y0))
        self.u = u
        self.w = (x1 - x0) * u + 2 * pad
        self.h = (y1 - y0) * u + 2 * pad
        self.pad = pad
        self.body = []
        for x in range(x0, x1 + 1):
            self.body.append(line(self.p(x, y0), self.p(x, y1), sw=1, stroke='#d4dbe2'))
        for y in range(y0, y1 + 1):
            self.body.append(line(self.p(x0, y), self.p(x1, y), sw=1, stroke='#d4dbe2'))
        if y0 <= 0 <= y1:
            self.body.append(line(self.p(x0, 0), self.p(x1, 0), sw=1.6))
            self.body.append(text(self.p(x1, 0)[0] + 13, self.p(x1, 0)[1], 'س', 17, weight='bold'))
            for x in range(x0, x1 + 1):
                if x:
                    q = self.p(x, 0)
                    self.body.append(text(q[0], q[1] + 12, ar(x), 12, fill='#333'))
        if x0 <= 0 <= x1:
            self.body.append(line(self.p(0, y0), self.p(0, y1), sw=1.6))
            self.body.append(text(self.p(0, y1)[0], self.p(0, y1)[1] - 13, 'ص', 17, weight='bold'))
            for y in range(y0, y1 + 1):
                if y:
                    q = self.p(0, y)
                    self.body.append(text(q[0] - 10, q[1], ar(y), 12, fill='#333'))
            if y0 <= 0 <= y1:
                o = self.p(0, 0)
                self.body.append(text(o[0] - 9, o[1] + 11, '٠', 12, fill='#333'))

    def p(self, x, y):
        return (self.pad + (x - self.x0) * self.u, self.pad + (self.y1 - y) * self.u)

    def point(self, x, y, name=None, dx=12, dy=-12, show=False):
        q = self.p(x, y)
        self.body.append(dot(q, 4.5))
        if name or show:
            lab = (name or '') + (f'({ar(x)}، {ar(y)})' if show else '')
            self.body.append(text(q[0] + dx, q[1] + dy, lab, 14, weight='bold'))
        return q

    def svg(self):
        return svg(self.body, round(self.w), round(self.h))


def plane(pts, x0=None, x1=None, y0=None, y1=None, polygon=False, diag=False, names=None, show=True, offs=None, pad=1):
    xs, ys = [p[0] for p in pts] + [0], [p[1] for p in pts] + [0]
    g = Grid(x0 if x0 is not None else min(xs) - pad, x1 if x1 is not None else max(xs) + pad,
             y0 if y0 is not None else min(ys) - pad, y1 if y1 is not None else max(ys) + pad, unit_px=None)
    px = [g.p(*p) for p in pts]
    if polygon:
        g.body.append(poly(px, fill='rgba(11,110,153,.12)', stroke='#0b6e99'))
    if diag:
        g.body.append(line(px[0], px[2], sw=1.5, dash=True) + line(px[1], px[3], sw=1.5, dash=True))
    for k, p in enumerate(pts):
        dx, dy = (offs[k] if offs else (12, -12))
        g.point(*p, name=names[k] if names else None, dx=dx, dy=dy, show=show)
    return g.svg()


def box3d(L, W, H, labels=None, open_top=False, w=420, h=270, grid=False, cubes=None):
    """Cuboid in oblique projection; L along x, W into depth, H up."""
    k = 0.5
    dxw, dyw = W * k * math.cos(math.radians(35)), W * k * math.sin(math.radians(35))
    m = {'A': (0, 0), 'B': (L, 0), 'C': (L, H), 'D': (0, H)}
    for n, (x, y) in list(m.items()):
        m[n + "'"] = (x + dxw, y + dyw)
    names = list(m)
    pts, s = fit([m[n] for n in names], w, h, 55)
    q = dict(zip(names, pts))
    body = []
    if open_top:
        body.append(poly([q['D'], q['C'], q["C'"], q["D'"]], fill='#e8eef3'))
    if cubes is None:
        hidden = [("A", "A'"), ("A'", "B'"), ("A'", "D'")]
        for a, b in hidden:
            body.append(line(q[a], q[b], sw=1.3, dash=True, stroke='#777'))
    body.append(poly([q['A'], q['B'], q['C'], q['D']], fill='white' if not cubes else 'none'))
    body.append(poly([q['B'], q["B'"], q["C'"], q['C']], fill='#f1f5f8' if not cubes else 'none'))
    if not open_top:
        body.append(poly([q['D'], q['C'], q["C'"], q["D'"]], fill='#f7fafc' if not cubes else 'none'))
    else:
        body.append(line(q['D'], q["D'"]) + line(q["D'"], q["C'"]))
    if labels:
        c = centroid(pts)
        body.append(side_label(q['A'], q['B'], labels[0], c))
        body.append(side_label(q['B'], q["B'"], labels[1], c, off=14))
        body.append(side_label(q["B'"], q["C'"], labels[2], c))
    return svg(body, w, h), q, s


def cubes_fig(cells, L, W, H, w=420, h=270, frame=False):
    """Unit cubes at (x, y, z) in an oblique view, drawn back-to-front."""
    k = 0.55
    ox, oy = math.cos(math.radians(35)) * k, math.sin(math.radians(35)) * k
    corners = [(x + y * ox, z + y * oy) for x in (0, L) for y in (0, W) for z in (0, H)]
    _, s = fit(corners, w, h, 45)
    xs = [c[0] for c in corners]
    zs = [c[1] for c in corners]
    X0 = (w - (max(xs) - min(xs)) * s) / 2
    Y0 = (h + (max(zs) - min(zs)) * s) / 2

    def pr(x, y, z):
        return (X0 + (x + y * ox) * s, Y0 - (z + y * oy) * s)

    body = []
    if frame:
        for a, b in [((0, W, 0), (L, W, 0)), ((0, W, 0), (0, W, H)), ((0, 0, 0), (0, W, 0))]:
            body.append(line(pr(*a), pr(*b), sw=1.3, dash=True, stroke='#777'))
    for (x, y, z) in sorted(cells, key=lambda c: (-c[1], c[2], c[0])):
        fr = [pr(x, y, z), pr(x + 1, y, z), pr(x + 1, y, z + 1), pr(x, y, z + 1)]
        tp = [pr(x, y, z + 1), pr(x + 1, y, z + 1), pr(x + 1, y + 1, z + 1), pr(x, y + 1, z + 1)]
        rt = [pr(x + 1, y, z), pr(x + 1, y + 1, z), pr(x + 1, y + 1, z + 1), pr(x + 1, y, z + 1)]
        body += [poly(rt, fill='#9cc6dc', sw=1.3), poly(tp, fill='#e3f0f7', sw=1.3), poly(fr, fill='#c4dfec', sw=1.3)]
    if frame:
        A, B, C, D = pr(0, 0, 0), pr(L, 0, 0), pr(L, 0, H), pr(0, 0, H)
        A2, B2, C2, D2 = pr(0, W, 0), pr(L, W, 0), pr(L, W, H), pr(0, W, H)
        for a, b in [(A, B), (B, C), (C, D), (D, A), (B, B2), (C, C2), (D, D2), (B2, C2), (C2, D2)]:
            body.append(line(a, b, sw=1.8))
    return svg(body, w, h)


def net_fig(cells, tris=(), w=420, h=260, shade='#e3f0f7'):
    """Net of unit squares at grid cells (col, row), rows going down; optional triangles
    given as (col, row, side) attached to that square's side ('t','b','l','r')."""
    cols = [c for c, r in cells] + [c for c, r, _ in tris]
    rows = [r for c, r in cells] + [r for c, r, _ in tris]
    nc, nr = max(cols) - min(cols) + 1, max(rows) - min(rows) + 3
    u = min((w - 60) / (nc), (h - 40) / (nr), 60)
    X0 = (w - nc * u) / 2 - min(cols) * u
    Y0 = (h - (max(rows) - min(rows) + 1) * u) / 2 - min(rows) * u
    body = []
    for c, r in cells:
        x, y = X0 + c * u, Y0 + r * u
        body.append(poly([(x, y), (x + u, y), (x + u, y + u), (x, y + u)], fill=shade))
    for c, r, sd in tris:
        x, y = X0 + c * u, Y0 + r * u
        hh = u * math.sqrt(3) / 2
        t = {'t': [(x, y), (x + u, y), (x + u / 2, y - hh)], 'b': [(x, y + u), (x + u, y + u), (x + u / 2, y + u + hh)]}[sd]
        body.append(poly(t, fill=shade))
    return svg(body, w, h)


# ---------- figures ----------
FIG = {}


def fig(q):
    def deco(fn):
        FIG[q] = fn
        return fn
    return deco


# Angles and parallel lines --------------------------------------------------

def parallel_in_triangle(A_deg, C_deg, k=0.45, labels=None, names=('أ', 'ب', 'ج', 'د', 'هـ'), arcs=None):
    """Triangle أ(top) ب(left) ج(right) with د on أب and هـ on أج, دهـ ∥ بج."""
    B, C, A = tri_aa(10, A_deg, C_deg)
    D = (A[0] + (B[0] - A[0]) * k, A[1] + (B[1] - A[1]) * k)
    E = (A[0] + (C[0] - A[0]) * k, A[1] + (C[1] - A[1]) * k)
    pts, s = fit([A, B, C, D, E], 420, 270, 50)
    A, B, C, D, E = pts
    cc = centroid([A, B, C])
    body = [poly([A, B, C]), line(D, E), arrows(D, E), arrows(B, C)]
    for p, n in zip((A, B, C), names[:3]):
        body.append(vlabel(p, n, cc))
    body.append(text(D[0] - 15, D[1] - 2, names[3], 17, weight='bold'))
    body.append(text(E[0] + 16, E[1] - 2, names[4], 17, weight='bold'))
    named = {'A': A, 'B': B, 'C': C, 'D': D, 'E': E}
    for v, a, b, lab, *kw in arcs or []:
        body.append(angle_arc(named[v], named[a], named[b], lab, **(kw[0] if kw else {})))
    return svg(body, 420, 270)


@fig('في الشكل، ك ل يوازي ب ج. قياس الزاوية أ = ٥٠°، وقياس الزاوية أ ل ك = ٧٠°. ما قيمة س؟')
def _():
    # أ top, ج left, ب right, ل on أج, ك on أب (as in the original figure). ∠ج = ٧٠ so ∠ب = ٦٠.
    Cm, Bm, Am = tri_aa(10, 70, 60)
    k = 0.6
    L = (Am[0] + (Cm[0] - Am[0]) * k, Am[1] + (Cm[1] - Am[1]) * k)
    K = (Am[0] + (Bm[0] - Am[0]) * k, Am[1] + (Bm[1] - Am[1]) * k)
    (A, C, B, L, K), s = fit([Am, Cm, Bm, L, K], 420, 270, 50)
    cc = centroid([A, B, C])
    body = [poly([A, C, B]), line(L, K), arrows(L, K), arrows(C, B),
            vlabel(A, 'أ', cc), vlabel(C, 'ج', cc), vlabel(B, 'ب', cc),
            text(L[0] - 15, L[1], 'ل', 17, weight='bold'), text(K[0] + 15, K[1], 'ك', 17, weight='bold'),
            angle_arc(A, C, B, deg(50), r=30),
            angle_arc(L, A, K, deg(70), r=20, loff=40),
            angle_arc(B, A, C, 'س', r=30)]
    return svg(body, 420, 270)


@fig('في مثلث أ ب ج، رُسم خط د هـ يوازي ب ج. إذا كانت الزاوية أ د هـ = ٦٥°، فما قياس الزاوية أ ب ج؟')
def _():
    return parallel_in_triangle(65, 55, arcs=[('D', 'A', 'E', deg(65), {'r': 22}), ('B', 'A', 'C', '؟', {'r': 30})])


@fig('في مثلث، زاويتان قياسهما ٤٥° و٨٥°. رُسم خط داخل المثلث يوازي الضلع الثالث. ما قياس الزاوية الثالثة للمثلث الصغير المتكوّن عند الرأس المشترك؟')
def _():
    B, C, A = tri_aa(10, 45, 85)
    k = 0.45
    D = (A[0] + (B[0] - A[0]) * k, A[1] + (B[1] - A[1]) * k)
    E = (A[0] + (C[0] - A[0]) * k, A[1] + (C[1] - A[1]) * k)
    (A, B, C, D, E), s = fit([A, B, C, D, E], 420, 270, 50)
    body = [poly([A, B, C]), line(D, E), arrows(D, E), arrows(B, C),
            angle_arc(B, C, A, deg(45), r=34), angle_arc(C, A, B, deg(85), r=26),
            angle_arc(A, B, C, '؟', r=22)]
    return svg(body, 420, 270)


@fig('قطع مستقيم خطين متوازيين م و ن. إذا كان قياس إحدى الزاويتين الداخليتين الواقعتين على الجهة نفسها من القاطع ١٣٠°، فما قياس الزاوية الأخرى س؟')
def _():
    # Transversal leans right at 50°, so the interior angle below the top line on the right is 130°.
    return parallels(50, ((0, 'br'), deg(130)), ((1, 'tr'), 'س'))


@fig('قطع مستقيم خطين متوازيين، فكانت إحدى الزوايا ٧٥°. ما قياس الزاوية المتبادلة معها؟')
def _():
    return parallels(75, ((0, 'bl'), deg(75)), ((1, 'tr'), '؟'))


@fig('قطع مستقيم خطين متوازيين. إحدى الزوايا ٤٠°. ما قياس الزاوية المحالفة لها (الداخلية على الجهة نفسها)؟')
def _():
    return parallels(40, ((0, 'bl'), deg(40)), ((1, 'tl'), '؟'))


@fig('في مثلث، زاويتان قياسهما ٥٠° و٧٠°. رُسم من الرأس الثالث قطعة تقسم زاويته إلى زاويتين إحداهما ٢٥°. ما قياس الزاوية الأخرى؟')
def _():
    B, C, A = tri_aa(10, 50, 70)
    # The segment from A makes 25° with AB.
    ang_ab = math.atan2(B[1] - A[1], B[0] - A[0])
    t = ang_ab + math.radians(25)
    # Intersect A + r(cos t, sin t) with y = 0.
    r = -A[1] / math.sin(t)
    D = (A[0] + r * math.cos(t), 0)
    (A, B, C, D), s = fit([A, B, C, D], 420, 260, 50)
    body = [poly([A, B, C]), line(A, D),
            angle_arc(B, C, A, deg(50), r=30), angle_arc(C, A, B, deg(70), r=30),
            angle_arc(A, B, D, deg(25), r=44), angle_arc(A, D, C, '؟', r=30)]
    return svg(body, 420, 260)


@fig('مثلث قياس زاويتين فيه ٣٥° و٩٠°. ما قياس الزاوية الثالثة؟')
def _():
    return triangle_fig([(0, 0), (10, 0), (0, 10 * math.tan(math.radians(35)))],
                        angles=[(1, deg(35), {'r': 40}), (2, '؟', {'r': 26})], right=0)


@fig('زاوية خارجية لمثلث قياسها ١١٠°، وإحدى الزاويتين الداخليتين البعيدتين ٤٥°. ما قياس الأخرى؟')
def _():
    B, C, A = tri_aa(10, 45, 70)
    X = (14, 0)
    (A, B, C, X), s = fit([A, B, C, X], 420, 250, 45)
    body = [poly([A, B, C]), line(C, X),
            angle_arc(B, C, A, deg(45), r=34), angle_arc(A, B, C, '؟', r=26),
            angle_arc(C, X, A, deg(110), r=26)]
    return svg(body, 420, 250)


def grid_angle(dx, dy, label, right=False, n=6, m=4):
    u = 44
    W, H = n * u + 60, m * u + 40
    body = []
    for i in range(n + 1):
        body.append(line((30 + i * u, 20), (30 + i * u, 20 + m * u), sw=1, stroke='#cfd8e0'))
    for j in range(m + 1):
        body.append(line((30, 20 + j * u), (30 + n * u, 20 + j * u), sw=1, stroke='#cfd8e0'))
    V = (30 + 3 * u, 20 + (m - 1) * u)
    if right:
        P1, P2 = (V[0] + 2 * u, V[1]), (V[0], V[1] - 2 * u)
        body += [line(V, P1, sw=2.5), line(V, P2, sw=2.5), dot(V), right_angle(V, P1, P2, 12)]
    else:
        P1 = (V[0] + 2 * u, V[1])
        P2 = (V[0] + dx * u, V[1] - dy * u)
        body += [line(V, P1, sw=2.5), line(V, P2, sw=2.5), dot(V), angle_arc(V, P1, P2, label, r=30)]
    return svg(body, W, H)


@fig('على شبكة مربعات، رُسم ضلع أفقي، ثم ضلع ثانٍ من نفس الرأس يمر بقُطر مربع واحد (وحدة يميناً ووحدة للأعلى). ما قياس الزاوية بينهما؟')
def _():
    return grid_angle(2, 2, '؟')


@fig('على شبكة المربعات، ضلع رأسي وضلع أفقي يلتقيان عند رأس واحد. ما نوع الزاوية؟')
def _():
    return grid_angle(0, 0, None, right=True)


@fig('طُويت ورقة على شكل مثلث متطابق الأضلاع من أحد رؤوسه، فتكوّنت زاوية قياسها ٧٠° بين خط الطي وأحد الضلعين. ما قياس الزاوية المجاورة لها على خط مستقيم؟')
def _():
    B, C, A = tri_aa(10, 60, 60)
    # Fold line from A meets BC at D with ∠ADB = 70°.
    t = math.radians(70)
    D = (A[0] - A[1] / math.tan(t), 0)
    (A, B, C, D), s = fit([A, B, C, D], 420, 260, 45)
    body = [poly([A, B, C]), line(A, D, dash=True), ticks(A, B), ticks(B, C), ticks(C, A),
            angle_arc(D, B, A, deg(70), r=22, loff=52), angle_arc(D, A, C, '؟', r=26)]
    return svg(body, 420, 260)


@fig('طُوي ركن ورقة مستطيلة فتكوّنت عند الحافة زاويتان متطابقتان قياس كل منهما ٣٥°، والزاوية الثالثة على الخط المستقيم هي س. ما قيمة س؟')
def _():
    # Bottom edge of the sheet; folded corner meets it at P. Angles at P (from the left): 35°, 35°, then س.
    P = (150, 200)
    L, R = (30, 200), (390, 200)
    a1, a2 = math.radians(35), math.radians(70)
    Q1 = (P[0] - 150 * math.cos(a1), P[1] - 150 * math.sin(a1))
    Q2 = (P[0] - 170 * math.cos(a2), P[1] - 170 * math.sin(a2))
    body = [poly([(30, 40), (390, 40), (390, 200), (30, 200)], fill='#f7fafc', sw=1.5),
            line(L, R, sw=2.5), line(P, Q1, dash=True), line(P, Q2),
            angle_arc(P, L, Q1, deg(35), r=46), angle_arc(P, Q1, Q2, deg(35), r=46),
            angle_arc(P, Q2, R, 'س', r=30), dot(P)]
    return svg(body, 420, 230)


@fig('في مثلث، زاويتان ٥٥° و٦٥°. ما الزاوية الثالثة؟')
def _():
    return triangle_fig(tri_aa(10, 55, 65), angles=[(0, deg(55)), (1, deg(65)), (2, '؟')])


@fig('مثلث متطابق الضلعين، زاوية الرأس فيه ٤٠°. ما قياس كل زاوية من زاويتي القاعدة؟')
def _():
    return triangle_fig(tri_aa(10, 70, 70), angles=[(2, deg(40), {'r': 34}), (0, '؟'), (1, '؟')],
                        ticks_on=[(0, 2, 1), (1, 2, 1)], h=270)


@fig('زاويتان متجاورتان على خط مستقيم، إحداهما ١٢٥°. ما الأخرى؟')
def _():
    V = (210, 170)
    t = math.radians(55)
    Q = (V[0] + 140 * math.cos(t), V[1] - 140 * math.sin(t))
    body = [line((40, 170), (380, 170)), line(V, Q), dot(V),
            angle_arc(V, (380, 170), Q, '؟', r=34), angle_arc(V, Q, (40, 170), deg(125), r=34)]
    return svg(body, 420, 210)


@fig('شكل رباعي ثلاث من زواياه ٩٠° و٨٠° و١٠٠°. ما الزاوية الرابعة؟')
def _():
    Lb, H = 10, 6
    A, B, D = (0, 0), (Lb, 0), (0, H)
    C = (Lb - H / math.tan(math.radians(80)), H)
    (A, B, C, D), s = fit([A, B, C, D], 420, 250, 50)
    body = [poly([A, B, C, D]), right_angle(A, B, D),
            angle_arc(B, C, A, deg(80), r=28), angle_arc(C, D, B, deg(100), r=26), angle_arc(D, A, C, '؟', r=26)]
    return svg(body, 420, 250)


@fig('متوازي أضلاع إحدى زواياه ٧٠°. ما قياسات زواياه الأخرى؟')
def _():
    off = 4 / math.tan(math.radians(70))
    (A, B, C, D), s = fit([(0, 0), (9, 0), (9 + off, 4), (off, 4)], 420, 240, 55)
    body = [poly([A, B, C, D]), arrows(A, B) + arrows(D, C), arrows(A, D, 2) + arrows(B, C, 2),
            angle_arc(A, B, D, deg(70), r=28), angle_arc(B, C, A, '؟', r=24),
            angle_arc(C, D, B, '؟', r=28), angle_arc(D, A, C, '؟', r=24)]
    return svg(body, 420, 240)


# Similar and congruent figures ------------------------------------------------

def two_tris(m1, m2, lab1, lab2, gap=40, w=420, h=240, ticks1=(), ticks2=()):
    W1 = max(p[0] for p in m1) - min(p[0] for p in m1)
    m2s = [(x + W1 + gap / 25 * 0 + 1.5, y) for x, y in m2]
    pts, s = fit(m1 + m2s, w, h, 40)
    t1, t2 = pts[:3], pts[3:]
    c1, c2 = centroid(t1), centroid(t2)
    body = [poly(t1), poly(t2)]
    for i, j, t in lab1:
        body.append(side_label(t1[i], t1[j], t, c1))
    for i, j, t in lab2:
        body.append(side_label(t2[i], t2[j], t, c2))
    for i, j, n in ticks1:
        body.append(ticks(t1[i], t1[j], n))
    for i, j, n in ticks2:
        body.append(ticks(t2[i], t2[j], n))
    return svg(body, w, h)


@fig('مثلثان متشابهان: أطوال أضلاع الأول ٥، ٦، ٨ سم، وأقصر ضلع في الثاني ١٠ سم. ما طول أطول ضلع في المثلث الثاني؟')
def _():
    t1 = tri_sss(8, 5, 6)
    t2 = [(x * 2, y * 2) for x, y in t1]
    return two_tris(t1, t2, [(0, 1, '٨ سم'), (0, 2, '٥ سم'), (1, 2, '٦ سم')],
                    [(0, 1, '؟'), (0, 2, '١٠ سم')], h=230)


@fig('صورة مستطيلة أبعادها ٤ سم × ٦ سم كُبّرت بحيث أصبح طولها ١٥ سم. كم يصبح عرضها إذا بقي الشكل متشابهاً؟')
def _():
    r1 = [(0, 0), (6, 0), (6, 4), (0, 4)]
    r2 = [(8 + x * 2.5, y * 2.5) for x, y in r1]
    pts, s = fit(r1 + r2, 420, 230, 58)
    a, b = pts[:4], pts[4:]
    body = [poly(a, fill=SHADE), poly(b, fill=SHADE),
            side_label(a[0], a[1], '٦ سم', centroid(a)), side_label(a[3], a[0], '٤ سم', centroid(a)),
            side_label(b[0], b[1], '١٥ سم', centroid(b)), side_label(b[1], b[2], '؟', centroid(b))]
    return svg(body, 420, 230)


@fig('المثلث أ ب ج يطابق المثلث د هـ و. إذا كان أ ب = ٥ سم، فما طول الضلع المناظر د هـ؟')
def _():
    t = tri_sss(6, 5, 4)  # أ=(0,0), ب? use vertices: 0=أ, 1=ج, 2=ب so أب=5 (left side)
    m2 = [(-x, y) for x, y in t]
    W = 6
    m2 = [(x + W * 2 + 3, y) for x, y in m2]
    pts, s = fit(t + m2, 420, 240, 45)
    a, b = pts[:3], pts[3:]
    ca, cb = centroid(a), centroid(b)
    body = [poly(a), poly(b),
            vlabel(a[0], 'أ', ca), vlabel(a[2], 'ب', ca), vlabel(a[1], 'ج', ca),
            vlabel(b[0], 'د', cb), vlabel(b[2], 'هـ', cb), vlabel(b[1], 'و', cb),
            side_label(a[0], a[2], '٥ سم', ca), side_label(b[0], b[2], '؟', cb),
            ticks(a[0], a[2], 1), ticks(b[0], b[2], 1), ticks(a[2], a[1], 2), ticks(b[2], b[1], 2),
            ticks(a[0], a[1], 3), ticks(b[0], b[1], 3)]
    return svg(body, 420, 240)


@fig('مثلثان متطابقان، أطوال أضلاع الأول ٤، ٥، ٦ سم. ما محيط الثاني؟')
def _():
    t1 = tri_sss(6, 4, 5)
    t2 = [(x, -y + max(p[1] for p in t1)) for x, y in t1]
    return two_tris(t1, t2, [(0, 1, '٦ سم'), (0, 2, '٤ سم'), (1, 2, '٥ سم')], [],
                    ticks1=[(0, 2, 1), (1, 2, 2), (0, 1, 3)], ticks2=[(0, 2, 1), (1, 2, 2), (0, 1, 3)])


# Parallelograms, triangles, trapezoids ----------------------------------------

@fig('متوازي أضلاع طول قاعدته ١٢ سم، وطول ضلعه المائل ٥ سم، وارتفاعه ٤ سم. احسبي محيطه ومساحته.')
def _():
    return para_fig(12, 5, 4, {'base': '١٢ سم', 'slant': '٥ سم', 'height': '٤ سم'})


@fig('مساحة متوازي أضلاع ٦٠ سم² وطول قاعدته ١٥ سم. ما ارتفاعه؟')
def _():
    return para_fig(15, None, 4, {'base': '١٥ سم', 'height': '؟', 'area': 'المساحة = ٦٠ سم²'}, left_off=3)


@fig('قطعة أرض على شكل متوازي أضلاع قاعدتها ٢٠ م وارتفاعها ٨ م وضلعها المائل ١٠ م. كم متراً من السياج تحتاج لإحاطتها؟')
def _():
    return para_fig(20, 10, 8, {'base': '٢٠ م', 'slant': '١٠ م', 'height': '٨ م'})


def tri_bh(base, height, apex_x, lab_b, lab_h, area=None, w=420, h=250):
    (A, B, C), s = fit([(0, 0), (base, 0), (apex_x, height)], w, h, 55)
    F = (C[0], A[1])
    body = [poly([A, B, C]), line(C, F, sw=1.5, dash=True), right_angle(F, C, B, 10),
            side_label(A, B, lab_b, centroid([A, B, C])),
            text(F[0] + 8, (C[1] + F[1]) / 2, lab_h, 18, anchor='start')]
    if area:
        body.append(text((A[0] + F[0]) / 2 + 4, F[1] - 22, area, 14))
    return svg(body, w, h)


@fig('مساحة المثلث = ½ × القاعدة × الارتفاع. ما مساحة مثلث قاعدته ١٠ سم وارتفاعه ٧ سم؟')
def _():
    return tri_bh(10, 7, 3.5, '١٠ سم', '٧ سم')


@fig('مثلث مساحته ٢٤ سم² وقاعدته ٨ سم. ما ارتفاعه؟')
def _():
    (A, B, C), s = fit([(0, 0), (8, 0), (5, 6)], 420, 260, 55)
    F = (C[0], A[1])
    body = [poly([A, B, C]), line(C, F, sw=1.5, dash=True), right_angle(F, C, B, 10),
            side_label(A, B, '٨ سم', centroid([A, B, C])),
            text(F[0] + 8, (C[1] + F[1]) / 2, '؟', 17, anchor='start'),
            text(C[0] + 90, C[1] + 16, 'المساحة = ٢٤ سم²', 17)]
    return svg(body, 420, 260)


def trapezoid(b1, b2, hgt, lab_b1, lab_b2, lab_h, lab_leg=None, iso=True, w=420, h=240, off=None):
    o = (b2 - b1) / 2 if iso else (off or 0)
    (A, B, C, D), s = fit([(0, 0), (b2, 0), (o + b1, hgt), (o, hgt)], w, h, 55)
    c = centroid([A, B, C, D])
    F = (D[0], A[1])
    body = [poly([A, B, C, D]), arrows(A, B), arrows(D, C), line(D, F, sw=1.5, dash=True), right_angle(F, D, B, 10),
            side_label(A, B, lab_b2, c), side_label(D, C, lab_b1, c),
            text(F[0] + 8, (D[1] + F[1]) / 2, lab_h, 18, anchor='start')]
    if lab_leg:
        body.append(side_label(B, C, lab_leg, c))
        body.append(side_label(A, D, lab_leg, c))
    if iso:
        body.append(ticks(A, D) + ticks(B, C))
    return svg(body, w, h)


@fig('مساحة شبه المنحرف = ½ × (ق١ + ق٢) × ع. احسبي المساحة إذا كانت ق١ = ٦، ق٢ = ١٠، ع = ٤.')
def _():
    (A, B, C, D), s = fit([(0, 0), (10, 0), (8, 4), (2, 4)], 420, 240, 55)
    c = centroid([A, B, C, D])
    F = (D[0], A[1])
    body = [poly([A, B, C, D]), arrows(A, B), arrows(D, C), line(D, F, sw=1.5, dash=True), right_angle(F, D, B, 10),
            side_label(A, B, 'ق٢ = ١٠', c), side_label(D, C, 'ق١ = ٦', c),
            text(F[0] + 8, (D[1] + F[1]) / 2, 'ع = ٤', 18, anchor='start')]
    return svg(body, 420, 240)


@fig('شبه منحرف متساوي الساقين قاعدتاه ٨ سم و١٤ سم وارتفاعه ٤ سم. ما محيطه؟')
def _():
    return trapezoid(8, 14, 4, '٨ سم', '١٤ سم', '٤ سم')


@fig('مثلثان لهما القاعدة نفسها ٦ سم ويقع رأساهما على خط يوازي القاعدة ويبعد عنها ٤ سم. قالت هدى إن مساحتيهما متساويتان. هل كلامها صحيح؟')
def _():
    (A, B, C1, C2, L1, L2), s = fit([(0, 0), (6, 0), (1.5, 4), (8.5, 4), (-2, 4), (10, 4)], 420, 230, 45)
    body = [line(L1, L2, sw=1.5), arrows(L1, (L1[0] + 60, L1[1])), arrows(add(A, (0, 0)), add(A, (60, 0))),
            poly([A, B, C1], fill='rgba(11,110,153,.15)'), poly([A, B, C2], fill='rgba(194,65,12,.12)'),
            side_label(A, B, '٦ سم', (A[0] + 50, A[1] - 40)),
            line((L1[0] + 4, L1[1]), (L1[0] + 4, A[1]), sw=1.3, dash=True),
            text(L1[0] + 12, (L1[1] + A[1]) / 2, '٤ سم', 17, anchor='start')]
    return svg(body, 420, 230)


@fig('في مستطيل طوله ١٠ سم وعرضه ٥ سم، رُسم مثلث قاعدته الضلع الطويل ورأسه على الضلع المقابل. ما مساحة المثلث؟')
def _():
    (A, B, C, D), s = fit([(0, 0), (10, 0), (10, 5), (0, 5)], 420, 240, 55)
    T = (A[0] + (B[0] - A[0]) * 0.35, D[1])
    c = centroid([A, B, C, D])
    body = [poly([A, B, C, D]), poly([A, B, T], fill=SHADE),
            side_label(A, B, '١٠ سم', c), side_label(B, C, '٥ سم', c)]
    for k, (p, q, r) in enumerate([(A, D, B), (B, A, C), (C, B, D), (D, C, A)]):
        body.append(right_angle(p, q, r, 10))
    return svg(body, 420, 240)


# Rectangles, squares, composite areas -----------------------------------------

@fig('مستطيل أبعاده ١٠ سم × ٦ سم، قُصّ منه مثلث قائم ضلعاه القائمان ٤ سم و٦ سم. ما مساحة الجزء الباقي؟')
def _():
    (A, B, C, D, E), s = fit([(0, 0), (10, 0), (10, 6), (0, 6), (6, 0)], 420, 250, 55)
    body = [HATCH, poly([A, E, C, D], fill=SHADE), poly([E, B, C], fill=CUT),
            right_angle(B, A, C, 11),
            side_label(D, C, '١٠ سم', (A[0] + 50, A[1] - 50)), side_label(A, D, '٦ سم', (A[0] + 50, A[1] - 50)),
            text((E[0] + B[0]) / 2, E[1] + 17, '٤ سم', 17),
            text(B[0] + 22, (B[1] + C[1]) / 2, '٦ سم', 17)]
    body.append(line((E[0], E[1] + 6), (E[0], E[1] - 6), sw=1.3))
    return svg(body, 420, 250)


@fig('مربع طول ضلعه ٨ سم، ظُلّل منه مثلث رأسه في منتصف أحد الأضلاع وقاعدته الضلع المقابل. ما مساحة الجزء المظلل؟')
def _():
    (A, B, C, D), s = fit([(0, 0), (8, 0), (8, 8), (0, 8)], 420, 270, 50)
    M = mid(D, C)
    c = centroid([A, B, C, D])
    body = [poly([A, B, C, D]), poly([A, B, M], fill=SHADE),
            side_label(A, B, '٨ سم', c), ticks(D, M), ticks(M, C), dot(M, 3.5)]
    for p, q, r in [(A, D, B), (B, A, C), (C, B, D), (D, C, A)]:
        body.append(right_angle(p, q, r, 10))
    return svg(body, 420, 270)


@fig('حديقة مستطيلة ١٥ م × ١٠ م، في وسطها حوض مربع ضلعه ٣ م. ما مساحة الحديقة المزروعة حول الحوض؟')
def _():
    (A, B, C, D, P, Q, R, S), s = fit([(0, 0), (15, 0), (15, 10), (0, 10), (6, 3.5), (9, 3.5), (9, 6.5), (6, 6.5)],
                                      420, 260, 50)
    c = centroid([A, B, C, D])
    body = [poly([A, B, C, D], fill='#d7ecd0'), poly([P, Q, R, S], fill='#bfe0f2'),
            side_label(A, B, '١٥ م', c), side_label(B, C, '١٠ م', c),
            text((P[0] + Q[0]) / 2, P[1] + 13, '٣ م', 13), text(c[0], c[1], 'حوض', 12, fill='#245')]
    return svg(body, 420, 260)


@fig('مستطيل طوله (س + ٣) وعرضه ٤. اكتبي تعبيراً جبرياً في أبسط صورة لمحيطه ولمساحته.')
def _():
    return rect_fig(9, 4, 'س + ٣', '٤')


@fig('مربع طول ضلعه (ص + ٢). ما التعبير الذي يمثل محيطه؟')
def _():
    return rect_fig(5, 5, 'ص + ٢', None, ticks4=True, h=280, pad=42)


@fig('مثلث أطوال أضلاعه س، (س + ١)، (س + ٢). اكتبي تعبيراً لمحيطه.')
def _():
    return triangle_fig(tri_sss(6, 4, 5), labels=[(0, 1, 'س + ٢'), (0, 2, 'س'), (1, 2, 'س + ١')])


@fig('مستطيل عرضه ن وطوله (ن + ٣). ما مساحته؟')
def _():
    return rect_fig(7, 4, 'ن + ٣', 'ن')


@fig('مستطيل طوله ٢س وعرضه س. ما مساحته؟')
def _():
    return rect_fig(8, 4, '٢س', 'س')


@fig('مستطيل طوله (ع + ٤) وعرضه ٥. ما مساحته؟')
def _():
    return rect_fig(9, 5, 'ع + ٤', '٥')


@fig('محيط مستطيل ٣٠ سم، وطوله (س + ٥) وعرضه س.\nأ) أوجدي قيمة س.\nب) أوجدي مساحة المستطيل.')
def _():
    return rect_fig(10, 5, 'س + ٥', 'س', inner='المحيط = ٣٠ سم')


@fig('محيط مربع ٣٦ سم وطول ضلعه (ص + ٤). ما قيمة ص؟')
def _():
    return rect_fig(5, 5, 'ص + ٤', None, inner='المحيط = ٣٦ سم', ticks4=True, h=280, pad=42)


@fig('مستطيل طوله ضعف عرضه، ومحيطه ٤٢ سم. ما بعداه؟')
def _():
    return rect_fig(14, 7, 'الطول', 'العرض', inner='المحيط = ٤٢ سم')


@fig('مستطيل أبعاده ١٥ سم × ٨ سم، قُصّ من أحد أركانه مربع طول ضلعه ص سم. اكتبي صيغة لمساحة الجزء الباقي.')
def _():
    (A, B, C, D, E, F, G), s = fit([(0, 0), (15, 0), (15, 5), (12, 5), (12, 8), (0, 8), (15, 8)], 420, 250, 55)
    body = [HATCH, poly([D, (G[0], E[1]), C], fill='none'), poly([A, B, C, D, E, F], fill=SHADE),
            poly([D, C, G, E], fill=CUT, sw=1.3, dash=True),
            side_label(A, B, '١٥ سم', (A[0] + 40, A[1] - 40)), side_label(A, F, '٨ سم', (A[0] + 40, A[1] - 40)),
            text((E[0] + G[0]) / 2, E[1] - 14, 'ص', 18), text(G[0] + 14, (G[1] + C[1]) / 2, 'ص', 18)]
    return svg(body, 420, 250)


@fig('مربع طول ضلعه ١٠ سم، قُصّ منه مستطيل أبعاده س × ٢. ما الصيغة التي تمثل المساحة الباقية؟')
def _():
    (A, B, C, D, P, Q, R, S), s = fit([(0, 0), (10, 0), (10, 10), (0, 10), (6, 10), (10, 10), (10, 8), (6, 8)],
                                      420, 270, 50)
    body = [HATCH, poly([A, B, C, D], fill=SHADE), poly([S, R, Q, P], fill=CUT, sw=1.3, dash=True),
            side_label(A, B, '١٠ سم', (A[0] + 40, A[1] - 40)), side_label(A, D, '١٠ سم', (A[0] + 40, A[1] - 40)),
            text((P[0] + Q[0]) / 2, P[1] - 14, 'س', 18), text(Q[0] + 14, (Q[1] + R[1]) / 2, '٢', 18)]
    return svg(body, 420, 270)


@fig('أرضية مستطيلة ٦ م × ٥ م، وُضعت فيها سجادة مربعة طول ضلعها ك م. ما مساحة الجزء غير المغطى إذا كانت ك = ٤؟')
def _():
    (A, B, C, D, P, Q, R, S), s = fit([(0, 0), (6, 0), (6, 5), (0, 5), (1, 0.5), (5, 0.5), (5, 4.5), (1, 4.5)],
                                      420, 260, 50)
    c = centroid([A, B, C, D])
    body = [poly([A, B, C, D], fill='#f3ede2'), poly([P, Q, R, S], fill='#c9b7e3'),
            side_label(A, B, '٦ م', c), side_label(B, C, '٥ م', c),
            text((S[0] + R[0]) / 2, S[1] + 24, 'ك', 18), text(Q[0] - 22, (Q[1] + R[1]) / 2, 'ك', 18),
            ticks(P, Q) + ticks(Q, R) + ticks(R, S) + ticks(S, P)]
    return svg(body, 420, 260)


@fig('مثلث أطوال أضلاعه (س + ٢)، (س + ٤)، (٢س). إذا كان محيطه ٢٢ سم، فما قيمة س؟')
def _():
    # With س = ٤ the sides are ٦، ٨، ٨.
    return triangle_fig(tri_sss(8, 6, 8), labels=[(0, 1, '٢س'), (0, 2, 'س + ٢'), (1, 2, 'س + ٤')], h=270)


@fig('مثلث متطابق الأضلاع طول ضلعه (ص + ٣) ومحيطه ٢٧ سم. ما قيمة ص؟')
def _():
    return triangle_fig(tri_sss(6, 6, 6), labels=[(0, 1, 'ص + ٣')], ticks_on=[(0, 1, 1), (1, 2, 1), (0, 2, 1)], h=260)


@fig('مستطيل طوله (٣ن − ١) وعرضه (ن + ١)، ومحيطه ٣٢ سم. أوجدي ن، ثم بُعدي المستطيل.')
def _():
    return rect_fig(11, 5, '٣ن − ١', 'ن + ١', inner='المحيط = ٣٢ سم')


@fig('مستطيل أبعاده ٨ سم × ٣ سم، ومثلث قاعدته ٨ سم ومساحته تساوي مساحة المستطيل. ما ارتفاع المثلث؟')
def _():
    m = [(0, 0), (8, 0), (8, 3), (0, 3), (10, 0), (18, 0), (13, 6)]
    pts, s = fit(m, 420, 230, 55)
    r, t = pts[:4], pts[4:]
    F = (t[2][0], t[0][1])
    body = [poly(r, fill=SHADE), poly(t, fill=SHADE),
            side_label(r[0], r[1], '٨ سم', centroid(r)), side_label(r[3], r[0], '٣ سم', centroid(r)),
            side_label(t[0], t[1], '٨ سم', centroid(t)),
            line(t[2], F, sw=1.5, dash=True), right_angle(F, t[2], t[1], 9),
            text(F[0] + 8, (t[2][1] + F[1]) / 2, '؟', 17, anchor='start')]
    for k in range(4):
        body.append(right_angle(r[k], r[k - 1], r[(k + 1) % 4], 9))
    return svg(body, 420, 230)


@fig('مستطيل محيطه ١٨ سم وطوله ٦ سم. ما مساحته؟')
def _():
    return rect_fig(6, 3, '٦ سم', '؟', inner='المحيط = ١٨ سم')


@fig('مربع مساحته ٤٩ سم². ما محيطه؟')
def _():
    return rect_fig(7, 7, None, None, inner='المساحة = ٤٩ سم²', ticks4=True, h=280, pad=42)


@fig('مستطيل محيطه ٢٠ سم ومساحته ٢٤ سم². ما بعداه؟')
def _():
    return rect_fig(6, 4, '؟', '؟', inner='المساحة = ٢٤ سم²\nالمحيط = ٢٠ سم', h=260, pad=45)


# Pythagoras -----------------------------------------------------------------

def rect_diag(L, W, lab_l, lab_w, lab_d, w=420, h=250, ticks4=False):
    (A, B, C, D), s = fit([(0, 0), (L, 0), (L, W), (0, W)], w, h, 55)
    c = centroid([A, B, C, D])
    body = [poly([A, B, C, D]), line(A, C, dash=True)]
    for p, q, r in [(A, D, B), (B, A, C), (C, B, D), (D, C, A)]:
        body.append(right_angle(p, q, r, 10))
    if lab_l:
        body.append(side_label(A, B, lab_l, c))
    if lab_w:
        body.append(side_label(B, C, lab_w, c))
    if lab_d:
        m = mid(A, C)
        n = unit((-(C[1] - A[1]), C[0] - A[0]))
        body.append(text(m[0] - n[0] * 16 - 6, m[1] - n[1] * 16, lab_d, 18))
    if ticks4:
        for p, q in [(A, B), (B, C), (C, D), (D, A)]:
            body.append(ticks(p, q))
    return svg(body, w, h)


@fig('بطاقة مستطيلة ١٢ سم × ٩ سم. هل تدخل بشكل مائل (قطرياً) في شق طوله ١٤ سم؟')
def _():
    return rect_diag(12, 9, '١٢ سم', '٩ سم', None)


@fig('شاشة تلفاز أبعادها ٨٠ سم × ٦٠ سم. ما طول قطرها؟')
def _():
    return rect_diag(80, 60, '٨٠ سم', '٦٠ سم', '؟')


@fig('صندوق قاعدته مربعة ضلعها ٣٠ سم. هل تدخل عصا طولها ٤٠ سم مستلقية على قاعدته؟ فسّري.')
def _():
    return rect_diag(30, 30, '٣٠ سم', '٣٠ سم', None, h=270, ticks4=True)


@fig('مستطيل طوله ١٢ سم وقطره ١٣ سم. ما عرضه؟')
def _():
    return rect_diag(12, 5, '١٢ سم', '؟', '١٣ سم')


@fig('مثلث قائم ضلعاه القائمان ٩ سم و١٢ سم. ما طول الوتر؟')
def _():
    return triangle_fig([(0, 0), (12, 0), (0, 9)], labels=[(0, 1, '١٢ سم'), (0, 2, '٩ سم'), (1, 2, '؟')], right=0)


@fig('مثلث قائم وتره ١٠ سم وأحد ضلعيه القائمين ٦ سم. ما مساحته؟')
def _():
    return triangle_fig([(0, 0), (8, 0), (0, 6)], labels=[(0, 2, '٦ سم'), (1, 2, '١٠ سم')], right=0)


@fig('مثلث متطابق الضلعين ساقاه ١٣ سم وقاعدته ١٠ سم. ما ارتفاعه؟')
def _():
    def h_(pts, s):
        F = mid(pts[0], pts[1])
        return (line(pts[2], F, sw=1.5, dash=True) + right_angle(F, pts[2], pts[1], 10) +
                text(F[0] + 8, (pts[2][1] + F[1]) / 2, '؟', 17, anchor='start'))
    return triangle_fig(tri_sss(10, 13, 13), labels=[(0, 1, '١٠ سم'), (0, 2, '١٣ سم'), (1, 2, '١٣ سم')],
                        ticks_on=[(0, 2, 1), (1, 2, 1)], extra=h_, h=280)


@fig('مثلث ارتفاعه ١٢ سم، يقسم قاعدته إلى جزأين: ٥ سم وجزء آخر. الضلع المقابل للجزء الآخر طوله ١٥ سم. ما مساحة المثلث؟')
def _():
    (A, B, C), s = fit([(0, 0), (14, 0), (5, 12)], 420, 280, 50)
    F = (C[0], A[1])
    cc = centroid([A, B, C])
    body = [poly([A, B, C]), line(C, F, sw=1.5, dash=True), right_angle(F, C, B, 10),
            text(F[0] + 8, (C[1] + F[1]) / 2, '١٢ سم', 17, anchor='start'),
            text((A[0] + F[0]) / 2, A[1] + 16, '٥ سم', 17), text((F[0] + B[0]) / 2, A[1] + 16, '؟', 18),
            side_label(B, C, '١٥ سم', cc)]
    return svg(body, 420, 280)


def dim(a, b, label, side, size=15):
    """Dimension line parallel to ab, shifted by the vector `side`, with end bars and a label."""
    a2, b2 = add(a, side), add(b, side)
    u = unit(side)
    out = [line(a, add(a2, mul(u, 5)), sw=1, stroke='#888'), line(b, add(b2, mul(u, 5)), sw=1, stroke='#888'),
           line(a2, b2, sw=1.3, stroke='#333')]
    for p, q in ((a2, b2), (b2, a2)):
        v = unit(sub(q, p))
        n = (-v[1], v[0])
        out.append(f'<polygon points="{P([p, add(add(p, mul(v, 9)), mul(n, 4)), add(add(p, mul(v, 9)), mul(n, -4))])}" fill="#333"/>')
    m = add(mid(a2, b2), mul(u, 14 + abs(u[0]) * len(label) * 4))
    out.append(text(m[0], m[1], label, size))
    return ''.join(out)


@fig('معين طولا قطريه ٦ سم و٨ سم. ما طول ضلعه؟')
def _():
    (A, B, C, D, O), s = fit([(0, 0), (4, 3), (8, 0), (4, -3), (4, 0)], 420, 270, 55)
    body = [poly([A, B, C, D]), line(A, C, sw=1.5, dash=True), line(B, D, sw=1.5, dash=True),
            right_angle(O, C, B, 10), ticks(A, B) + ticks(B, C) + ticks(C, D) + ticks(D, A),
            dim(A, C, '٨ سم', (0, D[1] - O[1] + 22)),
            dim(D, B, '٦ سم', (C[0] - O[0] + 24, 0)),
            side_label(A, B, '؟', O)]
    return svg(body, 420, 270)


@fig('مثلث أطوال أضلاعه ٦، ٨، ١٠ سم. هل هو قائم الزاوية؟ فسّري.')
def _():
    return triangle_fig(tri_sss(10, 6, 8), labels=[(0, 1, '١٠ سم'), (0, 2, '٦ سم'), (1, 2, '٨ سم')])


@fig('هل المثلث الذي أضلاعه ٤، ٦، ٧ قائم الزاوية؟')
def _():
    return triangle_fig(tri_sss(7, 4, 6), labels=[(0, 1, '٧'), (0, 2, '٤'), (1, 2, '٦')])


# Circles ---------------------------------------------------------------------

@fig('يمشي سالم من أ إلى ب على قطر دائرة نصف قطرها ١٤ م، بينما تمشي أخته على نصف محيط الدائرة. كم متراً تمشي أكثر منه؟ (استخدمي ط = ٢٢/٧)')
def _():
    O, r = (210, 150), 105
    A, B = (O[0] + r, O[1]), (O[0] - r, O[1])
    body = [circle(O, r, sw=1.5),
            f'<path d="M{A[0]},{A[1]} A{r},{r} 0 0 0 {B[0]},{B[1]}" fill="none" stroke="#c2410c" stroke-width="3.5" stroke-dasharray="9 5"/>',
            line(A, B, sw=3, stroke='#0b6e99'), dot(O, 3.5), dot(A), dot(B),
            text(A[0] + 16, A[1], 'أ', 17, weight='bold'), text(B[0] - 16, B[1], 'ب', 17, weight='bold'),
            text((O[0] + A[0]) / 2, O[1] + 15, '١٤ م', 17),
            text(O[0], O[1] - r - 14, 'طريق الأخت', 13, fill='#c2410c'),
            text(O[0] - 50, O[1] - 13, 'طريق سالم', 13, fill='#0b6e99')]
    return svg(body, 420, 280)


@fig('مضمار دائري نصف قطره ٧ م. ما طول دورة كاملة حوله؟ (ط = ٢٢/٧)')
def _():
    O, r = (210, 135), 100
    E = (O[0] + r, O[1])
    body = [circle(O, r, fill='#eef6fa', sw=2.5), line(O, E), dot(O, 3.5),
            text((O[0] + E[0]) / 2, O[1] - 13, '٧ م', 18)]
    return svg(body, 420, 270)


@fig('يريد طفلان الوصول من مركز ملعب دائري نصف قطره ٢١ م إلى نقطة على حافته: الأول يسير مستقيماً، والثاني يسير إلى الحافة ثم ربع المحيط. هل السباق عادل؟ فسّري. (ط = ٢٢/٧)')
def _():
    O, r = (210, 145), 105
    A = (O[0] + r, O[1])          # finish point
    B = (O[0], O[1] - r)          # second child reaches the edge here
    body = [circle(O, r, sw=1.5), line(O, A, sw=3, stroke='#0b6e99'), line(O, B, sw=3, stroke='#c2410c'),
            f'<path d="M{B[0]},{B[1]} A{r},{r} 0 0 1 {A[0]},{A[1]}" fill="none" stroke="#c2410c" stroke-width="3.5" stroke-dasharray="9 5"/>',
            right_angle(O, A, B, 11), dot(O), dot(A),
            text(O[0] - 18, O[1] + 14, 'م', 18, weight='bold'), text(A[0] + 16, A[1], 'أ', 17, weight='bold'),
            text((O[0] + A[0]) / 2, O[1] + 15, '٢١ م', 17),
            text(O[0] - 28, O[1] - r / 2, '٢١ م', 17),
            text(O[0] + 60, O[1] + 44, 'الأول', 13, fill='#0b6e99'), text(O[0] + 86, O[1] - r + 4, 'الثاني', 13, fill='#c2410c')]
    return svg(body, 420, 280)


# Grids and estimation ----------------------------------------------------------

def unit_grid(n, m, u, X0=20, Y0=20, color='#cfd8e0'):
    out = []
    for i in range(n + 1):
        out.append(line((X0 + i * u, Y0), (X0 + i * u, Y0 + m * u), sw=1, stroke=color))
    for j in range(m + 1):
        out.append(line((X0, Y0 + j * u), (X0 + n * u, Y0 + j * u), sw=1, stroke=color))
    return out


@fig('رُسم شكل غير منتظم على شبكة مربعات طول ضلع كل مربع ١ سم. يغطي الشكل ٧ مربعات كاملة و٦ أنصاف مربعات تقريباً. ما أفضل تقدير لمساحته؟')
def _():
    u, X0, Y0 = 40, 50, 20
    n, m = 7, 5
    def c(x, y):  # grid point (x right, y down)
        return (X0 + x * u, Y0 + y * u)
    # 7 full cells: (2..4, 1..2) and (3, 3); 6 halves cut on the diagonals around them.
    outline = [c(2, 1), c(3, 0), c(4, 1), c(5, 1), c(6, 2), c(5, 3), c(4, 3), c(4, 4), c(3, 4), c(3, 3),
               c(2, 3), c(1, 2)]
    body = unit_grid(n, m, u, X0, Y0)
    body.append(poly(outline, fill='rgba(11,110,153,.30)', stroke='#0b6e99', sw=2))
    body.append(text(X0 + n * u / 2, Y0 + m * u + 18, '□ = ١ سم²', 13, fill='#333'))
    return svg(body, X0 * 2 + n * u, Y0 + m * u + 36)


@fig('بحيرة مرسومة على خريطة شبكية كل مربع فيها ١ كم². تغطي البحيرة ١٢ مربعاً كاملاً و٨ مربعات جزئياً. ما أفضل تقدير لمساحتها؟')
def _():
    u, X0, Y0 = 40, 50, 20
    n, m = 8, 6
    # 12 full cells: columns 2..5, rows 2..4 (4 × 3). Eight partial cells get a bump each.
    x0, y0, x1, y1 = 2, 2, 6, 5
    def g(x, y):
        return (X0 + x * u, Y0 + y * u)
    d = []
    def bump_h(xa, y, dirn):  # bump across cell edge from xa to xa+1 on row line y (dirn -1 up, +1 down)
        a, b = g(xa + 0.15, y), g(xa + 0.85, y)
        cx, cy = g(xa + 0.5, y + dirn * 0.75)
        return f' L{f(a[0])},{f(a[1])} Q{f(cx)},{f(cy)} {f(b[0])},{f(b[1])}'
    def bump_v(x, ya, dirn):
        a, b = g(x, ya + 0.15), g(x, ya + 0.85)
        cx, cy = g(x + dirn * 0.75, ya + 0.5)
        return f' L{f(a[0])},{f(a[1])} Q{f(cx)},{f(cy)} {f(b[0])},{f(b[1])}'
    def bump_v_rev(x, ya, dirn):
        a, b = g(x, ya + 0.85), g(x, ya + 0.15)
        cx, cy = g(x + dirn * 0.75, ya + 0.5)
        return f' L{f(a[0])},{f(a[1])} Q{f(cx)},{f(cy)} {f(b[0])},{f(b[1])}'
    s = g(x0, y0)
    d.append(f'M{f(s[0])},{f(s[1])}')
    for xa in (2, 4, 5):          # top: 3 bumps
        d.append(bump_h(xa, y0, -1))
    e = g(x1, y0); d.append(f' L{f(e[0])},{f(e[1])}')
    for ya in (2, 4):             # right: 2 bumps
        d.append(bump_v(x1, ya, 1))
    e = g(x1, y1); d.append(f' L{f(e[0])},{f(e[1])}')
    for xa in (4, 3):             # bottom (right to left): 2 bumps
        a, b = g(xa + 0.85, y1), g(xa + 0.15, y1)
        cx, cy = g(xa + 0.5, y1 + 0.75)
        d.append(f' L{f(a[0])},{f(a[1])} Q{f(cx)},{f(cy)} {f(b[0])},{f(b[1])}')
    e = g(x0, y1); d.append(f' L{f(e[0])},{f(e[1])}')
    d.append(bump_v_rev(x0, 3, -1))   # left: 1 bump
    d.append(' Z')
    body = unit_grid(n, m, u, X0, Y0)
    body.append(f'<path d="{"".join(d)}" fill="rgba(56,140,200,.35)" stroke="#2b6f9e" stroke-width="2" stroke-linejoin="round"/>')
    body.append(text(X0 + n * u / 2, Y0 + m * u + 18, '□ = ١ كم²', 13, fill='#333'))
    return svg(body, X0 * 2 + n * u, Y0 + m * u + 36)


# Solids and nets --------------------------------------------------------------

@fig('علبة على شكل متوازي مستطيلات أبعادها ٤ سم × ٣ سم × ٢ سم. ما مساحتها الكلية؟')
def _():
    return box3d(4, 3, 2, ('٤ سم', '٣ سم', '٢ سم'))[0]


@fig('مكعب طول حرفه ٥ سم. كم سنتيمتراً مربعاً من الورق نحتاج لتغليفه كاملاً؟')
def _():
    return box3d(5, 5, 5, ('٥ سم', '٥ سم', '٥ سم'), h=280)[0]


@fig('صندوق بلا غطاء أبعاده ١٠ سم × ٦ سم × ٤ سم. ما مساحة الورق اللازم لتغطية سطحه الخارجي؟')
def _():
    return box3d(10, 6, 4, ('١٠ سم', '٦ سم', '٤ سم'), open_top=True)[0]


@fig('شبكة مكونة من ٦ مربعات متطابقة: ٤ مربعات في صف واحد، ومربع فوق المربع الثاني، ومربع تحت المربع الثاني أيضاً. هل تُطوى لتكوّن مكعباً؟')
def _():
    return net_fig([(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (1, 2)])


@fig('شبكة من ٦ مربعات: ٤ مربعات في صف، ومربعان فوق المربع الأول والثاني. هل تكوّن مكعباً؟ فسّري.')
def _():
    return net_fig([(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (1, 0)])


SIM_FIX = {
    # The original wording put both triangles over the same rectangle, which cannot be drawn.
    'شبكة فيها ٣ مستطيلات في صف ومثلثان على جهة واحدة من الصف (كلاهما فوق المستطيل الأوسط). هل تكوّن منشوراً ثلاثياً؟ فسّري.':
        'شبكة فيها ٣ مستطيلات في صف، ومثلثان على جهة واحدة من الصف (فوق المستطيل الأول وفوق المستطيل الأوسط) كما في الشكل. هل تكوّن منشوراً ثلاثياً؟ فسّري.',
}
EXPLAIN_FIX = {
    'شبكة فيها ٣ مستطيلات في صف، ومثلثان على جهة واحدة من الصف (فوق المستطيل الأول وفوق المستطيل الأوسط) كما في الشكل. هل تكوّن منشوراً ثلاثياً؟ فسّري.':
        'عند الطي يغطي المثلثان الطرف نفسه فيتداخلان، ويبقى الطرف الآخر مفتوحاً. يجب أن يكون أحد المثلثين فوق الصف والآخر تحته ليغطيا القاعدتين.',
}


@fig('شبكة فيها ٣ مستطيلات في صف، ومثلثان على جهة واحدة من الصف (فوق المستطيل الأول وفوق المستطيل الأوسط) كما في الشكل. هل تكوّن منشوراً ثلاثياً؟ فسّري.')
def _():
    return net_fig([(0, 1), (1, 1), (2, 1)], tris=[(0, 1, 't'), (1, 1, 't')], h=230)


@fig('صندوق أبعاده ٣ × ٢ × ٢ مكعبات. كم مكعباً يملؤه؟')
def _():
    return cubes_fig([(x, y, z) for x in range(3) for y in range(2) for z in range(2)], 3, 2, 2)


@fig('مكعب كبير مكوّن من مكعبات صغيرة، طول حرفه ٣ مكعبات. كم مكعباً صغيراً فيه؟')
def _():
    return cubes_fig([(x, y, z) for x in range(3) for y in range(3) for z in range(3)], 3, 3, 3)


@fig('صندوق ٤ × ٣ × ٢ وُضع فيه ١٥ مكعباً. كم مكعباً يلزم لملئه؟')
def _():
    cells = [(x, y, 0) for x in range(4) for y in range(3)] + [(0, 0, 1), (1, 0, 1), (0, 1, 1)]
    return cubes_fig(cells, 4, 3, 2, frame=True)


# Coordinates and transformations ----------------------------------------------

@fig('نُقل شكل ٣ وحدات إلى اليمين ووحدتين إلى الأعلى دون أن يدور أو ينقلب. ما اسم هذا التحويل؟')
def _():
    g = Grid(0, 9, 0, 6, unit_px=36)
    shape = [(1, 1), (3, 1), (3, 2), (2, 2), (2, 3), (1, 3)]
    img = [(x + 3, y + 2) for x, y in shape]
    g.body.append(poly([g.p(*p) for p in shape], fill='rgba(11,110,153,.25)', stroke='#0b6e99'))
    g.body.append(poly([g.p(*p) for p in img], fill='rgba(194,65,12,.18)', stroke='#c2410c', dash=True))
    a, b = g.p(1, 1), g.p(4, 3)
    g.body.append(line(a, b, sw=1.5, stroke='#555') + dot(b, 3, '#555'))
    return g.svg()


@fig('النقطة (٢، ٣) انعكست حول المحور الصادي ثم سُحبت وحدة واحدة إلى الأسفل. ما إحداثيات صورتها؟')
def _():
    return plane([(2, 3)], x0=-4, x1=4, y0=-1, y1=4)


@fig('النقطة (٣، ٤) انعكست حول المحور السيني. ما إحداثيات صورتها؟')
def _():
    return plane([(3, 4)], x0=-1, x1=5, y0=-5, y1=5)


@fig('شكل مكوّن من ٣ مربعات مظللة فوق خط أفقي ل مباشرة: الأول والثالث في الصف الأول، والثاني في الصف الثاني. أين تقع المربعات المظللة في صورته بالانعكاس حول ل؟')
def _():
    u, X0, Y0, n, m = 40, 40, 20, 7, 6
    body = unit_grid(n, m, u, X0, Y0)
    yl = Y0 + 3 * u
    for cx, row in [(2, 1), (4, 1), (3, 2)]:
        x, y = X0 + cx * u, yl - row * u
        body.append(poly([(x, y), (x + u, y), (x + u, y + u), (x, y + u)], fill='#0b6e99', sw=1))
    body += [line((X0 - 10, yl), (X0 + n * u + 10, yl), sw=3), text(X0 + n * u + 22, yl, 'ل', 17, weight='bold')]
    return svg(body, X0 * 2 + n * u + 10, Y0 * 2 + m * u)


@fig('النقطة (٢، ٠) دارت ٩٠° في اتجاه عقارب الساعة حول نقطة الأصل، ثم انعكست حول المحور الصادي. ما إحداثيات صورتها النهائية؟')
def _():
    return plane([(2, 0)], x0=-3, x1=3, y0=-3, y1=3, offs=[(10, -14)])


@fig('النقطة (١، ٣) دارت ١٨٠° حول نقطة الأصل. ما إحداثيات صورتها؟')
def _():
    return plane([(1, 3)], x0=-4, x1=4, y0=-4, y1=4)


@fig('رؤوس مثلث: أ(١، ٢)، ب(٣، ٢)، ج(١، ٥). أُجري له انسحاب ٢ وحدة إلى اليسار و٣ وحدات إلى الأسفل. ما إحداثيات رؤوس الصورة؟')
def _():
    return plane([(1, 2), (3, 2), (1, 5)], x0=-3, x1=5, y0=-3, y1=6, polygon=True, names=['أ', 'ب', 'ج'],
                 show=False, offs=[(-12, 10), (12, 10), (-12, -10)])


@fig('النقطة (−٢، ٤) سُحبت ٥ وحدات إلى اليمين. ما إحداثياتها الجديدة؟')
def _():
    return plane([(-2, 4)], x0=-4, x1=5, y0=-1, y1=5)


@fig('انتقلت النقطة م(٢، ١) بانسحاب إلى م′(٦، −٢). صفي الانسحاب.')
def _():
    return plane([(2, 1), (6, -2)], x0=-1, x1=7, y0=-3, y1=3, names=['م', 'م′'], offs=[(14, -12), (16, 12)], show=False)


@fig('مستطيل رؤوسه (١، ١)، (٥، ١)، (٥، ٤). ما إحداثيات الرأس الرابع؟')
def _():
    return plane([(1, 1), (5, 1), (5, 4)], x0=-1, x1=6, y0=-1, y1=5, offs=[(0, 14), (0, 14), (0, -14)])


@fig('مثلث متطابق الضلعين قاعدته من (٠، ٠) إلى (٦، ٠). أي نقطة تصلح رأساً ثالثاً؟')
def _():
    g = Grid(-1, 7, -1, 5, unit_px=36)
    a, b = g.p(0, 0), g.p(6, 0)
    g.body.append(line(a, b, sw=3, stroke='#0b6e99') + dot(a, 4.5) + dot(b, 4.5))
    return g.svg()


@fig('مربع رأسان متجاوران فيه (٢، ٢) و(٢، ٥). اكتبي إحداثيات رأسين آخرين ممكنين.')
def _():
    g = Grid(-2, 6, -1, 6, unit_px=34)
    a, b = g.p(2, 2), g.p(2, 5)
    g.body.append(line(a, b, sw=3, stroke='#0b6e99'))
    g.point(2, 2, show=True, dx=34, dy=0)
    g.point(2, 5, show=True, dx=34, dy=0)
    return g.svg()


@fig('مثلث رؤوسه (٠، ٠)، (٣، ٠)، (٠، ٢). أُجري له انسحاب ٤ وحدات يميناً ووحدة للأعلى. ما رؤوس الصورة؟')
def _():
    return plane([(0, 0), (3, 0), (0, 2)], x0=-1, x1=8, y0=-1, y1=4, polygon=True, show=False)


@fig('صورة النقطة (٥، −١) بعد انسحاب وحدتين لليسار و٣ للأعلى هي:')
def _():
    return plane([(5, -1)], x0=-1, x1=6, y0=-2, y1=3, offs=[(0, 16)])


@fig('مربع رؤوسه (١، ١)، (٤، ١)، (٤، ٤)، (١، ٤). شكل مطابق له رؤوسه (٦، ١)، (٩، ١)، (٩، ٤). ما الرأس الرابع؟')
def _():
    g = Grid(-1, 10, -1, 5, unit_px=32)
    sq = [g.p(*p) for p in [(1, 1), (4, 1), (4, 4), (1, 4)]]
    g.body.append(poly(sq, fill='rgba(11,110,153,.15)', stroke='#0b6e99'))
    for p in [(1, 1), (4, 1), (4, 4), (1, 4), (6, 1), (9, 1), (9, 4)]:
        g.point(*p)
    a, b, c = g.p(6, 1), g.p(9, 1), g.p(9, 4)
    g.body.append(line(a, b, sw=2, stroke='#c2410c') + line(b, c, sw=2, stroke='#c2410c'))
    return g.svg()


@fig('مثلث رؤوسه (٠، ٠)، (٢، ٠)، (٠، ٣). مثلث مطابق له رأسان منه (٥، ٥) و(٧، ٥). ما رأسه الثالث الممكن؟')
def _():
    g = Grid(-1, 8, -1, 8, unit_px=30)
    t = [g.p(*p) for p in [(0, 0), (2, 0), (0, 3)]]
    g.body.append(poly(t, fill='rgba(11,110,153,.15)', stroke='#0b6e99'))
    for p in [(0, 0), (2, 0), (0, 3), (5, 5), (7, 5)]:
        g.point(*p)
    g.body.append(line(g.p(5, 5), g.p(7, 5), sw=2, stroke='#c2410c'))
    return g.svg()


@fig('مستطيل رؤوسه (٠، ٠)، (٨، ٠)، (٨، ٦)، (٠، ٦). ما إحداثيات نقطة تقاطع قطريه؟')
def _():
    return plane([(0, 0), (8, 0), (8, 6), (0, 6)], x0=-1, x1=9, y0=-1, y1=7, polygon=True, diag=True, show=False)


@fig('مربع رؤوسه (١، ١)، (٥، ١)، (٥، ٥)، (١، ٥). ما نقطة تقاطع قطريه؟')
def _():
    return plane([(1, 1), (5, 1), (5, 5), (1, 5)], x0=-1, x1=6, y0=-1, y1=6, polygon=True, diag=True, show=False)


@fig('النقطتان أ(١، ٣) و ب(٧، ٣). اكتبي إحداثيات نقطة على مسافة متساوية منهما.')
def _():
    return plane([(1, 3), (7, 3)], x0=-1, x1=8, y0=-1, y1=5, names=['أ', 'ب'], show=False, offs=[(0, -15), (0, -15)])


@fig('النقطتان م(٢، ١) و ن(٦، ١). أعطي إحداثيات نقطة ل تجعل المثلث م ن ل متطابق الضلعين (ل م = ل ن).')
def _():
    return plane([(2, 1), (6, 1)], x0=-1, x1=8, y0=-1, y1=6, names=['م', 'ن'], show=False, offs=[(0, 15), (0, 15)])


@fig('مثلث رأساه (٠، ٠) و(٤، ٠). أي رأس ثالث يجعله متطابق الضلعين؟')
def _():
    g = Grid(-1, 5, -1, 4, unit_px=38)
    a, b = g.p(0, 0), g.p(4, 0)
    g.body.append(line(a, b, sw=3, stroke='#0b6e99') + dot(a, 4.5) + dot(b, 4.5))
    return g.svg()


@fig('مثلث رؤوسه (١، ١)، (٥، ١)، (٣، ٤). ما نوعه من حيث الأضلاع؟')
def _():
    return plane([(1, 1), (5, 1), (3, 4)], x0=-1, x1=6, y0=-1, y1=5, polygon=True, show=False)


def build():
    return {q: fn() for q, fn in FIG.items()}
