import React, { useEffect, useState, useRef, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  SafeAreaView,
  ScrollView,
  Alert,
  Image,
  RefreshControl,
  Linking,
} from 'react-native';
import { 
  ArrowLeft, 
  RefreshCw, 
  KeyRound, 
  Phone, 
  MessageCircle, 
  ShieldCheck, 
  Star, 
  MapPin, 
  Clock, 
  CreditCard, 
  AlertTriangle,
  CheckCircle2
} from 'lucide-react-native';
import { 
  bookingsApi, 
  BookingItem, 
  BookingLocationResponse, 
  ProviderProfileInfo, 
  ProviderGpsLocation, 
  CustomerLocationInfo 
} from '../api/bookings';
import { MobileLiveMap } from '../components/MobileLiveMap';
import { formatRupee } from '../utils/formatters';
import { DEV_BACKEND_ROOT_URL } from '../config/api';

const PIPELINE_STEPS = [
  { key: 'requested', label: 'Requested' },
  { key: 'accepted', label: 'Accepted' },
  { key: 'on the way', label: 'On The Way' },
  { key: 'arrived', label: 'Arrived' },
  { key: 'started', label: 'Started' },
  { key: 'completed', label: 'Completed' },
];

export const LiveTrackingScreen = ({ route, navigation }: any) => {
  const { bookingId } = route.params;
  const [booking, setBooking] = useState<BookingItem | null>(null);
  const [locationData, setLocationData] = useState<BookingLocationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  const loadData = useCallback(async () => {
    try {
      const [b, loc] = await Promise.all([
        bookingsApi.getBookingById(bookingId),
        bookingsApi.getBookingLocation(bookingId),
      ]);
      setBooking(b);
      setLocationData(loc);
    } catch (err) {
      console.warn('Live tracking data fetch error:', err);
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  }, [bookingId]);

  useEffect(() => {
    loadData();

    // Connect to real backend WebSocket stream
    try {
      const wsUrl = `${DEV_BACKEND_ROOT_URL.replace(/^http/, 'ws')}/ws/stream?channels=bookings,booking_${bookingId}`;
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onmessage = () => {
        loadData();
      };
    } catch (err) {
      console.warn('WS connection notice:', err);
    }

    // Auto-polling fallback every 4 seconds to guarantee synchronization
    const pollInterval = setInterval(loadData, 4000);

    return () => {
      if (wsRef.current) wsRef.current.close();
      clearInterval(pollInterval);
    };
  }, [bookingId, loadData]);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const handleCancelBooking = () => {
    Alert.alert(
      'Cancel Booking',
      'Are you sure you want to cancel this booking? This will notify your technician immediately.',
      [
        { text: 'Keep Booking', style: 'cancel' },
        {
          text: 'Cancel Booking',
          style: 'destructive',
          onPress: async () => {
            try {
              await bookingsApi.cancelBooking(bookingId, 'Cancelled by Customer');
              loadData();
            } catch (err: any) {
              Alert.alert('Error', err.response?.data?.detail || 'Failed to cancel booking.');
            }
          },
        },
      ]
    );
  };

  if (isLoading) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2563EB" />
        <Text style={styles.loadingText}>Connecting to live dispatch stream...</Text>
      </SafeAreaView>
    );
  }

  if (!booking) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <Text style={styles.errorTitle}>Booking Not Found</Text>
        <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
          <Text style={styles.backBtnText}>Go Back</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  const statusLower = (booking.status || '').toLowerCase().trim();
  const currentStepIndex = PIPELINE_STEPS.findIndex((s) => s.key === statusLower);

  const provider: ProviderProfileInfo | null =
    locationData?.provider ||
    (booking.provider_id
      ? {
          provider_id: booking.provider_id,
          full_name: booking.provider_name || 'Assigned Technician',
          experience_years: 6,
          reliability_score: 98.5,
          rating: 4.9,
          is_verified: true,
          service_area: booking.city || 'SmartServe Network',
        }
      : null);

  const providerLocation: ProviderGpsLocation | null = locationData?.provider_location || null;
  const customerLocation: CustomerLocationInfo | null = locationData?.customer_location || {
    latitude: 28.6280,
    longitude: 77.3649,
    address: booking.address_line1,
    city: booking.city,
  };

  // Show Start OTP whenever in transit (On The Way or Arrived)
  const startOtp = booking.start_otp || booking.otp_code;
  const showOtp = Boolean(startOtp && ['requested', 'assigned', 'accepted', 'on the way', 'arrived'].includes(statusLower));
  const completionOtp = booking.completion_otp;
  const showCompletionOtp = Boolean(completionOtp && statusLower === 'started');

  return (
    <SafeAreaView style={styles.safeArea}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.headerBtn} activeOpacity={0.8}>
          <ArrowLeft size={18} color="#0F172A" />
        </TouchableOpacity>
        <View style={{ alignItems: 'center' }}>
          <Text style={styles.headerTitle}>Live Technician Dispatch</Text>
          <Text style={styles.headerRef}>{booking.booking_reference}</Text>
        </View>
        <TouchableOpacity onPress={onRefresh} style={styles.headerBtn} activeOpacity={0.8}>
          <RefreshCw size={16} color="#0F172A" />
        </TouchableOpacity>
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#2563EB']} />}
        showsVerticalScrollIndicator={false}
      >
        {/* Status Hero Card */}
        <View style={styles.statusHeroCard}>
          <View style={styles.statusHeroTop}>
            <View style={styles.statusPill}>
              <View style={styles.statusDot} />
              <Text style={styles.statusText}>{booking.status.toUpperCase()}</Text>
            </View>
            <Text style={styles.serviceName}>{booking.service_name}</Text>
          </View>

          {/* Stepper Pipeline */}
          <View style={styles.stepperContainer}>
            {PIPELINE_STEPS.map((step, idx) => {
              const isPast = idx <= currentStepIndex;
              const isCurrent = idx === currentStepIndex;
              return (
                <View key={step.key} style={styles.stepItem}>
                  <View style={[
                    styles.stepCircle,
                    isPast && styles.stepCirclePast,
                    isCurrent && styles.stepCircleCurrent,
                  ]}>
                    {isPast ? <CheckCircle2 size={12} color="#FFFFFF" /> : null}
                  </View>
                  <Text style={[
                    styles.stepLabel,
                    isPast && styles.stepLabelPast,
                    isCurrent && styles.stepLabelCurrent,
                  ]}>
                    {step.label}
                  </Text>
                </View>
              );
            })}
          </View>
        </View>

        {/* Start Service OTP Box */}
        {showOtp && (
          <View style={styles.otpCard}>
            <View style={styles.otpHeaderRow}>
              <KeyRound size={20} color="#7C3AED" />
              <Text style={styles.otpTitle}>Service Verification Code (OTP)</Text>
            </View>
            <Text style={styles.otpSubtitle}>
              Share this 4-digit code with your technician upon arrival to start the service.
            </Text>

            <View style={styles.otpBoxesRow}>
              {startOtp!.split('').map((digit, i) => (
                <View key={`digit-${i}`} style={styles.otpBox}>
                  <Text style={styles.otpDigit}>{digit}</Text>
                </View>
              ))}
            </View>
            <Text style={styles.otpNotice}>Backend state machine requires this OTP to transition to STARTED.</Text>
          </View>
        )}

        {/* Completion Service OTP Box (Shown only when service is in progress) */}
        {showCompletionOtp && (
          <View style={[styles.otpCard, { backgroundColor: '#ECFDF5', borderColor: '#A7F3D0' }]}>
            <View style={styles.otpHeaderRow}>
              <KeyRound size={20} color="#059669" />
              <Text style={[styles.otpTitle, { color: '#065F46' }]}>Service Completion OTP</Text>
            </View>
            <Text style={[styles.otpSubtitle, { color: '#047857' }]}>
              Share this 4-digit completion code with your technician ONLY after you have inspected the finished work.
            </Text>

            <View style={styles.otpBoxesRow}>
              {completionOtp!.split('').map((digit, i) => (
                <View key={`comp-digit-${i}`} style={[styles.otpBox, { borderColor: '#10B981', backgroundColor: '#FFFFFF' }]}>
                  <Text style={[styles.otpDigit, { color: '#065F46' }]}>{digit}</Text>
                </View>
              ))}
            </View>
            <Text style={[styles.otpNotice, { color: '#059669' }]}>
              After entering this code, technician will record your cash on delivery payment.
            </Text>
          </View>
        )}

        {/* Live OSRM Road Map Canvas */}
        <MobileLiveMap
          providerLocation={providerLocation}
          customerLocation={customerLocation}
          provider={provider}
          bookingStatus={booking.status}
          onRefresh={onRefresh}
        />

        {/* Provider Profile Card */}
        {provider ? (
          <View style={styles.providerCard}>
            <View style={styles.providerTopRow}>
              <Image
                source={{ uri: `https://api.dicebear.com/7.x/avataaars/png?seed=${encodeURIComponent(provider.full_name)}` }}
                style={styles.providerAvatar}
              />
              <View style={{ flex: 1 }}>
                <View style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }}>
                  <Text style={styles.providerName}>{provider.full_name}</Text>
                  <ShieldCheck size={16} color="#059669" />
                </View>
                <Text style={styles.providerArea}>{provider.service_area || 'Verified SmartServe Specialist'}</Text>

                <View style={styles.provStatsRow}>
                  <View style={styles.provStatPill}>
                    <Star size={11} color="#EAB308" fill="#EAB308" />
                    <Text style={styles.provStatText}>{provider.rating || 4.9}</Text>
                  </View>
                  <View style={styles.provStatPill}>
                    <Text style={styles.provStatText}>{provider.reliability_score || 98}% Trust</Text>
                  </View>
                  <View style={styles.provStatPill}>
                    <Text style={styles.provStatText}>{provider.experience_years || 5}+ yrs exp</Text>
                  </View>
                </View>
              </View>
            </View>

            <View style={styles.providerActionRow}>
              <TouchableOpacity
                style={styles.actionBtnCall}
                onPress={() => Linking.openURL('tel:+919876543210')}
                activeOpacity={0.8}
              >
                <Phone size={15} color="#059669" />
                <Text style={styles.actionBtnTextCall}>Call Partner</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.actionBtnChat}
                onPress={() => navigation.navigate('SupportTab', {
                  screen: 'SupportDetail',
                  params: { bookingId: booking.id, subject: `Booking Chat: ${booking.service_name}` }
                })}
                activeOpacity={0.8}
              >
                <MessageCircle size={15} color="#2563EB" />
                <Text style={styles.actionBtnTextChat}>Message Provider</Text>
              </TouchableOpacity>
            </View>
          </View>
        ) : null}

        {/* Appointment & Delivery Address Details */}
        <View style={styles.detailsCard}>
          <Text style={styles.cardHeading}>Service Job Details</Text>

          <View style={styles.detailItem}>
            <Clock size={16} color="#2563EB" />
            <View>
              <Text style={styles.detailLabel}>SCHEDULED APPOINTMENT</Text>
              <Text style={styles.detailValue}>{booking.scheduled_date} at {booking.scheduled_time?.slice(0, 5)}</Text>
            </View>
          </View>

          <View style={styles.detailItem}>
            <MapPin size={16} color="#059669" />
            <View>
              <Text style={styles.detailLabel}>DELIVERY ADDRESS</Text>
              <Text style={styles.detailValue}>{booking.address_line1}, {booking.city} {booking.pincode}</Text>
            </View>
          </View>

          <View style={styles.detailItem}>
            <CreditCard size={16} color="#7C3AED" />
            <View>
              <Text style={styles.detailLabel}>PAYMENT & TOTAL</Text>
              <Text style={styles.detailValue}>{formatRupee(booking.total_price || booking.total_amount)} ({booking.payment_method || 'Cash on Delivery'})</Text>
            </View>
          </View>
        </View>

        {/* Cancel Action if Eligible */}
        {['requested', 'accepted'].includes(statusLower) && (
          <TouchableOpacity
            style={styles.cancelBookingBtn}
            onPress={handleCancelBooking}
            activeOpacity={0.7}
          >
            <Text style={styles.cancelBookingText}>Cancel Service Booking</Text>
          </TouchableOpacity>
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#FAF9F5' },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#FAF9F5' },
  loadingText: { marginTop: 12, fontSize: 14, color: '#64748B', fontWeight: '600' },
  errorTitle: { fontSize: 18, fontWeight: '800', color: '#0F172A', marginBottom: 12 },
  backBtn: { backgroundColor: '#2563EB', paddingHorizontal: 20, paddingVertical: 10, borderRadius: 10 },
  backBtnText: { color: '#FFFFFF', fontWeight: '700' },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 12,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E2E8F0',
  },
  headerBtn: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#F1F5F9',
    alignItems: 'center',
    justifyContent: 'center',
  },
  headerTitle: { fontSize: 15, fontWeight: '800', color: '#0F172A' },
  headerRef: { fontSize: 11, fontWeight: '700', color: '#64748B', fontFamily: 'monospace' },
  scrollContent: { padding: 20, paddingBottom: 40 },
  statusHeroCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 18,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 16,
    shadowColor: '#0F172A',
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 1,
  },
  statusHeroTop: { marginBottom: 16 },
  statusPill: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: '#EFF6FF',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    alignSelf: 'flex-start',
    marginBottom: 6,
  },
  statusDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: '#2563EB' },
  statusText: { fontSize: 11, fontWeight: '800', color: '#1E40AF', letterSpacing: 0.5 },
  serviceName: { fontSize: 18, fontWeight: '800', color: '#0F172A' },
  stepperContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
  },
  stepItem: { alignItems: 'center', gap: 4 },
  stepCircle: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: '#E2E8F0',
    alignItems: 'center',
    justifyContent: 'center',
  },
  stepCirclePast: { backgroundColor: '#059669' },
  stepCircleCurrent: { backgroundColor: '#2563EB', borderWidth: 2, borderColor: '#BFDBFE' },
  stepLabel: { fontSize: 9, fontWeight: '600', color: '#94A3B8' },
  stepLabelPast: { color: '#059669', fontWeight: '700' },
  stepLabelCurrent: { color: '#2563EB', fontWeight: '800' },
  otpCard: {
    backgroundColor: '#FAF5FF',
    borderRadius: 18,
    padding: 16,
    borderWidth: 1.5,
    borderColor: '#C084FC',
    marginBottom: 16,
  },
  otpHeaderRow: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 4 },
  otpTitle: { fontSize: 15, fontWeight: '800', color: '#6B21A8' },
  otpSubtitle: { fontSize: 12, color: '#7E22CE', marginBottom: 12, lineHeight: 16 },
  otpBoxesRow: { flexDirection: 'row', justifyContent: 'center', gap: 12, marginBottom: 10 },
  otpBox: {
    width: 52,
    height: 56,
    borderRadius: 12,
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#A855F7',
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#7C3AED',
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  otpDigit: { fontSize: 26, fontWeight: '900', color: '#581C87' },
  otpNotice: { fontSize: 10, color: '#9333EA', textAlign: 'center', fontWeight: '600' },
  providerCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 18,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 16,
  },
  providerTopRow: { flexDirection: 'row', gap: 12, marginBottom: 14 },
  providerAvatar: { width: 54, height: 54, borderRadius: 27, backgroundColor: '#E2E8F0' },
  providerName: { fontSize: 16, fontWeight: '800', color: '#0F172A' },
  providerArea: { fontSize: 12, color: '#64748B', marginTop: 1, marginBottom: 6 },
  provStatsRow: { flexDirection: 'row', gap: 8 },
  provStatPill: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 3,
    backgroundColor: '#F8FAFC',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  provStatText: { fontSize: 10, fontWeight: '700', color: '#334155' },
  providerActionRow: { flexDirection: 'row', gap: 10 },
  actionBtnCall: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    backgroundColor: '#ECFDF5',
    paddingVertical: 10,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#A7F3D0',
  },
  actionBtnTextCall: { color: '#065F46', fontSize: 13, fontWeight: '700' },
  actionBtnChat: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    backgroundColor: '#EFF6FF',
    paddingVertical: 10,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#BFDBFE',
  },
  actionBtnTextChat: { color: '#1E40AF', fontSize: 13, fontWeight: '700' },
  detailsCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 18,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 16,
    gap: 14,
  },
  cardHeading: { fontSize: 15, fontWeight: '800', color: '#0F172A', marginBottom: 2 },
  detailItem: { flexDirection: 'row', alignItems: 'flex-start', gap: 10 },
  detailLabel: { fontSize: 9, fontWeight: '800', color: '#64748B', letterSpacing: 0.5 },
  detailValue: { fontSize: 13, fontWeight: '700', color: '#0F172A', marginTop: 1 },
  cancelBookingBtn: {
    paddingVertical: 12,
    borderRadius: 12,
    backgroundColor: '#FEF2F2',
    borderWidth: 1,
    borderColor: '#FECACA',
    alignItems: 'center',
  },
  cancelBookingText: { color: '#DC2626', fontSize: 13, fontWeight: '700' },
});
