"""Build crawlable static language pages. No packages or server required.

The English body is in src/portfolio.html; translations are in src/translations.json.
By default, keep the currently configured host. --domain prepares a custom-domain
release locally, including CNAME. It does not change DNS, commit, or deploy.
"""

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES = {"fa": "fa_IR", "en": "en_US", "de": "de_DE"}
NAMES = {"fa": "فارسی", "en": "English", "de": "Deutsch"}
META = {
    "fa": {
        "title": "حامد ثنائی | مهندس نرم‌افزار و توسعه‌دهنده دات‌نت",
        "description": "پرتفولیوی حامد ثنائی، مهندس نرم‌افزار و توسعه‌دهنده فول‌استک دات‌نت؛ سوابق کاری، پروژه‌ها و مهارت‌ها در بک‌اند، پایگاه داده، شبکه، زیرساخت و DevOps.",
        "name": "حامد ثنائی",
        "job": "مهندس نرم‌افزار و توسعه‌دهنده فول‌استک دات‌نت",
        "contacts": "راه‌های ارتباطی", "languages": "انتخاب زبان", "skip": "رفتن به محتوای اصلی",
    },
    "en": {
        "title": "Hamed Sanaei | Software Engineer",
        "description": "Hamed Sanaei — Software Engineer and Full-Stack .NET Developer with experience in backend systems, databases, infrastructure, networking, DevOps and enterprise search.",
        "name": "Hamed Sanaei", "job": "Software Engineer and Full-Stack .NET Developer",
        "contacts": "Contact links", "languages": "Choose language", "skip": "Skip to content",
    },
    "de": {
        "title": "Hamed Sanaei | Softwareentwickler",
        "description": "Portfolio von Hamed Sanaei: Softwareentwickler und Full-Stack-.NET-Entwickler mit Erfahrung in Backend-Systemen, Datenbanken, Infrastruktur, Netzwerken und DevOps.",
        "name": "Hamed Sanaei", "job": "Softwareentwickler und Full-Stack-.NET-Entwickler",
        "contacts": "Kontaktlinks", "languages": "Sprache wählen", "skip": "Zum Hauptinhalt",
    },
}


PROJECT_LABELS = {
    "fa": {"source": "کد در گیت‌هاب", "site": "وب‌سایت", "bot": "ربات تلگرام"},
    "en": {"source": "Source on GitHub", "site": "Website", "bot": "Telegram bot"},
    "de": {"source": "Quellcode auf GitHub", "site": "Website", "bot": "Telegram-Bot"},
}


def render_projects(language):
    projects = json.loads((ROOT / "src/projects.json").read_text(encoding="utf-8"))
    labels = PROJECT_LABELS[language]
    esc = html.escape

    def links(project):
        result = f'<div class="project-links"><a href="{esc(project["repository"])}" target="_blank" rel="noopener">{labels["source"]}</a>'
        if project.get("live"):
            kind = labels[project.get("liveType", "site")]
            result += f'<a href="{esc(project["live"])}" target="_blank" rel="noopener">{kind} · <bdi dir="ltr">{esc(project["liveLabel"])}</bdi></a>'
        return result + '</div>'

    result = '<div class="projects">\n'
    for project in projects["featured"]:
        result += f'''<article class="project">
  <div><h3><bdi dir="auto">{esc(project["name"])}</bdi></h3>
    <p>{esc(project["description"][language])}</p>
    {links(project)}
  </div>
  <span dir="ltr">{esc(project["technologies"])}</span>
</article>\n'''
    return result + '</div>'


def render_body(language, translations):
    body = (ROOT / "src/portfolio.html").read_text(encoding="utf-8")

    def translate(match):
        text = match.group(0)
        key = " ".join(text.split())
        if not key or language == "en":
            return text
        if key not in translations:
            raise ValueError(f"Missing {language} translation: {key}")
        return text.replace(text.strip(), translations[key][language])

    body = re.sub(r"(?<=>)[^<]+(?=<)", translate, body)
    body = body.replace('<!-- PROJECTS -->', render_projects(language))
    body = re.sub(r'(href|src)="(assets/[^\"]+)"', r'\1="/\2"', body)
    body = body.replace('<main>', '<main id="main-content">')
    body = body.replace('aria-label="Contact links"', f'aria-label="{META[language]["contacts"]}"')
    body = body.replace('alt="Hamed Sanaei"', f'alt="{META[language]["name"]}"')
    navigation = f'<nav class="language-switcher" aria-label="{META[language]["languages"]}">\n'
    for lang, name in NAMES.items():
        current = ' aria-current="page"' if lang == language else ""
        navigation += f'      <a href="/{lang}/" lang="{lang}" hreflang="{lang}"{current}>{name}</a>\n'
    navigation += '    </nav>'
    body = body.replace('<div class="page">', f'<a class="skip-link" href="#main-content">{META[language]["skip"]}</a>\n  <div class="page">\n    {navigation}', 1)
    # Isolate left-to-right technical names, dates and addresses in the RTL page.
    if language == "fa":
        body = body.replace('<div class="when">', '<div class="when" dir="ltr">')
        body = re.sub(r'(<div><span>[^<]+</span><strong)(>)', r'\1 dir="ltr"\2', body)
        body = body.replace('<span>ASP.NET', '<span dir="ltr">ASP.NET')
        body = body.replace('<span>.NET', '<span dir="ltr">.NET')
        body = body.replace('<span>Docker', '<span dir="ltr">Docker')
        body = body.replace('>hamedsan76@gmail.com</a>', ' dir="ltr">hamedsan76@gmail.com</a>')
    return body


