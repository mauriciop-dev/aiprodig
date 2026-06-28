# Plan de Implementación de Optimización SEO + GEO para aiprodig.com

Este plan detalla la implementación de las mejoras técnicas y semánticas indicadas en el documento de auditoría de SEO + GEO de aiprodig.com, con el fin de corregir los fallos de rastreo, mejorar la velocidad (Core Web Vitals), optimizar la semántica HTML5 y construir un grafo de conocimiento completo de entidades (Entity Linking) mediante JSON-LD estructurado, garantizando una visibilidad premium en motores de búsqueda tradicionales y modelos de IA generativa (Gemini, Claude, ChatGPT, Perplexity).

## User Review Required

> [!IMPORTANT]
> **Datos de Reseñas y Testimonios:** La auditoría sugiere un esquema `AggregateRating` para la organización. Para evitar penalizaciones de Google por ratings artificiales, solo se integrará si existen testimonios reales en el sitio. Dado que no se encuentran secciones de reseñas de clientes en la homepage, se propone omitir este esquema hasta contar con testimonios verificables.
> 
> **Página de Autor y E-E-A-T:** Se creará la página `/sobre-mauricio-pineda.html` con un diseño moderno y el esquema `Person` para validar la autoridad de la firma. Se utilizará la foto de perfil que generaremos (`mauricio-pineda.jpg`) y se enlazará a su LinkedIn para señalizar su pericia verificable ante los LLMs.

## Open Questions

> [!NOTE]
> No hay preguntas abiertas críticas para bloquear la fase de diseño. Procederemos a implementar los esquemas JSON-LD según las especificaciones del documento de auditoría.

## Proposed Changes

---

### Componente 1: Configuración de Rastreo (Robots & Sitemaps)

Se actualizará la guía de indexación para los crawlers de búsqueda tradicional e IA generativa.

#### [MODIFY] [robots.txt](file:///c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/robots.txt)
- Permitir explícitamente el acceso total a los user-agents de IA: `GPTBot`, `ClaudeBot`, `Google-Extended`, `PerplexityBot`, `anthropic-ai`, `Gemini-GPTBot`.
- Enlazar a los sitemaps principales: `sitemap.xml` y `sitemap-blog.xml`.

#### [MODIFY] [sitemap.xml](file:///c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/sitemap.xml)
- Convertir en un **Sitemap Index** que apunta a `sitemap-pages.xml` y `sitemap-blog.xml`.

#### [NEW] [sitemap-pages.xml](file:///c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/sitemap-pages.xml)
- Incluir la homepage y las 10 páginas de servicios con sus respectivas prioridades y frecuencias de actualización.

#### [NEW] [sitemap-blog.xml](file:///c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/sitemap-blog.xml)
- Incluir todos los artículos del blog en español (`/Blog/*.html`) y en inglés (`/en/blog/*.html`).

---

### Componente 2: Estructura Semántica y Rendimiento (Landmarks HTML5, Preloads, Defer)

Se estructurarán semánticamente las páginas y se optimizarán recursos para los Core Web Vitals.

#### [MODIFY] [index.html](file:///c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/index.html)
- Cargar la librería Three.js de manera explícita en el `<head>` para solventar el error JavaScript de visualización en las tarjetas de servicio.
- Añadir preloads de Google Fonts y preconexiones en el `<head>`.
- Precargar la imagen hero (`/images/prodig-hero-futuro-digital.webp`) con prioridad alta.
- Envolver las secciones de contenido principales en un landmark `<main id="inicio" role="main">`.
- Reemplazar el SVG inline del hero por una etiqueta `<img>` moderna con formato WebP, dimensiones explícitas, y texto alternativo descriptivo.
- Añadir el atributo `aria-label` descriptivo a todos los enlaces de servicios.
- Agregar la etiqueta `<data>` para envolver las estadísticas del negocio en la sección "Nosotros".
- Mover scripts no críticos al final o añadirles `defer` para evitar el bloqueo del renderizado.
- Insertar los esquemas estructurados de JSON-LD: `Organization` (con catálogo de ofertas y KnowsAbout), `WebSite` y `DefinedTermSet` (glosario de términos semánticos de ProDig).
- Añadir dirección NAP estructurada en el footer.

