<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-19 · 10:33 (CEST) · Claude Fable 5</div>

---

# Rimessa a norma del layer legale/GDPR di **ifevs.com** — guida esecutiva per l'agente (Opus 4.8)

> **Come usare questo file.** È un **brief autosufficiente**: portalo nella root del sito
> **ifevs.com** (ambiente/checkout dei file statici del sito) e fallo eseguire da Opus 4.8.
> Puoi rinominarlo (es. `ISTRUZIONI_legale.md`) quando lo sposti. L'agente che lo esegue **non
> ha il contesto di questa conversazione**: qui dentro c'è tutto ciò che gli serve.
>
> **Obiettivo doppio.** (1) Rimettere a norma la parte legale di **ifevs.com**. (2) Produrla in
> modo che diventi il **master riusabile** per il sito della divisione di ricerca **REFLEXORA**
> (`reflexora.ai`), che è **lo stesso soggetto giuridico IFEVS** ma un sito tecnicamente diverso
> (v. §6: NON si copia pari-pari, si *sfronda*).

---

## 0. ISTRUZIONI PER L'AGENTE — leggere prima di toccare qualsiasi file

1. **NON sei un legale.** Tutti i testi che produci sono **BOZZE**. Non pubblicare/mettere online
   privacy, cookie policy o note legali senza **validazione di un professionista legale/DPO**.
   Marca in testa a ogni documento generato: `⚠️ BOZZA — richiede validazione legale prima della pubblicazione`.
2. **NON inventare dati societari.** Numeri di Registro Imprese, capitale sociale, PEC, sede
   legale esatta: usa **solo** ciò che è in §2 come confermato; tutto ciò che è marcato
   **⚠️ DA VERIFICARE** resta un **placeholder** (`⟦DA CONFERMARE IFEVS: …⟧`) finché IFEVS non
   fornisce il dato da visura camerale. Un documento legale con dati inventati è peggio che assente.
3. **Non rompere il sito.** Lavora su **copia/branch**; ogni modifica deve lasciare il sito che
   carica e naviga. Sito statico (HTML/CSS/JS): niente framework, niente dipendenze nuove.
4. **Verifica SEMPRE a schermo** ciò che affermi sul comportamento del sito (cookie realmente
   impostati, richieste a domini terzi, banner): la fonte di verità è il **sito reale corrente**,
   non questo documento (che è uno snapshot del 2026-07-19; il sito potrebbe essere cambiato).
   Come farlo: apri le pagine in un browser, e in console
   `performance.getEntriesByType('resource').map(r=>new URL(r.name).host)` per i domini terzi,
   `document.cookie` per i cookie di prima parte, e ispeziona gli `<iframe>`/`<script>` esterni.
5. **Bilingue IT/EN**: i documenti legali del sito sono già IT/EN — mantieni entrambe le lingue.
6. **Un intervento per volta, commit separati**, messaggio chiaro. Aggiorna una nota di changelog
   se il repo la prevede.

---

## 1. Contesto strategico (perché lo stiamo facendo)

REFLEXORA **non** è una società: è il nome della **divisione di ricerca di IFEVS**. Il sito
`reflexora.ai` è un sito **di IFEVS** → titolare del trattamento, P.IVA, sede e dati societari
esposti sono quelli di **Interactive Fully Electrical VehicleS S.r.l.**

La parte legale di ifevs.com oggi è carente (dettaglio in §3). La strategia:
**(a)** rimettere a norma ifevs.com; **(b)** consolidare un **blocco identità societaria** e un
**telaio privacy/cookie** puliti; **(c)** riusarli per reflexora.ai **sfrondati** dei trattamenti
che quel sito non ha (v. §6). L'errore da NON ripetere: descrivere trattamenti inesistenti
(oggi la privacy IFEVS descrive "form di contatto" che sul sito non ci sono).

---

## 2. Dati societari IFEVS — verificati e da verificare

Rilevati il 2026-07-19 da `ifevs.com` (footer + Privacy Policy). **Ricontrolla sul sito corrente**
prima di usarli.

