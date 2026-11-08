#!/usr/bin/env python3
"""Génère index.html (français), en/index.html (anglais) et sitemap.xml à partir d'une seule source.

Ajouter ou modifier un projet : éditer PROJETS, puis lancer `python3 build.py`.
Stades : "live" (En ligne), "build" (En chantier), "idea" (Idée).
Images : assets/img/<cle>-mobile.jpg (capture téléphone) et, si présente, une capture ordinateur.
"""
from pathlib import Path
import html, json

ROOT = Path(__file__).parent
SITE = "https://idee.studio"
GA_ID = ""  # identifiant Google Analytics (G-XXXX) de la propriété idee.studio
CONTACT = "contact@idee.studio"
e = html.escape

# bg = fond du chapitre, fg = texte, ac = couleur d'accent (celle du produit), dark = chapitre sombre
PROJETS = [
    dict(key="ronde", nom="Ronde Sécurité", stade="live", url="https://rondesecurite.ca",
         logo="ronde.svg", desktop="ronde-desktop.jpg", mobile="ronde-mobile.jpg",
         bg="#edf2ff", fg="#0d1430", ac="#1b5bff", dark=False,
         fr=dict(domaine="Transport", titre="La ronde de sécurité SAAQ, sur téléphone.",
                 texte="Les chauffeurs de camions font leur ronde avant départ en deux minutes. Les gestionnaires reçoivent le rapport PDF conforme et une alerte au moindre défaut critique.",
                 faits=["Web · iPhone · Android", "Flottes de véhicules lourds", "Sur l'App Store"]),
         en=dict(domaine="Transportation", titre="SAAQ pre-trip inspections, on a phone.",
                 texte="Truck drivers complete their pre-trip inspection in two minutes. Fleet managers get the compliant PDF report and an alert for any critical defect.",
                 faits=["Web · iPhone · Android", "Heavy-vehicle fleets", "On the App Store"])),
    dict(key="depot", nom="Le Dépôt", stade="live", url="https://ledepot.co",
         logo="depot.png", desktop="depot-galerie.jpg", mobile="depot-mobile.jpg",
         bg="#0c0c0b", fg="#f3f1ea", ac="#e9a825", dark=True, logo_invert=True,
         fr=dict(domaine="Création", titre="Le workspace des pros de la com africaine.",
                 texte="Portfolio, planner des médias sociaux, clients, devis et factures, adossés à une bibliothèque vivante des campagnes qui se font vraiment en Afrique francophone.",
                 faits=["154 campagnes publiées", "Afrique francophone", "Web"]),
         en=dict(domaine="Creative", titre="The workspace for Africa's communication pros.",
                 texte="Portfolio, social media planner, clients, quotes and invoices, built on a living library of the campaigns actually made in French-speaking Africa.",
                 faits=["154 published campaigns", "French-speaking Africa", "Web"])),
    dict(key="souper", nom="Souper Club", stade="live", url="https://souperclub.app",
         logo="souper.png", desktop="souper-desktop.jpg", mobile="souper-mobile.jpg",
         bg="#f1ecf6", fg="#211d2c", ac="#7b5cc4", dark=False,
         fr=dict(domaine="Social", titre="Sortez de votre tête-à-tête.",
                 texte="Deux couples, une bonne table, et la suite leur appartient. On choisit une table, on fait connaissance à son rythme, dans un lieu public.",
                 faits=["Canada · français et anglais", "Web en ligne", "Apps iPhone et Android en chantier"]),
         en=dict(domaine="Social", titre="Step out of your date-night routine.",
                 texte="Two couples, a good table, and the rest is up to them. Pick a table and get to know each other at your own pace, in a public place.",
                 faits=["Canada · French and English", "Live on the web", "iPhone and Android apps in progress"])),
    dict(key="bercail", nom="Bercail", stade="build", url="",
         logo="bercail.svg", desktop="", mobile="bercail-mobile.jpg",
         bg="#e7ebe2", fg="#13201b", ac="#13201b", dark=False,
         fr=dict(domaine="Famille", titre="La maison, en ordre.",
                 texte="Le budget, les repas, les tâches et l'agenda de la famille dans une seule app, avec une journée claire pour chacun, enfants compris.",
                 faits=["Budget · repas · tâches · agenda", "Connexion par clé d'accès", "Utilisée chaque jour à la maison"]),
         en=dict(domaine="Family", titre="A home, in order.",
                 texte="The family's budget, meals, chores and calendar in one app, with a clear day for everyone, kids included.",
                 faits=["Budget · meals · chores · calendar", "Passkey sign-in", "Used daily at home"])),
    dict(key="comptoir", nom="Comptoir+", stade="build", url="",
         logo="", desktop="", mobile="comptoir-mobile.jpg",
         bg="#15120f", fg="#f4ede4", ac="#ff6b2c", dark=True,
         fr=dict(domaine="Commerce", titre="Le bar, du comptoir à la caisse.",
                 texte="Serveuses, comptoir, cuisine et gérant sur le même téléphone : les commandes partent des tables, la caisse se compte en fin de journée, en espèces ou en Mobile Money.",
                 faits=["Bars et maquis", "Espèces · Mobile Money", "Prototype pour bars pilotes"]),
         en=dict(domaine="Retail", titre="The bar, from counter to cash drawer.",
                 texte="Servers, counter, kitchen and manager on the same phone: orders leave the tables, and the till is counted at day's end, in cash or Mobile Money.",
                 faits=["Bars and maquis", "Cash · Mobile Money", "Prototype for pilot bars"])),
    dict(key="cinelens", nom="CinéLens", stade="idea", url="",
         logo="", desktop="cinelens-desktop.jpg", mobile="cinelens-mobile.jpg",
         bg="#0b0906", fg="#f6efe0", ac="#d9a441", dark=True,
         fr=dict(domaine="IA", titre="Le film, à partir d'une capture.",
                 texte="On glisse une capture d'écran d'une scène. L'IA retrouve le titre, l'année, le réalisateur, le casting, où le regarder et des films proches.",
                 faits=["Analyse d'image par IA", "Jusqu'à 5 captures", "Idée"]),
         en=dict(domaine="AI", titre="The film, from a single screenshot.",
                 texte="Drop in a screenshot of a scene. AI finds the title, year, director, cast, where to stream it and similar films.",
                 faits=["AI image analysis", "Up to 5 screenshots", "Idea"])),
    dict(key="conseil", nom="gildasattachi.com", stade="live", url="https://gildasattachi.com",
         logo="", desktop="conseil-desktop.jpg", mobile="",
         bg="#f4f3ef", fg="#121210", ac="#121210", dark=False,
         fr=dict(domaine="Conseil", titre="La pratique conseil du fondateur.",
                 texte="Communication interne et 360, marque employeur et gestion du changement, pour des organisations du Québec.",
                 faits=["Communication · changement", "Québec", "Web"]),
         en=dict(domaine="Consulting", titre="The founder's consulting practice.",
                 texte="Internal and 360 communication, employer branding and change management, for organizations in Québec.",
                 faits=["Communication · change", "Québec", "Web"])),
]

