# Rejsedagbog — sådan virker det

En simpel statisk hjemmeside. Ingen build-trin, ingen server — du kan bare åbne
`index.html` i browseren, eller uploade hele mappen til fx GitHub Pages,
Netlify eller Vercel (træk-og-slip virker på begge de sidste to).

## Mappestruktur

```
rejseside/
  index.html          ← forside med alle lande
  styles.css           ← alt design, delt af alle sider
  script.js            ← sprogtoggle
  thailand/
    index.html          ← Thailand-oversigt (byer, tips, mad)
    bangkok.html         ← fuldt udfyldt eksempel
    koh-samui.html        ← tom skabelon, klar til indhold
    koh-phangan.html
    koh-tao.html
    krabi.html
    railay.html
    phi-phi.html
    pai.html
    chiang-mai.html
  images/               ← læg dine billeder her, når du har dem
```

## Sådan tilføjer du indhold til en by-side (fx Koh Samui)

Åbn `thailand/koh-samui.html` og brug `thailand/bangkok.html` som skabelon —
kopiér de sektioner du har brug for (Tips, Aktiviteter, Byen, Spisesteder,
Hvor vi boede) og erstat teksten. Fjern `<div class="coming-soon-box">...`
boksen, når siden er udfyldt.

## Sådan tilføjer du et helt nyt land (fx Vietnam)

1. Opret en ny mappe: `vietnam/`
2. Kopiér `thailand/index.html` ind i den, og omdøb til `index.html`
3. Ret alle referencer til "Thailand" til "Vietnam", og opdater by-listen
4. Kopiér `thailand/bangkok.html` som skabelon til hver by-side
5. Tilføj landet på forsiden (`index.html`) — kopiér `.country-card` blokken
   for Thailand, og peg linket på `vietnam/index.html`

## Sådan virker sprogtoggle (DA/EN)

Hver tekst skrives to gange i HTML'en, pakket i `<span>`:

```html
<span data-lang="da">Dansk tekst her</span>
<span data-lang="en">English text here</span>
```

Kun den ene vises ad gangen — styret af `data-lang="da"` eller `data-lang="en"`
på `<html>`-tagget, som skiftes af knappen øverst til højre. Valget huskes i
browseren (localStorage), så det følger med, når man klikker rundt på siden.

**Vigtigt:** Jeg har skrevet et udkast til engelsk oversættelse ud fra dit
danske indhold, men du nævnte at du selv har lavet en oversættelse — så gå
gerne igennem `data-lang="en"`-teksterne og sæt dine egne ord ind i stedet.

## Sådan tilføjer du billeder

Læg billedfiler i `images/`-mappen, og erstat en `<div class="img-placeholder">`
med:

```html
<img src="../images/dit-billede.jpg" alt="Kort beskrivelse">
```

(brug `../images/...` fra by-sider, `images/...` fra forsiden)

## Design

Temaet er "rejsepas / stempler" — cirklerne med stiplet kant (`.stamp`) er
ment som pas-stempler, og by-kortene (`.ticket`) ligner boardingpass. Farver,
fonte og alt andet ligger samlet i `styles.css` som CSS-variabler øverst i
filen (`:root { ... }`), så du nemt kan justere paletten ét sted.
