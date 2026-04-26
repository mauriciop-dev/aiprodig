import os
import re

import unicodedata


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = text.strip("-")
    return text


def publish_article(number):
    project_root = "c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG"
    base_path = os.path.join(project_root, "Blog")
    txt_path = os.path.join(base_path, "artículos", f"articulo{number}.txt")

    if not os.path.exists(txt_path):
        print(f"Error: No se encontró el archivo {txt_path}")
        return

    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    article_data = {}
    current_key = None
    body_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        lower_line = line.lower()
        if (
            lower_line.startswith("titulo:")
            or lower_line.startswith("título:")
            or lower_line.startswith("título del artículo:")
        ):
            article_data["title"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("fecha:") or lower_line.startswith(
            "fecha de publicación:"
        ):
            article_data["date"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("categoría:") or lower_line.startswith("categoria:"):
            article_data["category"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("meta") and (
            "descripcion" in lower_line or "descripción" in lower_line
        ):
            article_data["meta"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("imagen") or lower_line.startswith(
            "imagen del articulo"
        ):
            article_data["image"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("fuentes:"):
            article_data["sources"] = line.split(":", 1)[1].strip()
        elif (
            lower_line.startswith("cuerpo:")
            or lower_line.startswith("cuerpo del artículo:")
            or lower_line.startswith("cuerpo del articulo:")
        ):
            current_key = "body"
            rest = line.split(":", 1)[1].strip()
            if rest:
                body_lines.append(rest)
        elif current_key == "body":
            body_lines.append(line)

    article_data["body"] = body_lines
    if "sources" not in article_data:
        article_data["sources"] = ""

    # Template for individual article page
    slug = slugify(article_data["title"])
    html_filename = f"{slug}.html"
    html_path = os.path.join(base_path, html_filename)

    body_html = "".join([f"<p>{p}</p>" for p in article_data["body"]])

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data["title"]} - Blog AIPRODIG</title>
    <meta name="description" content="{article_data["meta"]}">
    <meta property="og:title" content="{article_data["title"]} - Blog AIPRODIG">
    <meta property="og:description" content="{article_data["meta"]}">
    <meta property="og:image" content="https://aiprodig.com/Blog/images/{article_data["image"]}">
    <meta property="og:url" content="https://aiprodig.com/Blog/{html_filename}">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.8; color: #333; margin: 0; padding: 0; background: #fff; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 0; text-align: center; }}
        .article-container {{ max-width: 800px; margin: 120px auto 60px; padding: 0 2rem; }}
        .date {{ color: #7f8c8d; font-size: 0.9rem; text-align: center; margin-bottom: 1rem; }}
        h1 {{ font-size: 2.5rem; text-align: center; color: #2c3e50; margin-bottom: 2rem; line-height: 1.2; }}
        .hero-img {{ width: 100%; height: auto; border-radius: 15px; margin-bottom: 2.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .content {{ font-size: 1.1rem; color: #444; }}
        .content p {{ margin-bottom: 1.5rem; }}
        .sources {{ margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #eee; font-size: 0.9rem; color: #7f8c8d; }}
        .social-share {{ display: flex; gap: 1.5rem; margin-top: 3rem; justify-content: center; }}
        .btn-action {{
            display: flex; align-items: center; gap: 0.6rem;
            padding: 10px 24px; border-radius: 50px;
            border: none; cursor: pointer;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; font-weight: bold; font-size: 0.95rem;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            font-family: inherit; text-decoration: none;
        }}
        .btn-action:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        }}
        .btn-action svg {{ width: 20px; height: 20px; }}
        .footer {{ background: #2c3e50; color: white; text-align: center; padding: 2rem 0; margin-top: 4rem; }}
        nav {{ display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; padding: 0 2rem; }}
        .logo {{ font-size: 1.5rem; font-weight: bold; color: white; text-decoration: none; }}
        header {{ position: fixed; width: 100%; top: 0; z-index: 1000; }}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="index.html" class="logo">ProDig Blog</a>
            <div style="color: white; font-size: 0.9rem;">Prospectiva Digital</div>
        </nav>
    </header>

    <article class="article-container">
        <div class="date">{article_data["date"]} | {article_data["category"]}</div>
        <h1>{article_data["title"]}</h1>
        <img src="images/{article_data["image"]}" alt="{article_data["title"]}" class="hero-img">
        <div class="content">
            {body_html}
        </div>
        <div class="sources">
            <strong>Fuentes:</strong><br>
            {article_data["sources"]}
        </div>
        
        <div class="social-share">
            <a href="https://www.facebook.com/sharer/sharer.php?u=https://aiprodig.com/Blog/{html_filename}" target="_blank" rel="noopener noreferrer" class="btn-action" aria-label="Me gusta">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
                </svg>
                <span>Me gusta</span>
            </a>
            <a href="https://api.whatsapp.com/send?text=https://aiprodig.com/Blog/{html_filename}" target="_blank" rel="noopener noreferrer" class="btn-action" aria-label="Compartir">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="18" cy="5" r="3"></circle>
                    <circle cx="6" cy="12" r="3"></circle>
                    <circle cx="18" cy="19" r="3"></circle>
                    <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                    <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
                </svg>
                <span>Compartir</span>
            </a>
        </div>
    </article>

    <footer class="footer">
        <p>&copy; 2026 ProDig Blog - Todos los derechos reservados</p>
    </footer>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Éxito: Artículo publicado en {html_path}")

    # Update main index.html
    update_index(base_path, article_data, html_filename)

    # Update project root index.html (home page carousel)
    root_index_path = os.path.join(project_root, "index.html")
    if os.path.exists(root_index_path):
        update_root_index(root_index_path, article_data, html_filename)


def update_index(base_path, article_data, html_filename):
    index_path = os.path.join(base_path, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    nuevo_badge = '<div style="position: absolute; top: 1rem; left: 1rem; background: #ef4444; color: white; font-size: 0.7rem; font-weight: 800; padding: 0.3rem 0.8rem; border-radius: 99px; z-index: 5; text-transform: uppercase;">Nuevo</div>'
    card = f"""                    <div class="blog-card" style="flex: 0 0 300px; border: 1px solid #eee; border-radius: 20px; overflow: hidden; transition: 0.3s; display: flex; flex-direction: column; background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.05); scroll-snap-align: start; position: relative;">
                        {nuevo_badge}
                        <img src="/Blog/images/{article_data["image"]}" style="width: 100%; height: 180px; object-fit: cover;">
                        <div style="padding: 1.5rem; flex-grow: 1; display: flex; flex-direction: column;">
                            <span style="color: #2563eb; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; margin-bottom: 0.5rem;">{article_data["category"]}</span>
                            <h3 style="font-size: 1.2rem; margin-bottom: 0.8rem; color: #0f172a;">{article_data["title"]}</h3>
                            <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 1.5rem; line-height: 1.4;">{article_data["meta"]}</p>
                            <a href="/Blog/{html_filename}" style="margin-top: auto; color: #2563eb; text-decoration: none; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem;">Leer más <i class="fas fa-arrow-right"></i></a>
                        </div>
                    </div>"""

    marker = "<!-- Card 5 -->"
    if marker in content:
        content = content.replace(marker, card + "\n                    " + marker)
    elif "<!-- Card" in content:
        import re

        match = re.search(r"(<!-- Card \d+ -->)", content)
        if match:
            content = content.replace(
                match.group(1), card + "\n                    " + match.group(1)
            )
    elif '<div class="blog-carousel"' in content:
        pos = content.find('<div class="blog-carousel"')
        end = content.find(">", pos) + 1
        content = content[:end] + "\n" + card + "\n                " + content[end:]

    if "position: relative; padding: 0 3rem;" not in content:
        if '<div class="blog-carousel-wrapper"' not in content:
            carousel_start = '<div class="blog-carousel"'
            wrapper = f"""<div class="blog-carousel-wrapper" style="position: relative; padding: 0 3rem;">
                <button class="blog-nav-btn blog-nav-prev" onclick="scrollBlog(-1)" style="position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 48px; height: 48px; border-radius: 50%; border: 1px solid #e2e8f0; background: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 10; box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: 0.2s;">
                    <i class="fas fa-chevron-left" style="color: #2563eb; font-size: 1.2rem;"></i>
                </button>
                <div class="blog-carousel" id="blogCarousel" style="display: flex; overflow-x: hidden; gap: 1.5rem; padding: 1rem 0 2rem; scroll-snap-type: x mandatory;">
"""
            content = content.replace(carousel_start, wrapper)
            content = content.replace(
                "</div>\n            </div>\n            <style>",
                '</div>\n                <button class="blog-nav-btn blog-nav-next" onclick="scrollBlog(1)" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); width: 48px; height: 48px; border-radius: 50%; border: 1px solid #e2e8f0; background: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 10; box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: 0.2s;">\n                    <i class="fas fa-chevron-right" style="color: #2563eb; font-size: 1.2rem;"></i>\n                </button>\n            </div>\n            <script>\n                function scrollBlog(dir) {\n                    const c = document.getElementById(\'blogCarousel\');\n                    const card = c ? c.querySelector(\'.blog-card\') : null;\n                    const cardWidth = card ? card.offsetWidth + 24 : 324;\n                    if (c) c.scrollBy({ left: cardWidth * dir, behavior: \'smooth\' });\n                }\n            </script>',
            )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


def update_root_index(root_index_path, article_data, html_filename):
    with open(root_index_path, "r", encoding="utf-8") as f:
        content = f.read()

    nuevo_badge = '<div style="position: absolute; top: 1rem; left: 1rem; background: #ef4444; color: white; font-size: 0.7rem; font-weight: 800; padding: 0.3rem 0.8rem; border-radius: 99px; z-index: 5; text-transform: uppercase;">Nuevo</div>'
    card = f"""                <!-- Card N -->
                <div class="blog-card" style="flex: 0 0 300px; border: 1px solid #eee; border-radius: 20px; overflow: hidden; transition: 0.3s; display: flex; flex-direction: column; background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.05); scroll-snap-align: start; position: relative;">
                    {nuevo_badge}
                    <img src="/Blog/images/{article_data["image"]}" style="width: 100%; height: 180px; object-fit: cover;">
                    <div style="padding: 1.5rem; flex-grow: 1; display: flex; flex-direction: column;">
                        <span style="color: #2563eb; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; margin-bottom: 0.5rem;">{article_data["category"]}</span>
                        <h3 style="font-size: 1.2rem; margin-bottom: 0.8rem; color: #0f172a;">{article_data["title"]}</h3>
                        <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 1.5rem; line-height: 1.4;">{article_data["meta"]}</p>
                        <a href="/Blog/{html_filename}" style="margin-top: auto; color: #2563eb; text-decoration: none; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem;">Leer más <i class="fas fa-arrow-right"></i></a>
                    </div>
                </div>"""

    marker = "<!-- Card 5 -->"
    if marker in content:
        content = content.replace(
            marker, card + "\n                    <!-- Card 5 -->"
        )
    elif "<!-- Card" in content:
        import re

        match = re.search(r"(<!-- Card \d+ -->)", content)
        if match:
            content = content.replace(
                match.group(1), card + "\n                    " + match.group(1)
            )
    elif '<div class="blog-carousel"' in content:
        pos = content.find('<div class="blog-carousel"')
        end = content.find(">", pos) + 1
        content = content[:end] + "\n" + card + "\n                " + content[end:]

    if "position: relative; padding: 0 3rem;" not in content:
        if '<div class="blog-carousel-wrapper"' not in content:
            carousel_start = '<div class="blog-carousel"'
            wrapper = f"""<div class="blog-carousel-wrapper" style="position: relative; padding: 0 3rem;">
                <button class="blog-nav-btn blog-nav-prev" onclick="scrollBlog(-1)" style="position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 48px; height: 48px; border-radius: 50%; border: 1px solid #e2e8f0; background: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 10; box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: 0.2s;">
                    <i class="fas fa-chevron-left" style="color: #2563eb; font-size: 1.2rem;"></i>
                </button>
                <div class="blog-carousel" id="blogCarousel" style="display: flex; overflow-x: hidden; gap: 1.5rem; padding: 1rem 0 2rem; scroll-snap-type: x mandatory;">
"""
            content = content.replace(carousel_start, wrapper)
            content = content.replace(
                "</div>\n            </div>\n            <style>",
                '</div>\n                <button class="blog-nav-btn blog-nav-next" onclick="scrollBlog(1)" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); width: 48px; height: 48px; border-radius: 50%; border: 1px solid #e2e8f0; background: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 10; box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: 0.2s;">\n                    <i class="fas fa-chevron-right" style="color: #2563eb; font-size: 1.2rem;"></i>\n                </button>\n            </div>\n            <script>\n                function scrollBlog(dir) {\n                    const c = document.getElementById(\'blogCarousel\');\n                    const card = c ? c.querySelector(\'.blog-card\') : null;\n                    const cardWidth = card ? card.offsetWidth + 24 : 324;\n                    if (c) c.scrollBy({ left: cardWidth * dir, behavior: \'smooth\' });\n                }\n            </script>',
            )

    with open(root_index_path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        publish_article(sys.argv[1])
    else:
        print("Uso: python publisher.py [numero_articulo]")
