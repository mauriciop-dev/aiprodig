# 🔍 Auditoría SEO + GEO — aiprodig.com
### Documento de instrucciones técnicas para implementación — Equipo Antigravity
**Fecha:** Junio 2026 | **Elaborado por:** ProDig / Mauricio Pineda  
**Versión:** 1.1 | **Estado:** Listo para implementar

---

## 📌 NOTA PREVIA — Cobertura del libro y gap EEAT

Antes de la auditoría, se revisó si la estructura de capítulos del libro cubre todos los pilares críticos. La respuesta corta: **falta un capítulo dedicado explícitamente a E-E-A-T**. Aquí el análisis:

| Pilar | Cubierto en libro | Capítulo |
|---|---|---|
| Robots.txt / Sitemap | ✅ | Cap. 1 |
| HTML Semántico | ✅ | Cap. 2 |
| Core Web Vitals | ✅ | Cap. 3 |
| JSON-LD / Schema | ✅ | Cap. 4 |
| llm.txt / llm-full.txt | ✅ | Cap. 5 |
| Citaciones en IA | ✅ | Cap. 6 |
| Intenciones conversacionales | ✅ | Cap. 7 |
| Marca + co-ocurrencia LLM | ✅ | Cap. 8 |
| Arquitecturas RAG | ✅ | Cap. 9 |
| **E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)** | ⚠️ Parcial (mencionado en Cap. 6 y 8) | **Falta capítulo propio** |
| **Señales de confianza (NAP, reviews, author pages)** | ❌ No explícito | **Falta** |
| **Contenido "First-hand Experience"** | ⚠️ Mencionado en Cap. 8 | **Sin profundidad** |

**Recomendación:** Insertar un **Capítulo 3B** titulado _"E-E-A-T en 2026: La Autoridad Verificable como Señal de Rankeabilidad y Citabilidad"_ entre los caps. 3 y 4. Es el puente entre SEO técnico y GEO semántico. Sin E-E-A-T, la estructura JSON-LD del Cap. 4 pierde contexto de por qué Google/LLMs priorizan ciertas fuentes.

---

## 🏗️ PARTE I — Diagnóstico Técnico del Sitio (aiprodig.com)

### 1.1 Estructura actual observada

| Elemento | Estado | Notas |
|---|---|---|
| SSL / HTTPS | ✅ Activo | Certificado válido |
| Meta title homepage | ✅ Presente | `"ProDig - Prospectiva Digital | Transformamos el futuro de tu negocio"` |
| Meta description homepage | ✅ Presente | Bien redactada, menciona ubicación Colombia |
| Open Graph | ✅ Implementado | `og:title`, `og:description`, `og:image`, `og:locale` presentes |
| Twitter Cards | ✅ Implementado | `summary_large_image` en homepage; `player` en blog |
| Canonical tags | ✅ Presentes | URL canónica declarada por página |
| Meta lang | ✅ `es` declarado | OK |
| robots meta | ✅ `index, follow` | OK |
| Meta keywords | ⚠️ Presentes | Google ignora keywords; no es error, pero es redundante |
| Sitemap XML | ❌ No detectado | Crítico — no se encontró `/sitemap.xml` |
| robots.txt | ❌ No detectado | Crítico — no se encontró `/robots.txt` |
| llm.txt | ❌ Ausente | Crítico para GEO |
| llm-full.txt | ❌ Ausente | Crítico para GEO |
| JSON-LD Schema | ❌ No detectado en homepage | Crítico — ningún schema estructurado visible |
| Entity Linking (@id) | ❌ Ausente | Crítico para GEO — sin grafo de conocimiento interno |
| Author pages | ❌ Ausentes | Problema E-E-A-T |
| Datos Dublin Core | ✅ En blog posts | `DC.creator`, `DC.date`, `DC.description` — bien |
| FAQPage Schema | ❌ Ausente | FAQs existen en seo-y-geo.html pero sin schema |
| Internal linking | ⚠️ Básico | Servicios enlazan desde homepage pero sin jerarquía profunda |
| Breadcrumbs | ❌ Ausentes | Sin schema BreadcrumbList |
| Imágenes con alt | ⚠️ Parcial | Imagen hero usa SVG inline sin alt descriptivo |
| Velocidad (estimada) | ⚠️ Sin datos medidos | Requiere Lighthouse / PageSpeed Insights |

---

## 🛠️ PARTE II — Instrucciones de Implementación por Capítulo

---

### 📘 CAPÍTULO 1 — robots.txt y sitemap.xml

#### ❌ Problema detectado
No existe `/robots.txt` ni `/sitemap.xml` en el dominio. Esto significa:
- Los crawlers de Google, Bing, GPTBot, ClaudeBot y otros no tienen guía explícita
- Ningún LLM crawler sabe qué páginas priorizar
- El sitio no referencia su sitemap, lo que ralentiza la indexación

#### ✅ Acción 1 — Crear `/robots.txt`

Crear el archivo en la raíz del sitio con el siguiente contenido:

