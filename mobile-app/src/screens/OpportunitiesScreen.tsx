import { useEffect, useMemo, useState } from 'react';
import { View, Text, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { supabase } from '../lib/supabase';
import { colors, spacing } from '../lib/theme';
import CompanyCard from '../components/CompanyCard';
import { Company, CompanyStatus, Role } from '../types';

const OpportunitiesScreen = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [roles, setRoles] = useState<Record<number, Role[]>>({});
  const [refreshing, setRefreshing] = useState(false);
  const [updatingId, setUpdatingId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadCompanies = async () => {
    setRefreshing(true);
    try {
      const { data: companyData, error: companyError } = await supabase
        .from('companies')
        .select('*')
        .order('id', { ascending: false })
        .limit(50);

      if (companyError) {
        throw companyError;
      }

      setCompanies(companyData ?? []);

      const ids = (companyData ?? []).map((company) => company.id);
      if (!ids.length) {
        setRoles({});
        return;
      }

      const { data: roleData, error: roleError } = await supabase
        .from('roles')
        .select('*')
        .in('company_id', ids);

      if (roleError) {
        throw roleError;
      }

      const grouped = (roleData ?? []).reduce<Record<number, Role[]>>((acc, role) => {
        const bucket = acc[role.company_id] ?? [];
        bucket.push(role as Role);
        acc[role.company_id] = bucket;
        return acc;
      }, {});

      setRoles(grouped);
      setError(null);
    } catch (err) {
      console.error('Failed to load companies', err);
      setError('Unable to reach Supabase. Double-check env vars and RLS.');
    } finally {
      setRefreshing(false);
    }
  };

  const updateStatus = async (companyId: number, status: CompanyStatus) => {
    setUpdatingId(companyId);
    try {
      const { error: updateError } = await supabase
        .from('companies')
        .update({ status })
        .eq('id', companyId);

      if (updateError) {
        throw updateError;
      }

      setCompanies((prev) =>
        prev.map((company) => (company.id === companyId ? { ...company, status } : company)),
      );
    } catch (err) {
      console.error('Failed to update status', err);
      setError('Could not update status. Check Supabase permissions.');
    } finally {
      setUpdatingId(null);
    }
  };

  useEffect(() => {
    loadCompanies();
  }, []);

  const subtitle = useMemo(() => {
    if (error) return error;
    if (!companies.length) return 'No companies yet — add some from the Capture tab or web app.';
    return 'Tap a status pill to keep your pipeline in sync.';
  }, [companies.length, error]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Opportunities</Text>
      <Text style={styles.subtitle}>{subtitle}</Text>

      <FlatList
        data={companies}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <CompanyCard
            company={item}
            roles={roles[item.id]}
            onUpdateStatus={(status) => updateStatus(item.id, status)}
            isUpdating={updatingId === item.id}
          />
        )}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={loadCompanies} />}
        contentContainerStyle={styles.listContent}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    padding: spacing.lg,
  },
  listContent: {
    paddingBottom: spacing.xl,
  },
  title: {
    color: colors.text,
    fontSize: 24,
    fontWeight: '800',
    marginBottom: spacing.xs,
  },
  subtitle: {
    color: colors.textMuted,
    marginBottom: spacing.lg,
  },
});

export default OpportunitiesScreen;
