#!/usr/bin/env python3
"""
SEO-GEO Generator
Escanea páginas HTML, extrae metadatos y genera sitemap.xml + llms.txt
"""

import os
import re
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser

BASE_URL = "https://aiprodig.com"
OUTPUT_DIR = Path(".")
SEO_DIR = Path("SEO-GEO")


class SEOParser(HTMLParser):
    """Parser para extraer meta tags seo-*"""

    def __init__(self):
        super().__init__()
        self.meta_tags = {}
        self.title = ""
        self.og_tags = {}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "title":
            pass

        elif tag == "meta":
            name = attrs_dict.get("name", attrs_dict.get("property", ""))
            content = attrs_dict.get("content", "")

            if name.startswith("seo-"):
                self.meta_tags[name] = content
            elif name.startswith("og:"):
                self.og_tags[name] = content
            elif name in ("description", "keywords", "author"):
                self.meta_tags[f"seo-{name}"] = content

    def handle_data(self, data):
        if not self.title:
            self.title = data.strip()


def extract_metadata(html_path):
    """Lee HTML y extrae metadatos SEO"""
    try:
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        parser = SEOParser()
        parser.feed(content)

        title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
        if title_match:
            parser.title = title_match.group(1).strip()

        base_path = html_path.as_posix().replace("\\", "/")

        if base_path == "index.html" or base_path == "./index.html":
            url = BASE_URL + "/"
            priority = "1.0"
            section = "home"
            changefreq = "weekly"
        elif "/Blog/" in base_path or "/blog/" in base_path:
            url = BASE_URL + "/" + base_path
            priority = parser.meta_tags.get("seo-priority", "0.6")
            section = "blog"
            changefreq = "monthly"
        elif parser.meta_tags.get("seo-section"):
            section = parser.meta_tags.get("seo-section")
            url = BASE_URL + "/" + base_path
            if section in ("services", "products"):
                priority = "0.8"
                changefreq = "monthly"
            else:
                priority = parser.meta_tags.get("seo-priority", "0.3")
                changefreq = "yearly"
        else:
            url = BASE_URL + "/" + base_path
            priority = parser.meta_tags.get("seo-priority", "0.8")
            section = "page"
            changefreq = "monthly"

        page_type = parser.meta_tags.get("seo-type", "website")
        lang = parser.meta_tags.get("seo-lang", "es")

        return {
            "title": parser.meta_tags.get("seo-title", parser.title),
            "description": parser.meta_tags.get("seo-description", ""),
            "keywords": parser.meta_tags.get("seo-keywords", ""),
            "type": page_type,
            "priority": priority,
            "section": section,
            "lang": lang,
            "url": url,
            "changefreq": changefreq,
            "og": parser.og_tags,
        }

    except Exception as e:
        print(f"Error procesando {html_path}: {e}")
        return None


def find_html_files():
    """Encuentra todos los archivos .html"""
    html_files = []

    exclude_dirs = {".git", "node_modules", ".next", "dist", "__pycache__", "SEO-GEO"}
    exclude_files = {"template.html"}

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file.endswith(".html") and file not in exclude_files:
                html_files.append(Path(root) / file)

    return sorted(html_files)


def validate_metadata(pages):
    """Valida límites de meta tags"""
    errors = []

    for page in pages:
        if not page:
            continue

        title = page.get("title", "")
        desc = page.get("description", "")

        if len(title) > 60:
            errors.append(f"[WARN] {page['url']}: title > 60 chars ({len(title)})")

        if len(desc) > 160:
            errors.append(
                f"[WARN] {page['url']}: description > 160 chars ({len(desc)})"
            )

    return errors


def generate_sitemap(pages):
    """Genera sitemap.xml"""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for page in pages:
        if not page:
            continue
        lines.append("  <url>")
        lines.append(f"    <loc>{page['url']}</loc>")
        lines.append(f"    <changefreq>{page['changefreq']}</changefreq>")
        lines.append(f"    <priority>{page['priority']}</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")

    return "\n".join(lines)


