Report di Revisione del Design — reflexora.ai
Versione: 1.0 · Data: 15 luglio 2026 · Sito in review: deploy provvisorio su dalmamrk.github.io/reflexora.ai (dominio finale reflexora.ai su hosting Aruba) · Committente: IFEVS — divisione ricerca REFLEXORA

Sintesi esecutiva
REFLEXORA si colloca nel filone deep-tech / Physical AI / computing neuromorfo e spintronico, con un posizionamento ibrido fra research lab (architettura Reflex–Policy, paper su Preprints.org) e IP / patent platform (12 depositi italiani, 2 EPO, 1 PCT). Il pubblico target — investitori, partner industriali, revisori di IP, ricercatori — richiede un sito che trasmetta autorevolezza scientifica, credibilità brevettuale e concretezza ingegneristica, non un'estetica generica da "AI startup".

Il design attuale ha basi solide (design system a token, mobile-first rigoroso, accessibilità pensata, font self-hosting pianificato), ma soffre di tre limiti strategici:

L'architettura Reflex–Policy — il vero asset concettuale — non è mai visualizzata. È descritta solo in prosa densa; manca il diagramma a strati che dovrebbe essere il protagonista visivo dell'hero.
Estetica "crypto/AI 2021": sfera neurale con anelli rotanti, glow ciano #00f2fe, glassmorphism uniforme — un repertorio ormai saturo che appiattisce Reflexora su centinaia di siti simili invece di distinguerla.
Mancanza di segnali di credibilità: niente metriche evidenziate, niente card dei paper, niente visual dei casi d'uso (Battery Reflex Module, crossbar), niente elementi che distinguano una research division da un generico landing.
La direzione consigliata è un "editorial deep-tech": ridurre il glow, innalzare la gerarchia tipografica, introdurre diagrammi tecnici nativi (non decorativi), numeri in grande scala, e un sistema di "evidence cards" per IP e pubblicazioni.

flowchart TB
  subgraph Sensor["Strato Sensoriale"]
    S[Event conditioning · ADC-light]
  end
  subgraph Reflex["Reflex Layer — azione locale vincolata"]
    R[Rule map · MCU/CPLD/FPGA/ASIC<br/>opzionale: crossbar spintronico]
  end
  subgraph Policy["Policy Layer — apprendimento, pianificazione"]
    P[Permessi · contesto · regole]
  end
  subgraph World["World Model — predizione / teacher"]
    W[Simulazione · ottimizzazione<br/>regole trasferite offline]
  end
  S -->|"evento urgente"| R
  R -->|"azione verificata<br/>+ event-action trace"| Actuator
  R -.->|"compact event report"| P
  P -.->|"aggiornamento regole"| R
  W -.->|"rule maps / thresholds"| R
  P --> W
  Actuator([Attuatore / potenza])
  classDef reflex fill:rgba(0,242,254,0.10),stroke:#00f2fe,color:#f8fafc;
  classDef policy fill:rgba(79,172,254,0.10),stroke:#4facfe,color:#f8fafc;
  classDef world fill:rgba(139,92,246,0.10),stroke:#8b5cf6,color:#f8fafc;
  class R reflex;
  class P policy;
  class W world;

  Il diagramma sopra rappresenta esattamente il tipo di visual nativo che oggi manca: dovrebbe sostituire o affiancare la sfera neurale nell'hero, perché comunica in 3 secondi ciò che la prosa attuale comunica in 3 paragrafi.
  1. Inquadramento di settore e benchmark
1.1 Il filone
REFLEXORA opera all'intersezione di quattro sottodomini: Physical AI / Embodied AI, neuromorphic & spintronic computing, edge AI safety-critical, e IP/patent platforms. Non è un prodotto SaaS né un venture puramente device: è un'architettura + portafoglio IP, con un percorso dichiarato verso spin-off indipendente. Questo posizionamento è raro e va difetto: i benchmark non vanno scelti fra le AI-tool directory, ma fra research lab, IP licensing e chip company neuromorfiche.

