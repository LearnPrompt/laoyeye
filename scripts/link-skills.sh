#!/usr/bin/env bash
# 把仓库里的 Skill 软链进本机的 Skill 目录，git pull 之后自动跟着更新。
# 加、删、改名之后重跑一次。
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for target in "$HOME/.claude/skills" "$HOME/.agents/skills" "${CODEX_HOME:-$HOME/.codex}/skills"; do
  [ -d "$(dirname "$target")" ] || continue
  mkdir -p "$target"
  while IFS= read -r skill; do
    name="$(basename "$skill")"
    link="$target/$name"
    if [ -e "$link" ] && [ ! -L "$link" ]; then
      echo "skip   $link 已存在且不是软链，没动它"
      continue
    fi
    if [ -L "$link" ] && [[ "$(readlink "$link")" != "$REPO"/* ]]; then
      echo "skip   $link 指向别的仓库（$(readlink "$link")），没动它"
      continue
    fi
    ln -sfn "$skill" "$link"
    echo "link   $link -> $skill"
  done < <(find "$REPO/skills" -name SKILL.md -exec dirname {} \; | sort)
done
