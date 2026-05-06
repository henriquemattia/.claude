---
name: feature-docs-html
description: Use when creating standalone HTML documentation pages for features, flows, architecture, data models, or technical reference. Generates single-file dark-theme HTML with polished UI, SVG flowcharts, scroll animations, and responsive layout. Triggers on requests like "create an HTML doc", "document this flow", "generate visual docs", "make an HTML page about..."
---

# Feature Docs HTML

Generate beautiful, performant, single-file HTML documentation pages for features, flows, and technical reference.

## Design System

Every page MUST use this foundation:

### Color Palette (Tailwind Slate-based dark theme)

```css
:root {
  --bg: #0f172a;
  --surface: #1e293b;
  --surface-hover: #263548;
  --border: #334155;
  --text: #f8fafc;
  --text-sec: #94a3b8;
  --text-dim: #64748b;
  --blue: #3b82f6;
  --blue-light: #60a5fa;
  --green: #10b981;
  --green-light: #34d399;
  --amber: #f59e0b;
  --red: #ef4444;
  --red-light: #f87171;
  --purple: #8b5cf6;
  --purple-light: #a78bfa;
  --cyan: #06b6d4;
  --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
}
```

### Required Head Elements

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

## Page Structure

Every page follows this skeleton:

1. **Sticky nav** - logo + section anchors, backdrop-blur glass effect
2. **Hero** - gradient title (`linear-gradient(135deg, var(--blue-light), var(--purple-light))` with `background-clip: text`), subtitle, optional badge
3. **Sections** - each with `id` for nav anchors, uppercase label with icon, content cards
4. **Footer** - simple "PX Nexus - Documentacao interna"

### Nav Pattern

```css
nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(15, 23, 42, 0.88);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
}
```

### Section Title Pattern

```css
.section-title {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-dim);
  margin-bottom: 1.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}
```

## Card Components

