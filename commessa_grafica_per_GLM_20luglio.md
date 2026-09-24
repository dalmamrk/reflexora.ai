<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-20 · 14:56 (CEST) · Claude Opus 4.8</div>

---

# Commessa grafica per GLM 5.2 (ZCode) — reflexora.ai

> **Cos'è questo documento.** È l'**ordine di lavoro** per te, **GLM 5.2**, che operi nella cartella
> del progetto via IDE. Nasce dalla **validazione** della tua analisi
> `analisi_design/analisi_design_GLM_20luglio.md` (fatta da Claude Opus 4.8): l'analisi è
> **solida e confermata dal codice**; qui la trasformo in modifiche da eseguire, **limitate alle
> priorità alte** decise dal committente. Le voci a priorità media/bassa restano in backlog (§3).

---

## 0. REGOLE — leggere prima di toccare qualsiasi file

1. **PRIMA di iniziare: leggi `for_agents.md`** (tutto §0 = regole, §5 = design system, §13 = changelog
   recente). **DOPO ogni task: aggiorna `for_agents.md`** — stato task, riga di §13 Changelog firmata
   (`AAAA-MM-GG · GLM (ZCode) · <task> · <sintesi>`), dashboard §11. È la regola §0.1, non opzionale.
2. **Un task alla volta, un commit per task.** Mai lasciare il sito rotto tra un task e l'altro (§0.7):
   ogni commit deve caricare e navigare.
3. **Testi congelati (§0.9): NON riscrivere il copy.** Qui si **impagina diversamente**, non si cambiano
   le parole. Nessun claim nuovo (§0.12): i numeri usati (12 IT + 2 EPO + 1 PCT, 8 domini) sono già in
   `for_agents.md` §4.
4. **ZERO risorse esterne / ZERO nuove dipendenze.** Il sito è appena stato reso **font self-hosted e
   senza terze parti** (Inter/Outfit in `fonts/*.woff2`, GDPR-clean — da questo dipendono le pagine
   legali che affermano "nessun contenuto di terze parti / nessun trasferimento extra-UE").
   **VIETATO** reintrodurre Google Fonts, CDN, icon-font esterni, immagini remote, `@import` da rete.
   Icone/loghi = **SVG inline** o file locali in `images/`. Dopo ogni modifica **verifica** (§4) che i
   domini terzi restino **zero**.
5. **Non toccare:** le 3 pagine legali (`privacy-policy.html`, `cookie-policy.html`, `note-legali.html`),
   il blocco footer legale (identificazione art. 2250 + link + ©), i `@font-face` e i `<link rel="preload">`
   dei font, i prototipi animazione `animazione_hero_prototipo_*.html` (sono standalone; **il V1
   `animazione_hero_prototipo.html` contiene ancora Google Fonts ma è archivio non deployato** — non usarlo
   come sorgente, non modificarlo). Fonte per la hero = **V10 + M1**.
6. **Accessibilità: non regredire.** Mantieni `prefers-reduced-motion`, `:focus-visible`, `skip-link`,
   landmark semantici, il gating `.js .reveal` (contenuto visibile senza JS), il contrasto AAA già
   verificato. Mobile-first: verifica a **375px** e **1280px**.
7. **Partial condivisi:** header e footer sono in `partials/` e si inlineano con `node build.mjs`
   (idempotente). Se modifichi header/footer, modifica il **partial** e rilancia `build.mjs` — non le
   singole pagine. Per contenuti che NON sono header/footer (es. il div `.bg-gradient-mesh`) l'inlining
   automatico non c'è: vanno aggiunti in modo **identico** in ogni pagina (v. T2).
8. **Verifica a schermo** ogni modifica (servi in locale + browser). Non fidarti dei numeri di riga di
   questo doc o della tua analisi: `css/styles.css` è cambiato dopo la tua analisi (aggiunti `@font-face`
   + blocco `.legal-*`), quindi **i riferimenti di riga sono sfasati** → localizza per **selettore/contenuto**.

---

## 1. Esito della validazione (cosa è confermato e cosa correggo)

**La tua analisi è accurata.** Verificato contro il codice:
- ✅ Pagine interne = **template clonato**: `architecture/technology/applications/research/company` hanno
  tutte l'inline `style="min-height: 70vh; padding: 8rem 0;"` e tutte `<h1 class="section-title center">`.
- ✅ `.bg-gradient-mesh` (il div glow) montato **solo** su `index.html` e `404.html`.
- ✅ **Duplicazioni CSS** presenti (`.hero-title`, `.section-title`, `.btn-primary`, `.app-card`,
  `.glass-card`, `.navbar.scrolled` ripetuti/override a strati).
