<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-17 · 21:56 (CEST) · Claude Fable 5</div>

---

# Istruzioni operative V9 — per Claude Code (Opus 4.8)

**Input:** `animazione_hero_prototipo_V8.html` (NON modificarlo — creare
`animazione_hero_prototipo_V9.html` come copia e lavorare lì).
**Output:** un singolo `.html` standalone, zero dipendenze, < 60 KB, apribile in un browser,
trasmissibile via mail. L'integrazione nel sito resta un passo successivo e separato.
**Analisi di riferimento:** `analisi_animazione_V8_FABLE.md` (motivazioni e priorità).

**Regole trasversali, valide per ogni intervento:**

- Le coordinate citate sono quelle reali del V8; dopo ogni gruppo di modifiche **riverificare a
  schermo** (server locale + browser, viewport 1280×900) — collisioni e overflow si vedono, non
  si deducono.
- ⚠️ La logica delle fasi si verifica **solo** via `matches('[data-ph~="n"]')` / attributo
  `data-phase` — mai via `getComputedStyle().opacity` (compositor del preview inaffidabile).
- **Nessun cambio al wording tecnico congelato.** In particolare NON toccare le 6 voci in attesa
  di Perlo (`POLICY / SUPERVISORY LAYER`, `SHARED ENERGY FEED`, `CURRENT-LIMITED ISOLATED
  INJECTION` + sottotitolo, `BATTERY ZONE`, `PV energy output`/`Bounded injection`,
  `Local evidence`). Tutto ciò che qui introduce *testo nuovo* è marcato ✋ o ✅ (v. sotto).

Marcatura interventi: **[GRAFICO]** = esegui subito · **✋ [PROPOSTA — richiede ok Perlo]** =
implementa pure ma segnala a Marco che va mostrata a Perlo prima della messa online.

---

## A — Priorità ALTA

### A1. [GRAFICO] Rifondazione scala tipografica

A 1136px la scala di rendering è **0,90** (viewBox 1260). Obiettivo: **nessun testo informativo
sotto ~11,5 SVG (≈10,4px resi)**. Mappa di sostituzione dei `font-size` (valori SVG):

| Attuale | Nuovo | Elementi (posizione nel V8) |
|---|---|---|
| 8 | 10.5 | `One active source per cycle` (r.396), `Charge · External` (r.402) |
| 8.5 | 10.5 | `Cell Set · Imax · Tmax · Δt` (r.321), `SHARED ENERGY FEED` (r.328), i due `rp-role-sub` del Policy (r.363, 365) |
| 9 | 10.5 | `Cell ID · Current · ΔV · Temperature · Outcome` (r.325) |
| 9.5 | 11.5 | `Topology Permission Envelope` (r.317), `Eligibility Envelope` (r.320), `AUXILIARY DC SOURCE` (r.401), `Locally Switchable Substrings` (r.429), `Cells · Groups · Bricks` (r.446) |
| 10 | 11.5 | banner `EXAMPLE APPLICATION…` (r.247), `Floating Output · One-Hot Route` (r.412) |
| 10.5 | 12 | zone label (r.255, 262), titolo 2 righe `AUTHORIZED SOURCE INTERFACE` (r.394-395) |
| 11 | 12.5 | `EVENT · ACTION · RESPONSE` (r.324 → **13**, è un titolo di canale), `BMS Safety Enable · Hard Inhibit` (r.331), blocco `Cell Telemetry…` (r.333-335), `rp-role` EMS/BMS (r.362, 364) |
| 12 | 13 | tutti i tag operativi (`Local evidence`, `Measured response`, ecc., r.338-352) |
| 13 | 14 | `POLICY / SUPERVISORY LAYER` (r.359), `CURRENT-LIMITED` / `ISOLATED INJECTION` (r.410-411) |
| 14 | 15 | `PV MOSFET SWITCHING NETWORK` (r.419) |
| 15 / 15.5 | invariati | titoli nodi principali già ok |
| `rp-sub` 11 | 12 | sottotitoli nodi (r.373, 381, 388, 420) |

**Conseguenze da gestire (ricalcolo contenitori):**

- chip `Topology Permission Envelope`: `x=330 w=180` → `x=315 w=210` (testo centrato su x=420 invariato);
- chip `Eligibility Envelope`: `h=34` → `h=38`, seconda riga a y+2;
- chip `EVENT · ACTION · RESPONSE`: `x=495 w=210` → `x=485 w=230`;
- chip `SHARED ENERGY FEED`: `x=667 w=110` → `x=655 w=134` (testo su x=722 invariato);
- nodo `AUTHORIZED SOURCE INTERFACE`: `w=170` → `w=180` (translate 515→510, così il centro resta);
- dopo l'aumento, **screenshot e controllo collisioni** su: area Policy (i due ruoli affiancati),
  blocco destro `Cell Telemetry`, chip vs tracce.

