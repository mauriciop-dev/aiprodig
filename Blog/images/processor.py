import os
import re
import html
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS ---
ARTICULOS_DIR = "Blog/artículos/"
# Intentar encontrar el directorio correcto si hay diferencias en mayúsculas/minúsculas
if not os.path.exists(ARTICULOS_DIR):
    ARTICULOS_DIR = "Blog/articulos/"

IMAGES_DIR = "Blog/images/"
IMG_PATH_URL = "/Blog/images/"
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
    """Extrae la metadata y el cuerpo del archivo .txt con alta flexibilidad"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def get_field(patterns, text, dotall=False):
        for pattern in patterns:
            regex = f"^{pattern}.*?:\\s*(.*?)(?=\\n[\\w\\s]+:|$)"
            match = re.search(regex, text, (re.DOTALL if dotall else 0) | re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""

    data = {
        "titulo": get_field(["Título del artículo", "Título", "Titulo"], content),
        "fecha": get_field(["Fecha de publicación", "Fecha"], content),
        "categoria": get_field(["Categoría", "Categoria"], content),
        "meta": get_field(["Meta descripción", "Meta-Descripción", "Meta"], content),
        "imagen": get_field(["Imagen"], content),
        "cuerpo": get_field(["Cuerpo del artículo", "Cuerpo"], content, dotall=True),
        "fuentes": get_field(["Fuentes"], content, dotall=True)
    }
    return data

def apply_format(text):
    """Aplica negritas y resaltado de frases impactantes"""
    paragraphs = text.split('\n\n')
    formatted = ""
    for p in paragraphs:
        p = p.strip()
        if p:
            p = re.sub(r'\"(.*?)\"', r'<b>"\1"</b>', p)
            if len(p) < 80 and not p.endswith('.') and not p.endswith(':'):
                formatted += f"<h3 class='article-subtitle'>{p}</h3>"
            else:
                formatted += f"<p class='article-paragraph'>{p}</p>"
    return formatted

def generate_html(data, lang="es", prev_article=None, next_article=None):
    """Genera el HTML final con navegación Entre artículos (Siguiente/Anterior)"""
    slug = create_slug(data['titulo'])
    canonical_url = f"https://aiprodig.com/Blog/{slug}" if lang=="es" else f"https://aiprodig.com/en/blog/{slug}"
    alt_lang_url = f"https://aiprodig.com/en/blog/{slug}" if lang=="es" else f"https://aiprodig.com/Blog/{slug}"
    alt_lang = "en" if lang=="es" else "es"
    
    # Textos según idioma
    txt_likes = "Me gusta" if lang=="es" else "Likes"
    txt_sources = "Fuentes y Referencias:" if lang=="es" else "Sources & References:"
    txt_back = "Volver al Blog" if lang=="es" else "Back to Blog"
    txt_prev = "Anterior" if lang=="es" else "Previous"
    txt_next = "Siguiente" if lang=="es" else "Next"

    # Construcción de navegación
    prev_html = f'<a href="{prev_article["slug"]}.html" class="nav-btn"><span>&larr; {txt_prev}</span><small>{prev_article["titulo"][:30]}...</small></a>' if prev_article else '<div></div>'
    next_html = f'<a href="{next_article["slug"]}.html" class="nav-btn text-right"><span>{txt_next} &rarr;</span><small>{next_article["titulo"][:30]}...</small></a>' if next_article else '<div></div>'

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
    
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        :root {{
            --primary: #000000;
            --accent: #2563eb;
            --text-main: #1f2937;
            --text-secondary: #4b5563;
            --bg-body: #ffffff;
            --bg-card: #f9fafb;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Outfit', sans-serif; line-height: 1.6; color: var(--text-main); background: var(--bg-body); overflow-x: hidden; }}
        
        /* Header Animado */
        .article-header {{ position: relative; padding: 8rem 2rem; text-align: center; background: #000; color: white; }}
        #bg-canvas {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.4; }}
        .header-content {{ position: relative; z-index: 2; max-width: 900px; margin: 0 auto; }}
        .category-tag {{ background: var(--accent); color: white; padding: 0.3rem 1.2rem; border-radius: 99px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }}
        .main-title {{ font-size: 3rem; margin: 1.5rem 0; font-weight: 700; }}

        /* Contenido */
        .article-container {{ max-width: 850px; margin: 0 auto; padding: 0 1.5rem 4rem; }}
        .hero-image {{ width: 100%; height: auto; border-radius: 20px; margin-top: -5rem; position: relative; z-index: 10; box-shadow: 0 20px 40px rgba(0,0,0,0.2); }}
        .article-body {{ font-size: 1.2rem; color: var(--text-main); margin-top: 4rem; }}
        .article-subtitle {{ font-size: 1.8rem; margin: 3rem 0 1.5rem; font-weight: 700; }}
        
        /* Navegación Inferior */
        .post-nav {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 1rem;
            align-items: center;
            margin: 5rem 0;
            padding: 2rem 0;
            border-top: 1px solid #eee;
            border-bottom: 1px solid #eee;
        }}
        
        .nav-btn {{
            text-decoration: none;
            color: var(--text-main);
            display: flex;
            flex-direction: column;
            transition: all 0.3s;
        }}
        
        .nav-btn span {{ font-weight: 700; font-size: 0.9rem; color: var(--accent); text-transform: uppercase; }}
        .nav-btn small {{ color: var(--text-secondary); font-size: 0.85rem; margin-top: 4px; }}
        .nav-btn:hover {{ transform: translateY(-3px); opacity: 0.8; }}
        .text-right {{ text-align: right; }}
        
        .back-blog {{
            width: 40px; height: 40px; border-radius: 50%; background: #f0f0f0;
            display: flex; align-items: center; justify-content: center; color: #666;
            text-decoration: none; transition: background 0.3s;
        }}
        .back-blog:hover {{ background: var(--accent); color: white; }}

        /* Interaction Footer */
        .interaction-footer {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 2rem; }}
        .btn-action {{ padding: 0.8rem 1.2rem; border-radius: 12px; border: 1px solid #ddd; background: white; cursor: pointer; text-decoration: none; color: inherit; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }}
        .btn-like.active {{ background: #fee2e2; color: #dc2626; border-color: #f87171; }}
        
        .whatsapp-float {{ position: fixed; bottom: 30px; right: 30px; background: #25d366; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); z-index: 1000; transition: transform 0.3s; }}
        .whatsapp-float:hover {{ transform: scale(1.1); }}

        @media (max-width: 600px) {{
            .main-title {{ font-size: 2rem; }}
            .post-nav {{ grid-template-columns: 1fr; text-align: center; }}
            .back-blog {{ margin: 0 auto; }}
            .text-right {{ text-align: center; }}
        }}
    </style>
</head>
<body>
    <header class="article-header">
        <canvas id="bg-canvas"></canvas>
        <div class="header-content">
            <span class="category-tag">{data['categoria']}</span>
            <h1 class="main-title">{data['titulo']}</h1>
            <p>{data['fecha']}</p>
        </div>
    </header>

    <main class="article-container">
        <img src="{IMG_PATH_URL}{data['imagen']}" alt="{data['titulo']}" class="hero-image">
        
        <article class="article-body">
            {apply_format(data['cuerpo'])}
        </article>

        <!-- Navegación -->
        <nav class="post-nav">
            {prev_html}
            <a href="/Blog" class="back-blog" title="{txt_back}"><i class="fa-solid fa-grid-2"></i><i class="fa-solid fa-house"></i></a>
            {next_html}
        </nav>
        
        <footer class="interaction-footer">
            <button id="likeBtn" class="btn-action btn-like">
                <i class="fa-solid fa-heart"></i> <span id="likeCount">0</span> {txt_likes}
            </button>
            <div style="display:flex; gap:1rem;">
                <a href="https://www.linkedin.com/sharing/share-offsite/?url={canonical_url}" class="btn-action" target="_blank"><i class="fab fa-linkedin"></i></a>
                <a href="https://wa.me/?text={data['titulo']}%20{canonical_url}" class="btn-action" target="_blank"><i class="fab fa-whatsapp"></i></a>
            </div>
        </footer>
    </main>

    <a href="https://wa.me/573144897092" class="whatsapp-float" target="_blank"><i class="fab fa-whatsapp"></i></a>

    <script>
        // Animación de partículas
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        function init() {{
            canvas.width = window.innerWidth; canvas.height = canvas.parentElement.offsetHeight;
            particles = [];
            for(let i=0; i<60; i++) particles.push({{x:Math.random()*canvas.width, y:Math.random()*canvas.height, vx:(Math.random()-0.5), vy:(Math.random()-0.5)}});
        }}
        function draw() {{
            ctx.clearRect(0,0,canvas.width, canvas.height);
            ctx.fillStyle = 'rgba(255,255,255,0.4)';
            ctx.strokeStyle = 'rgba(255,255,255,0.1)';
            particles.forEach((p,i) => {{
                p.x+=p.vx; p.y+=p.vy;
                if(p.x<0||p.x>canvas.width) p.vx*=-1; if(p.y<0||p.y>canvas.height) p.vy*=-1;
                ctx.beginPath(); ctx.arc(p.x,p.y,2,0,Math.PI*2); ctx.fill();
                for(let j=i+1; j<particles.length; j++) {{
                    let p2 = particles[j]; let d = Math.hypot(p.x-p2.x, p.y-p2.y);
                    if(d<100) {{ ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(p2.x,p2.y); ctx.stroke(); }}
                }}
            }});
            requestAnimationFrame(draw);
        }}
        window.onresize = init; init(); draw();

        // Likes persistent
        const aid = "{slug}";
        const lbtn = document.getElementById('likeBtn');
        const lcnt = document.getElementById('likeCount');
        let count = parseInt(localStorage.getItem('L_'+aid)) || Math.floor(Math.random()*20)+5;
        let liked = localStorage.getItem('H_'+aid) === 'Y';
        function up() {{ lcnt.innerText = count; lbtn.className = liked ? 'btn-action btn-like active' : 'btn-action btn-like'; }}
        lbtn.onclick = () => {{ if(liked) count--; else count++; liked=!liked; localStorage.setItem('L_'+aid, count); localStorage.setItem('H_'+aid, liked?'Y':'N'); up(); }};
        up();
    </script>
</body>
</html>"""
    return html_template

