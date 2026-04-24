import os
import re
import shutil
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS ---
ARTICULOS_DIR = "Blog/artículos/"
IMAGES_DIR = "Blog/images/"
OUTPUT_ES = "Blog/"
OUTPUT_EN = "en/blog/"

def create_slug(title):
    """Crea una URL amigable a partir del título"""
    slug = title.lower()
    # Eliminar acentos y eñes
    slug = re.sub(r'[áéíóúüñ]', lambda x: {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ü':'u','ñ':'n'}[x.group()], slug)
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    return slug

def parse_txt(file_path):
    """Extrae la metadata y el cuerpo del archivo .txt"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex para extraer campos (versión más robusta)
    def get_field(field, text, dotall=False):
        match = re.search(f"{field}:\\s*(.*?)(?=\\n[A-Z][a-z]+:|$)", text, re.DOTALL if dotall else 0)
        return match.group(1).strip() if match else ""

    data = {
        "titulo": get_field("Título", content),
        "fecha": get_field("Fecha", content),
        "categoria": get_field("Categoría", content),
        "meta": get_field("Meta-Descripción", content),
        "imagen": get_field("Imagen", content),
        "cuerpo": get_field("Cuerpo", content, dotall=True),
        "fuentes": get_field("Fuentes", content, dotall=True)
    }
    return data

def apply_format(text):
    """Aplica negritas y resaltado de frases impactantes"""
    # Formatear párrafos
    paragraphs = text.split('\n\n')
    formatted = ""
    for p in paragraphs:
        p = p.strip()
        if p:
            # Resaltar frases entre comillas y negrita: "frase" -> <b>"frase"</b>
            p = re.sub(r'\"(.*?)\"', r'<b>"\1"</b>', p)
            # Detectar subtítulos (líneas cortas sin punto final)
            if len(p) < 80 and not p.endswith('.') and not p.endswith(':'):
                formatted += f"<h3 class='article-subtitle'>{p}</h3>"
            else:
                formatted += f"<p class='article-paragraph'>{p}</p>"
    return formatted

def generate_html(data, lang="es"):
    """Genera el HTML final con la estética ProDig (Material Design)"""
    slug = create_slug(data['titulo'])
    canonical_url = f"https://aiprodig.com/blog/{slug}" if lang=="es" else f"https://aiprodig.com/en/blog/{slug}"
    alt_lang_url = f"https://aiprodig.com/en/blog/{slug}" if lang=="es" else f"https://aiprodig.com/blog/{slug}"
    alt_lang = "en" if lang=="es" else "es"
    
    # Google Analytics ID
    ga_id = "G-G5Z4R6W8NX" 

    html_template = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{data['meta']}">
    <title>{data['titulo']} | ProDig Blog</title>
    
    <!-- SEO & Canonical -->
    <link rel="canonical" href="{canonical_url}">
    <link rel="alternate" hreflang="{alt_lang}" href="{alt_lang_url}">
    
    <!-- Fonts & Styles -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #000000;
            --accent: #2563eb;
            --text-main: #1f2937;
            --text-secondary: #4b5563;
            --bg-body: #ffffff;
            --bg-card: #f9fafb;
        }}
        
        body {{
            font-family: 'Outfit', sans-serif;
            line-height: 1.6;
            color: var(--text-main);
            margin: 0;
            padding: 0;
            background: var(--bg-body);
        }}
        
        .article-container {{
            max-width: 800px;
            margin: 4rem auto;
            padding: 0 1.5rem;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        
        .category-tag {{
            background: var(--accent);
            color: white;
            padding: 0.25rem 1rem;
            border-radius: 99px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .date {{
            color: var(--text-secondary);
            margin-top: 1rem;
            font-size: 0.9rem;
        }}
        
        .main-title {{
            font-size: 2.5rem;
            line-height: 1.2;
            margin: 1.5rem 0;
            font-weight: 600;
        }}
        
        .hero-image {{
            width: 100%;
            height: auto;
            border-radius: 12px;
            margin-bottom: 3rem;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
        }}
        
        .article-body {{
            font-size: 1.15rem;
            color: var(--text-main);
            margin-bottom: 4rem;
        }}
        
        .article-subtitle {{
            font-size: 1.8rem;
            margin-top: 3rem;
            margin-bottom: 1.5rem;
            font-weight: 600;
        }}
        
        .article-paragraph {{
            margin-bottom: 1.5rem;
        }}
        
        b, strong {{
            font-weight: 600;
        }}
        
        .sources {{
            background: var(--bg-card);
            padding: 2rem;
            border-radius: 8px;
            margin-bottom: 4rem;
            border-left: 4px solid var(--accent);
        }}
        
        .interaction-footer {{
            border-top: 1px solid #eee;
            padding-top: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .btn-share {{
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            border: 1px solid #eee;
            background: white;
            cursor: pointer;
            font-family: inherit;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            text-decoration: none;
            color: var(--text-main);
            font-size: 0.9rem;
        }}
        
        .btn-share:hover {{
            background: #f3f4f6;
            transform: translateY(-2px);
        }}
        
        .whatsapp-float {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #25d366;
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 2px 2px 3px #999;
            z-index: 100;
            text-decoration: none;
        }}
    </style>
    
    <!-- GA4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{ga_id}');
    </script>
</head>
<body>
    <main class="article-container">
        <header>
            <span class="category-tag">{data['categoria']}</span>
            <p class="date">{data['fecha']}</p>
            <h1 class="main-title">{data['titulo']}</h1>
        </header>
        
        <img src="/blog/images/{data['imagen']}" alt="{data['titulo']}" class="hero-image">
        
        <article class="article-body">
            {apply_format(data['cuerpo'])}
        </article>
        
        <section class="sources">
            <h4>Fuentes y Referencias:</h4>
            <div class="sources-list">{apply_format(data['fuentes'])}</div>
        </section>
        
        <footer class="interaction-footer">
            <div class="interaction-buttons">
                <button class="btn-share" onclick="alert('¡Gracias por tu apoyo!')">❤️ Me gusta</button>
            </div>
            <div class="share-buttons" style="display:flex; gap: 0.5rem;">
                <a href="https://www.linkedin.com/sharing/share-offsite/?url={canonical_url}" class="btn-share" target="_blank">LinkedIn</a>
                <a href="https://twitter.com/intent/tweet?url={canonical_url}&text={data['titulo']}" class="btn-share" target="_blank">X</a>
                <a href="https://wa.me/?text={data['titulo']}%20{canonical_url}" class="btn-share" target="_blank">WhatsApp</a>
            </div>
        </footer>
    </main>

    <a href="https://wa.me/573144897092" class="whatsapp-float" target="_blank">
        <span style="font-size: 24px">WP</span>
    </a>
</body>
</html>"""
    return html_template

def publish(article_num):
    file_name = f"articulo{article_num}.txt"
    path = os.path.join(ARTICULOS_DIR, file_name)
    
    if not os.path.exists(path):
        # Intentar sin tilde
        path = os.path.join("Blog/articulos/", file_name)

    if os.path.exists(path):
        data = parse_txt(path)
        
        # Generar Versión ES
        html_es = generate_html(data, "es")
        slug_es = create_slug(data['titulo'])
        
        es_path = os.path.join(OUTPUT_ES, f"{slug_es}.html")
        with open(es_path, "w", encoding="utf-8") as f:
            f.write(html_es)
            
        if not os.path.exists(OUTPUT_EN): os.makedirs(OUTPUT_EN)
        
        print(f"✅ Artículo {article_num} generado en ES: {es_path}")
        return data, slug_es
    else:
        print(f"❌ Error: No se encontró {path}")
        return None, None

if __name__ == "__main__":
    import sys
    num = sys.argv[1] if len(sys.argv) > 1 else input("Número de artículo: ")
    publish(num)