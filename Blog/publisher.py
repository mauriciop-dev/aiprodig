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


def parse_article(txt_path):
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
    return article_data


def build_body_html(body_lines):
    html_parts = []
    for line in body_lines:
        if line.startswith(
            ("1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ")
        ):
            html_parts.append(
                f'<p class="article-paragraph"><strong>{line}</strong></p>'
            )
        elif line.startswith(("* ")):
            html_parts.append(f'<p class="article-paragraph">{line[2:]}</p>')
        elif re.match(r"^\d+\.\s", line):
            html_parts.append(f'<p class="article-paragraph">{line}</p>')
        elif line.startswith('"') or line.startswith('"'):
            html_parts.append(f'<p class="article-paragraph"><em>{line}</em></p>')
        else:
            html_parts.append(f'<p class="article-paragraph">{line}</p>')
    return "\n            ".join(html_parts)


def build_sources_html(sources):
    if not sources:
        return ""
    links = [l.strip() for l in sources.split("|") if l.strip()]
    items = "\n            ".join(
        [f'<p class="article-paragraph">{l}</p>' for l in links]
    )
    return f"""<div class="sources">
            <h4>Fuentes y Referencias:</h4>
            {items}
        </div>"""


def publish_article(number):
    project_root = "c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG"
    base_path = os.path.join(project_root, "Blog")
    txt_path = os.path.join(base_path, "artículos", f"articulo{number}.txt")

    if not os.path.exists(txt_path):
        print(f"Error: No se encontró el archivo {txt_path}")
        return

    article_data = parse_article(txt_path)
    slug = slugify(article_data["title"])
    html_filename = f"{slug}.html"
    html_path = os.path.join(base_path, html_filename)
    article_id = slug

    sources_html = build_sources_html(article_data.get("sources", ""))
    body_html = build_body_html(article_data["body"])

    canonical_url = f"https://aiprodig.com/Blog/{html_filename}"
    article_url = f"https://aiprodig.com/Blog/{html_filename}"

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{article_data["meta"]}">
    <title>{article_data["title"]} | ProDig Blog</title>
    
    <link rel="canonical" href="{canonical_url}">
    <link rel="alternate" hreflang="en" href="https://aiprodig.com/en/blog/{slug}">
    
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        :root {{
            --primary: #0f172a;
            --accent: #2563eb;
            --text-main: #334155;
            --bg-header: #f8fafc;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Outfit', sans-serif; line-height: 1.8; color: var(--text-main); background: #fff; }}
        
        .article-header {{ position: relative; padding: 4.5rem 2rem; text-align: center; background: var(--bg-header); border-bottom: 1px solid #e2e8f0; overflow: hidden; }}
        #bg-canvas {{ position: absolute; top:0; left:0; width:100%; height:100%; }}
        .header-content {{ position: relative; z-index: 2; max-width: 900px; margin: 0 auto; }}
        .category-tag {{ background: var(--accent); color: white; padding: 0.3rem 1rem; border-radius: 99px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }}
        .main-title {{ font-size: 2.8rem; margin: 1rem 0; font-weight: 700; color: var(--primary); }}
        .date {{ opacity: 0.6; font-size: 0.9rem; }}

        .article-container {{ max-width: 800px; margin: 0 auto; padding: 0 1.5rem 6rem; }}
        .hero-image {{ width: 100%; height: auto; border-radius: 20px; margin-top: -3.5rem; position: relative; z-index: 10; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
        .article-body {{ font-size: 1.2rem; margin-top: 4rem; text-align: justify; }}
        .article-subtitle {{ font-size: 1.8rem; margin: 3rem 0 1.5rem; font-weight: 700; color: var(--primary); }}
        .article-paragraph {{ margin-bottom: 1.8rem; }}
        
        .sources {{ background: #f1f5f9; padding: 2rem; border-radius: 16px; margin: 4rem 0; border-left: 6px solid var(--accent); }}
        .sources h4 {{ margin-bottom: 1rem; font-size: 1.1rem; }}
        .sources p {{ margin-bottom: 0.5rem; font-size: 0.95rem; }}
        
        .post-nav {{ display: grid; grid-template-columns: 1fr auto 1fr; gap: 1rem; align-items: center; margin: 4rem 0; padding: 1.5rem 0; border-top: 1px solid #eee; }}
        .nav-btn {{ text-decoration: none; display: flex; flex-direction: column; transition: 0.3s; }}
        .nav-btn span {{ font-weight: 700; font-size: 0.8rem; color: var(--accent); text-transform: uppercase; }}
        .nav-btn small {{ color: var(--text-main); font-size: 0.85rem; }}
        .back-home {{ width: 44px; height: 44px; border-radius: 50%; background: #f1f5f9; display: flex; align-items: center; justify-content: center; color: var(--text-main); text-decoration: none; }}

        .interaction-footer {{ display: flex; justify-content: space-between; align-items: center; padding: 1.5rem; background: #f8fafc; border-radius: 16px; }}
        .btn-action {{ padding: 0.7rem 1.2rem; border-radius: 12px; border: 1px solid #ddd; background: white; cursor: pointer; text-decoration: none; color: inherit; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }}
        .btn-like.active {{ background: #eff6ff; color: var(--accent); border-color: var(--accent); }}
        
        .whatsapp-float {{ position: fixed; bottom: 30px; right: 30px; background: #25d366; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; z-index: 1000; box-shadow: 0 8px 20px rgba(0,0,0,0.2); }}

        @media (max-width: 600px) {{ .main-title {{ font-size: 2rem; }} .post-nav {{ grid-template-columns: 1fr; text-align: center; }} .back-home {{ margin: 0 auto; order: -1; }} }}
    </style>
</head>
<body>
    <header class="article-header">
        <canvas id="bg-canvas"></canvas>
        <div class="header-content">
            <span class="category-tag">{article_data["category"]}</span>
            <h1 class="main-title">{article_data["title"]}</h1>
            <p class="date">{article_data["date"]}</p>
        </div>
    </header>

    <main class="article-container">
        <img src="/Blog/images/{article_data["image"]}" alt="{article_data["title"]}" class="hero-image">
        <article class="article-body">
            {body_html}
        </article>
        {sources_html}
        
        <nav class="post-nav">
            <a href="/Blog" class="back-home"><i class="fa-solid fa-house"></i></a>
            <div></div>
        </nav>
        
        <footer class="interaction-footer">
            <button id="likeBtn" class="btn-action btn-like"><i class="fa-solid fa-heart"></i> <span id="likeCount">0</span> Me gusta</button>
            <div style="display:flex; gap:1rem;">
                <a href="https://www.linkedin.com/sharing/share-offsite/?url={article_url}" class="btn-action" target="_blank"><i class="fab fa-linkedin"></i></a>
                <a href="https://wa.me/?text={article_data["title"]}%20{article_url}" class="btn-action" target="_blank"><i class="fab fa-whatsapp"></i></a>
            </div>
        </footer>
    </main>

    <a href="https://wa.me/573144897092" class="whatsapp-float" target="_blank"><i class="fab fa-whatsapp"></i></a>

    <script>
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        function init() {{
            canvas.width = window.innerWidth; canvas.height = canvas.parentElement.offsetHeight;
            particles = [];
            for(let i=0; i<65; i++) particles.push({{x:Math.random()*canvas.width, y:Math.random()*canvas.height, vx:(Math.random()-0.5)*0.6, vy:(Math.random()-0.5)*0.6}});
        }}
        function draw() {{
            ctx.clearRect(0,0,canvas.width, canvas.height);
            ctx.fillStyle = 'rgba(37, 99, 235, 0.45)';
            ctx.strokeStyle = 'rgba(37, 99, 235, 0.25)';
            particles.forEach((p,i) => {{
                p.x+=p.vx; p.y+=p.vy;
                if(p.x<0||p.x>canvas.width) p.vx*=-1; if(p.y<0||p.y>canvas.height) p.vy*=-1;
                ctx.beginPath(); ctx.arc(p.x,p.y,2.5,0,Math.PI*2); ctx.fill();
                for(let j=i+1; j<particles.length; j++) {{
                    let p2 = particles[j]; let d = Math.hypot(p.x-p2.x, p.y-p2.y);
                    if(d<130) {{ ctx.beginPath(); ctx.lineWidth=1; ctx.moveTo(p.x,p.y); ctx.lineTo(p2.x,p2.y); ctx.stroke(); }}
                }}
            }});
            requestAnimationFrame(draw);
        }}
        window.onresize = init; init(); draw();

        const aid = "{article_id}";
        const lbtn = document.getElementById('likeBtn');
        const lcnt = document.getElementById('likeCount');
        const API_BASE = "https://s34xeek7.functions.insforge.app";
        
        let count = 0;
        let liked = localStorage.getItem('H_'+aid) === 'Y';

        async function fetchStats() {{
            try {{
                const r = await fetch(API_BASE + "/get-stats");
                const data = await r.json();
                const item = data.find(i => i.article_id === aid);
                if (item) {{ count = item.likes_count; up(); }}
            }} catch (e) {{ console.error("Error fetching stats", e); }}
        }}

        function up() {{ lcnt.innerText = count; lbtn.className = liked ? 'btn-action btn-like active' : 'btn-action btn-like'; }}

        lbtn.onclick = async () => {{
            if(liked) return;
            count++; liked = true;
            localStorage.setItem('H_'+aid, 'Y');
            up();
            try {{ await fetch(API_BASE + "/handle-likes", {{ method: 'POST', body: JSON.stringify({{ article_id: aid }}) }}); }}
            catch (e) {{ console.error("Error saving like", e); }}
        }};

        fetchStats(); up();
    </script>
</body>
</html>"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Éxito: Artículo publicado en {html_path}")

    update_index(base_path, article_data, html_filename)

    root_index_path = os.path.join(project_root, "index.html")
    if os.path.exists(root_index_path):
        update_root_index(root_index_path, article_data, html_filename)


def update_index(base_path, article_data, html_filename):
    index_path = os.path.join(base_path, "index.html")
    if not os.path.exists(index_path):
        return
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    nuevo_badge = '<div style="position: absolute; top: 1rem; left: 1rem; background: #ef4444; color: white; font-size: 0.7rem; font-weight: 800; padding: 0.3rem 0.8rem; border-radius: 99px; z-index: 5; text-transform: uppercase;">Nuevo</div>'
    card = f"""            <div class="blog-card">
                <img src="/Blog/images/{article_data["image"]}" class="card-img" alt="{article_data["title"]}" style="position: relative;">
                {nuevo_badge}
                <div class="card-content">
                    <span class="card-tag">{article_data["category"]}</span>
                    <h3>{article_data["title"]}</h3>
                    <p>{article_data["meta"]}</p>
                    <a href="/Blog/{html_filename}" class="read-more">Leer Artículo <i class="fas fa-arrow-right"></i></a>
                </div>
            </div>"""

    marker = "<!-- Artículo 4 -->"
    if marker in content:
        content = content.replace(marker, card + "\n\n" + marker)
    elif "<!-- Artículo" in content:
        import re

        match = re.search(r"(<!-- Artículo \d+ -->)", content)
        if match:
            content = content.replace(match.group(1), card + "\n\n" + match.group(1))

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
                "</div>\n            </div>\n            <script>",
                '</div>\n                <button class="blog-nav-btn blog-nav-next" onclick="scrollBlog(1)" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); width: 48px; height: 48px; border-radius: 50%; border: 1px solid #e2e8f0; background: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 10; box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: 0.2s;">\n                    <i class="fas fa-chevron-right" style="color: #2563eb; font-size: 1.2rem;"></i>\n                </button>\n            </div>\n            <script>',
            )

    with open(root_index_path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        publish_article(sys.argv[1])
    else:
        print("Uso: python publisher.py [numero_articulo]")