```
# robots.txt — aiprodig.com
# Actualizado: Junio 2026

User-agent: *
Allow: /
Disallow: /cdn-cgi/
Disallow: /admin/
Disallow: /private/

# Crawlers de IA — permitir acceso explícito
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Gemini-GPTBot
Allow: /

# Sitemaps
Sitemap: https://aiprodig.com/sitemap.xml
Sitemap: https://aiprodig.com/sitemap-blog.xml
```

> **Nota:** Revisar y actualizar esta lista de user-agents de IA cada trimestre — nuevos crawlers emergen constantemente.

#### ✅ Acción 2 — Crear `/sitemap.xml` (sitemap principal)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://aiprodig.com/sitemap-pages.xml</loc>
    <lastmod>2026-06-01</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://aiprodig.com/sitemap-blog.xml</loc>
    <lastmod>2026-06-01</lastmod>
  </sitemap>
</sitemapindex>
```

#### ✅ Acción 3 — Crear `/sitemap-pages.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://aiprodig.com/</loc>
    <lastmod>2026-06-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://aiprodig.com/seo-y-geo.html</loc>
    <lastmod>2026-05-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://aiprodig.com/chatbots.html</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://aiprodig.com/saas.html</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://aiprodig.com/ia-local.html</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://aiprodig.com/rag.html</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://aiprodig.com/agentes-ia.html</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://aiprodig.com/power-platform.html</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://aiprodig.com/capacitacion.html</loc>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://aiprodig.com/consultoria.html</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://aiprodig.com/sitios-web-ia.html</loc>
    <priority>0.8</priority>
  </url>
</urlset>
```

#### ✅ Acción 4 — Crear `/sitemap-blog.xml`

Incluir todas las URLs del directorio `/Blog/` con `<lastmod>` real de cada artículo. Actualmente detectados 6 artículos. Añadir nuevos artículos al sitemap cada vez que se publique uno.

---

### 📘 CAPÍTULO 2 — Semántica HTML5

#### ⚠️ Problemas detectados
- La homepage usa estructura de sección ancla (`#servicios`, `#nosotros`) — es una SPA parcial, lo que puede dificultar el rastreo independiente por sección
- No se detectan etiquetas `<article>`, `<aside>`, `<nav>` explícitas en el HTML renderizado
- La imagen hero es un SVG inline codificado (data URI) sin `<img alt="">` descriptivo
- No hay `<header>`, `<main>`, `<footer>` explícitos visibles en el markup

#### ✅ Acciones requeridas

**A) Estructura de landmarks HTML5 — verificar que el HTML tenga:**
```html
<header role="banner">
  <nav aria-label="Navegación principal">...</nav>
</header>

<main id="inicio" role="main">
  <section id="hero" aria-label="Propuesta de valor">...</section>
  <section id="servicios" aria-label="Servicios ProDig">...</section>
  <section id="nosotros" aria-label="Sobre ProDig">...</section>
  <section id="blog" aria-label="Blog AIPRODIG">...</section>
  <section id="contacto" aria-label="Contacto">...</section>
</main>

<footer role="contentinfo">...</footer>
```

**B) Imagen hero — reemplazar SVG inline por:**
```html
<img 
  src="/images/prodig-hero-futuro-digital.webp" 
  alt="ProDig - Consultoría en Inteligencia Artificial y automatización digital en Bogotá, Colombia"
  width="400" height="300"
  loading="lazy"
/>
```

**C) Encabezados — verificar jerarquía:**
- Solo UN `<h1>` por página (en homepage: "Prospectiva Digital")
- Servicios individuales: `<h2>` para nombre de servicio
- Subcontenido: `<h3>`
- No saltar niveles (de h1 a h3 directo)

**D) Links de servicios — añadir `aria-label` descriptivo:**
```html
<a href="/seo-y-geo.html" aria-label="Servicio de SEO y GEO - Posicionamiento en modelos de IA">
  SEO y GEO
</a>
```

**E) Estadísticas numéricas — marcar con `<data>`:**
```html
<data value="50">+50</data> Proyectos Completados
<data value="98">98%</data> Satisfacción del Cliente
<data value="5">5+</data> Años de Experiencia
```

---

### 📘 CAPÍTULO 3 — Core Web Vitals

#### ⚠️ Problemas detectados (estimados)
- Imagen hero es un SVG codificado en base64 inline — esto infla el HTML y bloquea el LCP
- No se detectan hints de precarga (`<link rel="preload">`)
- No se ven indicios de lazy loading para imágenes del blog
- El chatbot widget (IA embebida) puede generar bloqueo de render si carga scripts síncronos

#### ✅ Acciones requeridas

**A) En el `<head>` — añadir preloads críticos:**
```html
<!-- Preload fuente principal si usa Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Preload imagen LCP (hero) -->
<link rel="preload" as="image" href="/images/prodig-hero.webp" fetchpriority="high">
```