def get_adj(num):
    """Obtiene info del artículo anterior y siguiente"""
    prev_info = None
    next_info = None
    
    # Anterior
    p_path = os.path.join(ARTICULOS_DIR, f"articulo{num-1}.txt")
    p_data = parse_txt(p_path)
    if p_data: prev_info = {"titulo": p_data['titulo'], "slug": create_slug(p_data['titulo'])}
    
    # Siguiente
    n_path = os.path.join(ARTICULOS_DIR, f"articulo{num+1}.txt")
    n_data = parse_txt(n_path)
    if n_data: next_info = {"titulo": n_data['titulo'], "slug": create_slug(n_data['titulo'])}
    
    return prev_info, next_info

def publish(article_num):
    article_num = int(article_num)
    file_name = f"articulo{article_num}.txt"
    path = os.path.join(ARTICULOS_DIR, file_name)

    if os.path.exists(path):
        data = parse_txt(path)
        prev_info, next_info = get_adj(article_num)
        
        # ES
        html_es = generate_html(data, "es", prev_info, next_info)
        slug_es = create_slug(data['titulo'])
        with open(os.path.join(OUTPUT_ES, f"{slug_es}.html"), "w", encoding="utf-8") as f:
            f.write(html_es)
        print(f"ES: {slug_es}.html")
        return data, slug_es
    return None, None

if __name__ == "__main__":
    import sys
    num = sys.argv[1] if len(sys.argv) > 1 else input("Article number: ")
    publish(num)