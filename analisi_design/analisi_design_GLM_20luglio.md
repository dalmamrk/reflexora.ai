# Analisi del design — reflexora.ai

**Autore:** GLM (ZCode)
**Data:** 20 luglio 2026
**Oggetto:** revisione grafica del sito statico (HTML/CSS/JS vanilla)
**Perimetro:** tutti i file `.html` in root + `css/styles.css` + `js/main.js` + `partials/`
**Tipo di output:** solo analisi e proposte. **Nessun file di progetto è stato modificato.**

---

## 0. Sintesi esecutiva

L'architettura informativa del sito è sana: gerarchia di pagine chiara, mobile-first onesto, design system a token, accessibilità base rispettata, font self-hosted GDPR-clean. **È un lavoro di ingegneria front-end corretto.**

**Nota preliminare importante (precisazione del committente, 2026-07-20):** la *neural sphere* attualmente in `index.html` **è un placeholder provvisorio, non una scelta definitiva**. L'elemento centrale del sito, già in fase di prototipazione, è **l'animazione Reflex–Policy** che si trova in `animazione_hero_prototipo_V10.html` (desktop) e `animazione_hero_prototipo_M1.html` (mobile). **La sfera verrà sostituita con un'immagine statica estrapolata dall'animazione** (freeze-frame), in attesa/dopo l'integrazione del componente animato completo. Questa informazione cambia in modo sostanziale l'analisi dell'hero: il "problema sfera" è già noto e già pianificato il rimedio, quindi il focus si sposta su (a) come estrarre un buon freeze-frame, (b) come integrare il componente animato V10, e (c) il resto del sito.

Ciò nonostante, dal punto di vista puramente **grafico** il sito trasmette ancora l'impressione di "landing generata da un assistente" e non di "vetrina di una divisione deep-tech di IFEVS con 15 domande brevettuali e una traiettoria societaria". Al netto del placeholder già noto, la sensazione deriva da quattro cause concrete, individuabili nel codice, **non dal contenuto**:

1. **Pagine di profondità clonate.** `architecture`, `technology`, `applications`, `research`, `company` sono letteralmente lo stesso template `[H1 centrato + intro + griglia di card]`, perfino con lo stesso inline style `min-height: 70vh; padding: 8rem 0;`. La mancanza di variazione è ciò che si percepisce come "generato".
2. **Incoerenza visiva tra home e pagine interne.** Solo `index.html` e `404.html` montano `.bg-gradient-mesh` e `body::before` (griglia engineered). Le altre 5 pagine sono piatte su sfondo uniforme: si passa da "premium dark" a "documento".
3. **Gerarchia tipografica appiattita.** Una sola scala `--fs-h2` per tutti i `section-title`, H1 delle pagine interne più piccolo dell'H1 della home, `.app-card h4` che salta la gerarchia (da h2 a h4 senza h3). Nessuna distinzione tra titoli di sezione, titoli di card e micro-label.
4. **Assenza di "evidenza".** Il posizionamento (12 IT + 2 EPO + 1 PCT, articoli peer-reviewed, partnership IFEVS) è sepolto in paragrafi di 60 parole. Niente numeri in grande, niente pull-quote, niente eyebrow, niente icone, niente blocchi "metrica".

Il rapporto "infrastruttura solida / superficie grafica debole" è esattamente il motivo per cui un sito ben costruito *sembra* fatto in fretta — a prescindere dal placeholder dell'hero.

Il report segue un percorso: **diagnosi → proposta per componente → priorità operative**. Le proposte rispettano tutti i vincoli di `for_agents.md`: sito statico, zero framework, dark theme, mobile-first, claim discipline, testi congelati. Una sezione dedicata (§3.1 e §4) analizza nel dettaglio l'animazione V10, dato che è l'elemento centrale del progetto.

---

## 1. Cosa ha di buono (da conservare)

Prima di dire cosa cambiare, è leale fissare cosa **non va toccato**:

| Elemento | Perché tenerlo |
|---|---|
| `:root` con token (colori, spacing, radius, z-index, tipografia fluida) | Base solida e coerente con §5 di `for_agents.md` |
| Self-hosting di Inter/Outfit (`@font-face` variabili, subset latin) | GDPR-clean, performante, già fatto (T-4.1) |
| Mobile-first con media query `min-width` (T-2.6) | Corretto e mantenuto |
| `prefers-reduced-motion` e `:focus-visible` globali (T-2.4) | Accessibilità rispettata |
| `.js .reveal` gating (T-2.5) | Contenuto visibile senza JS — buono per SEO/GEO |
| `skip-link`, landmark `<header>/<nav>/<main>/<footer>` | Struttura semantica corretta |
| Palette `--accent-cyan/blue/purple` con contrasto verificato (T-2.5: 7.7:1) | Accessibile, va conservata |
| Partial `header.html`/`footer.html` + `build.mjs` (opzione A, §3.4) | DRY senza costo runtime |

**Conclusione parziale:** il *design system* c'è ed è onesto. Il problema non è la base tecnica, è lo *strato espressivo* che ci sta sopra.

---

## 2. Diagnosi: perché "sembra generato"

