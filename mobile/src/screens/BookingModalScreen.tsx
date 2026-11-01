import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { 
  ArrowLeft, 
  Calendar, 
  Clock, 
  MapPin, 
  CreditCard, 
  Banknote, 
  CheckCircle2, 
  ShieldCheck, 
  UserCheck,
  Tag,
  KeyRound
} from 'lucide-react-native';
import { bookingsApi } from '../api/bookings';
import { couponsApi, CouponValidateResult } from '../api/coupons';
import { formatRupee, formatCategoryDisplayName } from '../utils/formatters';
import { useLanguage } from '../i18n/LanguageContext';

const TIME_SLOTS = [
  '09:00 AM - 11:00 AM',
  '11:00 AM - 01:00 PM',
  '02:00 PM - 04:00 PM',
  '04:00 PM - 06:00 PM',
  '06:00 PM - 08:00 PM',
];

function slotToTime(slot: string): string {
  const startPart = slot.split(' - ')[0].trim();
  const [timePart, ampm] = startPart.split(' ');
  const [hStr, mStr] = timePart.split(':');
  let h = parseInt(hStr, 10);
  if (ampm === 'PM' && h !== 12) h += 12;
  if (ampm === 'AM' && h === 12) h = 0;
  return `${String(h).padStart(2, '0')}:${mStr}:00`;
}

function getNextDates(): Array<{ label: string; dateStr: string }> {
  const dates = [];
  for (let i = 1; i <= 4; i++) {
    const d = new Date();
    d.setDate(d.getDate() + i);
    const dateStr = d.toISOString().split('T')[0];
    const label = i === 1 ? 'Tomorrow' : d.toLocaleDateString('en-IN', { weekday: 'short', month: 'short', day: 'numeric' });
    dates.push({ label, dateStr });
  }
  return dates;
}

