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
        orange="#bc4c00", chip="#ffffff", dots="#0b4f8a", bond="#aab4be", cell="#8c959f",
        statbg="#eef3f8",
    ),
    "dark": dict(
        bg="#0d1117", bg2="#0f1a2b", bg3="#142540", card="#161b22", border="#30363d",
        text="#e6edf3", muted="#9198a1", faint="#6e7681", accent="#79c0ff", teal="#56d4c3",
        orange="#f0883e", chip="#0d1117", dots="#79c0ff", bond="#4a5563", cell="#6e7681",
        statbg="#1c2533",
    ),
}

# Jmol element colours
ELEMENTS = {"Zr": ((148, 224, 224), 0.085), "Ni": ((80, 208, 80), 0.072), "Sn": ((102, 128, 128), 0.08)}


def shade(rgb, f):
    r, g, b = rgb
    if f >= 0:
        return "#%02x%02x%02x" % tuple(int(c + (255 - c) * f) for c in (r, g, b))
    return "#%02x%02x%02x" % tuple(int(c * (1 + f)) for c in (r, g, b))


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


# ---------------------------------------------------------------- crystal
def zrnisn_svg(t, cx, cy, size, yaw=0.62, pitch=-0.42, gid="g"):
    """Ball-and-stick conventional cell of half-Heusler ZrNiSn, projected and depth-sorted."""
    fcc = [(0, 0, 0), (0, .5, .5), (.5, 0, .5), (.5, .5, 0)]
    sites = [("Zr", (0, 0, 0)), ("Sn", (.5, .5, .5)), ("Ni", (.25, .25, .25))]
    atoms, seen = [], set()
    for el, off in sites:
        for f in fcc:
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    for k in (-1, 0, 1):
                        p = (f[0] + off[0] + i, f[1] + off[1] + j, f[2] + off[2] + k)
                        if all(-1e-6 < v < 1 + 1e-6 for v in p):
                            key = tuple(round(v, 3) for v in p)
                            if key not in seen:
                                seen.add(key)
                                atoms.append((el, p))
    nn = math.sqrt(3) / 4
    bonds = [(a, b) for a, (ea, pa) in enumerate(atoms) if ea == "Ni"
             for b, (eb, pb) in enumerate(atoms) if eb != "Ni" and abs(math.dist(pa, pb) - nn) < 1e-3]
    corners = [(i & 1, (i >> 1) & 1, (i >> 2) & 1) for i in range(8)]
    edges = [(a, b) for a in range(8) for b in range(a + 1, 8)
             if sum(abs(corners[a][n] - corners[b][n]) for n in range(3)) == 1]

    def proj(p):
        x, y, z = p[0] - .5, p[1] - .5, p[2] - .5
        cyw, syw, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
        x1, z1 = x * cyw + z * syw, -x * syw + z * cyw
        y1, z2 = y * cp - z1 * sp, y * sp + z1 * cp
        k = 3.2 / (3.2 + z2)
        return cx + x1 * k * size, cy - y1 * k * size, z2, k

    P = [proj(p) for _, p in atoms]
    C = [proj(c) for c in corners]
    out = []
    defs = []
    for el, (rgb, _) in ELEMENTS.items():
        defs.append(f'<radialGradient id="{gid}{el}" cx="38%" cy="34%" r="70%">'
                    f'<stop offset="0" stop-color="{shade(rgb, .78)}"/>'
                    f'<stop offset=".45" stop-color="{shade(rgb, .05)}"/>'
                    f'<stop offset="1" stop-color="{shade(rgb, -.5)}"/></radialGradient>')
    for a, b in edges:
        far = (C[a][2] + C[b][2]) / 2 > 0
        dash = ' stroke-dasharray="4 5"' if far else ""
        out.append((99, f'<line x1="{C[a][0]:.1f}" y1="{C[a][1]:.1f}" x2="{C[b][0]:.1f}" y2="{C[b][1]:.1f}" '
                        f'stroke="{t["cell"]}" stroke-width="1.2" opacity=".75"{dash}/>'))
    items = []
    for a, b in bonds:
        z = (P[a][2] + P[b][2]) / 2 + 0.02
        w = 5.2 * size / 300 * (P[a][3] + P[b][3]) / 2
        items.append((z, f'<line x1="{P[a][0]:.1f}" y1="{P[a][1]:.1f}" x2="{P[b][0]:.1f}" y2="{P[b][1]:.1f}" '
                         f'stroke="{t["bond"]}" stroke-width="{w:.2f}" stroke-linecap="round"/>'))
    for n, (el, _) in enumerate(atoms):
        x, y, z, k = P[n]
        r = ELEMENTS[el][1] * size * k * 1.15
        items.append((z, f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#{gid}{el})"/>'))
    items.sort(key=lambda it: -it[0])
    body = "".join(s for _, s in out) + "".join(s for _, s in items)
    return "".join(defs), body


# ---------------------------------------------------------------- banner
def banner(t, name):
    W, H = 1280, 340
    defs, crystal = zrnisn_svg(t, 1060, 150, 150, gid=f"b{name}")
    chips = ["Heusler thermoelectrics", "Graph neural networks", "MLIPs", "DFT"]
    chip_svg, x = [], 64
    for c in chips:
        w = 16 + len(c) * 9.6 + 16
        chip_svg.append(f'<rect x="{x}" y="250" width="{w:.0f}" height="38" rx="19" fill="{t["chip"]}" '
                        f'stroke="{t["border"]}"/>'
                        f'<text x="{x + w/2:.0f}" y="275" font-family="{SANS}" font-size="17" font-weight="600" '
                        f'fill="{t["accent"]}" text-anchor="middle">{escape(c)}</text>')
        x += w + 12
    legend = []
    lx = 940
    for el, (rgb, _) in ELEMENTS.items():
        legend.append(f'<circle cx="{lx}" cy="314" r="6" fill="{shade(rgb, 0)}"/>'
                      f'<text x="{lx + 11}" y="319" font-family="{SANS}" font-size="13" fill="{t["muted"]}">{el}</text>')
        lx += 52
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
{"".join(legend)}
<text x="1220" y="319" font-family="{SANS}" font-size="13" fill="{t["faint"]}" text-anchor="end">ZrNiSn, half-Heusler</text>
</svg>'''


# ---------------------------------------------------------------- stats strip
def stats(t, name):
    W, H = 1280, 150
    items = [("2", "first-author manuscripts"), ("106,235", "structures screened"),
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
    "screening": ("PREPRINT", "accent", "arXiv:2610.18179 · 2026",
                  "ML-guided thermoelectric screening of 106,235 Heuslers",
                  "The density of states can choose what to calculate; only a band structure shows whether a gap "
                  "exists.",
                  [("≈4×", "fewer DFT runs per confirmed hit"), ("80", "candidates, 61 never measured"),
                   ("3,625", "first-principles transport runs")]),
    "kappa": ("MANUSCRIPT", "teal", "Computational Materials Science · 2026",
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
    stops = [("2024", "IIT Bhilai", "Summer research intern", "cell"),
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
