# FOR_AGENTS.md — Piano operativo per gli agenti · reflexora.ai

> **Documento vivo.** È la fonte di verità per la costruzione del sito **reflexora.ai**.
> Contiene architettura, design system, contenuti e l'elenco completo dei task da eseguire,
> ciascuno assegnato a un agente specifico.
> Ambiente di lavoro degli agenti: **Antigravity** (modelli disponibili: **Gemini**,
> **Claude Sonnet**, **Claude Opus 4.6**).

---

## 0. REGOLE OPERATIVE (leggere sempre prima di agire)

Queste regole valgono per **ogni** agente, a **ogni** intervento.

1. **Aggiorna questo file dopo OGNI azione completata.** Non a fine sessione: dopo ogni singolo
   task. È la regola più importante del documento.
   - Cambia lo stato del task nella tabella di fase: `[ ]` → `[~]` (in corso) → `[x]` (fatto).
   - Compila le colonne **Agente** (chi ha eseguito) e **Data** (formato `AAAA-MM-GG`).
   - Aggiungi una riga al **§13 Changelog** con: data, agente, task ID, sintesi di 1 riga.
   - Aggiorna la **dashboard §11** (contatore completati).
   - Se un task viene diviso, aggiungi i sotto-task numerati (es. `T-5.2a`, `T-5.2b`).
2. **Un commit git per task** (o per gruppo logico), con messaggio in inglese:
   `type(scope): summary` es. `feat(seo): add JSON-LD Organization schema`.
   Non fare push automatici su rami condivisi senza che sia richiesto.
3. **Non inventare fatti.** Numeri di brevetto, claim scientifici, date, nomi: usare solo ciò
   che è in `per testi/` o esplicitamente confermato. In caso di dubbio, marcare `⚠️ DA VERIFICARE`
   nel codice con un commento HTML e segnalarlo nel Changelog.
4. **Rispetta il design system** (§5). Nessun colore/font/spaziatura fuori dai token definiti.
5. **Zero dipendenze runtime bloccanti.** Il sito resta statico (HTML/CSS/JS vanilla). Nessun
   framework JS lato client, nessuna CDN esterna obbligatoria (vedi §5.6 e §9 — hosting Aruba).
6. **Se un task tocca contenuti scientifici o corporate**, la fonte autorevole è
   `per testi/REFLEXORA_Corporate_Positioning_and_Website_Revision.docx` (10 luglio 2026):
   è la revisione più recente e prevale sui testi precedenti.
7. **Non lasciare mai il sito rotto tra un task e l'altro.** Ogni commit deve produrre un sito
   che carica e naviga.

### Legenda stato
| Simbolo | Significato |
|---|---|
| `[ ]` | Da fare |
| `[~]` | In corso |
| `[x]` | Completato |
| `[!]` | Bloccato / serve decisione umana (spiegare nel Changelog) |

---

## 1. OBIETTIVI DEL SITO

reflexora.ai è la vetrina digitale di **REFLEXORA**, la divisione di ricerca di **IFEVS**
dedicata all'architettura **Reflex–Policy** per la Physical & Spatial AI, in traiettoria verso
società indipendente. Il sito deve parlare a tre pubblici, in quest'ordine di priorità:

1. **Investitori / partner industriali** → credibilità, IP protetta, traiettoria societaria.
2. **Comunità scientifica** → paper, preprint, terminologia, priorità concettuale.
3. **Motori di ricerca e motori generativi (LLM)** → SEO **e GEO** (essere trovati *e* citati
   dagli assistenti AI).

**Principi guida del progetto**
- Chiarezza deep-tech, non hype. Tono sobrio, autorevole, "claim discipline" (§7 del docx:
  usare il denominatore più conservativo finché la validazione sperimentale non è consolidata).
- Performance e accessibilità come requisiti, non optional.
- Manutenibilità: le sezioni che cambiano (IP, pubblicazioni) devono essere facili da aggiornare.

---

## 2. ASSEGNAZIONE DEGLI AGENTI

Regola economica (indicata dal committente): **Gemini ha molti crediti gratuiti → usarlo per il
lavoro semplice e ripetitivo.** Riservare **Opus** ai task ad alto valore/ragionamento
(SEO, GEO, schema, contenuti, architettura decisionale, review finale). **Sonnet** per la fascia
intermedia (JS, componenti, refactor con giudizio, QA).

