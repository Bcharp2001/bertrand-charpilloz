"""Génère les pages /chansons/<slug>/ des quatre chansons phares.

Usage : python3 scripts/build_songs.py
Paroles : chansons/_paroles/<slug>.txt (extraites avec scripts/extract_paroles.py).
"""
import html, json, os

SITE = "https://www.bertrandcharpilloz.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SONGS = [
    {
        "slug": "sunset-boulevard",
        "title": "Sunset Boulevard",
        "num": "01",
        "lead": "« Sunset Boulevard » est la chanson qui résume le mieux Bertrand Charpilloz : face à la force des éléments, relativiser ses chagrins d'amour et choisir la lumière.",
        "story": [
            "Sur le boulevard qui file vers le Pacifique, le narrateur regarde le soleil se coucher sur l'océan. Devant ce spectacle, ses déceptions amoureuses reprennent leur juste place.",
            "La chanson défend un état d'esprit qui refuse le chaos : pensée positive, lâcher-prise, acceptation et poésie. « Je préfère l'amour au désespoir, vivre au grand jour, pas dans le noir. »",
            "Musicalement, elle part d'un parlé-chanté intimiste en mi mineur et s'ouvre sur un refrain majeur, lumineux et fédérateur, à 100 BPM. C'est le titre le plus évident pour un single ou une synchronisation.",
        ],
        "facts": [("Tempo", "100 BPM"), ("Tonalité", "Mi mineur, refrain en majeur"), ("Thèmes", "Lâcher-prise, amour, philosophie de vie"), ("Tableau du répertoire", "II. Géographies intimes & escales")],
        "tempo": 100,
    },
    {
        "slug": "sur-le-creux-de-ma-main",
        "title": "Sur le creux de ma main",
        "num": "02",
        "lead": "« Sur le creux de ma main » est une méditation sereine sur la finitude, écrite par un homme de 60 ans qui regarde tomber les feuilles et fait la paix avec le temps qui reste.",
        "story": [
            "Les feuilles qui tombent dans la main sont « des lettres sans adresse, un alphabet de fin ». Le narrateur sait qu'il ne verra peut-être pas le printemps prochain, et il le dit sans peur.",
            "Bertrand l'a écrite et composée dans l'état d'esprit d'un homme accompli, quoi qu'il arrive. La chanson ne pleure pas, elle remercie : « Dis à la vigne, dis au vent, que j'ai essayé d'être vivant. »",
            "C'est de ce texte qu'est tirée la devise du récital : « J'ai vécu d'accords mineurs et d'aurores ». Une ballade piano-voix à 76 BPM, avec un pont presque parlé.",
        ],
        "facts": [("Tempo", "76 BPM"), ("Thèmes", "Finitude, gratitude, temps qui passe"), ("Tableau du répertoire", "III. Résilience, temps & finitude")],
        "tempo": 76,
    },
    {
        "slug": "le-fil-rouge",
        "title": "Le Fil Rouge",
        "num": "03",
        "lead": "« Le Fil Rouge » est la chanson autobiographique de Bertrand Charpilloz : son AVC du 18 mars 1997, le coma, puis la longue reconquête, racontés en jeux de mots à double sens.",
        "story": [
            "Le 18 mars 1997, lors d'un déplacement professionnel à Aix-en-Provence, Bertrand est victime d'un AVC hémorragique. Il sort du coma le 1er avril, hémiplégique et aphasique.",
            "Chaque vers a deux sens. « Mars jour soixante-dix-sept » désigne le 18 mars, 77e jour de l'année. « Prisonnier en exil » dit l'hôpital loin de chez lui. « Moitié de moi d'avril » s'entend « moitié du mois d'avril » et dit aussi l'hémiplégie, la moitié du corps paralysée. « Le regard immobile » évoque la paralysie, « le mobile » joue sur ses deux sens, et le « poison d'avril » détourne le poisson d'avril du réveil.",
            "La chanson suit ensuite le temps : mars 2007, dix ans plus tard, puis mars 2024, « une vie à me battre pour voir ma fille grandir ». C'est la colonne vertébrale émotionnelle du répertoire. Bertrand raconte cette reconstruction dans son livre « Mes liaisons cérébrales » (2013).",
        ],
        "facts": [("Tempo", "78 BPM"), ("Tonalité", "Mi mineur"), ("Thèmes", "AVC, résilience, temps"), ("Tableau du répertoire", "III. Résilience, temps & finitude")],
        "tempo": 78,
    },
    {
        "slug": "mon-altesse-ego",
        "title": "Mon Altesse Ego",
        "num": "04",
        "lead": "« Mon Altesse Ego » est un inventaire amoureux, espiègle et sensuel, écrit en hommage à la pianiste Marie-Françoise Coelho. Elle a donné son nom au récital.",
        "story": [
            "La chanson est une longue liste de petits noms : « Ma toison d'or », « Mon sucre d'orge », « Ma citadelle », « Mon chiffre zéro zéro sept ». Le refrain la ramène à une envie simple : « De t'avoir sous ma couette, un bout de vie… ce serait chouette. »",
            "C'est un festival de jeux de mots dans l'esprit de Gainsbourg : « Ma pièce d'Éros » détourne la pièce d'euro, « Mon histoire d'O » et « Mon Altesse Ego » jouent sur les sons.",
            "Un swing cabaret-blues à 115 BPM, en parlé-chanté pince-sans-rire. « L'Altesse Ego » est le nom du récital piano-voix ; « Mon Altesse Ego » est la chanson.",
        ],
        "facts": [("Tempo", "115 BPM"), ("Thèmes", "Amour, désir, jeux de mots"), ("Tableau du répertoire", "I. Figures féminines, prénoms & muses")],
        "tempo": 115,
    },
]

