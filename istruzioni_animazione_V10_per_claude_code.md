<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-18 · 14:15 (CEST) · Claude Fable 5</div>

---

# Istruzioni operative V10 — per Claude Code (Opus 4.8)

**Input:** feedback del direttore scientifico (P. Perlo, elaborato dal suo agente AI, ricevuto
2026-07-18, 12 punti) su `animazione_hero_prototipo_V9.html`.
**Output:** `animazione_hero_prototipo_V10.html` — **un solo file standalone** contenente una
**famiglia di 3 viste sincronizzate**: `SYSTEM | PV SIDE | BATTERY SIDE`. V9 NON si tocca
(resta il riferimento "master approvato"); V10 si crea come copia e si evolve lì.
**Verdetto della direzione da rispettare:** *"retain V9 as the master and create two expanded
derivatives, not two simplified copies"* — le viste dedicate NON sono ritagli: sono
**ingrandimenti esplicativi** del rispettivo dominio fisico.

---

## 0. Stato terminologico — LETTURA OBBLIGATORIA prima di scrivere

Il punto 11 del feedback **scioglie le attese**:

1. **Termini CONGELATI in tutte e tre le viste** (il feedback li elenca; coincidono con la
   terminologia già in V9 → le 6 voci dell'appunto e le 8 label della legenda si considerano
   **confermate**): `Policy / Supervisory Layer` · `BMS Authority` · `Local Reflex` ·
   `Permission Envelope` · `Eligibility Envelope` · `One-Hot Selection` · `Bounded Action` ·
   `Local Evidence` · `Measured Response` · `Event · Action · Response` · `Shared Energy Feed` ·
   `Hard Inhibit`.
2. **Sinonimi VIETATI** ovunque: "smart balancing", "AI decision", "adaptive routing",
   "intelligent cell selection" (e simili).
3. **Decisione arrivata sui sub-label Policy** (in TUTTE le viste):
   `Optimization · Learning · Planning` → **`Optimize · Learn · Plan`**
   `Safety · Eligibility · Limits · Inhibit` → **`Safety · Eligibility · Limits`**
   ("Hard Inhibit" è già mostrato altrove e non va ripetuto nel sub-label). Bonus: i testi più
   corti permettono di alzare il corpo (target ≥ 11.5 SVG) — sparisce l'ultima eccezione
   tipografica della V9.
4. **Regola d'oro V10:** ogni testo nuovo visibile è una **citazione esatta dal feedback**
   (tutte fornite in questo doc). Non comporre wording tecnico nuovo. Per micro-testi di
   servizio non tecnici (aria-label, bottone ×) usare inglese neutro.

---

## 1. Architettura del file V10

- **Un unico componente `.rp`** con attributo di stato `data-view="system|pv|battery"` in
  aggiunta a `data-phase="1..7"`.
- **Tre `<svg>` fratelli** dentro `.rp__stage`: `#svgSystem` (il master V9, quasi intatto),
  `#svgPv`, `#svgBattery` — stessi viewBox `0 0 1260 728`, stessi `defs` duplicati per svg
  (id univoci: suffisso `-pv`, `-bat` per marker/pattern/mask, per evitare collisioni di id).
  CSS: `.rp[data-view="system"] #svgPv, ... { display:none }` (svg nascosti = animazioni CSS
  inattive, nessun costo).
- **Un solo rail** (7 bottoni) e **un solo switcher**, condivisi: le label del rail cambiano
  via JS in base alla vista.
