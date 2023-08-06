#!/usr/bin/env zsh
# read -d $'\n' -r marker
# dvar marker
# while read -d "$marker" -r cmd
while read -d "" -r cmd
do
    test -z "$cmd" && continue
    dact ec ----------------------
    dvar cmd
    # local errfile="$(mktemp)"
    # local out
    # out="$(eval "$cmd" 2>"$errfile")"
    eval "$cmd"
    local ret=$?
    print -n $'\0\n'
    print -r -- $ret
    print -n $'\0\n' >&2
done
