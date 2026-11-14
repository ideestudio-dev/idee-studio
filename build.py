#!/usr/bin/env python3
"""Génère index.html (français), en/index.html (anglais) et sitemap.xml à partir d'une seule source.

Ajouter ou modifier un projet : éditer PROJETS, puis lancer `python3 build.py`.
Images : assets/img/ (captures ordinateur et téléphone de chaque projet).
"""
from pathlib import Path
import html, json

ROOT = Path(__file__).parent
SITE = "https://idee.studio"
GA_ID = "G-SGMPTLN3CR"  # identifiant Google Analytics (G-XXXX) de la propriété idee.studio
CONTACT = "contact@idee.studio"
e = html.escape

# tile = fond de la vignette (couleur du produit) ; dark = vignette sombre ; large = pleine largeur
PROJETS = [
    dict(key="florvil", nom="Habitations Florvil", url="https://www.habitationsflorvil.com", annee="2026", large=True,
         desktop="florvil-desktop.jpg", mobile="florvil-mobile.jpg", tile="#e9e4dc", dark=False,
         fr=dict(type="Client · Site web bilingue", texte="Le site d'un entrepreneur en construction et rénovation résidentielles du Grand Montréal : design, contenus, articles de blogue et référencement, en français et en anglais.", etat=""),
         en=dict(type="Client · Bilingual website", texte="The website of a residential construction and renovation contractor in Greater Montréal: design, content, blog articles and search optimization, in French and English.", etat="")),
    dict(key="depot", nom="Le Dépôt", url="https://ledepot.co", annee="2026",
         desktop="depot-galerie.jpg", mobile="depot-mobile.jpg", tile="#0d0d0c", dark=True,
         fr=dict(type="Plateforme web", texte="Le workspace des professionnels de la communication en Afrique francophone : portfolio, planification, facturation et une bibliothèque de 154 campagnes.", etat=""),
         en=dict(type="Web platform", texte="The workspace for communication professionals in French-speaking Africa: portfolio, planning, invoicing and a library of 154 campaigns.", etat="")),
    dict(key="souper", nom="Souper Club", url="https://souperclub.app", annee="2026",
         desktop="", mobile="souper-mobile.jpg", tile="#efe9f5", dark=False,
         fr=dict(type="Application mobile · Site web", texte="Une application qui réunit deux couples autour d'une table au restaurant, au Canada, en français et en anglais.", etat=""),
         en=dict(type="Mobile app · Website", texte="An app that brings two couples together around a restaurant table, across Canada, in French and English.", etat="")),
    dict(key="ronde", nom="Ronde Sécurité", url="https://rondesecurite.ca", annee="2026", large=True,
         desktop="ronde-desktop.jpg", mobile="ronde-mobile.jpg", tile="#e9efff", dark=False,
         fr=dict(type="Application web et mobile · SaaS", texte="La ronde de sécurité des véhicules lourds, faite sur téléphone. Les gestionnaires de flotte reçoivent des rapports PDF conformes à la SAAQ et des alertes en temps réel.", etat=""),
         en=dict(type="Web and mobile app · SaaS", texte="Heavy-vehicle pre-trip inspections on a phone, with SAAQ-compliant PDF reports and real-time alerts for fleet managers.", etat="")),
    dict(key="bercail", nom="Bercail", url="https://bercail.idee.studio", annee="2026",
         desktop="", mobile="bercail-mobile.jpg", tile="#e5e9df", dark=False,
         fr=dict(type="Application web", texte="L'application de la maison, pour gérer en famille le budget, les repas, les tâches et l'agenda.", etat="Sur invitation"),
         en=dict(type="Web app", texte="The home app: the family's budget, meals, chores and calendar, all in one place.", etat="By invitation")),
    dict(key="comptoir", nom="Comptoir+", url="https://comptoir.idee.studio", annee="2026",
         desktop="", mobile="comptoir-mobile.jpg", tile="#ebe5d9", dark=False,
         fr=dict(type="Application mobile · Point de vente", texte="La prise de commande et la caisse des bars et maquis, du service en salle jusqu'au paiement en espèces ou par Mobile Money.", etat="Démo en ligne"),
         en=dict(type="Mobile app · Point of sale", texte="Ordering and checkout for bars and maquis, from table service to payment in cash or Mobile Money.", etat="Live demo")),
    dict(key="cinelens", nom="CinéLens", url="https://cinelens.idee.studio", annee="2026", large=True,
         desktop="cinelens-desktop.jpg", mobile="cinelens-mobile.jpg", tile="#e9ecf1", dark=False,
         fr=dict(type="Application web · Intelligence artificielle", texte="Retrouver un film à partir d'une capture d'écran : son titre, son réalisateur, sa distribution et où le regarder.", etat="Démo en ligne"),
         en=dict(type="Web app · Artificial intelligence", texte="Identify a film from a single screenshot: title, director, cast and where to watch it.", etat="Live demo")),
    dict(key="elan", nom="Élan", url="https://elan.idee.studio", annee="2026", large=True,
         desktop="elan-desktop.jpg", mobile="elan-mobile.jpg", tile="#0c0e0d", dark=True,
         fr=dict(type="Application mobile · Sport et santé", texte="Du sport pour les parents qui manquent de temps. Chaque matin, une séance de 10 à 30 minutes, ajustée selon la nuit, l'énergie et le temps disponible.", etat="Démo en ligne"),
         en=dict(type="Mobile app · Fitness", texte="Fitness for parents with no time: every morning, a 10 to 30 minute workout adjusted to last night's sleep, energy and the time available.", etat="Live demo")),
    dict(key="jama", nom="Jama", url="https://jama.idee.studio", annee="2026", large=True,
         desktop="jama-desktop.jpg", mobile="jama-mobile.jpg", tile="#eef3fa", dark=False,
         fr=dict(type="Application web · Clubs de sport", texte="Pour gérer un petit club de quartier en Afrique : matchs, présences, scores, cotisations par Mobile Money et dépenses. Le message pour le groupe WhatsApp est prêt à envoyer.", etat="Démo en ligne"),
         en=dict(type="Web app · Sports clubs", texte="Management for small neighbourhood sports clubs in Africa: matches, attendance, scores, Mobile Money dues and expenses, with the message ready for the WhatsApp group.", etat="Live demo")),
]