**B) Imágenes del blog — añadir lazy loading:**
```html
<img src="/Blog/images/imagen6.jpg" 
     alt="[descripción real del artículo]" 
     loading="lazy" 
     width="800" height="450">
```

**C) Script del chatbot — diferir carga:**
```html
<!-- Cambiar de esto: -->
<script src="chatbot.js"></script>

<!-- A esto: -->
<script src="chatbot.js" defer></script>
```

**D) Medir con herramientas:**
- PageSpeed Insights: https://pagespeed.web.dev/ → ingresar https://aiprodig.com
- Objetivo: LCP < 2.5s, FID/INP < 200ms, CLS < 0.1
- **Tomar capturas de pantalla de los resultados antes de hacer cualquier cambio — necesitamos baseline**

---

### 📘 CAPÍTULO 4 — JSON-LD, Schema.org y Entity Linking (CRÍTICO)

#### ❌ Problema detectado
**No existe ningún JSON-LD en el sitio.** Este es el gap más crítico para GEO. Sin datos estructurados, los LLMs no tienen señales semánticas explícitas para identificar a ProDig como entidad, sus servicios, su ubicación, ni su autoridad.

---

#### 🔗 CONCEPTO CLAVE — Entity Linking mediante `@id`

Antes de ver el código, es fundamental que Antigravity entienda la arquitectura que se está construyendo.

Los `@id` son URIs permanentes que funcionan como identificadores únicos de cada entidad. Cuando Google o un LLM rastrean múltiples páginas del sitio, los `@id` permiten que entiendan que el `"provider"` mencionado en `/seo-y-geo.html` **es exactamente la misma entidad** que el `Organization` declarado en la homepage — no una copia, la misma entidad.

**Sin `@id`:** cada página es una isla de datos desconectada.  
**Con `@id`:** el sitio entero forma un Knowledge Graph interno que los LLMs pueden razonar y citar con precisión.

##### Mapa del grafo de entidades de aiprodig.com

```
#organization  ←── Entidad raíz (homepage)
    │
    ├── founder ──────────────→ #mauricio-pineda (Person)
    │                                │
    │                                └── sameAs → LinkedIn
    │
    ├── publisher ←────────── #website (WebSite)
    │                              │
    │                              └── mainEntity ← cada WebPage
    │
    ├── provider ←─────────── cada Service (páginas de servicio)
    │                              │
    │                              └── mainEntityOfPage → WebPage del servicio
    │
    └── publisher ←────────── cada BlogPosting
                                   │
                                   └── author → #mauricio-pineda
```

##### Regla crítica para Antigravity
**Ningún `@id` en los schemas secundarios debe inventarse.** Todos deben apuntar exactamente a los mismos URIs declarados en la homepage:

| Entidad | @id canónico |
|---|---|
| La empresa | `https://aiprodig.com/#organization` |
| El sitio web | `https://aiprodig.com/#website` |
| El fundador | `https://aiprodig.com/#mauricio-pineda` |

Si en alguna página de servicio o blog aparece `"provider"` o `"author"`, el valor debe ser siempre `{ "@id": "https://aiprodig.com/#organization" }` o `{ "@id": "https://aiprodig.com/#mauricio-pineda" }` — nunca texto libre ni una URL diferente.

---

#### ✅ Acción 1 — Schema Organization en homepage (entidad raíz)

Insertar en el `<head>` del `index.html`. Este es el schema más importante — todos los demás referencian a este:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://aiprodig.com/#organization",
  "name": "ProDig - Prospectiva Digital",
  "alternateName": "ProDig",
  "url": "https://aiprodig.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://aiprodig.com/images/prodig-logo.png",
    "width": 300,
    "height": 100
  },
  "description": "Consultoría en Inteligencia Artificial y desarrollo de activos digitales. Chatbots, SaaS, SEO/GEO, Agentes IA, Power Platform. Bogotá, Colombia.",
  "foundingDate": "2021",
  "founder": {
    "@type": "Person",
    "@id": "https://aiprodig.com/#mauricio-pineda",
    "name": "Mauricio Pineda",
    "jobTitle": "Fundador y Director de Innovación Digital",
    "url": "https://aiprodig.com/sobre-mauricio-pineda.html",
    "sameAs": [
      "https://www.linkedin.com/in/mauriciopineda"
    ]
  },
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Bogotá",
    "addressRegion": "Cundinamarca",
    "addressCountry": "CO"
  },
  "contactPoint": [
    {
      "@type": "ContactPoint",
      "telephone": "+57-314-489-7092",
      "contactType": "customer service",
      "availableLanguage": ["Spanish"],
      "areaServed": ["CO", "LATAM"]
    }
  ],
  "sameAs": [
    "https://aiprodig.com",
    "https://materiaprogramable.com"
  ],
  "knowsAbout": [
    "Inteligencia Artificial",
    "Generative Engine Optimization",
    "SEO",
    "Chatbots",
    "Automatización de procesos",
    "Power Platform",
    "RAG - Retrieval Augmented Generation",
    "Agentes de IA"
  ],
  "areaServed": {
    "@type": "GeoCircle",
    "geoMidpoint": {
      "@type": "GeoCoordinates",
      "latitude": 4.711,
      "longitude": -74.0721
    },
    "name": "Bogotá, Colombia y Latinoamérica"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Servicios ProDig",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "SEO y GEO", "url": "https://aiprodig.com/seo-y-geo.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Chatbots con IA", "url": "https://aiprodig.com/chatbots.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Agentes de IA", "url": "https://aiprodig.com/agentes-ia.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "RAG - Chat con documentos", "url": "https://aiprodig.com/rag.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "SaaS a medida", "url": "https://aiprodig.com/saas.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "IA Local", "url": "https://aiprodig.com/ia-local.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Power Platform con IA", "url": "https://aiprodig.com/power-platform.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Sitios Web con IA", "url": "https://aiprodig.com/sitios-web-ia.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Capacitación en IA", "url": "https://aiprodig.com/capacitacion.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Consultoría estratégica", "url": "https://aiprodig.com/consultoria.html"}}
    ]
  }
}
</script>
```

#### ✅ Acción 2 — Schema WebSite (homepage) — referencia la entidad raíz

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "https://aiprodig.com/#website",
  "url": "https://aiprodig.com",
  "name": "ProDig - Prospectiva Digital",
  "description": "Consultoría en IA y activos digitales para empresas latinoamericanas",
  "inLanguage": "es",
  "publisher": {
    "@id": "https://aiprodig.com/#organization"
  }
}
</script>
```

