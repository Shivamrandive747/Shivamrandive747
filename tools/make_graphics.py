"""Generate the SVG graphics for the GitHub profile README.

Writes light and dark variants of every graphic into ../assets/.
Run:  python tools/make_graphics.py
"""
import math
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

SERIF = "Georgia, 'Times New Roman', serif"
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

THEMES = {
    "light": dict(
        bg="#ffffff", bg2="#f3f7fb", bg3="#e7eff8", card="#f6f8fa", border="#d0d7de",
        text="#1f2328", muted="#59636e", faint="#8c959f", accent="#0b4f8a", teal="#1a7f72",
        orange="#bc4c00", chip="#ffffff", dots="#0b4f8a", bond="#aab4be",
        statbg="#eef3f8",
    ),
    "dark": dict(
        bg="#0d1117", bg2="#0f1a2b", bg3="#142540", card="#161b22", border="#30363d",
        text="#e6edf3", muted="#9198a1", faint="#6e7681", accent="#79c0ff", teal="#56d4c3",
        orange="#f0883e", chip="#0d1117", dots="#79c0ff", bond="#4a5563",
        statbg="#1c2533",
    ),
}

def wrap(text, max_chars):
    """Greedy word wrap by character count (good enough for fixed font sizes)."""
    lines, line = [], ""
    for word in text.split():
        cand = f"{line} {word}".strip()
        if len(cand) <= max_chars or not line:
            line = cand
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def dot_pattern(t, pid, spacing=22, r=1.1, opacity=0.18):
    return (f'<pattern id="{pid}" width="{spacing}" height="{spacing}" patternUnits="userSpaceOnUse">'
            f'<circle cx="{spacing/2}" cy="{spacing/2}" r="{r}" fill="{t["dots"]}" opacity="{opacity}"/></pattern>')


