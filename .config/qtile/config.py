import os
from typing import List  # noqa: F401
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import qtile
from datetime import datetime


screen_name = os.environ.get('SCREEN_NAME')
screen_size = os.environ.get('SCREEN_SIZE')

date_journal_filename = datetime.now().strftime('%Y-%m')


mod = "mod4"
terminal = guess_terminal()
username = os.getlogin()

def open_llmr(model, mode):
    return f'alacritty --option font.size=20 -e bash -c "export PATH=\\"$PATH:/home/{os.environ["USER"]}/.local/bin\\"; llmr {model} {mode}; exec bash"'

llm_model_options = {
    #  "gemini":"gemini-2.5-pro-exp-03-25", #free
    "gemini": "gemini-2.5-pro-preview-03-25", #paid
    #  "openai": "openai/o3",
    "openai": "openai/gpt-4.1",
    #  "openai": "openai/o4-mini",
    "claude": "claude-3.7-sonnet", # for thinking: -o thinking 1 -o thinking_budget 1025
}

class LLMMode:
    default = "default"
    coding = "coding"
    default2 = "default2"
    code_analyst = "code-analyst"

def chosen_terminal(app):
    return f'kitty {app}'

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    #  Key([mod], "space", lazy.layout.next(),  <---- (useless)
        #  desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    #  Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes

    #  Key([mod, "shift"], "Return", lazy.layout.toggle_split(),  <---- ?
        #  desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    #------/ SCREENSHOTS
    Key([], "Print", lazy.spawn("scrot 'ArchLinux-%Y-%m-%d-%s_screenshot_$wx$h.jpg' -e 'mv $f ~/Pictures'")),
    Key([mod], "Print", lazy.spawn("scrot -s  'ArchLinux-%Y-%m-%d-%s_screenshot_$wx$h.jpg' -e 'mv $f ~/Pictures'")),

    #------/ Key apps
    #  Key([mod, "control"], "f", lazy.spawn("ranger-fix")),
    Key([mod, "control"], "f", lazy.spawn(chosen_terminal("ranger"))),
    Key([mod, "control"], "a", lazy.spawn(terminal + " -e pavucontrol")),
    Key([mod], "b", lazy.spawn("brave")),
    Key([mod, "control"], "b", lazy.spawn(chosen_terminal(f"nvim /home/{username}/.bashrc"))),

    #-----/ Scripts
    Key([mod], "space", lazy.spawn("toggle_keyboard_layout.sh")),
    Key([mod, "control"], "d", lazy.spawn("discord")),
    Key(["mod1", "control"], "t", lazy.spawn("Telegram")),
    Key([mod, "control"], "p", lazy.spawn("passmenu -l 5 -fn 'sans-10'")),
    Key([mod, "mod1"], "Escape", lazy.spawn("sudo shutdown now")),
    Key([mod, "lock"], "Escape", lazy.spawn("sudo reboot")),
    Key([mod, "control"], "Escape", lazy.spawn("xlock -delay 10000 -mode random")),
    Key([mod], "1", lazy.spawn(f"xrandr --output {screen_name} --mode {screen_size} --rate 48.05 --brightness 1")),
    Key([mod], "2", lazy.spawn(f"xrandr --output {screen_name} --mode {screen_size} --rate 48.05 --brightness 0.8")),
    Key([mod], "3", lazy.spawn(f"xrandr --output {screen_name} --mode {screen_size} --rate 48.05 --brightness 0.7")),
    Key([mod], "4", lazy.spawn(f"xrandr --output {screen_name} --mode {screen_size} --rate 48.05 --brightness 0.6")),
    Key([mod], "5", lazy.spawn(f"xrandr --output {screen_name} --mode {screen_size} --rate 48.05 --brightness 0.5")),
    Key([mod, "control"], "s", lazy.spawn(f"xrandr --output HDMI-1 --mode 1920x1080 --same-as eDP-1")),

    # ----/ second monitor 
    Key([mod, "control"], "1", lazy.to_screen(0)), # go to main monitor
    Key([mod, "control"], "2", lazy.to_screen(1)), # go to second monitor

    # ---- / Documents
    Key([mod, "control"], "t", lazy.spawn(chosen_terminal(f"nvim /home/{username}/Dropbox/0.Work-TODO.1.md"))),
    Key([mod], "t", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/z.work-memory/1.info-cache.md"))),
    #  "/home/ph/utils/llmr_py_runs/default/attachments.md"

    Key([mod], "n", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/z.work-memory/1.work-memory.md"))),
    Key([mod, "control"], "n", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/z.work-memory/2.work-memory.md"))),
    Key(["mod1"], "n", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/z.work-memory/3.personal-memory.md"))),
    Key(["mod1", "control"], "n", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/z.work-memory/4.personal-memory.md"))),
    Key(["mod1", "control"], "j", lazy.spawn(chosen_terminal(f"nvim /home/{username}/Dropbox/4.Writing/1.Journal/{date_journal_filename}.md"))),

    # --- / llm
    Key([mod, "control"], "u", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/llmr_py_runs/coding/last-log.md"))),
    Key(["mod1"], "u", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/llmr_py_runs/default/last-log.md"))),
    Key(["mod1", "control"], "u", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/llmr_py_runs/default2/last-log.md"))),

    Key([mod], "7", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/llmr_py_runs/coding/output.md"))),
    Key([mod, "control"], "7", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/llmr_py_runs/default/output.md"))),
    Key(["mod1"], "7", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/llmr_py_runs/default2/output.md"))),
    Key(["mod1", "control"], "7", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/llmr_py_runs/code-analyst/output.md"))),

    Key([mod], "y", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/llmr_py_runs/coding/task.md"))),
    Key([mod, "control"], "y", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/llmr_py_runs/default/task.md"))),
    Key(["mod1"], "y", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/llmr_py_runs/default2/task.md"))),
    Key(["mod1", "control"], "y", lazy.spawn(chosen_terminal(f"nvim /home/{username}/utils/llmr_py_runs/code-analyst/task.md"))),

    Key([mod], "m", lazy.spawn(open_llmr(llm_model_options["claude"], LLMMode.coding))),
    Key([mod, "control"], "m", lazy.spawn(open_llmr(llm_model_options["openai"], LLMMode.default))),
    Key(["mod1"], "m", lazy.spawn(open_llmr(llm_model_options["gemini"], LLMMode.default2))),
    Key(["mod1", "control"], "m", lazy.spawn(open_llmr(llm_model_options["gemini"], LLMMode.code_analyst))),

    # --- / configs
    Key([mod, "control"], "0", lazy.spawn(chosen_terminal(f"nvim /home/{username}/.config/qtile/config.py"))),
    # --- / Available
    #  Key([mod, "control"], "9", lazy.spawn("")),
    #  Key([mod], "w", lazy.spawn()),
    #  Key([mod, "control"], "0", lazy.spawn(chosen_terminal())),
    #  Key([mod, "control"], "8", lazy.spawn("")),
]

groups = [Group(i) for i in "asdfuiop"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])


layout_theme = {"border_width": 1,
                "margin": 0,
                "border_focus":"#71a3ad",
                "border_normal": "1D2330"
                }

layouts = [
    #  layout.Columns(border_focus_stack='#d75f5f', **layout_theme),
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    #  layout.Stack(num_stacks=2),
    #  layout.Bsp(),
    #  layout.Matrix(),
    #  layout.MonadTall(),
    #  layout.MonadWide(),
    #  layout.RatioTile(),
    #  layout.Tile(),
    #  layout.TreeTab(),
    #  layout.VerticalTile(),
    #  layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=2,
    background="#000000"
)
extension_defaults = widget_defaults.copy()

screen_widgets = [
    widget.Sep(
        linewidth = 0,
        padding = 8,
        foreground = '#ffffff',
        background = '#000000'
    ),

    widget.Image(
        filename = "~/.config/qtile/icons/python-icon.png",
        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("unimatrix-fix")},
    ),
    widget.GroupBox(),
    widget.WindowName(),
    widget.Chord(
        chords_colors={
            'launch': ("#ff0000", "#ffffff"),
        },
        name_transform=lambda name: name.upper(),
    ),
    #  widget.Systray(),

    widget.Prompt(),

    widget.Image(
       filename = "~/.config/qtile/icons/sound_icon.png",
       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("alacritty -e pavucontrol")}
    ),

    widget.TextBox(text = '   | ', foreground = '#ffffff', padding = 0, fontsize = 26),  # <---------------

    widget.Sep(
           linewidth = 0,
           padding = 8,
           foreground = '#ffffff',
           background = '#000000'
           ),

    widget.TextBox(
           text = '⚡  ',
           #  text = '⌛',
           #  background = "#282c34",
           foreground = '#ffffff',
           padding = 0,
           fontsize = 22
           ),
    widget.Battery(format='{percent:2.0%}', foreground='#ffffff', low_percentage=0.15),

    widget.TextBox(text = '  |  ', foreground = '#ffffff', padding = 0, fontsize = 26),  # <---------------

    widget.Image(
           filename = "~/.config/qtile/icons/calendar.png",
           ),
    widget.Clock(format='%A, %B %d  ', foreground='#ffffff'),

    widget.TextBox(text = '  |  ', foreground = '#ffffff', padding = 0, fontsize = 26),  # <---------------

    widget.TextBox(
           text = '⌚ ',
           #  text = '⌛',
           #  background = "#282c34",
           foreground = '#ffffff',
           padding = 0,
           fontsize = 22
           ),
    widget.Clock(format='%I:%M    ', foreground='#ffffff'),
]

screens = [
    Screen(
        #  bottom=bar.Bar(
        top=bar.Bar(
            screen_widgets,
            24,
        ),
    ),
    Screen(
        top=bar.Bar(
            screen_widgets,
            24,  # height of the bar
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
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