| Campo | Valore | Stato |
|---|---|---|
| Denominazione | **Interactive Fully Electrical VehicleS S.r.l.** (I-FEVS S.r.l.) | ✅ confermato (footer) |
| P.IVA / Codice Fiscale | **03395740040** | ✅ (footer + privacy coincidono) |
| REA | **CN-287520** (Cuneo) | ✅ (footer) |
| Legale rappresentante | Dott. **Pietro Perlo** | ✅ (privacy) |
| E-mail contatto | **info@ifevs.com** | ✅ |
| Sede **legale** | footer: *Strada Carignano 50/1, La Loggia (TO) 10040* · privacy: *Via Carle 23, 12048 Sommariva Bosco (CN)* | ⚠️ **CONTRADDITTORIA** (v. §3.1) |
| Sede **operativa** | Via/Strada Carignano 50/1, 10040 La Loggia (TO) | ✅ |
| Registro Imprese (n.) | — | ⚠️ **DA VERIFICARE** (spesso = C.F.) |
| Capitale sociale | — | ⚠️ **DA VERIFICARE** (versato/deliberato) |
| PEC | — | ⚠️ **DA VERIFICARE** (obbligatoria per S.r.l.) |
| Socio unico (sì/no) | — | ⚠️ **DA VERIFICARE** (se unipersonale va dichiarato) |

**Bloccante prima della pubblicazione:** IFEVS deve confermare da **visura camerale** la sede
legale reale (e coerenza col REA), n. Registro Imprese, capitale sociale, PEC, socio unico.

---

## 3. Diagnosi del sito ifevs.com — cosa NON va (e cosa già va bene)

### ✅ Da conservare come base
Privacy bilingue IT/EN che cita GDPR artt. 13-14, **elenca i diritti** (artt. 15-22) e il
**reclamo al Garante** (indirizzo + garanteprivacy.it); **titolare identificato**; footer con
identificazione societaria; **contatto senza form** (solo `info@ifevs.com`). Riusa questa
impostazione, ripulita.

### ❌ Difetti da correggere (per gravità)

**3.1 — Sede legale contraddittoria [GRAVE].** Footer dice sede legale a *La Loggia (TO)*; la
privacy dice *Sommariva Bosco (CN)*. Il **REA CN** (Cuneo) è coerente con **Sommariva Bosco (CN)**,
non con La Loggia (TO). Probabile causa: il footer etichetta come "sede legale" quella
**operativa**. → Riconcilia su visura: distingui **sede legale** (iscritta al Registro Imprese)
da **sede operativa**; se la società ha davvero spostato la sede legale a La Loggia, il REA
dovrebbe risultare TO-… e va aggiornato. **Non pubblicare finché non è chiaro.**

**3.2 — Toponimo incoerente.** "**Strada** Carignano" (footer) vs "**Via** Carignano" (privacy):
stesso luogo, dicitura diversa. Uniforma a quella catastale corretta.

**3.3 — Privacy Policy non aderente alla realtà.**
- Descrive **"form di contatto" che raccolgono nome/e-mail**, ma il sito **non ha form** (la
  pagina contatti espone solo `info@ifevs.com`). → Riscrivi il trattamento su ciò che accade
  davvero (contatto via e-mail + log server + eventuale embed, v. 3.5).
- Dichiara di trattare **"dati sensibili"** (categorie particolari, art. 9). → **RIMUOVI**:
  falso e pericoloso per un contatto e-mail.
- **"Conferimento obbligatorio … pena l'accesso al servizio"**. → Falso per un contatto
  volontario: **facoltativo**.
- **Manca la base giuridica per finalità** (art. 13(1)(c)) e un **periodo di conservazione
  determinato** (art. 13(2)(a)).
- **Nessuna informativa sui trasferimenti extra-UE** (art. 13(1)(f)) benché ci sia YouTube (3.5).
- Impostazione datata (apre col **D.lgs 196/2003**).

**3.4 — Cookie Policy boilerplate [non conforme Garante 2021].**
- Nessuna **tabella dei cookie realmente usati** (nome, provider, finalità, durata).
- Afferma che **"gli analytics non richiedono consenso"** → falso in generale (GA non è esente;
  nel 2022 ritenuto illecito dal Garante per i trasferimenti USA).
- Rimanda il consenso alle **"impostazioni del browser"** → approccio **superato**: il consenso
  va raccolto **nel sito**.
- Non nomina i terzi né linka le loro privacy.

**3.5 — Banner cookie non conforme + YouTube pre-consenso [GRAVE].**
- Banner con **solo "Accept"**: mancano **"Rifiuta"** ugualmente semplice e **"Personalizza"**.
- La home **incorpora `www.youtube.com`** (iframe) → cookie di terze parti Google + **trasferimento
  USA**, con ogni probabilità **prima del consenso**. Nessuna revoca possibile.