1.2 Benchmark selezionati
Sito
Filone
Cosa prendere
Cosa evitare
Cerebras (cerebras.ai)	Wafer-scale AI hardware	Hero basato su numeri enormi ("58× più grande, 15× più veloce"), customer logos, sezioni "advantage" a griglia	Estetica troppo "product-led", Reflexora non vende un chip
Rain AI (rain.ai)	Neuromorphic hardware	Minimalismo estremo: una headline, un CTA. Mostra che nel deep-tech la moderazione comunica autorevolezza	Troppo vuoto per un sito con 6 sezioni di contenuto
BrainChip / Akida (brainchip.com)	Neuromorphic edge AI, "Physical AI"	Mega-menu strutturato (Technology · Products · IP Cores · Research · Patents · White Papers), sezione "Use Cases" per modalità sensoriale, pagina Patents dedicata	Mega-menu pesante per un sito statico; prendere la struttura informativa, non la complessità di navigazione
Anthropic (anthropic.com)	AI research	Layout editorial, tipografia umanista ad alto contrasto, superfici chiare e thin dividers, ink "mai nero puro"	Tema chiaro — Reflexora resta su dark, ma può prendere la disciplina tipografica
IBM Research / Carbon	Design system enterprise	Token rigorosi, griglia, documentazione componenti	Eccesso di "enterprise formality"

1.3 Posizionamento consigliato
REFLEXORA dovrebbe porsi a metà strada fra Rain AI (autorevolezza minimal) e BrainChip (ricchezza informativa strutturata), con la disciplina tipografica di Anthropic. Il benchmark diretto per struttura è BrainChip (research + patents + use cases), il benchmark per tono visivo è una via di mezzo Rain AI / Anthropic.

2. Analisi dello stato attuale
2.1 Punti di forza (da preservare)
Design system a token già consolidato: --bg-dark, --accent-cyan, scala spaziatura 4/8px, radius, elevation, z-index.
Mobile-first dichiarato e implementato (@media (min-width: 48em) / 64em, tap target ≥44px, hamburger, niente overflow-x).
Tipografia fluida con clamp() già applicata a h1–h4 e body.
Accessibilità pianificata: prefers-reduced-motion, :focus-visible, skip-link, reveal-on-scroll con fallback no-JS.
Piano di self-hosting font per GDPR/performance su Aruba — corretto e necessario.
Contenuto denso e accurato: ogni pagina ha una tesi tecnica chiara.
2.2 Criticità (da risolvere)
#
Area
Problema
Impatto
C1	Hero	La "neural sphere" (anelli rotanti + core pulsante) è decoro generico che non comunica Reflex–Policy; occupa spazio prezioso senza informazione	Alto
C2	Architettura	Il concetto chiave (stratificazione Reflex/Policy/World Model) è solo testo; nessun diagramma nativo su nessuna pagina	Altissimo
C3	Palette	--accent-cyan: #00f2fe con --neon-glow diffuso produce un'estetica "crypto/glow" ormai datata e affaticante	Alto
C4	Gerarchia	Titoli, sotto-titoli e body hanno contrasto di peso insufficiente; tutto "galleggia" allo stesso livello	Medio-alto
C5	Credibilità	Portfolio IP (12+2+1) citato in una riga; nessuna card, nessun numero in grande, nessun link a paper	Alto
C6	Research page	Elenco testuale di "due Perspective papers" senza link, senza DOI, senza abstract	Alto
C7	Componenti	glass-card e app-card sono visivamente quasi identici (stesso surface-1, stesso hover translateY(-4px)); il catalogo componenti è nominalmente differenziato ma percepito come omogeneo	Medio
C8	Background	.bg-gradient-mesh con glow diffuso compete con il contenuto e satura il dark theme	Medio
C9	Footer	Ripetitivo su tutte le pagine, senza CTA differenziati né micro-navigazione	Basso-medio
C10	Identità	Nessun logo mark riconoscibile, nessun elemento visivo "firma" che distingua Reflexora	Medio