# ---------------------------------------------------------------- ML-for-materials loop
def loop_diagram(c, mid, title_fs=14, sub_fs=11.5, subtitles=True):
    """Structure -> learn -> predict -> verify, drawn in a 440 x 430 box.

    `c` maps roles to colours (hex, or var(--x) for the website); everything is styled
    through style="" so CSS variables work. `mid` keeps marker ids unique per document.
    Returns (defs, body).
    """
    S = lambda **kw: "; ".join(f"{k.replace('_', '-')}:{v}" for k, v in kw.items())
    W, H = 180, 170
    panels = [((20, 20), "1", "Structure", "crystal → graph"),
              ((240, 20), "2", "Learn", "GNN · interatomic potential"),
              ((240, 240), "3", "Predict", "DOS · Seebeck · κL"),
              ((20, 240), "4", "Verify", "against DFT & experiment")]
    defs = (f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="{S(fill=c["accent"])}"/></marker>')
    out = []

    def structure():
        g, pos = [], {}
        for i in range(5):
            for j in range(4):
                pos[i, j] = (30 + 30 * i, 54 + 26 * j)
        hub = (2, 1)
        for (i, j), (x, y) in pos.items():
            for di, dj in ((1, 0), (0, 1)):
                if (i + di, j + dj) in pos:
                    x2, y2 = pos[i + di, j + dj]
                    near = hub in ((i, j), (i + di, j + dj))
                    st = S(stroke=c["accent"], stroke_width=2.2) if near else S(stroke=c["muted"], stroke_width=1, opacity=.45)
                    g.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" style="{st}"/>')
        hx, hy = pos[hub]
        g.append(f'<circle cx="{hx}" cy="{hy}" r="12" style="{S(fill="none", stroke=c["teal"], stroke_width=1.5, stroke_dasharray="3 3")}"/>')
        for (i, j), (x, y) in pos.items():
            a = (i + j) % 2 == 0
            g.append(f'<circle cx="{x}" cy="{y}" r="{6.5 if a else 4.5}" style="{S(fill=c["accent"] if a else c["teal"])}"/>')
        return g

    def learn():
        g, layers = [], []
        for x, n in ((26, 4), (70, 5), (114, 4), (156, 1)):
            layers.append([(x, 93 + (k - (n - 1) / 2) * 20) for k in range(n)])
        pulse = {(0, 1, 2), (1, 2, 1), (2, 0, 0), (0, 3, 3), (1, 4, 3)}
        for li in range(3):
            for a, (x1, y1) in enumerate(layers[li]):
                for b, (x2, y2) in enumerate(layers[li + 1]):
                    g.append(f'<line x1="{x1}" y1="{y1:.0f}" x2="{x2}" y2="{y2:.0f}" style="{S(stroke=c["muted"], stroke_width=1, opacity=.3)}"/>')
                    if (li, a, b) in pulse:
                        g.append(f'<line class="pulse" x1="{x1}" y1="{y1:.0f}" x2="{x2}" y2="{y2:.0f}" style="{S(stroke=c["accent"], stroke_width=2)}"/>')
        for li, layer in enumerate(layers):
            for x, y in layer:
                last = li == 3
                g.append(f'<circle cx="{x}" cy="{y:.0f}" r="{7 if last else 5.5}" '
                         f'style="{S(fill=c["accent"] if last else c["panel"], stroke=c["accent"], stroke_width=1.6)}"/>')
        return g

    def predict():
        peaks = [(32, 42, 8), (54, 62, 7), (72, 34, 6), (116, 40, 6), (134, 66, 8), (155, 38, 6)]
        pts = []
        for n in range(73):
            x = 20 + 2 * n
            v = 0 if 84 < x < 104 else sum(A * math.exp(-((x - m) / s) ** 2) for m, A, s in peaks)
            pts.append(f"{x},{132 - v:.1f}")
        line = "M" + " L".join(pts)
        return [f'<path d="{line} L164,132 L20,132 Z" style="{S(fill=c["accent"], opacity=.14)}"/>',
                f'<path d="{line}" style="{S(fill="none", stroke=c["accent"], stroke_width=1.8, stroke_linejoin="round")}"/>',
                f'<line x1="16" y1="132" x2="168" y2="132" style="{S(stroke=c["muted"], stroke_width=1)}"/>',
                f'<line x1="94" y1="46" x2="94" y2="132" style="{S(stroke=c["now"], stroke_width=1.4, stroke_dasharray="3 3")}"/>',
                f'<text x="98" y="56" style="{S(fill=c["now"], font_family=SANS, font_size=f"{sub_fs - .5}px", font_style="italic")}">E<tspan dy="3" style="font-size:{sub_fs - 3}px">F</tspan></text>']

    def verify():
        g = [f'<path d="M30,46 L30,132 L162,132" style="{S(fill="none", stroke=c["muted"], stroke_width=1)}"/>',
             f'<line x1="30" y1="132" x2="158" y2="50" style="{S(stroke=c["muted"], stroke_width=1, stroke_dasharray="4 4", opacity=.8)}"/>']
        for t_, e in ((.1, .05), (.18, -.04), (.27, .06), (.35, -.02), (.42, .07), (.5, -.05),
                      (.57, .03), (.64, -.06), (.72, .04), (.8, -.03), (.88, .05), (.94, -.02)):
            x, y = 30 + 128 * t_, 132 - 82 * (t_ + e)
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.8" style="{S(fill=c["teal"], opacity=.9)}"/>')
        return g

    drawers = [structure, learn, predict, verify]
    for ((ox, oy), num, title, sub), draw in zip(panels, drawers):
        out.append(f'<g transform="translate({ox},{oy})">')
        out.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" style="{S(fill=c["panel"], stroke=c["border"])}"/>')
        out.append(f'<text x="14" y="{12 + title_fs}" style="{S(font_family=SANS, font_size=f"{title_fs}px", font_weight=600, fill=c["text"])}">'
                   f'<tspan style="{S(fill=c["teal"])}">{num}</tspan>  {escape(title)}</text>')
        if subtitles:
            out.append(f'<text x="14" y="{H - 12}" style="{S(font_family=SANS, font_size=f"{sub_fs}px", fill=c["muted"])}">{escape(sub)}</text>')
        out.extend(draw())
        out.append('</g>')
    arrow = S(fill="none", stroke=c["accent"], stroke_width=1.8)
    for d in ("M202,105 L236,105", "M330,192 L330,236", "M238,325 L204,325", "M110,238 L110,194"):
        out.append(f'<path class="flow" d="{d}" style="{arrow}" marker-end="url(#{mid})"/>')
    out.append(f'<text x="122" y="{219 + sub_fs / 3:.0f}" style="{S(font_family=SANS, font_size=f"{sub_fs}px", font_style="italic", fill=c["muted"])}">correct &amp; retrain</text>')
    return defs, "".join(out)


# ---------------------------------------------------------------- banner
def banner(t, name):
    W, H = 1280, 340
    colors = dict(panel=t["card"], border=t["border"], text=t["text"], muted=t["muted"],
                  accent=t["accent"], teal=t["teal"], now=t["orange"])
    defs, loop = loop_diagram(colors, f"arr{name}", title_fs=24, sub_fs=17, subtitles=False)
    crystal = f'<g transform="translate(918,14) scale(.725)">{loop}</g>'
    chips = ["AI for science", "Graph neural networks", "MLIPs", "DFT"]
    chip_svg, x = [], 64
    for c in chips:
        w = 16 + len(c) * 9.6 + 16
        chip_svg.append(f'<rect x="{x}" y="250" width="{w:.0f}" height="38" rx="19" fill="{t["chip"]}" '
                        f'stroke="{t["border"]}"/>'
                        f'<text x="{x + w/2:.0f}" y="275" font-family="{SANS}" font-size="17" font-weight="600" '
                        f'fill="{t["accent"]}" text-anchor="middle">{escape(c)}</text>')
        x += w + 12
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Shivam Randive: machine learning for materials discovery">
<defs>
<linearGradient id="bg{name}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg2"]}"/><stop offset="1" stop-color="{t["bg3"]}"/></linearGradient>
<radialGradient id="glow{name}" cx="80%" cy="50%" r="45%"><stop offset="0" stop-color="{t["accent"]}" stop-opacity=".16"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>
{dot_pattern(t, "dots" + name)}
{defs}
</defs>
<rect width="{W}" height="{H}" rx="18" fill="url(#bg{name})"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#dots{name})"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#glow{name})"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{t["border"]}"/>
<text x="64" y="78" font-family="{SANS}" font-size="15" font-weight="700" letter-spacing="2.6" fill="{t["teal"]}">MACHINE LEARNING FOR MATERIALS DISCOVERY</text>
<text x="62" y="148" font-family="{SERIF}" font-size="64" font-weight="700" fill="{t["text"]}">Shivam Randive</text>
<text x="64" y="194" font-family="{SANS}" font-size="23" fill="{t["muted"]}">Integrated M.Sc. Physics · SVNIT Surat, India</text>
<text x="64" y="228" font-family="{SANS}" font-size="23" fill="{t["muted"]}">Research intern · Spin Theory Group, NIMS, Japan</text>
{"".join(chip_svg)}
{crystal}
</svg>'''


# ---------------------------------------------------------------- stats strip
def stats(t, name):
    W, H = 1280, 150
    items = [("2", "first-author, submitted"), ("106,235", "structures screened"),
             ("3,625", "DFT transport runs"), ("9,495", "κL values in dataset"),
             ("4", "institutes, 2 countries")]
    cw = W / len(items)
    parts = []
    for i, (v, lbl) in enumerate(items):
        x = cw * i + cw / 2
        parts.append(f'<text x="{x:.0f}" y="70" font-family="{SERIF}" font-size="46" font-weight="700" '
                     f'fill="{t["accent"]}" text-anchor="middle">{escape(v)}</text>'
                     f'<text x="{x:.0f}" y="108" font-family="{SANS}" font-size="19" fill="{t["muted"]}" '
                     f'text-anchor="middle">{escape(lbl)}</text>')
        if i:
            parts.append(f'<line x1="{cw*i:.0f}" y1="34" x2="{cw*i:.0f}" y2="116" stroke="{t["border"]}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="At a glance">
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{t["card"]}" stroke="{t["border"]}"/>
{"".join(parts)}
</svg>'''


