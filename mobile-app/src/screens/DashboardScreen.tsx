import { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { supabase } from '../lib/supabase';
import { colors, spacing } from '../lib/theme';

interface MetricRow {
  label: string;
  value: number | string;
  helper?: string;
}

const DashboardScreen = () => {
  const [refreshing, setRefreshing] = useState(false);
  const [metrics, setMetrics] = useState<MetricRow[]>([{
    label: 'Companies',
    value: '—',
  }]);

  const loadMetrics = async () => {
    setRefreshing(true);
    try {
      const [{ count: companyCount, error: companyError }, { count: roleCount, error: roleError }] = await Promise.all([
        supabase.from('companies').select('id', { count: 'exact', head: true }),
        supabase.from('roles').select('id', { count: 'exact', head: true }),
      ]);

      if (companyError || roleError) {
        throw companyError ?? roleError;
      }

      setMetrics([
        { label: 'Companies', value: companyCount ?? 0, helper: 'Synced from web or CLI' },
        { label: 'Roles', value: roleCount ?? 0, helper: 'Opportunities connected to companies' },
        { label: 'Focus Ratio', value: formatFocusRatio(companyCount, roleCount) },
      ]);
    } catch (error) {
      console.error('Unable to load metrics', error);
      setMetrics([
        { label: 'Companies', value: '—', helper: 'Check Supabase URL and anon key' },
        { label: 'Roles', value: '—', helper: 'Verify RLS policies for anon access' },
      ]);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  return (
    <ScrollView
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={loadMetrics} />}
    >
      <Text style={styles.title}>Career Finder Mobile</Text>
      <Text style={styles.subtitle}>Tap around from Codespaces, Expo Go, or a simulator.</Text>

      <View style={styles.cardGrid}>
        {metrics.map((metric) => (
          <View key={metric.label} style={styles.metricCard}>
            <Text style={styles.metricLabel}>{metric.label}</Text>
            <Text style={styles.metricValue}>{metric.value}</Text>
            {metric.helper ? <Text style={styles.metricHelper}>{metric.helper}</Text> : null}
          </View>
        ))}
      </View>

      <View style={styles.copyBlock}>
        <Text style={styles.copyHeading}>Built for quick action</Text>
        <Text style={styles.copyText}>
          Use the Opportunities tab to view companies and mark their state without leaving your phone. The Capture
          tab lets you drop in new companies while you are browsing, and everything stays in Supabase for the web app
          and CLI to consume.
        </Text>
      </View>
    </ScrollView>
  );
};

const formatFocusRatio = (companies?: number | null, roles?: number | null) => {
  if (!companies || companies <= 0 || !roles) return '—';
  return `${(roles / companies).toFixed(1)} roles/company`;
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    padding: spacing.lg,
  },
  title: {
    color: colors.text,
    fontSize: 26,
    fontWeight: '800',
    marginBottom: spacing.xs,
  },
  subtitle: {
    color: colors.textMuted,
    marginBottom: spacing.lg,
  },
  cardGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.md,
  },
  metricCard: {
    backgroundColor: colors.card,
    padding: spacing.md,
    borderRadius: 14,
    borderColor: colors.border,
    borderWidth: 1,
    width: '46%',
  },
  metricLabel: {
    color: colors.textMuted,
    fontSize: 12,
    marginBottom: spacing.xs,
    textTransform: 'uppercase',
    letterSpacing: 0.6,
  },
  metricValue: {
    color: colors.text,
    fontSize: 28,
    fontWeight: '800',
    marginBottom: spacing.xs,
  },
  metricHelper: {
    color: colors.textMuted,
  },
  copyBlock: {
    marginTop: spacing.xl,
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: colors.border,
  },
  copyHeading: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '700',
    marginBottom: spacing.sm,
  },
  copyText: {
    color: colors.textMuted,
    lineHeight: 22,
  },
});

export default DashboardScreen;
