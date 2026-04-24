import os
import sys

# Add the path to the original script to import its functions
sys.path.append(os.path.join(os.getcwd(), 'Blog', 'images'))
from processor import create_slug, generate_html, OUTPUT_EN

articles_en = [
    {
        "titulo": "The Great Convergence: Why Today's AI is Tomorrow's Matter Operating System",
        "fecha": "April 23, 2026",
        "categoria": "AI-Technology",
        "meta": "Discover how ProDig's MDDC methodology is preparing the groundwork for programmable matter, transforming bits into atoms.",
        "imagen": "imagen3.jpg",
        "cuerpo": """Software development has reached a tipping point. For decades, we have lived in a divided world: on one side, digital logic (bits) and, on the other, physical reality (atoms). At ProDig, we believe this division is obsolete. We are entering the era of "The Great Convergence".

Software is no longer just for screens
Today, when we implement a multi-agent AI system or an automation with n8n, we are not simply optimizing a database. We are creating digital structures of thought. Our MDDC (Context-Driven Development Methodology) methodology is the first step in mastering this transition.

By prioritizing context over syntax, we enable artificial intelligence to understand human intention. "If an AI can understand the intention behind an administrative task, it will soon be able to understand the intention behind physical form."

From Bit to Atom: The Path to Programmable Matter
Programmable matter is ProDig's final horizon. Imagine a world where physical structures are not static, but can change shape and function according to user needs. To get there, we must first perfect the intelligence that will govern those atoms.

At ProDig, every line of code and every digital asset we develop, like PAIC, is an experiment in this direction. We are building the software that, in a few years, will stop living on servers to live within the very structure of our cities and tools.

"We are not programming applications; we are programming the reality of the future."

This is why the Latin American Institute of Programmable Matter (ILMP) is our North Star. It's not just about technology; it's about creating a physical reality that is as adaptable, efficient, and democratic as open-source software.""",
        "fuentes": """ProDig Manifesto: From Bit to Atom (2026).
Research on Programmable Matter and Contextual AI - ProDig Lab.
MDDC Framework Whitepaper."""
    },
    {
        "titulo": "Do you think having a website in 2026 is irrelevant? The reality will surprise you.",
        "fecha": "April 16, 2026",
        "categoria": "AI-Business",
        "meta": "In the era of artificial intelligence, social networks are the megaphone, but your website is the source of truth. Here's why, in 2026, your domain is your most valuable asset.",
        "imagen": "imagen1.jpg",
        "cuerpo": """Social networks are the megaphone, but your website is the source of truth. While Instagram and TikTok feed entertainment, AIs feed on the structured index of the web.

Your website is the source of truth
1. AIs don't "listen" to rumors, they read data
Social networks are "walled gardens." Meta and TikTok put up barriers so that Google or OpenAI AIs can't track their content. In contrast, a web with a sitemap (sitemap.xml) is an open invitation for AIs to index your services with precision.

2. The "Professional Passport"
Having your own domain is not just an aesthetic luxury; it's the infrastructure of your business. It is your centralized digital identity.

3. Reflection vs. Impulse
On social networks, speed and the algorithm prevail; on a web, information architecture prevails. This gives search engines E-E-A-T (Experience, Expertise, Authoritativeness, and Trustworthiness) signals.

4. The Trust Crisis and what's "Real"
With the proliferation of deepfakes, a web linked to a registered domain and a physical/legal address offers a layer of validation that a social media profile no longer guarantees.

5. Ownership vs. Renting
If Instagram decides to change its policies today, your audience disappears. Your website is your property.

6. Zero-Party Data (Privacy)
On your web, you own the statistics. On social media, your customers' data belongs to the platform.

7. Automation and AI Agents
In the very near future, your customers' AI agents will enter your web to schedule appointments or buy products. Those agents need a clear interface (your web) to operate.

8. The "Identity Curation" Argument
The process of creating a website requires a reflective pause. That same awareness that you put into writing your web is what AIs detect as signals of authority.

Conclusion:
In the heart of the AI era, the website has not died; it has evolved to become the core of your digital ecosystem.""",
        "fuentes": "http://aiprodig.com"
    },
    {
        "titulo": "Why is traditional 'Agile' slowing down your company in the age of AI?",
        "fecha": "April 16, 2026",
        "categoria": "AI-Automation",
        "meta": "Does Scrum still work in 2024? We analyze why traditional agile methodologies have become slow for SMEs in the face of the explosive speed of AI-assisted development.",
        "imagen": "imagen2.jpg",
        "cuerpo": """In the competitive business landscape, "agility" has been the mantra for the last decade. However, we are witnessing a paradox: the same tools designed to speed up development are, in many cases, becoming the main bottleneck.

The Great Mismatch: From Days to Seconds
Agile methodologies were born in an era where making a change required days of coordination. Today, with AI-assisted development, that same change takes seconds.

Does it make sense to wait for next Monday's Planning meeting for a task that AI solved on Sunday afternoon? Absolutely not.

The Dilemma of "Industrial Agile": Bureaucracy vs. Creation
What many large companies implement today is not real agility; it's "Industrial Agile." Burocracy has been prioritized over value. For an SME using AI, the administrative load of documenting every micro-task consumes more time than the creation itself.

What DOES Still Make Sense: True Agility
• Continuous Delivery of Value: With AI, you can launch functional versions daily.
• User Feedback: Agility must focus obsessively on validating with the real customer.
• Adaptability: The ability to pivot a project is the true competitive advantage.

The New Unit of Measurement: Orchestration Flow
We are measuring progress not in "Story Points," but in **Orchestration Flow**: the efficiency with which an idea is converted into a functional product by an "Augmented Full-Stack" professional.

Conclusion: Less Mechanics, More Value
Real agility in the AI era is not in following a Scrum manual, but in the speed of orchestration and direct adaptability to market feedback.""",
        "fuentes": "ProDig Research Lab"
    }
]

if not os.path.exists(OUTPUT_EN): os.makedirs(OUTPUT_EN)

for data in articles_en:
    html_en = generate_html(data, "en")
    slug_en = create_slug(data['titulo'])
    en_path = os.path.join(OUTPUT_EN, f"{slug_en}.html")
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(html_en)
    print(f"Generated: {en_path}")