T = {
    "fr": dict(
        lang="fr-CA", path="/", other="/en/", self_label="FR", other_label="EN",
        title="Idée Studio · Une boîte à idées, et ce qui en sort",
        desc="Idée Studio conçoit et construit ses propres produits numériques au Québec : Ronde Sécurité, Le Dépôt, Souper Club, Bercail, Comptoir+ et CinéLens.",
        skip="Aller au contenu", nav=("Projets", "Contact"),
        h1a="Une boîte à idées.", h1b="Voici ce qui en sort.",
        intro="On conçoit et on construit nos propres produits, du premier croquis jusqu'à l'App Store. Des outils simples pour des métiers précis : transporteurs, créatifs, couples, familles, bars.",
        compte=lambda n, l, b, i: f"{n} projets · {l} en ligne · {b} en chantier · {i} idée",
        stades={"live": "En ligne", "build": "En chantier", "idea": "Idée"},
        index_titre="Dans la boîte", cols=("N°", "Projet", "Domaine", "Stade"),
        visiter="Visiter", bientot="Bientôt",
        contact_k="Déposer une idée", contact_h="Une idée, un projet, un partenariat ?",
        contact_p="Écrivez au studio. On lit tout, et on répond vite.",
        bas="Conçu et construit au Québec.",
    ),
    "en": dict(
        lang="en-CA", path="/en/", other="/", self_label="EN", other_label="FR",
        title="Idée Studio · An idea box, and what comes out of it",
        desc="Idée Studio designs and builds its own digital products in Québec: Ronde Sécurité, Le Dépôt, Souper Club, Bercail, Comptoir+ and CinéLens.",
        skip="Skip to content", nav=("Projects", "Contact"),
        h1a="An idea box.", h1b="Here's what comes out.",
        intro="We design and build our own products, from the first sketch all the way to the App Store. Simple tools for specific trades: truckers, creatives, couples, families, bars.",
        compte=lambda n, l, b, i: f"{n} projects · {l} live · {b} in progress · {i} idea",
        stades={"live": "Live", "build": "In progress", "idea": "Idea"},
        index_titre="In the box", cols=("No.", "Project", "Field", "Stage"),
        visiter="Visit", bientot="Soon",
        contact_k="Drop an idea", contact_h="An idea, a project, a partnership?",
        contact_p="Write to the studio. We read everything, and reply quickly.",
        bas="Designed and built in Québec.",
    ),
}


