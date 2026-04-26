# PROTOCOLO DE REINGENIERÍA Y AUTOMATIZACIÓN: BLOG PRODIG v2.0

## 1. VISIÓN ESTRATÉGICA
El blog no es solo un repositorio de artículos, es el motor de autoridad para la "Gran Convergencia" (Del Bit al Átomo). Debe reflejar la metodología MDDC (Metodología de Desarrollo Dirigida por Contexto) y estar optimizado para una audiencia global (Español e Inglés).

## 2. ESTRUCTURA DE URLS (REINGENIERÍA)
Para evitar la fragmentación en Analytics, se unifican las rutas bajo minúsculas y sin extensiones .html visibles:

- **Home Blog (ES):** `aiprodig.com/blog`
- **Home Blog (EN):** `aiprodig.com/en/blog`
- **Artículos (ES):** `aiprodig.com/blog/[slug-titulo-articulo]`
- **Artículos (EN):** `aiprodig.com/en/blog/[slug-title-article]`
- **Recursos:** `aiprodig.com/blog/images/` | `aiprodig.com/blog/articulos/`

## 3. ORGANIZACIÓN DE ARCHIVOS FUENTE
- `/articulos/articulo[N].txt`: Contiene la metadata y cuerpo.
- `/images/imagen[N].jpg`: Imagen principal del post.

**Estructura del archivo .txt:**
- Título: [Título del post]
- Fecha: [DD/MM/AAAA]
- Categoría: [IA-Empresas | IA-Tecnología | IA-Automatización | IA-Media]
- Meta-Descripción: [Resumen para SEO]
- Imagen: [imagenN.jpg]
- Cuerpo: [Texto completo]
- Fuentes: [Lista de links]

## 4. SISTEMA DE PROCESAMIENTO (SCRIPT PYTHON)
Al activar el comando de publicación (Activador: "45" en el chat), el script ejecutará:

1. **Traducción Contextual:** Generar la versión en inglés manteniendo el tono experto y técnico de ProDig.
2. **Generación de Slugs:** Crear URLs amigables basadas en el título.
3. **Inyección de Componentes:**
   - Script de Google Analytics 4.
   - Botones de "Me Gusta" y "Compartir" (LinkedIn, X, WhatsApp).
   - Botón de WhatsApp flotante (+57 314 489 7092).
   - Modal de contacto integrado con Formspree.
4. **Despliegue:** Realizar `git add`, `commit` y `push` automático a GitHub para actualización vía Vercel/Cloudflare.

## 5. ESTÁNDAR DE DISEÑO DE PÁGINA DE ARTÍCULO (ÚNICO Y CONSISTENTE)
Todas las páginas de artículo DEBEN seguir el formato visual del artículo de referencia: https://aiprodig.com/Blog/el-activo-invisible-por-que-su-empresa-es-mas-pobre-de-lo-que-dicen-sus-libros-contables

**Componentes obligatorios:**
1. **Header:** `<header class="article-header">` con canvas de partículas (#bg-canvas), `.header-content`, `.category-tag`, `.main-title` (2.8rem, font-weight 700), `.date`.
2. **Contenedor:** `.article-container` (max-width 800px, centrado).
3. **Imagen hero:** `.hero-image` (border-radius 20px, margin-top -3.5rem, z-index 10, box-shadow 0 20px 40px).
4. **Cuerpo:** `.article-body` con `.article-subtitle` para h2 y `.article-paragraph` para párrafos.
5. **Fuentes:** `.sources` (background #f1f5f9, padding 2rem, border-radius 16px, border-left 6px solid var(--accent)).
6. **Navegación:** `.post-nav` con `.nav-btn` (Anterior/Siguiente) y `.back-home` (botón home circular).
7. **Footer interactivo:** `.interaction-footer` con botón like, botones LinkedIn y WhatsApp.
8. **WhatsApp flotante:** `.whatsapp-float` (bottom 30px, right 30px, background #25d366).
9. **Script de likes:** Integración con InsForge API (`/get-stats` y `/handle-likes`).

**CSS Variables obligatorias:**
```css
:root {
    --primary: #0f172a;
    --accent: #2563eb;
    --text-main: #334155;
    --bg-header: #f8fafc;
}
```

**Meta tags obligatorios:**
- `canonical` apuntando a la versión sin .html
- `alternate hreflang="en"` apuntando a la versión en inglés
- Google Fonts: Outfit (300, 400, 600, 700)
- Font Awesome 6.0.0

**NOTA:** El publisher.py DEBE generar TODOS los artículos con este formato exacto. Los artículos con estilos antiguos (header fijo con nav, fuente Segoe UI, footer con logo, etc.) deben ser re-generados.

## 5.1. ETIQUETA "NUEVO" EN TARJETAS DE ARTÍCULOS
- Al publicar un nuevo artículo, el publisher.py DEBE agregar la etiqueta "Nuevo" al primer artículo de las tarjetas del home (index.html principal).
- La etiqueta se implementa como un badge rojo con estilo: `background: #ef4444; color: white; font-size: 0.7rem; font-weight: 800; padding: 0.3rem 0.8rem; border-radius: 99px; z-index: 5; text-transform: uppercase;`.
- La etiqueta se posiciona en la esquina superior izquierda de la tarjeta.
- La etiqueta "Nuevo" solo debe aparecer en el artículo más reciente de las tarjetas del home principal (index.html). El home del blog (Blog/index.html) y el article body NO llevan esta etiqueta.

## 6. METODOLOGÍA DE DESARROLLO (MDDC)
Cada artículo generado debe servir como un activo de contexto. El sistema debe asegurar que las etiquetas `canonical` estén correctamente puestas para que la versión en inglés y español se reconozcan como traducciones mutuas y no contenido duplicado.