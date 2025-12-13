import 'dotenv/config';

export default ({ config }) => ({
  ...config,
  name: 'Career Finder Mobile',
  slug: 'career-finder-mobile',
  version: '1.0.0',
  orientation: 'portrait',
  scheme: 'careerfinder',
  platforms: ['ios', 'android'],
  userInterfaceStyle: 'light',
  extra: {
    supabaseUrl: process.env.SUPABASE_URL ?? '',
    supabaseAnonKey: process.env.SUPABASE_ANON_KEY ?? '',
  },
  updates: {
    fallbackToCacheTimeout: 0,
  },
  ios: {
    supportsTablet: true,
    bundleIdentifier: 'com.example.careerfindermobile',
  },
  android: {
    package: 'com.example.careerfindermobile',
  },
  plugins: ['expo-secure-store'],
});