**3.6 — Identificazione societaria incompleta (art. 2250 c.c.).** Il footer ha REA ma **non**
il n. **Registro Imprese**, **capitale sociale**, **PEC**, eventuale **socio unico**.

---

## 4. Interventi da eseguire su ifevs.com (per file)

> Prima: **mappa i file**. Da ispezione 2026-07-19 il sito è statico e include (nomi con spazi!):
> `index.html`, `privacy policy.html`, `cookies policy.html`, `contacts.html`, più
> `road_vehicles.html`, `air_mobility.html`, `i-bikes.html`, `events.html`, `microfactories.html`,
> `photovoltaics.html`, `technologies.html`, `demonstrators.html`,
> `recent-invited-presentations.html`, `acknowledgments.html`. Footer e banner appaiono
> **site-wide**. **Verifica se footer/banner sono un include condiviso o duplicati in ogni
> pagina**: se duplicati, correggili ovunque (meglio: centralizzali per evitare futuri disallineamenti).

### 4.1 Footer + identificazione societaria (art. 2250 c.c.) — su TUTTE le pagine
Footer unico con:
```
Interactive Fully Electrical VehicleS S.r.l.
Sede legale: ⟦DA CONFERMARE⟧  ·  Sede operativa: Via Carignano 50/1, 10040 La Loggia (TO)
P.IVA / C.F. 03395740040  ·  REA ⟦prov⟧-287520  ·  Registro Imprese ⟦n.⟧  ·  Cap. soc. ⟦€… i.v.⟧
PEC ⟦…⟧  ·  info@ifevs.com   —   © <anno> I-FEVS. All rights reserved.
[Privacy Policy] · [Cookie Policy] · [Note legali]
```
- Uniforma i dati **identici** in footer, privacy e note legali (l'errore 3.1 nasce da versioni
  divergenti). Aggiorna © all'anno corrente.

### 4.2 Privacy Policy (`privacy policy.html`) — riscrivi il corpo
Mantieni l'ossatura buona (titolare, diritti artt. 15-22, reclamo al Garante) e **correggi**:
- **Titolare**: dati completi §2, rappr. Perlo, e-mail per esercizio diritti. DPO: indicare se
  nominato (⚠️ verificare; per una PMI può non essere obbligatorio).
