"""Génère /en/, /de/ et /ja/ à partir de la page française (index.html).
Les chansons, extraits de paroles et citations restent en français.
Usage : python3 scripts/build_i18n.py   (depuis la racine du dépôt)
"""
import json, re, copy
from bs4 import BeautifulSoup, Comment

BASE = "https://www.bertrandcharpilloz.com"
LANGS = [("fr", "/", "FR"), ("en", "/en/", "EN"), ("de", "/de/", "DE"), ("ja", "/ja/", "日本語")]

def hreflang_block():
    out = [f'<link rel="alternate" hreflang="{l}" href="{BASE}{p}">' for l, p, _ in LANGS]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/">')
    return "\n".join(out)

def switcher(active):
    links = []
    for l, p, label in LANGS:
        cur = ' aria-current="page"' if l == active else ""
        links.append(f'<a href="{p}" lang="{l}" hreflang="{l}"{cur}>{label}</a>')
    return '<span class="lang-switch">' + "".join(links) + "</span>"

CSS = (".lang-switch{display:inline-flex;gap:0.7rem;margin-left:1.6rem;padding-left:1rem;border-left:1px solid var(--border)}"
       "\n.nav-links .lang-switch a{margin-left:0;font-size:0.7rem;letter-spacing:1px}"
       "\n.nav-links .lang-switch a[aria-current]{color:var(--gold)}")
CSS_MOBILE = "    .lang-switch{margin-left:0;padding-left:0;border-left:none}"

def add_common(html, active):
    """hreflang + sélecteur de langue (idempotent)."""
    html = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', "", html)
    html = html.replace('<link rel="canonical"', hreflang_block() + '\n<link rel="canonical"', 1)
    html = re.sub(r'<span class="lang-switch">.*?</span>', "", html, flags=re.S)
    html, n = re.subn(r'(<div class="nav-links">.*?)(\s*</div>)', lambda mm: mm.group(1) + "\n        " + switcher(active) + mm.group(2), html, count=1, flags=re.S)
    assert n == 1, "nav-links introuvable"
    if ".lang-switch{" not in html:
        html = html.replace("/* PRESSE */", CSS + "\n\n/* PRESSE */", 1)
        html = html.replace("    .press-grid{grid-template-columns:1fr}", "    .press-grid{grid-template-columns:1fr}\n" + CSS_MOBILE, 1)
    return html

def translate(fr_html, cfg):
    m, t, js = cfg["meta"], cfg["t"], cfg.get("js", {})
    lang, path = m["lang"], m["path"]
    url = BASE + path
    h = fr_html
    def rep(a, b, count=1):
        nonlocal h
        assert a in h, a[:60]
        h = h.replace(a, b, count)
    # --- head
    rep('<html lang="fr">', f'<html lang="{lang}">')
    h = re.sub(r"<title>.*?</title>", lambda _: f"<title>{m['title']}</title>", h, count=1, flags=re.S)
    def meta(attr, key, val):
        nonlocal h
        pat = re.compile(r'(<meta %s="%s" content=")[^"]*(">)' % (attr, re.escape(key)))
        assert pat.search(h), key
        h = pat.sub(lambda mm: mm.group(1) + val.replace('"', "&quot;") + mm.group(2), h, count=1)
    meta("name", "description", m["description"])
    meta("property", "og:url", url)
    meta("property", "og:locale", m["locale"])
    meta("property", "og:title", m["og_title"])
    meta("property", "og:description", m["og_desc"])
    meta("property", "og:image:alt", m["og_alt"])
    meta("name", "twitter:title", m["og_title"])
    meta("name", "twitter:description", m["og_desc"])
    h = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{url}">', h, count=1)
    # chemins absolus (la page vit dans un sous-dossier)
    h = h.replace('"img/', '"/img/').replace(", img/", ", /img/").replace('src="bertrand-charpilloz-', 'src="/bertrand-charpilloz-')
    # --- JSON-LD
    mm = re.search(r'(<script type="application/ld\+json">\n)(.*?)(\n</script>)', h, re.S)
    ld = json.loads(mm.group(2))
    graph = []
    for n in ld["@graph"]:
        if n.get("@type") == "FAQPage":
            continue
        if n.get("@type") == "ProfilePage":
            n = dict(n, **{"@id": url + "#page", "url": url, "name": m["page_name"], "inLanguage": lang})
        graph.append(n)
    ld["@graph"] = graph
    h = h[:mm.start(2)] + json.dumps(ld, ensure_ascii=False, indent=2) + h[mm.end(2):]
    # --- scripts : libellés du bloc contact
    for a, b in js.items():
        rep(a, b)
    # --- corps : textes visibles
    head, sep, rest = h.partition("<body")
    soup = BeautifulSoup(sep + rest, "html.parser")
    missing = set(t)
    for node in soup.find_all(string=True):
        if isinstance(node, Comment) or node.parent.name in ("script", "style"):
            continue
        s = str(node); key = s.strip()
        if key in t:
            missing.discard(key)
            val = t[key]
            lead = s[: len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
            if lang == "ja":
                lead = trail = ""
            elif val[:1] in ",.);:":
                lead = ""
            node.replace_with(lead + val + trail)
    for tag in soup.find_all("img"):
        if "Affiche du récital" in tag.get("alt", ""): tag["alt"] = m["alt_poster"]
        elif "Portrait officiel" in tag.get("alt", ""): tag["alt"] = m["alt_portrait"]
    soup.find("nav")["aria-label"] = m["nav_label"]
    for a in soup.find_all("audio"):
        lab = a.get("aria-label", "")
        mt = re.match(r"Écouter (.+), version (Radio Edit|piano-voix) — Bertrand Charpilloz", lab)
        if mt:
            ver = m["v_radio"] if mt.group(2) == "Radio Edit" else m["v_piano"]
            a["aria-label"] = m["aria_listen"].format(title=mt.group(1), version=ver)
    unused = sorted(k for k in missing if k not in ("L'essentiel sur",))
    return head + str(soup), unused

if __name__ == "__main__":
    fr = open("index.html", encoding="utf-8").read()
    fr = add_common(fr, "fr")
    open("index.html", "w", encoding="utf-8").write(fr)
    import os
    for lang, path, _ in LANGS[1:]:
        cfg = json.load(open(f"i18n/{lang}.json", encoding="utf-8"))
        html, unused = translate(fr, cfg)
        html = add_common(html, lang)
        os.makedirs(lang, exist_ok=True)
        open(f"{lang}/index.html", "w", encoding="utf-8").write(html)
        print(lang, "ok", "| clés non utilisées :", unused)
