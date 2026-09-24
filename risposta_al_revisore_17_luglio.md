# Risposta alla revisione del prototipo Reflex-Policy — esito degli interventi

Grazie: la revisione è stata utile e in buona parte l'abbiamo recepita. Il punto centrale — **manca
il ciclo completo Reflex-Policy** — era corretto e l'abbiamo trattato come priorità assoluta. Di
seguito, in modo trasparente, cosa abbiamo applicato, cosa no e perché, e due punti su cui la
revisione va corretta.

Sono state prodotte due versioni: **V4** (nello slot hero) e **V5** (fascia full-width, che è la
direzione scelta — vedi in fondo).

---

## 1. Il suo punto #1 è ancora più forte di come è stato argomentato

Lei lo inquadra come un problema di **UX narrativa**. In realtà è **strategico**.

REFLEXORA dispone di un'analisi di prior-art che conclude che la separazione reflex/policy, come
idea generale, **non è originale** (è prior art consolidata nella robotica). I differenziatori
difendibili sono esattamente: *confidence separata da authority, bounded first action, **measured
response**, **compact event-action traces**, **structured observability**, energy proportionality,
cyber-physical containment*.

Il prototipo mostrava sensing → decisione → comando → energia: cioè **precisamente la parte non
differenziante**, omettendo tutti i differenziatori. Come Hero, comunicava ciò che REFLEXORA ha in
comune con la letteratura, nascondendo ciò che la rende distintiva. La sua osservazione ha quindi
un impatto ben oltre la UX.

---

## 2. Applicato

| # | Suggerimento | Come è stato implementato |
|---|---|---|
| 1 | Ritorno Reflex → Policy | Canale dedicato con chip **`EVENT · ACTION · RESPONSE`**. I due rami **convergono** nella Policy: comunica "le tracce risalgono", non "la Policy comanda" |
| 2 | Measured response + observability | Fase dedicata nella sequenza (vedi §3: risolto senza aggiungere geometria) |
| 3 | Chiarire che è un esempio | Banner `EXAMPLE APPLICATION · PV-TO-BATTERY LOCAL ENERGY CONTROL` |
| 4 | Layout mobile dedicato | Layout verticale **reale** (non ridimensionamento). Titoli **13,4px vs 6,4px**: +109% |
| 5 | Sequenza causale | Le sue 7 fasi, ~1,2s ciascuna + pausa. Driver JS, `data-phase`, didascalia e step-tracker |
| 6 | Fix `IntersectionObserver` | Corretto in `intersectionRatio < 0.15`. Aggiunto anche `visibilitychange` |
| 7 | Policy Layer ≠ Main BMS | `POLICY / SUPERVISORY LAYER` + `BMS · EMS · AI · World Model` |
| 8 | Rinominare il bus | → **`SHARED ENERGY FEED`**. Conferma dalla nostra fonte R7, che dice esplicitamente che il modulo *"does not require a second pack-wide harness carrying balancing current"* e parla di *"shared auxiliary energy feed"*: l'etichetta precedente **contraddiceva** la fonte |
| 9 | Isolated injection | `CURRENT-LIMITED ISOLATED INJECTION` + `Floating Output + One-Hot Selector` |
| 10 | Marker colorati | Marker separati per policy/reflex/sense/power/feed |
| 11 | Pause/Play | Aggiunto — con una precisazione: **non è Priorità 2, è WCAG 2.2.2 (Livello A)**, obbligatorio per contenuto in movimento automatico in loop >5s |
| 12 | `lang` vs descrizione IT, versione V2/V3 | Corretti |
| 13 | Ridurre il carico dei filtri | `drop-shadow` ora **solo sulla fase attiva** |
| 14 | Harvested/Conditioned Energy | → `PV energy output` / `Bounded injection` |
| 15 | Battery Clusters | → `BATTERY ZONE · Cells · Groups · Bricks` (la sua alternativa "commerciale") |

