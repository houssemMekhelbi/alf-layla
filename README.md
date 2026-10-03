<p align="center"><img src=".github/banner.png" alt="Alf Layla: copper frames that nest" width="100%"></p>

<p align="center"><sub>كان يا ما كان في قديم الزمان<br>
once upon a time, in an age long past</sub></p>

# ✴ Alf Layla

*Alf Layla* (ألف ليلة, the Thousand and One Nights) is a story inside a story. Here copper frames nest, and the deeper the frame, the more it matters: windows are one frame deep, the bar, the popups and the lock field two, the adhan banner and a critical notification three. The lamp lights one thing at a time, on an aubergine night.

## ✧ The first night: the colours

| | | |
|---|---|---|
| **night** | `#110E24` | the ground |
| **raised** | `#1A1533` | frames |
| **parchment** | `#EFE4D0` | text |
| **copper** | `#C57B57` | the frames |
| **lamp** | `#F3B95F` | the one lit thing |
| **faience** | `#6FC2B6` | data |
| **rose** | `#E08497` | failure |

## ✧ The second night: what the frames hold

- **Windows**: gaps 6/14, rounding 8, a lamp → copper border on the focused window,
  lamp light around it
- **Waybar**: three frames two lines deep; a pendant with the lamp under the clock;
  eight-point star workspaces; the date counts nights (`night 262`)
- **mawaqit**: a banner three frames deep with a lattice window, lit for the adhan,
  dark with the lamp's star for the iqama
- **yawm**: `YAWM n` in lamp amber when due, a rose block when overdue
- **hyprlock**: a Libre Caslon Display clock, `Night N`, the saying in Arabic with
  its translation; no username
- **AlfLaylaQalam** cursor, **AlfLayla** icons (lantern folders, framed parchment,
  a copper jar for the trash), **GTK / Thunar**, **swaync** (frame depth = urgency)
- **Terminals**: Spline Sans Mono 10.5; tmux with a copper session block
- **Type**: Libre Caslon Display and Text, Scheherazade New, Albert Sans,
  Spline Sans Mono

## ✧ The third night: what you need

- Arch Linux (the package check uses `pacman`)
- Hyprland 0.56 or newer: the configuration is written in Lua
- waybar 0.15 or newer
- the packages in `alf-layla/packages.txt`:

```sh
sudo pacman -S --needed $(grep -v '^#' alf-layla/packages.txt)
```

## ✴ The fourth night: telling it

> [!WARNING]
> This is a whole desktop, not a colour scheme. It replaces every file listed
> in `alf-layla/MANIFEST`: the Hyprland, waybar, terminal, tmux, GTK and fontconfig
> configuration among them, and the theme line in `~/.zshrc`.
> Everything it replaces is backed up first.

```sh
git clone https://github.com/houssemMekhelbi/alf-layla.git
cd alf-layla
./alf-layla/restore.sh --dry-run   # show what would change, touch nothing
./alf-layla/restore.sh             # apply
```

`restore.sh` then:

1. reports missing packages;
2. backs up every path it is about to replace to `~/themes/.backups/before-alf-layla-<timestamp>/`;
3. copies the theme's `home/` over `$HOME` and removes the paths in its `ABSENT`;
4. points `~/.zshrc` at the theme's prompt;
5. applies its `gsettings.txt` and refreshes the font and icon caches;
6. builds the mawaqit-api image if it is missing, enables the user services and
   reloads Hyprland, waybar, hyprpaper, swaync and tmux.

`--files-only` copies the files and gsettings and leaves the services alone.

## ✧ The fifth night: taking it back

Copy the backup folder back over `$HOME`.

## ✧ The sixth night: prayer times

Prayer times come from [mawaqit.net](https://mawaqit.net) through a local copy of
[mawaqit-api](https://github.com/mrsofiane/mawaqit-api), run by podman on 127.0.0.1.
List your mosques in `~/.config/mawaqit/mosques`, one `<mawaqit.net slug> | <label>`
per line; scroll or right-click the prayer module to switch between them.

## ✧ The seventh night: the other stories

This is one of the hattin themes. They share one behaviour (binds, workspaces,
bar modules) and differ only in look. Clone several side by side and run the
`restore.sh` of the one you want: each switch removes what the previous theme
left that the new one does not use.

## ✧ And morning overtook Shahrazad

وأدرك شهرزاد الصباح فسكتت عن الكلام المباح

MIT, see [LICENSE](LICENSE). The fonts in `<theme>/home/.local/share/fonts/` are
under the SIL Open Font License; each licence text sits next to its font.
mawaqit-api (`<theme>/home/.local/share/mawaqit-api/`) is MIT, © Sofiane Louchene.
