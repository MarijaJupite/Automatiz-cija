241RDB126 Darja Kučerenko 1.grupa

241RDB067 Marija Jupite 5. grupa

# Automatizācija
---
## Īss programmas apraksts:
### Mūsu projektam mēs izvēlējāmies meklēšanas automatizāciju jeb **web scraping** — tehnoloģiju, kas ļauj automātiski savākt konkrētu informāciju no interneta vietnēm.

**Programma veic meklēšanu un informācijas savākšanu no vietnes** ar receptēm **[Garšīga Latvija](https://www.garsigalatvija.lv/)**.
Lietotājam tiek piedāvāta iespēja izvēlēties dažādu veidu receptes — piemēram, brokastis, zupas, deserti un citas kategorijas.
Pēc kategorijas izvēles programma automātiski atrod un parāda visas receptes šajā grupā.
Lietotājs var apskatīt sastāvdaļas un veidot recepšu izlasi.

---

## Projekta uzdevums:

Galvenais projekta uzdevums ir **izveidot ērtu automatizētu rīku**,
kas ļauj lietotājam ātri **atrast** vajadzīgo recepti,
**apskatīt** tās sastāvdaļas
un **saglabāt** iecienītās receptes,
neizmantojot pārlūkprogrammu un manuālu meklēšanu.

---

## Programmatūras izmantošanas metodes:

1. Lietotājs ievada *izvēlēto kategorijas numuru* no saraksta (piemēram, **2** - Zupas).
2. Programma savāc un parāda sarakstu no visam receptiem izvelētajā kategorijā - numurēto sarakstu ar katra recepta nosaukumu un saiti uz to.
3. Lietotājs var *izvēlēties receptes numuru* un ievadīt to, lai apskatītu tās sastāvdaļas.
4. Kad receptes sastāvdaļas tiek rādītas, lietotājam tiek dota iespēja *pievienot šo recepti izlasei* (Favorites), ievadot burtu **f**.
5. Izlase tiek saglabāta atsevišķā failā, un *tajā var piekļūt* jebkurā brīdī *no galvenā izvēlnes*, ievadot **0**.
6. Izlasē lietotājs var apskatīt saglabātās receptes, skatīt to sastāvdaļas vai *dzēst receptes no izlases* ievadot burtu **d**.
7. Programma nodrošina arī iespēju jebkurā brīdī *atgriezties pie kategoriju izvēles* vai *iziet no programmas*, ievadot **-1**.

---

## Python bibliotēkas, izmantotas projekta izstrādes laikā:

* 'requests' — nepieciešama, lai lejupielādētu tīmekļa lapas no interneta.
  Mūsu kodā to izmantojam, lai ielādētu receptes no vietnes garsigalatvija.lv un pārvietotos starp kategorijām un recepšu lapām.

* 'BeautifulSoup' (no 'bs4') — tiek lietota HTML koda parsēšanai un nepieciešamās informācijas iegūšanai.
  Mēs izmantojam šo bibliotēku, lai no lapas iegūtu recepšu nosaukumus, saites un sastāvdaļu sarakstu.

* 'json' — tiek izmantots, lai saglabātu un ielādētu iecienītās receptes failā 'favorites.json'.
  Tas ļauj lietotājam saglabāt patikušās receptes un skatīt tās vēlāk.

---

## Izmantotas definētas datu struktūras - klases 'Category' un 'Recipe':

* 'Category' — satur kategorijas nosaukumu un adresi lapai ar šīs kategorijas receptēm.
* 'Recipe' — satur receptes nosaukumu, saiti uz to un sastāvdaļu sarakstu.