#### [MODIFY] Páginas de Servicios (10 archivos HTML)
- Envolver el contenido principal en un landmark `<main role="main">`.
- Añadir `aria-label` a los enlaces de navegación y del footer.
- Insertar el esquema `Service` personalizado para cada servicio, enlazándolo a la entidad raíz `#organization` mediante `@id`.
- Agregar el marcado `SpeakableSpecification` en el esquema para facilitar la lectura por asistentes de voz y agentes conversacionales.
- Añadir la dirección NAP en el footer.
- *Nota: En [seo-y-geo.html](file:///c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/seo-y-geo.html), se integrará adicionalmente el esquema `FAQPage` con las 5 preguntas frecuentes existentes en el contenido.*

---

### Componente 3: Artículos de Autoridad (Blog y E-E-A-T)

Se potenciarán las señales de experiencia humana en los artículos de opinión técnica.

#### [MODIFY] Artículos de Blog (6 en español y 5 en inglés)
- Insertar el esquema `BlogPosting` en cada página de artículo, estableciendo como autor a Mauricio Pineda (`#mauricio-pineda`) y como publicador a la organización (`#organization`).
- Añadir la tarjeta de perfil de autor en formato microdata en la sección final del artículo.
- Agregar dimensiones y el atributo `loading="lazy"` a las imágenes de los artículos.

#### [NEW] [sobre-mauricio-pineda.html](file:///c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/sobre-mauricio-pineda.html)
- Nueva página de biografía profesional para Mauricio Pineda con su perfil, logros, experiencia, y enlaces externos a redes sociales (señales externas de autoridad).
- Contendrá el esquema JSON-LD `Person` enlazado mediante `@id` para cerrar el ciclo de Entity Linking del Knowledge Graph.

---

### Componente 4: Recursos Visuales (Imágenes del Sitio)

Generación de recursos optimizados para la web.

#### [NEW] `images/` (Directorio)
- Se creará el directorio `/images/` en la raíz del proyecto para alojar las imágenes globales.

#### [NEW] `images/prodig-logo.png`
- Logotipo oficial de ProDig para el grafo semántico y visual.

#### [NEW] `images/prodig-hero-futuro-digital.webp`
- Imagen hero abstracta y moderna con temática de inteligencia artificial y tecnología.

#### [NEW] `images/mauricio-pineda.jpg`
- Foto de perfil profesional para el autor de la firma.

---

### Componente 5: Archivos de Guía para Crawlers de IA (llm.txt y llm-full.txt)

Archivos críticos para GEO que instruyen directamente a los crawlers de modelos de lenguaje (GPTBot, ClaudeBot, Perplexity, Gemini) sobre qué contenido priorizar y cómo interpretar la arquitectura de información del sitio.

#### [MODIFY] [llm.txt](file:///c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/llm.txt)
- El archivo existe pero debe actualizarse para alinearse con las especificaciones de la auditoría (formato estandarizado `llmstxt`).
- Incluir: descripción de la firma, datos de contacto, fundador, ubicación, listado completo de páginas de servicio con enlaces, blog de autoridad con todos los artículos, metodología propietaria MDDC, y conceptos clave del glosario ProDig (GEO, Tasa de Referencia, Capa Verde, IA Local, MDDC).
- Añadir metadatos de contacto estructurados para extracción por LLMs.

#### [NEW] [llm-full.txt](file:///c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/llm-full.txt)
- Contendrá el texto completo y limpio (sin HTML) de todas las páginas importantes del sitio para que los LLMs puedan consumir el contenido completo sin necesidad de rastreo múltiple.
- Estructura: documento único con secciones delimitadas por `---` y cabeceras `## PÁGINA: [Nombre] ([URL])`.
- Incluir: homepage, las 10 páginas de servicio, la página de autor, y los 11 artículos del blog (6 español + 5 inglés).
- Archivo vivo: actualizar cada vez que se publique contenido nuevo.

---

### Componente 6: E-E-A-T Completo y Señales de Confianza

Implementación de las señales de Experience, Expertise, Authoritativeness y Trustworthiness que faltan en el sitio, según el capítulo faltante identificado en la auditoría.

#### [MODIFY] Footer de todas las páginas (11 páginas principales + artículos de blog)
- Añadir NAP (Name, Address, Phone) estructurado con microdata `itemscope itemtype="https://schema.org/LocalBusiness"` en la etiqueta `<address>` del footer.
- Incluir: nombre de la firma, ubicación (Bogotá, Colombia), teléfono, email.
- Añadir `itemprop="telephone"` y `itemprop="email"` para señalización semántica a crawlers.

#### [MODIFY] Artículos de Blog (6 español + 5 inglés)
- Añadir firma de autor con microdata `itemscope itemtype="https://schema.org/Person"` al final de cada artículo.
- Incluir: foto (`itemprop="image"` apuntando a `/images/mauricio-pineda.jpg`), nombre (`itemprop="name"`), cargo (`itemprop="jobTitle"`), y enlace al perfil (`itemprop="url"` apuntando a `/sobre-mauricio-pineda.html`).

#### [MODIFY] [index.html](file:///c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/index.html) — Schema DefinedTermSet
- Insertar el bloque JSON-LD `DefinedTermSet` con el glosario de conceptos propietarios de ProDig (Tasa de Referencia, GEO, Capa Verde, MDDC, IA Local).
- Este schema es diferencial para GEO: enseña explícitamente a los LLMs el significado de los términos acuñados por ProDig, asociándolos a la entidad `#organization` mediante `publisher: { "@id": "https://aiprodig.com/#organization" }`.

#### [MODIFY] [seo-y-geo.html](file:///c:/Users/micnu/OneDrive/PROYECTOS/AIPRODIG/seo-y-geo.html) — Schema SpeakableSpecification
- Insertar el bloque JSON-LD `SpeakableSpecification` (en el contexto de `WebPage`) para que asistentes de voz y LLMs de audio identifiquen los fragmentos clave de la página (`h1`, `h2`, `.descripcion-servicio`, `.faq-respuesta`).
- Añadir `isPartOf: { "@id": "https://aiprodig.com/#website" }` para cerrar el ciclo de Entity Linking.

#### [MODIFY] Páginas de Servicio y Blog — Schema BreadcrumbList
- Insertar el bloque JSON-LD `BreadcrumbList` en páginas internas para proporcionar jerarquía de navegación semántica a los crawlers y LLMs.
- Estructura típica: `Home > Servicios > [Nombre del Servicio]` o `Home > Blog > [Título del Artículo]`.
- Mejora la comprensión de la arquitectura de información del sitio por parte de los modelos de IA.

#### [PENDING] Schema AggregateRating
- Según la advertencia del documento de auditoría, este schema **solo se implementará si existen testimonios reales verificables** en el sitio.
- Propuesta: agregar sección de testimonios de clientes en la homepage o en `/sobre-mauricio-pineda.html` con datos reales, y entonces habilitar el `AggregateRating` con valores auténticos.

---

## Plan de Verificación

Se realizarán pruebas automatizadas y manuales para confirmar el correcto funcionamiento de los cambios.

### Pruebas Automatizadas

1. **Script de Verificación Semántica y Esquemas (`test_seo_geo.py`):**
   - Comprobar que `robots.txt` sea válido y permita crawlers de IA.
   - Comprobar que todos los sitemaps existan, estén bien formados y no tengan enlaces caídos.
   - Analizar las 11 páginas principales y los artículos del blog para validar la presencia de landmarks `<main>`, tags de encabezado jerárquicos, preloads de LCP, defer en scripts y etiquetas alt en imágenes.
   - Validar sintácticamente que los bloques de JSON-LD sean JSON válidos y contengan las propiedades requeridas (`@context`, `@type`, `@id`, `name`, `provider`, etc.).

2. **Validación de Enlaces y Recursos:**
   - Detectar si hay enlaces rotos (404) introducidos por los cambios en el menú o sitemaps.

### Verificación Manual

1. **Lighthouse / PageSpeed Insights:**
   - Medir el rendimiento en la homepage local y comparar con el baseline para verificar mejoras en Core Web Vitals (principalmente LCP y bloqueo de renderizado).
2. **Schema.org Validator:**
   - Pegar el código generado en la herramienta oficial [Schema.org Validator](https://validator.schema.org) para verificar que el grafo semántico de `@id` se resuelva correctamente y no haya advertencias.

3. **Validación de llm.txt y llm-full.txt:**
   - Usar [llmstxt.org](https://llmstxt.org) o herramientas similares para validar la estructura y formato de `llm.txt`.
   - Verificar que `llm-full.txt` contenga texto limpio sin HTML y que todas las URLs referenciadas sean accesibles.

4. **Rich Results Test de Google:**
   - Probar cada página en [Google Rich Results Test](https://search.google.com/test/rich-results) para verificar que los JSON-LD (Service, FAQPage, BlogPosting, DefinedTermSet, SpeakableSpecification, BreadcrumbList) sean detectados correctamente.

5. **Validador de microdata (NAP y firma de autor):**
   - Usar [Schema.org Validator](https://validator.schema.org) para verificar que las marcas `itemscope`/`itemtype` en el footer y en los artículos del blog sean válidas.

6. **Verificación de arquitectura de Entity Linking:**
   - Confirmar que los `@id` secundarios (`#mauricio-pineda`, `#website`, `#organization` en schemas Service, BlogPosting, SpeakableSpecification, DefinedTermSet) apunten exactamente a los mismos URIs declarados en el schema Organization de la homepage.
   - Sin esta verificación, el grafo de conocimiento se rompe silenciosamente.
