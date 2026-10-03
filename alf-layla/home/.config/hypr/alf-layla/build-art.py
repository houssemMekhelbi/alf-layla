#!/usr/bin/env python3
"""Generate the Alf Layla art: everything that is an image rather than CSS.

  ~/.config/hypr/alf-layla/wallpaper.svg, wallpaper.png   1920x1080: a lattice window
        with the lamp behind it, three nested copper frames around it, a crescent
        and a few stars in an aubergine night
  ~/.config/waybar/alf-layla/cap-start.png, cap-end.png    6x34 ends of a bar frame
        (outer copper line with 3px corners, inner line 4px in)
  ~/.config/waybar/alf-layla/pendant.png                   64x19 point that hangs under
        the clock, with the lamp dot
  ~/.config/waybar/alf-layla/ws-*.png                      20x20 workspace stars
  ~/.config/gtk-3.0/alf-layla/crumb-star.png               Thunar path separator

Deterministic; edit and re-run (needs rsvg-convert):  python3 build-art.py
"""

import math
import random
import subprocess
from pathlib import Path

CONF = Path.home() / ".config"
HYPR = CONF / "hypr/alf-layla"
BAR = CONF / "waybar/alf-layla"
GTK = CONF / "gtk-3.0/alf-layla"

GROUND, RAISED2, LINE, MUTED = "#110E24", "#231C42", "#3A2F5C", "#9E94BA"
COPPER, COPPER_LIT, LAMP = "#C57B57", "#E0A06C", "#F3B95F"
ROSE, ROSE_DEEP, TURQ = "#E08497", "#B5566B", "#6FC2B6"
LATTICE = "#0B0818"
BAR_BG = "rgba(17,14,36,0.90)"


def star_pts(cx, cy, R, ratio=0.62, n=8, rot=0.0):
    pts = []
    for k in range(2 * n):
        a = math.radians(rot + k * 180 / n - 90)
        rad = R if k % 2 == 0 else R * ratio
        pts.append(f"{cx + rad * math.cos(a):.2f},{cy + rad * math.sin(a):.2f}")
    return " ".join(pts)


def render(svg, out, w=None, h=None):
    src = out.with_suffix(".svg")
    src.write_text(svg)
    cmd = ["rsvg-convert", "-o", str(out)]
    if w:
        cmd += ["-w", str(w), "-h", str(h)]
    subprocess.run(cmd + [str(src)], check=True)
    if out.name != "wallpaper.png":
        src.unlink()


# ---- wallpaper -------------------------------------------------------------------
def wallpaper():
    W, H = 1920, 1080
    R = 34
    T = 2 * R
    ax, ay, aw, ah = 1120, 236, 440, 720          # the window: left, apex, width, height
    cx = ax + aw / 2
    spring = ay + 250
    lamp_y = ay + 330

    def arch(inset):
        l, r, top, bot = ax + inset, ax + aw - inset, ay + inset * 1.35, ay + ah - inset
        return (f"M{l},{bot} L{l},{spring} C{l},{spring - 150} {cx - 60},{top + 70} {cx},{top} "
                f"C{cx + 60},{top + 70} {r},{spring - 150} {r},{spring} L{r},{bot} Z")

    # the khatam lattice: eight-pointed stars that touch at their tips
    r_in = math.cos(math.radians(45)) / math.cos(math.radians(22.5))
    knot = lambda x, y: f'<rect x="{x - 5}" y="{y - 5}" width="10" height="10" fill="{LATTICE}" transform="rotate(45 {x} {y})"/>'
    random.seed(11)
    stars = []
    for _ in range(70):
        x, y = random.uniform(40, 1040), random.uniform(70, 560)
        if math.hypot(x - 868, y - 186) < 60:   # keep the crescent's dark side clear
            continue
        stars.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([1.0, 1.2, 1.6, 2.2])}" '
                     f'fill="#F6DDA8" opacity="{random.uniform(0.18, 0.55):.2f}"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<filter id="haze" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.0022 0.006" numOctaves="3" seed="7"/><feColorMatrix values="0 0 0 0 0.62  0 0 0 0 0.52  0 0 0 0 0.75  0 0 0 0.9 -0.32"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 0.9  0 0 0 0 0.8  0 0 0 0.10 0"/></filter>
