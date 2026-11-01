import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
  Alert,
  Image,
  Modal,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { 
  ArrowLeft, 
  MapPin, 
  Clock, 
  CreditCard, 
  KeyRound, 
  Camera, 
  CheckCircle2, 
  Banknote,
  Send
} from 'lucide-react-native';
import * as ImagePicker from 'expo-image-picker';
import { providerApi, ProviderBookingItem } from '../../api/provider';
import { formatRupee } from '../../utils/formatters';
import { getFullMediaUrl } from '../../config/api';
import { useLanguage } from '../../i18n/LanguageContext';

export const ProviderJobDetailScreen = ({ route, navigation }: any) => {
  const { bookingId } = route.params;
  const { t } = useLanguage();

  const [booking, setBooking] = useState<ProviderBookingItem | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isActionLoading, setIsActionLoading] = useState(false);

  // OTP Modal
  const [otpModalVisible, setOtpModalVisible] = useState(false);
  const [otpMode, setOtpMode] = useState<'start' | 'complete'>('start');
  const [otpCodeInput, setOtpCodeInput] = useState('');
  const [otpError, setOtpError] = useState<string | null>(null);

  // Cash Collection Modal
  const [cashModalVisible, setCashModalVisible] = useState(false);
  const [cashAmountInput, setCashAmountInput] = useState('');
  const [cashNoteInput, setCashNoteInput] = useState('');

  const loadJob = useCallback(async () => {
    try {
      const data = await providerApi.getBookingDetail(bookingId);
      setBooking(data);
      if (data.total_amount) {
        setCashAmountInput(String(data.total_amount));
      }
    } catch (err: any) {
      console.warn('Failed to load job details', err);
    } finally {
      setIsLoading(false);
    }
  }, [bookingId]);

  useEffect(() => {
    loadJob();
  }, [loadJob]);

  const handleMarkOnTheWay = async () => {
    setIsActionLoading(true);
    try {
      await providerApi.markOnTheWay(bookingId);
      await loadJob();
    } catch (err: any) {
      Alert.alert('Notice', err.response?.data?.detail || 'Failed to update status to On The Way.');
    } finally {
      setIsActionLoading(false);
    }
  };

  const handleMarkArrived = async () => {
    setIsActionLoading(true);
    try {
      await providerApi.markArrived(bookingId);
      await loadJob();
    } catch (err: any) {
      Alert.alert('Notice', err.response?.data?.detail || 'Failed to update status to Arrived.');
    } finally {
      setIsActionLoading(false);
    }
  };

  const handleOpenOtpModal = (mode: 'start' | 'complete') => {
    setOtpMode(mode);
    setOtpCodeInput('');
    setOtpError(null);
    setOtpModalVisible(true);
  };

  const handleSubmitOtp = async () => {
    if (!otpCodeInput.trim()) {
      setOtpError('Please enter the OTP verification code provided by the customer.');
      return;
    }

    setIsActionLoading(true);
    setOtpError(null);
    try {
      if (otpMode === 'start') {
        await providerApi.startJob(bookingId, otpCodeInput.trim());
      } else {
        await providerApi.completeJob(bookingId, otpCodeInput.trim());
      }
      setOtpModalVisible(false);
      await loadJob();
    } catch (err: any) {
      setOtpError(err.response?.data?.detail || 'Invalid OTP code. Please verify with customer.');
    } finally {
      setIsActionLoading(false);
    }
  };

  const handlePickAndUploadPhoto = async (type: 'before' | 'after') => {
    try {
      const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (!permission.granted) {
        Alert.alert('Permission Needed', 'Photo access permission is needed to upload job documentation.');
        return;
      }

      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        quality: 0.8,
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const photoUri = result.assets[0].uri;
        setIsActionLoading(true);
        if (type === 'before') {
          await providerApi.uploadBeforePhoto(bookingId, photoUri);
        } else {
          await providerApi.uploadAfterPhoto(bookingId, photoUri);
        }
        await loadJob();
        Alert.alert('Success', `${type === 'before' ? 'Before-service' : 'After-service'} photo uploaded successfully.`);
      }
    } catch (err: any) {
      Alert.alert('Upload Error', err.response?.data?.detail || 'Failed to upload photo.');
    } finally {
      setIsActionLoading(false);
    }
  };

  const handleReportCash = async () => {
    const amt = parseFloat(cashAmountInput);
    if (isNaN(amt) || amt <= 0) {
      Alert.alert('Amount Required', 'Please enter a valid cash amount.');
      return;
    }

    setIsActionLoading(true);
    try {
      const res = await providerApi.reportCashCollected(bookingId, amt, cashNoteInput.trim());
      setCashModalVisible(false);
      await loadJob();
      Alert.alert('Payment Recorded', res.message || 'Cash collection successfully reported to admin.');
    } catch (err: any) {
      Alert.alert('Error', err.response?.data?.detail || 'Failed to submit cash collection report.');
    } finally {
      setIsActionLoading(false);
    }
  };

  if (isLoading || !booking) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <ActivityIndicator size="large" color="#1E40AF" style={{ marginTop: 40 }} />
      </SafeAreaView>
    );
  }

  const stLower = (booking.status || '').toLowerCase().trim();
  const isAssigned = ['assigned', 'accepted', 'requested'].includes(stLower);
  const isOnTheWay = stLower === 'on the way';
  const isArrived = stLower === 'arrived';
  const isInProgress = ['started', 'in_progress'].includes(stLower);
  const isCompleted = ['completed', 'paid'].includes(stLower);

  return (
    <SafeAreaView style={styles.safeArea} edges={['top', 'bottom']}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <ArrowLeft size={18} color="#0F172A" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>{booking.booking_reference}</Text>
        <View style={{ width: 36 }} />
      </View>

      <ScrollView contentContainerStyle={styles.container}>
        {/* Status Card */}
        <View style={styles.statusBanner}>
          <View>
            <Text style={styles.statusLabel}>CURRENT JOB STAGE</Text>
            <Text style={styles.statusValue}>{booking.status.toUpperCase()}</Text>
          </View>
          <View style={styles.servicePill}>
            <Text style={styles.servicePillText}>{booking.category}</Text>
          </View>
        </View>

        {/* Customer & Address Details */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Customer & Location</Text>
          <View style={styles.row}>
            <MapPin size={16} color="#1E40AF" />
            <Text style={styles.addressText}>
              {booking.address_line1}
              {booking.landmark ? `\nLandmark: ${booking.landmark}` : ''}
              {`\n${booking.city} - ${booking.pincode}`}
            </Text>
          </View>

          <View style={[styles.row, { marginTop: 12 }]}>
            <Clock size={16} color="#64748B" />
            <Text style={styles.metaText}>
              Appointment: {booking.scheduled_date} at {booking.scheduled_time?.slice(0, 5)}
            </Text>
          </View>

          <View style={[styles.row, { marginTop: 8 }]}>
            <CreditCard size={16} color="#64748B" />
            <Text style={styles.metaText}>
              Payment: {booking.payment_method === 'COD' ? 'Cash on Delivery' : 'Online Prepaid'} •{' '}
              <Text style={{ fontWeight: '800', color: '#0F172A' }}>{formatRupee(booking.total_amount)}</Text>
            </Text>
          </View>
        </View>

        {/* Work Proof Photos Gallery */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Proof of Work Documentation</Text>
          <View style={styles.photosRow}>
            {/* Before Photo */}
            <View style={styles.photoBox}>
              <Text style={styles.photoBoxLabel}>Before Service</Text>
              {booking.before_photo_url ? (
                <Image
                  source={{ uri: getFullMediaUrl(booking.before_photo_url) }}
                  style={styles.photoImg}
                />
              ) : (
                <TouchableOpacity
                  style={styles.photoPlaceholder}
                  onPress={() => handlePickAndUploadPhoto('before')}
                  disabled={!isInProgress}
                >
                  <Camera size={22} color={isInProgress ? '#1E40AF' : '#94A3B8'} />
                  <Text style={[styles.photoUploadText, !isInProgress && { color: '#94A3B8' }]}>
                    Upload Photo
                  </Text>
                </TouchableOpacity>
              )}
            </View>

            {/* After Photo */}
            <View style={styles.photoBox}>
              <Text style={styles.photoBoxLabel}>After Service</Text>
              {booking.after_photo_url ? (
                <Image
                  source={{ uri: getFullMediaUrl(booking.after_photo_url) }}
                  style={styles.photoImg}
                />
              ) : (
                <TouchableOpacity
                  style={styles.photoPlaceholder}
                  onPress={() => handlePickAndUploadPhoto('after')}
                  disabled={!isInProgress}
                >
                  <Camera size={22} color={isInProgress ? '#1E40AF' : '#94A3B8'} />
                  <Text style={[styles.photoUploadText, !isInProgress && { color: '#94A3B8' }]}>
                    Upload Photo
                  </Text>
                </TouchableOpacity>
              )}
            </View>
          </View>
        </View>

        {/* Action Controls for State Machine */}
        <View style={styles.actionSection}>
          {isAssigned && (
            <TouchableOpacity
              style={[styles.primaryBtn, isActionLoading && styles.btnDisabled]}
              onPress={handleMarkOnTheWay}
              disabled={isActionLoading}
            >
              {isActionLoading ? (
                <ActivityIndicator color="#FFFFFF" />
              ) : (
                <Text style={styles.primaryBtnText}>Start Trip (On The Way)</Text>
              )}
            </TouchableOpacity>
          )}

          {isOnTheWay && (
            <TouchableOpacity
              style={[styles.primaryBtn, { backgroundColor: '#7E22CE' }, isActionLoading && styles.btnDisabled]}
              onPress={handleMarkArrived}
              disabled={isActionLoading}
            >
              {isActionLoading ? (
                <ActivityIndicator color="#FFFFFF" />
              ) : (
                <Text style={styles.primaryBtnText}>Mark Arrived at Location</Text>
              )}
            </TouchableOpacity>
          )}

          {isArrived && (
            <TouchableOpacity
              style={[styles.primaryBtn, { backgroundColor: '#1E40AF' }]}
              onPress={() => handleOpenOtpModal('start')}
            >
              <KeyRound size={18} color="#FFFFFF" style={{ marginRight: 6 }} />
              <Text style={styles.primaryBtnText}>{t('provider_start_job')}</Text>
            </TouchableOpacity>
          )}

          {isInProgress && (
            <TouchableOpacity
              style={[styles.primaryBtn, { backgroundColor: '#059669' }]}
              onPress={() => handleOpenOtpModal('complete')}
            >
              <CheckCircle2 size={18} color="#FFFFFF" style={{ marginRight: 6 }} />
              <Text style={styles.primaryBtnText}>{t('provider_complete_job')}</Text>
            </TouchableOpacity>
          )}

          {isCompleted && booking.payment_method === 'COD' && (
            <TouchableOpacity
              style={[styles.primaryBtn, { backgroundColor: '#D97706' }]}
              onPress={() => setCashModalVisible(true)}
            >
              <Banknote size={18} color="#FFFFFF" style={{ marginRight: 6 }} />
              <Text style={styles.primaryBtnText}>{t('provider_report_cash')}</Text>
            </TouchableOpacity>
          )}

          {isCompleted && (
            <View style={styles.completedBadgeBox}>
              <CheckCircle2 size={24} color="#059669" />
              <Text style={styles.completedBadgeTitle}>Service Job Completed Successfully</Text>
              <Text style={styles.completedBadgeSub}>
                All customer notifications & 7-day warranty tracking are now active.
              </Text>
            </View>
          )}
        </View>
      </ScrollView>

      {/* OTP Verification Modal */}
      <Modal visible={otpModalVisible} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <KeyRound size={22} color="#1E40AF" />
              <Text style={styles.modalTitle}>
                {otpMode === 'start' ? t('provider_enter_start_otp') : t('provider_enter_completion_otp')}
              </Text>
            </View>
            <Text style={styles.modalSub}>
              {otpMode === 'start'
                ? 'Ask the customer for the 6-digit start code displayed on their screen to begin work.'
                : 'Ask the customer for their 4-digit completion code to verify final delivery.'}
            </Text>

            {otpError && <Text style={styles.modalError}>{otpError}</Text>}

            <TextInput
              style={styles.otpInputField}
              value={otpCodeInput}
              onChangeText={setOtpCodeInput}
              placeholder="••••••"
              placeholderTextColor="#94A3B8"
              keyboardType="number-pad"
              maxLength={6}
              autoFocus
            />

            <View style={styles.modalButtons}>
              <TouchableOpacity
                style={styles.modalCancelBtn}
                onPress={() => setOtpModalVisible(false)}
              >
                <Text style={styles.modalCancelText}>Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.modalSubmitBtn, isActionLoading && styles.btnDisabled]}
                onPress={handleSubmitOtp}
                disabled={isActionLoading}
              >
                {isActionLoading ? (
                  <ActivityIndicator color="#FFFFFF" size="small" />
                ) : (
                  <Text style={styles.modalSubmitText}>Verify & Proceed</Text>
                )}
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

      {/* Cash Collection Modal */}
      <Modal visible={cashModalVisible} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Banknote size={22} color="#D97706" />
              <Text style={styles.modalTitle}>{t('provider_report_cash')}</Text>
            </View>

            <Text style={styles.inputLabel}>{t('provider_cash_amount')}</Text>
            <TextInput
              style={styles.textInput}
              value={cashAmountInput}
              onChangeText={setCashAmountInput}
              keyboardType="numeric"
              placeholder="e.g. 599"
              placeholderTextColor="#94A3B8"
            />

            <Text style={[styles.inputLabel, { marginTop: 10 }]}>{t('provider_receipt_number')}</Text>
            <TextInput
              style={styles.textInput}
              value={cashNoteInput}
              onChangeText={setCashNoteInput}
              placeholder="e.g. Cash collected in full from customer"
              placeholderTextColor="#94A3B8"
            />

            <View style={styles.modalButtons}>
              <TouchableOpacity
                style={styles.modalCancelBtn}
                onPress={() => setCashModalVisible(false)}
              >
                <Text style={styles.modalCancelText}>Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.modalSubmitBtn, { backgroundColor: '#D97706' }, isActionLoading && styles.btnDisabled]}
                onPress={handleReportCash}
                disabled={isActionLoading}
              >
                {isActionLoading ? (
                  <ActivityIndicator color="#FFFFFF" size="small" />
                ) : (
                  <Text style={styles.modalSubmitText}>Submit Report</Text>
                )}
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
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
  headerTitle: { fontSize: 16, fontWeight: '800', color: '#0F172A' },
  container: { padding: 16, paddingBottom: 40 },
  statusBanner: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  statusLabel: { fontSize: 10, fontWeight: '700', color: '#94A3B8', letterSpacing: 0.5 },
  statusValue: { fontSize: 18, fontWeight: '900', color: '#1E40AF', marginTop: 2 },
  servicePill: {
    backgroundColor: '#EFF6FF',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  servicePillText: { fontSize: 11, fontWeight: '700', color: '#1E40AF' },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 16,
  },
  cardTitle: { fontSize: 15, fontWeight: '700', color: '#0F172A', marginBottom: 12 },
  row: { flexDirection: 'row', alignItems: 'flex-start', gap: 8 },
  addressText: { fontSize: 13, color: '#334155', lineHeight: 18, flex: 1 },
  metaText: { fontSize: 13, color: '#64748B' },
  photosRow: { flexDirection: 'row', gap: 12 },
  photoBox: { flex: 1 },
  photoBoxLabel: { fontSize: 11, fontWeight: '600', color: '#64748B', marginBottom: 6 },
  photoPlaceholder: {
    height: 110,
    backgroundColor: '#F8FAFC',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#CBD5E1',
    borderStyle: 'dashed',
    alignItems: 'center',
    justifyContent: 'center',
  },
  photoUploadText: { fontSize: 11, fontWeight: '600', color: '#1E40AF', marginTop: 4 },
  photoImg: { width: '100%', height: 110, borderRadius: 10 },
  actionSection: { marginTop: 8 },
  primaryBtn: {
    flexDirection: 'row',
    backgroundColor: '#1E40AF',
    borderRadius: 10,
    paddingVertical: 14,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10,
  },
  btnDisabled: { opacity: 0.6 },
  primaryBtnText: { color: '#FFFFFF', fontSize: 15, fontWeight: '700' },
  completedBadgeBox: {
    backgroundColor: '#ECFDF5',
    borderRadius: 12,
    padding: 20,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#A7F3D0',
    marginTop: 8,
  },
  completedBadgeTitle: { fontSize: 15, fontWeight: '800', color: '#065F46', marginTop: 8 },
  completedBadgeSub: { fontSize: 12, color: '#047857', textAlign: 'center', marginTop: 4 },
  // Modals
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContent: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 22,
    width: '100%',
    maxWidth: 360,
  },
  modalHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  modalTitle: { fontSize: 16, fontWeight: '800', color: '#0F172A' },
  modalSub: { fontSize: 12, color: '#64748B', marginBottom: 14, lineHeight: 16 },
  modalError: { fontSize: 12, color: '#DC2626', marginBottom: 8 },
  otpInputField: {
    borderWidth: 2,
    borderColor: '#1E40AF',
    borderRadius: 10,
    paddingVertical: 12,
    fontSize: 22,
    textAlign: 'center',
    letterSpacing: 6,
    fontWeight: '800',
    color: '#0F172A',
    backgroundColor: '#F8FAFC',
    marginBottom: 16,
  },
  inputLabel: { fontSize: 12, fontWeight: '600', color: '#475569', marginBottom: 4 },
  textInput: {
    borderWidth: 1,
    borderColor: '#CBD5E1',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 14,
    color: '#0F172A',
    backgroundColor: '#F8FAFC',
    marginBottom: 12,
  },
  modalButtons: { flexDirection: 'row', gap: 10, marginTop: 8 },
  modalCancelBtn: { flex: 1, paddingVertical: 10, alignItems: 'center', borderRadius: 8, backgroundColor: '#F1F5F9' },
  modalCancelText: { fontSize: 13, fontWeight: '600', color: '#64748B' },
  modalSubmitBtn: { flex: 1, paddingVertical: 10, alignItems: 'center', borderRadius: 8, backgroundColor: '#1E40AF' },
  modalSubmitText: { fontSize: 13, fontWeight: '700', color: '#FFFFFF' },
});

