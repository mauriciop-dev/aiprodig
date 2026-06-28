#!/usr/bin/env python3
"""test_seo_geo.py - Verificacion automatica de implementacion SEO+GEO para aiprodig.com"""
import os, sys, json, ssl
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://aiprodig.com"
passed = 0
failed = 0

CHECKMARK = "[PASS]"
CROSSMARK = "[FAIL]"

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  {CHECKMARK} {name}")
    else:
        failed += 1
        msg = f"  {CROSSMARK} {name}"
        if detail:
            msg += " - " + detail
        print(msg)

def read_file(rel_path):
    full = os.path.join(BASE_DIR, rel_path)
    try:
        with open(full, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

# ── HTML Parsers ──────────────────────────────────────────────────

class LandmarkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.has_main_main = False
        self.has_footer_lb = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main" and a.get("role") == "main":
            self.has_main_main = True
        if tag == "footer":
            self.has_footer_lb = "itemscope" in a and "LocalBusiness" in (a.get("itemtype") or "")

class JSONLDExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self._capture = False
        self._buf = []
    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self._capture = True
            self._buf = []
    def handle_endtag(self, tag):
        if tag == "script" and self._capture:
            text = "".join(self._buf).strip()
            if text:
                try:
                    self.scripts.append(json.loads(text))
                except json.JSONDecodeError:
                    self.scripts.append(None)
            self._capture = False
            self._buf = []
    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)

# ── Helpers ────────────────────────────────────────────────────────

def get_jsonld(path):
    html = read_file(path)
    if html is None:
        return None
    p = JSONLDExtractor()
    p.feed(html)
    return p.scripts

def find_ld(path, type_name):
    scripts = get_jsonld(path)
    if scripts is None:
        return None
    for s in scripts:
        if isinstance(s, dict) and s.get("@type") == type_name:
            return s
    return None

def has_ld(path, *types):
    scripts = get_jsonld(path)
    if scripts is None:
        return False, "Archivo no encontrado"
    if not scripts:
        return False, "Sin bloques JSON-LD"
    if any(s is None for s in scripts):
            return False, "JSON invalido"
    found = [s.get("@type") for s in scripts if isinstance(s, dict)]
    missing = [t for t in types if t not in found]
    if missing:
        return False, "Faltan @type: " + str(missing) + ", encontrados: " + str(found)
    return True, ""

def collect_ids(obj, result=None):
    if result is None:
        result = set()
    if isinstance(obj, dict):
        if "@id" in obj:
            result.add(obj["@id"])
        for v in obj.values():
            collect_ids(v, result)
    elif isinstance(obj, list):
        for item in obj:
            collect_ids(item, result)
    return result

def count_entity_refs(obj, target_id, count=None):
    if count is None:
        count = [0]
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "@id" and v == target_id:
                count[0] += 1
            else:
                count_entity_refs(v, target_id, count)
    elif isinstance(obj, list):
        for item in obj:
            count_entity_refs(item, target_id, count)
    return count[0]

def head_url(url, timeout=8):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = Request(url, method="HEAD")
        resp = urlopen(req, timeout=timeout, context=ctx)
        return resp.getcode()
    except (URLError, HTTPError, OSError) as e:
        return None

# ── Page lists ─────────────────────────────────────────────────────

SERVICE_PAGES = [
    "seo-y-geo.html", "chatbots.html", "saas.html", "ia-local.html",
    "rag.html", "agentes-ia.html", "power-platform.html",
    "capacitacion.html", "consultoria.html", "sitios-web-ia.html",
]
MAIN_PAGES = ["index.html"] + SERVICE_PAGES

BLOG_ES = [
    "Blog/del-caos-algoritmico-a-la-tasa-de-referencia-la-metamorfosis-del-seo-al-geo-y-el-surgimiento-de-la-autoridad-humana-en-2026.html",
    "Blog/el-activo-invisible-por-que-su-empresa-es-mas-pobre-de-lo-que-dicen-sus-libros-contables.html",
    "Blog/la-gran-convergencia-por-que-la-ia-de-hoy-es-el-sistema-operativo-de-la-materia-de-manana.html",
    "Blog/crees-que-tener-una-pagina-web-en-2026-es-irrelevante-la-realidad-te-sorprendera.html",
    "Blog/por-que-el-agile-tradicional-esta-frenando-tu-empresa-en-la-era-de-la-ia.html",
    "Blog/el-sindrome-del-software-frankenstein-la-tragedia-del-subuso-tecnologico-en-el-sector-publico-y-como-solucionarlo.html",
]
BLOG_EN = [
    "en/blog/do-you-think-having-a-website-in-2026-is-irrelevant-the-reality-will-surprise-you.html",
    "en/blog/the-great-convergence-why-today-s-ai-is-tomorrow-s-matter-operating-system.html",
    "en/blog/the-invisible-asset-why-your-company-is-poorer-than-your-accounting-books-say.html",
    "en/blog/why-is-traditional-agile-slowing-down-your-company-in-the-age-of-ai.html",
    "en/blog/the-frankenstein-software-syndrome-the-tragedy-of-technological-underuse-in-the-public-sector-and-how-to-fix-it.html",
]
ALL_BLOG_ARTICLES = BLOG_ES + BLOG_EN

