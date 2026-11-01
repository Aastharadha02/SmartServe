import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ArrowLeft, ShieldCheck, Clock, CheckCircle2, AlertTriangle } from 'lucide-react-native';
import { warrantyApi, WarrantyCardResponse } from '../api/warranty';
import { useLanguage } from '../i18n/LanguageContext';

export const WarrantyClaimModalScreen = ({ route, navigation }: any) => {
  const { bookingId, bookingReference, serviceName } = route.params;
  const { t } = useLanguage();

  const [warranty, setWarranty] = useState<WarrantyCardResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [claimSuccess, setClaimSuccess] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    loadWarrantyInfo();
  }, [bookingId]);

  const loadWarrantyInfo = async () => {
    setIsLoading(true);
    try {
      const data = await warrantyApi.getWarrantyCard(bookingId);
      setWarranty(data);
    } catch {
      // offline fallback
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitClaim = async () => {
    if (!description.trim() || description.trim().length < 10) {
      Alert.alert('Details Required', 'Please provide at least 10 characters describing the issue that requires rework.');
      return;
    }

    setIsSubmitting(true);
    try {
      const res = await warrantyApi.submitWarrantyClaim(bookingId, description.trim());
      setClaimSuccess(true);
      setSuccessMsg(res.message);
      loadWarrantyInfo(); // refresh card
    } catch (err: any) {
      Alert.alert('Notice', err.response?.data?.detail || 'Unable to submit warranty claim at this moment.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea} edges={['top', 'bottom']}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <ArrowLeft size={18} color="#0F172A" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>{t('warranty_claim_title')}</Text>
        <View style={{ width: 36 }} />
      </View>

      <ScrollView contentContainerStyle={styles.container} keyboardShouldPersistTaps="handled">
        {isLoading ? (
          <ActivityIndicator size="large" color="#1E40AF" style={{ marginTop: 40 }} />
        ) : (
          <>
            {/* Warranty Badge Header Card */}
            <View style={styles.policyCard}>
              <View style={styles.policyHeader}>
                <ShieldCheck size={28} color="#059669" />
                <View style={{ flex: 1, marginLeft: 10 }}>
                  <Text style={styles.policyTitle}>{t('warranty_title')}</Text>
                  <Text style={styles.policySubtitle}>
                    {warranty?.badge_label || 'Standardized 7-Day Protection'}
                  </Text>
                </View>
              </View>

              <View style={styles.policyDivider} />

              <View style={styles.policyMetaRow}>
                <View style={styles.metaItem}>
                  <Text style={styles.metaLabel}>Duration</Text>
                  <Text style={styles.metaValue}>7 Days</Text>
                </View>
                <View style={styles.metaItem}>
                  <Text style={styles.metaLabel}>Inspection Fee</Text>
                  <Text style={[styles.metaValue, { color: '#059669' }]}>₹0 (Free Rework)</Text>
                </View>
                <View style={styles.metaItem}>
                  <Text style={styles.metaLabel}>Days Left</Text>
                  <Text style={[styles.metaValue, { color: (warranty?.days_remaining || 0) > 0 ? '#1E40AF' : '#DC2626' }]}>
                    {warranty ? `${warranty.days_remaining} Days` : '7 Days'}
                  </Text>
                </View>
              </View>

              <Text style={styles.termsText}>
                {warranty?.terms || '100% Free rework labor if identical issues occur within 7 days of service completion.'}
              </Text>
            </View>

            {/* Service & Booking Details */}
            <View style={styles.serviceBox}>
              <Text style={styles.serviceBoxLabel}>SERVICE</Text>
              <Text style={styles.serviceBoxName}>{serviceName || warranty?.service_name || 'Home Service'}</Text>
              <Text style={styles.serviceBoxRef}>Booking Ref: {bookingReference}</Text>
            </View>

            {/* Claim Status or Submission Form */}
            {warranty?.claim_status && warranty.claim_status !== 'None' ? (
              <View style={styles.activeClaimCard}>
                <View style={styles.activeClaimHeader}>
                  <CheckCircle2 size={20} color="#059669" />
                  <Text style={styles.activeClaimTitle}>Warranty Claim Status: {warranty.claim_status}</Text>
                </View>
                <Text style={styles.activeClaimDesc}>
                  "{warranty.claim_description || 'Rework request registered with our support team.'}"
                </Text>
                {warranty.claim_submitted_at && (
                  <View style={styles.timestampRow}>
                    <Clock size={12} color="#64748B" />
                    <Text style={styles.timestampText}>
                      Submitted on {new Date(warranty.claim_submitted_at).toLocaleDateString()}
                    </Text>
                  </View>
                )}
                <View style={styles.supportNotice}>
                  <Text style={styles.supportNoticeText}>
                    Our quality team has assigned a supervisor to coordinate free rework.
                  </Text>
                </View>
              </View>
            ) : claimSuccess ? (
              <View style={styles.successBanner}>
                <CheckCircle2 size={24} color="#059669" />
                <Text style={styles.successMsg}>{successMsg}</Text>
              </View>
            ) : !warranty?.is_eligible ? (
              <View style={styles.ineligibleBox}>
                <AlertTriangle size={20} color="#D97706" />
                <Text style={styles.ineligibleTitle}>Service Not Eligible for Warranty</Text>
                <Text style={styles.ineligibleText}>
                  Diagnostic or one-time inspection services do not carry the 7-day labor warranty.
                </Text>
              </View>
            ) : (
              <View style={styles.formCard}>
                <Text style={styles.formTitle}>{t('warranty_issue_desc')}</Text>
                <Text style={styles.formSub}>
                  Please detail what went wrong after the service was completed so our team can rectify it.
                </Text>

                <TextInput
                  style={styles.textArea}
                  placeholder="e.g. AC cooling dropped again 2 days after servicing, pipe leaking..."
                  placeholderTextColor="#94A3B8"
                  value={description}
                  onChangeText={setDescription}
                  multiline
                  numberOfLines={4}
                  textAlignVertical="top"
                />

                <TouchableOpacity
                  style={[styles.submitBtn, isSubmitting && styles.submitBtnDisabled]}
                  onPress={handleSubmitClaim}
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <ActivityIndicator color="#FFFFFF" size="small" />
                  ) : (
                    <Text style={styles.submitBtnText}>{t('warranty_submit_claim')}</Text>
                  )}
                </TouchableOpacity>
              </View>
            )}
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#FAF9F5' },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: '#E2E8F0',
    backgroundColor: '#FFFFFF',
  },
  backBtn: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#F1F5F9',
    alignItems: 'center',
    justifyContent: 'center',
  },
  headerTitle: { fontSize: 16, fontWeight: '700', color: '#0F172A' },
  container: { padding: 20 },
  policyCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 16,
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  policyHeader: { flexDirection: 'row', alignItems: 'center' },
  policyTitle: { fontSize: 17, fontWeight: '800', color: '#0F172A' },
  policySubtitle: { fontSize: 12, color: '#059669', fontWeight: '600', marginTop: 1 },
  policyDivider: { height: 1, backgroundColor: '#F1F5F9', marginVertical: 14 },
  policyMetaRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 12 },
  metaItem: { alignItems: 'center' },
  metaLabel: { fontSize: 11, color: '#64748B', fontWeight: '600' },
  metaValue: { fontSize: 14, fontWeight: '800', color: '#0F172A', marginTop: 2 },
  termsText: { fontSize: 11, color: '#64748B', lineHeight: 16, backgroundColor: '#F8FAFC', padding: 8, borderRadius: 6 },
  serviceBox: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    padding: 14,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 16,
  },
  serviceBoxLabel: { fontSize: 10, fontWeight: '700', color: '#94A3B8', letterSpacing: 0.5 },
  serviceBoxName: { fontSize: 15, fontWeight: '700', color: '#0F172A', marginTop: 2 },
  serviceBoxRef: { fontSize: 12, color: '#64748B', marginTop: 2 },
  formCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  formTitle: { fontSize: 15, fontWeight: '700', color: '#0F172A' },
  formSub: { fontSize: 12, color: '#64748B', marginTop: 2, marginBottom: 12, lineHeight: 16 },
  textArea: {
    borderWidth: 1,
    borderColor: '#CBD5E1',
    borderRadius: 8,
    padding: 12,
    fontSize: 13,
    color: '#0F172A',
    height: 100,
    backgroundColor: '#F8FAFC',
    marginBottom: 16,
  },
  submitBtn: {
    backgroundColor: '#1E40AF',
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  submitBtnDisabled: { opacity: 0.6 },
  submitBtnText: { color: '#FFFFFF', fontSize: 14, fontWeight: '700' },
  activeClaimCard: {
    backgroundColor: '#ECFDF5',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: '#A7F3D0',
  },
  activeClaimHeader: { flexDirection: 'row', alignItems: 'center', gap: 6, marginBottom: 8 },
  activeClaimTitle: { fontSize: 14, fontWeight: '700', color: '#065F46' },
  activeClaimDesc: { fontSize: 13, color: '#047857', fontStyle: 'italic', marginBottom: 8 },
  timestampRow: { flexDirection: 'row', alignItems: 'center', gap: 4, marginBottom: 10 },
  timestampText: { fontSize: 11, color: '#64748B' },
  supportNotice: { backgroundColor: '#FFFFFF', padding: 10, borderRadius: 6, borderWidth: 1, borderColor: '#D1FAE5' },
  supportNoticeText: { fontSize: 11, color: '#065F46', fontWeight: '500' },
  successBanner: {
    backgroundColor: '#ECFDF5',
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#A7F3D0',
  },
  successMsg: { fontSize: 13, color: '#065F46', fontWeight: '600', textAlign: 'center', marginTop: 8 },
  ineligibleBox: {
    backgroundColor: '#FFFBEB',
    padding: 18,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#FDE68A',
    alignItems: 'center',
  },
  ineligibleTitle: { fontSize: 14, fontWeight: '700', color: '#92400E', marginTop: 6 },
  ineligibleText: { fontSize: 12, color: '#B45309', textAlign: 'center', marginTop: 4, lineHeight: 16 },
});

