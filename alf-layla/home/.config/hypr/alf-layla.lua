-- Alf Layla look and feel.
-- A story inside a story: copper frames nest, and the deeper the frame the more
-- it matters. Loaded after futuwwa.lua so these values win; behaviour and binds
-- stay there.
--
-- Hyprland draws one border per window, so a window is one frame deep. The
-- second frame of the popups comes from fzf's own border, and the bar, the
-- prayer banner, the lock field and the notifications draw theirs themselves.
-- Lamp amber lights one thing at a time: here, the focused window's border
-- and the warm light around it.

local C = {
    ground = "110E24",
    line   = "3A2F5C",
    copper = "C57B57",
    lamp   = "F3B95F",
    night  = "05030E",
}

hl.config({
    general = {
        gaps_in     = 6,
        gaps_out    = 14,
        border_size = 1,
        col = {
            active_border   = { colors = { "rgb(" .. C.lamp .. ")", "rgb(" .. C.copper .. ")" }, angle = 45 },
            inactive_border = "rgb(" .. C.line .. ")",
        },
    },

    decoration = {
        rounding       = 8,
        rounding_power = 2.0,

        active_opacity   = 0.95,
        inactive_opacity = 0.88,

        blur = {
            enabled           = true,
            size              = 8,
            passes            = 3,
            vibrancy          = 0.10,
            noise             = 0.015,
            new_optimizations = true,
            popups            = true,
        },

        glow = {
            enabled = false,
        },

        -- Lamp light around the focused window, plain night under the others.
        shadow = {
            enabled        = true,
            range          = 40,
            render_power   = 3,
            offset         = { 0, 6 },
            color          = "rgba(" .. C.lamp .. "26)",
            color_inactive = "rgba(" .. C.night .. "88)",
        },
    },

    group = {
        col = {
            border_active   = "rgb(" .. C.lamp .. ")",
            border_inactive = "rgb(" .. C.line .. ")",
        },
    },

    misc = {
        disable_hyprland_logo    = true,
        disable_splash_rendering = true,
        background_color         = "rgb(" .. C.ground .. ")",
    },
})

-- Cursor: AlfLaylaQalam (~/.local/share/icons/AlfLaylaQalam, hyprcursor + XCursor).
-- On a live theme switch restore.sh runs `hyprctl setcursor` from gsettings.txt.
hl.env("HYPRCURSOR_THEME", "AlfLaylaQalam")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("XCURSOR_THEME", "AlfLaylaQalam")
hl.env("XCURSOR_SIZE", "24")

-- A config reload resets the cursor to the default theme; set it again.
local function layla_cursor()
    hl.exec_cmd("hyprctl setcursor AlfLaylaQalam 24")
end
hl.on("hyprland.start", layla_cursor)
hl.on("config.reloaded", layla_cursor)

-- Launcher bind points at the Alf Layla launcher; futuwwa.lua binds the Girih one.
hl.unbind("SUPER + D")
hl.bind("SUPER + D",
    hl.dsp.exec_cmd(os.getenv("HOME") .. "/.local/bin/layla-launcher"),
    { description = "Application launcher" })

-- Terminals draw their own night glass (foot/alacritty/ghostty alpha) so text stays opaque.
hl.window_rule({
    name    = "layla-terminal-opaque",
    match   = { class = "^(foot|footclient|Alacritty|com.mitchellh.ghostty)$" },
    opacity = "1.0 override 1.0 override",
})

-- Blur behind layer surfaces: the bar frames, alert banners, launcher, notifications.
-- ignore_alpha keeps the wallpaper between the bar frames unblurred.
hl.layer_rule({
    name         = "layla-bar-glass",
    match        = { namespace = "^hattin-" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "layla-launcher-glass",
    match        = { namespace = "^launcher$" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "layla-notify-glass",
    match        = { namespace = "^swaync" },
    blur         = true,
    ignore_alpha = 0.1,
})

-- Launcher: floating foot + fzf (~/.local/bin/layla-launcher).
hl.window_rule({
    name     = "layla-launcher",
    match    = { class = "^layla-launcher$" },
    float    = true,
    size     = "780 470",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

-- Taskwarrior popups from the waybar "yawm" module (~/.local/bin/layla-yawm).
hl.window_rule({
    name     = "layla-yawm",
    match    = { class = "^layla-yawm$" },
    float    = true,
    size     = "820 600",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

hl.window_rule({
    name     = "layla-yawm-add",
    match    = { class = "^layla-yawm-add$" },
    float    = true,
    size     = "720 240",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

local layla_popups = { "layla-launcher", "layla-yawm", "layla-yawm-add" }

-- Close every popup window except those of class `keep`.
-- hl.get_windows matches `class` exactly (no regex), so pass the plain name.
function layla_close_popups(keep)
    for _, class in ipairs(layla_popups) do
        if class ~= keep then
            for _, w in ipairs(hl.get_windows({ class = class })) do
                hl.dispatch(hl.dsp.window.close({ window = "address:" .. w.address }))
            end
        end
    end
end

function layla_close_launcher()
    layla_close_popups()
end

-- Close popups as soon as focus moves elsewhere.
hl.on("window.active", function(win)
    layla_close_popups(win and win.class)
end)
