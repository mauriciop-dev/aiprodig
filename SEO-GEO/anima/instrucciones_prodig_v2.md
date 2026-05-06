# Protocolo Maestro: Desarrollo de Servicios Vivos ProDig (v2)

Este protocolo define la estructura técnica y el flujo de automatización para la nueva sección de servicios de https://aiprodig.com, enfocándose en el concepto de "Materia Programable" donde las animaciones sustituyen a las imágenes estáticas.

## 1. Definición de Servicios (Catálogo 2026)
Antigravity debe usar este listado para generar el contenido de las subpáginas:
1. **Sitios Web IA**: Integración de automatización y dinamismo.
2. **SEO y GEO**: Referenciación en modelos de lenguaje (Gemini, Claude, GPT).
3. **Chatbots**: Respuesta multimedia y audio interactivo.
4. **SaaS**: Demos en 48h (Agentes constructores).
5. **IA Local**: Privacidad y seguridad con modelos locales.
6. **RAG**: Valorización de datos internos (multiformato).
7. **Power Platform**: Ecosistema Microsoft + IA.
8. **Agentes de IA**: Reducción de horas hombre mediante ADK de Google.
9. **Capacitación**: Formación presencial e in-company.
10. **Consultoría**: Impacto estratégico (primera hora gratis).

## 2. Estructura Obligatoria por Página de Servicio
Cada subpágina generada por Antigravity debe seguir este orden:
- **H1**: Título del servicio.
- **Background Canvas**: Animación (Three.js/Anime.js) específica basada en el prompt del servicio.
- **Resumen Técnico**: 400-500 caracteres detallando la propuesta de valor.
- **Sección Evidencias**: Grid dinámico para videos, fotos y enlaces.
- **FAQ (GEO Ready)**: Acordeón con 5 preguntas clave optimizadas para ser citadas por IAs.
- **Tabla de Precios**: Formato básico claro.
- **SEO/GEO Metadata**: Meta-tags descriptivas.
- **JSON-LD**: Marcado de datos estructurados para Schema.org.

## 3. Instrucciones de Animación (Concepto Visual)
Las animaciones NO son genéricas. Deben representar la lógica del servicio:
- **SEO/GEO**: Agentes de ProDig conversando con agentes de Google/OpenAI.
- **IA Local**: Representación de datos fluyendo dentro de un perímetro seguro (On-premise).
- **RAG**: Conexión entre chat y archivos multiformato (PDF, Audio, Video).
- **Formatos**: Generar dos variantes por servicio (Tarjeta 1:1 y Hero Background Fullscreen).

## 4. Automatización para Antigravity

### Script: `tools/prodig_automation.py`
Este script debe ser creado para automatizar el despliegue:
1. **Screenshot Bot**: Visita cada servicio y captura la versión de "tarjeta" para el `og:image`.
2. **SEO Generator**: Lee el archivo `servicios.yaml` y genera los archivos HTML/JSX con las meta-etiquetas correspondientes.
3. **JSON-LD Linker**: Inyecta los esquemas de datos estructurados.

---
*Instrucción: Antigravity, inicializa el entorno creando `servicios.yaml` con las descripciones técnicas y el script de captura basado en Playwright.*