#### ✅ Acción 3 — FAQPage Schema en `/seo-y-geo.html`

Las FAQs ya existen en la página pero sin schema. Añadir en el `<head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Qué diferencia hay entre SEO tradicional y GEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "El SEO tradicional optimiza para motores de búsqueda como Google, mientras que el GEO (Generative Engine Optimization) optimiza para modelos de IA generativa como Gemini, ChatGPT y Claude. Los LLMs no indexan como Google; aprenden de patrones y citan fuentes basándose en autoridad, relevancia y estructura semántica. El GEO requiere optimizar para ser citado por IA en lugar de ser rankeado por algoritmo."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuánto tiempo toma ver resultados en GEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Los primeros resultados de visibilidad en IA aparecen en 4 a 8 semanas, pero la autoridad de marca en modelos de lenguaje se construye a lo largo de 3 a 6 meses. ProDig realiza reportes mensuales de citas en LLMs y ajustes estratégicos continuos."
      }
    },
    {
      "@type": "Question",
      "name": "¿Para qué modelos de IA optimizan en ProDig?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Optimizamos para todos los principales modelos: Google Gemini, OpenAI ChatGPT, Anthropic Claude, Microsoft Copilot, Perplexity, y otros modelos emergentes. Cada modelo tiene particularidades técnicas que adaptamos en la estrategia de GEO."
      }
    },
    {
      "@type": "Question",
      "name": "¿El GEO reemplaza al SEO tradicional?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No, el GEO complementa y amplifica el SEO tradicional. Los factores técnicos básicos como velocidad, mobile-friendly y backlinks siguen siendo relevantes. El GEO añade una capa de optimización para el nuevo paradigma de búsqueda generativa con IA."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cómo miden el éxito del GEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Medimos mediante: porcentaje de citas en LLMs para términos clave de la industria, posición de marca en respuestas generativas, tráfico atribuido desde chatbots y asistentes IA, y share of voice en el ecosistema de IA. Proporcionamos dashboard de monitoreo."
      }
    }
  ]
}
</script>
```

#### ✅ Acción 4 — Schema Service para cada página de servicio (con Entity Linking)

Ejemplo para `/seo-y-geo.html`. Replicar el patrón en las 10 páginas de servicio, cambiando `name`, `description`, `@id` de la página y `offers`.

