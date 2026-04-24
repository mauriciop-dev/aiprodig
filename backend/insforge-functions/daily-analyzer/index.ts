import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.39.7'

export default async (req: Request) => {
  try {
    const supabase = createClient(
      Deno.env.get('INSFORGE_URL') ?? '',
      Deno.env.get('INSFORGE_SERVICE_ROLE_KEY') ?? ''
    )

    // 1. Análisis de usuarios no hispanohablantes
    const { data: nonEsUsers } = await supabase.rpc('get_non_es_traffic')

    // 2. Detección de Rage Clicks (Bugs posibles)
    const { data: rageClicks } = await supabase.rpc('get_rage_clicks')

    // 3. Seguridad (URLs sospechosas)
    const { data: suspiciousReqs } = await supabase.rpc('get_suspicious_urls')

    const report = `
RESUMEN PARA MAURICIO - REPORTE DE ACTIVIDAD (ÚLTIMAS 24H)
---------------------------------------------------------

🚀 OPORTUNIDADES DETECTADAS (Tráfico Internacional)
${nonEsUsers?.length > 0 
  ? nonEsUsers.map((u: any) => `- Página: ${u.path} (${u.count} visitas de habla no hispana). Considerar traducción prioritaria.`).join('\n')
  : '- Sin tráfico internacional significativo hoy.'}

🐛 POSIBLES BUGS (Detección de Rage Clicks)
${rageClicks?.length > 0 
  ? rageClicks.map((r: any) => `- Fricción en: ${r.path}. Un usuario hizo clic repetidamente ${r.count} veces en < 2s. Revisar interactividad.`).join('\n')
  : '- No se detectaron patrones de frustración (rage clicks).'}

⚠️ ALERTAS DE SEGURIDAD
${suspiciousReqs?.length > 0 
  ? suspiciousReqs.map((s: any) => `- ALERTA: Intento de acceso sospechoso detectado en ${s.path}. Se detectaron caracteres de inyección.`).join('\n')
  : '- Sistema limpio. Sin intentos de inyección detectados.'}
    `;

    console.log(report);

    return new Response(JSON.stringify({ message: "Report generated", report }), {
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { status: 500 })
  }
}