### 2.1 Hero: la *neural sphere* è un placeholder provvisorio (già pianificata la sostituzione)

Nel CSS (`styles.css:471-551`) la `.neural-sphere` è composta da tre `.ring` animati con `rotateX/rotateY/rotateZ` + un `.core` con `pulseCore` 3s. Esteticamente è un "atomo cyber" generico.

**Precisazione importante (fonte committente, 2026-07-20):** questa sfera **non è una scelta stilistica ma un placeholder**. L'elemento centrale del sito è l'animazione Reflex–Policy (prototipi `animazione_hero_prototipo_V10.html` desktop e `animazione_hero_prototipo_M1.html` mobile). La sfera sarà sostituita da un'immagine **statica estratta dall'animazione** (freeze-frame), con integrazione successiva del componente animato completo (D-6, `for_agents.md`).

Di conseguenza, qui non si tratta di "cosa mettere al posto della sfera" (la decisione è già presa: il diagramma Reflex–Policy), ma di:

- **quale fase del V10 usare come freeze-frame** per la home statica (vedi §3.1.B),
- **come gestire il passaggio freeze-frame → animazione completa** quando il componente sarà integrato,
- **come si comporta il freeze-frame su mobile** (il V10 è desktop-only; il freeze-frame va rigenerato o adattato per il viewport mobile).

L'analisi del V10 come componente è in §3.1 e §4 (opinione estesa).

### 2.2 Pagine interne = template duplicato

Confronto diretto fra i 5 file di profondità (estratto semplificato):

```html
<!-- architecture.html, technology.html, applications.html, research.html, company.html -->
<main id="main" style="min-height: 70vh; padding: 8rem 0;">
  <section><div class="container reveal">
    <h1 class="section-title center">…</h1>
    <p class="section-intro …">…</p>
  </div></section>
  <section><div class="container reveal-delay">
    …griglia di .glass-card o .app-card…
  </div></section>
</main>
```

**Identico, pagina per pagina.** Questo è l'aspetto che più di tutto comunica "chatbot": ogni pagina sembra un'istanza dello stesso stampo. Manca:

- un **hero variato per pagina** (immagine/diagramma/numero differente),
- un **ritmo verticale differenziato** (sezioni full-bleed alternate a sezioni strette),
- **componenti specifici** (es. timeline per Research, comparison table per Technology, mappa applicativa per Applications, scheda team/company per Company).

Inoltre le pagine interne **non montano `.bg-gradient-mesh` né `body::before`**: solo `index.html` e `404.html` lo fanno. Risultato: si passa dalla home (premium, con glow + griglia engineered) a una pagina interna (piatta,Uniforme) e l'occhio percepisce un "salto di qualità".

### 2.3 Tipografia: una sola dimensione per troppi titoli

La scala tipografica definita in `:root` è fluida e corretta:

```css
--fs-h1: clamp(2.75rem, 6vw, 5rem);
--fs-h2: clamp(1.9rem, 4vw, 2.75rem);
--fs-h3: clamp(1.15rem, 2.5vw, 1.5rem);
--fs-h4: clamp(1.05rem, 1.5vw, 1.25rem);
```

Ma nell'uso pratico:

- `.section-title` usa sempre `--fs-h2`, sia per l'H1 delle pagine interne (`<h1 class="section-title center">`) sia per gli H2 di sezione. **L'H1 di "Architecture" è grande quanto un H2 di sezione.** Nessuna gerarchia percepita.
- La home ha `<h1 class="hero-title">` a `--fs-h1`; le pagine interne hanno `<h1 class="section-title">` a `--fs-h2`. **H1 della home ≈ 1.8× H1 delle altre pagine.**
- In `.app-card` si passa da H2 (sezione) a **H4** (`<h4>Robotics and Humanoids</h4>`) senza H3 intermedio: salto gerarchico.
- `.hero-title` viene ridichiarata tre volte nel CSS (riga 442 base, riga 979 responsive, riga 1067 design pass) con valori diversi: 2.2rem → 3rem → 4rem → `var(--fs-h1)`. *Fragile e ridondante.*

### 2.4 Mancanza di "evidenza" credibilità

Elementi che un sito deep-tech usa per dichiarare autorevolezza e che qui mancano tutti:

- **Numeri in grande.** "12 Italian patent applications, 2 EPO, 1 PCT" è una frase sepolta nel paragrafo IP. Dovrebbe essere una *metric band* con 3 numeri grandi.
- **Pull-quote.** Lo statement identitario *"REFLEXORA brings intelligence closer to the event…"* è un paragrafo come un altro.
- **Eyebrow / kicker.** La classe `.eyebrow` è definita nel CSS (riga 1019) ma **mai usata** nelle pagine.
- **Iconografia nelle card.** Le `.app-card` hanno solo testo; nessun marker visivo che distingua "Robotics" da "Energy Storage".
- **Affiliazione IFEVS.** Una delle Few credibilità esterne disponibili, eppure è una riga grigia nel footer.
- **Glossario visivo.** I termini Reflex Layer / Policy Layer / EROIE / event-action trace sono il cuore della *claim discipline* (§0.12), ma non hanno un trattamento grafico dedicato.

