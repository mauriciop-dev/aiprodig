/**
 * chat.js - Experience Engine for ProDig Assistant
 * Features: Three.js Particles, Markdown Rendering, Automated Interaction, A2UI Components
 */

// --- CONFIGURATION ---
const N8N_WEBHOOK_URL = 'https://n8n.automatizarempresa.online/webhook/1d4c933d-2dd1-453d-b413-2481fab30717/chat';
const USER_SESSION_ID = 'prodig_user_' + Math.random().toString(36).substr(2, 9);

// --- A2UI COMPONENTS (10 Artefacts) ---
function getA2UIComponent(type) {
    const components = {
        services: `
            <div class="a2ui-services-grid">
                <div class="a2ui-grid-header">
                    <i class="fas fa-rocket"></i> Servicios ProDig
                </div>
                <div class="a2ui-grid">
                    <div class="a2ui-service-card">
                        <div class="a2ui-service-icon">🌐</div>
                        <div class="a2ui-service-title">Sitios Web IA</div>
                        <div class="a2ui-service-desc">Websites autogestionados con AI</div>
                    </div>
                    <div class="a2ui-service-card">
                        <div class="a2ui-service-icon">🔍</div>
                        <div class="a2ui-service-title">SEO & GEO</div>
                        <div class="a2ui-service-desc">Posicionamiento local y AI</div>
                    </div>
                    <div class="a2ui-service-card">
                        <div class="a2ui-service-icon">💬</div>
                        <div class="a2ui-service-title">Chatbots</div>
                        <div class="a2ui-service-desc">Asistentes IA para tu negocio</div>
                    </div>
                    <div class="a2ui-service-card">
                        <div class="a2ui-service-icon">🎓</div>
                        <div class="a2ui-service-title">Capacitación</div>
                        <div class="a2ui-service-desc">Formación equipo</div>
                    </div>
                </div>
            </div>`,
        contact: `
            <div class="a2ui-contact-form">
                <div class="a2ui-form-header">
                    <i class="fas fa-envelope"></i>
                    <span>Agenda una Consultoría</span>
                </div>
                <form class="a2ui-form" onsubmit="event.preventDefault(); alert('¡Gracias! Te contactaremos pronto.');">
                    <div class="a2ui-form-group">
                        <label>Nombre Completo</label>
                        <input type="text" name="nombre" required placeholder="Tu nombre">
                    </div>
                    <div class="a2ui-form-group">
                        <label>Email</label>
                        <input type="email" name="email" required placeholder="tu@email.com">
                    </div>
                    <div class="a2ui-form-group">
                        <label>Teléfono</label>
                        <input type="tel" name="telefono" placeholder="+57 300 000 0000">
                    </div>
                    <div class="a2ui-form-group">
                        <label>Servicio de Interés</label>
                        <select>
                            <option>Selecciona un servicio</option>
                            <option>Sitios Web IA</option>
                            <option>SEO y GEO</option>
                            <option>Chatbots</option>
                            <option>Consultoría</option>
                        </select>
                    </div>
                    <div class="a2ui-form-group">
                        <label>Mensaje</label>
                        <textarea rows="3" placeholder="¿Cómo podemos ayudarte?"></textarea>
                    </div>
                    <button type="submit" class="a2ui-submit-btn">
                        <i class="fas fa-paper-plane"></i> Enviar Solicitud
                    </button>
                </form>
            </div>`,
        pricing: `
            <div class="a2ui-pricing-table">
                <div class="a2ui-pricing-header">Planes ProDig</div>
                <div class="a2ui-pricing-grid">
                    <div class="a2ui-pricing-card">
                        <div class="a2ui-price-title">Básico</div>
                        <div class="a2ui-price-amount">$299</div>
                        <div class="a2ui-price-period">mes</div>
                        <ul class="a2ui-price-features">
                            <li><i class="fas fa-check"></i> Chatbot básico</li>
                            <li><i class="fas fa-check"></i> 100 msgs/mes</li>
                            <li><i class="fas fa-check"></i> Email support</li>
                        </ul>
                    </div>
                    <div class="a2ui-pricing-card featured">
                        <div class="a2ui-price-badge">Popular</div>
                        <div class="a2ui-price-title">Pro</div>
                        <div class="a2ui-price-amount">$599</div>
                        <div class="a2ui-price-period">mes</div>
                        <ul class="a2ui-price-features">
                            <li><i class="fas fa-check"></i> Chatbot avanzado</li>
                            <li><i class="fas fa-check"></i> 500 msgs/mes</li>
                            <li><i class="fas fa-check"></i> Integraciones</li>
                            <li><i class="fas fa-check"></i> Analytics</li>
                        </ul>
                    </div>
                    <div class="a2ui-pricing-card">
                        <div class="a2ui-price-title">Enterprise</div>
                        <div class="a2ui-price-amount">Custom</div>
                        <div class="a2ui-price-period">contacto</div>
                        <ul class="a2ui-price-features">
                            <li><i class="fas fa-check"></i> Solución completa</li>
                            <li><i class="fas fa-check"></i> Msgs ilimitados</li>
                            <li><i class="fas fa-check"></i> Soporte 24/7</li>
                            <li><i class="fas fa-check"></i> Custom AI</li>
                        </ul>
                    </div>
                </div>
            </div>`,
        automation: `
            <div class="a2ui-process-map">
                <div class="a2ui-process-header">
                    <i class="fas fa-cogs"></i> Proceso de Automatización
                </div>
                <div class="a2ui-process-steps">
                    <div class="a2ui-step">
                        <div class="a2ui-step-num">1</div>
                        <div class="a2ui-step-title">Auditoría</div>
                        <div class="a2ui-step-desc">Analizamos tus procesos</div>
                    </div>
                    <div class="a2ui-step">
                        <div class="a2ui-step-num">2</div>
                        <div class="a2ui-step-title">Diseño</div>
                        <div class="a2ui-step-desc">Creamos el flujo optimizado</div>
                    </div>
                    <div class="a2ui-step">
                        <div class="a2ui-step-num">3</div>
                        <div class="a2ui-step-title">Implementación</div>
                        <div class="a2ui-step-desc">Integramos con tus sistemas</div>
                    </div>
                    <div class="a2ui-step">
                        <div class="a2ui-step-num">4</div>
                        <div class="a2ui-step-title">Medición</div>
                        <div class="a2ui-step-desc">Monitoreamos resultados</div>
                    </div>
                </div>
            </div>`,
        ialocal: `
            <div class="a2ui-benefits-carousel">
                <div class="a2ui-benefits-header">
                    <i class="fas fa-shield-alt"></i> IA Local - Privacidad Primero
                </div>
                <div class="a2ui-benefits-grid">
                    <div class="a2ui-benefit-card">
                        <div class="a2ui-benefit-icon">🔒</div>
                        <div class="a2ui-benefit-title">Datos en tu servidor</div>
                        <div class="a2ui-benefit-desc">Tu información nunca sale de tus sistemas</div>
                    </div>
                    <div class="a2ui-benefit-card">
                        <div class="a2ui-benefit-icon">🌐</div>
                        <div class="a2ui-benefit-title">Funciona sin internet</div>
                        <div class="a2ui-benefit-desc">Operación offline disponible</div>
                    </div>
                    <div class="a2ui-benefit-card">
                        <div class="a2ui-benefit-icon">⚡</div>
                        <div class="a2ui-benefit-title">Respuesta instantánea</div>
                        <div class="a2ui-benefit-desc">Sin latencia de red</div>
                    </div>
                    <div class="a2ui-benefit-card">
                        <div class="a2ui-benefit-icon">🎯</div>
                        <div class="a2ui-benefit-title">100% Personalizable</div>
                        <div class="a2ui-benefit-desc">Entrena con tus datos específicos</div>
                    </div>
                </div>
            </div>`,
        demo: `
            <div class="a2ui-calendar-booking">
                <div class="a2ui-calendar-header">
                    <i class="fas fa-calendar-check"></i> Agenda tu Demo
                </div>
                <div class="a2ui-calendar-body">
                    <div class="a2ui-calendar-info">
                        <p><strong>Demo gratuita de 30 min</strong></p>
                        <p>Conoce cómo ProDig puede transformar tu negocio</p>
                    </div>
                    <div class="a2ui-calendar-slots">
                        <button class="a2ui-time-slot">📅 Hoy - 2:00 PM</button>
                        <button class="a2ui-time-slot">📅 Mañana - 10:00 AM</button>
                        <button class="a2ui-time-slot">📅 Mañana - 3:00 PM</button>
                    </div>
                    <button class="a2ui-calendar-btn" onclick="alert('¡Gracias! Te enviaremos el enlace de la reunión.')">
                        <i class="fas fa-video"></i> Confirmar Demo
                    </button>
                </div>
            </div>`
    };
    return components[type] || null;
}

