# ~/.config/zsh/alf-layla.zsh-theme
# Alf Layla prompt: standalone (no oh-my-zsh), no powerline blocks.
# Two lines: the context line, then the lit prompt mark.
#   status  rose "✕ code", ⚡ root, ⚙ jobs; only when there is something to say
#   context muted user@host, only over SSH or as another user
#   dir     lit copper, bold (the shortened path)
#   git     faience branch, rose ± when dirty
#   prompt  a lamp-amber › on the second line; the clock sits right, dim
# Hex colours need zsh 5.7+ and a true-colour terminal.

setopt prompt_subst

LAYLA_DEFAULT_USER=${LAYLA_DEFAULT_USER:-rahal}   # hide context on your own box

S_TEXT='#EFE4D0'  S_STRUCT='#E0A06C' S_MUTED='#9E94BA'
S_TAN='#6A618E'   S_SHU='#E08497'    S_AI='#6FC2B6'
S_LAMP='#F3B95F'

# ~/dotfiles/hypr -> ~/d/hypr
layla_short_pwd() {
  local p=${(%):-%~}
  local -a parts=("${(@s:/:)p}")
  local i
  for (( i = 1; i < ${#parts}; i++ )); do
    [[ -z ${parts[i]} || ${parts[i]} == '~' ]] && continue
    if [[ ${parts[i]} == .* ]]; then
      parts[i]=${parts[i][1,2]}
    else
      parts[i]=${parts[i][1]}
    fi
  done
  print -rn -- "${(j:/:)parts//\%/%%}"
}

layla_status() {
  local -a s
  (( LAYLA_RETVAL != 0 )) && s+="✕ $LAYLA_RETVAL"
  (( UID == 0 )) && s+="⚡"
  [[ -n ${jobstates} ]] && s+="⚙"
  (( ${#s} )) && print -n "%F{$S_SHU}${(j: :)s}%f  "
}

layla_context() {
  [[ $USER != $LAYLA_DEFAULT_USER || -n $SSH_CONNECTION ]] &&
    print -n "%F{$S_MUTED}%n@%m%f  "
}

layla_dir() {
  print -n "%B%F{$S_STRUCT}$(layla_short_pwd)%f%b"
}

layla_git() {
  command git rev-parse --is-inside-work-tree &>/dev/null || return
  local ref
  ref=$(command git symbolic-ref --short HEAD 2>/dev/null) ||
    ref="➦ $(command git rev-parse --short HEAD 2>/dev/null)"
  ref=${ref//\%/%%}
  print -n "  %F{$S_AI}$ref%f"
  [[ -n $(command git status --porcelain --ignore-submodules=dirty 2>/dev/null | head -n1) ]] &&
    print -n "%F{$S_SHU} ±%f"
}

layla_build_prompt() {
  layla_status
  layla_context
  layla_dir
  layla_git
}

layla_precmd() { LAYLA_RETVAL=$? }
autoload -Uz add-zsh-hook
add-zsh-hook precmd layla_precmd

PROMPT='%{%f%b%k%}$(layla_build_prompt)
%F{$S_LAMP}›%f '
RPROMPT="%F{$S_TAN}%*%f"

# ---- completion ------------------------------------------------------
autoload -Uz compinit && compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' list-colors 'ma=48;2;35;28;66;38;2;243;185;95'

# ---- plugins ---------------------------------------------------------
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=$S_TAN"
[[ -r /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ]] &&
  source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

# zsh-syntax-highlighting must be sourced last, then styled.
if [[ -r /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]]; then
  source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
  ZSH_HIGHLIGHT_STYLES[command]='fg=#EFE4D0'
  ZSH_HIGHLIGHT_STYLES[builtin]='fg=#EFE4D0'
  ZSH_HIGHLIGHT_STYLES[alias]='fg=#EFE4D0'
  ZSH_HIGHLIGHT_STYLES[function]='fg=#EFE4D0'
  ZSH_HIGHLIGHT_STYLES[precommand]='fg=#EFE4D0,underline'
  ZSH_HIGHLIGHT_STYLES[path]='fg=#E0A06C,underline'
  ZSH_HIGHLIGHT_STYLES[single-hyphen-option]='fg=#6FC2B6'
  ZSH_HIGHLIGHT_STYLES[double-hyphen-option]='fg=#6FC2B6'
  ZSH_HIGHLIGHT_STYLES[single-quoted-argument]='fg=#9CC58A'
  ZSH_HIGHLIGHT_STYLES[double-quoted-argument]='fg=#9CC58A'
  ZSH_HIGHLIGHT_STYLES[unknown-token]='fg=#E08497,underline'
fi

export FZF_DEFAULT_OPTS="--color=bg+:#231C42,fg:#9E94BA,fg+:#EFE4D0,hl:#E0A06C,hl+:#F3B95F,pointer:#F3B95F,prompt:#F3B95F,info:#9E94BA,border:#C57B57 --pointer='✴' --prompt='› ' --border=rounded"