---

## 3. Non applicato — e perché

**Blocco one-hot separato** e **quarta linea per il measured response.** Entrambi peggioravano la
**densità**, che è il problema numero uno (misurato: vedi §4). Abbiamo risolto diversamente: il
measured response usa **lo stesso canale di sensing in un momento diverso** (fase 6). È anche più
onesto sul piano fisico — è realmente lo stesso canale AFE/comparatori che riporta lo stato dopo
l'azione, come descrive il nostro report R7. **La sequenza fa il lavoro che altrimenti avrebbe
richiesto più geometria.**

**Sezione "UX della Hero".** Qui la revisione è a vuoto, per mancanza di contesto: il diagramma non
*è* la Hero, va **accanto** a una Hero che ha già headline, subheadline e due CTA. Inoltre i testi
del sito sono congelati e validati dalla direzione e da revisori umani: il copy proposto non è
adottabile.

**Selettore Battery / PV / Robotics / Spatial AI.** Ottima idea, ma è una feature, non un fix.
Rinviata, non scartata.

**`Battery Clusters` → `Addressable Series Elements`.** Più preciso ma più gergale: peggiora la
leggibilità per investitori e partner.

---

## 4. Due correzioni alla revisione

**a) Contraddizione interna su `<symbol>` + `<use>`.** Lei elogia l'architettura SVG basata su
`<symbol>` + `<use>` come robusta. Ma è **proprio quella scelta a rendere impossibile la sua
Priorità-1 #4** (layout mobile dedicato): `<use>` clona la *stessa geometria*, quindi desktop e
mobile non possono avere layout diversi. Le due raccomandazioni sono incompatibili. Per implementare
il layout mobile abbiamo dovuto abbandonare `<use>` in favore di due layout reali selezionati via
media query.

*(Nota di metodo: sospettavamo anche che `<use>` impedisse al CSS a classi di applicarsi allo shadow
tree. Abbiamo verificato: **è falso**, gli stili si applicano. Il problema è solo la geometria
condivisa.)*

**b) Il problema non è solo il mobile: anche il desktop non regge.** Lei considera accettabile il
desktop e critica solo il mobile. Le misure dicono altro. Nello slot hero a 568×500:

| Elemento | px effettivi |
|---|---|
| Titoli nodi | **10,8** |
| Sottotitoli | **7,6** |
| Etichette | **7,9** |
| Zone label | **6,9** |

Solo i titoli erano al limite del leggibile; **tutto il resto era sotto soglia già su desktop**.

---

## 5. Conseguenza: il diagramma esce dalla Hero

Questa misura ha portato alla decisione più importante, che converge con la sua "soluzione
raccomandata" per altra via: **il diagramma non può stare nello slot hero**. È troppo denso, punto.

Nella versione **V5** diventa una **fascia full-width** (~1136px). Risultato misurato:

| Elemento | Slot hero | Fascia V5 |
|---|---|---|
| Titoli nodi | 10,8px | **15px** |
| Etichette | 7,9px | **11,2px** |
| Titoli mobile | 6,4px | **13,4px** |

Nella Hero resterà un elemento più semplice ed evocativo.

---

## 6. Resta aperto

I rename terminologici (`SHARED ENERGY FEED`, `CURRENT-LIMITED ISOLATED INJECTION`,
`POLICY / SUPERVISORY LAYER`) toccano semantica di dominio: sono in validazione presso il
responsabile tecnico. Se dovessero cambiare, la struttura del diagramma non ne risente.

Grazie ancora: la revisione ha migliorato il prototipo in modo sostanziale, e soprattutto ha
corretto un errore di posizionamento che avremmo portato online.


---

*Redatto da Claude Code (Opus 4.8) per REFLEXORA / IFEVS — 2026-07-17. Riferito alla versione V5 del prototipo; V6/V7/V8 hanno poi recepito ulteriori osservazioni tecniche di P. Perlo.*
