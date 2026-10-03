#!/usr/bin/env python3
"""Generate the AlfLayla icon theme (Alf Layla) next to this file.

scalable/  64-unit SVGs. Folders are lanterns: an aubergine body in a copper
           frame with one lit cut-out on the front (an eight-point star, or a
           mark for the special folders), glowing in lamp amber. Documents are
           parchment sheets in a copper frame with one ink mark for their type
           (rose only on PDF, faience on images and code). Devices are framed
           aubergine boxes with a lamp light; the trash is a copper jar.
16/        sidebar size: plain line icons in Muted.
Anything not drawn here falls through to Adwaita.
Run: python3 build.py   (then gtk-update-icon-cache runs by itself)
"""

import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "AlfLayla"

GROUND, BODY, FRONT, LINE = "#110E24", "#231C42", "#2D2452", "#3A2F5C"
COPPER, COPPER_LIT, LAMP = "#C57B57", "#E0A06C", "#F3B95F"
PARCH, PARCH_FOLD, INK = "#EFE4D0", "#D6C7A8", "#2D2452"
TURQ, TURQ_INK, ROSE = "#6FC2B6", "#2E8C80", "#B5566B"
SIDE = "#9E94BA"

GLOW = ('<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="2.4"/></filter>')


def star_pts(cx, cy, R, ratio=0.62, n=8):
    pts = []
    for k in range(2 * n):
        a = math.radians(k * 180 / n - 90)
        rad = R if k % 2 == 0 else R * ratio
        pts.append(f"{cx + rad * math.cos(a):.2f},{cy + rad * math.sin(a):.2f}")
    return " ".join(pts)


def svg64(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
            f'<defs>{GLOW}</defs>{body}</svg>\n')


def lit(shape):
    """A cut-out with the lamp behind it: the shape blurred, then the shape."""
    return f'<g filter="url(#glow)" opacity="0.8">{shape}</g>{shape}'


def write(rel, content, names):
    for name in names:
        path = ROOT / rel / f"{name}.svg"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


# ---- folders: lanterns -------------------------------------------------------------
def stroke(d, w=2.6):
    return f'<path d="{d}" fill="none" stroke="{LAMP}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


MARKS = {
    None: f'<polygon points="{star_pts(32, 40, 9)}" fill="{LAMP}"/>',
    "home": f'<path d="M25 50 V40 C25 35 30 33 32 29 C34 33 39 35 39 40 V50 Z" fill="{LAMP}"/>',
    "documents": "".join(f'<rect x="23" y="{y}" width="{w}" height="2.6" rx="1" fill="{LAMP}"/>' for y, w in ((33, 18), (39, 18), (45, 12))),
    "downloads": stroke("M32 31 V44 M26.5 39.5 L32 45 L37.5 39.5 M25 49.5 H39"),
    "music": stroke("M28 47 V33 L39 31 V45") + f'<circle cx="25.5" cy="47" r="3" fill="{LAMP}"/><circle cx="36.5" cy="45" r="3" fill="{LAMP}"/>',
    "pictures": f'<path d="M22 49 L29 38 L33.5 44 L37 40 L43 49 Z" fill="{LAMP}"/><circle cx="38.5" cy="33.5" r="2.6" fill="{LAMP}"/>',
    "videos": f'<path d="M27 32 L41 40 L27 48 Z" fill="{LAMP}"/>',
    "desktop": stroke("M23 33 H41 V45 H23 Z M28 49.5 H36", 2.2),
    "templates": f'<rect x="24" y="32" width="16" height="16" fill="none" stroke="{LAMP}" stroke-width="2.2" stroke-dasharray="3.2 2.6"/>',
    "share": stroke("M27 40 L37 34 M27 40 L37 47", 1.8) + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{LAMP}"/>' for x, y in ((26, 40), (38, 33.5), (38, 47.5))),
    "remote": stroke("M32 31.5 a9 9 0 1 0 0.01 0 M23 40.5 H41 M32 31.5 C27 36 27 45 32 49.5 M32 31.5 C37 36 37 45 32 49.5", 1.7),
}


def folder(kind=None):
    body = (f'<path d="M6 13 H24 L29 19 H58 V54 H6 Z" fill="{BODY}" stroke="{COPPER}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<rect x="4.75" y="24.75" width="54.5" height="31.5" rx="2" fill="{FRONT}" stroke="{COPPER}" stroke-width="1.5"/>'
            f'<rect x="8.5" y="28.5" width="47" height="24" fill="none" stroke="{COPPER}" stroke-opacity="0.5" stroke-width="1"/>'
            + lit(MARKS[kind]))
    return svg64(body)


