# Architettura del Sito Reflexora.ai

Questo documento descrive l'architettura della landing page di Reflexora.ai. Il progetto è stato sviluppato come un sito statico, pensato per essere altamente performante, responsive e pronto per la pubblicazione su qualsiasi servizio di hosting (es. GitHub Pages, Vercel, Netlify o server tradizionale).

## Struttura delle Directory e dei File

La struttura del progetto è essenziale ma scalabile, basata su Vanilla HTML, CSS e JavaScript per garantire il massimo controllo e l'assenza di dipendenze esterne bloccanti.

```
REFLEXORA.AI/
│
├── index.html            # La pagina principale (landing page)
├── architettura_sito.md  # Questo documento
│
├── css/
│   └── styles.css        # Fogli di stile (Vanilla CSS, Dark Theme)
│
├── js/
│   └── main.js           # Logica di interattività e micro-animazioni
│
└── images/               # Cartella per gli asset visivi (immagini generate, loghi)
```

## Componenti Architetturali

### 1. Livello di Presentazione (HTML)
Il file `index.html` è suddiviso in sezioni semantiche:
- **Header/Navigazione:** Un menu fisso o "sticky" in alto per la navigazione rapida.
- **Hero Section:** La prima sezione visibile "above-the-fold", che cattura l'attenzione con il payoff principale ("Reflexora — Pioneering Reflexive Intelligence at the Edge").
- **About/Tech Section:** Spiegazione dell'architettura a due livelli (Reflex Layer e Policy Layer).
- **Applicazioni:** Una griglia o lista delle applicazioni target (Robotica, IoT, ecc.).
- **Footer:** Chiusura con call-to-action e contatti.

### 2. Livello di Stile (CSS)
Il file `css/styles.css` implementa:
- **Design System Premium:** Tema scuro con sfondi in tonalità `#0a0f1a` (blu molto scuro) e accenti neon ciano/blu elettrico per richiamare i concetti di AI, edge computing e reti neurali.
- **Micro-animazioni e Hover:** Transizioni fluide sugli elementi interattivi, fade-in allo scroll.
- **Responsive Design:** Utilizzo di Flexbox e CSS Grid per adattare perfettamente i contenuti su desktop, tablet e mobile.
- **Performance:** Nessun framework CSS pesante (niente Bootstrap o Tailwind importati se non strettamente necessari); tutto è scritto custom per caricamenti istantanei.

### 3. Livello di Interattività (JavaScript)
Il file `js/main.js` è utilizzato per migliorare l'esperienza utente (UX):
- **Scroll Reveal:** Utilizzo della `IntersectionObserver` API per animare gli elementi (es. fade in verso l'alto) man mano che diventano visibili durante lo scorrimento della pagina.
- **Dinamismo Background:** Animazioni dinamiche per lo sfondo "hero" nel caso di sfondi generati o creati via codice.

## Note per il Deployment
Poiché il sito è interamente statico:
- Non richiede alcun database o runtime lato server (es. Node.js, PHP).
- Può essere ospitato su un qualsiasi bucket S3 o servizi CDN gratuiti.
- Le immagini/video (quando aggiunti alla cartella `images/`) devono utilizzare percorsi relativi per mantenere la compatibilità in caso di test offline (es. `src="images/hero.webp"`).
