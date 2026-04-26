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

## 5. DISEÑO Y FORMATO (UI/UX)
- **Estética:** Mantener el estilo "Material Design" de ProDig (Limpio, profesional, fuentes Google Sans/Arial).
- **Home del Blog:** - Título: "BLOG AIPRODIG".
    - Layout: Dos columnas de tarjetas verticales.
    - Tarjeta: Imagen pequeña, Título (Size 10), Meta-descripción y Etiqueta de Categoría.
- **Página de Artículo:**
    - Título centrado, Fecha de publicación y Categoría visible.
    - Imagen proporcionada al ancho del texto.
    - Cuerpo: Párrafos claros, subtítulos en negrilla, frases impactantes resaltadas en **"comillas y negrilla"**.
    - Footer: Sección de fuentes, botones sociales y CTA de contacto.

## 5.1. ETIQUETA "NUEVO" EN TARJETAS DE ARTÍCULOS
- Al publicar un nuevo artículo, el publisher.py DEBE agregar la etiqueta "Nuevo" al primer artículo de las tarjetas del home (index.html principal).
- La etiqueta se implementa como un badge rojo con estilo: `background: #ef4444; color: white; font-size: 0.7rem; font-weight: 800; padding: 0.3rem 0.8rem; border-radius: 99px; z-index: 5; text-transform: uppercase;`.
- La etiqueta se posiciona en la esquina superior izquierda de la tarjeta.
- La etiqueta "Nuevo" solo debe aparecer en el artículo más reciente de las tarjetas del home principal (index.html). El home del blog (Blog/index.html) y el article body NO llevan esta etiqueta.

## 6. METODOLOGÍA DE DESARROLLO (MDDC)
Cada artículo generado debe servir como un activo de contexto. El sistema debe asegurar que las etiquetas `canonical` estén correctamente puestas para que la versión en inglés y español se reconozcan como traducciones mutuas y no contenido duplicado.