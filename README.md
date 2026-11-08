# idee.studio

Site vitrine d'Idée Studio : la « boîte à idées » qui liste tous les projets du studio.

- Site statique (HTML, CSS, un peu de JS), en français (`/`) et en anglais (`/en/`).
- **Une seule source :** `build.py`. Pour ajouter ou changer un projet, modifier la liste `PROJETS`, puis lancer `python3 build.py`, qui régénère `index.html`, `en/index.html` et `sitemap.xml`.
- Stades d'un projet : `live` (En ligne), `build` (En chantier), `idea` (Idée).
- Google Analytics : renseigner `GA_ID` dans `build.py` (propriété idee.studio du compte GA « Idée Studio »).
- Hébergement : GitHub Pages, domaine `idee.studio` (fichier `CNAME`).
- Aperçu local : `python3 -m http.server 4321`, puis http://localhost:4321