def wordmark(p):
    """Logo réel quand il existe, sinon le mot-symbole dans la police du produit."""
    if p["logo"] == "depot.png":
        return f'<span class="wm"><img class="lg-wide" src="/assets/logos/depot.png" alt="Le Dépôt" style="filter:invert(1)" width="160" height="40"></span>'
    if p["logo"]:
        return f'<span class="wm"><img class="lg-icon" src="/assets/logos/{p["logo"]}" alt="" width="44" height="44"><span class="wm-txt">{e(p["nom"])}</span></span>'
    if p["key"] == "comptoir":
        return '<span class="wm wm-comptoir">Comptoir<b>+</b></span>'
    if p["key"] == "cinelens":
        return '<span class="wm wm-cinelens">CinéLens</span>'
    return f'<span class="wm wm-plain">{e(p["nom"])}</span>'


def phone(src, alt, cls=""):
    return f'<figure class="phone {cls}"><img src="/assets/img/{src}" alt="{e(alt)}" loading="lazy" width="390" height="800"></figure>'


def browser(src, alt):
    return f'<figure class="browser"><span class="dots" aria-hidden="true"></span><img src="/assets/img/{src}" alt="{e(alt)}" loading="lazy" width="1600" height="867"></figure>'


def page(lg):
    t = T[lg]
    n = len(PROJETS)
    c = {k: sum(p["stade"] == k for p in PROJETS) for k in ("live", "build", "idea")}

    avec_mobile = [p for p in PROJETS if p["mobile"]]
    fan = "\n".join(
        f'        <li style="--i:{i};--n:{len(avec_mobile)}"><a href="#p-{p["key"]}" aria-label="{e(p["nom"])}">{phone(p["mobile"], p["nom"])}</a></li>'
        for i, p in enumerate(avec_mobile))

    rows = []
    for i, p in enumerate(PROJETS, 1):
        L = p[lg]
        prev = p["mobile"] or p["desktop"]
        rows.append(f'''        <li><a class="row" href="#p-{p["key"]}" data-preview="/assets/img/{prev}" style="--ac:{p["ac"] if not p["dark"] else p["ac"]}">
          <span class="c-n">{i:02d}</span><span class="c-name">{e(p["nom"])}</span>
          <span class="c-dom">{e(L["domaine"])}</span><span class="c-st st-{p["stade"]}">{t["stades"][p["stade"]]}</span>
        </a></li>''')

    chaps = []
    for i, p in enumerate(PROJETS, 1):
        L = p[lg]
        faits = "".join(f"<li>{e(f)}</li>" for f in L["faits"])
        cta = (f'<a class="go" href="{p["url"]}" target="_blank" rel="noopener">{t["visiter"]} {e(p["url"].replace("https://", ""))} <span aria-hidden="true">↗</span></a>'
               if p["url"] else f'<span class="go go-off">{t["bientot"]}</span>')
        if p["desktop"] and p["mobile"]:
            visu = f'<div class="visu duo">{browser(p["desktop"], p["nom"])}{phone(p["mobile"], p["nom"], "over")}</div>'
        elif p["desktop"]:
            visu = f'<div class="visu solo">{browser(p["desktop"], p["nom"])}</div>'
        else:
            visu = f'<div class="visu single">{phone(p["mobile"], p["nom"])}</div>'
        chaps.append(f'''    <section class="chap{' dark' if p['dark'] else ''}" id="p-{p["key"]}" style="--bg:{p["bg"]};--fg:{p["fg"]};--ac:{p["ac"]}">
      <div class="chap-in">
        <div class="txt">
          <div class="meta"><span>{i:02d}</span><span>{e(L["domaine"])}</span><span class="st-{p["stade"]}">{t["stades"][p["stade"]]}</span></div>
          {wordmark(p)}
          <h2>{e(L["titre"])}</h2>
          <p>{e(L["texte"])}</p>
          <ul class="facts">{faits}</ul>
          {cta}
        </div>
        {visu}
      </div>
    </section>''')

    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Idée Studio", "url": SITE,
          "email": CONTACT, "logo": f"{SITE}/assets/icon.svg", "description": t["desc"],
          "address": {"@type": "PostalAddress", "addressRegion": "QC", "addressCountry": "CA"}}
    ga = (f'''  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}',{{anonymize_ip:true}});</script>
''' if GA_ID else "")
    autre = "en" if lg == "fr" else "fr"

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
  <meta property="og:image" content="{SITE}/assets/og.jpg">
  <meta property="og:locale" content="{t["lang"].replace("-", "_")}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#f6f5f1">
  <link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500&family=Bodoni+Moda:opsz,wght@6..96,700&family=Plus+Jakarta+Sans:wght@800&display=swap">
  <link rel="stylesheet" href="/assets/styles.css">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{ga}</head>