**Observar cómo `provider` y `mainEntityOfPage` conectan con la homepage mediante `@id`:**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://aiprodig.com/seo-y-geo.html#service",
  "name": "SEO y GEO — Posicionamiento en Modelos de IA",
  "description": "Optimizamos tu presencia digital para que modelos como Gemini, Claude y ChatGPT citen tu contenido como fuente autorizada. Estrategias de citation engineering, structured data y optimización de entidades.",
  "provider": {
    "@id": "https://aiprodig.com/#organization"
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://aiprodig.com/seo-y-geo.html"
  },
  "areaServed": "Latinoamérica",
  "serviceType": "Generative Engine Optimization",
  "offers": [
    {
      "@type": "Offer",
      "name": "Plan Presencia",
      "priceCurrency": "COP",
      "price": "1200000",
      "description": "Configuración Google Search Console, Analytics 4, meta-etiquetas, JSON-LD Organization, FAQs semánticas"
    },
    {
      "@type": "Offer",
      "name": "Plan Relevancia",
      "priceCurrency": "COP",
      "price": "2500000",
      "priceSpecification": {
        "@type": "UnitPriceSpecification",
        "billingDuration": "P1M"
      },
      "description": "Core Web Vitals, SEO Local, Schema Service/Product, Glosario Semántico"
    },
    {
      "@type": "Offer",
      "name": "Plan Autoridad AI",
      "priceCurrency": "COP",
      "price": "4800000",
      "priceSpecification": {
        "@type": "UnitPriceSpecification",
        "billingDuration": "P1M"
      },
      "description": "Topic Clusters, Backlinks, Entity Linking, Monitoreo de menciones en LLMs"
    }
  ]
}
</script>
```

#### ✅ Acción 5 — Schema BlogPosting para cada artículo (con Entity Linking)

Añadir en el `<head>` de cada post del blog. Observar cómo `author`, `publisher` y `mainEntityOfPage` referencian las entidades raíz:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "@id": "https://aiprodig.com/Blog/[slug-del-articulo].html#article",
  "headline": "Del Caos Algorítmico a la Tasa de Referencia: La Metamorfosis del SEO al GEO",
  "description": "Descubre la transformación del SEO al GEO en 2026. Cómo la IA ha cambiado las reglas del posicionamiento y por qué la autoridad humana es el activo más valioso.",
  "image": "https://aiprodig.com/Blog/images/imagen5.jpg",
  "datePublished": "2026-04-25",
  "dateModified": "2026-04-25",
  "inLanguage": "es",
  "author": {
    "@id": "https://aiprodig.com/#mauricio-pineda"
  },
  "publisher": {
    "@id": "https://aiprodig.com/#organization"
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://aiprodig.com/Blog/[slug-del-articulo].html"
  },
  "keywords": ["GEO", "SEO 2026", "Generative Engine Optimization", "LLM", "IA", "posicionamiento"],
  "articleSection": "IA-Estrategia",
  "wordCount": 1800,
  "about": [
    {"@type": "Thing", "name": "Generative Engine Optimization"},
    {"@type": "Thing", "name": "Inteligencia Artificial"},
    {"@type": "Thing", "name": "Posicionamiento digital"}
  ]
}
</script>
```

#### ✅ Acción 6 — Schema DefinedTerm para conceptos propietarios (GEO avanzado)

Este schema es poco usado pero muy poderoso para GEO: le enseña explícitamente a los LLMs qué significan los términos propietarios de ProDig. Cuando un modelo vea "Tasa de Referencia" en cualquier contexto, sabrá que es un concepto acuñado por ProDig.

Insertar en la homepage y/o en páginas de servicio relevantes:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "DefinedTermSet",
  "@id": "https://aiprodig.com/#glosario-prodig",
  "name": "Glosario ProDig — Conceptos propietarios de IA y GEO",
  "publisher": {
    "@id": "https://aiprodig.com/#organization"
  },
  "hasDefinedTerm": [
    {
      "@type": "DefinedTerm",
      "name": "Tasa de Referencia",
      "description": "Métrica propietaria de ProDig que mide la frecuencia con la que modelos de lenguaje como Gemini, Claude y ChatGPT citan una marca o contenido en sus respuestas generativas. Análogo al PageRank pero para el ecosistema de IA.",
      "inDefinedTermSet": "https://aiprodig.com/#glosario-prodig"
    },
    {
      "@type": "DefinedTerm",
      "name": "GEO - Generative Engine Optimization",
      "description": "Disciplina de optimización digital orientada a que el contenido de una empresa sea citado, referenciado y recomendado por motores de búsqueda generativos basados en IA, como Google AI Overviews, ChatGPT, Claude y Perplexity.",
      "inDefinedTermSet": "https://aiprodig.com/#glosario-prodig"
    },
    {
      "@type": "DefinedTerm",
      "name": "Capa Verde",
      "description": "Concepto ProDig que describe el conjunto de contenido público, técnico y verificable que actúa como combustible para el posicionamiento en modelos de lenguaje. La Capa Verde es el activo de autoridad que los LLMs consumen para aprender sobre una marca.",
      "inDefinedTermSet": "https://aiprodig.com/#glosario-prodig"
    },
    {
      "@type": "DefinedTerm",
      "name": "MDDC - Metodología de Desarrollo Dirigida por Contexto",
      "description": "Marco metodológico propietario de ProDig para el desarrollo de productos digitales con IA. Se basa en tres pilares: Context Engineering (diseño de contextos para agentes), Context-Directed Orchestration (orquestación de agentes por contexto) y Asset Architecture (construcción de activos digitales duraderos).",
      "inDefinedTermSet": "https://aiprodig.com/#glosario-prodig"
    },
    {
      "@type": "DefinedTerm",
      "name": "IA Local",
      "description": "Modalidad de implementación de inteligencia artificial en la que los modelos de lenguaje se ejecutan en la infraestructura propia de la empresa, sin enviar datos a servidores externos. Garantiza privacidad total y cumplimiento normativo.",
      "inDefinedTermSet": "https://aiprodig.com/#glosario-prodig"
    }
  ]
}
</script>
```

#### ✅ Acción 7 — Schema SpeakableSpecification (GEO para voz y asistentes)

Permite que asistentes de voz y LLMs de audio (Google Assistant, Alexa, futuros agentes) identifiquen los fragmentos más importantes de cada página para leer en voz alta. Insertar en páginas clave:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "https://aiprodig.com/seo-y-geo.html",
  "name": "SEO y GEO — Posicionamiento en Modelos de IA | ProDig",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": ["h1", "h2", ".descripcion-servicio", ".faq-respuesta"]
  },
  "isPartOf": {
    "@id": "https://aiprodig.com/#website"
  }
}
</script>
```

