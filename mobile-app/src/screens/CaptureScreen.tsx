import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { supabase } from '../lib/supabase';
import { colors, spacing } from '../lib/theme';

const CaptureScreen = () => {
  const [companyName, setCompanyName] = useState('');
  const [companyUrl, setCompanyUrl] = useState('');
  const [careerPageUrl, setCareerPageUrl] = useState('');
  const [notes, setNotes] = useState('');
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);

  const reset = () => {
    setCompanyName('');
    setCompanyUrl('');
    setCareerPageUrl('');
    setNotes('');
  };

  const handleSave = async () => {
    if (!companyName.trim()) {
      setFeedback('Add a company name to save the record.');
      return;
    }

    setSaving(true);
    setFeedback(null);
    try {
      const payload = {
        company_name: companyName.trim(),
        url: companyUrl.trim() || null,
        career_page_url: careerPageUrl.trim() || null,
        notes: notes.trim() || null,
      };

      const { error } = await supabase.from('companies').insert(payload);
      if (error) {
        throw error;
      }

      setFeedback('Saved to Supabase — check the Opportunities tab for it.');
      reset();
    } catch (err) {
      console.error('Unable to save company', err);
      setFeedback('Unable to save. Confirm your anon key has insert rights.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      style={styles.container}
    >
      <Text style={styles.title}>Capture</Text>
      <Text style={styles.subtitle}>Save new companies on the go. Fields are optional beyond name.</Text>

      <View style={styles.form}>
        <Text style={styles.label}>Company name</Text>
        <TextInput
          value={companyName}
          onChangeText={setCompanyName}
          placeholder="Figma"
          placeholderTextColor={colors.textMuted}
          style={styles.input}
        />

        <Text style={styles.label}>Company site</Text>
        <TextInput
          value={companyUrl}
          onChangeText={setCompanyUrl}
          placeholder="https://figma.com"
          placeholderTextColor={colors.textMuted}
          style={styles.input}
          autoCapitalize="none"
        />

        <Text style={styles.label}>Career page</Text>
        <TextInput
          value={careerPageUrl}
          onChangeText={setCareerPageUrl}
          placeholder="https://figma.com/careers"
          placeholderTextColor={colors.textMuted}
          style={styles.input}
          autoCapitalize="none"
        />

        <Text style={styles.label}>Notes</Text>
        <TextInput
          value={notes}
          onChangeText={setNotes}
          placeholder="Why this company, referrals, etc."
          placeholderTextColor={colors.textMuted}
          style={[styles.input, styles.notes]}
          multiline
        />

        <TouchableOpacity style={[styles.button, saving && styles.disabled]} onPress={handleSave} disabled={saving}>
          <Text style={styles.buttonText}>{saving ? 'Saving…' : 'Save to Supabase'}</Text>
        </TouchableOpacity>
        {feedback ? <Text style={styles.feedback}>{feedback}</Text> : null}
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    padding: spacing.lg,
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
  form: {
    backgroundColor: colors.card,
    padding: spacing.lg,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: colors.border,
    gap: spacing.sm,
  },
  label: {
    color: colors.textMuted,
    fontWeight: '600',
  },
  input: {
    backgroundColor: colors.surface,
    color: colors.text,
    borderRadius: 12,
    padding: spacing.md,
    borderWidth: 1,
    borderColor: colors.border,
  },
  notes: {
    height: 120,
    textAlignVertical: 'top',
  },
  button: {
    marginTop: spacing.md,
    backgroundColor: colors.accent,
    borderRadius: 12,
    paddingVertical: spacing.md,
    alignItems: 'center',
  },
  buttonText: {
    color: '#0b1a23',
    fontSize: 16,
    fontWeight: '800',
  },
  feedback: {
    color: colors.textMuted,
    marginTop: spacing.sm,
  },
  disabled: {
    opacity: 0.7,
  },
});

export default CaptureScreen;
