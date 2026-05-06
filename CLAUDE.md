# CLAUDE.md

## WHY - Purpose

Configuration repository for Claude Code: agent definitions, settings, and utilities that control how Claude Code operates across all projects.

## WHAT - Architecture

```
~/.claude/
├── agents/           # Multi-agent system: feature-refiner → coder → qa-code-reviewer
├── commands/         # Custom slash commands
├── skills/           # User-authored skills
├── utils/            # Shell helpers (cl command)
└── settings.json     # Global settings
```

**Stack**: Markdown agents with YAML frontmatter, bash utilities

## HOW - Key Commands

```bash
source ~/.claude/utils/shell-alias-setup.sh  # Enable cl helper
cl "your question"                            # Quick terminal help
```

## Coding Guidelines

1. Never add code comments
2. Minimize logging and console output
3. Functional React only (no classes)
4. Simplicity first — YAGNI

## Documentation Pointers

| Topic | File |
|-------|------|
| Agent workflow & invocation | `agent_docs/agents.md` |
| Coding standards & QA criteria | `agent_docs/coding-standards.md` |
| Full directory structure | `agent_docs/directory-structure.md` |
| Shell integration details | `agent_docs/shell-integration.md` |

## Critical Notes

- Agent chain: feature-refiner → coder → qa-code-reviewer (coder ALWAYS delegates to qa)
- ALWAYS ask permission before committing — user reviews everything before any commit
- NEVER run destructive DB commands (`--fresh`, drops, truncates) on any project
- Specs go in `specs/[feature-name].md`