> **Nota para Antigravity:** Los valores de `cssSelector` deben corresponder a las clases CSS reales del sitio. Revisar y ajustar antes de implementar.

---

### 📘 CAPÍTULO 5 — llm.txt y llm-full.txt (CRÍTICO PARA GEO)

#### ❌ Problema detectado
Ninguno de los dos archivos existe. Esto significa que crawlers de IA como GPTBot, ClaudeBot y Perplexity navegan el sitio sin guía, pudiendo ignorar las páginas más valiosas.

#### ✅ Acción 1 — Crear `/llm.txt`

```markdown
# ProDig - Prospectiva Digital
> Consultoría especializada en Inteligencia Artificial y activos digitales para empresas latinoamericanas. Con sede en Bogotá, Colombia, ProDig transforma y automatiza negocios mediante IA generativa, chatbots, agentes autónomos, arquitecturas RAG y posicionamiento en modelos de lenguaje (GEO).

Fundador: Mauricio Pineda
Sitio web: https://aiprodig.com
Contacto: +57 314 489 7092
Ubicación: Bogotá, Colombia
Mercados: Colombia, Latinoamérica

## Páginas principales

- [Inicio](https://aiprodig.com/): Propuesta de valor, servicios y visión de ProDig
- [SEO y GEO](https://aiprodig.com/seo-y-geo.html): Posicionamiento en modelos de IA — Gemini, Claude, ChatGPT
- [Chatbots](https://aiprodig.com/chatbots.html): Asistentes IA con respuesta multimedia
- [SaaS](https://aiprodig.com/saas.html): Demos funcionales en 48 horas con agentes constructores
- [IA Local](https://aiprodig.com/ia-local.html): Modelos de IA ejecutándose en infraestructura propia
- [RAG](https://aiprodig.com/rag.html): Chat con documentos internos — PDF, audio, video
- [Power Platform](https://aiprodig.com/power-platform.html): Ecosistema Microsoft con IA — Power BI, Apps, Automate
- [Agentes de IA](https://aiprodig.com/agentes-ia.html): Automatización con Google ADK
- [Sitios Web IA](https://aiprodig.com/sitios-web-ia.html): Webs inteligentes con IA integrada
- [Capacitación](https://aiprodig.com/capacitacion.html): Formación in-company en IA
- [Consultoría](https://aiprodig.com/consultoria.html): Primera hora gratis, roadmap tecnológico

## Blog — Contenido de autoridad

- [Del Caos Algorítmico al GEO (2026)](https://aiprodig.com/Blog/del-caos-algoritmico-a-la-tasa-de-referencia-la-metamorfosis-del-seo-al-geo-y-el-surgimiento-de-la-autoridad-humana-en-2026.html)
- [El Activo Invisible — Soberanía digital](https://aiprodig.com/Blog/el-activo-invisible-por-que-su-empresa-es-mas-pobre-de-lo-que-dicen-sus-libros-contables.html)
- [La Gran Convergencia — IA y Materia](https://aiprodig.com/Blog/la-gran-convergencia-por-que-la-ia-de-hoy-es-el-sistema-operativo-de-la-materia-de-manana.html)
- [Web en 2026 — ¿Importa aún?](https://aiprodig.com/Blog/crees-que-tener-una-pagina-web-en-2026-es-irrelevante-la-realidad-te-sorprendera.html)
- [Agile vs IA](https://aiprodig.com/Blog/por-que-el-agile-tradicional-esta-frenando-tu-empresa-en-la-era-de-la-ia.html)
- [El Síndrome del Software Frankenstein](https://aiprodig.com/Blog/el-sindrome-del-software-frankenstein-la-tragedia-del-subuso-tecnologico-en-el-sector-publico-y-como-solucionarlo.html)

## Metodología propietaria

ProDig opera bajo la **MDDC (Metodología de Desarrollo Dirigida por Contexto)**, basada en tres pilares:
1. Context Engineering — diseño de prompts y contextos para agentes IA
2. Context-Directed Orchestration — orquestación de agentes mediante contexto
3. Asset Architecture — construcción de activos digitales duraderos

## Conceptos clave ProDig

- **GEO (Generative Engine Optimization):** Optimización para ser citado por modelos de IA generativa
- **Tasa de Referencia:** Métrica ProDig que mide la frecuencia de citas de una marca en LLMs
- **Capa Verde:** Contenido público de autoridad técnica, combustible del GEO
- **IA Local:** Modelos ejecutándose en infraestructura propia con privacidad total
- **MDDC:** Metodología de Desarrollo Dirigida por Contexto — framework propietario de ProDig
- **Del bit al átomo:** Visión de ProDig sobre la convergencia de IA y materia física
```