### Standard Card

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  transition: all 0.25s ease;
}
.card:hover {
  background: var(--surface-hover);
  border-color: rgba(99,102,241,0.3);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
```

### Colored Accent Cards (for NEW, WARNING, etc.)

Use `rgba()` fills with low opacity for backgrounds, higher opacity for borders:
- Green (new): `fill="rgba(16,185,129,0.06)" stroke="rgba(16,185,129,0.35)"`
- Amber (warning): `fill="rgba(245,158,11,0.06)" stroke="rgba(245,158,11,0.25)"`
- Red (danger): `fill="rgba(239,68,68,0.06)" stroke="rgba(239,68,68,0.3)"`
- Purple (highlight): `fill="rgba(139,92,246,0.06)" stroke="rgba(139,92,246,0.35)"`

### Data Model Cards

```css
.model-card h4 {
  font-size: 0.82rem;
  padding: 0.85rem 1.15rem;
  border-bottom: 1px solid var(--border);
  color: var(--cyan);
  font-weight: 700;
}
.model-row {
  display: flex;
  padding: 0.6rem 1.15rem;
  border-bottom: 1px solid rgba(51,65,85,0.3);
  font-size: 0.78rem;
}
.model-col { font-family: var(--mono); color: var(--blue-light); }
.model-type { color: var(--purple-light); font-family: var(--mono); font-size: 0.72rem; }
```

## SVG Flowcharts

### Critical Rules

1. **viewBox MUST accommodate ALL content** - text extending beyond viewBox is silently clipped
2. **Calculate text width**: monospace ~7px/char at font-size 12, proportional ~6.5px/char
3. **Add 15-20% padding** to viewBox beyond rightmost/bottommost content
4. **Center flow nodes** in the middle of the viewBox, NOT at the left edge
5. **Branching labels** (like "NAO: ...") need extra viewBox width - measure the full text

### Node Styling

```svg
<!-- Standard node -->
<rect x="50" y="8" width="280" height="44" rx="10"
      fill="#1e293b" stroke="#334155" stroke-width="1"/>
<text x="190" y="27" text-anchor="middle" class="node-text" font-weight="600">Label</text>
<text x="190" y="41" text-anchor="middle" class="node-sub">sublabel</text>

<!-- Decision diamond -->
<polygon points="190,204 290,240 190,276 90,240"
         fill="rgba(245,158,11,0.06)" stroke="rgba(245,158,11,0.3)" stroke-width="1"/>

<!-- Edge/arrow -->
<line x1="190" y1="52" x2="190" y2="72" class="edge"/>

<!-- NEW badge -->
<rect x="260" y="10" width="32" height="14" rx="3" fill="#059669"/>
<text x="276" y="20" text-anchor="middle" class="new-tag">NEW</text>
```

### SVG Text Classes

```css
.node-text { font-family: var(--font); font-size: 12px; fill: var(--text); }
.node-sub  { font-family: var(--font); font-size: 10px; fill: var(--text-dim); }
.edge      { stroke: #334155; stroke-width: 1.5; fill: none; marker-end: url(#arrow); }
.edge-label { font-family: var(--font); font-size: 9px; font-weight: 700; }
```

### Arrow Markers (required defs)

```svg
<svg width="0" height="0">
  <defs>
    <marker id="arrow" viewBox="0 0 10 7" refX="10" refY="3.5"
            markerWidth="8" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 3.5 L 0 7 z" fill="#334155"/>
    </marker>
  </defs>
</svg>
```

## Animations

### Scroll-triggered fade-in (IntersectionObserver)

```css
.animated {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.animated.vis { opacity: 1; transform: translateY(0); }
```

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) e.target.classList.add('vis');
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.animated').forEach(el => observer.observe(el));
```

### Active nav tracking

```javascript
const navLinks = document.querySelectorAll('nav a');
const sections = document.querySelectorAll('section[id]');
const navObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      navLinks.forEach(l => l.classList.remove('active'));
      const link = document.querySelector(`nav a[href="#${e.target.id}"]`);
      if (link) link.classList.add('active');
    }
  });
}, { threshold: 0.3 });
sections.forEach(s => navObserver.observe(s));
```

## Content Types and When to Use

| Content | Component |
|---------|-----------|
| Step-by-step process | Timeline (vertical line + numbered dots) |
| Decision flow | SVG flowchart with diamonds |
| Data model / schema | Model cards with mono-font columns |
| Metrics / KPIs | Grid of metric cards with icons |
| Scenarios / use cases | Expandable cards or scenario cards with flow badges |
| SQL / code reference | Expandable accordion cards with syntax highlighting |
| Hierarchy / cascade | Indented node tree |
| Survey / form mockup | Styled form elements (non-functional, visual only) |

## Expandable Cards (for SQL, code, details)

```css
.sql-card-body { max-height: 0; overflow: hidden; transition: max-height 0.35s ease; }
.sql-card.open .sql-card-body { max-height: 2000px; }
.sql-card-header { cursor: pointer; user-select: none; }
.sql-card.open .chevron { transform: rotate(180deg); }
```

```html
<div class="sql-card">
  <div class="sql-card-header" onclick="this.parentElement.classList.toggle('open')">
    <h4>Title <span class="badge">type</span></h4>
    <span class="chevron">&#x25BC;</span>
  </div>
  <div class="sql-card-body"><div class="sql-card-content">
    <!-- content -->
  </div></div>
</div>
```

## SQL Syntax Highlighting (inline spans)

```html
<div class="sql-block">
  <span class="kw">SELECT</span> <span class="fn">COUNT</span>(*)
  <span class="kw">FROM</span> <span class="col">sessions</span>
  <span class="kw">WHERE</span> <span class="col">status</span> = <span class="str">'active'</span>
</div>
```

```css
.sql-block .kw  { color: var(--blue-light); }   /* keywords */
.sql-block .fn  { color: var(--amber); }         /* functions */
.sql-block .col { color: var(--green-light); }   /* columns/tables */
.sql-block .str { color: #f472b6; }              /* strings */
```

## Responsive Breakpoints

```css
@media (max-width: 900px) {
  .chart-container { flex-direction: column; align-items: center; }
  .chart-card { max-width: 100%; }
  .model-grid { grid-template-columns: 1fr; }
}
@media (max-width: 700px) {
  .wrap { padding: 0 1rem; }
  section { padding: 2.5rem 0; }
  .hero { padding: 4rem 1rem 2.5rem; }
}
```

## Performance Rules

1. **Single file** - everything in one `.html`, no external CSS/JS deps (except Google Fonts)
2. **No frameworks** - vanilla CSS + JS only
3. **Minimal JS** - only IntersectionObserver and toggle handlers
4. **CSS variables** - all colors via `var()` for easy theming
5. **SVG over images** - all diagrams as inline SVG, never raster
6. **Lazy animations** - IntersectionObserver, not on-load

## Checklist Before Delivering

- [ ] Google Fonts loaded with `preconnect`
- [ ] All CSS via variables (no hardcoded colors in HTML)
- [ ] Sticky nav with section links that work
- [ ] Hero with gradient title
- [ ] All cards have hover transitions
- [ ] Scroll animations on visible elements
- [ ] SVG viewBox wide enough for ALL text (especially branching labels)
- [ ] Responsive at 700px and 900px breakpoints
- [ ] Footer present
- [ ] File opens correctly standalone (no server needed)