### 2.5 CSS cresciuto a strati, non consolidato

Il file `css/styles.css` (1292 righe) è leggibile ma contiene **tre passate di override** che si sovrappongono:

- base originale (dark theme, neural sphere, glassmorphism),
- pass T-2.x (token, mobile-first, fluid type),
- "DESIGN REFINEMENT PASS — 2026-07-12" (eyebrow, badge, hairline, nav active).

Sintomi concreti di duplicazione:

- `.btn-primary` definito due volte (riga 328 e 351),
- `.app-card` definito due volte (riga 776 e 1118),
- `.glass-card` definito due volte (riga 553 e 1093),
- `.hero-title` definito tre volte (riga 442, 979, 1067),
- `.section-title` definito due volte (riga 594 e 1078),
- `.navbar.scrolled` definito due volte (riga 167 e 1167).

Non è un bug, ma è *debito tecnico visivo*: quando una proprietà viene vinta da selettorità, il risultato a schermo dipende dall'ordine del file. Per chi mantiene (e per l'agente successivo) è fonte di regressioni.

### 2.6 Micro-segnali

- Il `<header class="navbar">` ha `padding: 1.5rem 0` e `1rem 0` da scrolled: **non c'è un contenitore orizzontale allineato al `.container`** (max 1200px). Su wide-screen il logo e i link "galleggiano" ai margini del viewport.
- `.btn-primary { width: 100% }` su mobile (T-2.6) è corretto in hero, ma fa apparire bottoni giganti in `.cta-container` inline (es. *Contact* page, dove il `mailto:` occupa tutta la riga anche quando non dovrebbe).
- Il footer `.footer-bottom` accatasta 5 righe (`legal-id`, 3 link, copyright) senza gerarchia: sembra un "tappeto" legale invece di una chiusura elegante.
- Le `.glass-card` hanno un'animazione *shine sweep* (`.glass-card::before` che viaggia da `left: -100%` a `left: 200%`). È un effetto luminoso che ha poco senso su una *research division*: trasmette "prodotto consumer" non "IP platform".

---

## 3. Proposta per componente

Le proposte sono ordinate per **impatto percepito / sforzo**. Ogni voce indica: file coinvolti, rispetto dei vincoli (`for_agents.md`), e note di implementazione.

### 3.1 Hero: dalla *neural sphere* al diagramma Reflex–Policy (priorità: altissima)

**Contesto (precisazione committente 2026-07-20).** La sfera è un placeholder. L'elemento centrale del sito è l'animazione V10 (desktop) + M1 (mobile), già prototipata. La sfera sarà sostituita da un'immagine **statica estratta dal V10** (freeze-frame), con integrazione successiva del componente animato completo (D-6). Le tre azioni conseguenti:

#### 3.1.A — Freeze-frame statico (azione immediata, sostituisce la sfera)

Estrarre dal V10 un'immagine statica (PNG/WebP, meglio SVG inline o `<img>` da SVG rasterizzato) che funge da nuova `.hero-visual`. Suggerimenti su **quale fase catturare**:

- **Fase 5 (Execute bounded action)** è la candidata migliore: mostra contemporaneamente Policy → Reflex → Power path → Physical system, con il `.rp-armed` (anello colorato sul nodo iniettore) e la cella selezionata one-hot. È lo *snapshot* che racconta il "contratto elettronico" (§0.12 di `for_agents.md`) in un colpo d'occhio.
- **Alternativa: fase 7 (Report evidence)** se si vuole enfatizzare l'osservabilità (event-action trace che risale al Policy Layer) — più "ricerca", meno "prodotto".
- **Sconsigliata la fase 1** (solo flussi di sensing): visivamente povera, non distingue il V10 da un diagramma a blocchi qualunque.

Dettagli operativi per il freeze-frame:
- **Sorgente:** il solo sottoalbero `.rp` del V10 (vedi marcatori `<!-- COMPONENTE DA INTEGRARE -->` / `<!-- FINE COMPONENTE -->`); l'harness (`.art-head`, `.frame`, `.frame__flag`, `.harness-hint`) va escluso — è materiale interno IFEVS, codificato in ambra (§9 di `for_agents.md`).
- **Vista:** la vista `system` (PV+battery integrati) è più ricca e rappresentativa; le viste `pv` e `battery` sono derivate e vanno bene per pagine di profondità ma non per l'hero.
- **Mobile:** il V10 è desktop-only (viewBox 1260×728). Per il freeze-frame in hero mobile serve una **seconda estrazione** dal M1 (viewBox 360×490, contratto generico a 4 nodi), non uno scaling del V10 che diventerebbe illeggibile (testi a 3,6–4,8px a 375px, come già notato in D-6).
- **Attributi `data-ph`:** nel freeze-frame impostare `data-phase="5"` (o la fase scelta) **e aggiungere la classe `.is-static`** al container `.rp`: il CSS del componente (`animazione_hero_prototipo_V10.html:303`) forza `[data-ph] { opacity: .85 }` con `.is-static`, mostrando tutti gli elementi della fase senza animazione. Questo permette di riusare la stessa SVG senza riscriverla.
- **Formato:** preferire SVG inline (niente richieste extra, scalabile, stampabile). Se si rasterizza, WebP a 2× per retina.