FOLDERS = {
    None: ["folder", "inode-directory", "folder-open", "folder-drag-accept", "folder-visiting"],
    "home": ["user-home", "folder-home"],
    "documents": ["folder-documents"],
    "downloads": ["folder-download"],
    "music": ["folder-music"],
    "pictures": ["folder-pictures"],
    "videos": ["folder-videos"],
    "templates": ["folder-templates"],
    "share": ["folder-publicshare"],
    "desktop": ["user-desktop"],
    "remote": ["folder-remote", "network-workgroup"],
}
for kind, names in FOLDERS.items():
    write("scalable/places", folder(kind), names)
    if kind is None:
        write("scalable/mimetypes", folder(kind), names)


# ---- documents: parchment in a frame ---------------------------------------------------
def sheet():
    return (f'<path d="M13 4.75 H41 L52.25 16 V59.25 H13 Z" fill="{PARCH}" stroke="{COPPER}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M41 4.75 V16 H52.25 Z" fill="{PARCH_FOLD}" stroke="{COPPER}" stroke-width="1.2" stroke-linejoin="round"/>'
            f'<path d="M17 20.5 H48.5 V55.5 H17 Z" fill="none" stroke="{COPPER}" stroke-opacity="0.55" stroke-width="1"/>')


def lines(ys, color=INK, x0=21, x1=44.5, op=0.75):
    return "".join(f'<rect x="{x0}" y="{y}" width="{(x1 - x0) - (8 if i == len(ys) - 1 else 0)}" height="2" rx="1" '
                   f'fill="{color}" opacity="{op}"/>' for i, y in enumerate(ys))


def ink(d, color=INK, w=2.4):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


DOC_MARKS = {
    None: "",
    "text": lines([25, 31, 37, 43, 49]),
    "script": ink("M22 27 L28 32 L22 37", TURQ_INK) + ink("M31 38 H42", TURQ_INK) + lines([45, 50], INK, 21, 44, 0.45),
    "code": ink("M28 27 L21.5 35 L28 43", TURQ_INK) + ink("M37 27 L43.5 35 L37 43", TURQ_INK) + lines([50], INK, 21, 44, 0.45),
    "exec": f'<polygon points="{star_pts(32.7, 36, 9.5)}" fill="{INK}"/>' + lines([50], INK, 21, 44, 0.45),
    "image": f'<rect x="21" y="25" width="23.5" height="22" fill="{TURQ}"/><path d="M21 47 L29 35 L34 42 L38 37.5 L44.5 47 Z" fill="{TURQ_INK}"/>'
             f'<circle cx="38.5" cy="30.5" r="2.6" fill="{LAMP}"/>',
    "pdf": lines([25, 31, 37]) + f'<rect x="17.5" y="43" width="30.5" height="9" fill="{ROSE}"/>',
    "audio": ink("M21 38 C24 26 27 50 31 38 C35 26 38 50 44.5 36"),
    "video": f'<path d="M26 27 L42 37 L26 47 Z" fill="{INK}"/>',
    "archive": f'<rect x="29" y="5.5" width="7.5" height="53" fill="{COPPER}"/>'
               f'<rect x="26.5" y="30" width="12.5" height="9" rx="1" fill="{PARCH}" stroke="{INK}" stroke-width="1.8"/>',
    "grid": ink("M21 27 H44.5 M21 35 H44.5 M21 43 H44.5 M29 23.5 V49 M37 23.5 V49", INK, 1.6),
    "slide": f'<rect x="21" y="25" width="23.5" height="15" fill="{COPPER}"/>' + ink("M32.7 40 V49 M27 50 H38.5", INK, 2),
    "font": ink("M23 50 L32.7 25 L42.5 50 M26.5 41.5 H39"),
}
DOCUMENTS = {
    None: ["application-x-generic", "unknown", "empty"],
    "text": ["text-x-generic", "text-plain", "x-office-document", "text-markdown", "text-x-readme"],
    "script": ["text-x-script", "application-x-shellscript", "text-x-python", "text-x-makefile"],
    "exec": ["application-x-executable", "application-x-sharedlib"],
    "image": ["image-x-generic"],
    "audio": ["audio-x-generic"],
    "video": ["video-x-generic"],
    "archive": ["package-x-generic", "application-x-archive", "application-zip", "application-x-compressed-tar", "application-x-tar"],
    "pdf": ["application-pdf"],
    "code": ["text-html", "application-json", "text-x-csrc", "text-x-c++src", "text-x-javascript"],
    "grid": ["x-office-spreadsheet"],
    "slide": ["x-office-presentation"],
    "font": ["font-x-generic"],
}
for kind, names in DOCUMENTS.items():
    write("scalable/mimetypes", svg64(sheet() + DOC_MARKS[kind]), names)


