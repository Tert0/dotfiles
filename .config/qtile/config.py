# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.layout.base import _SimpleLayoutBase
from typing import List  # noqa: F401
import subprocess
import re

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger

mod = "mod4"
alt = "mod1"
terminal = "gnome-terminal"
browser = "brave"
shell = "zsh"


def dmenu_windows(_):
    p = subprocess.Popen(["dmenu"], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdin = ('\n'.join(map(lambda window: window.name,
                           qtile.current_group.windows))).encode("utf-8")
    window_name = p.communicate(input=stdin)[0].decode("utf-8")
    if window_name not in map(lambda w: w.name, qtile.current_group.windows):
        return
    window = list(filter(lambda w: w.name == window_name.rstrip("\n"),
                  qtile.current_group.windows))[0]
    qtile.current_screen.set_group(window.group)
    window.group.focus(window)


def switch_group_relative(_, count=1):
    groups = list(filter(lambda g: g.windows or g.screen or g ==
                  qtile.current_group, qtile.groups))
    i = groups.index(qtile.current_group)
    qtile.current_screen.set_group(groups[(i + count) % len(groups)])


keys = [
    # Switch Groups Relatively
    Key(["control", alt], "h", lazy.function(switch_group_relative, -1)),
    Key(["control", alt], "l", lazy.function(switch_group_relative, 1)),
    # Move window focus
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move window
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Resize Window
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle Split/Unsplit
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Lauch Keybinds
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch Browser"),
    Key([], "XF86Calculator", lazy.spawn("speedcrunch")),
    Key([mod, "shift"], "w", lazy.function(
        dmenu_windows), desc="Show Names of all Windows"),
    # Change Layout
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Kill Window
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    # Reload
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    # Logout
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Lauch Program
    Key([mod], "r", lazy.spawn("dmenu_run"),
        desc="Spawn a command using a prompt widget"),
    # Flameshot Screenshot
    Key([], "Print", lazy.spawn("flameshot gui")),
    # Audio
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute 0 toggle"), desc="Mute Audio"),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume 0 -5%"), desc="Lower Audio Volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume 0 +5%"), desc="Raise Audio Volume"),
    # Toggle Floating
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
]
default_layout = "columns"
groups_data = [  # Format: (Name: str, Key: str, layout: str, spawn: List[str])
    ("1:  ", "1", default_layout, [terminal]),
    ("2:  ", "2", default_layout, [browser]),
    ("3:  ", "3", default_layout, []),
    ("4:  ", "4", default_layout, []),
    ("5:  ", "5", "i3tab", []),
    ("6:  ", "6", default_layout, []),
    ("7:  ", "7", default_layout, []),
    ("8:  ", "8", default_layout, []),
    ("9:  ", "9", default_layout, []),
    ("10: misc", "0", default_layout, []),
    ("11:  ", "ssharp", default_layout, []),
]
groups = [Group(name[0], spawn=name[3], layout=name[2])
          for name in groups_data]

for i in groups_data:
    keys.extend(
        [
            # mod + letter of group = switch to group
            Key(
                [mod],
                i[1],
                lazy.group[i[0]].toscreen(),
                desc="Switch to group {}".format(i[0]),
            ),
            # mod + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i[1],
                lazy.window.togroup(i[0], switch_group=True),
                desc="Switch to & move focused window to group {}".format(
                    i[0]),
            ),
        ]
    )


class I3Tab(_SimpleLayoutBase):
    def add(self, client):
        return super().add(client, 1)

    def configure(self, client, screen_rect):
        client.unhide()
        if self.clients and client is self.clients.current_client:
            client.place(screen_rect.x, screen_rect.y,
                         screen_rect.width, screen_rect.height, 0, None)
        else:
            client.place(screen_rect.x+(screen_rect.width*2), screen_rect.y+(screen_rect.height*2),
                         screen_rect.width, screen_rect.height, 0, None)

    cmd_previous = _SimpleLayoutBase.previous
    cmd_next = _SimpleLayoutBase.next

    cmd_up = cmd_previous
    cmd_down = cmd_next

    cmd_left = cmd_previous
    cmd_right = cmd_next


layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=3),
    layout.Max(),
    I3Tab(),
    # layout.Floating(),
    # Try more layouts by unleashing below layouts.
    layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(),
    layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Font Awesome 5 Free",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()
colors = {
    "background": "#222222",
    "background-focus": "#444444",
    "foreground": "#dfdfdf",
    "widget1": "#002B36",  # ff3c38 048a81
    "widget2": "#839496",  # a23e48 32a287
}

bar_size = 30


def create_widget_seperator(left: str, right: str) -> widget.TextBox:
    return widget.TextBox(
        text="",
        fontsize=bar_size*1.9,
        foreground=colors[right],
        background=colors[left],
        padding=0,
        margin=0,
    )


powerline_bar = [
    create_widget_seperator("background", "widget2"),
    widget.WindowName(
        font="sans",
        background=colors["widget2"],
        max_chars=50,
    ),
    create_widget_seperator("widget2", "widget1"),
    widget.Systray(
        background=colors["widget1"]
    ),
    create_widget_seperator("widget1", "widget2"),
    widget.CheckUpdates(
        background=colors["widget2"],
        display_format=" {updates}",
        distro="Arch_paru",
    ),
    create_widget_seperator("widget2", "widget1"),
    widget.DF(
        background=colors["widget1"],
        visible_on_warn=False,
        format="{p}: {r:.0f}%",
    ),
    create_widget_seperator("widget1", "widget2"),
    widget.Memory(
        format=" {MemPercent}%",
        background=colors["widget2"],
    ),
    create_widget_seperator("widget2", "widget1"),
    widget.CPU(
        format=" {load_percent}%",
        background=colors["widget1"],
    ),
    create_widget_seperator("widget1", "widget2"),
    widget.ThermalSensor(
        fmt=" {}",
        background=colors["widget2"],
    ),
    create_widget_seperator("widget2", "widget1"),
    widget.Volume(
        background=colors["widget1"],
        fmt=" {}",
    ),
    create_widget_seperator("widget1", "widget2"),
    widget.Clock(
        format=" %a, %b %e - %R",
        background=colors["widget2"],
    ),
    create_widget_seperator("widget2", "widget1"),
    widget.QuickExit(
        default_text="[ logout ] ",
        countdown_start=3,
        background=colors["widget1"],
    ),
]

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.Image(
                    filename="~/.config/qtile/icons/logo.png",
                    mouse_callbacks={"Button1": lazy.spawn(
                        f"{browser} kernel.org")}
                ),
                widget.CurrentLayout(),
                widget.GroupBox(
                    highlight_method="line",
                    highlight_color=colors["background-focus"],
                    hide_unused=True,
                    disable_drag=True,
                ),
                *powerline_bar,
            ],
            bar_size,
            background=colors["background"],
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # top=bar.Bar(
        #    [
        #        widget.TaskList(
        #            icon_size=0,
        #            spacing=10,
        #            max_title_width=300,
        #        ),
        #    ],
        #    int(bar_size*0.8),
        #    background=colors["background"],
        # ),
        # left=bar.Gap(3),
        # right=bar.Gap(3),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="SpeedCrunch"),  # SpeedCrunch Calculator
    ],
)
auto_fullscreen = True
focus_on_window_activation = "urgent"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
# Autostart


@ hook.subscribe.startup
def startup():
    def execute_once(process, executable=None):
        if executable is None:
            executable = process

        def process_running():
            pgrep = subprocess.Popen(
                ["pgrep", "-x", process], stdout=subprocess.PIPE)
            for line in pgrep.stdout:
                if line.decode("utf-8") != "":
                    return True
            return False
        if not process_running():
            subprocess.Popen(
                executable.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    execute_once("nitrogen --restore")
    execute_once("flameshot")
    execute_once("nm-applet")
    execute_once("pnmixer")
    execute_once("keepassxc")
    execute_once("clipit")
    execute_once("xcompmgr")
    execute_once("polkit-gnome-authentication-agent-1",
                 "/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1")
    execute_once("gnome-keyring-daemon --start --components=ssh")
