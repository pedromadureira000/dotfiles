#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

source $HOME/.env-var

#ignore duplicated
export HISTCONTROL=ignoreboth

alias ls='ls --color=auto'

# PS1='[\u@\h \W]\$ '
# export PS1='\[\e[36m\][\u@\h \w]\$ \[\e[0m\]'
export PS1='\[\e[0;36m\][\u@\h \w]\$ \[\e[0m\]'

#--- pyenv
# export PYENV_ROOT="$HOME/.pyenv"
# export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init --path)"
# eval "$(pyenv virtualenv-init -)"

# Aliases
alias mng='python $VIRTUAL_ENV/../manage.py'
alias vim='nvim'
# alias ranger='ranger-fix'
alias unimatrix='unimatrix-fix'
alias la='ls -A'
alias du='du -h --max-depth=1'
alias grep='grep --color=auto'
alias ..='cd ..'
alias gc='git commit -m'
alias gC='git checkout'
alias gp='git push'
alias ga='git add'
alias gs='git status'
alias gd='git diff'
# alias gl='git log --graph --abbrev-commit --all'  XXX This will get commits for other branches
alias gl='git log --graph --abbrev-commit'
alias gb='git branch'
alias journal='sudo journalctl -e'
alias used_space2='sudo du -h --max-depth=1 | sort -h'
alias used_space='sudo find . -maxdepth 1 -type d -exec du -sh {} \; | sort -h'
alias top_biggest_folders='du -h --max-depth=1 | sort -hr | head -5'
alias top_biggest_files='find . -maxdepth 1 -type f -exec du -h {} + | sort -hr | head -5'

alias free_space='df -a -h /'
alias used_memory='free -h'
alias cl='clear'
alias diff='git diff HEAD~1 HEAD'
alias make_script='chmod +x'
alias llmlj='llm logs -n 1 --json'
alias llml='llm logs -n 1'
alias ip_show='iwctl station wlan0 show'
alias start_docker='sudo systemctl start docker'
alias restart_dhcp='sudo systemctl restart dhcpcd'
alias status_dhcp='sudo systemctl status dhcpcd'

LLM_OPENAI_SHOW_RESPONSES=1

alias mount_sync_vault_daemon="rclone mount --daemon --vfs-cache-mode full sync-vault:/sync_vault /home/ph/Documents/sync_vault_mount"
alias mount_sync_vault="rclone mount --vfs-cache-mode full sync-vault:/sync_vault /home/ph/Documents/sync_vault_mount"

alias check_difference_rclone2="rclone check sync-vault:/sync_vault /home/ph/Documents/sync_vault --checksum"
alias check_difference_rclone="rclone check /home/ph/Documents/sync_vault sync-vault:/sync_vault --checksum"

alias turn_on_wifi="sudo mv /var/lib/iwd/'TIM ULTRAFIBRA_9DE0_2G.psk_' /var/lib/iwd/'TIM ULTRAFIBRA_9DE0_2G.psk' && sudo systemctl restart iwd"
alias turn_off_wifi="sudo mv /var/lib/iwd/'TIM ULTRAFIBRA_9DE0_2G.psk' /var/lib/iwd/'TIM ULTRAFIBRA_9DE0_2G.psk_' && sudo systemctl restart iwd"

# set default programs
export PATH=$PATH:$HOME/.scripts
export EDITOR=nvim
export VISUAL=nvim
export BROWSER=brave
export TERM=alacritty

# For check 'flutter doctor' boxe
#export CHROME_EXECUTABLE=google-chrome-stable
export CHROME_EXECUTABLE=brave
export ANDROID_HOME=$HOME/android-sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
# add flutter commands on path
export PATH="$PATH":"$HOME/.pub-cache/bin"

# fzf completion and keybindings
source /usr/share/fzf/completion.bash
source /usr/share/fzf/key-bindings.bash

if [[ "$(tty)" = "/dev/tty1" ]]; then
	startx
fi


export PATH="$PATH":"$HOME/apache-maven-3.9.7/bin"

# Created by `pipx` on 2024-10-09 13:25:57
export PATH="$PATH:/home/ph/.local/bin"

# ruby
export PATH="$HOME/.local/share/gem/ruby/3.3.0/bin:$PATH"

# nvm (nodejs versions control)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

#rbenv
export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"
