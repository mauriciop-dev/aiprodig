// Telemetría simple para el Shadow Agent de ProDig
const trackProDigEvent = async (eventName, details = {}) => {
    const payload = {
        event: eventName,
        url: window.location.pathname,
        lang: navigator.language,
        timestamp: new Date().toISOString(),
        ...details
    };

    // Aquí enviaremos los datos al endpoint que InsForge nos genere
    console.log("ProDig Shadow Tracking:", payload);

    try {
        await fetch('TU_ENDPOINT_DE_INSFORGE', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
    } catch (e) {
        // Silencioso para no afectar la UX
    }
};

// Ejemplo: Rastrear cuando alguien ve un proyecto
document.querySelectorAll('.proyecto-card').forEach(card => {
    card.addEventListener('click', () => trackProDigEvent('project_click', { project: card.id }));
});