function renderA2UIArtifact(data) {
    let html = '';
    
    if (data.artifact === 'ServiceGrid') {
        html = `
            <div class="a2ui-services-grid">
                <div class="a2ui-grid-header">
                    <i class="fas fa-rocket"></i> Servicios ProDig
                </div>
                <div class="a2ui-grid">
                    ${data.services.map(s => `
                        <div class="a2ui-service-card">
                            <div class="a2ui-service-icon">${s.icon}</div>
                            <div class="a2ui-service-title">${s.title}</div>
                            <div class="a2ui-service-desc">${s.desc}</div>
                        </div>
                    `).join('')}
                </div>
            </div>`;
    } 
    else if (data.artifact === 'PriceCard') {
        html = `
            <div class="a2ui-pricing-table">
                <div class="a2ui-pricing-header">${data.service_name}</div>
                <div class="a2ui-pricing-grid">
                    ${data.plans.map((p, index) => `
                        <div class="a2ui-pricing-card ${index === 1 ? 'featured' : ''}">
                            ${index === 1 ? '<div class="a2ui-price-badge">Recomendado</div>' : ''}
                            <div class="a2ui-price-title">${p.title}</div>
                            <div class="a2ui-price-amount" style="font-size: 1.5rem; margin: 10px 0;">${p.price}</div>
                            <ul class="a2ui-price-features">
                                ${p.benefits.map(b => `<li><i class="fas fa-check" style="color: #00ff88;"></i> ${b}</li>`).join('')}
                            </ul>
                            <a href="${p.link}" target="_blank" class="a2ui-calendar-btn" style="text-decoration:none; display:inline-block; text-align:center; margin-top:15px; width: 100%;">
                                ${p.cta}
                            </a>
                        </div>
                    `).join('')}
                </div>
            </div>`;
    }
    else if (data.artifact === 'ProcessMap') {
        html = `
            <div class="a2ui-process-map">
                <div class="a2ui-process-header">
                    <i class="fas fa-cogs"></i> Cómo Funciona
                </div>
                <div class="a2ui-process-steps">
                    ${data.steps.map((s, i) => `
                        <div class="a2ui-step">
                            <div class="a2ui-step-num">${i + 1}</div>
                            <div class="a2ui-step-title">${s.title.replace(/^\d+\.\s*/, '')}</div>
                            <div class="a2ui-step-desc">${s.desc}</div>
                        </div>
                    `).join('')}
                </div>
            </div>`;
    }
    else if (data.artifact === 'BenefitsCarousel') {
        html = `
            <div class="a2ui-benefits-carousel">
                <div class="a2ui-benefits-header">
                    <i class="fas fa-star"></i> Beneficios
                </div>
                <div class="a2ui-benefits-grid">
                    ${data.benefits.map(b => `
                        <div class="a2ui-benefit-card">
                            <div class="a2ui-benefit-icon">${b.icon}</div>
                            <div class="a2ui-benefit-title">${b.title}</div>
                            <div class="a2ui-benefit-desc">${b.desc}</div>
                        </div>
                    `).join('')}
                </div>
            </div>`;
    }
    else if (data.artifact === 'FAQ') {
        html = `
            <div class="a2ui-pricing-table">
                <div class="a2ui-pricing-header"><i class="fas fa-question-circle"></i> Preguntas Frecuentes</div>
                <div class="a2ui-pricing-grid" style="display:flex; flex-direction:column; gap:10px; padding: 15px;">
                    ${data.faqs.map(f => `
                        <div class="a2ui-pricing-card" style="text-align: left;">
                            <strong style="color: #9d4edd; display: block; margin-bottom: 8px;">${f.q}</strong>
                            <span style="font-size: 0.9em; color: #ccc;">${f.a}</span>
                        </div>
                    `).join('')}
                </div>
            </div>`;
    }
    else if (data.artifact === 'ContactForm') {
        html = getA2UIComponent('contact');
    }
    
    if (html) {
        addA2UIMessage(html);
    } else {
        // Fallback for unknown artifacts
        addMessage(JSON.stringify(data, null, 2), 'assistant');
    }
}

