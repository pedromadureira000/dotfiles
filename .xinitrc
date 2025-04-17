[[ -f ~/.Xmodmap ]] && xmodmap ~/.Xmodmap

if [[ "$USE_IWD" == "true" ]]; then
    sudo systemctl start iwd
fi

xset r rate 300 50
xrandr --output $SCREEN_NAME --mode $SCREEN_SIZE --rate 48.05 --brightness 1
nitrogen --restore
dropbox start &
qtile start
