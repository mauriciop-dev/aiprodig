import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.39.7'

export default async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST', 'Access-Control-Allow-Headers': 'Content-Type' } })
  }

  try {
    const supabase = createClient(
      Deno.env.get('INSFORGE_URL') ?? '',
      Deno.env.get('INSFORGE_SERVICE_ROLE_KEY') ?? ''
    )

    const { event, url, lang, user_id } = await req.json()

    const { error } = await supabase.from('events').insert([
      { 
        event_type: event, 
        path: url, 
        lang: lang, 
        user_id: user_id || 'anonymous' 
      }
    ])

    if (error) throw error

    return new Response(JSON.stringify({ success: true }), {
      headers: { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { 
      status: 500,
      headers: { 'Access-Control-Allow-Origin': '*' }
    })
  }
}