#### ✅ Acción 2 — Crear `/llm-full.txt`

Este archivo debe contener el texto completo y limpio (sin HTML) de todas las páginas importantes. Estructura sugerida:

```markdown
# ProDig - Prospectiva Digital — Contenido completo para modelos de IA
# Fuente: https://aiprodig.com | Actualizado: Junio 2026

---
## PÁGINA: Inicio (https://aiprodig.com/)
[Pegar aquí el texto completo de la homepage sin HTML]

---
## PÁGINA: SEO y GEO (https://aiprodig.com/seo-y-geo.html)
[Pegar aquí el texto completo de la página]

---
## BLOG: Del Caos Algorítmico al GEO
[Pegar aquí el texto completo del artículo]

[... continuar con todas las páginas ...]
```

> **Nota para Antigravity:** Este archivo es vivo — actualizarlo cada vez que se publique contenido nuevo o se modifique una página existente.

---

## 🔴 CAPÍTULO FALTANTE — E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)

Este es el gap estratégico más importante no cubierto por los capítulos actuales. E-E-A-T es el fundamento que justifica por qué un LLM decide citar ProDig en lugar de un competidor.

### ❌ Problemas detectados en aiprodig.com

1. **No existe página de autor** para Mauricio Pineda
2. **No hay bio con credenciales** visibles en el sitio
3. **Las estadísticas** (+50 proyectos, 98% satisfacción, 5+ años) no tienen fuente verificable
4. **El blog no muestra autor** con perfil enlazado en cada post
5. **No hay reseñas o testimonios** con schema Review
6. **No hay NAP consistente** (Name, Address, Phone) en formato estructurado
7. **No hay perfil de Google Business** referenciado en el sitio

### ✅ Acciones E-E-A-T requeridas

**A) Crear página `/sobre-mauricio-pineda.html`:**

Contenido mínimo:
- Foto real (con `alt` descriptivo)
- Cargo: Fundador, ProDig - Prospectiva Digital
- Años de experiencia y áreas de especialización
- Proyectos destacados (sin violar NDA)
- Presencia en LinkedIn (enlace externo — señal de identidad verificable)
- Schema Person con `@id: "https://aiprodig.com/#mauricio-pineda"` y `sameAs` a LinkedIn

**B) Añadir firma de autor en cada post del blog:**

```html
<div itemscope itemtype="https://schema.org/Person">
  <img itemprop="image" src="/images/mauricio-pineda.jpg" alt="Mauricio Pineda, fundador ProDig">
  <span itemprop="name">Mauricio Pineda</span>
  <span itemprop="jobTitle">Fundador, ProDig - Prospectiva Digital</span>
  <a itemprop="url" href="https://aiprodig.com/sobre-mauricio-pineda.html">Ver perfil</a>
</div>
```

**C) Schema AggregateRating (si hay testimonios reales verificables):**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://aiprodig.com/#organization",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "12",
    "bestRating": "5"
  }
}
</script>
```

> **Importante:** Solo implementar si los datos son reales y verificables. Google penaliza ratings falsos.

**D) NAP estructurado en footer (todas las páginas):**

```html
<address itemscope itemtype="https://schema.org/LocalBusiness">
  <span itemprop="name">ProDig - Prospectiva Digital</span>
  <span itemprop="addressLocality">Bogotá</span>,
  <span itemprop="addressCountry">Colombia</span>
  <a itemprop="telephone" href="tel:+573144897092">+57 314 489 7092</a>
  <a itemprop="email" href="mailto:contacto@aiprodig.com">contacto@aiprodig.com</a>
