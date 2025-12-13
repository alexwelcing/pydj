import { memo } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Linking } from 'react-native';
import { colors, shadows, spacing } from '../lib/theme';
import { Company, Role, CompanyStatus } from '../types';

const STATUSES: { label: string; value: CompanyStatus }[] = [
  { label: 'Wishlist', value: 'wishlist' },
  { label: 'Applied', value: 'applied' },
  { label: 'Interviewing', value: 'interviewing' },
  { label: 'Offer', value: 'offer' },
  { label: 'Rejected', value: 'rejected' },
];

interface Props {
  company: Company;
  roles?: Role[];
  onUpdateStatus?: (status: CompanyStatus) => void;
  isUpdating?: boolean;
}

const CompanyCard = ({ company, roles = [], onUpdateStatus, isUpdating }: Props) => {
  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <View style={{ flex: 1 }}>
          <Text style={styles.title}>{company.company_name}</Text>
          {company.url ? (
            <Text
              style={styles.link}
              onPress={() => Linking.openURL(company.url as string)}
              numberOfLines={1}
            >
              {company.url}
            </Text>
          ) : null}
          {company.career_page_url ? (
            <Text
              style={styles.link}
              onPress={() => Linking.openURL(company.career_page_url as string)}
              numberOfLines={1}
            >
              Careers: {company.career_page_url}
            </Text>
          ) : null}
        </View>
        <View style={styles.badge}>
          <Text style={styles.badgeText}>{company.status ?? 'Untracked'}</Text>
        </View>
      </View>

      {company.notes ? <Text style={styles.notes}>{company.notes}</Text> : null}

      {roles.length ? (
        <View style={styles.rolesContainer}>
          {roles.slice(0, 3).map((role) => (
            <View key={`${company.id}-${role.id}`} style={styles.rolePill}>
              <Text style={styles.roleText}>{role.role_title}</Text>
            </View>
          ))}
          {roles.length > 3 ? (
            <Text style={styles.roleOverflow}>+{roles.length - 3} more</Text>
          ) : null}
        </View>
      ) : (
        <Text style={styles.emptyState}>No roles synced yet</Text>
      )}

      {onUpdateStatus ? (
        <View style={styles.actions}>
          {STATUSES.map((status) => (
            <TouchableOpacity
              key={status.value ?? 'none'}
              style={[
                styles.statusButton,
                company.status === status.value && styles.statusButtonActive,
                isUpdating && styles.disabled,
              ]}
              onPress={() => onUpdateStatus(status.value)}
              disabled={isUpdating}
            >
              <Text
                style={[
                  styles.statusText,
                  company.status === status.value && styles.statusTextActive,
                ]}
              >
                {status.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.card,
    borderRadius: 14,
    padding: spacing.md,
    marginBottom: spacing.md,
    gap: spacing.sm,
    borderWidth: 1,
    borderColor: colors.border,
    ...shadows.card,
  },
  header: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  title: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '700',
  },
  link: {
    color: colors.accent,
    marginTop: 2,
  },
  badge: {
    backgroundColor: colors.accent,
    borderRadius: 12,
    paddingHorizontal: spacing.sm,
    paddingVertical: 4,
    alignSelf: 'flex-start',
  },
  badgeText: {
    color: '#0b1a23',
    fontWeight: '600',
  },
  notes: {
    color: colors.textMuted,
    marginTop: spacing.xs,
  },
  rolesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.xs,
  },
  rolePill: {
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.sm,
    paddingVertical: 6,
    borderRadius: 10,
    borderColor: colors.border,
    borderWidth: 1,
  },
  roleText: {
    color: colors.text,
  },
  roleOverflow: {
    color: colors.textMuted,
  },
  emptyState: {
    color: colors.textMuted,
  },
  actions: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.xs,
  },
  statusButton: {
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: spacing.sm,
    paddingVertical: 6,
  },
  statusButtonActive: {
    borderColor: colors.accent,
    backgroundColor: '#1d2d43',
  },
  statusText: {
    color: colors.text,
    fontWeight: '600',
  },
  statusTextActive: {
    color: colors.accent,
  },
  disabled: {
    opacity: 0.6,
  },
});

export default memo(CompanyCard);