- ✅ `.eyebrow` **definita nel CSS ma mai usata** nelle pagine del sito.
- ✅ `.app-card` usa `<h4>` (salto h2→h4); shine-sweep presente (`.glass-card::before`, `.app-card::before`).

**3 correzioni da tenere presenti (mie, in validazione):**
1. **`body::before` (la griglia engineered) è GLOBALE** (`body::before`, non gated): è già su **tutte**
   le pagine. Ciò che manca alle 5 interne è **solo il div `.bg-gradient-mesh`** (il glow radiale). Quindi
   T2 aggiunge il **div**, non la griglia.
2. **Freeze-frame + `.is-static`:** attenzione — `.is-static` porta **tutti** gli elementi `[data-ph]`
   a opacità .85 (mostra l'**intera** architettura, non la sola fase 5). Va benissimo per un hero
   "panoramica dell'architettura", ma **non** dà l'enfasi di una singola fase. Scegli consapevolmente
   (v. T1).
3. **Riferimenti di riga sfasati** (v. §0.8): localizza per selettore.

---

## 2. LA COMMESSA — 4 workstream (priorità alte)

Ordine consigliato: T1 → T2 → T3 → T4. Sono indipendenti; T4 (consolidamento) conviene **dopo** T1-T3
per non ripulire codice che stai per cambiare.

### T1 — Hero: placeholder dell'animazione `[FATTA da Claude Code — NON rifare]`

**Decisione committente aggiornata (2026-07-20): niente freeze-frame, niente estrazione dal V10.**
In `index.html` la `.neural-sphere` è già stata sostituita (da Claude Code) con un **segnaposto
etichettato** `.hero-placeholder` (box tratteggiato con gradiente accent + testo *"Qui verrà piazzata
l'animazione Reflex–Policy (V10)"*, eyebrow "PLACEHOLDER"). Verificato desktop+mobile, in tema, 0 JS,
0 risorse esterne.

**Cosa deve fare GLM su questo punto: NULLA ora**, tranne:
- **NON** estrarre freeze-frame né integrare V10/M1: l'integrazione del componente animato è differita
  (avverrà con il **componente definitivo**, quando pronto — è la Fase 2/D-6).
- In **T4** (consolidamento CSS): la regola `.neural-sphere` (+ `.ring*`, `.core`, relativi
  `@keyframes`) è ora **codice morto** (non più referenziata in pagina) → **rimuoverla**. Mantenere
  invece `.hero-placeholder*` finché il segnaposto è in uso.
- Quando arriverà il componente definitivo, la sostituzione sarà **solo** dentro `.hero-visual`
  (scambio del contenuto del segnaposto) — l'impalcatura resta.

### T2 — Substrato visivo coerente su tutte le pagine `[alta]`

**Obiettivo:** eliminare il "salto di qualità" home→pagine interne.

- Aggiungi il **div `<div class="bg-gradient-mesh"></div>`** (il glow radiale animato) **a tutte le
  pagine** che ne sono prive: `architecture, technology, applications, research, company, contact,
  privacy-policy, cookie-policy, note-legali` (index e 404 ce l'hanno già). **Posizione identica** a quella
  di `index.html` (subito dopo l'apertura `<body>`/header, come nel file esistente — copia il pattern
  esatto). La griglia `body::before` è **già globale**, non toccarla.
- Rimuovi l'inline `style="min-height: 70vh; padding: 8rem 0;"` dai 5 `<main>` interni e sostituiscilo con
  una **classe** (es. `.page-main` con gli stessi valori spostati in CSS/token) — coerente con lo spirit
  "niente inline style" del design system.
- **Attenzione motion:** `.bg-gradient-mesh` è animato → verifica che rispetti `prefers-reduced-motion`
  (se l'animazione non è già gated, gate-la).
- **Accettazione:** le 5 pagine interne hanno lo stesso substrato "premium dark" della home; nessun inline
  style residuo nei `<main>`; reduced-motion ok; verificato a 375/1280px.

### T3 — Gerarchia tipografica `[alta]`

**Obiettivo:** far sì che H1 pagina ≠ H2 sezione ≠ titolo card, e togliere la fragilità delle triple
dichiarazioni.

1. Nuova classe **`.page-title`** a `var(--fs-h1)` per gli **H1 delle pagine interne** (oggi
   `<h1 class="section-title center">` → diventa `<h1 class="page-title center">`). Distingue il titolo
   di pagina dal titolo di sezione.
2. **Consolida `.hero-title`** in **una sola** dichiarazione a `var(--fs-h1)` con eventuale override
   responsive `min-width` (oggi è ridichiarata più volte con valori diversi: fragile).
3. **Hero della home:** oggi l'unico H1 è "REFLEXORA" (brand). Aggiungi un **eyebrow/sottotitolo** (dal
   copy esistente) che dica *cosa fa* REFLEXORA, così il lettore lo capisce prima del paragrafo. (Non
   inventare testo: usa il posizionamento già presente.)
4. **`.app-card`**: risolvi il salto h2→h4 → porta i titoli card a `<h3>` (o introduci un livello visivo
   intermedio coerente). Verifica che l'ordine dei heading resti semanticamente corretto per gli screen
   reader.
5. Usa finalmente la classe **`.eyebrow`** già definita (mono kicker) dove serve un sovra-titolo di sezione.
- **Accettazione:** H1 pagina interna visibilmente più grande/distinto dai section-title; una sola
  `.hero-title`; nessun salto di heading non semantico; verificato a schermo.

### T4 — Consolidamento CSS `[alta, meccanica]`

**Obiettivo:** eliminare il debito degli override a strati (nessun cambiamento visivo atteso).

1. **Unifica le dichiarazioni duplicate** portandole a **una sola** ciascuna: `.btn-primary`,
   `.app-card`, `.glass-card`, `.hero-title`, `.section-title`, `.navbar.scrolled`. Il "DESIGN REFINEMENT
   PASS 2026-07-12" diventa la **base**, non un override in coda. Verifica pixel-a-pixel prima/dopo (il
   rischio è cambiare la resa vinta per ordine-file).
2. **Sposta i valori "magici" in token** (`--space-*`, `--radius-*`) dove esistono già equivalenti.
3. **Rimuovi lo shine-sweep** decorativo (`.glass-card::before`, `.app-card::before` con lo skew che
   traversa): vezzo consumer, in conflitto col tono "research division". (Se un `::before` serve a scopo
   strutturale e non solo allo sweep, conserva quello.)
4. **Aggiungi un indice a inizio file** e separa nettamente le sezioni: il prossimo agente deve capire
   dove sta cosa. NON toccare il blocco `@font-face` in testa né il blocco `.legal-*`.
- **Accettazione:** ogni selettore chiave definito una volta; 0 regressioni visive (confronto screenshot);
  `styles.css` più corto e navigabile.

---

## 3. Backlog — Fase 2 (NON in questa commessa)

Decisione committente: fare **ora solo** T1–T4. Restano per una fase successiva (dalla tua analisi, tutte
valide, da non perdere):
- **§3.3 Differenziazione pagine interne:** timeline (research), compare-table 3-col (technology), bento
  asimmetrico (applications), anchored cards con `id` deep-link (architecture, utile GEO), stat block
  (company).
- **§3.5 Evidence components:** `.stat-band` (12·2·1·8), `.pull-quote` (statement identitario),
  `.term-card` (glossario Reflex/Policy/EROIE — utile GEO).
- **§3.1.B Integrazione animazione completa** V10+M1 (D-6) in `architecture.html` o sezione full-bleed;
  valutare modalità `ambient` (home) vs `study` (architecture) sul `.rp`.
- **§3.7 Navbar** (inner max-width, logo mark, active pill), **§3.8 Footer 3-colonne**, **§3.9 micro**
  (scroll-padding-top, text-wrap:pretty, hover link, btn full-width solo in hero, eventuale tema light).

---

## 4. Verifica finale (obbligatoria, a schermo) + chiusura

Per **ogni** task, prima del commit:
1. **Zero risorse esterne** (il vincolo più importante). In console:
   `[...new Set(performance.getEntriesByType('resource').map(r=>new URL(r.name).host))]`
   → deve contenere **solo** l'host locale. E: `document.cookie` → vuoto.
2. **Nessuna regressione visiva** non voluta: confronto screenshot prima/dopo su home + 1 pagina interna,
   a **375px** e **1280px**. Nessun overflow orizzontale.
3. **Accessibilità intatta:** `prefers-reduced-motion` (animazioni ferme), `:focus-visible` visibile su
   nav/bottoni, skip-link funzionante, heading order semantico, contenuto visibile senza JS.
4. **Pagine legali + footer legale + font preload/`@font-face` invariati.**
5. `node build.mjs` rilanciato se hai toccato i partial; sito che carica e naviga su tutte le pagine.
6. **`for_agents.md` aggiornato e firmato** (§0.1): stato task, riga §13, dashboard §11.

> Nota di coordinamento: se durante T1 emergono decisioni sul componente animato (contenitore fluido,
> fusione M1, modalità ambient/study), **non** anticiparle qui — appartengono a D-6/Fase 2. Segnalale nel
> changelog come "da valutare in integrazione D-6".

---

*Commessa redatta da Claude Opus 4.8 su validazione dell'analisi GLM (ZCode) del 2026-07-20. Scope: solo
priorità alte. Esecuzione: GLM 5.2. Aggiornare `for_agents.md` a ogni task.*

<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-20 · 14:56 (CEST) · Claude Opus 4.8</div>
