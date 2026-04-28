#!/usr/bin/env python3
"""
SEO Injector - Agrega meta tags seo-* a páginas existentes
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser

BASE_URL = "https://aiprodig.com"


class SEOInjector:
    """Inyecta meta tags seo-* en páginas HTML"""

    def __init__(self):
        self.updated_count = 0

    def process_file(self, html_path):
        """Procesa un archivo HTML"""
        try:
            with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if "seo-title" in content:
                print(f"   [SKIP] {html_path} - ya tiene meta tags")
                return False

            title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else ""

            desc_match = re.search(
                r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']',
                content,
                re.IGNORECASE,
            )
            description = desc_match.group(1).strip() if desc_match else ""

            keywords_match = re.search(
                r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']*)["\']',
                content,
                re.IGNORECASE,
            )
            keywords = (
                keywords_match.group(1).strip()
                if keywords_match
                else "IA, Inteligencia Artificial, Chatbot, SEO, GEO"
            )

            og_title_match = re.search(
                r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']*)["\']',
                content,
                re.IGNORECASE,
            )
            og_title = og_title_match.group(1).strip() if og_title_match else title

            og_desc_match = re.search(
                r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']*)["\']',
                content,
                re.IGNORECASE,
            )
            og_desc = (
                og_desc_match.group(1).strip() if og_desc_match else description[:160]
            )

            og_image_match = re.search(
                r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']*)["\']',
                content,
                re.IGNORECASE,
            )
            og_image = (
                og_image_match.group(1).strip()
                if og_image_match
                else f"{BASE_URL}/images/og-default.jpg"
            )

            base_path = html_path.as_posix().replace("\\", "/")
            url = (
                f"{BASE_URL}/{base_path}"
                if base_path != "index.html"
                else BASE_URL + "/"
            )

            section = self.detect_section(base_path)
            page_type = self.detect_type(base_path, section)
            priority = self.detect_priority(section)
            lang = "en" if "/en/" in base_path else "es"

            seo_tags = f'''
    <!-- SEO Meta Tags -->
    <meta name="seo-title" content="{self.truncate(title, 60)}">
    <meta name="seo-description" content="{self.truncate(description, 160)}">
    <meta name="seo-keywords" content="{keywords}">
    <meta name="seo-type" content="{page_type}">
    <meta name="seo-priority" content="{priority}">
    <meta name="seo-section" content="{section}">
    <meta name="seo-lang" content="{lang}">
'''

            og_tags = f'''
    <!-- Open Graph -->
    <meta property="og:title" content="{self.truncate(og_title, 60)}">
    <meta property="og:description" content="{self.truncate(og_desc, 160)}">
    <meta property="og:image" content="{og_image}">
    <meta property="og:url" content="{url}">
    <meta property="og:type" content="{page_type}">
    <meta property="og:locale" content="{lang}_CO">
    <meta property="og:site_name" content="ProDig - Prospectiva Digital">
'''

            twitter_tags = f'''
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{self.truncate(og_title, 60)}">
    <meta name="twitter:description" content="{self.truncate(og_desc, 160)}">
'''

            new_meta_block = seo_tags + og_tags + twitter_tags

            insert_pattern = r'(<meta charset="UTF-8">)'
            new_content = re.sub(
                insert_pattern, r"\1\n" + new_meta_block, content, count=1
            )

            if insert_pattern not in content:
                insert_pattern = r"(<head>)"
                new_content = re.sub(
                    insert_pattern, r"\1\n" + new_meta_block, content, count=1
                )

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"   [OK] {html_path}")
            self.updated_count += 1
            return True

        except Exception as e:
            print(f"   [ERROR] {html_path}: {e}")
            return False

    def detect_section(self, path):
        if path == "index.html" or path == "./index.html":
            return "home"
        elif "/Blog/" in path or "/blog/" in path:
            return "blog"
        elif (
            "/privacidad" in path
            or "/condiciones" in path
            or "/eliminacion" in path
            or "/registrometa" in path
        ):
            return "legal"
        elif "/chatbot" in path:
            return "services"
        elif "/powerbi" in path or "/powerapps" in path:
            return "services"
        elif "/conjuntos" in path:
            return "services"
        else:
            return "page"

    def detect_type(self, path, section):
        if section == "blog":
            return "article"
        elif section == "services":
            return "service"
        else:
            return "website"

    def detect_priority(self, section):
        priorities = {
            "home": "1.0",
            "services": "0.8",
            "products": "0.8",
            "blog": "0.6",
            "legal": "0.3",
            "page": "0.8",
        }
        return priorities.get(section, "0.8")

    def truncate(self, text, max_len):
        if len(text) <= max_len:
            return text
        return text[: max_len - 3].strip() + "..."


def find_html_files():
    """Encuentra archivos HTML a procesar"""
    html_files = []
    exclude_dirs = {
        ".git",
        "node_modules",
        ".next",
        "dist",
        "__pycache__",
        "SEO-GEO",
        "en",
    }
    exclude_files = {"template.html", "index.html"}

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file.endswith(".html"):
                html_files.append(Path(root) / file)

    return sorted(html_files)


def main():
    print("SEO Injector v1.0")
    print("=" * 40)

    injector = SEOInjector()

    print("\n[1/2] Buscando archivos HTML...")
    html_files = find_html_files()

    print(f"   Encontrados: {len(html_files)} archivos")

    print("\n[2/2] Procesando archivos...")
    for html_file in html_files:
        injector.process_file(html_file)

    print("\n" + "=" * 40)
    print(f"[OK] Completado! Archivos actualizados: {injector.updated_count}")


if __name__ == "__main__":
    main()