</address>
```

---

## 📋 RESUMEN — Checklist de implementación para Antigravity

### 🔴 Prioridad CRÍTICA (implementar primero)

| # | Tarea | Archivo/Página | Cap. |
|---|---|---|---|
| 1 | Crear `/robots.txt` con user-agents de IA | Raíz del servidor | Cap. 1 |
| 2 | Crear `/sitemap.xml` (índice) | Raíz del servidor | Cap. 1 |
| 3 | Crear `/sitemap-pages.xml` | Raíz del servidor | Cap. 1 |
| 4 | Crear `/sitemap-blog.xml` | Raíz del servidor | Cap. 1 |
| 5 | Insertar JSON-LD Organization en homepage (entidad raíz) | `index.html` | Cap. 4 |
| 6 | Insertar JSON-LD WebSite en homepage | `index.html` | Cap. 4 |
| 7 | Insertar JSON-LD FAQPage en `/seo-y-geo.html` | `seo-y-geo.html` | Cap. 4 |
| 8 | Crear `/llm.txt` | Raíz del servidor | Cap. 5 |
| 9 | Crear `/llm-full.txt` | Raíz del servidor | Cap. 5 |

### 🟡 Prioridad ALTA (implementar en semana 2)

| # | Tarea | Archivo/Página | Cap. |
|---|---|---|---|
| 10 | Insertar JSON-LD Service en 10 páginas de servicio (con `provider: @id`) | Páginas `/servicio.html` | Cap. 4 |
| 11 | Insertar JSON-LD BlogPosting en 6 artículos (con `author: @id` y `publisher: @id`) | Directorio `/Blog/` | Cap. 4 |
| 12 | Insertar JSON-LD DefinedTermSet con glosario ProDig | `index.html` | Cap. 4 |
| 13 | Verificar landmarks HTML5 (`<main>`, `<header>`, `<footer>`, `<section aria-label>`) | Todas las páginas | Cap. 2 |
| 14 | Reemplazar imagen hero SVG inline por WebP con alt descriptivo | `index.html` | Cap. 2 & 3 |
| 15 | Añadir `loading="lazy"` y dimensiones a imágenes del blog | Directorio `/Blog/` | Cap. 3 |
| 16 | Añadir `defer` a scripts no críticos (chatbot widget) | Todas las páginas | Cap. 3 |
| 17 | Crear página de autor `/sobre-mauricio-pineda.html` con Schema Person | Nueva página | E-E-A-T |

### 🟢 Prioridad MEDIA (implementar en semana 3-4)

| # | Tarea | Archivo/Página | Cap. |
|---|---|---|---|
| 18 | Insertar JSON-LD SpeakableSpecification en páginas de servicio clave | Páginas de servicio | Cap. 4 |
| 19 | Añadir firma de autor con microdata en cada post del blog | Directorio `/Blog/` | E-E-A-T |
| 20 | Añadir NAP estructurado en footer de todas las páginas | Todas las páginas | E-E-A-T |
| 21 | Añadir `<link rel="preload">` para recursos críticos en `<head>` | Todas las páginas | Cap. 3 |
| 22 | Añadir `aria-label` a todos los enlaces de servicios | `index.html` | Cap. 2 |
| 23 | Medir Core Web Vitals con PageSpeed Insights y reportar resultados | — | Cap. 3 |
| 24 | Insertar JSON-LD BreadcrumbList en páginas internas | Páginas de servicio y blog | Cap. 4 |
| 25 | Añadir `<data>` a estadísticas numéricas | `index.html` | Cap. 2 |
| 26 | Actualizar `llm-full.txt` con contenido de nuevas páginas | Raíz del servidor | Cap. 5 |

---

## 🔗 Herramientas de validación post-implementación

| Herramienta | URL | Para verificar |
|---|---|---|
| Google Rich Results Test | https://search.google.com/test/rich-results | JSON-LD schemas y Entity Linking |
| Schema.org Validator | https://validator.schema.org | Estructura de schemas |
| Google PageSpeed Insights | https://pagespeed.web.dev | Core Web Vitals |
| Google Search Console | https://search.google.com/search-console | Indexación, sitemap |
| llms.txt Checker | https://llmstxt.org | Validar llm.txt |
| Ahrefs / Screaming Frog | — | Auditoría técnica general |
| OpenGraph Debugger (Meta) | https://developers.facebook.com/tools/debug/ | OG tags |
| Twitter Card Validator | https://cards-dev.twitter.com/validator | Twitter Cards |
| Google Knowledge Panel | https://google.com → buscar "ProDig Bogotá" | Verificar si aparece panel |

---

## 📝 Notas finales para Antigravity

1. **Antes de cualquier cambio** — tomar capturas de PageSpeed Insights en desktop y mobile para tener baseline
2. **Los JSON-LD** deben validarse en Rich Results Test después de cada implementación
3. **Entity Linking es arquitectura, no decoración** — si un `@id` está mal copiado en un schema secundario, el grafo se rompe silenciosamente. Validar con Schema.org Validator después de cada página
4. **El `llm-full.txt`** es un archivo vivo — crear proceso para actualizarlo cuando se publique contenido nuevo
5. **Los robots.txt user-agents de IA** deben revisarse trimestralmente — nuevos crawlers emergen constantemente
6. **El sitemap debe enviarse** a Google Search Console y Bing Webmaster Tools inmediatamente después de crearlo
7. **E-E-A-T no es técnico** — requiere decisión de Mauricio sobre qué información personal/profesional publicar
8. **DefinedTermSet y SpeakableSpecification** son schemas de GEO avanzado — baja prioridad técnica pero alto impacto en diferenciación de marca en LLMs

---

*Documento elaborado por ProDig - Prospectiva Digital | aiprodig.com*  
*Basado en auditoría directa del sitio web y estándares SEO/GEO vigentes a Junio 2026*  
*Versión 1.1 — Integra Entity Linking (@id), DefinedTermSet y SpeakableSpecification*
