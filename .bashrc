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
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"


# criar .venv no diretorio do projeto
export PIPENV_VENV_IN_PROJECT=1

# pipenv read pyenv python version
export PIPENV_PYTHON="/home/phsw/.pyenv/shims/python"

eval "$(pyenv virtualenv-init -)"

# Aliases
alias mng='python $VIRTUAL_ENV/../manage.py'
alias vim='nvim'
alias ranger='ranger-fix'
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
alias used_space='sudo du -h --max-depth=1 | sort -h'
alias free_space='df -a -h /'

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

# fzf completion and keybindings
source /usr/share/fzf/completion.bash
source /usr/share/fzf/key-bindings.bash

if [[ "$(tty)" = "/dev/tty1" ]]; then
	startx
fi