def generate_llms(pages, org_info):
    """Genera llms.txt"""
    lines = [
        "# ProDig (Prospectiva Digital)",
        "> Consultoría de vanguardia en Inteligencia Artificial y desarrollo de activos digitales.",
        "",
        "## Resumen",
        f"{org_info['description']}",
        "",
        "## Productos y Activos",
    ]

    for product in org_info.get("products", []):
        lines.append(f"- **{product['name']}:** {product['desc']} {product['url']}")

    lines.extend(["", "## Servicios"])

    for service in org_info.get("services", []):
        lines.append(f"- **{service}**")

    lines.extend(
        [
            "",
            "## Stack Tecnológico",
            org_info.get(
                "stack",
                "n8n, Supabase, Vercel, GitHub y modelos avanzados de IA (Gemini, OpenAI).",
            ),
            "",
            "## Contacto y Ubicación",
            f"Sede principal en {org_info['location']}.",
            f"Web: {org_info['website']}",
            f"WhatsApp: {org_info['whatsapp']}",
            f"email: {org_info['email']}",
            "",
            "## Páginas del Sitio",
        ]
    )

    home_pages = [p for p in pages if p and p.get("section") == "home"]
    service_pages = [
        p for p in pages if p and p.get("section") in ("services", "products")
    ]
    blog_pages = [p for p in pages if p and p.get("section") == "blog"]
    legal_pages = [p for p in pages if p and p.get("section") == "legal"]
    other_pages = [
        p
        for p in pages
        if p
        and p.get("section") not in ("home", "services", "products", "blog", "legal")
    ]

    if home_pages:
        lines.append("### Home")
        lines.append(f"- {home_pages[0]['title']}: {BASE_URL}/")

    if service_pages:
        lines.append("### Servicios y Productos")
        for p in service_pages:
            lines.append(f"- {p['title']}: {p['url']}")

    if blog_pages:
        lines.append("### Blog")
        for p in blog_pages:
            lang = p.get("lang", "es")
            lang_label = " (EN)" if lang == "en" else ""
            lines.append(f"- {p['title']}{lang_label}: {p['url']}")

    if other_pages:
        lines.append("### Otras Páginas")
        for p in other_pages:
            lines.append(f"- {p['title']}: {p['url']}")

    if legal_pages:
        lines.append("### Legal")
        for p in legal_pages:
            lines.append(f"- {p['title']}: {p['url']}")

    lines.append("")
    return "\n".join(lines)


def main():
    print("SEO-GEO Generator v1.0")
    print("=" * 40)

    print("\n[1/4] Escaneando archivos HTML...")
    html_files = find_html_files()
    print(f"   Encontrados: {len(html_files)} archivos")

    print("\n[2/4] Extrayendo metadatos...")
    pages = []
    for html_file in html_files:
        meta = extract_metadata(html_file)
        if meta:
            pages.append(meta)
            print(f"   [OK] {meta['url']} ({meta['type']})")

    print("\n[3/4] Validando meta tags...")
    errors = validate_metadata(pages)
    if errors:
        for err in errors:
            print(f"   {err}")
    else:
        print("   [OK] Límites OK")

    print("\n[4/4] Generando archivos...")

    org_info = {
        "description": "ProDig, liderada por Mauricio Pineda, se especializa en la creación de soluciones basadas en IA para optimizar procesos empresariales y residenciales.",
        "products": [
            {
                "name": "PAIC",
                "desc": "Plataforma de Administración Inteligente de Conjuntos (SaaS)",
                "url": "https://www.paicai.com.co/",
            },
            {
                "name": "NexoSalud",
                "desc": "Integración de datos de salud y cumplimiento normativo (RDA)",
                "url": "https://nexosalud-rda.vercel.app/",
            },
            {
                "name": "Notaria Digital",
                "desc": "Verificación de documentos mediante blockchain",
                "url": "https://validador-hazel.vercel.app/",
            },
        ],
        "services": [
            "Sitios Web IA integrados con IA y/o automatización",
            "SEO y GEO - Ser el referente de las IAs",
            "Chatbots - Iniciá en el mundo de IA",
            "SaaS - Demo en 48 horas",
            "IA Local - RAG seguro en tu empresa",
            "Power Platform - Power BI, Power Apps, Power Automate",
            "Agentes de IA con Google ADK",
            "Capacitación en IA",
            "Consultoría especializada",
        ],
        "stack": "n8n, Supabase, Vercel, GitHub y modelos avanzados de IA (Gemini, OpenAI). Vibe Coding.",
        "location": "Bogotá, Colombia",
        "website": "https://aiprodig.com",
        "whatsapp": "+57 3144897092",
        "email": "info@aiprodig.com",
    }

    sitemap = generate_sitemap(pages)
    with open(OUTPUT_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"   [OK] sitemap.xml")

    llms = generate_llms(pages, org_info)
    with open(OUTPUT_DIR / "llms.txt", "w", encoding="utf-8") as f:
        f.write(llms)
    print(f"   [OK] llms.txt")

    print("\n" + "=" * 40)
    print("[OK] SEO-GEO Generator completado!")
    print(f"   Paginas procesadas: {len(pages)}")
    print(f"   Errores/Warnings: {len(errors)}")


if __name__ == "__main__":
    main()
