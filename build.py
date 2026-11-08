#!/usr/bin/env python3
"""Génère index.html (français) et en/index.html (anglais) à partir d'une seule source.

Pour ajouter ou modifier un projet : éditer PROJETS, puis lancer `python3 build.py`.
Stades : "live" (En ligne), "build" (En chantier), "idea" (Idée).
"""
from pathlib import Path
import html, json

ROOT = Path(__file__).parent
SITE = "https://idee.studio"
GA_ID = ""  # identifiant Google Analytics (G-XXXX) de la propriété idee.studio
CONTACT = "contact@idee.studio"

PROJETS = [
    dict(key="ronde", lettre="R", couleur="#0f6b4f", stade="live", url="https://rondesecurite.ca", large=True,
         nom="Ronde Sécurité",
         fr=("La ronde de sécurité des camions et véhicules lourds, sur téléphone : rapport PDF conforme SAAQ, alertes de défauts critiques, zéro papier.", "SaaS · Transport · Québec"),
         en=("Pre-trip inspections for trucks and heavy vehicles, on a phone: SAAQ-compliant PDF reports, critical defect alerts, no paper.", "SaaS · Transportation · Québec")),
    dict(key="depot", lettre="D", couleur="#b5432a", stade="live", url="https://ledepot.co", large=True,
         nom="Le Dépôt",
         fr=("Le workspace des pros de la communication en Afrique francophone : portfolio, campagnes, devis et inspiration au même endroit.", "Plateforme · Créatifs · Afrique"),
         en=("The workspace for communication professionals in French-speaking Africa: portfolio, campaigns, quotes and inspiration in one place.", "Platform · Creatives · Africa")),
    dict(key="souper", lettre="S", couleur="#8a3ffc", stade="live", url="https://souperclub.app",
         nom="Souper Club",
         fr=("Des soupers entre deux couples, au restaurant, pour sortir de la routine et agrandir son cercle. Apps iPhone et Android en chantier.", "Social · Canada"),
         en=("Dinners between two couples, at a restaurant, to break the routine and grow your circle. iPhone and Android apps on the way.", "Social · Canada")),
    dict(key="bercail", lettre="B", couleur="#d98a00", stade="build", url="",
         nom="Bercail",
         fr=("L'app de la maison : budget, repas, tâches et agenda de la famille, réunis au même endroit.", "Famille · Organisation"),
         en=("The home app: the family's budget, meals, chores and calendar, all in one place.", "Family · Organization")),
    dict(key="comptoir", lettre="C+", couleur="#1d6fd8", stade="build", url="",
         nom="Comptoir+",
         fr=("Les commandes et la caisse des bars et maquis : serveuses, comptoir et encaissement en espèces ou Mobile Money.", "Commerce · Afrique"),
         en=("Orders and checkout for bars and maquis: servers, counter, and payment in cash or Mobile Money.", "Retail · Africa")),
    dict(key="cinelens", lettre="Ci", couleur="#e0245e", stade="idea", url="",
         nom="CinéLens",
         fr=("Retrouvez un film à partir d'une capture d'écran : titre, casting, où le regarder et films similaires, grâce à l'IA.", "IA · Cinéma"),
         en=("Find a film from a screenshot: title, cast, where to stream it and similar films, powered by AI.", "AI · Film")),
    dict(key="conseil", lettre="GA", couleur="#15130f", stade="live", url="https://gildasattachi.com", xl=True,
         nom="gildasattachi.com",
         fr=("La pratique conseil du fondateur : communication interne, marque employeur et gestion du changement, au Québec.", "Conseil · Communication"),
         en=("The founder's consulting practice: internal communication, employer branding and change management, in Québec.", "Consulting · Communication")),
]