T = {
    "fr": dict(
        lang="fr-CA", path="/", other="/en/", self_label="FR", other_label="EN",
        title="Idée Studio · Sites web et applications, studio créatif au Québec",
        desc="Idée Studio conçoit et développe des sites web, des applications web et mobiles et des identités de marque, de l'idée jusqu'au lancement.",
        skip="Aller au contenu", nav=("Services", "Projets", "Studio", "Contact"),
        eyebrow="Studio créatif",
        h1="On transforme vos idées en produits numériques.",
        lead="Nous concevons et développons des sites web, des applications web et mobiles et des identités de marque, jusqu'à leur mise en ligne. Des outils clairs et rapides, faits pour les gens qui s'en servent.",
        cta=("Parlons de votre projet", "Voir nos projets"),
        services_k="Services", services_h="Ce que nous faisons.",
        services=[
            ("Sites web", "Sites vitrines et sites de contenu, rapides et bien référencés. Vous pouvez les mettre à jour facilement.", ["Conception et rédaction", "Référencement (SEO)", "Statistiques et suivi"]),
            ("Applications web", "Plateformes, tableaux de bord et outils métier, avec comptes, paiements et données en temps réel.", ["SaaS et abonnements", "Espaces clients", "Automatisations"]),
            ("Applications mobiles", "Applications iPhone et Android, de la maquette jusqu'à la publication sur l'App Store et Google Play.", ["iOS et Android", "Notifications", "Publication dans les boutiques d'applications"]),
            ("Identité et design", "Logos, interfaces et systèmes visuels cohérents, du premier croquis au produit fini.", ["Identité de marque", "Design d'interface", "Prototypes"]),
        ],
        projets_k="Projets récents", projets_h="Des sites et des applications conçus, développés et lancés par le studio.",
        visiter="Voir le site",
        methode_k="Méthode", methode_h="Une façon de travailler simple.",
        methode=[
            ("Comprendre", "On part de votre métier, de vos utilisateurs et de vos objectifs avant d'écrire une ligne de code."),
            ("Concevoir", "Maquettes et prototype cliquable : on valide le parcours ensemble, écran par écran."),
            ("Développer", "Une première version utile, livrée vite, puis améliorée par petites étapes."),
            ("Lancer et faire évoluer", "On met le produit en ligne, on soigne le référencement, puis on suit les statistiques pour l'améliorer."),
        ],
        studio_k="Le studio", studio_h="Un studio indépendant qui crée aussi ses propres produits.",
        studio_p=["Nous travaillons pour des entreprises et des organismes. Nous développons aussi nos propres applications, utilisées par des transporteurs, des créatifs, des couples et des familles.",
                  "Cette double casquette change notre façon de travailler. Nous prenons chaque décision comme si le produit était le nôtre, de la conception à l'hébergement, jusqu'au suivi après le lancement."],
        contact_h="Un projet en tête ?", contact_p="Décrivez-nous votre idée en quelques lignes. Nous vous répondons rapidement, avec des questions et une première estimation.",
        contact_btn="Écrire au studio",
        bas="Studio créatif au Québec",
        vie_privee="Mesure d'audience avec Google Analytics, adresse IP anonymisée.",
    ),
    "en": dict(
        lang="en-CA", path="/en/", other="/", self_label="EN", other_label="FR",
        title="Idée Studio · Websites and apps, creative studio in Québec",
        desc="Idée Studio designs and builds websites, web and mobile apps and brand identities, from idea to launch.",
        skip="Skip to content", nav=("Services", "Work", "Studio", "Contact"),
        eyebrow="Creative studio",
        h1="We turn your ideas into digital products.",
        lead="Websites, web and mobile apps, brand identities: we design, build and launch clear, fast tools made for the people who use them.",
        cta=("Tell us about your project", "See our work"),
        services_k="Services", services_h="What we do.",
        services=[
            ("Websites", "Fast showcase and content websites, well ranked on search engines and easy to update.", ["Design and copywriting", "Search engine optimization", "Analytics"]),
            ("Web apps", "Platforms, dashboards and business tools, with accounts, payments and real-time data.", ["SaaS and subscriptions", "Client portals", "Automation"]),
            ("Mobile apps", "iPhone and Android apps, from mockups to publication on the App Store and Google Play.", ["iOS and Android", "Notifications", "Store publishing"]),
            ("Brand and design", "Logos, interfaces and consistent visual systems, from the first sketch to the finished product.", ["Brand identity", "Interface design", "Prototypes"]),
        ],
        projets_k="Recent work", projets_h="Websites and apps designed, built and launched by the studio.",
        visiter="Visit site",
        methode_k="Approach", methode_h="A simple way of working.",
        methode=[
            ("Understand", "We start from your business, your users and your goals before writing a single line of code."),
            ("Design", "Mockups and a clickable prototype: we validate the journey together, screen by screen."),
            ("Build", "A first useful version, delivered quickly, then improved in short iterations."),
            ("Launch and improve", "We put the product online, take care of search optimization, then track the analytics to keep improving it."),
        ],
        studio_k="The studio", studio_h="An independent studio that also builds its own products.",
        studio_p=["We work for businesses and organizations. We also build our own apps, used by truckers, creatives, couples and families.",
                  "Wearing both hats shapes how we work: every decision is made as if the product were ours, from design to hosting and support after launch."],
        contact_h="Have a project in mind?", contact_p="Tell us about your idea in a few lines. We'll get back to you quickly, with questions and a first estimate.",
        contact_btn="Write to the studio",
        bas="Creative studio in Québec",
        vie_privee="Audience measurement with Google Analytics, IP address anonymized.",
    ),
}


