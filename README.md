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
│   │   │   │   ...
│   │   │   └── BRID_ee25756e-b517-4953-984a-9f4794cbbebc.json
│   │   └── 2
│   │       ├── BID_001328a4-3279-492c-99da-8e51f8e9a587.json
│   │       │   ...
│   │       └── BID_fff80110-f6d3-4587-8e54-67dfb0d93453.json
│   ├── lines
│   │       ...
│   └── points
│           ...
├── metadata
│   ├── BID_001328a4-3279-492c-99da-8e51f8e9a587.json
│   │   ...
│   └── BRID_ee25756e-b517-4953-984a-9f4794cbbebc.json
├── tiles
│   ├── facets
│   │   ├── 1
│   │   │   ...
│   │   └── 2
│   │       ...
│   ├── lines
│   │       ...
│   └── points
│           ...
│
└── exports

```

- název souboru je ID objektu, jehož se obsah souboru týká
- `metadata` obsahuje metadata jednotlivých budov
- `geometry` obsahuje podadresáře odpovídající typům geometrie obsažené v objektech, které jsou dále dělěny do podadresářů dle jejich lod, v souborech je dump vertex, normal a semantic bufferů (base64-coded numpy array (buffer)) 
- `export` - exporty, název odpovídá primitivu + lod


- OBJEKT = všechny dostupné informace pro identifikátor (geometrie + metadata)
- MODEL = geometrická data daného typu (point, line, facet) pro dané lod 

## Query ke zvážení

- Exportuj goemterii pro každou budovu v tom nejvyšším dostupném LOD

## TODOs
https://github.com/orgs/MetacitySuite/projects/1#card-64130535 (private project). 