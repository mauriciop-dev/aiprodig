import os
import sys

# Add the path to the original script to import its functions
sys.path.append(os.path.join(os.getcwd(), 'Blog', 'images'))
from processor import create_slug, generate_html, OUTPUT_EN

articles_en = [
    {
        "id": 1,
        "titulo": "Why is traditional 'Agile' slowing down your company in the age of AI?",
        "fecha": "April 16, 2026",
        "categoria": "AI-Automation",
        "meta": "Does Scrum still work in 2026? We analyze why traditional agile methodologies have become slow for SMEs.",
        "imagen": "imagen2.jpg",
        "cuerpo": """In the competitive business landscape, "agility" has been the mantra for the last decade. However, we are witnessing a paradox: the same tools designed to speed up development are, in many cases, becoming the main bottleneck.

Agile methodologies were born in an era where making a change required days of coordination. Today, with AI-assisted development, that same change takes seconds.

Does it make sense to wait for next Monday's Planning meeting for a task that AI solved on Sunday afternoon? Absolutely not.""",
        "fuentes": "ProDig Research Lab"
    },
    {
        "id": 2,
        "titulo": "Do you think having a website in 2026 is irrelevant? The reality will surprise you.",
        "fecha": "April 16, 2026",
        "categoria": "AI-Business",
        "meta": "In the era of artificial intelligence, social networks are the megaphone, but your website is the source of truth.",
        "imagen": "imagen1.jpg",
        "cuerpo": """Social networks are the megaphone, but your website is the source of truth. While Instagram and TikTok feed entertainment, AIs feed on the structured index of the web.""",
        "fuentes": "http://aiprodig.com"
    },
    {
        "id": 3,
        "titulo": "The Great Convergence: Why Today's AI is Tomorrow's Matter Operating System",
        "fecha": "April 23, 2026",
        "categoria": "AI-Technology",
        "meta": "Discover how ProDig's MDDC methodology is preparing the groundwork for programmable matter, transforming bits into atoms.",
        "imagen": "imagen3.jpg",
        "cuerpo": """Software development has reached a tipping point. For decades, we have lived in a divided world: on one side, digital logic (bits) and, on the other, physical reality (atoms). At ProDig, we believe this division is obsolete. We are entering the era of "The Great Convergence".""",
        "fuentes": "ProDig Manifesto: From Bit to Atom (2026)."
    }
]

if not os.path.exists(OUTPUT_EN): os.makedirs(OUTPUT_EN)

for i, data in enumerate(articles_en):
    prev_info = None
    next_info = None
    
    if i > 0:
        prev_data = articles_en[i-1]
        prev_info = {"titulo": prev_data['titulo'], "slug": create_slug(prev_data['titulo'])}
    
    if i < len(articles_en) - 1:
        next_data = articles_en[i+1]
        next_info = {"titulo": next_data['titulo'], "slug": create_slug(next_data['titulo'])}
        
    html_en = generate_html(data, "en", prev_info, next_info)
    slug_en = create_slug(data['titulo'])
    en_path = os.path.join(OUTPUT_EN, f"{slug_en}.html")
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(html_en)
    print(f"Generated EN: {slug_en}.html")