CSS = """:root{--bg:#0a0908;--card:#141210;--ivory:#f4efe6;--muted:#b8b2a6;--red:#c81d25;--gold:#d49a56;--border:rgba(244,239,230,0.12)}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--ivory);font-family:'Montserrat',sans-serif;font-weight:300;line-height:1.7;-webkit-text-size-adjust:100%}
h1,h2,.serif{font-family:'Cormorant Garamond',serif;line-height:1.2;font-weight:400}
a{color:var(--gold)}
a:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
nav{border-bottom:1px solid var(--border);padding:1rem 5%;display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}
.nav-logo{font-family:'Cormorant Garamond',serif;font-size:1.3rem;letter-spacing:3px;text-transform:uppercase;color:var(--ivory);text-decoration:none}
.nav-logo span{color:var(--red);font-weight:bold}
.nav-links a{color:var(--muted);text-decoration:none;font-size:0.75rem;letter-spacing:2px;text-transform:uppercase;margin-left:1.2rem}
.nav-links a:hover{color:var(--ivory)}
main{max-width:820px;margin:0 auto;padding:2.5rem 16px 4rem}
.crumbs{font-size:0.75rem;letter-spacing:1px;color:var(--muted);margin-bottom:2rem}
.crumbs a{color:var(--muted)}
.tag{font-size:0.75rem;letter-spacing:4px;text-transform:uppercase;color:var(--gold);display:block;margin-bottom:0.6rem}
h1{font-size:clamp(2.2rem,6vw,3.4rem);margin-bottom:1.2rem}
.lead{font-size:1.1rem;color:var(--ivory);margin-bottom:2rem}
h2{font-size:1.8rem;margin:2.8rem 0 1rem;color:var(--ivory)}
p{color:var(--muted);margin-bottom:1rem}
.players{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1.5rem 0 0.6rem}
.player{background:var(--card);border:1px solid var(--border);padding:1rem}
.player p{font-size:0.75rem;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:0.6rem}
audio{width:100%}
.note{font-size:0.8rem}
.lyrics{white-space:pre-line;font-family:'Cormorant Garamond',serif;font-size:1.2rem;line-height:1.6;color:var(--ivory);background:rgba(0,0,0,0.45);border-left:2px solid var(--gold);padding:1.4rem 1.6rem}
table{width:100%;border-collapse:collapse;margin-top:0.5rem}
th,td{text-align:left;padding:0.6rem 0;border-bottom:1px solid var(--border);vertical-align:top;font-size:0.9rem}
th{color:var(--gold);font-weight:400;width:40%;padding-right:1rem}
td{color:var(--ivory)}
.others{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:0.6rem}
.others a{display:block;border:1px solid var(--border);padding:0.8rem 1rem;text-decoration:none;color:var(--ivory)}
.others a:hover{border-color:var(--gold)}
.cta{display:inline-block;margin-top:1rem;padding:0.9rem 1.6rem;background:var(--red);color:var(--ivory);text-decoration:none;font-size:0.8rem;letter-spacing:2px;text-transform:uppercase}
footer{border-top:1px solid var(--border);padding:2rem 16px;text-align:center;font-size:0.8rem;color:var(--muted)}
footer a{color:var(--muted)}
@media (max-width:640px){.players,.others{grid-template-columns:1fr}.nav-links a{margin-left:0.8rem}}"""


def e(s):
    return html.escape(s, quote=True)