#### 3.1.B — Integrazione del componente animato completo (azione differita, D-6)

Quando il componente V10+M1 viene fuso nel singolo `.rp` responsive (breakpoint `max-width: 900px` + `matchMedia`, vedi D-6 di `for_agents.md`), il freeze-frame della home viene **sostituito dall'animazione vera e propria** o usato come poster/preview iniziale (`<img poster>` concettuale) mentre il JS carica. Pianificare:
- pagine candidate all'animazione completa: `architecture.html` (il posto più naturale, dove il contratto è spiegato) oppure una **nuova sezione full-bleed** della home subito sotto l'hero;
- in `index.html` hero mantenere il freeze-frame (l'animazione sotto l'hero H1 sottrae attenzione al copy);
- considerare una **versione "ambient" loop-only** (no switcher, no rail, no pannelli) per la home e la versione **"studio" completa** (switcher + rail + pannelli + demo Hard Inhibit) in `architecture.html` — il V10 oggi accoppia le due cose, ma il pubblico della home (investitori) vuole un loop elegante, quello della pagina di profondità (scienziati) vuole i controlli.

> Vincoli rispettati: sito statico, zero framework, niente UA sniffing (D-6), claim discipline (le etichette del V10 sono testi verbatim dalle fonti R7 e feedback direzione, §0.12).

### 3.2 Uniformare il " substrato" visivo tra home e pagine interne (priorità: alta)

Aggiungere `.bg-gradient-mesh` e la relativa `<div>` + il `body::before` della griglia engineered **a tutte le pagine** (non solo `index.html` e `404.html`). Modifica minima (rigenerabile via `build.mjs`), impatto forte: la percezione di "premium dark" si estende a tutto il sito.

Verificare che il `body::before` attualmente definito solo logicamente nel CSS sia effettivamente presente su ogni documento (controllare selettore).

### 3.3 Differenziare le pagine interne (priorità: alta)

Per uscire dal "template clonato", ogni pagina di profondità dovrebbe avere **almeno un componente specifico** che le altre non hanno:

| Pagina | Componente specifico proposto |
|---|---|
| `architecture.html` | Il diagramma Reflex–Policy (V10 o SVG statico, vedi 3.1) come *hero visivo*; le 6 caratteristiche distintive come *anchored cards* con `id` per deep-link (utile per GEO: "Reflex–Policy bounded authority → URL#bounded-authority"). |
| `technology.html` | **Tabella comparativa** "Conventional vs Spintronic vs Emerging" con 3 colonne (pro, contro, status qualifica) invece di due `.glass-card` parallele. Le tabelle in `overflow-x:auto` su mobile sono già previste dal §5.0. |
| `applications.html` | Icona + *eyebrow* per ciascuna delle 6 card; trasformare la griglia in un layout "bento" asimmetrico (card grandi e piccole) invece della griglia 3-col uniforme. |
| `research.html` | **Timeline** delle pubblicazioni (article peer-reviewed → perspective papers → preprint) con anno e status. Niente card, niente griglia: solo una linea verticale con tappe. |
| `company.html` | **Stat block** "12 IT · 2 EPO · 1 PCT" + "research division of IFEVS" con marchio IFEVS visibile (non solo link testuale). |

Sono tutte realizzabili con il catalogo componenti già presente (§5.4) più uno o due componenti nuovi (`.stat-band`, `.timeline`, `.compare-table`).

### 3.4 Ripristinare la gerarchia tipografica (priorità: alta)

Modifiche mirate al CSS:

1. **H1 delle pagine interne** deve usare una nuova classe `.page-title` a `--fs-h1` (non `section-title`). Visivamente distinto dal titolo di sezione.
2. **H1 della home** (`.hero-title`) resta a `--fs-h1` ma **con un sottotitolo/eyebrow** che dichiara cosa fa REFLEXORA, non solo il nome brand. Oggi l'unico H1 della home è "REFLEXORA": il lettore non sa cosa vende l'azienda finché non legge il paragrafo.
3. **Eliminare le triple dichiarazioni** di `.hero-title` (riga 442, 979, 1067): una sola, a `var(--fs-h1)`, con override responsive `min-width`.
4. **Aggiungere `h3` intermedi** nelle `.app-card` (oggi saltano da H2 a H4): portare `<h4>` a `<h3>` o introdurre un livello visivo intermedio.
5. **Variare `--fs-h2`** fra sezioni principali e sottosezioni (es. `.section-title--lg` per le 2-3 sezioni top, `.section-title--sm` per i blocchi interni).

### 3.5 Introdurre "evidence components" (priorità: alta)

Tre componenti nuovi, leggeri, che trasmettono credibilità senza inventare claim:

**`.stat-band`** — fascia orizzontale con 3-4 numeri grandi (font Outfit 900, gradient text) + label mono sotto. Da inserire in home (sezione IP) e in `company.html`:
```
[ 12 ] IT patent applications   [ 2 ] EPO   [ 1 ] PCT   [ 8 ] application domains
```

