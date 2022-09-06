[[ -f ~/.Xmodmap ]] && xmodmap ~/.Xmodmap

#----pam-gnupg 
# if [ -x /usr/bin/gpg-agent ]; then
	# eval "$(/usr/bin/gpg-agent --daemon)"
# fi

# ExecStartPre=/usr/bin/sleep 5

#---pam-gnupg END

xset r rate 300 50
xrandr --output eDP1 --mode 1366x768 --rate 48.05 --brightness 0.7
nitrogen --restore
qtile start

