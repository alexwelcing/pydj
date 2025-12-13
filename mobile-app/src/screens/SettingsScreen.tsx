import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { getEnv } from '../lib/env';
import { colors, spacing } from '../lib/theme';

const SettingsScreen = () => {
  const { supabaseUrl } = getEnv();

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Settings</Text>
      <Text style={styles.subtitle}>Environment-driven so you can point at any Supabase project.</Text>

      <View style={styles.card}>
        <Text style={styles.label}>Supabase URL</Text>
        <Text style={styles.value}>{supabaseUrl}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.label}>How to ship</Text>
        <Text style={styles.value}>
          Use Expo Go for quick previews, then `npx expo prebuild` before submitting to the iOS App Store or Google Play.
          The app stays read/write against your Supabase tables so your Django web app and CLI remain in sync.
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    padding: spacing.lg,
    gap: spacing.md,
  },
  title: {
    color: colors.text,
    fontSize: 24,
    fontWeight: '800',
  },
  subtitle: {
    color: colors.textMuted,
    marginBottom: spacing.sm,
  },
  card: {
    backgroundColor: colors.card,
    padding: spacing.lg,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: colors.border,
    gap: spacing.xs,
  },
  label: {
    color: colors.textMuted,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 0.6,
  },
  value: {
    color: colors.text,
    lineHeight: 22,
  },
});

export default SettingsScreen;