# ---- devices and trash -----------------------------------------------------------------
def framed(x, y, w, h, rx=3):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{BODY}" stroke="{COPPER}" stroke-width="1.5"/>'
            f'<rect x="{x + 3.5}" y="{y + 3.5}" width="{w - 7}" height="{h - 7}" fill="none" stroke="{COPPER}" stroke-opacity="0.5" stroke-width="1"/>')


def led(cx, cy, r=2.6):
    return lit(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{LAMP}"/>')


DRIVE = framed(8.75, 21.75, 46.5, 22.5) + f'<rect x="16" y="32" width="20" height="2" rx="1" fill="{COPPER_LIT}" opacity="0.7"/>' + led(46, 33)
write("scalable/devices", svg64(DRIVE), ["drive-harddisk", "drive-harddisk-system", "drive-multidisk"])
REMOVABLE = (f'<rect x="24.75" y="8.75" width="14.5" height="12" fill="{LINE}" stroke="{COPPER}" stroke-width="1.5"/>'
             + framed(18.75, 20.75, 26.5, 35.5) + led(32, 40))
write("scalable/devices", svg64(REMOVABLE), ["drive-removable-media", "drive-harddisk-usb", "media-removable", "media-flash"])
OPTICAL = (f'<circle cx="32" cy="32" r="21.25" fill="{BODY}" stroke="{COPPER}" stroke-width="1.5"/>'
           f'<circle cx="32" cy="32" r="17" fill="none" stroke="{COPPER}" stroke-opacity="0.5" stroke-width="1"/>'
           + lit(f'<polygon points="{star_pts(32, 32, 6)}" fill="{LAMP}"/>') + f'<circle cx="32" cy="32" r="1.6" fill="{GROUND}"/>')
write("scalable/devices", svg64(OPTICAL), ["drive-optical", "media-optical"])
COMPUTER = framed(9.75, 10.75, 44.5, 31.5) + ink("M32 42.5 V53 M23 54 H41", COPPER, 2) + led(32, 26.5, 3)
write("scalable/devices", svg64(COMPUTER), ["computer", "video-display"])

JAR = "M25 8 H39 M27 8 V16 C15 23 12 34 14 46 C16 56 24 60 32 60 C40 60 48 56 50 46 C52 34 49 23 37 16 V8"
JAR_FILL = "M27 16 C15 23 12 34 14 46 C16 56 24 60 32 60 C40 60 48 56 50 46 C52 34 49 23 37 16 Z"
BANDS = ink("M16 33 H48 M14.5 45 H49.5", COPPER, 1)
write("scalable/places", svg64(f'<path d="{JAR_FILL}" fill="{BODY}"/>' + ink(JAR, COPPER_LIT, 1.8) + BANDS), ["user-trash"])
write("scalable/places",
      svg64(f'<path d="M28 3 H38 L37 17 H27 Z" fill="{PARCH}" stroke="{COPPER}" stroke-width="1"/>'
            f'<path d="{JAR_FILL}" fill="{BODY}"/>' + ink(JAR, COPPER_LIT, 1.8) + BANDS
            + lit(f'<polygon points="{star_pts(32, 39, 4.5)}" fill="{LAMP}"/>')),
      ["user-trash-full"])


# ---- 16px sidebar: plain line icons ------------------------------------------------------
SYM = {
    "home": '<path d="M2 8 L8 2.5 L14 8"/><path d="M4 7 V14 H12 V7"/>',
    "desktop": '<rect x="2" y="3" width="12" height="8"/><path d="M6 14 H10"/>',
    "documents": '<path d="M4 2 H10 L13 5 V14 H4 Z"/><path d="M6.5 8 H10.5 M6.5 11 H9.5"/>',
    "downloads": '<path d="M8 2 V11"/><path d="M4 7.5 L8 11.5 L12 7.5"/><path d="M3 14 H13"/>',
    "music": '<path d="M5.5 12.5 V3.5 L12.5 2.5 V11.5"/><circle cx="4" cy="12.5" r="1.6"/><circle cx="11" cy="11.5" r="1.6"/>',
    "pictures": '<path d="M2 13 L6 7 L9 10.5 L11 8.5 L14 13 Z"/><circle cx="11.5" cy="4.5" r="1.2"/>',
    "videos": '<path d="M5 3 V13 L13 8 Z"/>',
    "templates": '<rect x="2.5" y="2.5" width="11" height="11" stroke-dasharray="2.2 2"/>',
    "share": '<circle cx="4" cy="8" r="1.6"/><circle cx="12" cy="3.8" r="1.6"/><circle cx="12" cy="12.2" r="1.6"/><path d="M5.4 7.2 L10.6 4.6 M5.4 8.8 L10.6 11.4"/>',
    "folder": '<path d="M2 4 H6.5 L8 5.5 H14 V13 H2 Z"/>',
    "recent": '<circle cx="8" cy="8" r="6"/><path d="M8 4.5 V8 L10.5 9.5"/>',
    "trash": '<path d="M6 2 H10 M6.7 2 V4 C3 6 2.6 9 3.2 11.5 C3.8 13.5 6 14.5 8 14.5 C10 14.5 12.2 13.5 12.8 11.5 C13.4 9 13 6 9.3 4 V2"/>',
    "bookmark": '<path d="M4 2 H12 V14 L8 10.5 L4 14 Z"/>',
    "drive": '<rect x="2" y="5" width="12" height="6"/><path d="M10.5 8 H11.5"/>',
    "removable": '<rect x="4.5" y="5" width="7" height="9"/><path d="M6 5 V2 H10 V5"/>',
    "optical": '<circle cx="8" cy="8" r="6"/><circle cx="8" cy="8" r="1.5"/>',
    "computer": '<rect x="2" y="2.5" width="12" height="8"/><path d="M5 14 H11 M8 10.5 V14"/>',
    "network": '<circle cx="8" cy="8" r="6"/><path d="M2 8 H14 M8 2 C5 5 5 11 8 14 M8 2 C11 5 11 11 8 14"/>',
}


def sym16(key):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none" '
            f'stroke="{SIDE}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{SYM[key]}</svg>\n')


