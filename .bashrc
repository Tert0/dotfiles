#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias nosudopacman='pacman'
alias pacman='sudo pacman'
alias open='nemo $PWD &'
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

export JAVA_HOME="/usr/lib/jvm/java-8-openjdk"
export ANDROID_HOME="~/Android/Sdk"
export PATH="/usr/lib/jvm/java-8-openjdk/bin/:~/Android/Sdk/tools/:~/Android/Sdk/emulator/:$PATH"