### A2. [GRAFICO + ✋ micro-copy] Legenda "cartiglio tecnico"

Riempire il vuoto della colonna centrale bassa con un blocco legenda. Area disponibile:
**x 505–715, y 540–715** (sotto `AUXILIARY DC SOURCE`, che occupa y 462–502; le zone laterali
finiscono a x=480 e x=720).

Struttura consigliata (dentro l'SVG, gruppo `<g class="rp-legend">`):

- riquadro hairline stile `.rp-chip` ma fill trasparente: `x=505 y=540 w=210 h=170 rx=10`,
  stroke `var(--rp-hair)`;
- titoletto eyebrow: `LEGEND` (mono, 10.5, letter-spacing .18em, fill `var(--rp-muted)`);
- **5 righe dominio** (swatch = segmento di linea 16px nello stile del flusso corrispondente,
  con lo stesso dash-pattern, + label 10.5):
  `Policy · authority` (viola) · `Reflex · local decision` (cyan) · `Local evidence` (verde) ·
  `Power path` (arancio) · `Shared energy feed` (ambra);
- separatore hairline;
- **3 righe stato-cella** (swatch = mini-rect 14×8 che replica ESATTAMENTE gli stili `bz-low`,
  `bz-elig`, `bz-sel` — riuso visivo, non ridisegno):
  `Physical low state` · `BMS-eligible` · `Reflex-selected · one-hot`.

✋ **PROPOSTA — richiede ok Perlo:** le 8 label della legenda sono testo nuovo, composto solo con
vocabolario già presente nel diagramma/R7, ma vanno mostrate a Perlo insieme alle 6 voci già in
attesa. Implementarle pure in V9 (il file serve proprio a discuterle), segnalandolo a Marco.

### A3. [GRAFICO] Rail delle 7 fasi — sempre visibile, cliccabile, in HTML

Sostituisce caption transiente e step-bars. **Fuori dall'SVG** (testo HTML nitido, veri bottoni
accessibili), **dentro il componente** `.rp` (andrà anche nel sito).

1. **Rimuovere dall'SVG:** `#stepsW` (r.458-466), `#capW` (r.467), e dal CSS `.rp-caption`,
   `.rp-step` e le righe che le riferenziano in `.is-static` / reduced-motion.
2. **Ridurre il viewBox:** `0 0 1260 770` → `0 0 1260 728` (gli elementi più bassi — zone e
   bracket — finiscono a y=724). Aggiornare i due `rect` di sfondo/mask (`width=1260 height=770`
   → `728`, r.230 e r.244).
3. **Layout componente:** `.rp { display:flex; flex-direction:column; }`; l'SVG in un wrapper
   `.rp__stage { flex:1 1 auto; min-height:0; }`; sotto, il rail `~64px`. Il frame resta 740px:
   a 1136px l'SVG renderizza ~656px + rail 64px + margini ≈ ok. **Verificare che non nasca
   scroll interno.**
4. **Markup rail:**
   ```html
   <div class="rp-rail" role="group" aria-label="Causal sequence — 7 phases">
     <button type="button" class="rp-rail__item" data-goto="1">
       <span class="rp-rail__num">1</span>
       <span class="rp-rail__label">Local physical evidence</span>
     </button>
     <!-- … ×7, label = le stringhe ESISTENTI dell'array PHASES, verbatim -->
   </div>
   ```
5. **Stile:** griglia 7 colonne; hairline-top sul contenitore; num mono 12px, label mono 10px
   `var(--rp-muted)`; item attivo: num e barretta superiore in `var(--rp-reflex)`, label
   `var(--rp-ink)`, `aria-current="step"`; item passati del ciclo: num a opacità piena (stessa
   semantica delle vecchie step-bars). Focus ring: riusare lo stile di `.rp-ctl:focus-visible`.
   Hit-area verticale ≥ 40px.