# ---------------------------------------------------------------- project card
def card(t, name, tag, tag_color, meta, title, line, nums):
    W, H = 620, 360
    tag_w = 20 + len(tag) * 10.2
    title_lines = wrap(title, 35)[:2]
    line_lines = wrap(line, 56)[:3]
    parts = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{t["card"]}" stroke="{t["border"]}"/>',
             f'<rect x="0" y="0" width="{W}" height="5" rx="2" fill="{t[tag_color]}"/>',
             f'<rect x="28" y="26" width="{tag_w:.0f}" height="30" rx="6" fill="{t[tag_color]}"/>',
             f'<text x="{28 + tag_w/2:.0f}" y="47" font-family="{SANS}" font-size="15" font-weight="700" '
             f'letter-spacing="1.2" fill="{t["bg"]}" text-anchor="middle">{escape(tag)}</text>',
             f'<text x="{40 + tag_w:.0f}" y="47" font-family="{SANS}" font-size="17" fill="{t["muted"]}">{escape(meta)}</text>']
    y = 100
    for tl in title_lines:
        parts.append(f'<text x="28" y="{y}" font-family="{SERIF}" font-size="30" font-weight="700" '
                     f'fill="{t["text"]}">{escape(tl)}</text>')
        y += 37
    y += 6
    for ll in line_lines:
        parts.append(f'<text x="28" y="{y}" font-family="{SANS}" font-size="18.5" font-style="italic" '
                     f'fill="{t["muted"]}">{escape(ll)}</text>')
        y += 25
    bw, gap, by = (W - 56 - 2 * 14) / 3, 14, H - 110
    for i, (v, lbl) in enumerate(nums):
        bx = 28 + i * (bw + gap)
        parts.append(f'<rect x="{bx:.0f}" y="{by}" width="{bw:.0f}" height="86" rx="10" fill="{t["statbg"]}"/>')
        parts.append(f'<text x="{bx + 14:.0f}" y="{by + 35}" font-family="{SERIF}" font-size="27" font-weight="700" '
                     f'fill="{t["accent"]}">{escape(v)}</text>')
        for n, l in enumerate(wrap(lbl, 20)[:2]):
            parts.append(f'<text x="{bx + 14:.0f}" y="{by + 58 + n*18}" font-family="{SANS}" font-size="15.5" '
                         f'fill="{t["muted"]}">{escape(l)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{escape(title)}">{"".join(parts)}</svg>')


