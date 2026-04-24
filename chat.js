/**
 * chat.js - Experience Engine for ProDig Assistant
 * Features: Three.js Particles, Markdown Rendering, Automated Interaction
 */

// --- CONFIGURATION ---
const N8N_WEBHOOK_URL = 'https://mauricioprodig.app.n8n.cloud/webhook/chatbot-prodig'; // URL detectada o placeholder
const USER_SESSION_ID = 'prodig_user_' + Math.random().toString(36).substr(2, 9);

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
        
        // 5. Add Assistant Message
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
window.onload = () => userInput.focus();
