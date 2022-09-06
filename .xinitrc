[[ -f ~/.Xmodmap ]] && xmodmap ~/.Xmodmap

xset r rate 300 50
xrandr --output eDP1 --mode 1366x768 --rate 48.05 --brightness 0.7
nitrogen --restore
qtile start

