<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-17 · 11:49 (CEST) · Claude Opus 4.8</div>

---

# Appunto per Pietro Perlo — richiesta di conferma terminologica

**Oggetto:** diagramma animato Reflex-Policy (esempio PV↔batteria) destinato al sito reflexora.ai.
**Cosa serve:** una conferma su **6 etichette**. Sono decisioni di dominio, non di grafica: non le
prendiamo senza il tuo avallo.
**Tempo richiesto:** ~5 minuti. Basta un OK / NO / alternativa per ciascuna riga.

**Contesto.** Una revisione tecnica indipendente ha segnalato che alcune diciture del diagramma
sono ambigue o fuorvianti. Verificandole contro il report **R7 — Battery Reflex Module**, in due
casi il revisore ha ragione e **l'etichetta attuale contraddice la nostra stessa fonte**. Le
modifiche sono già implementate nel prototipo ma **sono reversibili**: se una non ti convince, si
torna indietro senza impatti sulla struttura.

---

## Le 6 voci

### 1. Supervisore — ⚠️ potenziale errore tecnico
| | |
|---|---|
| **Attuale** | `POLICY LAYER / MAIN BMS` — *Supervision, Learning & Safety* |
| **Proposto** | `POLICY / SUPERVISORY LAYER` — *BMS · EMS · AI · World Model* |
| **Perché** | Il diagramma copre **PV e batteria**. Un *Main BMS* non supervisiona il lato PV: lì il supervisore è un EMS, un inverter controller o un plant controller. L'etichetta attuale fonde il livello architetturale generale con un componente specifico della batteria. |
| **Fondamento** | R7 parla di *"BMS authority"* solo in ambito batteria. |

### 2. Bus energetico — ⚠️ contraddice R7
| | |
|---|---|
| **Attuale** | `DC BALANCING BUS` |
| **Proposto** | `SHARED ENERGY FEED` |
| **Perché** | "Balancing bus" suggerisce un bus di *active balancing* convenzionale, cioè esattamente ciò che R7 dice di **non** essere. |
| **Fondamento (R7, testuale)** | *"It does not require a second pack-wide harness carrying balancing current from a central box to every cell"* · *"A shared auxiliary energy feed is brought to each local module"* |
| **Alternative** | `AUTHORIZED ENERGY FEED` · `SHARED ZONE ENERGY FEED` · `CONDITIONED DC ENERGY FEED` |

### 3. Stadio di iniezione — ⚠️ **qui serve davvero la tua decisione**
| | |
|---|---|
| **Attuale** | `ISOLATED INJECTION` — *Multi-Output Power Stage* |
| **Proposto** | `CURRENT-LIMITED ISOLATED INJECTION` — *Floating Output + One-Hot Selector* |
| **Perché** | Il revisore osserva che *"Multi-Output"* può far intendere **più uscite attive contemporaneamente**, mentre il concetto è la **one-hot selection**. |
| **Nota importante** | **R7 usa entrambi i termini**: elenca *"a transformer-isolated multi-output stage"* fra le topologie pratiche, e parla di *"current-limited isolated or floating converter"* e di *"one-hot interlocks"*. Quindi non è un errore: è una **scelta di cosa comunicare**. Tecnicamente il multi-output descrive la *topologia*; il one-hot descrive la *regola di selezione*. |
| **Domanda** | Preferisci enfatizzare la topologia (multi-output) o il vincolo di sicurezza (one-hot)? |

### 4. Elemento fisico di storage — solo stile
| | |
|---|---|
| **Attuale** | `BATTERY CLUSTERS` — *Physical Energy Storage* |
| **Proposto** | `BATTERY ZONE` — *Cells · Groups · Bricks* |
| **Perché** | Comunica l'elemento **localmente indirizzabile**, che "clusters" non trasmette. |
| **Alternativa del revisore** | `ADDRESSABLE SERIES ELEMENTS` — più preciso ma più gergale: l'abbiamo scartata pensando al pubblico investitori/partner. Se la preferisci tecnicamente, si cambia. |

### 5. Etichette di energia — solo chiarezza
| | |
|---|---|
| **Attuale** | `Harvested Energy` · `Conditioned Energy` |
| **Proposto** | `PV energy output` · `Bounded injection` |
| **Perché** | La direzione del flusso non era immediata. *"Bounded injection"* è coerente con il linguaggio Battery Reflex-Balance. |
| **Fondamento (R7)** | *"injects a bounded current into that cell"* |

### 6. Sensing — cambio sottile ma con un motivo preciso
| | |
|---|---|
| **Attuale** | `Local Flags (V, T, Shade)` · `Local Flags (V, T, Fault)` |
| **Proposto** | `Local evidence (V, T, Shade)` · `Local evidence (V, T, Fault)` |
| **Perché** | Lo **stesso canale** ora trasporta due cose in momenti diversi: l'**evidenza iniziale** e la **measured response** dopo l'azione. "Flags" copre bene la prima, non la seconda. "Evidence" copre entrambe ed è il termine usato nell'analisi di prior-art (*"low-bit physical evidence"*). |
| **Se preferisci** | Si può tornare a "Local Flags" e usare "Measured response" solo nella didascalia della fase 6. |

---

## Riepilogo per la risposta

| # | Da | A | Natura |
|---|---|---|---|
| 1 | POLICY LAYER / MAIN BMS | POLICY / SUPERVISORY LAYER | correzione tecnica |
| 2 | DC BALANCING BUS | SHARED ENERGY FEED | **contraddice R7** |
| 3 | Multi-Output Power Stage | Floating Output + One-Hot Selector | **scelta comunicativa — decidi tu** |
| 4 | BATTERY CLUSTERS | BATTERY ZONE | stile |
| 5 | Harvested / Conditioned Energy | PV energy output / Bounded injection | chiarezza |
| 6 | Local Flags | Local evidence | coerenza con il closed loop |

**Le più urgenti sono la 2 e la 3.** La 2 perché l'etichetta attuale dice il contrario di R7 e
finirebbe online. La 3 perché è l'unica dove R7 supporta entrambe le opzioni e serve una scelta.

---

<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-17 · 11:49 (CEST) · Claude Opus 4.8</div>