// --- 1. THREE.JS BACKGROUND MAGIC ---
let scene, camera, renderer, particles, starGeo;

function initThree() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.z = 1;
    camera.rotation.x = Math.PI/2;

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    starGeo = new THREE.BufferGeometry();
    const positions = [];
    const velocities = [];
    
    for (let i=0; i<6000; i++) {
        positions.push(Math.random() * 600 - 300, Math.random() * 600 - 300, Math.random() * 600 - 300);
        velocities.push(0);
    }

    starGeo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    
    let sprite = new THREE.TextureLoader().load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/sprites/circle.png');
    let starMaterial = new THREE.PointsMaterial({
        color: 0x9d4edd,
        size: 0.7,
        map: sprite,
        transparent: true,
        opacity: 0.8
    });

    particles = new THREE.Points(starGeo, starMaterial);
    scene.add(particles);

    window.addEventListener('resize', onWindowResize, false);
    animate();
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    const positions = starGeo.attributes.position.array;
    for (let i = 0; i < positions.length; i += 3) {
        positions[i+1] -= 0.1; // Slow vertical drift
        if (positions[i+1] < -300) {
            positions[i+1] = 300;
        }
    }
    starGeo.attributes.position.needsUpdate = true;
    particles.rotation.y += 0.0008;

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
}