- **Trattamenti reali** (elenca solo questi):
  1. **Contatto e-mail**: dati che l'utente include scrivendo a `info@ifevs.com`, **al solo fine
     di rispondere**. Base giuridica: art. 6(1)(b)/f (⟦da confermare col legale⟧). **Conferimento
     facoltativo.** Conservazione: periodo determinato (es. 24 mesi) ⟦da definire⟧.
  2. **Log del server (hosting)**: IP/dati tecnici per sicurezza/funzionamento; base giuridica
     legittimo interesse; conservazione secondo policy hosting ⟦verificare⟧.
  3. **YouTube** (se l'embed resta, v. 4.5): trattamento e **trasferimento USA** da parte di
     Google; base giuridica **consenso**; rimando alla privacy di Google. *(Se si adotta il
     click-to-load, dirlo.)*
- **RIMUOVI** "dati sensibili", "form", "conferimento obbligatorio", cornice D.lgs 196/2003 come
  principale.
- **Aggiungi**: base giuridica per finalità, retention determinata, **trasferimenti extra-UE**
  (presenti finché c'è YouTube), destinatari/responsabili (**hosting** ex art. 28 → serve **DPA**),
  data e versione.

### 4.3 Cookie Policy (`cookies policy.html`) — sostituisci il boilerplate
- **Tabella dei cookie realmente presenti** (ricavata dalla verifica 4.6): per ciascuno →
  nome, tipo (tecnico/analitico/terze parti), finalità, provider, durata.
- **Rimuovi** l'affermazione "analytics sempre esenti" e il rimando alle "impostazioni del
  browser" come modalità di consenso.
- Se restano cookie non tecnici/terzi (YouTube): descrivili, linka le privacy dei provider,
  e collega il tutto al banner (4.4).

### 4.4 Banner cookie — rendilo conforme (Garante 2021)
- **"Accetta" e "Rifiuta" ugualmente evidenti** + **"Personalizza"** (scelta granulare per
  categoria). La chiusura (X) = rifiuto.
- **Nessun cookie non necessario / nessun embed terzo prima del consenso.**
- **Revoca** sempre possibile (link "Preferenze cookie" nel footer).
- Preferisci una soluzione **self-hosted/leggera** (vanilla) per non introdurre a sua volta terzi.
- Persistenza della scelta e ri-proposta secondo linee guida (durata ragionevole).

### 4.5 Embed YouTube — elimina il pre-consenso
- Sostituisci l'iframe `youtube.com` con **`youtube-nocookie.com`** **e** **click-to-load**:
  mostra una preview statica (thumbnail) e carica l'iframe **solo dopo** che l'utente clicca
  (= consenso esplicito a quel contenuto). Così nessun cookie/trasferimento prima del consenso.
- In alternativa, gate l'iframe dietro il consenso "contenuti di terze parti" del banner.

### 4.6 Verifica tecnica a schermo (prima di scrivere la cookie policy)
Apri il sito **corrente** e rileva i **cookie realmente impostati** e i **domini terzi** contattati
(vedi §0.4). La cookie policy e il banner devono riflettere **questo**, non le categorie astratte.

### 4.7 (Consigliato) Pagina "Note legali / Legal notice"
Una pagina che raccolga in un punto: identificazione societaria completa (art. 2250), titolare,
contatti, © e disclaimer. Non è obbligo formale ma dà ordine e un'ancora unica.

---

## 5. Checklist esecuzione ifevs.com

**Dati (bloccante — da IFEVS):**
- [ ] Sede legale reale + coerenza REA · [ ] Registro Imprese · [ ] Capitale sociale · [ ] PEC · [ ] socio unico · [ ] DPO sì/no · [ ] DPA hosting

**Da fare (agente, poi validazione legale):**
- [ ] Footer/identificazione societaria completi e **identici** su tutte le pagine
- [ ] Privacy riscritta e aderente (no "sensibili"/no "form"/no "obbligatorio"; base giuridica + retention + trasferimenti + destinatari/DPA)
- [ ] Verifica cookie/terzi a schermo → Cookie Policy con **tabella reale**
- [ ] Banner con **Rifiuta + Personalizza**, nessun cookie/embed prima del consenso, revoca
- [ ] YouTube in **nocookie + click-to-load**
- [ ] HTTPS forzato · [ ] data/versione sui documenti · [ ] © aggiornato

**Gate finale:** revisione **legale/DPO** prima di pubblicare. Nessuna bozza AI va online as-is.

---

## 6. Derivazione per reflexora.ai — **sfrondare, non copiare**

Una volta pulito ifevs.com, per `reflexora.ai` (stesso titolare IFEVS, sito **diverso e più
snello**) riusa il **telaio** ma adatta i contenuti alla sua **realtà tecnica**:

- **Riusa VERBATIM:** blocco identità societaria (footer/note legali), sezione diritti
  dell'interessato + reclamo al Garante, struttura bilingue, stile.
- **SFRONDA nella privacy:** reflexora.ai è **form-free** (solo `mailto`), **font self-hosted**,
  **animazione senza cookie/CDN**, analytics previsto **Plausible cookieless**, **nessun embed
  YouTube/terzi**. Quindi: **niente sezione YouTube**, **niente trasferimenti extra-UE**
  (dichiara l'assenza come punto di forza), trattamenti = solo *contatto e-mail* + *log server*
  (+ *Plausible* se attivato, senza cookie).
- **Cookie:** verifica a schermo il sito reflexora finito; se risulta **cookieless** (obiettivo)
  → **NIENTE banner**, basta una **breve Cookie Policy** che dichiara assenza di cookie di
  profilazione/terzi. Se in futuro si introduce un embed/analytics con cookie → allora, e solo
  allora, si porta anche su reflexora il banner conforme costruito per IFEVS (4.4).
- **Regola d'oro:** ogni documento descrive **solo i trattamenti del proprio sito**. Non
  trascinare su reflexora ciò che vale solo per ifevs (YouTube, banner) e viceversa.

Risultato atteso: reflexora.ai **più conforme del sito madre** — privacy breve e veritiera,
footer legale completo, potenzialmente **senza banner**.

---

*Consulenza — Fable 5, 2026-07-19. Non costituisce parere legale.*

<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-19 · 10:33 (CEST) · Claude Fable 5</div>
