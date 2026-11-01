import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { 
  Briefcase, 
  CheckCircle, 
  Star, 
  Clock, 
  MapPin, 
  ChevronRight, 
  IndianRupee,
  RefreshCw 
} from 'lucide-react-native';
import { providerApi, ProviderBookingItem, ProviderDashboardStats } from '../../api/provider';
import { formatRupee } from '../../utils/formatters';
import { useLanguage } from '../../i18n/LanguageContext';

export const ProviderDashboardScreen = ({ navigation }: any) => {
  const { t } = useLanguage();
  const [stats, setStats] = useState<ProviderDashboardStats | null>(null);
  const [bookings, setBookings] = useState<ProviderBookingItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = useCallback(async () => {
    try {
      const [sData, bData] = await Promise.all([
        providerApi.getDashboardStats(),
        providerApi.getAssignedBookings(),
      ]);
      setStats(sData);
      setBookings(bData);
    } catch (err) {
      console.warn('Failed to fetch provider dashboard data', err);
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, [loadData]);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const getStatusColor = (status: string) => {
    const s = (status || '').toLowerCase();
    switch (s) {
      case 'assigned':
      case 'accepted':
        return { bg: '#EFF6FF', text: '#1E40AF', border: '#BFDBFE' };
      case 'on the way':
        return { bg: '#FFF7ED', text: '#C2410C', border: '#FED7AA' };
      case 'arrived':
        return { bg: '#FAF5FF', text: '#7E22CE', border: '#E9D5FF' };
      case 'started':
      case 'in_progress':
        return { bg: '#EEF2FF', text: '#4338CA', border: '#C7D2FE' };
      case 'completed':
      case 'paid':
        return { bg: '#ECFDF5', text: '#065F46', border: '#A7F3D0' };
      default:
        return { bg: '#F1F5F9', text: '#475569', border: '#CBD5E1' };
    }
  };

  return (
    <SafeAreaView style={styles.safeArea} edges={['top']}>
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>{t('provider_dashboard')}</Text>
          <Text style={styles.subtitle}>Active dispatches & service fulfillment</Text>
        </View>
        <TouchableOpacity style={styles.refreshBtn} onPress={onRefresh}>
          <RefreshCw size={16} color="#475569" />
        </TouchableOpacity>
      </View>

      <ScrollView
        contentContainerStyle={styles.container}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#1E40AF']} />}
      >
        {/* Metric Cards */}
        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <Briefcase size={20} color="#1E40AF" />
            <Text style={styles.statValue}>{bookings.length}</Text>
            <Text style={styles.statLabel}>Assigned Jobs</Text>
          </View>
          <View style={styles.statCard}>
            <CheckCircle size={20} color="#059669" />
            <Text style={styles.statValue}>{stats?.completed_bookings || 0}</Text>
            <Text style={styles.statLabel}>Completed</Text>
          </View>
          <View style={styles.statCard}>
            <Star size={20} color="#F59E0B" />
            <Text style={styles.statValue}>{stats?.rating ? stats.rating.toFixed(1) : '4.9'}</Text>
            <Text style={styles.statLabel}>Rating</Text>
          </View>
          <View style={styles.statCard}>
            <IndianRupee size={20} color="#0F172A" />
            <Text style={styles.statValue}>₹{stats?.total_earnings || 0}</Text>
            <Text style={styles.statLabel}>Earnings</Text>
          </View>
        </View>

        {/* Section Header */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>{t('provider_active_jobs')}</Text>
          <Text style={styles.jobCount}>{bookings.length} Total</Text>
        </View>

        {isLoading ? (
          <ActivityIndicator color="#1E40AF" style={{ marginVertical: 32 }} />
        ) : bookings.length === 0 ? (
          <View style={styles.emptyCard}>
            <Briefcase size={40} color="#94A3B8" style={{ marginBottom: 10 }} />
            <Text style={styles.emptyTitle}>No Jobs Currently Assigned</Text>
            <Text style={styles.emptySubtitle}>
              New customer booking dispatches matching your skills will appear here automatically.
            </Text>
          </View>
        ) : (
          bookings.map((b) => {
            const badge = getStatusColor(b.status);

            return (
              <TouchableOpacity
                key={b.id}
                style={styles.jobCard}
                activeOpacity={0.85}
                onPress={() => navigation.navigate('ProviderJobDetail', { bookingId: b.id })}
              >
                <View style={styles.jobTop}>
                  <View style={{ flex: 1 }}>
                    <Text style={styles.jobRef}>{b.booking_reference}</Text>
                    <Text style={styles.jobServiceName}>{b.service_name}</Text>
                  </View>
                  <View style={[styles.statusBadge, { backgroundColor: badge.bg, borderColor: badge.border }]}>
                    <Text style={[styles.statusText, { color: badge.text }]}>
                      {b.status.toUpperCase()}
                    </Text>
                  </View>
                </View>

                <View style={styles.jobMetaRow}>
                  <Clock size={13} color="#64748B" />
                  <Text style={styles.jobMetaText}>
                    {b.scheduled_date} at {b.scheduled_time?.slice(0, 5)}
                  </Text>
                </View>

                <View style={styles.jobMetaRow}>
                  <MapPin size={13} color="#64748B" />
                  <Text style={styles.jobMetaText} numberOfLines={1}>
                    {b.address_line1}, {b.city}
                  </Text>
                </View>

                <View style={styles.jobBottom}>
                  <View>
                    <Text style={styles.amountLabel}>Total Due</Text>
                    <Text style={styles.amountValue}>{formatRupee(b.total_amount)}</Text>
                  </View>
                  <View style={styles.openJobRow}>
                    <Text style={styles.openJobText}>Manage Job & Verify OTP</Text>
                    <ChevronRight size={14} color="#1E40AF" />
                  </View>
                </View>
              </TouchableOpacity>
            );
          })
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
    paddingTop: 16,
    paddingBottom: 12,
  },
  title: { fontSize: 22, fontWeight: '800', color: '#0F172A' },
  subtitle: { fontSize: 12, color: '#64748B', marginTop: 2 },
  refreshBtn: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#E2E8F0',
    alignItems: 'center',
    justifyContent: 'center',
  },
  container: { padding: 16, paddingBottom: 40 },
  statsGrid: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 20,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  statValue: { fontSize: 16, fontWeight: '800', color: '#0F172A', marginTop: 4 },
  statLabel: { fontSize: 10, color: '#64748B', marginTop: 2, textAlign: 'center' },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: { fontSize: 16, fontWeight: '700', color: '#0F172A' },
  jobCount: { fontSize: 12, fontWeight: '600', color: '#64748B' },
  emptyCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 32,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  emptyTitle: { fontSize: 16, fontWeight: '700', color: '#0F172A', marginBottom: 4 },
  emptySubtitle: { fontSize: 12, color: '#64748B', textAlign: 'center', lineHeight: 16 },
  jobCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 14,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 12,
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
  },
  jobTop: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 6 },
  jobRef: { fontSize: 11, fontWeight: '700', color: '#94A3B8', letterSpacing: 0.5 },
  jobServiceName: { fontSize: 16, fontWeight: '800', color: '#0F172A', marginTop: 1 },
  statusBadge: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: 6, borderWidth: 1 },
  statusText: { fontSize: 10, fontWeight: '800' },
  jobMetaRow: { flexDirection: 'row', alignItems: 'center', gap: 6, marginTop: 4 },
  jobMetaText: { fontSize: 12, color: '#64748B' },
  jobBottom: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
    paddingTop: 10,
    marginTop: 10,
  },
  amountLabel: { fontSize: 10, color: '#94A3B8' },
  amountValue: { fontSize: 15, fontWeight: '800', color: '#0F172A' },
  openJobRow: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  openJobText: { fontSize: 12, fontWeight: '700', color: '#1E40AF' },
});

