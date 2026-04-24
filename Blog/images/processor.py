import os
import re
import html
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS ---
ARTICULOS_DIR = "Blog/artículos/"
IMAGES_DIR = "Blog/images/"
# Usamos rutas absolutas para las imágenes para evitar errores de case-sensitivity
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
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def get_field(patterns, text, dotall=False):
        for pattern in patterns:
            # Búsqueda más flexible que permite cualquier combinación de caracteres antes del :
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

def generate_html(data, lang="es"):
    """Genera el HTML final con la estética ProDig (Premium)"""
    slug = create_slug(data['titulo'])
    canonical_url = f"https://aiprodig.com/Blog/{slug}" if lang=="es" else f"https://aiprodig.com/en/blog/{slug}"
    alt_lang_url = f"https://aiprodig.com/en/blog/{slug}" if lang=="es" else f"https://aiprodig.com/Blog/{slug}"
    alt_lang = "en" if lang=="es" else "es"
    
    # Textos según idioma
    txt_likes = "Me gusta" if lang=="es" else "Likes"
    txt_sources = "Fuentes y Referencias:" if lang=="es" else "Sources & References:"
    txt_back = "Volver al Blog" if lang=="es" else "Back to Blog"

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
        body {{ font-family: 'Outfit', sans-serif; line-height: 1.6; color: var(--text-main); background: var(--bg-body); }}
        
        /* Header con Animación Materia Programable */
        .article-header {{
            position: relative;
            padding: 8rem 2rem 4rem;
            text-align: center;
            background: #000;
            color: white;
            overflow: hidden;
        }}
        
        #bg-canvas {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.4;
        }}
        
        .header-content {{ position: relative; z-index: 2; max-width: 900px; margin: 0 auto; }}
        
        .category-tag {{
            background: var(--accent);
            color: white;
            padding: 0.3rem 1.2rem;
            border-radius: 99px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}
        
        .main-title {{ font-size: 3rem; margin: 1.5rem 0; font-weight: 700; line-height: 1.1; }}
        .date {{ opacity: 0.7; font-size: 0.9rem; }}

        /* Contenido */
        .article-container {{ max-width: 850px; margin: 0 auto; padding: 4rem 1.5rem; }}
        
        .hero-image {{
            width: 100%;
            height: auto;
            border-radius: 20px;
            margin-top: -6rem;
            position: relative;
            z-index: 10;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
            background: #eee;
        }}
        
        .article-body {{ font-size: 1.2rem; color: var(--text-main); margin-top: 4rem; }}
        .article-subtitle {{ font-size: 1.8rem; margin: 3rem 0 1.5rem; font-weight: 700; color: #000; }}
        .article-paragraph {{ margin-bottom: 1.8rem; }}
        b {{ font-weight: 700; color: #000; }}
        
        .sources {{
            background: var(--bg-card);
            padding: 2.5rem;
            border-radius: 16px;
            margin: 4rem 0;
            border-left: 5px solid var(--accent);
        }}
        
        /* Footer de Interacción */
        .interaction-footer {{
            border-top: 1px solid #eee;
            padding-top: 3rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 2rem;
        }}
        
        .like-container {{ display: flex; align-items: center; gap: 1rem; }}
        
        .btn-action {{
            padding: 0.8rem 1.5rem;
            border-radius: 12px;
            border: 1px solid #ddd;
            background: white;
            cursor: pointer;
            font-family: inherit;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            text-decoration: none;
            color: var(--text-main);
            font-weight: 600;
        }}
        
        .btn-action:hover {{ background: #f8f9fa; transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }}
        .btn-like.active {{ background: #fee2e2; border-color: #f87171; color: #dc2626; }}
        
        .share-group {{ display: flex; gap: 0.8rem; }}
        
        /* WhatsApp Floating */
        .whatsapp-float {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #25d366;
            color: white;
            width: 65px;
            height: 65px;
            border-radius: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 25px rgba(37, 211, 102, 0.3);
            z-index: 1000;
            text-decoration: none;
            font-size: 32px;
            transition: transform 0.3s;
        }}
        .whatsapp-float:hover {{ transform: scale(1.1) rotate(10deg); }}

        @media (max-width: 768px) {{
            .main-title {{ font-size: 2.2rem; }}
            .hero-image {{ margin-top: -3rem; }}
        }}
    </style>
</head>
<body>
    <header class="article-header">
        <canvas id="bg-canvas"></canvas>
        <div class="header-content">
            <span class="category-tag">{data['categoria']}</span>
            <h1 class="main-title">{data['titulo']}</h1>
            <p class="date">{data['fecha']}</p>
        </div>
    </header>

    <main class="article-container">
        <img src="{IMG_PATH_URL}{data['imagen']}" alt="{data['titulo']}" class="hero-image">
        
        <article class="article-body">
            {apply_format(data['cuerpo'])}
        </article>
        
        <section class="sources">
            <h4>{txt_sources}</h4>
            <div style="margin-top: 1rem;">{apply_format(data['fuentes'])}</div>
        </section>
        
        <footer class="interaction-footer">
            <div class="like-container">
                <button id="likeBtn" class="btn-action btn-like">
                    <i class="fa-solid fa-heart"></i>
                    <span>{txt_likes}</span>
                    <span id="likeCount">0</span>
                </button>
            </div>
            
            <div class="share-group">
                <a href="https://www.linkedin.com/sharing/share-offsite/?url={canonical_url}" class="btn-action" target="_blank"><i class="fab fa-linkedin"></i></a>
                <a href="https://twitter.com/intent/tweet?url={canonical_url}" class="btn-action" target="_blank"><i class="fab fa-x-twitter"></i></a>
                <a href="https://wa.me/?text={data['titulo']}%20{canonical_url}" class="btn-action" target="_blank"><i class="fab fa-whatsapp"></i></a>
            </div>
        </footer>
        
        <div style="margin-top: 4rem; text-align: center;">
            <a href="/Blog" style="text-decoration: none; color: var(--accent); font-weight: 600;">&larr; {txt_back}</a>
        </div>
    </main>

    <a href="https://wa.me/573144897092" class="whatsapp-float" target="_blank">
        <i class="fab fa-whatsapp"></i>
    </a>

    <!-- Scripts de Funcionalidad -->
    <script>
        // --- ANIMACIÓN FONDO (MATERIA PROGRAMABLE) ---
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        function initCanvas() {{
            canvas.width = window.innerWidth;
            canvas.height = canvas.parentElement.offsetHeight;
            particles = [];
            for (let i = 0; i < 80; i++) {{
                particles.push({{
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 0.5,
                    vy: (Math.random() - 0.5) * 0.5,
                    size: Math.random() * 2 + 1
                }});
            }}
        }}

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
            
            particles.forEach((p, i) => {{
                p.x += p.vx;
                p.y += p.vy;
                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
                
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();
                
                for (let j = i + 1; j < particles.length; j++) {{
                    const p2 = particles[j];
                    const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                    if (dist < 100) {{
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.stroke();
                    }}
                }}
            }});
            requestAnimationFrame(animate);
        }}

        window.addEventListener('resize', initCanvas);
        initCanvas();
        animate();

        // --- CONTADOR DE LIKES (PERSISTENCIA LOCAL) ---
        const articleId = "{slug}";
        const likeBtn = document.getElementById('likeBtn');
        const likeCountEl = document.getElementById('likeCount');
        
        // Simulación de persistencia (en producción usaría una DB real)
        let likes = parseInt(localStorage.getItem('likes_' + articleId)) || Math.floor(Math.random() * 50) + 10;
        let hasLiked = localStorage.getItem('hasLiked_' + articleId) === 'true';

        function updateUI() {{
            likeCountEl.textContent = likes;
            if (hasLiked) likeBtn.classList.add('active');
            else likeBtn.classList.remove('active');
        }}

        likeBtn.onclick = () => {{
            if (!hasLiked) {{
                likes++;
                hasLiked = true;
            }} else {{
                likes--;
                hasLiked = false;
            }}
            localStorage.setItem('likes_' + articleId, likes);
            localStorage.setItem('hasLiked_' + articleId, hasLiked);
            updateUI();
        }};
        
        updateUI();
    </script>
</body>
</html>"""
    return html_template

def publish(article_num):
    file_name = f"articulo{article_num}.txt"
    path = os.path.join(ARTICULOS_DIR, file_name)
    if not os.path.exists(path): path = os.path.join("Blog/articulos/", file_name)

    if os.path.exists(path):
        data = parse_txt(path)
        # ES
        html_es = generate_html(data, "es")
        slug_es = create_slug(data['titulo'])
        with open(os.path.join(OUTPUT_ES, f"{slug_es}.html"), "w", encoding="utf-8") as f:
            f.write(html_es)
        print(f"Generated ES Version: {slug_es}.html")
        return data, slug_es
    else:
        print(f"File {path} not found.")
        return None, None

if __name__ == "__main__":
    import sys
    num = sys.argv[1] if len(sys.argv) > 1 else input("Article number: ")
    publish(num)