T = {
    "fr": dict(
        lang="fr-CA", path="/", other="/en/", other_label="EN", self_label="FR",
        title="Idée Studio · La boîte à idées qui devient produits",
        desc="Idée Studio conçoit, construit et fait grandir des applications utiles, au Québec et en Afrique francophone : Ronde Sécurité, Le Dépôt, Souper Club et les prochaines.",
        skip="Aller au contenu", nav=("La boîte", "Démarche", "Contact"),
        eyebrow="Studio de produits numériques · Québec",
        h1='Une boîte à <em>idées</em> qui deviennent des produits<span class="dot">.</span>',
        lead="Idée Studio conçoit, construit et fait grandir des applications utiles. Chaque projet commence comme une fiche dans la boîte, puis sort quand il est prêt à servir.",
        cta=("Ouvrir la boîte", "Déposer une idée"),
        ticker=["Concevoir", "Construire", "Lancer", "Écouter", "Améliorer", "Faire grandir"],
        box_kicker="La boîte à idées", box_h2="Ce qui sort de la boîte.",
        box_p="Des produits en ligne, d'autres en chantier, et des idées qui attendent leur tour.",
        filters=("Tout", "En ligne", "En chantier", "Idées"),
        stades={"live": "En ligne", "build": "En chantier", "idea": "Idée"},
        idea_n="Idée n°", visit="Visiter", soon="Prochainement",
        steps_kicker="Démarche", steps_h2="De la fiche au produit.",
        steps_p="Une méthode simple, appliquée à chaque idée de la boîte.",
        steps=[("Concevoir", "On part d'un vrai problème, observé sur le terrain, et on le dessine avec ceux qui le vivent."),
               ("Construire", "Une première version utile, rapide et soignée, sur le web et sur téléphone."),
               ("Faire grandir", "On mesure, on écoute, on améliore. Le produit évolue avec ses utilisateurs.")],
        contact_h2="Une idée à déposer dans la boîte ?",
        contact_p="Un projet, un partenariat, une question sur nos produits : écrivez au studio, on répond vite.",
        contact_btn="Écrire au studio", rights="Tous droits réservés.",
    ),
    "en": dict(
        lang="en-CA", path="/en/", other="/", other_label="FR", self_label="EN",
        title="Idée Studio · An idea box that turns into products",
        desc="Idée Studio designs, builds and grows useful apps, in Québec and French-speaking Africa: Ronde Sécurité, Le Dépôt, Souper Club and what comes next.",
        skip="Skip to content", nav=("The box", "Approach", "Contact"),
        eyebrow="Digital product studio · Québec",
        h1='An <em>idea</em> box that turns into products<span class="dot">.</span>',
        lead="Idée Studio designs, builds and grows useful apps. Every project starts as a card in the box, and comes out when it's ready to help.",
        cta=("Open the box", "Drop an idea"),
        ticker=["Design", "Build", "Launch", "Listen", "Improve", "Grow"],
        box_kicker="The idea box", box_h2="What comes out of the box.",
        box_p="Products that are live, others under construction, and ideas waiting their turn.",
        filters=("All", "Live", "In progress", "Ideas"),
        stades={"live": "Live", "build": "In progress", "idea": "Idea"},
        idea_n="Idea no. ", visit="Visit", soon="Coming soon",
        steps_kicker="Approach", steps_h2="From card to product.",
        steps_p="A simple method, applied to every idea in the box.",
        steps=[("Design", "We start from a real problem, seen in the field, and shape it with the people who live it."),
               ("Build", "A first useful version, fast and polished, on the web and on phones."),
               ("Grow", "We measure, listen and improve. The product evolves with its users.")],
        contact_h2="Got an idea for the box?",
        contact_p="A project, a partnership, a question about our products: write to the studio, we reply quickly.",
        contact_btn="Write to the studio", rights="All rights reserved.",
    ),
}

e = html.escape


def carte(p, i, t, lg):
    desc, tags = p[lg]
    stade = p["stade"]
    tag = "a" if p["url"] else "div"
    attrs = f' href="{p["url"]}" target="_blank" rel="noopener"' if p["url"] else ' aria-disabled="true"'
    cls = "card reveal" + (" wide" if p.get("large") else "") + (" xl" if p.get("xl") else "") + ("" if p["url"] else " is-soon")
    pied = (f'<span class="go">{t["visit"]} {e(p["url"].replace("https://", ""))}</span>' if p["url"]
            else f'<span class="go-soon">{t["soon"]}</span>')
    return f'''      <{tag} class="{cls}" data-stade="{stade}" style="--c:{p["couleur"]}"{attrs}>
        <div class="card-top"><span class="mark" aria-hidden="true">{e(p["lettre"])}</span><span class="status {stade}">{t["stades"][stade]}</span></div>
        <div>
          <div class="num">{t["idea_n"]}{i:02d}</div>
          <h3>{e(p["nom"])}</h3>
          <p>{e(desc)}</p>
        </div>
        <div class="rule" aria-hidden="true"></div>
        <div class="card-foot"><span class="tags">{e(tags)}</span>{pied}</div>
      </{tag}>'''