**`.pull-quote`** — blocco tipografico per lo statement identitario, con virgolette grandi e bordo laterale cyan. Trasforma una frase sepolta in un momento editoriale.

**`.term-card`** — piccolo riquadro "glossary" inline (border hairline + eyebrow mono "TERM") per ogni termine chiave (Reflex Layer, Policy Layer, EROIE, event-action trace). Serve anche alla GEO (§10 glossario): estrazione LLM-friendly.

> Vincoli rispettati: i numeri 12+2+1 sono già confermati in `for_agents.md` §4; le definizioni dei termini sono nel §10. Nessun claim nuovo.

### 3.6 Consolidare il CSS (priorità: media, ma ad alto ritorno per chi mantiene)

Azioni meccaniche, nessun cambiamento visivo:

1. **Unificare le dichiarazioni duplicate**: portare `.btn-primary`, `.app-card`, `.glass-card`, `.hero-title`, `.section-title`, `.navbar.scrolled` a una sola definizione ciascuna. Il "design pass 2026-07-12" deve diventare la base, non un override.
2. **Spostare in token** i rimanenti valori "magici" (es. `padding: 2.5rem` delle glass-card → `var(--space-6)`; `border-radius: 20px` → `var(--radius-lg)`).
3. **Rimuovere l'effetto *shine sweep*** da `.glass-card` e `.app-card` (le pseudo-element `::before` con `skewX(-25deg)`): è un vezzo consumer che confligge con il tono *research division*.
4. **Documentare a sezioni** il file: oggi i commenti `/* ============ */` ci sono ma il pass 2026-07-12 non è separato nettamente. Un indice all'inizio del file aiuta gli agenti successivi.

### 3.7 Navbar e contenitori (priorità: media)

- Avvolgere `.nav-container` in un `.navbar-inner` con lo stesso `max-width: 1200px; padding: 0 2rem;` del `.container`. Oggi la navbar ha `padding: 1.5rem 0` senza inner max-width: su wide-screen il logo e i link si allargano al viewport.
- Aggiungere un **logo mark** minimale accanto al wordmark "REFLEXORA.AI" (es. un glifo derivato dal diagramma Reflex–Policy: due archi concentrici). Anche solo un'immagine vettoriale da 1 KB distingue il brand dal "testo centrato".
- Rendere l'`active` state della nav più evidente: oggi è una sottolineatura gradient di 2px sotto il link. Aggiungere un *pill background* `--surface-2` sul link attivo, oltre alla linea.

### 3.8 Footer (priorità: media-bassa)

Il footer è informative ma visivamente farraginoso. Proposta di riorganizzazione a **3 colonne desktop / stack mobile**:

- Colonna 1: brand + tagline + affiliazione IFEVS (con piccolo logo IFEVS).
- Colonna 2: nav secondaria (Architecture, Technology, …, Contact).
- Colonna 3: contatto (`contact@reflexora.ai`) + link alle pagine legali.
- Footer-bottom: solo riga legale art. 2250 + © in una riga sola, più piccola.

### 3.9 Micro-dettagli (priorità: bassa, cumulativa)

- **`prefers-color-scheme: light`**: oggi il sito è dark-only. Per un pubblico investor/scientifico che legge a lungo, considerare un *token flip* verso un tema light opzionale. Non obbligatorio, ma da valutare.
- **`scroll-padding-top`** su `html` per compensare la navbar fissa quando si naviga via anchor (es. `#bounded-authority`).
- **`text-wrap: pretty`** (supporto moderno) sui paragrafi lunghi per evitare orfani tipografici.
- **Stato hover dei link nel corpo testo**: oggi i link inline non hanno trattamento (solo `.legal-col a`). Aggiungere `border-bottom` hairline on hover.
- **Pulsanti full-width**: ridefinire `.btn-primary { width: 100% }` su mobile solo in `.hero-actions`, non globalmente, per evitare bottoni oversized in `.cta-container` inline.

---

## 4. Opinione estesa sul prototipo `animazione_hero_prototipo_V10.html`

Questa sezione non è una diagnosi del sito ma un'**analisi critica del componente** che diventerà l'elemento centrale del sito (precisazione committente 2026-07-20). È basata sulla lettura completa del file (1177 righe, ~85 KB, standalone desktop-only).

### 4.1 Giudizio complessivo

**V10 è un ottimo prototipo, ben al di sopra della media dei "diagrammi animati" che si vedono sui siti deep-tech.** Non è decorativo: è un **diagramma tecnico interattivo** che racconta una sequenza causale reale (7 fasi: Detect → Classify → Verify permission → Reflex decision → Execute → Validate → Report). È esattamente il tipo di visual che manca alla maggior parte dei siti di IP/research, che si limitano a stock illustration. Trasmette "chi ha fatto questo capisce il dominio" — che è proprio il messaggio di una research division con 15 domande brevettuali.

