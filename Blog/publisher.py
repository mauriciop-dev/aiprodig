import os
import re

import unicodedata

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text

def publish_article(number):
    base_path = 'c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/Blog'
    txt_path = os.path.join(base_path, 'artículos', f'articulo{number}.txt')
    
    if not os.path.exists(txt_path):
        print(f"Error: No se encontró el archivo {txt_path}")
        return

    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    article_data = {}
    current_key = None
    body_lines = []
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if line.lower().startswith('titulo:'):
            article_data['title'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('fecha:'):
            article_data['date'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('categoría:'):
            article_data['category'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('meta descripción:'):
            article_data['meta'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('imagen:'):
            article_data['image'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('fuentes:'):
            article_data['sources'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('cuerpo:'):
            current_key = 'body'
            # Add the rest of the line if there's text after 'Cuerpo:'
            rest = line.split(':', 1)[1].strip()
            if rest: body_lines.append(rest)
        elif current_key == 'body':
            body_lines.append(line)

    article_data['body'] = body_lines
    
    # Template for individual article page
    slug = slugify(article_data['title'])
    html_filename = f"{slug}.html"
    html_path = os.path.join(base_path, html_filename)
    
    body_html = "".join([f"<p>{p}</p>" for p in article_data['body']])
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data['title']} - Blog AIPRODIG</title>
    <meta name="description" content="{article_data['meta']}">
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
        .social-share {{ display: flex; gap: 1rem; margin-top: 3rem; justify-content: center; }}
        .btn-share {{ padding: 10px 20px; border-radius: 50px; text-decoration: none; color: white; font-weight: bold; font-size: 0.9rem; }}
        .btn-facebook {{ background: #1877f2; }}
        .btn-whatsapp {{ background: #25d366; }}
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
        <div class="date">{article_data['date']} | {article_data['category']}</div>
        <h1>{article_data['title']}</h1>
        <img src="images/{article_data['image']}" alt="{article_data['title']}" class="hero-img">
        <div class="content">
            {body_html}
        </div>
        <div class="sources">
            <strong>Fuentes:</strong><br>
            {article_data['sources']}
        </div>
        
        <div class="social-share">
            <a href="#" class="btn-share btn-facebook"><i class="fab fa-facebook-f"></i> Me gusta</a>
            <a href="#" class="btn-share btn-whatsapp"><i class="fab fa-whatsapp"></i> Compartir</a>
        </div>
    </article>

    <footer class="footer">
        <p>&copy; 2026 ProDig Blog - Todos los derechos reservados</p>
    </footer>
</body>
</html>
"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Éxito: Artículo publicado en {html_path}")
    
    # Update main index.html
    update_index(base_path, article_data, html_filename)

def update_index(base_path, article_data, html_filename):
    index_path = os.path.join(base_path, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_card = f"""
            <a href="{html_filename}" class="blog-card">
                <img src="images/{article_data['image']}" alt="{article_data['title']}" class="blog-card-image">
                <div class="blog-card-content">
                    <span class="blog-card-category">{article_data['category']}</span>
                    <h2 class="blog-card-title small-text">{article_data['title']}</h2>
                    <p class="blog-card-description">{article_data['meta']}</p>
                </div>
            </a>"""
    
    # Insert before the closing grid div
    if '<!-- Los artículos se cargarán aquí' in content:
        placeholder = '<!-- Los artículos se cargarán aquí dinámicamente o se añadirán manualmente -->'
        content = content.replace(placeholder, placeholder + new_card)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        publish_article(sys.argv[1])
    else:
        print("Uso: python publisher.py [numero_articulo]")
