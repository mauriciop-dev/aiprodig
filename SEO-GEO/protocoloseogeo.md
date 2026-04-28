# PROTOCOLO DE DESPLIEGUE: SEO & GEO (Generative Engine Optimization)

Este documento contiene las reglas obligatorias para la generación y actualización de activos de visibilidad en cada despliegue de este proyecto.

## 1. Sitemap (sitemap.xml)
**Objetivo:** Permitir que los motores de búsqueda tradicionales indexen todas las rutas.
- **Acción:** En cada despliegue, el script de build debe generar un archivo `public/sitemap.xml`.
- **Contenido:** Debe incluir la URL base y todas las rutas dinámicas detectadas en el sistema de archivos o base de datos.
- **Prioridad:** 1.0 para la home, 0.8 para servicios/productos y 0.6 para artículos de blog.

## 2. Contexto para Modelos de Lenguaje (llms.txt)
**Objetivo:** Proporcionar una "Fuente de Verdad" resumida para que agentes de IA (Gemini, Claude, GPT) comprendan el sitio.
- **Acción:** Mantener un archivo `public/llms.txt` en formato Markdown plano.
- **Ver archivo:** se genero el archivo llms.txt en la carpeta /SEO-GEO

## 3. Datos Estructurados (JSON-LD)
**Objetivo:** Definir explícitamente el tipo de contenido para los buscadores (GEO).
- **Acción:** Revisar e inyectar en el `<head>` de las páginas principales el script `application/ld+json`.
- **Esquemas Requeridos:**
    - **WebSite:** Para la home.
    - **Organization:** Detallando nombre, logo y redes sociales.
    - **Product/Service:** Específico para las páginas de oferta (ej: PAIC o NexoSalud).
    - **Article:** Para las entradas del blog (incluyendo autor y fecha de publicación).

## 4. Meta Tags (SEO Tradicional)
**Objetivo:** Optimización para motores de búsqueda tradicionales (Google, Bing) y redes sociales.
- **Acción:** Cada página debe incluir en el `<head>`:
  - `<title>` - Máximo 60 caracteres
  - `<meta name="description">` - Máximo 160 caracteres
  - `<meta name="keywords">` - Palabras clave relevantes
  - Open Graph tags (og:title, og:description, og:image, og:url)
  - Twitter Card tags
- **Validación:** Pre-deploy validar límites de caracteres (title ≤60, description ≤160)
- **Actualización:** Al crear/actualizar páginas, regenerar estas meta tags

## 5. Convenciones SEO-GEO para Automatización
**Objetivo:** Permitir que el script seo_generator.py extraiga metadatos automáticamente.

### 5.1 Meta tags en HTML (prefijos seo-)
Cada página debe incluir en el `<head>`:
```html
<meta name="seo-title" content="Título de la página - hasta 60 caracteres">
<meta name="seo-description" content="Descripción - hasta 160 caracteres">
<meta name="seo-keywords" content="palabra1, palabra2, palabra3">
<meta name="seo-type" content="website|article|service|product">
<meta name="seo-priority" content="1.0|0.8|0.6|0.3">
<meta name="seo-section" content="home|blog|services|products|legal">
<meta name="seo-lang" content="es|en">
```

### 5.2 Open Graph (og-)
```html
<meta property="og:title" content="Título para redes">
<meta property="og:description" content="Descripción para compartir">
<meta property="og:image" content="https://dominio.com/images/og-image.jpg">
<meta property="og:url" content="https://dominio.com/pagina.html">
```

### 5.3 JSON-LD automático
El script genera automáticamente el schema basándose en seo-type:
- **website:** → WebSite + Organization
- **article:** → Article + Person
- **service:** → Service + Organization
- **product:** → Product + Organization

## 6. Script de Automatización (seo_generator.py)
**Ubicación:** `/SEO-GEO/seo_generator.py`

**Uso:**
```bash
python SEO-GEO/seo_generator.py
```

**Funciones:**
1. Escanea todos los archivos .html del proyecto
2. Extrae metadatos de meta tags seo-* 
3. Genera sitemap.xml con prioridades
4. Genera llms.txt con contexto para IAs
5. Valida límites de caracteres (title ≤60, description ≤160)

**Ejecución automática:**
- Pre-deploy: `python SEO-GEO/seo_generator.py`
- O configurar en package.json: `"seo": "python SEO-GEO/seo_generator.py"`

## 7. Plantilla estándar
Todas las páginas nuevas deben usar: `/SEO-GEO/template.html`

## 8. Workflow completo
1. Crear nueva página usando template.html
2. Completar meta tags seo-* con contenido real
3. Ejecutar `python SEO-GEO/seo_generator.py`
4. Verificar sitemap.xml y llms.txt generados

---
*Nota: Este protocolo es propiedad de ProDig (Prospectiva Digital). Al realizar cambios en el código, asegúrate de que estos archivos se sincronicen con las nuevas rutas creadas.*