ENTITY_FRAGMENTS = {"#organization", "#mauricio-pineda", "#website", "#glosario-prodig"}

# ── Main ────────────────────────────────────────────────────────────

def main():
    global passed, failed
    print("\n=== SEO+GEO Verification - aiprodig.com ===\n")

    # ── 1. robots.txt ──────────────────────────────────────────
    print("--- 1. robots.txt ---")
    robots = read_file("robots.txt")
    check("robots.txt existe", robots is not None)
    if robots:
        norm = robots.replace("\r\n", "\n")
        ia_crawlers = [
            "GPTBot", "ClaudeBot", "Google-Extended", "PerplexityBot",
            "anthropic-ai", "Gemini-GPTBot", "OAI-SearchBot", "Applebot-Extended",
        ]
        for c in ia_crawlers:
            block = f"User-agent: {c}"
            check(f"robots.txt: User-agent: {c}", block in norm)
        check("robots.txt: Sitemap: sitemap.xml",
              "Sitemap: https://aiprodig.com/sitemap.xml" in norm)
        check("robots.txt: Sitemap: sitemap-blog.xml",
              "Sitemap: https://aiprodig.com/sitemap-blog.xml" in norm)

    # ── 2. Sitemaps ────────────────────────────────────────────
    print("\n--- 2. Sitemaps ---")
    SMS_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", SMS_NS)
    all_sitemap_urls = []

    for sm in ["sitemap.xml", "sitemap-pages.xml", "sitemap-blog.xml"]:
        content = read_file(sm)
        check(f"{sm} existe", content is not None)
        if content:
            try:
                root = ET.fromstring(content)
                check(f"{sm} XML v\u00e1lido", True)
                if sm == "sitemap.xml":
                    for sm_child in root.iter(f"{{{SMS_NS}}}sitemap"):
                        loc = sm_child.find(f"{{{SMS_NS}}}loc")
                        if loc is not None and loc.text:
                            all_sitemap_urls.append(loc.text)
                else:
                    for url_el in root.iter(f"{{{SMS_NS}}}url"):
                        loc = url_el.find(f"{{{SMS_NS}}}loc")
                        if loc is not None and loc.text:
                            all_sitemap_urls.append(loc.text)
            except ET.ParseError:
                check(f"{sm} XML v\u00e1lido", False, "Error de parseo")

    # Accessibility of sitemap URLs (HEAD requests)
    print("   (Verificando accesibilidad de URLs en sitemaps - requiere conexion a internet)...")
    accessible = 0
    inaccessible = 0
    all_conn_err = True
    for url in all_sitemap_urls:
        code = head_url(url)
        if code == 200:
            accessible += 1
        else:
            inaccessible += 1
            if code is not None:
                all_conn_err = False
    if all_sitemap_urls:
        if all_conn_err:
            print("   [INFO] {} URLs en sitemaps (verificacion HTTP omitida - sin conexion a internet)".format(len(all_sitemap_urls)))
        else:
            ok = inaccessible == 0
            check("{}/{} URLs accesibles".format(accessible, len(all_sitemap_urls)), ok, "{} fallaron".format(inaccessible) if not ok else "")

    # ── 3. HTML5 Landmarks ─────────────────────────────────────
    print("\n--- 3. HTML5 Landmarks ---")
    for page in MAIN_PAGES:
        html = read_file(page)
        if html is None:
            check(f"{page}: archivo", False)
            continue
        p = LandmarkParser()
        p.feed(html)
        label = page if page != "index.html" else "index.html (home)"
        check(f"{label}: <main role=\"main\">", p.has_main_main)
        check(f"{label}: <footer itemscope itemtype=\"LocalBusiness\">", p.has_footer_lb)

    # ── 4. JSON-LD Validation ─────────────────────────────────
    print("\n--- 4. JSON-LD Validation ---")

    # 4a. index.html
    ok, detail = has_ld("index.html", "Organization", "WebSite", "DefinedTermSet")
    check("index.html: Organization, WebSite, DefinedTermSet", ok, detail)

    org = find_ld("index.html", "Organization")
    if org and "aggregateRating" in org:
        ar = org["aggregateRating"]
        check("index.html: AggregateRating.ratingValue == 5.0",
              isinstance(ar, dict) and ar.get("ratingValue") == "5.0")
        check("index.html: AggregateRating.reviewCount >= 3",
              isinstance(ar, dict) and int(ar.get("reviewCount", 0)) >= 3)
    else:
        check("index.html: AggregateRating en Organization", False, "No encontrado")

    # 4b. seo-y-geo.html
    ok, detail = has_ld("seo-y-geo.html", "Service", "FAQPage", "WebPage")
    check("seo-y-geo.html: Service, FAQPage, SpeakableSpecification", ok, detail)

    # 4c. Service pages -> Service schema with provider @id
    for page in SERVICE_PAGES:
        svc = find_ld(page, "Service")
        if svc is None:
            check(f"{page}: Schema Service", False, "No encontrado")
        else:
            prov = svc.get("provider")
            has_provider = isinstance(prov, dict) and prov.get("@id") == f"{SITE_URL}/#organization"
            check(f"{page}: Service.provider -> #organization", has_provider)

    # 4d. Blog articles -> BlogPosting
    for article in ALL_BLOG_ARTICLES:
        bp = find_ld(article, "BlogPosting")
        if bp is None:
            check(f"{article}: Schema BlogPosting", False, "No encontrado")
        else:
            auth = isinstance(bp.get("author"), dict) and bp["author"].get("@id") == f"{SITE_URL}/#mauricio-pineda"
            pub = isinstance(bp.get("publisher"), dict) and bp["publisher"].get("@id") == f"{SITE_URL}/#organization"
            check(f"{article}: BlogPosting.author -> #mauricio-pineda", auth)
            check(f"{article}: BlogPosting.publisher -> #organization", pub)

    # Blog listing pages -> CollectionPage
    for bp_page in ["Blog/index.html", "en/blog/index.html"]:
        cp = find_ld(bp_page, "CollectionPage")
        check(f"{bp_page}: Schema CollectionPage", cp is not None)

    # 4e. sobre-mauricio-pineda.html -> Person
    person = find_ld("sobre-mauricio-pineda.html", "Person")
    check("sobre-mauricio-pineda.html: Schema Person", person is not None)
    if person:
        check("Person.worksFor -> #organization",
              isinstance(person.get("worksFor"), dict) and person["worksFor"].get("@id") == f"{SITE_URL}/#organization")

    # ── 5. Entity Linking ─────────────────────────────────────
    print("\n--- 5. Entity Linking Verification ---")
    entity_pages = MAIN_PAGES + ALL_BLOG_ARTICLES + ["Blog/index.html", "en/blog/index.html", "sobre-mauricio-pineda.html"]
    for page in entity_pages:
        scripts = get_jsonld(page)
        if scripts is None or not scripts:
            continue
        all_ids = set()
        for s in scripts:
            if isinstance(s, dict):
                all_ids |= collect_ids(s)
        for frag in ENTITY_FRAGMENTS:
            expected_id = SITE_URL + "/" + frag
            found_bad = False
            for ref in all_ids:
                if frag in ref and ref != expected_id:
                    check("{}: @id ref {} incorrecto: {}".format(page, frag, ref),
                          False, "Debe ser " + expected_id)
                    found_bad = True
                    break
            if not found_bad:
                if any(frag in rid for rid in all_ids):
                    check("{}: @id ref {} usa URI absoluta".format(page, frag), True)

    # ── 6. BreadcrumbList ──────────────────────────────────────
    print("\n--- 6. BreadcrumbList ---")
    for page in SERVICE_PAGES + ["sobre-mauricio-pineda.html"]:
        bc = find_ld(page, "BreadcrumbList")
        check(f"{page}: Schema BreadcrumbList", bc is not None)

    # ── 7. llm files ───────────────────────────────────────────
    print("\n--- 7. LLM Files ---")
    for fname in ["llm.txt", "llm-full.txt", "llms.txt"]:
        content = read_file(fname)
        check(f"{fname} existe", content is not None)
        if content is not None:
            check(f"{fname} no vac\u00edo", len(content.strip()) > 0)

    # ── 8. Image Files ─────────────────────────────────────────
    print("\n--- 8. Image Files ---")
    for img in ["images/prodig-logo.png", "images/prodig-hero-futuro-digital.webp", "images/mauricio-pineda.jpg"]:
        full = os.path.join(BASE_DIR, img)
        check(f"{img} existe", os.path.isfile(full))

    # ── Results ────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Resultados: {passed} pasaron, {failed} fallaron (de {total})")
    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()
