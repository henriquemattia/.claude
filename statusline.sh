#!/usr/bin/env bash

input=$(cat)
j() { printf '%s' "$input" | jq -r "$1"; }

ESC=$'\033'
r="${ESC}[0m"
dim="${ESC}[38;5;109m"
sep=" | "

project_dir=$(j '.workspace.project_dir')
project_name=$(basename "$project_dir")
model=$(j '.model.display_name')

context_size=$(j '.context_window.context_window_size')
cur_in=$(j '.context_window.current_usage.input_tokens // 0')
cur_out=$(j '.context_window.current_usage.output_tokens // 0')
cache_read=$(j '.context_window.current_usage.cache_read_input_tokens // 0')
current_total=$((cur_in + cur_out + cache_read))
current_k=$(awk -v t="$current_total" 'BEGIN{printf "%.0f", t/1000}')
context_k=$(awk -v s="$context_size" 'BEGIN{printf "%.0f", s/1000}')

palette=(31 32 33 36 91 92 96)
model_color=${palette[$((RANDOM % ${#palette[@]}))]}

out="${ESC}[94m${project_name}${r}"

branch=""
if [ -d "$project_dir/.git" ]; then
  branch=$(cd "$project_dir" && git --no-optional-locks symbolic-ref --short HEAD 2>/dev/null || git --no-optional-locks rev-parse --short HEAD 2>/dev/null)
fi
[ -n "$branch" ] && out+="${sep}${ESC}[95m${branch}${r}"

out+="${sep}${ESC}[${model_color}m${model}${r}"
out+="${sep}${ESC}[93m${current_k}k/${context_k}k${r}"

window() {
  local label=$1 pct=$2 epoch=$3 tfmt=$4
  { [ -z "$pct" ] || [ "$pct" = null ]; } && return
  local pct_i col reset_str=""
  pct_i=$(awk -v p="$pct" 'BEGIN{printf "%.0f", p}')
  col=$(awk -v p="$pct" 'BEGIN{ if (p+0>=85) print 91; else if (p+0>=50) print 33; else print 32 }')
  if [ -n "$epoch" ] && [ "$epoch" != null ]; then
    reset_str=" ${dim}$(date -r "${epoch%.*}" "+$tfmt")${r}"
  fi
  printf '%s' "${sep}${dim}${label} ${ESC}[${col}m${pct_i}%${r}${reset_str}"
}

out+=$(window "5h" "$(j '.rate_limits.five_hour.used_percentage // empty')" "$(j '.rate_limits.five_hour.resets_at // empty')" "%H:%M")
out+=$(window "7d" "$(j '.rate_limits.seven_day.used_percentage // empty')" "$(j '.rate_limits.seven_day.resets_at // empty')" "%a %H:%M")

printf '%s' "$out"
