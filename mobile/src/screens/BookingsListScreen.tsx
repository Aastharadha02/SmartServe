import React, { useEffect, useState, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  SafeAreaView,
  RefreshControl,
  Image,
} from 'react-native';
import { 
  Calendar, 
  Clock, 
  ChevronRight, 
  KeyRound, 
  User, 
  RefreshCw,
  Plus
} from 'lucide-react-native';
import { bookingsApi, BookingItem } from '../api/bookings';
import { formatRupee, formatCategoryDisplayName } from '../utils/formatters';
import { getServiceImage } from '../utils/serviceImages';

export const BookingsListScreen = ({ navigation }: any) => {
  const [bookings, setBookings] = useState<BookingItem[]>([]);
  const [filterTab, setFilterTab] = useState<'all' | 'active' | 'completed' | 'cancelled'>('all');
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadBookings = useCallback(async () => {
    try {
      const data = await bookingsApi.getAllBookings();
      setBookings(data);
    } catch (err) {
      console.warn('Failed to load bookings', err);
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadBookings();
    // Auto-sync polling every 5 seconds to keep live with Web and PostgreSQL
    const interval = setInterval(loadBookings, 5000);
    return () => clearInterval(interval);
  }, [loadBookings]);

  const onRefresh = () => {
    setRefreshing(true);
    loadBookings();
  };

  const filteredBookings = bookings.filter((b) => {
    const st = (b.status || '').toLowerCase().trim();
    if (filterTab === 'active') {
      return ['requested', 'assigned', 'accepted', 'on the way', 'arrived', 'started'].includes(st);
    }
    if (filterTab === 'completed') {
      return ['completed', 'paid'].includes(st);
    }
    if (filterTab === 'cancelled') {
      return ['cancelled', 'rejected'].includes(st);
    }
    return true;
  });

  const getStatusBadgeStyle = (statusStr: string) => {
    const s = (statusStr || '').toLowerCase().trim();
    switch (s) {
      case 'requested':
        return { bg: '#FEF3C7', text: '#B45309', border: '#FDE68A' };
      case 'accepted':
        return { bg: '#EFF6FF', text: '#1D4ED8', border: '#BFDBFE' };
      case 'on the way':
        return { bg: '#FFF7ED', text: '#C2410C', border: '#FED7AA' };
      case 'arrived':
        return { bg: '#FAF5FF', text: '#7E22CE', border: '#E9D5FF' };
      case 'started':
        return { bg: '#EEF2FF', text: '#4338CA', border: '#C7D2FE' };
      case 'completed':
      case 'paid':
        return { bg: '#ECFDF5', text: '#065F46', border: '#A7F3D0' };
      case 'cancelled':
      case 'rejected':
        return { bg: '#FEF2F2', text: '#B91C1C', border: '#FECACA' };
      default:
        return { bg: '#F1F5F9', text: '#475569', border: '#CBD5E1' };
    }
  };

  if (isLoading) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2563EB" />
        <Text style={styles.loadingText}>Fetching bookings from backend...</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      {/* Header Bar */}
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>My Service Bookings</Text>
          <Text style={styles.subtitle}>Track live technician dispatches and status updates</Text>
        </View>
        <TouchableOpacity style={styles.refreshIconBtn} onPress={onRefresh} activeOpacity={0.7}>
          <RefreshCw size={16} color="#475569" />
        </TouchableOpacity>
      </View>

      {/* Filter Tabs matching Customer Web */}
      <View style={styles.tabsRow}>
        {[
          { key: 'all', label: `All (${bookings.length})` },
          { key: 'active', label: 'Active' },
          { key: 'completed', label: 'Completed' },
          { key: 'cancelled', label: 'Cancelled' },
        ].map((tab) => {
          const isActive = filterTab === tab.key;
          return (
            <TouchableOpacity
              key={tab.key}
              style={[styles.tabButton, isActive && styles.tabButtonActive]}
              onPress={() => setFilterTab(tab.key as any)}
              activeOpacity={0.8}
            >
              <Text style={[styles.tabButtonText, isActive && styles.tabButtonTextActive]}>
                {tab.label}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>

      {/* Bookings List */}
      {filteredBookings.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Calendar size={48} color="#94A3B8" style={{ marginBottom: 12 }} />
          <Text style={styles.emptyTitle}>No Bookings Found</Text>
          <Text style={styles.emptySubtitle}>
            You have no {filterTab !== 'all' ? filterTab : ''} bookings recorded in your account.
          </Text>
          <TouchableOpacity
            style={styles.bookFirstBtn}
            onPress={() => navigation.navigate('CatalogTab')}
            activeOpacity={0.85}
          >
            <Plus size={16} color="#FFFFFF" style={{ marginRight: 6 }} />
            <Text style={styles.bookFirstText}>Explore Services</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <FlatList
          data={filteredBookings}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.listContainer}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#2563EB']} />}
          showsVerticalScrollIndicator={false}
          renderItem={({ item }) => {
            const badge = getStatusBadgeStyle(item.status);
            const stLower = (item.status || '').toLowerCase().trim();
            const isInTransit = ['on the way', 'arrived'].includes(stLower);
            const imgUrl = getServiceImage(item.category, item.subcategory, item.service_name);

            return (
              <TouchableOpacity
                style={styles.card}
                activeOpacity={0.85}
                onPress={() => navigation.navigate('LiveTracking', { bookingId: item.id })}
              >
                <View style={styles.cardTop}>
                  <Image source={{ uri: imgUrl }} style={styles.serviceThumbnail} />
                  <View style={{ flex: 1 }}>
                    <View style={styles.refRow}>
                      <Text style={styles.refCode}>{item.booking_reference}</Text>
                      <View style={[styles.statusBadge, { backgroundColor: badge.bg, borderColor: badge.border }]}>
                        <Text style={[styles.statusText, { color: badge.text }]}>
                          {item.status.toUpperCase()}
                        </Text>
                      </View>
                    </View>

                    <Text style={styles.serviceName} numberOfLines={1}>{item.service_name}</Text>

                    <View style={styles.metaRow}>
                      <Clock size={12} color="#64748B" />
                      <Text style={styles.metaText}>{item.scheduled_date} at {item.scheduled_time?.slice(0, 5)}</Text>
                    </View>

                    {item.provider_name ? (
                      <View style={styles.metaRow}>
                        <User size={12} color="#64748B" />
                        <Text style={styles.metaText}>
                          Provider: <Text style={{ color: '#0F172A', fontWeight: '700' }}>{item.provider_name}</Text>
                        </Text>
                      </View>
                    ) : (
                      <Text style={styles.awaitingProviderText}>Technician assignment in progress...</Text>
                    )}

                    {(item.start_otp || item.otp_code) && isInTransit && (
                      <View style={styles.otpPill}>
                        <KeyRound size={12} color="#7C3AED" />
                        <Text style={styles.otpText}>Start OTP: <Text style={{ fontWeight: '800' }}>{item.start_otp || item.otp_code}</Text></Text>
                      </View>
                    )}
                    {item.completion_otp && stLower === 'started' && (
                      <View style={[styles.otpPill, { backgroundColor: '#ECFDF5', borderColor: '#A7F3D0' }]}>
                        <KeyRound size={12} color="#059669" />
                        <Text style={[styles.otpText, { color: '#065F46' }]}>Done OTP: <Text style={{ fontWeight: '800' }}>{item.completion_otp}</Text></Text>
                      </View>
                    )}
                  </View>
                </View>

                <View style={styles.cardBottom}>
                  <Text style={styles.priceText}>{formatRupee(item.total_price || item.total_amount)}</Text>
                  <View style={styles.viewDetailRow}>
                    <Text style={styles.viewDetailText}>Live Dispatch & Details</Text>
                    <ChevronRight size={14} color="#2563EB" />
                  </View>
                </View>
              </TouchableOpacity>
            );
          }}
        />
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#FAF9F5' },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#FAF9F5' },
  loadingText: { marginTop: 12, fontSize: 14, color: '#64748B', fontWeight: '600' },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 16,
    paddingBottom: 12,
  },
  title: { fontSize: 22, fontWeight: '800', color: '#0F172A' },
  subtitle: { fontSize: 12, color: '#64748B', marginTop: 2 },
  refreshIconBtn: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#E2E8F0',
    alignItems: 'center',
    justifyContent: 'center',
  },
  tabsRow: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    gap: 8,
    marginBottom: 12,
  },
  tabButton: {
    paddingHorizontal: 12,
    paddingVertical: 7,
    borderRadius: 10,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  tabButtonActive: {
    backgroundColor: '#EFF6FF',
    borderColor: '#2563EB',
  },
  tabButtonText: { fontSize: 12, fontWeight: '600', color: '#64748B' },
  tabButtonTextActive: { color: '#2563EB', fontWeight: '800' },
  listContainer: { paddingHorizontal: 20, paddingBottom: 40 },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    padding: 14,
    marginBottom: 12,
    shadowColor: '#0F172A',
    shadowOpacity: 0.03,
    shadowRadius: 6,
    elevation: 1,
  },
  cardTop: { flexDirection: 'row', gap: 12 },
  serviceThumbnail: { width: 68, height: 68, borderRadius: 12, backgroundColor: '#F1F5F9' },
  refRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 },
  refCode: { fontSize: 11, fontWeight: '800', color: '#64748B', fontFamily: 'monospace' },
  statusBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 6, borderWidth: 1 },
  statusText: { fontSize: 9, fontWeight: '800', letterSpacing: 0.3 },
  serviceName: { fontSize: 15, fontWeight: '800', color: '#0F172A', marginBottom: 4 },
  metaRow: { flexDirection: 'row', alignItems: 'center', gap: 5, marginBottom: 3 },
  metaText: { fontSize: 11, color: '#64748B' },
  awaitingProviderText: { fontSize: 11, color: '#D97706', fontStyle: 'italic', marginBottom: 3 },
  otpPill: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: '#F5F3FF',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#DDD6FE',
    alignSelf: 'flex-start',
    marginTop: 4,
  },
  otpText: { fontSize: 11, fontWeight: '700', color: '#7C3AED' },
  cardBottom: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 12,
    paddingTop: 10,
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
  },
  priceText: { fontSize: 16, fontWeight: '800', color: '#0F172A' },
  viewDetailRow: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  viewDetailText: { fontSize: 12, fontWeight: '700', color: '#2563EB' },
  emptyContainer: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 32, marginTop: 40 },
  emptyTitle: { fontSize: 18, fontWeight: '800', color: '#0F172A', marginBottom: 4 },
  emptySubtitle: { fontSize: 13, color: '#64748B', textAlign: 'center', marginBottom: 20 },
  bookFirstBtn: {
    backgroundColor: '#2563EB',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 12,
    flexDirection: 'row',
    alignItems: 'center',
  },
  bookFirstText: { color: '#FFFFFF', fontSize: 14, fontWeight: '700' },
});