def phone(src, alt, cls=""):
    return f'<figure class="phone {cls}"><img src="/assets/img/{src}" alt="{e(alt)}" loading="lazy" width="390" height="800"></figure>'


def browser(src, alt):
    return f'<figure class="browser"><span class="bar" aria-hidden="true"></span><img src="/assets/img/{src}" alt="{e(alt)}" loading="lazy" width="1600" height="867"></figure>'


def visuel(p):
    if p["desktop"] and p["mobile"]:
        return f'<div class="comp duo">{browser(p["desktop"], p["nom"])}{phone(p["mobile"], p["nom"], "over")}</div>'
    if p["desktop"]:
        return f'<div class="comp">{browser(p["desktop"], p["nom"])}</div>'
    return f'<div class="comp single">{phone(p["mobile"], p["nom"])}</div>'


def page(lg):
    t = T[lg]
    autre = "en" if lg == "fr" else "fr"
    nav = t["nav"]

    services = "\n".join(f'''        <li class="svc">
          <span class="svc-n">{i:02d}</span>
          <h3>{e(nom)}</h3>
          <p>{e(txt)}</p>
          <ul>{"".join(f"<li>{e(x)}</li>" for x in pts)}</ul>
        </li>''' for i, (nom, txt, pts) in enumerate(t["services"], 1))

    cases = []
    for p in PROJETS:
        L = p[lg]
        etat = f'<span class="etat">{e(L["etat"])}</span>' if L["etat"] else ""
        lien_o, lien_f = (f'<a class="case-link" href="{p["url"]}" target="_blank" rel="noopener">', "</a>") if p["url"] else ('<div class="case-link">', "</div>")
        voir = f'<span class="voir">{t["visiter"]} ↗</span>' if p["url"] else ""
        cases.append(f'''        <article class="case{' wide' if p.get('large') else ''}" id="p-{p["key"]}">
          {lien_o}
            <div class="tile{' dark' if p['dark'] else ''}" style="--tile:{p["tile"]}">{visuel(p)}</div>
            <div class="cap">
              <div class="cap-top"><h3>{e(p["nom"])}</h3>{etat}<span class="yr">{p["annee"]}</span></div>
              <p class="type">{e(L["type"])}</p>
              <p class="desc">{e(L["texte"])}</p>
              {voir}
            </div>
          {lien_f}
        </article>''')

    methode = "\n".join(f'''        <li><span>{i:02d}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>'''
                        for i, (a, b) in enumerate(t["methode"], 1))
    studio_p = "".join(f"<p>{e(x)}</p>" for x in t["studio_p"])

    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Idée Studio", "url": SITE,
          "email": CONTACT, "logo": f"{SITE}/assets/icon.svg", "description": t["desc"],
          "address": {"@type": "PostalAddress", "addressRegion": "QC", "addressCountry": "CA"},
          "knowsAbout": [s[0] for s in t["services"]]}
    ga = (f'''  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}',{{anonymize_ip:true}});</script>
''' if GA_ID else "")

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
  <meta name="theme-color" content="#ffffff">
  <link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap">
  <link rel="stylesheet" href="/assets/styles.css">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{ga}</head>