CARDS = {
    "nims": ("CURRENT", "orange", "NIMS, Tsukuba · 2026",
             "New alkali- and alkaline-earth Heusler thermoelectrics",
             "Combinatorial Heusler compositions ranked by predicted Seebeck coefficient and lattice thermal "
             "conductivity with transfer-learned universal interatomic potentials.",
             [("2", "pretrained MLIPs: eSEN, EquiformerV3"), ("S, κL", "Seebeck and lattice thermal conductivity"),
              ("New", "alkali and alkaline-earth compositions")]),
    "screening": ("SUBMITTED", "accent", "arXiv:2610.18179 · 2026",
                  "ML-guided thermoelectric screening of 106,235 Heuslers",
                  "The density of states can choose what to calculate; only a band structure shows whether a gap "
                  "exists.",
                  [("≈4×", "fewer DFT runs per confirmed hit"), ("80", "candidates, 61 never measured"),
                   ("3,625", "first-principles transport runs")]),
    "kappa": ("SUBMITTED", "teal", "Code & data on Zenodo · 2026",
              "Making ML predictions of thermal conductivity match experiment",
              "Published calculations overestimate measured lattice thermal conductivity by a median 1.69×; a "
              "two-parameter correction fixes it.",
              [("33%", "median error vs 46–47% baselines"), ("9,495", "κL values for 960 compounds"),
               ("101→37%", "ML force-field error, corrected")]),
    "srfp": ("REPORT", "accent", "SRFP 2025 · S. N. Bose Centre",
             "Do graph neural networks work on unseen materials?",
             "High accuracy on familiar data is not discovery: breadth of training data decides how a model "
             "generalizes.",
             [(">92%", "specialists, familiar data"), ("≈48%", "specialists, unseen perovskites"),
              ("≈80%", "pretrained model, unseen")]),
    "descriptors": ("PROJECT", "teal", "SVNIT · 2025",
                    "Physical descriptors as first predictors",
                    "Classical machine learning on ionic radii and electronegativity for perovskites and "
                    "half-Heusler alloys.",
                    [("≈90%", "perovskite formability accuracy (SVM)"), ("137", "half-Heuslers, GPR lattice constants"),
                     ("4", "physical descriptors")]),
    "strain": ("INTERNSHIP", "orange", "IIT Bhilai · 2024",
               "Strain in silicon thin films for stretchable electronics",
               "A COMSOL finite-element model whose strain maps fed a collaborator's DFT study of strain-tuned "
               "electronic properties.",
               [("FEM", "COMSOL Multiphysics"), ("Si / PI", "film on flexible polyimide"),
                ("→ DFT", "strain maps as input")]),
}