<body>
  <a class="skip" href="#contenu">{t["skip"]}</a>
  <header class="top">
    <a class="brand" href="{t["path"]}" aria-label="Idée Studio">idée<span>studio</span></a>
    <nav aria-label="Navigation">
      <a class="hide-sm" href="#projets">{t["nav"][0]}</a>
      <a class="hide-sm" href="#contact">{t["nav"][1]}</a>
      <span class="lang"><a href="{t["path"]}" aria-current="true">{t["self_label"]}</a><a href="{t["other"]}" hreflang="{autre}">{t["other_label"]}</a></span>
    </nav>
  </header>

  <main id="contenu">
    <section class="hero">
      <div class="hero-txt">
        <p class="count">{t["compte"](n, c["live"], c["build"], c["idea"])}</p>
        <h1><span>{t["h1a"]}</span> <span class="mute">{t["h1b"]}</span></h1>
        <p class="intro">{e(t["intro"])}</p>
      </div>
      <ul class="fan">
{fan}
      </ul>
    </section>

    <section class="index" id="projets" aria-labelledby="idx-t">
      <h2 id="idx-t" class="k">{t["index_titre"]}</h2>
      <div class="thead" aria-hidden="true"><span>{t["cols"][0]}</span><span>{t["cols"][1]}</span><span>{t["cols"][2]}</span><span>{t["cols"][3]}</span></div>
      <ol class="rows">
{chr(10).join(rows)}
      </ol>
      <img class="peek" alt="" aria-hidden="true">
    </section>

{chr(10).join(chaps)}

    <section class="contact" id="contact">
      <p class="k">{t["contact_k"]}</p>
      <h2>{t["contact_h"]}</h2>
      <p>{t["contact_p"]}</p>
      <a class="mail" href="mailto:{CONTACT}">{CONTACT}<span aria-hidden="true"> →</span></a>
    </section>
  </main>

  <footer class="foot">
    <span>© <span data-annee>2026</span> Idée Studio</span>
    <span>{t["bas"]}</span>
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