3. Raccomandazioni di intervento
3.1 Palette & contrasto
Diagnosi accessibilità (verifica WCAG AA):

--text-secondary: #94a3b8 su --bg-dark: #070a13 → rapporto ≈ 6,9:1 ✅ supera AA per testo normale (≥4,5:1). Il dubbio espresso in for_agents.md §5.1 è risolvibile in positivo.
--accent-cyan: #00f2fe su --bg-dark → ≈ 12,9:1 ✅ supera AA, ma su testo piccolo causa affaticamento per via dell'elevata luminanza; va riservato a accenti, icone e bordi, non a corpo testo.
Interventi consigliati:

Smutare il ciano. Sostituire --accent-cyan: #00f2fe con una variante meno saturata e leggermente più "tecnica", es. #22d3ee o #2dd4bf (teal). Mantiene riconoscibilità ma riduce il "glow crypto".
Aggiungere un accento neutro "ingegneristico" per superfici e diagrammi: un grigio-azzurro freddo #7dd3fc per linee tecniche e un #cbd5e1 per testo secondario su superfici card.
Introdurre una quarta funzionale per "World Model / IP": il --accent-purple attuale è fine, ma andrebbe usato consequenzialmente (sempre e solo per lo strato world model / brevetti) per creare un codice cromatico degli strati coerente col diagramma §0.
Ridurre --neon-glow da 0 0 20px rgba(0,242,254,0.5) a un valore ≤ 0 0 12px rgba(…,0.25) o riservarlo al solo stato :hover attivo.

:root {
  /* Palette ridefinita — editorial deep-tech */
  --accent-cyan:    #22d3ee;   /* meno saturato, più "strumento" */
  --accent-blue:    #60a5fa;
  --accent-purple:  #a78bfa;   /* world model / IP */
  --accent-teal:    #2dd4bf;   /* opzionale, strato reflex */
  --line-technical: #7dd3fc;   /* linee diagrammi, hairline attive */
  --neon-glow:      0 0 12px rgba(34, 211, 238, 0.22);
  --hairline:       rgba(255, 255, 255, 0.10);
  --hairline-strong:rgba(255, 255, 255, 0.16);
}
3.2 Tipografia
Outfit + Inter è una scelta solida e diffusa; per distinguere Reflexora nel settore serve un tocco editoriale:

