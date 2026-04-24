import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.39.7'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

export default async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabase = createClient(
      Deno.env.get('INSFORGE_URL') ?? '',
      Deno.env.get('INSFORGE_SERVICE_ROLE_KEY') ?? ''
    )

    const { article_id } = await req.json()

    if (!article_id) {
      return new Response(JSON.stringify({ error: 'article_id is required' }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 400,
      })
    }

    // Upsert for incrementing (SQL raw query for atomic increment)
    const { data, error } = await supabase.rpc('increment_likes', { art_id: article_id })

    if (error) throw error

    return new Response(JSON.stringify({ message: 'Success', data }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 500,
    })
  }
}
