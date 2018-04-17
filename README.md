# Statistik från Stockholms bostadsförmedling

Detta projekt innehållet data om bostadsförmedling från bostad.stockholm.se, kod för att skrapa den och kod för att 
presentera/utforska datat.

## Vad/hur datat hämtats

Bostadsförmedlingen har en [statistiktjänst](https://bostad.stockholm.se/statistik/statistiktjansten/) där de presenterar
aggregerad data med vissa filter. När man klickar på en stapel visas 10 av de förmedlade bostäderna med en del data (det
är ändra stället de skriver ut kötiden för den som fick lägenheten, vad jag vet). Den listan kan man få ut opaginerad genom
att posta med lämpliga filter till https://bostad.stockholm.se/statistik/statistiktjansten/RenderApartmentList/. Datat 
därifrån finns i [data/full_list.json](data/full_list.json).

Tyvärr innehåller de samlade listorna inte all info jag behövde, så jag har skrapat detaljsidan för alla annonser som finns
med i de listorna. Därifrån har jag bland annat kunnat hämta ut datum för annonsen, hyresvärd och koordinater. Datat 
därifrån finns i [data/extra_ad_data.json](data/extra_ad_data.json).

En sammanslagning av de två finns i [data/full_data.json](data/full_data.json)

## Vad kan man göra med datat?

You tell me. Själv var jag nyfiken på att se hur vad som förmedlats senaste året inom den kötid jag har och vissa andra
kriterier (alltid bra att veta om det är helt hopplöst eller bara lite hopplöst).

Du kan själv utforska datat på [alvinlindstam.github.io/bostadsdata](https://alvinlindstam.github.io/bostadsdata). Jag 
har inte direkt engagerat mig i design eller användbarhet, men mer eller mindre alla grafer eller inputfält kan användas för
att filtrera ut de förmedlingar som är intressanta.

## Uppdatera data

Allt detta bygger på att bostadsförmedlingens statistiktjänst och annonser har en viss struktur. Om den ändras får scripten
uppdateras. Som det är nu behöver man köra fyra script för att hålla hämta senaste datan:

  1. `download_list.py`
  2. `parse_lists.py`
  3. `get_extra_data.py`
  4. `merge_data.py`

Bara byggt för python 3.
