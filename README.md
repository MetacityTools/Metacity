# Metacity

- [x] Konverze CityGML do CityJSONu
- [ ] Segmentace modelu
- [ ] Struktura pro streamování modelu


## Log

- zpracována instalace CityGML Tools, instalace Javy - zatím manuální, totžná instalace javy je potřeba pro spuštění MATSimu, doporučeno instalovat globálně OpenJDK verze 11, při instalaci lze verzi ověřit ve výpise 
- skript pro konverzi v pythonu napojen na java framework CityGML-tools

## Zpracování geometrie

1. otevření a načtení souboru
2. segmentace objektů a export geometrie s metadaty:
    - export dle typu modelu
    - export dle lod
    - export dle lokace (bounding boxy)
3. rozřezání geometrie na dlaždice a export do interní reprezentace

## Reprezentace segmentované geometrie
Po zpracování je v adresáři `segmented` podadresář `geometry`. V tomto adresáři se nachází dělení segmentované geometrie dle dostupných LOD. 

- každý objekt může mít více LOD a ještě navíc více geometrií pro každé LOD

Triangulace pomocí self-deplynutého `earcut` balíčku https://github.com/MetacitySuite/earcut-python 

Metacity reprezentuje zvlášť 
- geometrie
- meta
- semantika

Stěny jsou triangulované, každý vertex:

- souřadnice
- normála
- texturovací souřadnice
- id do tabulky s meta budov
- id do tabulky se semantikou geometrie

## Query ke zvážení

- Exportuj goemterii pro akždou budovu v tom nejvyšším dostupném LOD