// --- 2. CHAT COMMAND CENTER ---
const chatWindow = document.getElementById('chat-window');
const messagesArea = document.getElementById('messages-area');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const ping = document.getElementById('ping-sound');

// Configure marked.js to be clean
marked.setOptions({
    breaks: true,
    gfm: true,
    headerIds: false
});

async function handleSend() {
    const text = userInput.value.trim();
    if (!text) return;

    // 1. Add User Message
    addMessage(text, 'user');
    userInput.value = '';
    
    // 2. Typing indicator
    const tempId = addTypingIndicator();

    try {
        // 3. Call n8n
        const response = await fetch(N8N_WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                chatInput: text, 
                sessionId: USER_SESSION_ID 
            })
        });

        if (!response.ok) throw new Error('Network error');

        const data = await response.json();
        
        // Remove typing indicator
        document.getElementById(tempId).remove();

        // 4. Extract response (handling n8n array format)
        const botResponse = Array.isArray(data) ? data[0].output : data.output;
        
        // 5. Try to parse A2UI JSON artifact
        try {
            // First try strict parsing (removing markdown code blocks)
            let cleanJson = botResponse.trim();
            if (cleanJson.startsWith('```json')) cleanJson = cleanJson.substring(7);
            else if (cleanJson.startsWith('```')) cleanJson = cleanJson.substring(3);
            if (cleanJson.endsWith('```')) cleanJson = cleanJson.substring(0, cleanJson.length - 3);
            cleanJson = cleanJson.trim();

            let parsed = null;
            try {
                parsed = JSON.parse(cleanJson);
            } catch (e) {
                // If strict parse fails, try to extract JSON using regex (LLM mixed text + JSON)
                const jsonMatch = botResponse.match(/\{[\s\S]*"artifact"[\s\S]*\}/);
                if (jsonMatch) {
                    parsed = JSON.parse(jsonMatch[0]);
                }
            }

            if (parsed && parsed.artifact) {
                renderA2UIArtifact(parsed);
                // Play premium sound
                ping.currentTime = 0;
                ping.play().catch(e => console.log("Audio play blocked by browser"));
                return;
            }
        } catch (e) {
            // Not JSON or missing artifact, fall back to normal markdown text
            console.log("JSON parsing skipped/failed:", e);
        }

        addMessage(botResponse || "Disculpa, no pude procesar tu solicitud.", 'assistant');
        
        // Play premium sound
        ping.currentTime = 0;
        ping.play().catch(e => console.log("Audio play blocked by browser"));

    } catch (error) {
        console.error(error);
        document.getElementById(tempId).remove();
        addMessage("⚠️ Hubo un problema conectando con el servidor ProDig. Por favor intenta de nuevo.", 'assistant');
    }
}

function addMessage(text, side) {
    const div = document.createElement('div');
    div.className = `message ${side}`;
    
    // Convert Markdown to HTML (avoiding literal ## or **)
    div.innerHTML = marked.parse(text);
    
    messagesArea.appendChild(div);
    
    // Auto-scroll to bottom
    chatWindow.scrollTo({
        top: chatWindow.scrollHeight,
        behavior: 'smooth'
    });
}

function addA2UIMessage(htmlContent) {
    const div = document.createElement('div');
    div.className = 'message assistant a2ui-message';
    div.innerHTML = htmlContent;
    messagesArea.appendChild(div);
    chatWindow.scrollTo({
        top: chatWindow.scrollHeight,
        behavior: 'smooth'
    });
}

function addTypingIndicator() {
    const id = 'typing-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = 'message assistant typing';
    div.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
    messagesArea.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return id;
}

// --- INITIALIZE ---
initThree();

sendBtn.addEventListener('click', handleSend);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
});

// Focus input on load
window.onload = () => {
    userInput.focus();
    setTimeout(showQuickReplies, 1500);
};

// Quick Reply Buttons
function showQuickReplies() {
    const quickRepliesDiv = document.createElement('div');
    quickRepliesDiv.className = 'quick-replies';
    quickRepliesDiv.innerHTML = `
        <button onclick="showA2UI('services')">Servicios</button>
        <button onclick="showA2UI('pricing')">Precios</button>
        <button onclick="showA2UI('contact')">Contacto</button>
        <button onclick="showA2UI('demo')">Demo</button>
    `;
    messagesArea.appendChild(quickRepliesDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function showA2UI(type) {
    const component = getA2UIComponent(type);
    if (component) {
        const div = document.createElement('div');
        div.className = 'message assistant a2ui-message';
        div.innerHTML = component;
        messagesArea.appendChild(div);
        chatWindow.scrollTo({ top: chatWindow.scrollHeight, behavior: 'smooth' });
        ping.currentTime = 0;
        ping.play().catch(e => {});
    }
}