Il **punto di forza più rilevante** è la **coerenza claim-discipline** (§0.12): tutti i 12 termini congelati dalla direzione sono usati letteralmente, e il testo del pannello disclosure (riga 993) contiene la formulazione di sicurezza sulla prior art: *"The lowest-voltage cell is not automatically selected. The BMS first determines eligibility; the Reflex then selects one eligible destination..."*. È raro trovare un visual che rispetti così bene la *claim discipline*.

### 4.2 Punti di forza specifici

1. **Famiglia di 3 viste sincronizzate** (`SYSTEM | PV SIDE | BATTERY SIDE`): il meccanismo `data-view` + il fatto che **la fase e la modalità si preservano al cambio vista** (riga 1088, `paintPhase()` richiamato in `setView`) è un'accortezza rara. Chi cambia vista mentre è in fase 5 resta in fase 5 e vede gli elementi equivalenti della nuova vista. Ottima UX.
2. **Rail cliccabile delle 7 fasi** (riga 934-942): non è solo un indicatore passivo, è un **navigatore**. Click = modalità studio → apre il pannello disclosure con il testo verbatim. `aria-current="step"` corretto. Tap target `min-height: 54px` superano i 44px WCAG.
3. **Progressive disclosure ben calibrato**: di default l'animazione scorre in loop (chilometrica ma leggibile); al click su una fase si entra in modalità studio con il testo esplicito. Risolve il dilemma "spiegare tutto vs. non affogare il lettore".
4. **Accessibilità presa sul serio**:
   - `prefers-reduced-motion` → `.is-static` (riga 1108): tutti gli elementi `[data-ph]` a `opacity: .85`, niente animazione, rail resta cliccabile. **L'informazione non dipende dal motion** — requisito fondamentale che il 90% dei siti animati ignora.
   - Pause/Play off-screen via `IntersectionObserver` (riga 1114) + `visibilitychange` (riga 1120): non spreca CPU/batteria quando non è visibile. Requisito WCAG 2.2.2 (pause, stop, hide) soddisfatto.
   - Focus visibile (`:focus-visible` con `box-shadow: 0 0 0 3px rgba(0,242,254,.35)`) su switcher, rail, pannello.
