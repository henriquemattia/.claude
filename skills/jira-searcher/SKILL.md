---
name: jira-searcher
description: Consulta read-only de épicos e tasks no Jira do planejamento
---

# Jira Reader

Consulta dados do Jira Cloud via wrapper seguro (read-only).

## Ferramenta

```bash
~/.claude/tools/jira_read.py <action> <ISSUE-KEY>
```

**IMPORTANTE**: Sempre use o caminho absoluto `~/.claude/tools/jira_read.py`, não o caminho relativo.

## Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `issue <KEY>` | Detalhes completos de uma issue (todos os campos + custom fields) |
| `epic <KEY>` | Alias para `issue` (retrocompatível) |
| `epic-children <KEY>` | Lista tasks filhas de um épico |

## Custom Fields Mapeados

A tool traduz automaticamente custom fields para nomes legíveis:

| Campo Jira | Nome amigável | Descrição |
|------------|---------------|-----------|
| `customfield_10718` | `technicalDefinition` | Definição técnica da task |
| `customfield_10387` | `quarter` | Quarter (Q1-2026, etc) |
| `customfield_10585` | `developer` | Desenvolvedor atribuído |
| `customfield_11613` | `teams` | Times associados |

## Exemplos

```bash
# Ver detalhes completos de uma task (incluindo technical definition)
~/.claude/tools/jira_read.py issue AT-352

# Retrocompatível: 'epic' funciona igual a 'issue'
~/.claude/tools/jira_read.py epic PROJ-123

# Listar todas as tasks filhas de um épico
~/.claude/tools/jira_read.py epic-children PROJ-123
```

## Restrições

- Apenas leitura (sem criar, editar ou comentar)
- Formato de key: `PROJETO-NUMERO` (ex: PROJ-123, AT-352)
- Não usar `acli` diretamente
