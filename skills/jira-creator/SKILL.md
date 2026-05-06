---
name: jira-creator
description: Cria tasks, bugs e stories no Jira via CLI. Suporta criacao individual, em lote, transicao de status, assign e comentarios.
---

# Jira Creator

Cria e gerencia work items no Jira Cloud via wrapper seguro.

## Ferramenta

```bash
~/.claude/tools/jira_write.py <action> [args...]
```

**IMPORTANTE**: Sempre use o caminho absoluto `~/.claude/tools/jira_write.py`.

## Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `create <PROJECT> <TYPE> <SUMMARY> [opts]` | Cria uma issue individual |
| `create-bulk <JSON_FILE>` | Cria múltiplas issues de um arquivo JSON |
| `create-from-json '<JSON>'` | Cria múltiplas issues de uma string JSON inline |
| `edit <KEY> [--summary] [--type] [--description] [--label]` | Edita campos de uma issue |
| `transition <KEY> <STATUS>` | Move issue para um status (ex: "Done", "In Progress") |
| `assign <KEY> <EMAIL\|@me>` | Atribui issue a alguém |
| `comment <KEY> <TEXT>` | Adiciona comentário a uma issue |

## Criar Issue Individual

```bash
~/.claude/tools/jira_write.py create AT Task "Titulo da task" \
  --description "Descricao detalhada" \
  --label "routing,backend" \
  --assignee "@me" \
  --parent "AT-352"
```

**Tipos validos (PT-BR, case-sensitive)**: Tarefa, Bug, História, Epic, Incidente

**Regra de tipo**: Prefixo `fix:` no titulo → tipo **Bug**. Prefixo `feat:` → tipo **Tarefa** ou **História**.
**Flags opcionais**: `--description`, `--parent`, `--label`, `--assignee`

## Criar em Lote (bulk)

Gere um arquivo JSON e passe para `create-bulk`:

```json
{
  "issues": [
    {
      "summary": "feat: N:N CG e Filas",
      "projectKey": "AT",
      "issueType": "Task",
      "label": ["routing"],
      "assignee": "@me"
    },
    {
      "summary": "fix: vazamento de estado no chat",
      "projectKey": "AT",
      "issueType": "Bug",
      "assignee": "@me"
    }
  ]
}
```

```bash
~/.claude/tools/jira_write.py create-bulk /tmp/issues.json
```

Ou inline sem arquivo intermediario:

```bash
~/.claude/tools/jira_write.py create-from-json '{"issues": [...]}'
```

## Transicionar Status

```bash
~/.claude/tools/jira_write.py transition AT-400 "Done"
~/.claude/tools/jira_write.py transition AT-400 "In Progress"
```

## Atribuir Issue

```bash
~/.claude/tools/jira_write.py assign AT-400 "@me"
~/.claude/tools/jira_write.py assign AT-400 "user@example.com"
```

## Adicionar Comentário

```bash
~/.claude/tools/jira_write.py comment AT-400 "Deploy feito em staging, testado OK"
```

## Projeto Padrão

O board de Atendimento usa o projeto **AT**.

## Regra Obrigatória: Status Inicial

**SEMPRE** transicionar para "Ready to Dev" logo após criar a issue. Tasks no Backlog não aparecem no board downstream.

```bash
~/.claude/tools/jira_write.py create AT Tarefa "titulo" --assignee "@me"
~/.claude/tools/jira_write.py transition AT-XXX "Ready to Dev"
```

## Restrições

- Sempre confirmar com o usuario antes de criar issues (acao visivel para outros)
- Nao deletar issues sem autorizacao explicita
- Tipos de issue sao case-sensitive (Task, Bug, Story, Epic)
- Description em plain text (o acli converte para ADF automaticamente)