# ---------------------------------------------------------------- journey
def journey(t, name):
    W, H = 1280, 230
    stops = [("2024", "IIT Bhilai", "Summer research intern", "muted"),
             ("2025 –", "SVNIT Surat", "Student researcher", "accent"),
             ("2025", "S. N. Bose Centre", "SRFP fellow, Kolkata", "accent"),
             ("2026", "NIMS, Japan", "Research intern, Spin Theory Group", "orange"),
             ("2027", "IIT Delhi", "Semester exchange (upcoming)", "faint")]
    x0, x1, ly = 130, 1150, 80
    parts = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{t["card"]}" stroke="{t["border"]}"/>',
             f'<line x1="{x0}" y1="{ly}" x2="{x1}" y2="{ly}" stroke="{t["border"]}" stroke-width="3"/>']
    for i, (yr, place, role, col) in enumerate(stops):
        x = x0 + (x1 - x0) * i / (len(stops) - 1)
        now = col == "orange"
        nxt = col == "faint"
        if now:
            parts.append(f'<circle cx="{x:.0f}" cy="{ly}" r="15" fill="{t["orange"]}" opacity=".18"/>')
        dash = ' stroke-dasharray="3 3"' if nxt else ""
        fill = t["orange"] if now else t["card"]
        parts.append(f'<circle cx="{x:.0f}" cy="{ly}" r="8" fill="{fill}" stroke="{t[col]}" stroke-width="3"{dash}/>')
        parts.append(f'<text x="{x:.0f}" y="44" font-family="{SANS}" font-size="18" font-weight="700" '
                     f'fill="{t["orange"] if now else t["muted"]}" text-anchor="middle">{escape(yr)}</text>')
        parts.append(f'<text x="{x:.0f}" y="128" font-family="{SERIF}" font-size="25" font-weight="700" '
                     f'fill="{t["text"]}" text-anchor="middle">{escape(place)}</text>')
        for n, l in enumerate(wrap(role, 20)):
            parts.append(f'<text x="{x:.0f}" y="{158 + n*22}" font-family="{SANS}" font-size="18" '
                         f'fill="{t["muted"]}" text-anchor="middle">{escape(l)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Research journey">{"".join(parts)}</svg>')


def main():
    for name, t in THEMES.items():
        (OUT / f"banner-{name}.svg").write_text(banner(t, name), encoding="utf-8")
        (OUT / f"stats-{name}.svg").write_text(stats(t, name), encoding="utf-8")
        (OUT / f"journey-{name}.svg").write_text(journey(t, name), encoding="utf-8")
        for key, spec in CARDS.items():
            (OUT / f"card-{key}-{name}.svg").write_text(card(t, name, *spec), encoding="utf-8")
    print("wrote", len(list(OUT.glob("*.svg"))), "SVG files to", OUT)


if __name__ == "__main__":
    main()
