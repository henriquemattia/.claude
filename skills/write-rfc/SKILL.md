---
name: write-rfc
description: Create RFC documents following the PROBE framework (Problema, Restricoes, Opcoes, Balanceamento, Execucao) used at PX organization. Use when documenting architectural decisions, new features, system changes, or technical proposals. Triggers on "create an RFC", "write an ADR", "document this decision", "RFC about...", "registrar decisao".
---

# Write RFC

Generate RFC documents following the PROBE framework used by PX squads in `px-center/px-docs`.

## Template Structure

Every RFC follows the PROBE framework:

```markdown
# RFC-NNN: {Titulo descritivo}

**Status:** Draft
**Autor:** @{github-username}
**Data:** YYYY-MM-DD

---

## (P)roblema

### Qual e o problema real vs o sintoma?

**Sintoma:** [O que parece estar errado]

**Problema real:** [A causa raiz], resultando em:
- [Consequencia 1]
- [Consequencia 2]

### O que acontece se NAO resolvermos?
[Lista de impactos de nao agir]

### Por que isso e problema AGORA?
[Por que resolver agora e nao depois]

---

## (R)estricoes

### Quanto tempo temos para resolver?
### Quais sistemas/APIs precisamos integrar?
### O que e nao-negociavel?

---

## (O)pcoes

### Opcao 1: Status Quo
### Opcao 2: [Abordagem recomendada]
### Opcao 3: [Alternativa]

Cada opcao segue: descricao, como funciona, em caso de erro, reversibilidade.

---

## (B)alanceamento

### Comparativo das Opcoes
[Tabela criterios x opcoes]

### Analise: [Opcao Recomendada]
- O que ganhamos
- O que perdemos
- Escala quanto
- Custo de manutencao

### Por que nao [Opcao X]?

---

## (E)xecucao

### Decisao: [Opcao escolhida]
[Detalhes tecnicos: modelo de dados, integracoes, permissoes, fluxos]

### Qual o primeiro passo concreto?
### Como sabemos que funcionou?
### Qual e o plano B?

### Riscos e Mitigacoes
| Risco | Probabilidade | Impacto | Mitigacao |
```

## Rules

### Language
- Portuguese (pt-BR) throughout
- Formal but clear — write for someone who wasn't in the room
- No jargon without explanation

### Header Format
- Title: `# RFC-NNN: {Titulo descritivo}`
- Bold metadata: `**Status:** Draft`, `**Autor:** @user`, `**Data:** YYYY-MM-DD`
- Horizontal rule `---` after header and between PROBE sections

### Status Values
| Status | When to use |
|--------|------------|
| `Draft` | Decisao ainda em discussao |
| `Accepted` | Decisao aprovada |
| `Rejected` | Decisao descartada |
| `Deprecated` | Decisao que nao se aplica mais |
| `Superseded by [XXX]` | Substituida por outra |

### PROBE Sections

**(P)roblema** — Start with the PROBLEM, not the solution
- "Sintoma vs Problema real" structure
- Include "O que acontece se NAO resolvermos?"
- Include "Por que isso e problema AGORA?"

**(R)estricoes** — Non-negotiables and constraints
- Timeframe, integrations needed, hard requirements

**(O)pcoes** — Always 2+ options, including Status Quo
- Each option: how it works, error handling, reversibility
- Code blocks or diagrams when helpful

**(B)alanceamento** — Comparative analysis
- Table comparing all options across criteria
- Explicit "why not X" for rejected options

**(E)xecucao** — The chosen path with concrete details
- Technical details (data model, APIs, permissions)
- First concrete step, success criteria, plan B
- Risks table with probability/impact/mitigation

## File Naming

Two contexts:

**In px-docs (cross-org visibility):**
```
docs/{squad}/{project}/RFCs/rfc-NNN-{slug}.md
```
Examples:
- `docs/ai-platform/cortex/RFCs/rfc-001-monorepo.md`
- `docs/customer-success/nexus/RFCs/rfc-001-cortex-feedback.md`

**In project repo (local reference):**
```
docs/rfc-{slug}.md
```
Examples:
- `docs/rfc-cortex-feedback-system.md`
- `docs/rfc-routing-engine-v2.md`

## px-docs PR Workflow

When creating an RFC in px-docs:
1. Check if the squad folder exists (`docs/{squad}/{project}/RFCs/`)
2. If not, create it following the pattern of existing squads (e.g., `ai-platform/cortex`)
3. Number the RFC sequentially within the squad (first = 001)
4. Create branch: `rfc/{slug}` or `docs/rfc-NNN-{slug}`
5. Create PR as **draft** — RFCs start as drafts for discussion

## Checklist Before Delivering

- [ ] Title follows `RFC-NNN: {Descriptive title}` format
- [ ] Header has Status, Autor, Data in bold
- [ ] All 5 PROBE sections present with content
- [ ] Problema starts with symptom, then root cause
- [ ] At least 2 options in Opcoes (including Status Quo)
- [ ] Balanceamento has comparison table
- [ ] Execucao has success criteria and risks table
- [ ] Horizontal rules between PROBE sections
- [ ] Language is pt-BR throughout
- [ ] File saved with correct naming convention

## Reference

The PROBE framework comes from `px-center/px-docs`:
- Examples: `docs/ai-platform/cortex/RFCs/rfc-001-*.md` through `rfc-013-*.md`
- Squad structure: `docs/{squad}/{project}/RFCs/`
