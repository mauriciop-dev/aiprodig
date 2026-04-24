import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.39.7'

export default async (req: Request) => {
  // Manejo de CORS para peticiones desde el sitio web
  if (req.method === 'OPTIONS') {
    return new Response('ok', { 
      headers: { 
        'Access-Control-Allow-Origin': '*', 
        'Access-Control-Allow-Methods': 'POST', 
        'Access-Control-Allow-Headers': 'Content-Type' 
      } 
    })
  }

  try {
    const supabase = createClient(
      Deno.env.get('INSFORGE_URL') ?? '',
      Deno.env.get('INSFORGE_SERVICE_ROLE_KEY') ?? ''
    )

    const body = await req.json()
    
    // Extraer campos según requerimiento
    const { event_name, url, user_lang, timestamp, metadata } = body

    const { data, error } = await supabase
      .from('prodig_telemetry')
      .insert([
        { 
          event_name, 
          url, 
          user_lang, 
          timestamp: timestamp || new Date().toISOString(), 
          metadata: metadata || {} 
        }
      ])

    if (error) throw error

    return new Response(JSON.stringify({ success: true, message: "Data recorded in prodig_telemetry" }), {
      headers: { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      status: 201
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { 
      status: 400,
      headers: { 'Access-Control-Allow-Origin': '*' }
    })
  }
}