| Agente | Usare per | Esempi di task |
|---|---|---|
| **Gemini** (economico, volume) | Lavoro meccanico, scaffolding, ripetizione, conversioni | Boilerplate HTML delle pagine, estrazione/impaginazione contenuti, self-hosting font, `robots.txt`/`sitemap.xml`, compressione immagini, `.htaccess` boilerplate, fix di accessibilità meccanici (alt, label), responsive tweak guidati |
| **Claude Sonnet** (intermedio) | Logica e giudizio moderati | JavaScript interattività, componenti UI riutilizzabili, refactor CSS, QA cross-browser, form contatti, 404, cookie banner |
| **Claude Opus 4.6** (alto valore) | Ragionamento, strategia, testo, correttezza | **SEO** tecnico e strategico, **GEO/AEO**, **JSON-LD schema**, `llms.txt`, meta description e copy, gerarchia informativa, glossario/entità, **review finale** di ogni fase |

> Ogni task nelle tabelle di fase ha già l'agente consigliato nella colonna **Agente cons.**
> Se un agente ritiene che un altro sia più adatto, può riassegnare **annotandolo nel Changelog**.

---

## 3. ARCHITETTURA DEL SITO

### 3.1 Strategia: single-page forte + pagine di profondità
La home resta una **single-page** persuasiva (ideale per un'iniziativa pre-società). Attorno,
poche **pagine dedicate** per i contenuti che (a) vanno aggiornati nel tempo e (b) danno
profondità SEO/GEO. Niente over-engineering.

### 3.2 Mappa delle pagine
```
/                     index.html         Home (hero + sezioni sintetiche, molti link interni)
/architecture         architecture.html  Approfondimento Reflex–Policy (event-to-action, bounded authority…)
/technology           technology.html    Complementarità tecnologica, spintronica, decision–power isolation
/applications         applications.html  Domini applicativi (robotica, mobility, PV, storage, edge/IoT)
/research             research.html      Fondamento scientifico: perspective papers, preprint, terminologia
/patents              patents.html       Brevetti & IP — pagina mantenuta/aggiornata separatamente
/company              company.html       Evoluzione corporate, rapporto con IFEVS, traiettoria societaria
/contact              contact.html       Contatti / partnership
/privacy              privacy.html       Privacy policy (GDPR)
/cookie-policy        cookie-policy.html Cookie policy (GDPR)
/404                  404.html           Pagina di errore
```
> URL "puliti" senza `.html`: gestiti via `.htaccess` su Aruba/Apache (§9). Standardizzare i link
> interni su **percorsi assoluti senza estensione** e lasciare che `.htaccess` mappi.

### 3.3 Struttura delle directory (target)
```
REFLEXORA.AI/
├── index.html
├── architecture.html
├── technology.html
├── applications.html
├── research.html
├── patents.html
├── company.html
├── contact.html
├── privacy.html
├── cookie-policy.html
├── 404.html
│
├── llms.txt                 # GEO: guida per i motori generativi
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── .htaccess                # HTTPS, www→non-www, URL puliti, header, cache, 404
│
├── css/
│   ├── styles.css           # design system + base
│   └── (opz.) pages.css     # stili specifici pagina, se serve
├── js/
│   └── main.js              # nav, reveal, cookie banner, form
├── fonts/                   # font self-hosted (woff2) — NO Google Fonts esterno
├── images/
│   ├── og/                  # immagini Open Graph (1200×630)
│   ├── icons/               # favicon, touch icon, safari-pinned
│   └── ...                  # asset visivi (webp/avif + fallback)
├── partials/                # (opz.) header/footer condivisi — vedi §3.4
│
├── for_agents.md            # QUESTO documento
└── per testi/               # fonti di contenuto (NON pubblicare) — vedi §3.5
```

### 3.4 Gestione header/footer condivisi (DRY)
Con più pagine, header e footer si ripetono. Il sito è statico su Aruba, quindi **non** c'è build
server. Due opzioni ammesse:
- **A (preferita, zero-JS):** mantenere `partials/header.html` e `partials/footer.html` come
  **fonte** e copiarli in ogni pagina; un piccolo script Node opzionale (`build.mjs`) può fare
  l'inline in locale prima del deploy. Semplice, nessun costo runtime.
- **B (JS fallback):** includere header/footer via `fetch()` in `main.js`. Ammesso solo con
  fallback statico per no-JS e crawler (peggiore per SEO → **sconsigliato**).

**Decisione di default: opzione A.** Fino al build script, gli agenti duplicano header/footer
mantenendo i due partial come riferimento canonico.

### 3.5 `per testi/` — sorgenti, non pubblicabili
La cartella `per testi/` contiene i documenti di lavoro (docx, pdf, txt). **Non deve essere
pubblicata** né indicizzata: escluderla dal deploy FTP e da `robots.txt`/sitemap. È solo fonte.

---

## 4. MAPPA DEI CONTENUTI (fonte → pagina)

Fonte autorevole: `per testi/REFLEXORA_Corporate_Positioning_and_Website_Revision.docx`.
Il §8 di quel documento ("Recommended website copy") fornisce il copy ufficiale. Usarlo verbatim
dove indicato, adattando solo per web (heading, liste).

| Pagina | Contenuti chiave | Fonte |
|---|---|---|
| Home | Hero + supporting line, "What REFLEXORA is", "Why Reflex–Policy", "A complementary architecture", "What the architecture enables", teaser applicazioni/IP, closing statement | docx §8 |
| Architecture | Event-to-action partitioning, Bounded authority, Measured closure, Compact observability, Energy proportionality (EROIE), World model as teacher | docx §4 |
| Technology | Complementarità (neuromorfico/spintronico/in-memory/analog/digitale), binary vs multilevel spintronics, Decision–Power Path Isolation, World Models as Teachers | docx §5 + Overview.txt |
| Applications | Robotica & humanoids, automotive/autonomous, energy harvesting (PV shadow), energy storage (battery reflex), edge & IoT | docx "Application domains" + Overview.txt |
| Research | Due Perspective paper, preprint su Preprints.org, terminologia, agenda di ricerca. **Claim discipline** (§7 docx: risultati = simulazioni/stime finché non validati) | docx §6, §7 |
| Patents & IP | **12 domande di brevetto italiane, 2 EPO, 1 PCT** (tutte "deposited applications", non concesse). Tabella con status, aggiornabile. ⚠️ Rimuovere il vecchio "8 patent families". | docx §2, §8 |
| Company | REFLEXORA = divisione di ricerca IFEVS; posizionamento per investimento; transizione a società indipendente. Paragrafo corporate autorevole = docx §12. Rapporto con IFEVS (ifevs.com) | docx §2, §8, §12 |
| Contact | Email `contact@reflexora.ai`, invito partnership | index attuale |

**Correzioni fattuali obbligatorie (docx §2):**
- ❌ NON dire che REFLEXORA è già società indipendente → ✅ "research division of IFEVS … intended to become an independent company".
- ❌ Rimuovere ogni riferimento a "eight patents / patent families" → ✅ portfolio 12 IT + 2 EPO + 1 PCT, tutte *deposited applications*.

---

## 5. DESIGN SYSTEM

Base di partenza già in `css/styles.css` (dark theme premium). Va **consolidata in token** e
irrobustita. Non introdurre stili ad-hoc inline nelle nuove pagine: usare classi/utility.

### 5.1 Colori (token confermati)
```
--bg-dark:       #070a13    /* sfondo principale */
--bg-darker:     #040609    /* nav scrolled, footer */
--bg-card:       rgba(15,23,42,0.6)
--text-primary:  #f8fafc
--text-secondary:#94a3b8
--accent-cyan:   #00f2fe
--accent-blue:   #4facfe
--accent-purple: #8b5cf6
--glass-border:  rgba(255,255,255,0.08)
```
> **Accessibilità (WCAG AA):** verificare che `--text-secondary` su `--bg-dark` raggiunga ≥ 4.5:1
> per testo normale. Non usare mai testo `--accent-cyan` piccolo su sfondo scuro senza verificare
> il contrasto (task T-9.2).

### 5.2 Tipografia
- Heading: **Outfit** (400/700/900). Body: **Inter** (300/400/600/800).
- **Self-hostare** i font (§5.6) in `woff2`. Scala tipografica fluida con `clamp()`
  (es. h1 `clamp(2.5rem, 6vw, 4.5rem)`), non dimensioni fisse.

### 5.3 Spaziatura & layout
- Scala di spaziatura basata su 4/8px (token `--space-1…-12`).
- Container max `1200px`, padding laterale `2rem` (mobile `1.25rem`).
- Griglie con CSS Grid (`grid-2-col`, `grid-3-col`) già presenti → estendere con `minmax()`.

### 5.4 Componenti (catalogo)
Definire/riordinare come classi riutilizzabili: `navbar`, `btn-primary`/`btn-secondary`/`btn-primary-sm`,
`glass-card`, `card`, `app-card`, `badge`, `section-title`, `features-list`, `hero-visual` (neural
sphere), `crossbar-grid`. Ogni nuova pagina compone **solo** da questo catalogo.

### 5.5 Motion & accessibilità
- Mantenere reveal-on-scroll (IntersectionObserver) e micro-animazioni.
- **Obbligatorio** `@media (prefers-reduced-motion: reduce)` che disattiva animazioni/parallax.
- Focus visibile su tutti gli elementi interattivi (`:focus-visible`), skip-link "Skip to content".

### 5.6 Font self-hosting (perché è un task, non un dettaglio)
Il sito oggi carica Google Fonts da `fonts.googleapis.com`. Su Aruba (UE) questo è (a) una
dipendenza esterna che rallenta il primo render e (b) un tema **GDPR** (trasferimento IP a Google).
→ Scaricare Outfit/Inter, convertirli in `woff2`, servirli da `/fonts`, `@font-face` con
`font-display: swap`, e **rimuovere** i `<link>` a Google Fonts.

---

## 6. FASI DI LAVORO — INDICE
- **Fase 0** — Setup & housekeeping repo
- **Fase 1** — Architettura multi-pagina & partial condivisi
- **Fase 2** — Consolidamento design system
- **Fase 3** — Contenuti per pagina
- **Fase 4** — Performance (font, immagini, asset)
- **Fase 5** — SEO tecnico
- **Fase 6** — GEO / AEO (ottimizzazione per motori generativi)
- **Fase 7** — Legal / GDPR
- **Fase 8** — Deployment Aruba
- **Fase 9** — QA, accessibilità, test
- **Fase 10** — Launch checklist

> **Ordine consigliato:** 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 9 → 8 → 10.
> Le fasi 5/6/7 possono procedere in parallelo alla 3 una volta stabile la struttura.

---

## Fase 0 — Setup & housekeeping

| ID | Stato | Agente cons. | Task | Criterio di completamento | Agente | Data |
|---|---|---|---|---|---|---|
| T-0.1 | [x] | Gemini | Aggiungere `.gitignore` (`.DS_Store`, `node_modules/`, `*.log`, `/dist`) e rimuovere `.DS_Store` dal tracking | `git status` pulito, `.DS_Store` non più tracciato | Gemini | 2026-07-11 |
| T-0.2 | [x] | Gemini | Creare cartelle mancanti: `fonts/`, `images/og`, `images/icons`, `partials/` (con `.gitkeep`) | Cartelle presenti | Gemini | 2026-07-11 |
| T-0.3 | [ ] | Sonnet | Definire `build.mjs` opzionale per inline dei partial (§3.4 opzione A) — **solo scaffold**, documentato | Script che copia header/footer nelle pagine | | |
| T-0.4 | [ ] | Opus | Rivedere e confermare mappa pagine (§3.2) e mappa contenuti (§4) rispetto al docx; segnalare gap | Nota di conferma nel Changelog | | |

---

## Fase 1 — Architettura multi-pagina & partial

| ID | Stato | Agente cons. | Task | Criterio di completamento | Agente | Data |
|---|---|---|---|---|---|---|
| T-1.1 | [ ] | Gemini | Estrarre header (navbar) e footer attuali in `partials/header.html` e `partials/footer.html` | I due partial rendono identici all'attuale index | | |
| T-1.2 | [ ] | Gemini | Aggiornare la navbar: link a tutte le pagine (§3.2), stato "active" per pagina corrente, menu mobile hamburger | Nav funziona su desktop e mobile, evidenzia pagina corrente | | |
| T-1.3 | [ ] | Gemini | Creare gli scheletri HTML di `architecture/technology/applications/research/patents/company/contact` con header/footer inclusi e `<main>` vuoto | 7 pagine caricano con nav+footer, nessun 404 interno | | |
| T-1.4 | [ ] | Sonnet | Rifattorizzare `index.html`: sezioni sintetiche che rimandano alle pagine dedicate (CTA "Learn more →") | Home coerente, ogni sezione linka alla pagina di profondità | | |
| T-1.5 | [ ] | Gemini | Aggiungere skip-link "Skip to content" e landmark ARIA (`<header> <nav> <main> <footer>`) | Skip-link funzionante, landmark presenti su ogni pagina | | |
| T-1.6 | [ ] | Sonnet | Creare `404.html` in tema, con link di rientro | Pagina 404 stilizzata, testata via URL inesistente | | |

---

## Fase 2 — Consolidamento design system

| ID | Stato | Agente cons. | Task | Criterio di completamento | Agente | Data |
|---|---|---|---|---|---|---|
| T-2.1 | [ ] | Sonnet | Consolidare i token in `:root` (colori §5.1, spaziatura §5.3, radius, ombre, z-index) | Nessun valore "magico" ripetuto nel CSS delle sezioni | | |
| T-2.2 | [ ] | Sonnet | Introdurre scala tipografica fluida con `clamp()` per h1–h4 e body | Tipografia scala senza scatti tra 320px e 1920px | | |
| T-2.3 | [ ] | Gemini | Sostituire gli stili inline presenti in `index.html` con classi/utility | Zero `style="..."` non giustificati nelle pagine | | |
| T-2.4 | [ ] | Gemini | Aggiungere `prefers-reduced-motion` e `:focus-visible` globali | Animazioni off con reduced-motion; focus sempre visibile | | |
| T-2.5 | [ ] | Opus | Review design system: coerenza, gerarchia visiva, densità, "claim discipline" visiva (niente over-promise grafico) | Nota di review + eventuali fix nel Changelog | | |

---

## Fase 3 — Contenuti per pagina

> Copy verbatim dal docx §8 dove indicato; adattare in heading/liste per il web. Applicare le
> **correzioni fattuali** (§4). Lingua del sito: **inglese**.

| ID | Stato | Agente cons. | Task | Criterio di completamento | Agente | Data |
|---|---|---|---|---|---|---|
| T-3.1 | [ ] | Gemini | Impaginare **Home** con il copy docx §8 (hero, what is, why, complementary, enables, closing) | Home completa, testo = docx, link interni attivi | | |
| T-3.2 | [ ] | Opus | Redigere **Architecture** dai 6 tratti distintivi (docx §4) con struttura scan-friendly + micro-diagrammi CSS | Pagina chiara, terminologia coerente, nessun claim non supportato | | |
| T-3.3 | [ ] | Opus | Redigere **Technology** (complementarità, binary vs multilevel spintronics, decision–power isolation) | Distinzioni tecniche corrette, tono sobrio | | |
| T-3.4 | [ ] | Gemini | Impaginare **Applications** (5 domini) come griglia di card | 5 card con testo da fonte | | |
| T-3.5 | [ ] | Opus | Redigere **Research** con la **claim discipline** (risultati = simulazioni/stime), lista Perspective paper + preprint, glossario (EROIE, Reflex Layer, Policy Layer, event-action trace) | Nessun over-claim; glossario presente (utile anche per GEO) | | |
| T-3.6 | [ ] | Opus | Costruire **Patents & IP**: intro + **tabella** (tipo, giurisdizione, status "deposited", ambito) per 12 IT + 2 EPO + 1 PCT, con nota "applications, not granted" e blocco "last updated" | Tabella aggiornabile, wording conforme docx §2 | | |
| T-3.7 | [ ] | Opus | Redigere **Company**: paragrafo corporate autorevole (docx §12), rapporto con IFEVS, traiettoria societaria | Testo = docx §12, link a ifevs.com | | |
| T-3.8 | [ ] | Sonnet | **Contact**: form (nome, email, messaggio) + email diretta; senza backend → `mailto:` o servizio form statico (es. Formspree) **con consenso** | Form usabile, privacy-safe, nessun dato in querystring | | |
| T-3.9 | [ ] | Opus | Pass editoriale finale su tutte le pagine: coerenza terminologica, tono, "claim discipline", correzioni fattuali applicate | Checklist coerenza spuntata nel Changelog | | |

---

## Fase 4 — Performance

| ID | Stato | Agente cons. | Task | Criterio di completamento | Agente | Data |
|---|---|---|---|---|---|---|
| T-4.1 | [ ] | Gemini | **Self-hostare i font** (Outfit, Inter → woff2 in `/fonts`), `@font-face` con `font-display: swap`, rimuovere i `<link>` Google Fonts | Nessuna richiesta a `fonts.googleapis.com`; testo renderizza | | |
| T-4.2 | [ ] | Gemini | Ottimizzare immagini: convertire in `webp`/`avif`, `width`/`height` espliciti, `loading="lazy"` sotto la piega, `<picture>` con fallback | Nessuna immagine sovradimensionata; niente layout shift | | |
| T-4.3 | [ ] | Gemini | Aggiungere `preload` per font critici e CSS; `preconnect` solo a domini realmente usati | Lighthouse: nessun warning su risorse critiche | | |
| T-4.4 | [ ] | Sonnet | Minificare CSS/JS per il deploy (sorgenti leggibili in repo; output in `/dist` o via gzip/br `.htaccess`) | Asset minificati in produzione | | |
| T-4.5 | [ ] | Opus | Budget performance & review Lighthouse (target Perf ≥ 90, Best Practices ≥ 95) | Report Lighthouse nel Changelog | | |

---

## Fase 5 — SEO tecnico  ·  (Opus guida, Gemini esegue il meccanico)

| ID | Stato | Agente cons. | Task | Criterio di completamento | Agente | Data |
|---|---|---|---|---|---|---|
| T-5.1 | [ ] | Opus | `<title>` e `meta description` unici per **ogni** pagina (≤ 60 / ≤ 155 char) | 10 pagine con title+description distinti | | |
| T-5.2 | [ ] | Opus | **Open Graph** + **Twitter Card** per ogni pagina + immagini OG 1200×630 in `images/og` | Anteprima social corretta (validata) | | |
| T-5.3 | [ ] | Gemini | `robots.txt` (consenti tutto tranne `per testi/`, `partials/`, `/dist`; punta a sitemap) | robots valido, `per testi/` esclusa | | |
| T-5.4 | [ ] | Gemini | `sitemap.xml` con tutte le pagine pubbliche + `lastmod` | Sitemap valida, referenziata in robots | | |
| T-5.5 | [ ] | Opus | **Canonical** per pagina; decidere `www` vs non-`www` (default **non-www**) e coerenza | Ogni pagina ha canonical assoluto https | | |
| T-5.6 | [ ] | Opus | **JSON-LD**: `Organization` (REFLEXORA, sameAs IFEVS/LinkedIn), `WebSite`, `BreadcrumbList` per pagina | Structured data valido (Rich Results Test) | | |
| T-5.7 | [ ] | Opus | JSON-LD `ScholarlyArticle`/`CreativeWork` per Perspective paper/preprint su Research | Paper marcati, validi | | |
| T-5.8 | [ ] | Gemini | Favicon set + `site.webmanifest` + apple-touch-icon + theme-color | Icone corrette su browser/mobile | | |
| T-5.9 | [ ] | Opus | Gerarchia heading (un solo `<h1>`/pagina), alt descrittivi, link interni sensati | Audit heading/alt senza errori | | |

---

## Fase 6 — GEO / AEO (Generative / Answer Engine Optimization)  ·  **Opus**

> Obiettivo: far sì che ChatGPT, Claude, Gemini, Perplexity ecc. **capiscano e citino** REFLEXORA
> correttamente. La GEO premia contenuti fattuali, strutturati, con entità chiare e definizioni.

| ID | Stato | Agente cons. | Task | Criterio di completamento | Agente | Data |
|---|---|---|---|---|---|---|
| T-6.1 | [ ] | Opus | Creare **`llms.txt`** (root): descrizione sintetica di REFLEXORA, glossario entità, elenco pagine con 1-riga, fatti chiave (IP 12+2+1, divisione IFEVS), contatto | `llms.txt` raggiungibile, accurato, allineato alle correzioni §4 | | |
| T-6.2 | [ ] | Opus | Sezione **FAQ** (Home o Research) con `FAQPage` JSON-LD: "What is Reflex–Policy?", "Is REFLEXORA a company?", "What is EROIE?", "How many patents?" | FAQ visibile + schema valido, risposte fattuali | | |
| T-6.3 | [ ] | Opus | **Definizioni di entità** citabili: glossario per Reflex Layer, Policy Layer, EROIE, event-action trace, world model — frasi autoconclusive (estraibili dagli LLM) | Ogni termine ha definizione di 1–2 frasi indipendente dal contesto | | |
| T-6.4 | [ ] | Opus | Struttura "answer-first": ogni pagina apre con abstract di 2–3 frasi che risponde alla domanda implicita | Abstract in cima a ogni pagina di contenuto | | |
| T-6.5 | [ ] | Opus | Coerenza di **naming e claim** tra sito, `llms.txt`, JSON-LD e docx (una sola versione dei fatti) | Nessuna discrepanza tra le fonti pubbliche | | |
| T-6.6 | [ ] | Opus | `sameAs`/entità: collegare REFLEXORA↔IFEVS↔dominio↔profili (LinkedIn) per grounding degli LLM | Grafo di entità coerente nei JSON-LD | | |

---

## Fase 7 — Legal / GDPR

| ID | Stato | Agente cons. | Task | Criterio di completamento | Agente | Data |
|---|---|---|---|---|---|---|
| T-7.1 | [ ] | Opus | Redigere **Privacy Policy** (titolare, dati dal form, base giuridica, diritti, contatto). ⚠️ Bozza tecnica — **richiede validazione legale umana** prima del go-live | Pagina completa, marcata `[!]` finché non validata | | |
| T-7.2 | [ ] | Opus | Redigere **Cookie Policy** coerente con gli strumenti effettivi (analytics?) | Pagina coerente con gli script realmente usati | | |
| T-7.3 | [ ] | Sonnet | **Cookie banner** minimale (accetta/rifiuta non essenziali); nessun cookie non essenziale prima del consenso | Banner funzionante, default privacy-preserving | | |
| T-7.4 | [ ] | Sonnet | Analytics **privacy-friendly** (Plausible/Umami self-host o GA4 dietro consenso). Default: **Plausible** (no cookie) | Analytics attivo solo secondo consenso | | |

---

## Fase 8 — Deployment Aruba

> Aruba hosting Linux/Apache. Deploy via **FTP/SFTP**. Dominio finale: **reflexora.ai** (HTTPS).

| ID | Stato | Agente cons. | Task | Criterio di completamento | Agente | Data |
|---|---|---|---|---|---|---|
| T-8.1 | [ ] | Gemini | `.htaccess`: forza **HTTPS**, redirect `www`→non-www (coerente con T-5.5), **URL puliti** (rimozione `.html`), `ErrorDocument 404 /404.html` | Regole testate in locale/staging | | |
| T-8.2 | [ ] | Gemini | `.htaccess`: **cache** (Expires/Cache-Control statici), **compressione** gzip/brotli | Header cache/compressione presenti | | |
| T-8.3 | [ ] | Sonnet | `.htaccess`: **security header** (`X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`/`frame-ancestors`, `Content-Security-Policy` — pulita grazie al self-host) | Header verificati (securityheaders.com) | | |
| T-8.4 | [ ] | Gemini | Definire il **set di file da caricare** (escludere `per testi/`, `for_agents.md`, `partials/` sorgente, `.git`, `node_modules`) | Lista/`.deployignore` documentata | | |
| T-8.5 | [ ] | Opus | Checklist pre-deploy: DNS/SSL Aruba attivi, canonical/sitemap con dominio finale, robots non in `Disallow: /` | Checklist spuntata nel Changelog | | |
| T-8.6 | [!] | — (umano) | **Upload FTP e attivazione SSL** su Aruba: azione con credenziali → **la esegue l'umano**, non l'agente | Sito live su https://reflexora.ai | | |

> ⚠️ **T-8.6 è umano.** Gli agenti non inseriscono credenziali FTP/hosting. Preparano il pacchetto
> e le istruzioni; il caricamento finale lo fa il committente (o con supervisione).

---

## Fase 9 — QA, accessibilità, test

| ID | Stato | Agente cons. | Task | Criterio di completamento | Agente | Data |
|---|---|---|---|---|---|---|
| T-9.1 | [ ] | Sonnet | Test responsive: 320 / 375 / 768 / 1024 / 1440 / 1920 px su tutte le pagine | Nessun overflow orizzontale, layout integro | | |
| T-9.2 | [ ] | Gemini | Verifica contrasto colori (WCAG AA) su tutte le combinazioni testo/sfondo | Tutte le coppie ≥ 4.5:1 (o 3:1 large) o corrette | | |
| T-9.3 | [ ] | Sonnet | Navigazione da tastiera + screen reader (landmark, alt, label form, focus order) | Percorso tastiera completo senza trappole | | |
| T-9.4 | [ ] | Gemini | Link check: nessun link interno rotto, tutti gli esterni `rel="noopener"` | 0 link rotti | | |
| T-9.5 | [ ] | Sonnet | Cross-browser: Chrome, Firefox, Safari (+ iOS), Edge | Render coerente | | |
| T-9.6 | [ ] | Opus | **Review finale integrata**: SEO + GEO + contenuti + accessibilità + performance. Firma la go-live readiness | Report finale nel Changelog | | |

---

## Fase 10 — Launch checklist (gate finale)

- [ ] Tutte le correzioni fattuali applicate (no "già società", no "8 brevetti") — §4
- [ ] Font self-hosted, nessuna chiamata esterna non necessaria
- [ ] `title`/`description`/OG/canonical unici per pagina
- [ ] JSON-LD valido (Organization, WebSite, BreadcrumbList, FAQ, articoli)
- [ ] `llms.txt`, `robots.txt`, `sitemap.xml` presenti e coerenti col dominio finale
- [ ] Privacy/Cookie policy validate (T-7.1 sblocca `[!]`)
- [ ] Cookie banner + analytics conformi
- [ ] `.htaccess`: HTTPS, URL puliti, 404, header, cache
- [ ] Lighthouse: Perf ≥ 90, Access ≥ 95, Best Practices ≥ 95, SEO = 100
- [ ] `per testi/` e file sorgente esclusi dal deploy
- [ ] Review finale Opus firmata (T-9.6)

---

## 7. CONVENZIONI DI CODICE

- **HTML:** semantico, indentazione 4 spazi, attributi in minuscolo, `lang="en"`, un solo `<h1>`.
- **CSS:** custom properties per tutto ciò che si ripete; classi kebab-case; niente `!important`
  salvo utility; mobile-first con `min-width` media query.
- **JS:** vanilla ES moduli, nessuna dipendenza; funzioni piccole; niente blocchi render-critical.
- **Commit:** Conventional Commits in inglese (`feat`, `fix`, `chore`, `docs`, `style`, `perf`,
  `refactor`). Scope = area (`seo`, `geo`, `css`, `content`, `deploy`…).
- **Accessibilità:** ogni immagine ha `alt`; ogni input ha `label`; focus sempre visibile.
- **Commenti `⚠️ DA VERIFICARE`** per ogni fatto non confermato dalle fonti.

---

## 8. DECISIONI APERTE (servono input umano)

| # | Decisione | Default proposto | Chi decide |
|---|---|---|---|
| D-1 | `www` vs non-`www` come canonico | non-www | committente |
| D-2 | Analytics | Plausible (no-cookie) | committente |
| D-3 | Gestione form contatti senza backend | `mailto:` + (opz.) Formspree con consenso | committente |
| D-4 | Includere pagina/bio team (es. Pietro Perlo, IFEVS) | Sì, in Company — ⚠️ verificare dati prima di pubblicare | committente |
| D-5 | `per testi/` resta nel repo git come fonte ma esclusa dal deploy | Sì | committente |

> Finché una decisione è aperta, i task collegati restano `[!]` e non si va in produzione su quel punto.

---

## 9. NOTE DEPLOYMENT ARUBA (dettaglio tecnico)

- Hosting Apache: `.htaccess` è il punto di controllo per redirect, URL puliti, header, cache,
  compressione, 404. È l'unico "server config" disponibile.
- **HTTPS/SSL:** attivare il certificato dal pannello Aruba; poi forzare HTTPS via `.htaccess`.
- **Deploy:** FTP/SFTP. Caricare solo i file pubblici (vedi T-8.4). **Mai** `per testi/`,
  `for_agents.md`, `partials/` sorgente, `.git`, `node_modules`.
- **DNS:** puntare `reflexora.ai` all'hosting Aruba; gestire `www` coerentemente con D-1.
- **Nessun runtime server** (no Node/PHP necessario): il sito è 100% statico.

---

## 10. GLOSSARIO (riferimento per contenuti e GEO)

- **Reflex Layer** — livello che esegue solo la prima azione permessa, verifica la risposta fisica
  e riporta un event-action trace compatto; agisce localmente quando attendere sarebbe non sicuro,
  inefficiente o energeticamente dispendioso.
- **Policy Layer** — definisce permessi, contesto e regole; responsabile di apprendimento,
  pianificazione e predizione. Separa il percorso locale urgente dall'intelligenza supervisoria.
- **World model** — predice; insegna offline/periodicamente regole limitate ai livelli inferiori.
- **EROIE** — Energy Returned on Invested Energy for Embodied Intelligence: proporzionalità
  energetica di un'azione.
- **Event-action trace** — traccia compatta: cosa è accaduto, cosa era permesso, cosa è stato
  comandato, cosa è stato misurato, se è servito contenimento/fallback.
- **Regola centrale** — assegnare ogni evento fisico al **lowest sufficient layer** capace di
  agire in modo sicuro e corretto.

---

## 11. STATO GENERALE (dashboard)

| Fase | Task totali | Completati | Stato |
|---|---|---|---|
| 0 Setup | 4 | 2 | 🔄 In corso |
| 1 Architettura | 6 | 0 | ⬜ Non iniziata |
| 2 Design system | 5 | 0 | ⬜ Non iniziata |
| 3 Contenuti | 9 | 0 | ⬜ Non iniziata |
| 4 Performance | 5 | 0 | ⬜ Non iniziata |
| 5 SEO | 9 | 0 | ⬜ Non iniziata |
| 6 GEO | 6 | 0 | ⬜ Non iniziata |
| 7 Legal | 4 | 0 | ⬜ Non iniziata |
| 8 Deploy | 6 | 0 | ⬜ Non iniziata |
| 9 QA | 6 | 0 | ⬜ Non iniziata |

> **Aggiornare questa dashboard** ogni volta che si chiude un task (regola §0.1).

---

## 12. STORICO ORIGINALE (architettura di partenza)

Il sito nasce come landing single-page statica (Vanilla HTML/CSS/JS, dark theme, sfondo mesh
animato, neural sphere e crossbar in puro CSS). Questo documento evolve quell'impianto verso la
struttura multi-pagina e la readiness SEO/GEO/GDPR descritta sopra, **preservando** il linguaggio
visivo esistente.

---

## 13. CHANGELOG (append-only — una riga per azione)

Formato: `AAAA-MM-GG · <agente> · <task ID> · <sintesi>`

- 2026-07-11 · Opus (setup) · — · Creato `for_agents.md` (rinominato da `architettura_sito.md`): architettura multi-pagina, design system, piano task per fasi con assegnazione agenti (Gemini/Sonnet/Opus), SEO/GEO/GDPR, deploy Aruba.

- 2026-07-11 · Gemini · T-0.1 · Creato `.gitignore` e rimosso `.DS_Store` dal tracking git.
- 2026-07-11 · Gemini · T-0.2 · Create cartelle `fonts/`, `images/og/`, `images/icons/`, `partials/` con `.gitkeep`.

<!-- Aggiungere qui sotto le nuove righe, in ordine cronologico -->
