# Metacity

Toolkit pro zpracování a vizualizaci urbanistických dat

## Adresářová Metastruktura

```
project/
├── config.json
├── geometry
│   ├── facets
│   │   ├── 1
│   │   │   ├── BID_001328a4-3279-492c-99da-8e51f8e9a587.json
│   │   │   │   ...
│   │   │   └── BRID_ee25756e-b517-4953-984a-9f4794cbbebc.json
│   │   └── 2
│   │       ├── BID_001328a4-3279-492c-99da-8e51f8e9a587.json
│   │       │   ...
│   │       └── BID_fff80110-f6d3-4587-8e54-67dfb0d93453.json
│   ├── line
│   └── points
├── objects
│   ├── BID_001328a4-3279-492c-99da-8e51f8e9a587.json
│   │   ... 
│   └── BRID_ee25756e-b517-4953-984a-9f4794cbbebc.json
└── stl
    ├── facets_1.stl
    └── facets_2.stl
```

- náyev souboru je ID objektu, jehož se obsah souboru týká
- `objects` obsahuje dump jednotlivých objektů v CityJSON souborech
- `geometry` obsahuje podadresáře odpovídající typům geometrie obsažené v objektech, které jsou dále dělěny do podadresářů dle jejich lod, v souborech je dump vertex, normal a semantic bufferů (base64-coded numpy array (buffer)) 
- `stl` - stl exporty, název odpovídá primitivu + lod


## Install and Run Info

- zpracována instalace CityGML Tools + instalace Javy, pro opakované spuštění je potřeba doplnit cesty do .bashrc 
- skript pro konverzi v pythonu napojen na java framework CityGML-tools


## Reprezentace segmentované geometrie
Po zpracování je v adresář `geometry`. V tomto adresáři se nachází dělení segmentované geometrie dle typu primitiva a dostupných LOD. 

- každý objekt může mít více LOD a ještě navíc více geometrií pro každé LOD
- triangulace se prování pomocí self-deplynutého `earcut` balíčku https://github.com/MetacitySuite/earcut-python 

Metacity reprezentuje zvlášť 
- geometrie
- meta
- semantika

Stěny jsou triangulované, každý vertex:

- pozice
- normála
- id do tabulky s meta budov
- id do tabulky se semantikou geometrie budovy (části budovy, fasády)

## Query ke zvážení

- Exportuj goemterii pro akždou budovu v tom nejvyšším dostupném LOD

## TODOs
https://github.com/orgs/MetacitySuite/projects/1#card-64130535 (private project). 