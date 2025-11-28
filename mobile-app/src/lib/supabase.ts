import { createClient } from '@supabase/supabase-js';
import { getEnv } from './env';

const { supabaseUrl, supabaseAnonKey } = getEnv();

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn('Supabase URL or anon key missing. Set SUPABASE_URL and SUPABASE_ANON_KEY in .env');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: false,
  },
});