5. **Semantica SVG**: ogni `<svg>` ha `<title>` + `<desc>` con descrizione testuale della vista. Per uno screen reader il diagramma ha un'etichetta significativa, non un "image".
6. **Demo Hard Inhibit** (riga 1132-1170): mostra il caso di contenimento cyber-fisico (corollario della §0.12 — cyber-physical containment). È il tipo di "caso limite" che distingue una architettura seria da una demo generica. Limitato alla vista battery (dov'è significativo) e disattivato in reduced-motion.
7. **Igiene del codice**: IIFE scoped, niente globale, niente dipendenze, `escapeHtml` per il pannello (riga 1076). Zero richieste esterne, 0 cookie, GDPR-clean.

### 4.3 Punti di attenzione / debolezze

1. **Mobile assente (ma pianificato in M1).** Il V10 è esplicitamente desktop-only (viewBox 1260×728, ~1136px fascia). Senza il ramo M1, a 375px il diagramma scala a ~0,30 con testi di 3,6–4,8px — illeggibile. **È già gestito in D-6** (fusione responsive via `matchMedia`), ma va considerato un punto fermo: V10 e M1 **non sono alternativi, sono complementari**, e il componente pubblicato deve contenere entrambi i rami. L'attuale separazione in due file è un debito di prototipazione, non una scelta architetturale.
2. **Densità informativa altissima.** È al tempo stesso il pregio e il limite. La vista SYSTEM contiene ~40 elementi SVG (nodi, flussi, chip, etichette, legenda, safe state). Su monitor 1280px è leggibile; su 1024px (laptop piccolo) comincia a essere affollata; su 1440p è perfetta. Suggerimento: in `architecture.html` prevedere un **contenitore che non sia full-width della pagina** ma della larghezza del `.container` (1200px) con il componente che occupa 100% del contenitore. Oggi nel prototipo il `.frame--band` è fisso a 1136px: nel sito deve diventare fluido (`width: 100%; max-width: 1136px`).
3. **Complessità del JS di demo Hard Inhibit** (riga 1132-1170): 3 timeout concatenati con stato manuale (`demoOn`, `demoTimers`, `endDemo`). Funziona, ma è il punto più fragile del componente: se l'utente clicca rapidamente, o passa a un'altra vista durante la demo, o chiude la pagina, la gestione degli stati può race-conditionare. Da testare attentamente prima della pubblicazione; considerare una macchina a stati esplicita (`idle | playing | study | demo`) invece di tre booleani.
4. **Ridondanza SVG tra le 3 viste.** Le tre `<svg>` ridichiarano la legenda, il safe state, il blocco Policy quasi uguali (stesso blocco `POLICY / SUPERVISORY LAYER` compare 3 volte, identico). È comprensibile (sono self-contained), ma quando si integra nel sito il **peso inline del componente sarà ~80-100 KB** di SVG ripetuto. Valutare un ` <defs>` condiviso (alcuni marker come `a5neu`, `a5pol` sono già in `<defs>` solo della vista system; spostarli fuori e referenziarli ridurrebbe il peso).
5. **Switcher view + demo + pause in overlay** possono collidere spazialmente su viewport intermedio (es. 1100px di larghezza fascia). Il `.rp-ctl` (pause) è in `top:4px right:4px`, il `.rp-ctl--demo` in `top:4px left:4px`, lo switcher centrato in alto. Funziona a 1136px; verificare a 1024px e 1136px-esatti.
6. **Legenda diversa per vista.** SYSTEM ha 7 voci (Policy, Reflex, Evidence, Power, Feed, low state, eligible, selected), PV ha 6 + 2 testi, BATTERY ha 5. È coerente col contenuto di ciascuna vista, ma chi naviga tra le 3 viste potrebbe disorientarsi nel vedere la legenda cambiare. Considerare una **legenda unificata e fissa** (magari outside-stage, nel rail o in fondo) con tutti i 7 simboli, indipendente dalla vista.
7. **Statement "Signals decide. Power electronics carry energy."** (riga 610, 754, 917) ripetuto 3 volte, una per vista. Va bene come *tagline* di chiusura, ma ripeterlo identico sotto ogni SVG è ridondante nel componente integrato (dove il cambio vista non ricarica la pagina). Metterlo una volta sola, fuori dallo stage.
8. **I 9px dei sub-label Policy** (già segnalati in `for_agents.md` changelog V9/V10: *"i 2 sub-label Policy restano i più piccoli (9px) per vincolo geometrico"*) sono effettivamente al limite della leggibilità anche su desktop con display DPI standard. Una volta nel sito, dove il componente vivrà in un container e non full-window, il problema può solo peggiorare. Se la direzione ha sciolto il vincolo terminologico (12 termini confermati), accorciare "Optimize · Learn · Plan" / "Safety · Eligibility · Limits" a 2 elementi ciascuno permetterebbe di salire a 11-12px.
9. **Naming `rp__band`** (riga 369, 623, 764): la classe è usata nelle 3 viste SVG ma il CSS ha regole per `.rp__tall` (il ramo mobile M1, vedi D-6) che non sono nel V10. Quando si farà la fusione, assicurarsi che le classi `band` e `tall` siano effettivamente alternate dal media query e che il `.rp__view` display-none non si porti dietro stili `tall` residui.

### 4.4 Suggerimenti per l'integrazione nel sito

Quando V10+M1 entreranno nel sito (D-6), l'operazione non è "copia-incolla il componente" ma una **piccola integrazione**:

1. **Estrazione**: prendere il solo sottoalbero `.rp` (marcatori `<!-- COMPONENTE DA INTEGRARE -->` / `<!-- FINE COMPONENTE -->`), scartando l'harness ambra.
2. **CSS scoped**: il componente usa `--rp-*` custom properties (riga 87-97). Sono locale al `.rp` e non collidono con i token globali del sito (`--accent-cyan` ecc.) — **decisione giusta**, va mantenuta. Eventualmente mappare `--rp-reflex: var(--accent-cyan)` per coerenza, ma non è obbligatorio (i nomi `rp-*` aiutano la manutenibilità).
3. **Posizionamento**: nel sito, il `.rp` non deve essere `position: relative` figlio di un `.frame` ma di una `<section>` full-width. Verificare che `width: 100%; height: 100%` (riga 99) si adatti al nuovo contenitore (che deve avere un'altezza definita, es. `aspect-ratio: 1260/800` o un'altezza fissa tipo `min-height: 600px`).
4. **Prevenire CLS**: l'animazione occupa molto spazio verticale (~800px desktop). Assegnare `aspect-ratio` o un `min-height` al contenitore **prima** del load del JS per evitare layout shift.
5. **`scroll-padding-top`** su `html` per compensare la navbar fissa (già suggerito in §3.9), così gli anchor interni non finiscono sotto la navbar.
6. **Caricamento**: il JS del V10 è in fondo al body e parte subito con `setTimeout(tick, PHASES[i].dur)` (riga 1110). Nel sito, dove ci sono altri script (`main.js`), incapsulare in un unico IIFE già fatto; aggiungere `requestIdleCallback` o `DOMContentLoaded` se si osservano jank al primo paint.
7. **Pagina ospite**: `architecture.html` è la candidata naturale (il testo del contratto è lì). In home, meglio il freeze-frame statico (§3.1.A) — non rubare attenzione al copy, non impone loop motion all'utente che sta leggendo il posizionamento.
8. **Versione "ambient" vs "studio"** (suggerimento nuovo, non nel prototipo): considerare un parametro `data-mode="ambient|study"` sul `.rp`. In `ambient` (home): niente switcher, niente rail, niente pannello, solo il loop fase 1→7 con le etichette rail come didascalia passiva. In `study` (architecture): switcher + rail + pannello + demo. Si riutilizza lo stesso SVG, cambia solo quali controlli sono `display: none`. Questo evita di manutenere due SVG diversi e risolve il problema di "troppi controlli in home".

### 4.5 Opinione sintetica (TL;DR)

V10 è **pronto per l'integrazione** con interventi minori (fluidità del container, fusione M1 per mobile, valutazione di una modalità "ambient" per la home). Non è un prototipo grezzo: è un componente maturo, accessibile, claim-disciplined, che **distinguerà reflexora.ai dai siti deep-tech generici**. La direzione ha fatto bene a investire 9 iterazioni (V2→V10) su questo visual: è l'asset grafico più importante del progetto, molto più di qualunque fotografia stock o icona.

L'unico **vero rischio** è la densità: nel sito, dove il componente non avrà il monitor intero ma una porzione di pagina, va **dimensionato con cura** e **contestualizzato con testo** (eyebrow, titolo, didascalia) per orientare il lettore prima che entri nel dettaglio dei 7 nodi. Un visual così ricco senza cornice editoriale può disorientare chi arriva "freddo".

---



---

## 5. Priorità operative (cosa fare prima)

Se fosse un sprint, l'ordine di lavoro secondo il rapporto *percezione/sforzo*:

1. **Estrarre il freeze-frame dal V10** (vista system, fase 5, `.is-static`) e sostituire la neural sphere nella home, con una seconda estrazione dal M1 per il mobile. → *Sostituzione del placeholder già pianificata; impatto massimo, sforzo meccanico.*
2. **Integrazione del componente animato completo V10+M1** in `architecture.html` (o sezione full-bleed della home) rispettando D-6. → *Differisce per la fusione responsive; nel frattempo il freeze-frame tiene il posto.*
3. **Estendere `.bg-gradient-mesh` + `body::before`** a tutte le pagine. → *Coerenza cross-pagina in 1 task.*
4. **Ripristinare la gerarchia tipografica** (`.page-title`, eliminare triple dichiarazioni). → *Impatto alto, sforzo meccanico.*
5. **Aggiungere `.stat-band` + `.pull-quote`** in home e company. → *Trasforma "paragrafo sepolto" in "credibilità visibile".*
6. **Differenziare le pagine interne** (timeline per research, compare-table per technology, bento per applications).
7. **Consolidare il CSS** (rimuovere duplicazioni, spostare valori magici in token).
8. Micro-dettagli (navbar inner max-width, logo mark, footer a 3 colonne).

Le voci 1-5 sono *quick win* ad alto impatto. La 6-8 sono *strutturali* e possono essere distribuite fra agenti (Gemini per il meccanico, Sonnet per i componenti nuovi, Opus per la *claim discipline* visiva — come da §2 di `for_agents.md`).

---

## 6. Rispetto dei vincoli (audit)

Tutte le proposte sono compatibili con `for_agents.md`:

| Vincolo | Compatibilità |
|---|---|
| §0.5 Sito statico, zero framework, zero CDN | ✅ Tutto vanilla HTML/CSS/JS, font già self-hosted |
| §0.8 Mobile-first | ✅ Tutti i nuovi componenti proposti partono da mobile |
| §0.9 Testi congelati | ✅ Non si riscrive il copy, si impagina diversamente |
| §0.12 Claim discipline | ✅ Niente numeri non validati; le metriche proposte (12+2+1, 8 domini) sono già confermate in §4 |
| §5 Design system a token | ✅ I nuovi componenti usano token esistenti, ne aggiungono solo lo stretto necessario |
| §5.5 Motion & accessibilità | ✅ Mantenuto `prefers-reduced-motion`, focus visibile, skip-link |
| §9 Aruba hosting | ✅ Nessuna dipendenza runtime, tutto deployabile via FTP |
| D-6 Animazione V10/M1 | ✅ L'integrazione proposta rispetta la decisione (singolo componente responsive, niente UA sniffing) |

---

## 7. Riferimenti di settore (per orientamento, non per copiare)

Per calibrare il "tono editoriale deep-tech" auspicato, senza fossilizzare riferimenti specifici che potrebbero invecchiare, i filoni da tenere presenti come *mood* (non come template da clonare):

- Siti di **research labs** (industrial o accademic) che usano diagrammi tecnici nativi come protagonisti, non stock illustration.
- Siti di **hardware/IP companies** che mettono i numeri chiave (brevetti, domini, partner) in stat band evidenti.
- Editorial design **"engineering sobrio"**: dark theme con un solo accento, tipografia forte, molto bianco respiro, niente glow uniforme.

La direzione è: **meno "AI startup 2021", più "research division con IP seria"**.

---

## 8. Note finali

- Il report è **only-analysis**: nessun file HTML/CSS/JS è stato modificato.
- Le proposte sono ordinate per priorità ma sono *indipendenti*: possono essere eseguite in ordine diverso o in parallelo da agenti diversi (§2 di `for_agents.md`).
- Per ogni modifica che si deciderà di fare, ricordare la regola §0.1: aggiornare `for_agents.md` (stato task, changelog, dashboard) e §0.7: mai lasciare il sito rotto tra un task e l'altro.
- I numeri (12 IT + 2 EPO + 1 PCT, 8 domini applicativi) e le definizioni (Reflex Layer, Policy Layer, EROIE) sono presi verbatim da `for_agents.md` §4 e §10: nessun claim nuovo introdotto.

— *GLM (ZCode), 20 luglio 2026.*