<body>
  <a class="skip" href="#contenu">{t["skip"]}</a>
  <header class="top">
    <a class="brand" href="{t["path"]}">Id<span class="acc">é</span>e Studio</a>
    <nav aria-label="Navigation">
      <a class="hide-sm" href="#services">{nav[0]}</a>
      <a class="hide-sm" href="#projets">{nav[1]}</a>
      <a class="hide-sm" href="#studio">{nav[2]}</a>
      <a class="hide-sm" href="#contact">{nav[3]}</a>
      <a class="lang" href="{t["other"]}" hreflang="{autre}" lang="{autre}">{t["other_label"]}</a>
    </nav>
  </header>

  <main id="contenu">
    <section class="hero wrap">
      <p class="k">{t["eyebrow"]}</p>
      <h1>{t["h1"]}</h1>
      <p class="lead">{e(t["lead"])}</p>
      <div class="cta">
        <a class="btn" href="mailto:{CONTACT}">{t["cta"][0]}</a>
        <a class="btn ghost" href="#projets">{t["cta"][1]}</a>
      </div>
    </section>

    <section class="services wrap" id="services">
      <div class="head"><p class="k">{t["services_k"]}</p><h2>{t["services_h"]}</h2></div>
      <ol class="svc-list">
{services}
      </ol>
    </section>

    <section class="work wrap" id="projets">
      <div class="head"><p class="k">{t["projets_k"]}</p><h2>{t["projets_h"]}</h2></div>
      <div class="cases">
{chr(10).join(cases)}
      </div>
    </section>

    <section class="method wrap">
      <div class="head"><p class="k">{t["methode_k"]}</p><h2>{t["methode_h"]}</h2></div>
      <ol class="steps">
{methode}
      </ol>
    </section>

    <section class="studio wrap" id="studio">
      <p class="k">{t["studio_k"]}</p>
      <div class="studio-grid"><h2>{t["studio_h"]}</h2><div>{studio_p}</div></div>
    </section>

    <section class="contact wrap" id="contact">
      <h2>{t["contact_h"]}</h2>
      <p>{t["contact_p"]}</p>
      <a class="btn" href="mailto:{CONTACT}">{t["contact_btn"]}</a>
      <a class="mail" href="mailto:{CONTACT}">{CONTACT}</a>
    </section>
  </main>

  <footer class="foot wrap">
    <span>© <span data-annee>2026</span> Idée Studio · {t["bas"]}</span>
    <span class="vp">{t["vie_privee"]}</span>
    <a href="mailto:{CONTACT}">{CONTACT}</a>
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