def page(lg):
    t = T[lg]
    compte = {k: sum(1 for p in PROJETS if p["stade"] == k) for k in ("live", "build", "idea")}
    cartes = "\n".join(carte(p, i + 1, t, lg) for i, p in enumerate(PROJETS))
    ticker = "".join(f"<span>{e(w)}</span>" for w in t["ticker"] * 2)
    steps = "\n".join(f'      <div class="step reveal"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in t["steps"])
    ld = {
        "@context": "https://schema.org", "@type": "Organization", "name": "Idée Studio",
        "url": SITE, "email": CONTACT, "logo": f"{SITE}/assets/icon.svg",
        "description": t["desc"],
        "owns": [{"@type": "SoftwareApplication" if p["key"] != "conseil" else "WebSite", "name": p["nom"], **({"url": p["url"]} if p["url"] else {})} for p in PROJETS],
    }
    ga = (f'''  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}',{{anonymize_ip:true}});</script>
''' if GA_ID else "")
    f, l, b, i_ = t["filters"]
    return f'''<!doctype html>
<html lang="{t["lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(t["title"])}</title>
  <meta name="description" content="{e(t["desc"])}">
  <link rel="canonical" href="{SITE}{t["path"]}">
  <link rel="alternate" hreflang="fr-CA" href="{SITE}/">
  <link rel="alternate" hreflang="en-CA" href="{SITE}/en/">
  <link rel="alternate" hreflang="x-default" href="{SITE}/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Idée Studio">
  <meta property="og:title" content="{e(t["title"])}">
  <meta property="og:description" content="{e(t["desc"])}">
  <meta property="og:url" content="{SITE}{t["path"]}">
  <meta property="og:image" content="{SITE}/assets/og.png">
  <meta property="og:locale" content="{t["lang"].replace("-", "_")}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#f5f1ea">
  <link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Inter+Tight:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="/assets/styles.css">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{ga}</head>
<body>
  <a class="skip" href="#contenu">{t["skip"]}</a>
  <header class="top">
    <div class="wrap">
      <a class="logo" href="{t["path"]}" aria-label="Idée Studio"><b>id<span class="acc">é</span>e</b><small>studio</small></a>
      <nav class="nav" aria-label="Navigation">
        <a class="hide-sm" href="#boite">{t["nav"][0]}</a>
        <a class="hide-sm" href="#demarche">{t["nav"][1]}</a>
        <a class="hide-sm" href="#contact">{t["nav"][2]}</a>
        <span class="lang"><a href="{t["path"]}" aria-current="true">{t["self_label"]}</a><a href="{t["other"]}" hreflang="{"en" if lg == "fr" else "fr"}">{t["other_label"]}</a></span>
      </nav>
    </div>
  </header>

  <main id="contenu">
    <section class="hero">
      <svg class="orbit" viewBox="0 0 320 320" aria-hidden="true">
        <circle cx="160" cy="160" r="150"/><circle cx="160" cy="160" r="104"/><circle cx="160" cy="160" r="58"/>
        <circle class="dot" cx="160" cy="10" r="9"/><circle class="dot b" cx="160" cy="56" r="6"/>
      </svg>
      <div class="wrap">
        <span class="eyebrow">{e(t["eyebrow"])}</span>
        <h1>{t["h1"]}</h1>
        <p class="lead">{e(t["lead"])}</p>
        <div class="cta">
          <a class="btn btn-ink" href="#boite">{t["cta"][0]}</a>
          <a class="btn btn-line" href="mailto:{CONTACT}">{t["cta"][1]}</a>
        </div>
      </div>
    </section>

    <div class="ticker" aria-hidden="true"><div class="ticker-track">{ticker}</div></div>

    <section class="section" id="boite">
      <div class="wrap">
        <div class="section-head">
          <div><span class="eyebrow">{t["box_kicker"]}</span><h2>{t["box_h2"]}</h2></div>
          <p>{t["box_p"]}</p>
        </div>
        <div class="filters" role="group" aria-label="Filtres">
          <button class="chip" data-filtre="all" aria-pressed="true">{f}<span class="n">{len(PROJETS)}</span></button>
          <button class="chip" data-filtre="live" aria-pressed="false">{l}<span class="n">{compte["live"]}</span></button>
          <button class="chip" data-filtre="build" aria-pressed="false">{b}<span class="n">{compte["build"]}</span></button>
          <button class="chip" data-filtre="idea" aria-pressed="false">{i_}<span class="n">{compte["idea"]}</span></button>
        </div>
        <div class="grid">
{cartes}
        </div>
      </div>
    </section>

    <section class="section" id="demarche">
      <div class="wrap">
        <div class="section-head">
          <div><span class="eyebrow">{t["steps_kicker"]}</span><h2>{t["steps_h2"]}</h2></div>
          <p>{t["steps_p"]}</p>
        </div>
        <div class="steps">
{steps}
        </div>
      </div>
    </section>

    <section class="section" id="contact">
      <div class="wrap">
        <div class="contact reveal">
          <h2>{t["contact_h2"]}</h2>
          <p>{t["contact_p"]}</p>
          <a class="btn" href="mailto:{CONTACT}">{t["contact_btn"]} · {CONTACT}</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="foot">
    <div class="wrap">
      <span>© <span data-annee>2026</span> Idée Studio. {t["rights"]}</span>
      <a href="mailto:{CONTACT}">{CONTACT}</a>
    </div>
  </footer>
  <script src="/assets/main.js" defer></script>
</body>
</html>
'''


(ROOT / "index.html").write_text(page("fr"), encoding="utf-8")
(ROOT / "en").mkdir(exist_ok=True)
(ROOT / "en" / "index.html").write_text(page("en"), encoding="utf-8")
(ROOT / "sitemap.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url><loc>{SITE}/</loc><xhtml:link rel="alternate" hreflang="fr-CA" href="{SITE}/"/><xhtml:link rel="alternate" hreflang="en-CA" href="{SITE}/en/"/></url>
  <url><loc>{SITE}/en/</loc><xhtml:link rel="alternate" hreflang="fr-CA" href="{SITE}/"/><xhtml:link rel="alternate" hreflang="en-CA" href="{SITE}/en/"/></url>
</urlset>
''', encoding="utf-8")
print("Pages générées : index.html, en/index.html, sitemap.xml")
