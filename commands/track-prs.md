---
description: Analisa PRs mergeados sem task Jira e gera relatorio para criacao de tasks
argument-hint: "[dias-atras] (default: 7)"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Track Untracked PRs

Analise PRs mergeados por mim no repositorio atual que nao possuem task Jira rastreada e gere um relatorio para revisao.

## Passos

1. **Determinar periodo**: Use o argumento como numero de dias para buscar (default: 7). Calcule a data inicial.

2. **Listar PRs mergeados**: Execute `gh pr list --author=@me --state=merged --search="merged:>=YYYY-MM-DD" --json number,title,mergedAt,url,body,additions,deletions,changedFiles --limit 50`

3. **Identificar PRs com key Jira explicita**: Um PR esta diretamente rastreado se:
   - O titulo contem uma key Jira (pattern: `[A-Z]+-\d+`, ex: AT-352, PROJ-123)
   - OU o body menciona uma key Jira
   - PRs de revert (titulo comeca com "Revert") devem ser ignorados
   - PRs puramente de merge (titulo comeca com "Merge") devem ser ignorados

4. **Cruzar com Jira via jira-searcher**: Para PRs que mencionam uma key Jira, validar se a task realmente existe usando a skill `jira-searcher` (tool em `~/.claude/tools/jira_read.py`):
   - `~/.claude/tools/jira_read.py issue AT-XXX` para confirmar que a task existe
   - Se a key referenciada for um Epic, verificar se existe uma sub-task correspondente ao PR usando `~/.claude/tools/jira_read.py epic-children AT-XXX`
   - PRs que referenciam apenas o Epic pai (ex: AT-352) sem sub-task propria devem ser considerados **nao rastreados** (o Epic e a iniciativa, nao a task individual)

5. **Agrupar por tipo**: Baseado no prefixo convencional do titulo:
   - `feat:` ou `feat(...):`  → Tipo Jira: **Tarefa**
   - `fix:` ou `fix(...):`  → Tipo Jira: **Bug**
   - `perf:`, `refactor:`, `chore:`, `ci:`, `test:`, `docs:` → Tipo Jira: **Tarefa**
   - Sem prefixo → inferir do conteudo

6. **Gerar relatorio**: Crie o arquivo `tasks-pendentes.md` na raiz do repositorio com:

```markdown
# PRs sem task Jira — [data inicio] a [data fim]

> Gerado automaticamente via `/track-prs`. Revise e remova o que nao quiser criar.

## Resumo

| Total PRs mergeados | Com task Jira | Sem task Jira |
|---------------------|---------------|---------------|
| X                   | Y             | Z             |

## Tasks sugeridas

### 1. [Titulo limpo sem prefixo convencional]

**Titulo Jira:** `[prefixo]: [descricao]`
**Tipo:** Tarefa | Bug
**Descricao:** [Extrair do body do PR, resumir em 2-3 frases]
**PR:** #NNN | **Merge:** DD/MMM HH:mm | **Impacto:** +X / -Y / Z arquivos

---

[repetir para cada PR sem task]
```

7. **Apresentar resultado**: Mostre ao usuario quantos PRs sem task foram encontrados e o caminho do arquivo gerado. Pergunte se quer criar as tasks no Jira.

8. **Criacao de tasks (se o usuario aprovar)**: Use a skill `jira-creator` (tool em `~/.claude/tools/jira_write.py`) para criar as tasks. Para cada task no relatorio:
   - `~/.claude/tools/jira_write.py create AT <TIPO> "<TITULO>" --description "<DESCRICAO>" --assignee "@me"` onde TIPO e "Tarefa" para feat/perf/refactor/chore/ci/test/docs ou "Bug" para fix
   - `~/.claude/tools/jira_write.py transition AT-XXX "Ready to Dev"` (obrigatorio apos criacao)
   - Mostre a tabela final com key, tipo e titulo de cada task criada

## Regras

- NAO crie tasks no Jira sem aprovacao do usuario — gere o relatorio primeiro, pergunte, e so crie se o usuario confirmar
- Datas no formato brasileiro (DD/MMM)
- Descricoes em portugues
- Se todos os PRs ja tem task, informe e nao gere arquivo
- Se o arquivo `tasks-pendentes.md` ja existir, sobrescreva
- Sempre usar `~/.claude/tools/jira_write.py` (caminho absoluto) para interagir com Jira
- Sempre transicionar para "Ready to Dev" imediatamente apos criar cada task
- Tipo Jira e PT-BR e case-sensitive: "Tarefa", "Bug", "Historia", "Epic"
