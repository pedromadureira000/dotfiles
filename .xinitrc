[[ -f ~/.Xmodmap ]] && xmodmap ~/.Xmodmap

# /usr/bin/pipewire &
# /usr/bin/pipewire-pulse &
# /usr/bin/wireplumber &


xset r rate 300 50
xrandr --output eDP1 --mode 1366x768 --rate 48.05 --brightness 1
nitrogen --restore
qtile start

