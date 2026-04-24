// ProDig Global Telemetry System
const TELEMETRY_ENDPOINT = 'https://s34xeek7.functions.insforge.app/prodig-telemetry';

const sendTelemetry = async (eventName, metadata = {}) => {
    const payload = {
        event_name: eventName,
        url: window.location.pathname,
        user_lang: navigator.language || navigator.userLanguage,
        timestamp: new Date().toISOString(),
        metadata: {
            ...metadata,
            screen_resolution: `${window.screen.width}x${window.screen.height}`,
            referrer: document.referrer
        }
    };

    try {
        // Usamos keepalive para asegurar que los eventos de cierre de sesión se envíen
        await fetch(TELEMETRY_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            keepalive: true,
            mode: 'cors'
        });
    } catch (e) {}
};

// 1. Carga de página (page_view)
window.addEventListener('DOMContentLoaded', () => sendTelemetry('page_view'));

// 2. Interacciones (botones y enlaces externos)
document.addEventListener('click', (e) => {
    const target = e.target.closest('a, button');
    if (target) {
        const isExternal = target.tagName === 'A' && target.hostname !== window.location.hostname;
        sendTelemetry('interaction', {
            type: target.tagName,
            text: target.innerText?.trim().substring(0, 50),
            id: target.id,
            is_external: isExternal,
            href: target.href
        });
    }
});

// 3. Fin de sesión (session_end)
window.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
        sendTelemetry('session_end', {
            time_on_page: performance.now()
        });
    }
});