export const BookingModalScreen = ({ route, navigation }: any) => {
  const { t } = useLanguage();
  const { service, selectedProvider, selectedAddons, finalPrice } = route.params;

  const nextDates = getNextDates();
  const [selectedDate, setSelectedDate] = useState(nextDates[0].dateStr);
  const [selectedSlot, setSelectedSlot] = useState(TIME_SLOTS[0]);
  const [addressLine1, setAddressLine1] = useState('Flat 402, Sunshine Apartments, Sector 62');
  const [landmark, setLandmark] = useState('Near Fortis Hospital');
  const [city, setCity] = useState('Noida');
  const [pincode, setPincode] = useState('201301');
  const [paymentMethod, setPaymentMethod] = useState<'COD' | 'Online'>('COD');
  const [notes, setNotes] = useState('');

  // Coupon state
  const [couponCodeInput, setCouponCodeInput] = useState('');
  const [isValidatingCoupon, setIsValidatingCoupon] = useState(false);
  const [appliedCoupon, setAppliedCoupon] = useState<CouponValidateResult | null>(null);
  const [couponError, setCouponError] = useState<string | null>(null);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [bookingSuccess, setBookingSuccess] = useState(false);
  const [createdBooking, setCreatedBooking] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const basePrice = finalPrice || service.base_price;
  const discountAmount = appliedCoupon?.is_valid ? Number(appliedCoupon.discount_amount) : 0;
  const payableTotal = Math.max(0, basePrice - discountAmount);

  const handleApplyCoupon = async () => {
    if (!couponCodeInput.trim()) {
      setCouponError('Please enter a coupon code.');
      return;
    }
    setCouponError(null);
    setIsValidatingCoupon(true);
    try {
      const res = await couponsApi.validateCoupon({
        code: couponCodeInput.trim().toUpperCase(),
        subtotal: basePrice,
        service_id: service.id,
        category: service.category,
      });

      if (res.is_valid) {
        setAppliedCoupon(res);
        setCouponError(null);
      } else {
        setAppliedCoupon(null);
        setCouponError(res.message || 'Coupon code is invalid or expired.');
      }
    } catch (err: any) {
      setAppliedCoupon(null);
      setCouponError(err.response?.data?.detail || 'Failed to validate coupon.');
    } finally {
      setIsValidatingCoupon(false);
    }
  };

  const handleRemoveCoupon = () => {
    setAppliedCoupon(null);
    setCouponCodeInput('');
    setCouponError(null);
  };

  const handleConfirmBooking = async () => {
    if (!addressLine1.trim() || addressLine1.trim().length < 5) {
      Alert.alert('Address Required', 'Please enter a valid service delivery address.');
      return;
    }

    setErrorMessage(null);
    setIsSubmitting(true);
    try {
      const result = await bookingsApi.createBooking({
        service_id: service.id,
        service_name: service.name,
        category: service.category,
        scheduled_date: selectedDate,
        scheduled_time: slotToTime(selectedSlot),
        address_line1: addressLine1.trim(),
        landmark: landmark.trim() || undefined,
        city: city.trim() || 'Noida',
        pincode: pincode.trim() || '201301',
        payment_method: paymentMethod,
        notes: notes.trim() || undefined,
        provider_id: selectedProvider?.provider_id || undefined,
      });

      setCreatedBooking(result);
      setBookingSuccess(true);
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setErrorMessage(detail || 'Failed to create booking on backend. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (bookingSuccess && createdBooking) {
    const startOtp = createdBooking.start_otp || createdBooking.otp_code;

    return (
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.successContainer}>
          <View style={styles.successIconBadge}>
            <CheckCircle2 size={48} color="#059669" />
          </View>
          <Text style={styles.successTitle}>{t('booking_success_msg')}</Text>
          <Text style={styles.successSubtitle}>
            Your service request has been confirmed and assigned to SmartServe technicians.
          </Text>

          {/* Reference & Start OTP */}
          <View style={styles.successRefBox}>
            <Text style={styles.successRefLabel}>BOOKING REFERENCE</Text>
            <Text style={styles.successRefValue}>{createdBooking.booking_reference}</Text>

            {startOtp && (
              <View style={styles.otpBanner}>
                <KeyRound size={20} color="#1E40AF" />
                <View style={{ marginLeft: 8 }}>
                  <Text style={styles.otpLabel}>{t('otp_start_label')}</Text>
                  <Text style={styles.otpValue}>{startOtp}</Text>
                  <Text style={styles.otpSub}>{t('otp_start_instruction')}</Text>
                </View>
              </View>
            )}
          </View>

          {/* Warranty Notice */}
          <View style={styles.warrantyCard}>
            <ShieldCheck size={20} color="#059669" />
            <View style={{ marginLeft: 10, flex: 1 }}>
              <Text style={styles.warrantyCardTitle}>{t('warranty_title')}</Text>
              <Text style={styles.warrantyCardText}>{t('warranty_desc')}</Text>
            </View>
          </View>

          <View style={styles.successDetailCard}>
            <Text style={styles.successDetailRow}>
              Service: <Text style={{ fontWeight: '700', color: '#0F172A' }}>{service.name}</Text>
            </Text>
            <Text style={styles.successDetailRow}>
              Date & Time: <Text style={{ fontWeight: '700', color: '#0F172A' }}>{selectedDate} at {selectedSlot.split(' - ')[0]}</Text>
            </Text>
            <Text style={styles.successDetailRow}>
              Total Amount: <Text style={{ fontWeight: '700', color: '#0F172A' }}>{formatRupee(payableTotal)}</Text>
            </Text>
            <Text style={styles.successDetailRow}>
              Payment: <Text style={{ fontWeight: '700', color: '#0F172A' }}>{paymentMethod === 'COD' ? 'Cash on Delivery (Pay after service)' : 'Online UPI'}</Text>
            </Text>
          </View>

          <TouchableOpacity
            style={styles.trackBookingBtn}
            onPress={() => {
              navigation.navigate('LiveTracking', { bookingId: createdBooking.id });
            }}
            activeOpacity={0.85}
          >
            <Text style={styles.trackBookingBtnText}>Track Service Live & View OTP</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.myBookingsBtn}
            onPress={() => {
              navigation.navigate('BookingsTab');
            }}
            activeOpacity={0.7}
          >
            <Text style={styles.myBookingsBtnText}>View in My Bookings</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn} activeOpacity={0.8}>
          <ArrowLeft size={18} color="#0F172A" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>{t('booking_checkout_title')}</Text>
        <View style={{ width: 36 }} />
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {/* Service Summary Card */}
        <View style={styles.serviceSummaryCard}>
          <Text style={styles.summaryCategory}>{formatCategoryDisplayName(service.category)}</Text>
          <Text style={styles.summaryName}>{service.name}</Text>
          <Text style={styles.summaryPrice}>{formatRupee(basePrice)}</Text>
        </View>

        {selectedProvider ? (
          <View style={styles.chosenProviderCard}>
            <UserCheck size={16} color="#059669" />
            <Text style={styles.chosenProviderText}>
              Selected Specialist: <Text style={{ fontWeight: '700' }}>{selectedProvider.full_name}</Text>
            </Text>
          </View>
        ) : null}

        {errorMessage ? (
          <View style={styles.errorBox}>
            <Text style={styles.errorText}>{errorMessage}</Text>
          </View>
        ) : null}

        {/* 1. Date Selection */}
        <View style={styles.formSection}>
          <View style={styles.sectionLabelRow}>
            <Calendar size={15} color="#1E40AF" />
            <Text style={styles.sectionLabel}>{t('booking_date')}</Text>
          </View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginHorizontal: -20, paddingHorizontal: 20 }}>
            {nextDates.map((item) => {
              const isSelected = selectedDate === item.dateStr;
              return (
                <TouchableOpacity
                  key={item.dateStr}
                  style={[styles.dateChip, isSelected && styles.dateChipSelected]}
                  onPress={() => setSelectedDate(item.dateStr)}
                  activeOpacity={0.8}
                >
                  <Text style={[styles.dateChipLabel, isSelected && styles.dateChipLabelSelected]}>
                    {item.label}
                  </Text>
                  <Text style={[styles.dateChipDate, isSelected && styles.dateChipDateSelected]}>
                    {item.dateStr.slice(5)}
                  </Text>
                </TouchableOpacity>
              );
            })}
          </ScrollView>
        </View>

        {/* 2. Time Slot Selection */}
        <View style={styles.formSection}>
          <View style={styles.sectionLabelRow}>
            <Clock size={15} color="#1E40AF" />
            <Text style={styles.sectionLabel}>{t('booking_time')}</Text>
          </View>
          <View style={styles.slotsGrid}>
            {TIME_SLOTS.map((slot) => {
              const isSelected = selectedSlot === slot;
              return (
                <TouchableOpacity
                  key={slot}
                  style={[styles.slotCard, isSelected && styles.slotCardSelected]}
                  onPress={() => setSelectedSlot(slot)}
                  activeOpacity={0.8}
                >
                  <Text style={[styles.slotText, isSelected && styles.slotTextSelected]}>
                    {slot}
                  </Text>
                </TouchableOpacity>
              );
            })}
          </View>
        </View>

        {/* 3. Service Address */}
        <View style={styles.formSection}>
          <View style={styles.sectionLabelRow}>
            <MapPin size={15} color="#1E40AF" />
            <Text style={styles.sectionLabel}>{t('booking_address')}</Text>
          </View>
          <TextInput
            style={styles.textInput}
            placeholder="Flat, House no., Building, Street"
            placeholderTextColor="#94A3B8"
            value={addressLine1}
            onChangeText={setAddressLine1}
          />
          <View style={styles.rowInputs}>
            <TextInput
              style={[styles.textInput, { flex: 1 }]}
              placeholder="Landmark (Optional)"
              placeholderTextColor="#94A3B8"
              value={landmark}
              onChangeText={setLandmark}
            />
            <TextInput
              style={[styles.textInput, { width: 100 }]}
              placeholder="Pincode"
              placeholderTextColor="#94A3B8"
              value={pincode}
              onChangeText={setPincode}
              keyboardType="number-pad"
            />
          </View>
        </View>

        {/* 4. Coupon Code Input */}
        <View style={styles.formSection}>
          <View style={styles.sectionLabelRow}>
            <Tag size={15} color="#1E40AF" />
            <Text style={styles.sectionLabel}>{t('booking_apply_coupon')}</Text>
          </View>
          {appliedCoupon ? (
            <View style={styles.appliedCouponCard}>
              <View style={{ flex: 1 }}>
                <Text style={styles.appliedCouponCode}>{appliedCoupon.code}</Text>
                <Text style={styles.appliedCouponDiscount}>
                  Saved {formatRupee(appliedCoupon.discount_amount)} on this order
                </Text>
              </View>
              <TouchableOpacity onPress={handleRemoveCoupon} style={styles.removeCouponBtn}>
                <Text style={styles.removeCouponText}>Remove</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <View>
              <View style={styles.couponInputRow}>
                <TextInput
                  style={[styles.textInput, { flex: 1, textTransform: 'uppercase' }]}
                  placeholder={t('booking_coupon_placeholder')}
                  placeholderTextColor="#94A3B8"
                  value={couponCodeInput}
                  onChangeText={(val) => {
                    setCouponCodeInput(val);
                    setCouponError(null);
                  }}
                  autoCapitalize="characters"
                />
                <TouchableOpacity
                  style={[styles.applyCouponBtn, isValidatingCoupon && styles.applyCouponBtnDisabled]}
                  onPress={handleApplyCoupon}
                  disabled={isValidatingCoupon}
                >
                  {isValidatingCoupon ? (
                    <ActivityIndicator color="#FFFFFF" size="small" />
                  ) : (
                    <Text style={styles.applyCouponBtnText}>Apply</Text>
                  )}
                </TouchableOpacity>
              </View>
              {couponError && <Text style={styles.couponErrorText}>{couponError}</Text>}
            </View>
          )}
        </View>

        {/* 5. Payment Method */}
        <View style={styles.formSection}>
          <View style={styles.sectionLabelRow}>
            <CreditCard size={15} color="#1E40AF" />
            <Text style={styles.sectionLabel}>{t('booking_payment_method')}</Text>
          </View>
          <View style={styles.paymentMethodRow}>
            <TouchableOpacity
              style={[styles.paymentCard, paymentMethod === 'COD' && styles.paymentCardSelected]}
              onPress={() => setPaymentMethod('COD')}
              activeOpacity={0.8}
            >
              <Banknote size={20} color={paymentMethod === 'COD' ? '#1E40AF' : '#64748B'} />
              <View style={{ marginLeft: 8, flex: 1 }}>
                <Text style={[styles.paymentTitle, paymentMethod === 'COD' && styles.paymentTitleSelected]}>
                  Cash on Delivery
                </Text>
                <Text style={styles.paymentSub}>Pay technician after job completion</Text>
              </View>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.paymentCard, paymentMethod === 'Online' && styles.paymentCardSelected]}
              onPress={() => setPaymentMethod('Online')}
              activeOpacity={0.8}
            >
              <CreditCard size={20} color={paymentMethod === 'Online' ? '#1E40AF' : '#64748B'} />
              <View style={{ marginLeft: 8, flex: 1 }}>
                <Text style={[styles.paymentTitle, paymentMethod === 'Online' && styles.paymentTitleSelected]}>
                  Online / UPI
                </Text>
                <Text style={styles.paymentSub}>Instant digital verification</Text>
              </View>
            </TouchableOpacity>
          </View>
        </View>

        {/* 6. Special Notes */}
        <View style={styles.formSection}>
          <Text style={styles.sectionLabel}>Special Instructions (Optional)</Text>
          <TextInput
            style={[styles.textInput, styles.textArea]}
            placeholder="Gate code, specific preferences, or pet warnings..."
            placeholderTextColor="#94A3B8"
            value={notes}
            onChangeText={setNotes}
            multiline
            numberOfLines={3}
          />
        </View>

        {/* Standardized 7-Day Warranty Guarantee Note */}
        <View style={styles.guaranteeNote}>
          <ShieldCheck size={18} color="#059669" />
          <View style={{ marginLeft: 8, flex: 1 }}>
            <Text style={styles.guaranteeBold}>{t('warranty_title')} (₹0 Fee)</Text>
            <Text style={styles.guaranteeText}>{t('warranty_desc')}</Text>
          </View>
        </View>

        {/* Price Breakdown */}
        <View style={styles.priceBreakdownCard}>
          <View style={styles.breakdownRow}>
            <Text style={styles.breakdownLabel}>Service Base Price</Text>
            <Text style={styles.breakdownValue}>{formatRupee(basePrice)}</Text>
          </View>
          {appliedCoupon && (
            <View style={styles.breakdownRow}>
              <Text style={[styles.breakdownLabel, { color: '#059669' }]}>
                Coupon Discount ({appliedCoupon.code})
              </Text>
              <Text style={[styles.breakdownValue, { color: '#059669' }]}>
                - {formatRupee(discountAmount)}
              </Text>
            </View>
          )}
          <View style={[styles.breakdownRow, styles.breakdownTotalRow]}>
            <Text style={styles.breakdownTotalLabel}>{t('booking_total')}</Text>
            <Text style={styles.breakdownTotalValue}>{formatRupee(payableTotal)}</Text>
          </View>
        </View>

        {/* Submit Button */}
        <TouchableOpacity
          style={[styles.confirmBtn, isSubmitting && styles.confirmBtnDisabled]}
          onPress={handleConfirmBooking}
          disabled={isSubmitting}
          activeOpacity={0.85}
        >
          {isSubmitting ? (
            <ActivityIndicator color="#FFFFFF" size="small" />
          ) : (
            <Text style={styles.confirmBtnText}>
              {t('booking_confirm_button')} • {formatRupee(payableTotal)}
            </Text>
          )}
        </TouchableOpacity>
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
  scrollContent: { padding: 20, paddingBottom: 40 },
  serviceSummaryCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 16,
  },
  summaryCategory: { fontSize: 11, fontWeight: '700', color: '#1E40AF', textTransform: 'uppercase' },
  summaryName: { fontSize: 18, fontWeight: '800', color: '#0F172A', marginTop: 2 },
  summaryPrice: { fontSize: 16, fontWeight: '700', color: '#0F172A', marginTop: 6 },
  chosenProviderCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ECFDF5',
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#A7F3D0',
    marginBottom: 16,
  },
  chosenProviderText: { fontSize: 13, color: '#065F46', marginLeft: 8 },
  errorBox: {
    backgroundColor: '#FEE2E2',
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#F87171',
    marginBottom: 16,
  },
  errorText: { color: '#991B1B', fontSize: 13, fontWeight: '500' },
  formSection: { marginBottom: 20 },
  sectionLabelRow: { flexDirection: 'row', alignItems: 'center', gap: 6, marginBottom: 10 },
  sectionLabel: { fontSize: 13, fontWeight: '700', color: '#1E293B' },
  dateChip: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    paddingVertical: 10,
    paddingHorizontal: 14,
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    alignItems: 'center',
  },
  dateChipSelected: {
    backgroundColor: '#1E40AF',
    borderColor: '#1E40AF',
  },
  dateChipLabel: { fontSize: 12, fontWeight: '600', color: '#64748B' },
  dateChipLabelSelected: { color: '#FFFFFF' },
  dateChipDate: { fontSize: 11, color: '#94A3B8', marginTop: 2 },
  dateChipDateSelected: { color: '#DBEAFE' },
  slotsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  slotCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 8,
    paddingVertical: 8,
    paddingHorizontal: 10,
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  slotCardSelected: {
    backgroundColor: '#EFF6FF',
    borderColor: '#1E40AF',
  },
  slotText: { fontSize: 12, fontWeight: '500', color: '#475569' },
  slotTextSelected: { color: '#1E40AF', fontWeight: '700' },
  textInput: {
    backgroundColor: '#FFFFFF',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#CBD5E1',
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 13,
    color: '#0F172A',
    marginBottom: 8,
  },
  rowInputs: { flexDirection: 'row', gap: 8 },
  textArea: { height: 70, textAlignVertical: 'top' },
  couponInputRow: { flexDirection: 'row', gap: 8 },
  applyCouponBtn: {
    backgroundColor: '#1E40AF',
    borderRadius: 8,
    paddingHorizontal: 16,
    justifyContent: 'center',
    alignItems: 'center',
    height: 42,
  },
  applyCouponBtnDisabled: { opacity: 0.6 },
  applyCouponBtnText: { color: '#FFFFFF', fontWeight: '700', fontSize: 13 },
  appliedCouponCard: {
    backgroundColor: '#ECFDF5',
    borderWidth: 1,
    borderColor: '#A7F3D0',
    padding: 12,
    borderRadius: 8,
    flexDirection: 'row',
    alignItems: 'center',
  },
  appliedCouponCode: { fontSize: 14, fontWeight: '800', color: '#065F46' },
  appliedCouponDiscount: { fontSize: 12, color: '#047857', marginTop: 2 },
  removeCouponBtn: { padding: 4 },
  removeCouponText: { fontSize: 12, fontWeight: '700', color: '#DC2626' },
  couponErrorText: { fontSize: 12, color: '#DC2626', marginTop: 4 },
  paymentMethodRow: { gap: 8 },
  paymentCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    padding: 12,
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  paymentCardSelected: {
    borderColor: '#1E40AF',
    backgroundColor: '#EFF6FF',
  },
  paymentTitle: { fontSize: 13, fontWeight: '700', color: '#334155' },
  paymentTitleSelected: { color: '#1E40AF' },
  paymentSub: { fontSize: 11, color: '#64748B', marginTop: 1 },
  guaranteeNote: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: '#ECFDF5',
    padding: 12,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#A7F3D0',
    marginBottom: 16,
  },
  guaranteeBold: { fontSize: 12, fontWeight: '700', color: '#065F46' },
  guaranteeText: { fontSize: 11, color: '#047857', marginTop: 2, lineHeight: 15 },
  priceBreakdownCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    padding: 14,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 20,
  },
  breakdownRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 6 },
  breakdownLabel: { fontSize: 12, color: '#64748B' },
  breakdownValue: { fontSize: 12, fontWeight: '600', color: '#0F172A' },
  breakdownTotalRow: {
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
    paddingTop: 8,
    marginTop: 4,
    marginBottom: 0,
  },
  breakdownTotalLabel: { fontSize: 14, fontWeight: '800', color: '#0F172A' },
  breakdownTotalValue: { fontSize: 16, fontWeight: '800', color: '#1E40AF' },
  confirmBtn: {
    backgroundColor: '#1E40AF',
    borderRadius: 10,
    paddingVertical: 14,
    alignItems: 'center',
    justifyContent: 'center',
  },
  confirmBtnDisabled: { opacity: 0.6 },
  confirmBtnText: { color: '#FFFFFF', fontSize: 15, fontWeight: '700' },
  // Success View Styles
  successContainer: { flex: 1, padding: 24, alignItems: 'center', justifyContent: 'center' },
  successIconBadge: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#ECFDF5',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  successTitle: { fontSize: 22, fontWeight: '800', color: '#0F172A', textAlign: 'center' },
  successSubtitle: {
    fontSize: 13,
    color: '#64748B',
    textAlign: 'center',
    marginTop: 6,
    lineHeight: 18,
    marginBottom: 20,
  },
  successRefBox: {
    width: '100%',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    alignItems: 'center',
    marginBottom: 12,
  },
  successRefLabel: { fontSize: 10, fontWeight: '700', color: '#94A3B8', letterSpacing: 0.5 },
  successRefValue: { fontSize: 18, fontWeight: '900', color: '#1E40AF', marginVertical: 4 },
  otpBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#EFF6FF',
    borderWidth: 1,
    borderColor: '#BFDBFE',
    borderRadius: 8,
    padding: 10,
    marginTop: 10,
    width: '100%',
  },
  otpLabel: { fontSize: 11, fontWeight: '700', color: '#1E40AF' },
  otpValue: { fontSize: 20, fontWeight: '900', color: '#1E40AF', letterSpacing: 4, marginVertical: 2 },
  otpSub: { fontSize: 10, color: '#3B82F6' },
  warrantyCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ECFDF5',
    borderRadius: 10,
    padding: 12,
    borderWidth: 1,
    borderColor: '#A7F3D0',
    width: '100%',
    marginBottom: 12,
  },
  warrantyCardTitle: { fontSize: 12, fontWeight: '700', color: '#065F46' },
  warrantyCardText: { fontSize: 11, color: '#047857', marginTop: 1 },
  successDetailCard: {
    width: '100%',
    backgroundColor: '#F8FAFC',
    borderRadius: 10,
    padding: 12,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 20,
  },
  successDetailRow: { fontSize: 12, color: '#64748B', marginBottom: 4 },
  trackBookingBtn: {
    backgroundColor: '#1E40AF',
    borderRadius: 10,
    paddingVertical: 14,
    width: '100%',
    alignItems: 'center',
    marginBottom: 10,
  },
  trackBookingBtnText: { color: '#FFFFFF', fontSize: 14, fontWeight: '700' },
  myBookingsBtn: {
    paddingVertical: 12,
    width: '100%',
    alignItems: 'center',
  },
  myBookingsBtnText: { color: '#64748B', fontSize: 13, fontWeight: '600' },
});