<radialGradient id="lamp" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{lamp_y}" r="520">
<stop offset="0" stop-color="#FFE3A3"/><stop offset="0.10" stop-color="#F6C56C"/><stop offset="0.32" stop-color="#D98B3D"/><stop offset="0.60" stop-color="#7A3B3A"/><stop offset="1" stop-color="#1B1433"/></radialGradient>
<radialGradient id="spill" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{lamp_y + 60}" r="900">
<stop offset="0" stop-color="{LAMP}" stop-opacity="0.30"/><stop offset="0.45" stop-color="#C5703F" stop-opacity="0.10"/><stop offset="1" stop-color="#C5703F" stop-opacity="0"/></radialGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0F0C20"/><stop offset="1" stop-color="#171230"/></linearGradient>
<pattern id="lat" width="{T}" height="{T}" patternUnits="userSpaceOnUse" x="{cx - R}" y="{lamp_y - R}">
<polygon points="{star_pts(R, R, R, r_in, rot=90)}" fill="none" stroke="{LATTICE}" stroke-width="7" stroke-linejoin="miter"/>
<circle cx="{R}" cy="{R}" r="7" fill="{LATTICE}"/>
{knot(0, 0)}{knot(T, 0)}{knot(0, T)}{knot(T, T)}
</pattern>
<mask id="crescent"><rect width="{W}" height="{H}" fill="#fff"/><circle cx="877" cy="181" r="38.5" fill="#000"/></mask>
<clipPath id="win"><path d="{arch(0)}"/></clipPath>
</defs>
<rect width="{W}" height="{H}" fill="url(#night)"/>
<rect width="{W}" height="{H}" filter="url(#haze)" opacity="0.22"/>
<rect width="{W}" height="{H}" fill="url(#spill)"/>
<path d="{arch(-54)}" fill="none" stroke="{COPPER}" stroke-opacity="0.22" stroke-width="1.5"/>
<path d="{arch(-36)}" fill="none" stroke="{COPPER}" stroke-opacity="0.40" stroke-width="1.5"/>
<path d="{arch(-18)}" fill="{LATTICE}" stroke="{COPPER}" stroke-opacity="0.75" stroke-width="2"/>
<g clip-path="url(#win)">
<rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" fill="url(#lamp)"/>
<rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" fill="url(#lat)"/>
</g>
<path d="{arch(0)}" fill="none" stroke="{LATTICE}" stroke-width="10"/>
<path d="{arch(0)}" fill="none" stroke="{COPPER_LIT}" stroke-opacity="0.55" stroke-width="1.5"/>
<rect x="0" y="{ay + ah + 54}" width="{W}" height="1.5" fill="{COPPER}" opacity="0.28"/>
{"".join(stars)}
<circle cx="860" cy="190" r="40" fill="#F6DDA8" opacity="0.85" mask="url(#crescent)"/>
<rect width="{W}" height="{H}" filter="url(#grain)"/>
</svg>
'''
    render(svg, HYPR / "wallpaper.png", W, H)


# ---- bar frames ------------------------------------------------------------------
def caps():
    for name, flip in (("cap-start", False), ("cap-end", True)):
        tr = ' transform="translate(6 0) scale(-1 1)"' if flip else ""
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="6" height="34" viewBox="0 0 6 34"><g{tr}>
<rect x="0.5" y="0.5" width="40" height="33" rx="3" fill="{BAR_BG}" stroke="{COPPER}" stroke-width="1"/>
<rect x="4.5" y="4.5" width="40" height="25" fill="none" stroke="{COPPER}" stroke-opacity="0.55" stroke-width="1"/>
</g></svg>'''
        render(svg, BAR / f"{name}.png")


def pendant():
    # Sits at y=29 of the centre frame: covers the two bottom lines and hangs 14px below.
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="19" viewBox="0 0 64 19">
<defs><filter id="g" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1.6"/></filter></defs>
<polygon points="0,0 64,0 64,4.5 32,18 0,4.5" fill="{GROUND}"/>
<polyline points="0,4.5 32,18 64,4.5" fill="none" stroke="{COPPER}" stroke-width="1"/>
<polyline points="1.5,0.5 32,13.4 62.5,0.5" fill="none" stroke="{COPPER}" stroke-opacity="0.55" stroke-width="1"/>
<circle cx="32" cy="8.2" r="3" fill="{LAMP}" opacity="0.7" filter="url(#g)"/>
<circle cx="32" cy="8.2" r="2" fill="{LAMP}"/>
</svg>'''
    render(svg, BAR / "pendant.png")


def workspace_stars():
    glow = ('<defs><filter id="g" x="-100%" y="-100%" width="300%" height="300%">'
            '<feGaussianBlur stdDeviation="2.2"/></filter></defs>')
    shapes = {
        "empty": f'<polygon points="{star_pts(10, 10, 6)}" fill="none" stroke="{MUTED}" stroke-opacity="0.8" stroke-width="1.2"/>',
        "occupied": f'<polygon points="{star_pts(10, 10, 6.5)}" fill="{COPPER}"/>',
        "active": f'<polygon points="{star_pts(10, 10, 6.5)}" fill="{LAMP}" opacity="0.55"/>',
        "focused": f'{glow}<polygon points="{star_pts(10, 10, 7.5)}" fill="{LAMP}" opacity="0.75" filter="url(#g)"/>'
                   f'<polygon points="{star_pts(10, 10, 7.5)}" fill="{LAMP}"/>',
        "urgent": f'<polygon points="{star_pts(10, 10, 6.5)}" fill="{ROSE_DEEP}" stroke="{ROSE}" stroke-width="1"/>',
    }
    for name, body in shapes.items():
        render(f'<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">{body}</svg>',
               BAR / f"ws-{name}.png")


def crumb():
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="18" viewBox="0 0 10 18">'
           f'<polygon points="{star_pts(5, 9, 3.6)}" fill="none" stroke="{COPPER}" stroke-width="1"/></svg>')
    render(svg, GTK / "crumb-star.png")


if __name__ == "__main__":
    for d in (HYPR, BAR, GTK):
        d.mkdir(parents=True, exist_ok=True)
    wallpaper()
    caps()
    pendant()
    workspace_stars()
    crumb()
    print("Alf Layla art written")
