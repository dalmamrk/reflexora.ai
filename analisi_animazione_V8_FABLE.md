<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-17 · 21:56 (CEST) · Claude Fable 5</div>

---

# Analisi di design — `animazione_hero_prototipo_V8.html`

**Oggetto:** consulenza di design sul diagramma animato Reflex-Policy (esempio PV↔batteria).
**Doppio ruolo dell'artefatto:** oggi strumento di comunicazione interna (file `.html` standalone
scambiato via mail/presentazioni con la direzione); domani elemento centrale del sito reflexora.ai,
in fascia full-width ~1136px.
**Metodo:** lettura integrale del sorgente V8; rendering servito in locale e ispezionato a 1280×900;
misura **oggettiva** delle dimensioni testo renderizzate via script (non a occhio); verifica della
logica delle fasi via `matches()`/`data-ph` (il compositor del browser di preview è inaffidabile
sulle opacità animate — confermato durante l'ispezione). Fonti incrociate:
`architettura_reflex_policy_hero.md`, `appunto_perlo_terminologia_diagramma.md`,
`sintesi_analisi_design.md` (+ 4 report consulenti), `css/styles.css`, `index.html`.

---

## 1. Giudizio sintetico

Il V8 è **concettualmente maturo e tecnicamente ben costruito**: la simmetria PV-Reflex (COME) /
Battery-Reflex (DOVE) / BMS Authority (SE) è leggibile nella struttura, la sequenza causale a 7 fasi
è corretta, l'impianto `data-phase`/`data-ph` è pulito, robusto ed estendibile, l'accessibilità è
sopra la media dei diagrammi animati (Pause/Play WCAG 2.2.2, `prefers-reduced-motion`, `role="img"`
+ `desc` ricca, pausa off-screen e su tab nascosta). Il file pesa 39,6 KB, zero dipendenze: il
vincolo "leggero e trasmissibile" è già rispettato.

Il problema non è l'impianto: è che **l'artefatto spiega meno di quanto sa**. Tre carenze
strutturali lo frenano nel ruolo di strumento di comunicazione — e diventerebbero gravi nel ruolo
di elemento centrale del sito:

1. **metà dei testi è sotto la soglia di leggibilità** (misurato: 12 testi sotto i 9px renderizzati);
2. **il codice colore — l'asse semantico dell'intero diagramma — non è spiegato da nessuna parte**;
3. **la narrazione a 7 fasi esiste solo come didascalia transiente**, che sparisce in pausa e in
   reduced-motion: chi apre il file e ferma l'animazione perde la storia.

Nessuna delle tre richiede stravolgimenti: si risolvono dentro l'architettura esistente.

---

## 2. Analisi per area

### 2.1 Gerarchia visiva e leggibilità a 1136px — ⚠️ il difetto n. 1

Il viewBox è 1260×770; a 1136px la scala è **0,90**. Misura reale dei testi renderizzati:

| Font SVG | Renderizzato | Quanti testi | Esempi | Verdetto |
|---|---|---|---|---|
| 8–9,5 | **7,2–8,6 px** | 12 | `Cell Set · Imax · Tmax · Δt`, `SHARED ENERGY FEED`, `Eligibility Envelope`, ruoli Policy | **illeggibili** senza zoom |
| 10–11 | 9,0–9,9 px | 17 | `EVENT · ACTION · RESPONSE`, `BMS Safety Enable · Hard Inhibit`, zone label | sotto soglia comfort |
| 12 | 10,8 px | 13 | `Local evidence`, `Measured response`, tag operativi | al limite |
| 13–15,5 | 11,7–14,0 px | 10 | titoli nodi, caption | ok |

Tradotto: **i contenuti a più alto valore comunicativo** — i due envelope (il cuore del contratto
Reflex-Policy!), i ruoli interni del Policy layer, il feed condiviso — sono proprio quelli
illeggibili. I titoli dei box si leggono, la *meccanica* no. In una presentazione proiettata o su
un laptop 13″ il danno raddoppia. La nota storica del progetto ("a 1136px i testi salgono a ~15px")
vale solo per i titoli dei nodi.

**Serve una rifondazione della scala tipografica**: nessun testo informativo sotto ~11,5 SVG
(≈10,5px resi), envelope e chip trattati da protagonisti, micro-dettagli accorpati o promossi.
L'aumento dei corpi impone di riallargare i chip e rivedere qualche collisione — lavoro meccanico,
non concettuale.

### 2.2 Chiarezza della narrazione a 7 fasi — l'investitore capisce in 10 secondi?

**Oggi: no.** Capisce che "qualcosa scorre in un sistema a due colonne con un supervisore". La
storia — evidenza → valutazione → envelope → selezione → iniezione bounded → verifica → trace —
arriva solo a chi guarda l'intero ciclo (8,4 s + pausa) *leggendo* la caption in basso, che è:
un solo rigo, transiente, 11,7px, in fondo al diagramma, e **nascosta** in pausa/reduced-motion/no-JS.

Tre conseguenze:

- **Per la comunicazione interna:** Perlo e il revisore non possono "puntare" una fase. Discutere
  la fase 3 via mail richiede cronometrare l'animazione. Lo strumento non supporta il suo caso
  d'uso principale: la *discussione*.
- **Per l'accessibilità:** l'utente reduced-motion perde per intero la narrazione (le caption sono
  soppresse in static). La `desc` SVG copre gli screen reader, ma l'utente *vedente* con
  reduced-motion non ha nulla.
- **Per il sito:** un elemento centrale che comunica solo se guardato per 10 secondi consecutivi
  è fragile; serve uno stato "a colpo d'occhio".

**La soluzione ha più valore di qualsiasi ritocco estetico:** un **rail delle 7 fasi sempre
visibile** (numero + label breve), con la fase corrente evidenziata e — questo è il salto di
qualità — **cliccabile**: click sulla fase = salto manuale, l'animazione riprende da lì. Il
diagramma passa da "video che si guarda" a "strumento che si esplora". Le attuali step-bars
(24×3px, non interattive) e la caption singola vengono assorbite dal rail. Costo contenuto: il
driver JS ha già `render()` centralizzato.

### 2.3 Codice colore — l'asse semantico non dichiarato

Il diagramma regge su due convenzioni cromatiche eccellenti e **mai spiegate**:

1. **5 colori di dominio**: viola=Policy/autorità, cyan=Reflex/decisione, verde=evidenza
   fisica/sensing, arancio=potenza, ambra=feed condiviso.
2. **3 stati concentrici della cella** (la trovata migliore del V8): arancio=condizione fisica
   bassa → anello viola=dichiarata eleggibile dal BMS → anello cyan=selezionata one-hot dal Reflex.
   È la *tesi dell'azienda in un'unica micro-visualizzazione* — SE (viola) prima di DOVE (cyan) —
   e il destinatario non ha modo di decodificarla.

Serve un **blocco legenda** compatto, in stile "cartiglio da disegno tecnico" (molto coerente con
l'estetica deep-tech/engineering emersa dai 4 report di design: Anduril, Physical Intelligence).
Lo spazio c'è: la colonna centrale sotto `AUXILIARY DC SOURCE` (~x 500–710, y 540–700) è
attualmente **vuota** — v. §2.5. Nota: la legenda introduce micro-testi nuovi; vanno composti solo
con vocabolario già presente nel diagramma/R7, e comunque mostrati a Perlo (v. istruzioni).

### 2.4 Equilibrio cromatico e uso degli accenti

Il sito predica "accenti sobri, non neon ovunque"; il diagramma è necessariamente policromo
(5 semantiche), ma oggi **parla tutto insieme anche da fermo**: frecce colorate su tracce grigie
statiche, chip con testi colorati sparsi, bracket cyan, tag laterali viola. Il risultato non è
caotico, ma è più rumoroso del linguaggio del sito.

Strategia consigliata: **"base quieta, fase sonora"** —

- le **tracce statiche** restano hairline neutre, ma con **frecce neutre** (oggi le punte colorate
  su linee grigie sono rumore a riposo; il colore deve arrivare *con il flusso animato*);
- zone/bracket/label di zona un gradino più discreti;
- il colore pieno appartiene alla fase attiva (flussi, highlight, anello armed).

Così lo stato di quiete somiglia a un *blueprint* (credibilità ingegneristica) e ogni fase "accende"
solo la sua semantica — il contrasto percettivo aumenta senza aggiungere saturazione.

### 2.5 Composizione, spaziatura, allineamenti

- **Colonna centrale sfilacciata:** `AUTHORIZED SOURCE INTERFACE` e `AUXILIARY DC SOURCE`
  galleggiano con un grande vuoto sotto (centro-basso morto ~180px). È l'area naturale per la
  legenda (§2.3), che ripara due difetti con una mossa.
- **Chip `EVENT · ACTION · RESPONSE`** (x495–705, y176): etichetta la traccia di ritorno ma
  fluttua senza ancoraggio visivo; il micro-testo di fase 7 (`Cell ID · Current · ΔV…`, x740 y214)
  è staccato dal suo chip e invade l'area della battery zone.
- **Margine destro ragged:** `Cell Telemetry` / `· Faults` / `Response Validation` (x1128) pendono
  fuori dalla zona batteria; il "· Faults" a capo, orfano del suo separatore, è un dettaglio da
  bozza. Da ricomporre in un blocchetto allineato con tick di connessione al canale di supervisione.
- **Refusi di finitura:** la classe `rp-tag--mid` è usata (tag `BMS Safety Enable · Hard Inhibit`)
  ma **non esiste nel CSS** → il tag è ancorato a sinistra invece che centrato; la frame-label
  dice "1136 × 620" ma il frame è alto 740; nel file viaggiano ~15 righe di **dead code** (il
  blocco JS di clonazione mobile `rpDiagramM` e il CSS `.frame--bandm`, residui del layout
  archiviato). In un artefatto che gira in direzione, i residui si notano.
- **Buoni allineamenti altrove:** la griglia dei nodi (150/760, larghezze 290) è disciplinata; le
  due zone sono specchiate correttamente; il pattern di griglia 40px con mask radiale è coerente
  con il fondo del sito.

### 2.6 Qualità del motion

- **I flussi dashed** (`rpFlow`, dashoffset −40, 1s linear) sono efficaci e leggeri. Bene i 6
  pattern di dash differenziati per semantica.
- **Il ritmo è piatto:** 1200ms uguali per tutte le fasi. Ma le fasi non pesano uguale: la 5
  (enable BMS + feed + iniezione bounded — il *climax fisico* e commerciale) dura quanto la 2
  (una valutazione locale). Un timing differenziato (climax più lungo, transizioni brevi più
  corte, pausa di fine ciclo più ampia) trasformerebbe la sequenza da metronomo a *racconto*.
- **Fase 5 senza teatro:** oggi si accendono in simultanea enable, feed e anello armed. La causalità
  interna (autorizzazione → feed → iniezione) si perde. Uno **stagger interno di poche centinaia
  di ms** (via `transition-delay`, dichiarativo, robusto anche col compositor capriccioso)
  racconterebbe la catena senza aggiungere alcun effetto. Niente glow diffuso: le direttive design
  del progetto lo vietano giustamente; il dramma qui si fa col *tempo*, non con la luce.
- **Easing:** le transizioni usano `ease` generico; il sito ha `--ease-out: cubic-bezier(.22,1,.36,1)`.
  Dettaglio, ma è coerenza di linguaggio.
- **Il pulse** (rpPulse 1.1s sui nodi in valutazione) è ben calibrato — conservarlo.

### 2.7 Coerenza col design system del sito

- **Già coerente:** palette base (#070a13, ink #f8fafc), hairline, mono per label, griglia sottile,
  focus ring cyan, radius. L'artefatto "parlerà la lingua" della fascia senza traumi.
- **Da allineare:** easing (§2.6); il muted del diagramma (`#a8b6cc`) differisce dal
  `--text-secondary` del sito (`#94a3b8`) — scelta difendibile (più chiaro = più leggibile su
  micro-corpi) ma da rendere *intenzionale* documentandola, o unificare;
- **Manca l'identità dell'artefatto:** il file viaggia via mail **senza titolo, versione, data**
  visibili nel rendering. La harness-note attuale è da prototipo. Un'intestazione sobria in stile
  sito (eyebrow monospace, titolo, meta `V9 · data`) trasforma la percezione da "bozza" a
  "documento tecnico" — e chiarisce a colpo d'occhio *quale versione* si sta commentando, problema
  reale in un processo di review iterativo a 8+ versioni. (Resta fuori dal componente integrabile.)

### 2.8 Accessibilità — punti deboli residui

Base già solida (v. §1). Restano:

1. **reduced-motion perde la narrazione** (caption soppresse in static) → risolto dal rail §2.2;
2. le **step-bars** non sono interattive né esposte semanticamente; se diventano navigazione,
   servono veri `<button>` HTML con label (`Fase 3: BMS definisce l'envelope`) e stato
   `aria-current` — altro argomento per fare il rail in HTML fuori dall'SVG;
3. il testo `#a8b6cc` sui micro-corpi regge il contrasto (≥7:1 su #080c15) ma **il contrasto non
   ripara corpi da 7px**: la leggibilità si sistema in §2.1, non scurendo/chiarendo;
4. la `desc` SVG è ottima ma statica: se il rail HTML elenca le 7 fasi, anche gli screen reader
   ne beneficiano gratis.

### 2.9 "Wow factor" percepito (investitori / partner / comunità scientifica)

- **Scienziati/ingegneri:** il pubblico meglio servito — il diagramma è onesto, denso, senza
  misticismo AI (in linea con i benchmark Physical Intelligence / documentazione tecnica). Con
  legenda e testi leggibili diventa *citabile*.
- **Investitori:** oggi vedono complessità ordinata ma non la *tesi*. I tre stati concentrici
  della cella (SE→DOVE in due anelli) sono l'argomento di investimento reso visibile — vanno
  spiegati (legenda) e celebrati (climax di fase temporizzato). Il wow qui non è spettacolo:
  è **"si capisce che c'è un contratto"**.
- **Direzione/review:** il salto percepito verrà da rail cliccabile + intestazione versione —
  lo strumento smette di essere un filmato e diventa un tavolo di discussione.

---

## 3. Priorità d'intervento

| # | Intervento | Impatto | Sforzo |
|---|---|---|---|
| 1 | Rifondazione scala tipografica (nessun testo informativo < ~10,5px resi) | **Alto** | Medio |
| 2 | Rail 7 fasi sempre visibile, cliccabile, in HTML (sostituisce caption+step bars) | **Alto** | Medio |
| 3 | Legenda colori + stati cella (cartiglio nel vuoto centrale) | **Alto** | Basso |
| 4 | Intestazione artefatto (titolo/versione/data, stile sito) | **Alto** (per l'uso attuale) | Basso |
| 5 | "Base quieta, fase sonora": frecce statiche neutre, zone più discrete | Medio | Basso |
| 6 | Timing differenziato per fase + stagger interno fase 5 + easing di sito | Medio | Basso |
| 7 | Ricomposizione margine destro + ancoraggio chip EVENT·ACTION·RESPONSE | Medio | Basso |
| 8 | Finitura: `rp-tag--mid` mancante, frame-label errata, dead code | Medio | Minimo |

Il dettaglio esecutivo (valori, coordinate, sequenza) è in
`istruzioni_animazione_V9_per_claude_code.md`.

---

*Consulenza design — Fable 5, 2026-07-17*

<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-17 · 21:56 (CEST) · Claude Fable 5</div>
