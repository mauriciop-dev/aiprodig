import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.39.7'

export default async (req: Request) => {
  try {
    const supabase = createClient(
      Deno.env.get('INSFORGE_URL') ?? Deno.env.get('INSFORGE_INTERNAL_URL') ?? '',
      Deno.env.get('INSFORGE_SERVICE_ROLE_KEY') ?? Deno.env.get('SERVICE_ROLE_KEY') ?? Deno.env.get('API_KEY') ?? ''
    )

    // 1. Segmentación Idiomática
    const { data: langData } = await supabase.rpc('analyze_languages') 
    // Nota: Como alternativa usaremos consultas directas si el RPC no existe aún
    
    const { count: totalEvents } = await supabase
      .from('prodig_telemetry')
      .select('*', { count: 'exact', head: true })

    const { count: nonEsEvents } = await supabase
      .from('prodig_telemetry')
      .select('*', { count: 'exact', head: true })
      .not('user_lang', 'ilike', 'es%')

    const { data: internationalPaths } = await supabase
      .from('prodig_telemetry')
      .select('url')
      .not('user_lang', 'ilike', 'es%')
      .limit(10)

    // 2. Análisis de Fricción (Múltiples interacciones en corto tiempo)
    const { data: frictionData } = await supabase
      .from('prodig_telemetry')
      .select('url, event_name, timestamp')
      .eq('event_name', 'interaction')
      // Aquí el agente debería procesar por ventanas de tiempo de 1 min.
      // Por simplicidad en este MVP, reportamos URLs con más clics totales hoy.

    // 3. Vigilancia de Seguridad
    const suspiciousPatterns = ['<script', 'javascript:', 'alert(', 'onclick', 'onerror', '../', '%2e%2e%2f'];
    const { data: securityAlerts } = await supabase
      .from('prodig_telemetry')
      .select('*')
      .or(`url.ilike.%${suspiciousPatterns.join('%,url.ilike.%')}%`)

    // Construcción del Reporte
    const report = {
      timestamp: new Date().toISOString(),
      summary: {
        total_capture: totalEvents,
        international_reach_pct: totalEvents ? (nonEsEvents / totalEvents) * 100 : 0,
        international_top_paths: Array.from(new Set(internationalPaths?.map(p => p.url) || [])),
      },
      friction_analysis: {
          note: "Revisar URLs con ráfagas de interacciones.",
          total_interactions: frictionData?.length || 0
      },
      security_watch: {
        incidents_found: securityAlerts?.length || 0,
        alerts: securityAlerts?.slice(0, 5) || []
      }
    };

    // Guardar en shadow_reports
    const { error: saveError } = await supabase
      .from('shadow_reports')
      .insert([{ report_content: report }])

    if (saveError) throw saveError

    return new Response(JSON.stringify({ 
      success: true, 
      message: "Análisis completado y guardado en shadow_reports",
      report_id: report.timestamp 
    }), {
      headers: { 'Content-Type': 'application/json' }
    })

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { status: 500 })
  }
}