Aggiungere un display serif o un grotesk più carattivale per l'h1 dell'hero. Opzioni: Söhne (a pagamento), General Sans, Space Grotesk (open, ben si sposa col monospazio tecnico). In alternativa, mantenere Outfit ma caricare il peso 900 per h1 e usarlo a dimensioni molto grandi con letter-spacing: -0.02em.
Elevare il contrasto di scala: l'attuale --fs-h1: clamp(2.75rem, 6vw, 5rem) è corretto ma l'h2 (clamp(1.9rem, 4vw, 2.75rem)) è troppo vicino. Ampliare il salto: h2 a clamp(1.6rem, 3vw, 2.25rem).
Outfit per heading, Inter per body, JetBrains Mono per etichette tecniche (già introdotto in --font-mono) — mantenerlo e estenderlo sistematicamente: usare il mono per eyebrow labels, metric labels, patent IDs, coordinate di strato. Questo crea un "look da datasheet" coerente con il contenuto ingegneristico.
Self-hosting (conferma §5.6): scaricare Outfit (400/700/900), Inter (300/400/600/800), JetBrains Mono (400/500) in woff2, @font-face con font-display: swap, rimuovere i <link> a Google Fonts — indispensabile per GDPR su hosting Aruba UE.
@font-face {
  font-family: 'Outfit';
  src: url('/fonts/Outfit-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
  font-style: normal;
}
3.3 Layout & composizione
Hero a due colonne su desktop (testo a sinistra, diagramma/architettura a destra), non centrato come ora. Il centramento attuale diluisce la gerarchia e spreca lo spazio accanto alla sfera.
Sostituire la neural sphere con il diagramma a strati (§0 mermaid). In produzione, realizzarlo in SVG inline + CSS (non canvas/WebGL) per accessibilità, prefers-reduced-motion e zero dipendenze. Gli strati si illuminano progressivamente allo scroll.
Sezione "metriche" subito dopo l'hero, stile Cerebras: grandi numeri con etichetta mono, es.:
12 depositi brevettuali IT · 2 EPO · 1 PCT
1–3 ordini di grandezza compressione comunicazione upstream
2 Perspective papers su Preprints.org
Container max 1200px confermato; aggiungere un layout a 12 colonne con gap per allineare diagrammi e testo.
Griglie minmax() come da §5.3 — estendere ovunque, in particolare la griglia applicazioni che oggi è 1fr → repeat(3,1fr) e su tablet intermedio rischia spaziature morte.
3.4 Componenti (catalogo)
Riordinare e differenziare visivamente le card, oggi troppo simili:

Classe
Uso
Trattamento proposto
glass-card	Feature concettuali (es. "Bounded authority")	Hairline --hairline, surface-1, hover translateY(-2px), linea accenso top 2px gradiente cyan→blue
app-card	Casi d'uso (robotica, battery, edge)	Bordo sinistro accent colorato per dominio, icona tecnica, mini-diagramma SVG
evidence-card (nuova)	Paper / brevetto	Stile "scheda bibliografica": ID mono, titolo, autori, stato (deposited/published), link DOI/PDF
metric-card (nuova)	Numeri hero/stat	Solo numero gigantesco + etichetta mono, niente bordo
layer-pill (nuova)	Etichette strato architettura	Pill mono con colore dello strato (cyan/blue/purple)

Principio: ogni tipo di contenuto ha una firma visiva dedicata; oggi tutto è surface-1 + translateY(-4px).

3.5 Motion & interattività
Ridurre parallax e glow animato costante; mantenere reveal-on-scroll (IntersectionObserver) ma con translateY(20px) più contenuto e durata 0.5s.
Diagramma architetturale animato: gli strati si "attivano" sequenzialmente allo scroll, e al passaggio del mouse su uno strato appare una tooltip mono con la sua responsabilità. Sotto prefers-reduced-motion, tutto statico.
Hover sui pulsanti: lo "shine sweep" attuale è un pattern anni 2010; sostituirlo con un semplice cambio di --grad-accent-hover + box-shadow più contenuto.
Micro-interazione sui link di navigazione: underline che si espande da sinistra (0→100%) invece del solo cambio colore.
3.6 Accessibilità (approfondimento)
Oltre a quanto già in for_agents.md §5.5:

Diagrammi SVG: fornire <title> e <desc> per ogni strato, role="img" e aria-labelledby. Lo strato attivo al focus deve essere navigabile da tastiera.
--accent-cyan su testo piccolo: anche se supera AA numericamente, per testo < 18px usare --text-primary o --accent-blue (più scuro) come da raccomandazione §3.1.
Skip link già presente — verificare che sia visibile al focus con contrasto sufficiente (attualmente presumibilmente nascosto).
Hamburger menu: assicurare che al toggle il focus si sposti nel menu e che Esc lo chiuda (pattern WAI-ARIA).
3.7 Content design & architettura dell'informazione
Research page: trasformare l'elenco testuale in griglia di evidence-card con link reali a Preprints.org (i paper esistono: 202606.0822, 202606.0573, Spatial AI Needs Reflex-Policy del 13 luglio 2026). Aggiungere abstract di 2 righe e badge di stato.
Architecture page: il contenuto testuale è ottimo — va visualizzato. Ogni bullet ("Event-to-action partitioning", "Bounded authority", "Measured closure"…) deve essere una mini-card con micro-diagramma SVG affianco, non solo testo.
Technology page: la distinzione convenzionale vs spintronico è cruciale — un diagramma comparativo a due colonne (MCU/CPLD/FPGA/ASIC ↔ MRAM/RRAM/FeFET/spintronic) con stato di maturazione sarebbe molto più efficace della lista attuale.
Applications page: ogni caso d'uso (Robotics, Automotive, Energy Harvesting, Battery Reflex Module, Sensing, Edge AI) merita un'icona tecnica SVG dedicata e, per il Battery Reflex Module, un diagramma di blocco del modulo (sense → rule → inject → verify).
Company page: aggiungere timeline della transizione (research division → funding → independent company) e un mini-team/investigator section, anche solo nominale, per dare volto umano all'IP.
Footer: differenziare per pagina (su Research → CTA "Read papers"; su Applications → CTA "Partner with us").

P1 — Quick win (alto impatto, basso sforzo, 1–3 giorni)
#
Azione
Sforzo
P1.1	Aggiungere sezione metriche (12/2/1, 1–3 ordini) sotto l'hero con metric-card	0,5 g
P1.2	Trasformare Research page in griglia evidence-card con link reali a Preprints.org	0,5 g
P1.3	Ridurre --neon-glow e smutare --accent-cyan → #22d3ee	0,25 g
P1.4	Sostituire "shine sweep" sui bottoni con hover più sobrio	0,25 g
P1.5	Estendere --font-mono a eyebrow/ID/label tecnici	0,5 g
P1.6	Self-hosting font (Outfit/Inter/JetBrains Mono) + rimozione Google Fonts	0,5 g

P2 — Strategico (alto impatto, medio sforzo, 1–2 settimane)
#
Azione
Sforzo
P2.1	Realizzare il diagramma architetturale SVG a strati per hero + Architecture page	3 g
P2.2	Hero a due colonne (testo + diagramma), abbandonare la neural sphere	1 g
P2.3	Micro-diagrammi SVG per ogni "distinctive feature" in Architecture	2 g
P2.4	Diagramma comparativo convenzionale vs spintronico in Technology	1,5 g
P2.5	Diagramma di blocco del Battery Reflex Module in Applications	1,5 g
P2.6	Differenziare glass-card / app-card / evidence-card / metric-card	1 g
P2.7	Icone SVG tecniche dedicate per i 6 casi d'uso	1,5 g

P3 — Rifinitura (medio impatto)
Timeline transizione aziendale in Company page
Footer differenziato per pagina
Hover underline animato in nav
Codice cromatico degli strati applicato coerentemente ovunque
Mega-struttura informativa in stile BrainChip (senza mega-menu pesante)
P4 — Rimandare
Logo mark custom completo (richiede branding dedicato)
Eventuale micro-animazione WebGL per il diagramma (l'SVG + CSS basta e avanza)
5. Snippet pronti all'uso
5.1 Token consolidati (estratto :root)
:root {
  /* Colori — editorial deep-tech */
  --bg-dark:        #070a13;
  --bg-darker:      #040609;
  --bg-card:        rgba(15, 23, 42, 0.6);
  --surface-1:      rgba(255, 255, 255, 0.025);
  --surface-2:      rgba(255, 255, 255, 0.045);

  --text-primary:   #f8fafc;
  --text-secondary: #94a3b8;          /* 6,9:1 su bg-dark ✅ AA */
  --ink:            #05141b;

  --accent-cyan:    #22d3ee;          /* strato Reflex */
  --accent-blue:    #60a5fa;          /* strato Policy */
  --accent-purple:  #a78bfa;          /* strato World Model / IP */
  --accent-teal:    #2dd4bf;
  --line-technical: #7dd3fc;

  --hairline:        rgba(255, 255, 255, 0.10);
  --hairline-strong: rgba(255, 255, 255, 0.16);

  --grad-accent:       linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
  --grad-accent-hover: linear-gradient(135deg, #67e8f9, #93c5fd);
  --neon-glow:         0 0 12px rgba(34, 211, 238, 0.22);
  --focus-ring:        0 0 0 3px rgba(34, 211, 238, 0.40);

  /* Tipografia */
  --font-heading: 'Outfit', system-ui, sans-serif;
  --font-body:    'Inter', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', ui-monospace, monospace;

  --fs-h1: clamp(2.75rem, 6vw, 5rem);
  --fs-h2: clamp(1.6rem, 3vw, 2.25rem);     /* salto maggiore da h1 */
  --fs-h3: clamp(1.15rem, 2.5vw, 1.5rem);
  --fs-body: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --fs-eyebrow: 0.78rem;

  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
}

5.2 evidence-card (paper / brevetto)

.evidence-card {
  background: var(--surface-1);
  border: 1px solid var(--hairline);
  border-left: 3px solid var(--accent-purple); /* codice IP */
  border-radius: var(--radius-sm);
  padding: var(--space-5);
  transition: transform 0.25s var(--ease-out), border-color 0.25s var(--ease-out);
}
.evidence-card:hover {
  transform: translateY(-2px);
  border-left-color: var(--accent-cyan);
}
.evidence-card .ev-id {
  font-family: var(--font-mono);
  font-size: var(--fs-eyebrow);
  color: var(--text-secondary);
  letter-spacing: 0.04em;
}
.evidence-card .ev-title {
  font-family: var(--font-heading);
  font-weight: 700;
  margin: var(--space-2) 0 var(--space-3);
}
.evidence-card .ev-status {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  color: var(--accent-teal);
}

5.3 metric-card
.metric-card { text-align: left; padding: var(--space-5) 0; }
.metric-card .m-value {
  font-family: var(--font-heading);
  font-weight: 900;
  font-size: clamp(2.5rem, 5vw, 3.75rem);
  line-height: 1;
  background: var(--grad-accent);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.metric-card .m-label {
  font-family: var(--font-mono);
  font-size: var(--fs-eyebrow);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-top: var(--space-2);
}
5.4 Strato architetturale SVG (schema base)
6. Note operative per il deploy su Aruba
Self-hosting font (§5.6 di for_agents.md) è non negoziabile su hosting UE: ogni <link> a fonts.googleapis.com trasferisce IP a Google ed è un tema GDPR. Le @font-face vanno in css/styles.css, i .woff2 in /fonts.
Nessuna risorsa esterna tracciante: niente Google Analytics senza cookie banner conforme, niente iframe. Per analytics, preferire Plausible self-hosted o equivalente UE-friendly.
Cache headers: configurare Cache-Control per /fonts e /css (long-lived, con hash nel filename al cambio).
Compressione Brotli/gzip lato Aruba per HTML/CSS/JS.
prefers-reduced-motion: verificare che sul hosting finale il JS di IntersectionObserver carichi correttamente e che il fallback no-JS mantenga i contenuti visibili (già gestito nel CSS attuale).
7. Riepilogo
La base tecnica del sito è sana: design system a token, mobile-first rigoroso, accessibilità pianificata, content denso e accurato. Il salto di qualità si gioca su tre mosse coordinate: (1) sostituire il decoro generico — neural sphere e glow diffuso — con visualizzazioni native del concetto Reflex–Policy (diagramma a strati, metric-card, evidence-card); (2) smutare la palette verso un "editorial deep-tech" meno saturo e più ingegneristico; (3) dare struttura visiva alla credibilità — paper, brevetti, numeri — oggi sepolti nel testo. I benchmark del settore (Cerebras per i numeri, BrainChip per la struttura research+patents, Rain AI/Anthropic per il tono minimale autorevole) confermano che la direzione è coerente con le aspettative del pubblico investitori/ricercatori.

Le azioni P1 (quick win, ~3 giorni complessivi) sono immediatamente implementabili senza riscrivere il design system e producono già un salto percepibile; le P2 (diagrammi e hero a due colonne) sono il vero investimento di immagine e andrebbero pianificate come secondo sprint prima del go-live su reflexora.ai.