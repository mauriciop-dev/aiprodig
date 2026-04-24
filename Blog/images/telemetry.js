// Telemetría ProDig Shadow Agent
const API_URL = 'https://s34xeek7.functions.insforge.app/event-tracking';

const trackProDigEvent = async (eventName, details = {}) => {
    const payload = {
        event: eventName,
        url: window.location.pathname,
        lang: navigator.language,
        user_id: localStorage.getItem('prodig_user_id') || 'anon_' + Math.random().toString(36).substr(2, 9),
        ...details
    };

    if (!localStorage.getItem('prodig_user_id')) {
        localStorage.setItem('prodig_user_id', payload.user_id);
    }

    try {
        await fetch(API_URL, {
            method: 'POST',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
    } catch (e) {}
};

// Auto-track: Vista de página
window.addEventListener('DOMContentLoaded', () => trackProDigEvent('page_view'));

// Auto-track: Clics en elementos interactivos
document.addEventListener('click', (e) => {
    const target = e.target.closest('button, a, .interactive');
    if (target) {
        trackProDigEvent('click', { 
            element: target.tagName, 
            text: target.innerText?.substring(0, 30),
            id: target.id 
        });
    }
});