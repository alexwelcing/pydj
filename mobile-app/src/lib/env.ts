import Constants from 'expo-constants';

export const getEnv = () => {
  const supabaseUrl = (Constants.expoConfig?.extra?.supabaseUrl as string | undefined) ?? '';
  const supabaseAnonKey = (Constants.expoConfig?.extra?.supabaseAnonKey as string | undefined) ?? '';

  return { supabaseUrl, supabaseAnonKey };
};