SIDEBAR = {
    "places": {
        "home": ["user-home", "folder-home", "go-home"], "desktop": ["user-desktop"], "documents": ["folder-documents"],
        "downloads": ["folder-download"], "music": ["folder-music"], "pictures": ["folder-pictures"],
        "videos": ["folder-videos"], "templates": ["folder-templates"], "share": ["folder-publicshare"],
        "folder": ["folder", "inode-directory", "folder-open", "folder-drag-accept", "folder-visiting"],
        "recent": ["document-open-recent", "folder-recent"], "trash": ["user-trash", "user-trash-full"],
        "bookmark": ["user-bookmarks", "bookmark-new"], "network": ["folder-remote", "network-workgroup", "network-server"],
    },
    "devices": {
        "drive": ["drive-harddisk", "drive-harddisk-system", "drive-multidisk"],
        "removable": ["drive-removable-media", "drive-harddisk-usb", "media-removable", "media-flash"],
        "optical": ["drive-optical", "media-optical"], "computer": ["computer", "video-display"],
    },
}
for ctx, groups in SIDEBAR.items():
    for key, names in groups.items():
        write(f"16/{ctx}", sym16(key), names)

(ROOT / "index.theme").write_text(f"""[Icon Theme]
Name={NAME}
Comment=Alf Layla: lantern folders with a lit cut-out, framed parchment documents, plain 16px line icons
Inherits=Adwaita,hicolor
Example=folder

Directories=16/places,16/devices,scalable/places,scalable/mimetypes,scalable/devices

[16/places]
Size=16
Context=Places
Type=Fixed

[16/devices]
Size=16
Context=Devices
Type=Fixed

[scalable/places]
Size=64
MinSize=20
MaxSize=512
Context=Places
Type=Scalable

[scalable/mimetypes]
Size=64
MinSize=16
MaxSize=512
Context=MimeTypes
Type=Scalable

[scalable/devices]
Size=64
MinSize=20
MaxSize=512
Context=Devices
Type=Scalable
""")
subprocess.run(["gtk-update-icon-cache", "-f", "-t", str(ROOT)], check=False,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"{NAME} icons written to {ROOT}")