def page(song):
    slug, title = song["slug"], song["title"]
    url = f"{SITE}/chansons/{slug}/"
    lyrics = open(os.path.join(ROOT, "chansons", "_paroles", f"{slug}.txt"), encoding="utf-8").read().strip()
    desc = song["lead"]
    if len(desc) > 158:
        desc = desc[:155].rsplit(" ", 1)[0] + "…"
    audio_arr = f"/bertrand-charpilloz-{slug}-radio-edit.mp3"
    audio_pv = f"/bertrand-charpilloz-{slug}-piano-voix.mp3"
    facts = [("Paroles et musique", "Bertrand Charpilloz"), ("Interprète", "Bertrand Charpilloz")] + song["facts"] + [("Dépôt", "SUISA"), ("Langue", "Français")]
    others = [s for s in SONGS if s["slug"] != slug]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": url,
                "url": url,
                "name": f"{title} — Bertrand Charpilloz, paroles et histoire",
                "description": song["lead"],
                "inLanguage": "fr",
                "isPartOf": {"@id": f"{SITE}/#site"},
                "about": {"@id": f"{url}#oeuvre"},
                "breadcrumb": {"@id": f"{url}#fil"},
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#fil",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Bertrand Charpilloz", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Répertoire", "item": f"{SITE}/#repertoire"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": url},
                ],
            },
            {
                "@type": "MusicComposition",
                "@id": f"{url}#oeuvre",
                "name": title,
                "url": url,
                "inLanguage": "fr",
                "composer": {"@id": f"{SITE}/#bertrand"},
                "lyricist": {"@id": f"{SITE}/#bertrand"},
                "description": song["lead"],
                "isPartOf": {"@id": f"{SITE}/#repertoire"},
                "lyrics": {"@type": "CreativeWork", "inLanguage": "fr", "text": lyrics},
                "recordedAs": [
                    {"@type": "MusicRecording", "name": f"{title} (maquette arrangée)", "byArtist": {"@id": f"{SITE}/#bertrand"}, "audio": {"@type": "AudioObject", "contentUrl": SITE + audio_arr, "encodingFormat": "audio/mpeg"}},
                    {"@type": "MusicRecording", "name": f"{title} (maquette piano-voix)", "byArtist": {"@id": f"{SITE}/#bertrand"}, "audio": {"@type": "AudioObject", "contentUrl": SITE + audio_pv, "encodingFormat": "audio/mpeg"}},
                ],
            },
        ],
    }
    story = "\n".join(f"    <p>{e(p)}</p>" for p in song["story"])
    rows = "\n".join(f"      <tr><th scope=\"row\">{e(k)}</th><td>{e(v)}</td></tr>" for k, v in facts)
    links = "\n".join(f"      <li><a href=\"/chansons/{o['slug']}/\">{e(o['title'])}</a></li>" for o in others)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)} — Bertrand Charpilloz, paroles et histoire</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="Bertrand Charpilloz">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0a0908">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="music.song">
<meta property="og:site_name" content="Bertrand Charpilloz">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)} — Bertrand Charpilloz">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}/img/bertrand-charpilloz-og.jpg">
<meta property="og:audio" content="{SITE}{audio_pv}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Montserrat:wght@300;400&display=swap" rel="stylesheet">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
<style>
{CSS}
</style>
</head>
<body>
<nav aria-label="Navigation principale">
  <a class="nav-logo" href="/">Bertrand <span>Charpilloz</span></a>
  <div class="nav-links"><a href="/#ecoute">Écoute</a><a href="/#repertoire">Répertoire</a><a href="/#contact">Contact</a></div>
</nav>
<main>
  <p class="crumbs"><a href="/">Bertrand Charpilloz</a> › <a href="/#repertoire">Répertoire</a> › {e(title)}</p>
  <span class="tag">Chanson {song['num']} · Récital L'Altesse Ego</span>
  <h1>{e(title)}</h1>
  <p class="lead">{e(song['lead'])}</p>

  <div class="players">
    <div class="player"><p>Maquette arrangée</p><audio controls preload="none" src="{audio_arr}" aria-label="Écouter {e(title)}, maquette arrangée — Bertrand Charpilloz"></audio></div>
    <div class="player"><p>Maquette piano-voix</p><audio controls preload="none" src="{audio_pv}" aria-label="Écouter {e(title)}, maquette piano-voix — Bertrand Charpilloz"></audio></div>
  </div>
  <p class="note">Maquettes d'arrangement, avant l'enregistrement studio du duo avec Marie-Françoise Coelho.</p>

  <section>
    <h2>L'histoire de la chanson</h2>
{story}
  </section>

  <section>
    <h2>Les paroles</h2>
    <div class="lyrics">{e(lyrics)}</div>
    <p class="note">Paroles et musique : Bertrand Charpilloz. Tous droits réservés, œuvre déposée à la SUISA.</p>
  </section>

  <section>
    <h2>Fiche de l'œuvre</h2>
    <table>
{rows}
    </table>
  </section>

  <section>
    <h2>Les autres chansons phares</h2>
    <ul class="others">
{links}
      <li><a href="/#repertoire">Les 21 chansons du répertoire</a></li>
    </ul>
    <a class="cta" href="mailto:contact@bertrandcharpilloz.com?subject={e(title).replace(' ', '%20')}%20%E2%80%94%20demande%20professionnelle">Contact professionnel</a>
  </section>
</main>
<footer>
  <p>© 2026 Bertrand Charpilloz — <a href="/">Retour au dossier de présentation</a> · <a href="mailto:contact@bertrandcharpilloz.com">contact@bertrandcharpilloz.com</a></p>
</footer>
</body>
</html>
"""


if __name__ == "__main__":
    for s in SONGS:
        d = os.path.join(ROOT, "chansons", s["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(s))
        print("ok", s["slug"])