- **Stato condiviso**: al cambio vista si preservano fase corrente e modalità
  (autoplay/manuale/pausa) — requisito esplicito del punto 5 (*"the transition should preserve
  the currently selected phase"*).
- Ogni svg ha il proprio `<title>`/`<desc>` (desc derivate dai titoli del feedback).
- Vincoli invariati da V9: standalone, zero dipendenze/CDN, niente glow diffuso, desktop-only,
  Pause/Play WCAG 2.2.2, `prefers-reduced-motion`, verifica logica **solo** via
  `matches('[data-ph~="n"]')`/`data-view` (mai `getComputedStyle().opacity`).
- **Peso target: < 150 KB** (3 SVG nello stesso file; V9 pesa 47 KB).

---

## 2. Interventi — PRIORITÀ A (core)

### A1. Scaffold: copia, header, switcher

1. `cp animazione_hero_prototipo_V9.html animazione_hero_prototipo_V10.html`; aggiornare
   `<title>` pagina e header artefatto: `V10 · <data build> · 3 synchronized views`.
2. **Switcher viste** sopra lo stage, dentro il componente (andrà anche nel sito):
   ```html
   <div class="rp-views" role="group" aria-label="Diagram view">
     <button type="button" class="rp-views__btn is-on" data-view-btn="system" aria-pressed="true">SYSTEM</button>
     <button type="button" class="rp-views__btn" data-view-btn="pv" aria-pressed="false">PV SIDE</button>
     <button type="button" class="rp-views__btn" data-view-btn="battery" aria-pressed="false">BATTERY SIDE</button>
   </div>
   ```
   Stile: chip mono uppercase 11px, hairline, attivo = bordo/testo cyan + `aria-pressed`;
   focus ring come `.rp-ctl`. Altezza riga ~34px: ricavarla riducendo lo stage (flex column:
   switcher + stage + rail dentro il frame 740px — verificare che non nasca scroll).
3. JS: `setView(v)` → aggiorna `data-view`, `aria-pressed`, label del rail (A2), contenuto
   pannello se aperto (A6). NON tocca `data-phase` né lo stato di run.

### A2. Rail sincronizzato: label per vista

Le 7 fasi restano **gli stessi numeri** in tutte le viste (punto 4). Label del rail = tabella
del feedback (verbatim):

| # | SYSTEM | PV SIDE | BATTERY SIDE |
|---|---|---|---|
| 1 | Detect local evidence | Detect PV condition | Detect cell condition |
| 2 | Classify local event | Classify cloud/anomaly | Identify deficit |
| 3 | Verify permission | Verify topology envelope | Declare BMS eligibility |
| 4 | Local Reflex decision | Select PV response | Select one-hot cell |
| 5 | Execute bounded action | Reconfigure PV path | Inject bounded current |
| 6 | Validate response | Measure source response | Measure cell response |
| 7 | Report evidence | Report PV outcome | Report transfer outcome |

Implementazione: oggetto JS `RAIL_LABELS = {system:[...], pv:[...], battery:[...]}`;
`setView()` riscrive i `.rp-rail__label`. NB: le label V10 del master sostituiscono le label
lunghe V9 (che migrano nel pannello disclosure, A6). Durate per fase (`dur`) e stagger fase 5:
**identici in tutte le viste** (punto 2: *"same animation timing"*).

**Nuovo comportamento click sul rail** (serve il punto 6): click su una fase = *modalità
studio*: salta alla fase, **ferma l'autoplay** (manuale), **apre il pannello disclosure** di
quella fase. `Play` chiude il pannello e riprende il ciclo. (Cambia il comportamento V9
"click-in-autoplay-continua": documentarlo nel changelog.)

### A3. Ritocchi al MASTER (#svgSystem) — punto 1: "keep essentially as is"

Il master NON acquisisce nuovo dettaglio tecnico (*"already close to the maximum useful
information density"*). Solo questi 4 ritocchi trasversali:

1. **Sub-label Policy** (→ §0.3): `Optimize · Learn · Plan` e `Safety · Eligibility · Limits`,
   corpo alzato a ≥ 11.5 SVG.
2. **Statement control/energy path** (punto 7), permanente, sotto/accanto alla legenda, stile
   `rp-legend-lbl` ma `fill var(--rp-ink)`, corpo 12:
   **`Signals decide. Power electronics carry energy.`**
   (Alternativa pre-approvata dalla direzione se Marco preferisce il registro divulgativo:
   *"Decision path selects the action; power path executes it."* — sceglierne UNA, coerente
   nelle 3 viste.)
3. **Chip SAFE STATE** (punto 8), sempre visibile, discreto (stile `.rp-chip`, testo muted,
   NON deve dominare), posizione: angolo in basso a destra dell'svg (area libera x~1100-1250,
   y~690-720). Testo verbatim su 2 righe:
   `SAFE STATE`
   `Converter off · Selector all-off · No authorization`
4. Banner invariato. Nessun altro cambiamento al master.

### A4. Vista PV (#svgPv) — "enlarged, not cropped"

**Titolo banner** (verbatim dal feedback): `PV-SIDE REFLEX` ·
sottotitolo `Local source-state detection and bounded topology response`.
**Riga concettuale** sotto il banner (verbatim, è LA distinzione che questa vista deve
insegnare): `A coherent cloud event is not the same as a localized source anomaly.`

**Mantiene identici a V9/master** (punto 2): colori, font, timing, rail 7 fasi, blocco Policy
(con i nuovi sub-label), Pause, struttura legenda, ritorno `EVENT · ACTION · RESPONSE`,
statement A3.2, chip SAFE STATE A3.3.

**Elementi da INGRANDIRE** (lista della direzione — tutti obbligatori):
substring/rami PV · ramo illuminato normale · ramo in ombra/anomalo · evidenza V-I-T-shade ·
blocco decisionale PV-Side Reflex · rete MOSFET · percorso bypass/riconfigurazione · MPPT
reacquisition · PV energy output · report event-action-response.

**Blueprint di composizione** (indicativo — Opus compone e verifica a schermo; font informativi
≥ 12 SVG, titoli nodi 15–16):

```
[banner titolo + riga concettuale]                      y 8–56
[POLICY / SUPERVISORY LAYER  480×82, come master]       y 60–142
[envelope chip Topology Permission Envelope — grande]   y ~150
SX (fisica, x 130–620):            DX (decisione, x 660–1130):
  PV SEGMENTS espanso                PV-SIDE REFLEX espanso
  (3 substring ~90×26,               + 2 chip classificatori (fase 2):
   shade sulla centrale,               [ COHERENT CLOUD VARIATION ]
   bypass ben visibile)                [ LOCALIZED ANOMALY ]  ← si accende
  MOSFET SWITCHING NETWORK           evidence path grande (V, I, T, shade)
  DC-DC CONVERTER · MPPT             ritorno EVENT·ACTION·RESPONSE al Policy
  PV energy output → SHARED ENERGY FEED (chip terminale, la batteria NON appare)
[legenda + statement + SAFE STATE]                      y 560–724
```

**Chip classificatori (fase 2)** — realizzano il punto 9 ("una sola anomalia: shade
localizzato") e la distinzione cloud/anomalia: due chip affiancati vicino al Reflex; in fase 2
`LOCALIZED ANOMALY` si accende (stroke cyan, `data-ph="2 3 4 5 6 7"`),
`COHERENT CLOUD VARIATION` resta neutro/spento. Testi derivati dal wording di fase 2 del
feedback (*"Coherent weather variation is distinguished from localized abnormal behaviour"*).
Nessun altro guasto nel default (scenari multipli = futuro selettore, NON in V10).

### A5. Vista BATTERY (#svgBattery) — la rappresentazione autorevole del Battery Reflex-Balance

**Titolo banner** (verbatim): `BATTERY-SIDE REFLEX` ·
sottotitolo `BMS-authorized one-hot corrective energy injection`.
**Riga concettuale** sotto il banner (prima frase del teaching message, verbatim):
`The lowest-voltage cell is not automatically selected.`
(Il messaggio completo va nel pannello della fase 4, v. A6.)

**Elementi da INGRANDIRE** (lista della direzione — tutti obbligatori):
BMS authority · percorso telemetria · eligibility envelope · rappresentazione cella a 3 stati ·
Reflex locale · selettore one-hot · shared energy feed · stadio injection current-limited ·
bounded injection · response validation · hard inhibit · event recording.

**Blueprint di composizione** (indicativo):

```
[banner titolo + riga concettuale]                      y 8–56
[POLICY layer come master; in questa vista la metà BMS AUTHORITY
 riceve il crest/evidenza visiva]                       y 60–142
[Eligibility Envelope chip GRANDE: Cell Set · Imax · Tmax · Δt]
SX (potenza, x 130–600):           DX (autorità+decisione, x 640–1130):
  SHARED ENERGY FEED (ingresso       telemetria permanente GRANDE
   da sx, la PV NON appare)          BATTERY-SIDE REFLEX espanso
  CURRENT-LIMITED ISOLATED           ONE-HOT SELECTOR come blocco proprio
   INJECTION espanso                  (3+ rotte candidate, UNA chiusa)
  BMS Safety Enable · Hard Inhibit   Response Validation
   (percorso indipendente, visibile) ritorno EVENT·ACTION·RESPONSE
[BATTERY ZONE espansa: 6 elementi, 1 low → anello viola → anello ciano,
 stati concentrici GRANDI]                              y ~560–690
[legenda (con i 3 stati) + statement + SAFE STATE]      in area libera
```

**Vincoli specifici:**
- I **3 stati cromatici concentrici** restano identici nella semantica (arancio = physical low,
  viola = BMS-eligible, ciano = Reflex-selected one-hot) — la direzione li definisce *"one of
  the most effective didactical features"*: qui vanno resi GRANDI e inequivocabili.
- Il **selettore one-hot** diventa un elemento visivo esplicito (blocco o simbolo con N rotte
  di cui UNA attiva), non più implicito nelle sole rotte tratteggiate.
- Una sola anomalia nel default (punto 9): **una cella low eleggibile**. Niente fault multipli.

### A6. Progressive disclosure — pannello per fase (punto 6)

**Markup** (HTML, fuori dagli svg, dentro `.rp`):
```html
<aside class="rp-panel" role="region" aria-live="polite" hidden>
  <button type="button" class="rp-panel__close" aria-label="Close">×</button>
  <span class="rp-panel__eyebrow">PHASE <n> — <rail label corrente></span>
  <div class="rp-panel__body">…</div>
</aside>
```
Posizione: overlay assoluto ancorato a destra dentro lo stage (~300px, fondo `rgba(8,12,21,.94)`,
hairline, radius 10), NON copre il rail. Apertura: click fase (v. A2); chiusura: ×, `Esc`, o `Play`.
Cambio vista con pannello aperto → il corpo si aggiorna alla stessa fase nella nuova vista.

**Contenuti = 21 voci (3 viste × 7 fasi), tutte citazioni verbatim dal feedback** (max 2–3
frasi come richiesto):

- **SYSTEM** (riuso delle label lunghe V9, già approvate): 1 `Local physical evidence` ·
  2 `Local Reflex evaluation` · 3 `BMS / Policy defines the safe action envelope` ·
  4 `Local Reflex selects one authorized destination` · 5 `Authorized source · BMS-enabled
  bounded injection` · 6 `Measured response verified` · 7 `Outcome returned to BMS ·
  eligibility updated`.
- **PV** (wording suggerito, punto 2): 1 `Voltage, current, temperature and irradiance
  behaviour are observed.` · 2 `Coherent weather variation is distinguished from localized
  abnormal behaviour.` · 3 `Permitted topology actions and operating limits are confirmed.` ·
  4 `The permitted first response is selected.` · 5 `MOSFET switching, bypass, isolation or
  MPPT reacquisition is initiated.` · 6 `Electrical behaviour after the action is verified.` ·
  7 `Event, action and measured outcome are returned to Policy.`
- **BATTERY** (wording suggerito, punto 3): 1 `Voltage, temperature, fault state and freshness
  are monitored.` · 2 `A physically low or limiting element is detected.` · 3 `Cell set,
  current, temperature and duration limits are issued.` · 4 (teaching message completo)
  `The lowest-voltage cell is not automatically selected. The BMS first determines
  eligibility; the Reflex then selects one eligible destination; the power stage injects
  bounded energy; the measured response confirms what physically occurred.` ·
  5 `The converter and selector execute the authorized transfer.` **+ blocco
  "Authorization conditions"** (esempio esplicito del feedback, elenco puntato):
  `valid BMS permission · eligible destination · source ready · selector verified ·
  current limit active · no hard inhibit` · 6 `Current, voltage response, temperature and
  timeout are checked.` · 7 `Cell identity, delivered charge, response and termination
  reason are recorded.`

### A7. "What changed physically?" (punto 10)

Nelle sole viste specialistiche, a **fine fase 5** appare una riga conclusiva (poi resta in
fase 6, sparisce dalla 7). Implementazione: `<text>` con `data-ph="5 6"` e, scoped sotto
`.rp[data-phase="5"]`, `transition-delay: 1.2s` (fase 5 dura 2000ms → appare negli ultimi
800ms; in fase 6 nessun delay). Stile: `rp-tag`, corpo 13, colore `--rp-ink`, posizione
vicino all'elemento fisico interessato. Testi verbatim:
- PV: **`The local electrical topology has changed.`**
- Battery: **`Useful energy is now entering one authorized cell.`**

### A8. Reduced-motion (migliora il limite V9)

In `prefers-reduced-motion`: le 3 viste restano statiche (tutto visibile a .85), lo **switcher
resta attivo** (cambiare vista non è animazione), e il **rail resta cliccabile SOLO per aprire
i pannelli** (nessun salto di fase animato: `jump()` non parte, si apre solo il pannello della
fase cliccata). Così i 21 contenuti disclosure restano accessibili a tutti.

---

## 3. Intervento — PRIORITÀ B (dopo il core, se il budget di sessione lo consente)

### B1. Demo Hard Inhibit (punto 8, "optional demonstration")

Solo in vista BATTERY: bottone `DEMO · HARD INHIBIT` (stile `.rp-ctl`, accanto a Pause,
visibile solo con `data-view="battery"`). Sequenza scriptata FUORI dal ciclo a 7 fasi
(stati via classe `.is-inhibited` sul root + elementi dedicati `data-demo="inh"`):
1. forza fase 5 (transfer attivo), 800ms;
2. `.is-inhibited`: il flusso injection si spegne, il percorso `BMS Safety Enable · Hard
   Inhibit` si accende pieno (power/policy), il selettore torna all-off (rotte tutte
   tratteggiate), il chip SAFE STATE si evidenzia (stroke `--rp-power`), 1500ms;
3. l'evento viene riportato (flusso trace fase-7 attivo), 1500ms;
4. cleanup: rimozione classe, ritorno in manuale a fase 5, pannello chiuso.
Durante la demo: rail e switcher disabilitati; un secondo click annulla. In reduced-motion il
bottone non appare. Verifica via classi/attributi, non opacity.

---

## 4. Cosa NON fare

- NON modificare V9 (`animazione_hero_prototipo_V9.html`), V8, né alcun file del sito.
- NON aggiungere dettaglio tecnico al master (punto 1 — è al massimo utile di densità).
- NON introdurre i sinonimi vietati (§0.2), né wording non citato nel feedback.
- NON mostrare più anomalie simultanee nel default (punto 9). NESSUN selettore scenari in V10
  (shade/hotspot/reverse-current… e low-SOC/impedance/temperature/invalid-measurement sono
  **roadmap futura**: annotarli nel changelog come deferred).
- NON far comparire la batteria nella vista PV né il PV nella vista battery (ognuna racconta
  il proprio dominio; il punto di contatto è il chip `SHARED ENERGY FEED`).
- NON caricare il diagramma di testo permanente (punto 6: le spiegazioni vivono nel pannello).
- NON rimuovere/indebolire: Pause/Play, reduced-motion, `role="img"`+`title`/`desc` per svg,
  pausa off-screen, pausa su tab nascosta, focus ring.

---

## 5. Nota per l'integrazione futura (punto 12 — NON parte di V10, registrare in for_agents)

Gerarchia sito decisa dalla direzione: 1º visual = master system view · 2º = "How the PV-side
Reflex acts" · 3º = "How the Battery-side Reflex acts", con sotto lo statement di collegamento
(verbatim, da usare in pagina): *"One architecture, two local Reflex domains: the PV side
determines how energy is made available; the battery side determines where authorized
corrective energy is applied. Policy determines whether the action is permitted."*
Con lo switcher V10 le tre viste possono anche vivere in UN solo embed — decisione di layout
da prendere in fase di integrazione, non ora.

---

## 6. Checklist di verifica finale (obbligatoria, a schermo, per OGNI vista)

1. **Overflow**: nessuno scroll orizzontale pagina né interno al frame (switcher+stage+rail
   dentro 740px).
2. **Audit tipografico** (script V9, esteso ai 3 svg): **zero** testi informativi < 10.4px
   resi (unica tolleranza: readout fase 7 del master a 9.9). I sub-label Policy accorciati
   devono risultare ≥ 10.4.
3. **Logica fasi × vista**: per ciascuna vista e n=1..7, conteggio `matches('[data-ph~="n"]')`
   registrato nel changelog; master = conteggi V9 invariati (6/5/8/8/13/13/8).
4. **Switcher**: SYSTEM→PV→BATTERY→SYSTEM preservando fase e modalità (test esplicito del
   caso del feedback: pausa a fase 4 nel master → BATTERY SIDE → si apre a fase 4).
5. **Rail**: click fase → manuale + pannello aperto con contenuto giusto (vista×fase);
   Play → pannello chiuso, ciclo riparte; `Esc` chiude; `aria-current` corretto.
6. **Pannello fase 5 battery**: presente il blocco Authorization conditions (6 voci).
7. **A7**: riga "what changed" appare a fine fase 5 e persiste in fase 6 (verifica via
   presenza `data-ph="5 6"` + delay scoped, e visivamente).
8. **Terminologia**: grep dei 12 termini congelati (≥1 dove pertinente) e grep NEGATIVO dei
   4 sinonimi vietati (=0). Grep dei vecchi sub-label (`Optimization · Learning · Planning`,
   `· Inhibit`) = 0.
9. **SAFE STATE + statement** presenti nelle 3 viste; demo Hard Inhibit (se fatta): ciclo
   completo + annullamento + assenza in reduced-motion.
10. **Reduced-motion** (browser reale): 3 viste statiche, switcher attivo, rail apre solo
    pannelli.
11. **Igiene**: peso < 150 KB; nessuna risorsa esterna (solo xmlns); console pulita; V9/V8
    intatti (`git status` + `ls -la` date); id SVG unici (nessuna collisione marker tra svg).
12. **Screenshot** delle 3 viste (fase 5) + changelog `for_agents.md` aggiornato e firmato,
    con nota: terminologia confermata dal feedback 2026-07-18 (punto 11) e scenari multipli
    deferred.

---

*Consulenza design — Fable 5, 2026-07-18*

<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-18 · 14:15 (CEST) · Claude Fable 5</div>
