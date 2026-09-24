<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-19 · 11:20 (CEST) · Claude Opus 4.8</div>

---

# Layer legale per reflexora.ai — versione "sfrondata" (derivata da ifevs.com)

Tre pagine autonome, bilingui IT/EN, da **importare nell'ambiente di reflexora.ai**:

- `privacy-policy.html`
- `cookie-policy.html`
- `note-legali.html`

Sono file **self-contained** (con un piccolo `<style>` neutro incorporato): si aprono così
come sono, ma sono pensati per essere integrati nel template di reflexora. Puoi rimuovere
il blocco `<style>` e incollare il contenuto `<main>` nelle tue pagine.

## Cosa è stato "sfrondato" rispetto a ifevs.com (§6 del brief)
- **Nessuna sezione YouTube / contenuti di terze parti** (reflexora non li ha).
- **Nessun trasferimento extra-UE**: dichiarato come punto di forza.
- **Nessun banner cookie**: il sito è previsto **cookieless**, quindi la Cookie Policy è
  breve e dichiara l'assenza di cookie di profilazione/terzi. **Non serve `main.js`.**
- **Riusato verbatim** da IFEVS: blocco identità societaria (art. 2250), diritti artt.
  15-22 + reclamo al Garante, struttura bilingue.
- Trattamenti dichiarati = **solo** contatto e-mail + log del server (hosting).

## Da personalizzare prima di pubblicare
1. **E-mail di contatto**: i file usano `info@ifevs.com`. Se reflexora ha un proprio
   indirizzo (es. `info@reflexora.ai`), sostituiscilo nei `mailto:` e nel testo.
2. **Plausible Analytics**: se/quando lo attivi (cookieless), **decommenta** il blocco
   `<!-- OPZIONALE ... -->` già pronto in `privacy-policy.html` (IT ed EN). Finché non è
   attivo, lascialo commentato (una policy deve descrivere solo trattamenti reali).
3. **Font self-hosted / animazioni senza CDN**: verifica che sia davvero così; se un font
   o un'animazione arriva da un CDN esterno, va dichiarato (contatto con terzo/eventuale
   trasferimento) e la parte "nessun trasferimento extra-UE" va rivista.

## ⚠️ Verifica a schermo obbligatoria (quando reflexora.ai è online)
Apri il sito finito e controlla in console:
- domini terzi contattati: `performance.getEntriesByType('resource').map(r=>new URL(r.name).host)`
- cookie di prima parte: `document.cookie`

Se risulta **cookieless e senza terzi** → questi file sono corretti e **non serve banner**.
Se compare un embed/analytics con cookie → allora, e solo allora, porta anche su reflexora
il **banner conforme** costruito per IFEVS (`js/main.js` + relativo CSS) e amplia la Cookie
Policy con la tabella dei cookie reali.

## Nota
Bozze non legali: come per IFEVS, è consigliata una revisione **legale/DPO** prima della
messa online, in particolare su basi giuridiche e tempi di conservazione.

---

<div align="center"><b>DOCUMENTO INTERNO IFEVS</b><br>Compilato il 2026-07-19 · 11:20 (CEST) · Claude Opus 4.8</div>