6. **Comportamento JS (estendere `driver()`):**
   - `render()` aggiorna anche il rail (`aria-current`, classi `is-on`/`is-past`);
   - click su `data-goto="n"`: se in autoplay → salta a fase *n* e **continua** l'autoplay;
     se in pausa/static → esce da static, mostra fase *n* e resta in **manuale** (timer fermo;
     il bottone Play riprende l'autoplay);
   - `prefers-reduced-motion`: rail visibile ma non interattivo (`disabled` + `aria-disabled`),
     tutte le fasi restano mostrate staticamente → la narrazione non si perde più (fix a11y).
7. Le label del rail sono **le stringhe già esistenti** di `PHASES` — nessun wording nuovo.

### A4. [GRAFICO + ✅ testo non tecnico] Intestazione dell'artefatto

Sostituire l'attuale `.harness-note` (r.197-202) con un header sobrio in stile sito, **sopra il
frame, chiaramente marcato come NON parte del componente integrabile**:

```html
<!-- HARNESS — intestazione artefatto per uso interno. NON integrare nel sito. -->
<header class="art-head">
  <span class="art-eyebrow">REFLEXORA · INTERNAL REVIEW ARTIFACT</span>
  <h1 class="art-title">Reflex-Policy architecture — PV-to-battery example</h1>
  <p class="art-meta">V9 · <data di build> · standalone HTML · desktop-only ·
     mobile layout archiviato in animazione_hero_fonti/</p>
</header>
```

- `art-eyebrow`: mono 10px, letter-spacing .22em, uppercase, `var(--text-secondary)`;
- `art-title`: `'Outfit', system-ui, sans-serif` (fallback di sistema: nessun font esterno),
  ~20px, peso 700, `var(--text-primary)`;
- `art-meta`: mono 11px, `var(--text-secondary)`.
- Il titolo riusa **verbatim** il `<title>` SVG esistente (r.214) — nessun wording nuovo.
  Eyebrow e meta sono testo di servizio non tecnico. ✅
- Aggiornare anche il `<title>` della pagina: `… — Full-width Band V9`.

---

## B — Priorità MEDIA

### B1. [GRAFICO] "Base quieta, fase sonora"

1. **Frecce statiche neutre.** Nuovo marker `a5neu` (copia di `a5pol`, `fill`
   `rgba(148,163,184,.55)`). Sostituire `marker-end` su TUTTE le `.rp-trace` statiche
   (r.265-288) con `url(#a5neu)`. I marker colorati restano SOLO sui flussi animati `.rp-flow`
   → i flussi animati vanno quindi dotati di `marker-end` colorato proprio (oggi non ce l'hanno:
   aggiungerlo, es. `marker-end="url(#a5sen)"` sul flusso sense, ecc.), così il colore "arriva"
   con la fase.
2. **Canale supervisione** (r.290): marker dedicato `a5polFaint` (`fill rgba(167,139,250,.45)`)
   al posto di `a5pol` pieno.
3. **Zone più discrete:** `.rp-zone-label` opacity `.75` → `.55`; `.rp-bracket` stroke
   `rgba(0,242,254,.4)` → `.28`.

### B2. [GRAFICO] Ricomposizione margine destro

Blocco `Cell Telemetry` (r.333-335): eliminare il `·` orfano; ricomporre in:

```
Cell Telemetry      (y 404)
Faults              (y 421)
Response Validation (y 446, data-ph="6", invariato)
```

(La rimozione del separatore è punteggiatura, non wording. ✅) Aggiungere un tick di connessione
hairline dal canale verticale di supervisione (x=1120) alle label: `M 1120 400 L 1125 400`,
stroke come `.rp-superv`.

### B3. [GRAFICO] Ancoraggio del canale di ritorno

- Spostare il micro-testo di fase 7 `Cell ID · Current · ΔV · Temperature · Outcome` (r.325,
  oggi a x=740 y=214, staccato e invadente sull'area battery) **sotto il suo chip**:
  `x=600 y=214`, `text-anchor: middle` (è un `.rp-micro`, già middle).
- Verificare che col nuovo corpo (10.5) non tocchi la traccia envelope (r.278) — in caso
  abbassare a y=216.

### B4. [GRAFICO] Finitura / igiene del file

1. **CSS mancante:** aggiungere `.rp-tag--mid { text-anchor: middle; }` e sul tag
   `BMS Safety Enable · Hard Inhibit` (r.331) impostare `x=923` (punto medio della traccia
   785→1062) — oggi è ancorato a sinistra per la classe fantasma.
2. **Frame label** (r.205): `1136 × 620` → `1136 × 740`.
3. **Dead code:** rimuovere il blocco JS di clonazione mobile (r.528-540, `rpDiagramM` non esiste
   nel V8) e il CSS `.frame--bandm` (r.47).
4. Aggiornare il commento di testa del CSS (r.9-15): parla ancora di "V5" e di preview mobile.

---

## C — Priorità MEDIA (motion)

### C1. [GRAFICO] Timing differenziato per fase

In `PHASES`, aggiungere `dur` per fase e usarlo in `tick()` al posto della costante `STEP`:

| Fase | dur (ms) | Razionale |
|---|---|---|
| 1 | 1400 | doppia evidenza (PV + batteria), va letta |
| 2 | 1100 | transizione breve |
| 3 | 1500 | l'envelope è il contratto — respiro |
| 4 | 1200 | selezione |
| 5 | 2000 | climax fisico (con stagger interno, v. C3) |
| 6 | 1400 | verifica |
| 7 | 1600 | trace di ritorno + chiusura |

`PAUSE_AFTER_CYCLE`: 1400 → **2000**.

### C2. [GRAFICO] Easing di sito

Nelle transition di `.rp [data-ph]` e `.rp-flow`: `ease` → `cubic-bezier(.22,1,.36,1)`
(il `--ease-out` del sito). Pulse `rpPulse` invariato.

### C3. [GRAFICO] Stagger interno della fase 5 (niente glow — solo tempo)

Raccontare la causalità autorizzazione → sorgente/feed → iniezione con `transition-delay`
**scoped sotto `.rp[data-phase="5"]`** (così l'uscita di fase resta immediata):

1. aggiungere classi helper ai flussi di fase 5: `ph5-cmd` (flusso policy r.309 + flusso reflex
   r.297), `ph5-src` (i 3 flussi power lato PV r.298-300 + feed r.301), `ph5-inj` (flusso power
   iniezione r.310 + anello `.rp-armed` r.408);
2. CSS:
   ```css
   .rp[data-phase="5"] .ph5-cmd { transition-delay: 0s; }
   .rp[data-phase="5"] .ph5-src { transition-delay: .25s; }
   .rp[data-phase="5"] .ph5-inj { transition-delay: .5s; }
   ```
3. enfasi sobria sul feed: `.rp-flow--feed` stroke-width `4` → `4.5`; marker `a5fee`
   markerWidth/Height `5` → `6`.

---

## D — Cosa NON fare

- Non modificare V8 né alcun file del sito (`index.html`, `css/styles.css`, pagine).
- Non toccare le 6 voci terminologiche in attesa di Perlo (elenco in
  `appunto_perlo_terminologia_diagramma.md`).
- Non aggiungere font esterni, CDN, librerie. Niente filtri glow/neon diffusi.
- Non reintrodurre il layout mobile (resta archiviato; le scelte sopra non lo precludono:
  il rail HTML è riusabile tal quale in colonna).
- Non rimuovere/indebolire: Pause/Play, `prefers-reduced-motion`, `role="img"` +
  `aria-labelledby`, pausa off-screen (IntersectionObserver), pausa su tab nascosta.

---

## E — Checklist di verifica finale (obbligatoria, a schermo)

Servire in locale e aprire V9 a viewport 1280×900:

1. **Overflow:** `document.documentElement.scrollWidth <= window.innerWidth`; il frame è 1136px;
   nessuno scroll interno al componente.
2. **Audit tipografico** (script console): nessun `<text>` renderizzato sotto **10,4px**:
   ```js
   (() => { const svg = document.querySelector('.rp__band');
     const s = svg.getBoundingClientRect().width / 1260;
     return [...svg.querySelectorAll('text')].map(t => ({
       px: +(parseFloat(t.getAttribute('font-size') || 12) * s).toFixed(1),
       txt: t.textContent.trim().slice(0, 30)
     })).filter(x => x.px < 10.4); })()   // atteso: []
   ```
3. **Logica fasi** (mai via opacity!): per n = 1…7, `root.setAttribute('data-phase', n)` e
   conteggio `[...root.querySelectorAll('[data-ph]')].filter(e => e.matches('[data-ph~="'+n+'"]')).length`
   — confrontare con gli stessi conteggi eseguiti sul V8: devono coincidere, salvo i delta
   intenzionali di questo piano (es. fase 5: stessi elementi, solo classi helper in più).
4. **Rail:** click su ogni fase → `data-phase` corretto e `aria-current` sul bottone giusto;
   comportamento autoplay/manuale come da A3.6; tab-order e focus ring visibile.
5. **Pause/Play:** toggle `aria-pressed`, `is-static` applicato/rimosso, icona/testo aggiornati;
   in pausa il click sul rail mostra la singola fase (modalità manuale).
6. **Reduced-motion:** verifica in un browser reale (il preview non la emula in modo
   affidabile): tutto visibile staticamente, `.rp-ctl` nascosto, rail visibile ma disabilitato.
7. **Igiene:** peso file < 60 KB; `grep -iE "https?://|@import"` → nessuna risorsa esterna;
   console senza errori; `git status` conferma V8 intatto.
8. **Screenshot finale** dell'intera band + una fase a scelta (5), da allegare al changelog di
   `for_agents.md` (regola §0.1: aggiornare changelog e firmare).

---

*Consulenza design — Fable 5, 2026-07-17*

<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-17 · 21:56 (CEST) · Claude Fable 5</div>
