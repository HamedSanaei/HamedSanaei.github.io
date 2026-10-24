"""Check generated language pages, SEO metadata and local links."""

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("fa", "en", "de")


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.projects = []
        self.current_project = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "article" and attrs.get("class") == "project":
            self.current_project = []
            self.projects.append(self.current_project)
        if tag == "a" and self.current_project is not None:
            self.current_project.append(attrs["href"])

    def handle_endtag(self, tag):
        if tag == "article":
            self.current_project = None

    def find(self, tag, **attrs):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in attrs.items())]


def check(root=ROOT):
    cname = root / "CNAME"
    host = cname.read_text(encoding="utf-8").strip() if cname.exists() else "hamedsanaei.github.io"
    base = f"https://{host}"
    expected = {lang: f"{base}/{lang}/" for lang in LANGUAGES}
    for lang in LANGUAGES:
        text = (root / lang / "index.html").read_text(encoding="utf-8")
        page = Page(text)
        assert page.find("html", lang=lang, dir="rtl" if lang == "fa" else "ltr"), f"Incorrect lang/dir: {lang}"
        assert len(page.find("h1")) == 1, f"Expected one H1: {lang}"
        assert {tuple(links) for links in page.projects} == {
            ("https://github.com/HamedSanaei/Vendora", "https://vendorashop.ir/"),
            ("https://github.com/HamedSanaei/cloud", "https://parserver.ir/"),
            ("https://github.com/HamedSanaei/telegram-media-downloader-bot", "https://t.me/DownloadKadeBot"),
            ("https://github.com/HamedSanaei/cloud-server-seller-bot", "https://t.me/ServerHubbBot"),
        } and len(page.projects) == 4, f"Expected four projects, each with its source and live link: {lang}"
        for profile in ("https://t.me/Hamed_Sanaei", "https://x.com/hamedsan"):
            assert page.find("a", href=profile), f"Missing social profile: {lang}: {profile}"
        assert page.find("link", rel="canonical") == [{"rel": "canonical", "href": expected[lang]}], f"Canonical: {lang}"
        alternates = {a["hreflang"]: a["href"] for a in page.find("link", rel="alternate")}
        assert alternates == {**expected, "x-default": expected["fa"]}, f"Hreflang: {lang}"
        assert page.find("meta", name="description")[0]["content"], f"Description: {lang}"
        assert page.find("meta", property="og:url")[0]["content"] == expected[lang]
        assert not page.find("meta", **{"http-equiv": "refresh"}), f"Language page redirects: {lang}"
        assert "noindex" not in text and "\ufffd" not in text, f"Indexing or encoding error: {lang}"
        assert len(page.find("a", **{"aria-current": "page", "href": f"/{lang}/"})) == 1
        for target in LANGUAGES:
            assert page.find("a", href=f"/{target}/", hreflang=target), f"Missing language link: {lang} -> {target}"
        for tag, attrs in page.tags:
            for name in ("href", "src"):
                value = attrs.get(name, "")
                if not value or urlsplit(value).scheme or value.startswith("#"):
                    continue
                path = root / unquote(urlsplit(value).path).lstrip("/")
                if path.is_dir():
                    path /= "index.html"
                assert path.is_file(), f"Broken local {name}: {lang}: {value}"
        start = text.index('<script type="application/ld+json">') + len('<script type="application/ld+json">')
        person = json.loads(text[start:text.index("</script>", start)])
        assert person["@type"] == "Person" and person["url"] == expected[lang]
        if lang == "fa":
            assert '"name": "حامد ثنائی"' in text
        print(f"PASS {lang}: language, links, canonical, hreflang, metadata, structured data")
    redirect = Page((root / "index.html").read_text(encoding="utf-8"))
    assert redirect.find("meta", **{"http-equiv": "refresh", "content": "0; url=/fa/"})
    assert redirect.find("link", rel="canonical")[0]["href"] == expected["fa"]
    sitemap = ET.parse(root / "sitemap.xml")
    urls = [e.text for e in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    assert len(urls) == 3 and set(urls) == set(expected.values())
    robots = (root / "robots.txt").read_text(encoding="utf-8")
    assert "Allow: /" in robots and f"Sitemap: {base}/sitemap.xml" in robots
    print(f"PASS default redirect, sitemap and robots on {base}")


if __name__ == "__main__":
    check()