def render_page(language, base, translations):
    meta = META[language]
    url = f"{base}/{language}/"
    esc = html.escape
    alternates = "\n".join(f'  <link rel="alternate" hreflang="{lang}" href="{base}/{lang}/">' for lang in LOCALES)
    og_alternates = "\n".join(f'  <meta property="og:locale:alternate" content="{locale}">' for lang, locale in LOCALES.items() if lang != language)
    person = {
        "@context": "https://schema.org", "@type": "Person", "@id": f"{base}/#person",
        "name": meta["name"], "alternateName": "Hamed Sanaei" if language == "fa" else "حامد ثنائی",
        "url": url, "image": f"{base}/assets/profile.png", "email": "mailto:hamedsan76@gmail.com",
        "jobTitle": meta["job"], "sameAs": ["https://github.com/HamedSanaei", "https://www.linkedin.com/in/hamedsanaei/", "https://t.me/Hamed_Sanaei", "https://x.com/hamedsan"],
    }
    return f'''<!DOCTYPE html>
<html lang="{language}" dir="{"rtl" if language == "fa" else "ltr"}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(meta["title"])}</title>
  <meta name="description" content="{esc(meta["description"])}">
  <meta name="author" content="Hamed Sanaei">
  <link rel="canonical" href="{url}">
{alternates}
  <link rel="alternate" hreflang="x-default" href="{base}/fa/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(meta["title"])}">
  <meta property="og:description" content="{esc(meta["description"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="{esc(meta["name"])}">
  <meta property="og:locale" content="{LOCALES[language]}">
{og_alternates}
  <meta property="og:image" content="{base}/assets/portfolio-preview.png">
  <meta property="og:image:secure_url" content="{base}/assets/portfolio-preview.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="627">
  <meta property="og:image:alt" content="{esc(meta["title"])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(meta["title"])}">
  <meta name="twitter:description" content="{esc(meta["description"])}">
  <meta name="twitter:image" content="{base}/assets/portfolio-preview.png">
  <meta name="twitter:image:alt" content="{esc(meta["title"])}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&amp;family=Vazirmatn:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/style.css">
  <script type="application/ld+json">
{json.dumps(person, ensure_ascii=False, indent=2)}
  </script>
</head>
{render_body(language, translations)}
</html>
'''


def build(domain=None):
    if domain and (not re.fullmatch(r"[a-z0-9]+(?:[.-][a-z0-9]+)*\.[a-z]{2,}", domain) or len(domain) > 253):
        raise ValueError("Pass a hostname only, for example hamedsanaei.ir")
    cname = ROOT / "CNAME"
    host = domain or (cname.read_text(encoding="utf-8").strip() if cname.exists() else "hamedsanaei.github.io")
    base = f"https://{host}"
    translations = json.loads((ROOT / "src/translations.json").read_text(encoding="utf-8"))
    # Render everything before writing so incomplete translations cannot leave half a build.
    pages = {lang: render_page(lang, base, translations) for lang in LOCALES}
    for lang, content in pages.items():
        (ROOT / lang).mkdir(exist_ok=True)
        (ROOT / lang / "index.html").write_text(content, encoding="utf-8")
    (ROOT / "index.html").write_text(f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{META["fa"]["title"]}</title>
  <link rel="canonical" href="{base}/fa/">
  <meta http-equiv="refresh" content="0; url=/fa/">
</head>
<body>
  <p>در حال انتقال به <a href="/fa/">پرتفولیوی فارسی حامد ثنائی</a>…</p>
  <nav aria-label="انتخاب زبان"><a href="/en/" lang="en">English</a> · <a href="/de/" lang="de">Deutsch</a></nav>
</body>
</html>
''', encoding="utf-8")
    urls = "\n".join(f"  <url><loc>{base}/{lang}/</loc></url>" for lang in LOCALES)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    if domain:
        cname.write_text(domain + "\n", encoding="utf-8")
    print(f"Built /fa/, /en/, /de/ with Persian default on {base}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", help="Prepare a custom-domain release locally; does not deploy")
    build(parser.parse_args().domain)
