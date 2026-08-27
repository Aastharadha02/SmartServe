import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  Image,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  TextInput,
  RefreshControl,
  SafeAreaView,
  Dimensions,
} from 'react-native';
import { catalogApi, ServiceItem } from '../api/catalog';
import { getServiceImage } from '../utils/serviceImages';
import { formatRupee, formatCategoryDisplayName } from '../utils/formatters';
import { useAuth } from '../context/AuthContext';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
const CARD_WIDTH = (SCREEN_WIDTH - 48 - 12) / 2;

export const HomeScreen = ({ navigation }: any) => {
  const { user } = useAuth();
  const [categories, setCategories] = useState<string[]>([]);
  const [popularServices, setPopularServices] = useState<ServiceItem[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [networkError, setNetworkError] = useState(false);

  const fetchData = async () => {
    try {
      setNetworkError(false);
      const [cats, svcs] = await Promise.all([
        catalogApi.getCategories(),
        catalogApi.getAllServices(),
      ]);
      setCategories(cats);
      // Select popular active services
      const active = svcs.filter((s) => s.status === 'active').slice(0, 6);
      setPopularServices(active);
    } catch (err) {
      console.warn('Home fetch error:', err);
      setNetworkError(true);
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchData();
  };

  const handleSearchSubmit = () => {
    if (searchQuery.trim()) {
      navigation.navigate('CatalogTab', {
        screen: 'ServiceList',
        params: { search: searchQuery.trim() },
      });
    }
  };

  if (isLoading) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#1E40AF" />
        <Text style={styles.loadingText}>Loading SmartServe...</Text>
      </SafeAreaView>
    );
  }

  if (networkError) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <View style={styles.errorCard}>
          <Text style={styles.errorTitle}>Unable to connect to SmartServe</Text>
          <Text style={styles.errorSub}>
            Please verify your backend connection or network settings.
          </Text>
          <TouchableOpacity style={styles.retryBtn} onPress={fetchData}>
            <Text style={styles.retryBtnText}>Retry Connection</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        contentContainerStyle={styles.scrollContainer}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        showsVerticalScrollIndicator={false}
      >
        {/* Top Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greetingText}>Welcome back,</Text>
            <Text style={styles.userName}>{user?.email?.split('@')[0] || 'Customer'}</Text>
          </View>
          <View style={styles.badgePill}>
            <Text style={styles.badgeText}>India 🇮🇳</Text>
          </View>
        </View>

        {/* Search Bar */}
        <View style={styles.searchBox}>
          <Text style={styles.searchIcon}>🔍</Text>
          <TextInput
            style={styles.searchInput}
            placeholder="Search home cleaning, salon, AC repair..."
            placeholderTextColor="#94A3B8"
            value={searchQuery}
            onChangeText={setSearchQuery}
            onSubmitEditing={handleSearchSubmit}
            returnKeyType="search"
          />
        </View>

        {/* Banner Promo */}
        <View style={styles.promoCard}>
          <View style={styles.promoContent}>
            <Text style={styles.promoTag}>SMARTSERVE VERIFIED</Text>
            <Text style={styles.promoTitle}>Quality Services, At Your Doorstep</Text>
            <Text style={styles.promoSub}>Professional background-verified technicians</Text>
          </View>
        </View>

        {/* Categories Section */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Explore Categories</Text>
          <TouchableOpacity onPress={() => navigation.navigate('CatalogTab')}>
            <Text style={styles.seeAllText}>View All ({categories.length})</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.categoryGrid}>
          {categories.slice(0, 8).map((cat) => {
            const cleanName = formatCategoryDisplayName(cat);
            const imgUrl = getServiceImage(cat);
            return (
              <TouchableOpacity
                key={cat}
                style={styles.categoryCard}
                activeOpacity={0.8}
                onPress={() =>
                  navigation.navigate('CatalogTab', {
                    screen: 'SubcategoryList',
                    params: { category: cat },
                  })
                }
              >
                <Image source={{ uri: imgUrl }} style={styles.categoryImage} />
                <View style={styles.categoryInfo}>
                  <Text style={styles.categoryName} numberOfLines={2}>
                    {cleanName}
                  </Text>
                </View>
              </TouchableOpacity>
            );
          })}
        </View>

        {/* Popular Services Section */}
        <View style={[styles.sectionHeader, { marginTop: 24 }]}>
          <Text style={styles.sectionTitle}>Trending Services</Text>
        </View>

        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.horizontalScroll}>
          {popularServices.map((svc) => {
            const imgUrl = getServiceImage(svc.category, svc.subcategory, svc.name);
            return (
              <TouchableOpacity
                key={svc.id}
                style={styles.trendingCard}
                activeOpacity={0.85}
                onPress={() => navigation.navigate('ServiceDetail', { serviceId: svc.id })}
              >
                <Image source={{ uri: imgUrl }} style={styles.trendingImage} />
                <View style={styles.trendingInfo}>
                  <Text style={styles.trendingCategory}>{formatCategoryDisplayName(svc.category)}</Text>
                  <Text style={styles.trendingName} numberOfLines={1}>
                    {svc.name}
                  </Text>
                  <View style={styles.trendingPriceRow}>
                    <Text style={styles.priceValue}>{formatRupee(svc.final_price || svc.base_price)}</Text>
                    <Text style={styles.durationBadge}>⏱ {svc.duration_minutes}m</Text>
                  </View>
                </View>
              </TouchableOpacity>
            );
          })}
        </ScrollView>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#FAF9F5',
  },
  scrollContainer: {
    paddingHorizontal: 20,
    paddingBottom: 32,
  },
  loadingContainer: {
    flex: 1,
    backgroundColor: '#FAF9F5',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  loadingText: {
    marginTop: 12,
    fontSize: 14,
    color: '#64748B',
    fontWeight: '500',
  },
  errorCard: {
    backgroundColor: '#FFFFFF',
    padding: 24,
    borderRadius: 16,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  errorTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#0F172A',
    marginBottom: 8,
    textAlign: 'center',
  },
  errorSub: {
    fontSize: 14,
    color: '#64748B',
    textAlign: 'center',
    marginBottom: 16,
  },
  retryBtn: {
    backgroundColor: '#1E40AF',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 10,
  },
  retryBtnText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 16,
    paddingBottom: 16,
  },
  greetingText: {
    fontSize: 13,
    color: '#64748B',
    fontWeight: '500',
  },
  userName: {
    fontSize: 22,
    fontWeight: '800',
    color: '#0F172A',
  },
  badgePill: {
    backgroundColor: '#EEF2F6',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  badgeText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#334155',
  },
  searchBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 18,
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 1,
  },
  searchIcon: {
    fontSize: 16,
    marginRight: 10,
  },
  searchInput: {
    flex: 1,
    fontSize: 14,
    color: '#0F172A',
  },
  promoCard: {
    backgroundColor: '#1E3A8A',
    borderRadius: 16,
    padding: 18,
    marginBottom: 24,
  },
  promoContent: {
    maxWidth: '90%',
  },
  promoTag: {
    fontSize: 11,
    fontWeight: '700',
    color: '#93C5FD',
    letterSpacing: 0.5,
    marginBottom: 4,
  },
  promoTitle: {
    fontSize: 18,
    fontWeight: '800',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  promoSub: {
    fontSize: 13,
    color: '#E0E7FF',
    lineHeight: 18,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 14,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#0F172A',
  },
  seeAllText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#2563EB',
  },
  categoryGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  categoryCard: {
    width: CARD_WIDTH,
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    overflow: 'hidden',
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 1,
  },
  categoryImage: {
    width: '100%',
    height: 100,
    backgroundColor: '#E2E8F0',
  },
  categoryInfo: {
    padding: 10,
    minHeight: 52,
    justifyContent: 'center',
  },
  categoryName: {
    fontSize: 13,
    fontWeight: '600',
    color: '#1E293B',
    lineHeight: 18,
  },
  horizontalScroll: {
    marginHorizontal: -20,
    paddingHorizontal: 20,
  },
  trendingCard: {
    width: 220,
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    overflow: 'hidden',
    marginRight: 14,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 1,
  },
  trendingImage: {
    width: '100%',
    height: 120,
    backgroundColor: '#E2E8F0',
  },
  trendingInfo: {
    padding: 12,
  },
  trendingCategory: {
    fontSize: 11,
    fontWeight: '600',
    color: '#2563EB',
    textTransform: 'uppercase',
    marginBottom: 2,
  },
  trendingName: {
    fontSize: 15,
    fontWeight: '700',
    color: '#0F172A',
    marginBottom: 8,
  },
  trendingPriceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  priceValue: {
    fontSize: 16,
    fontWeight: '800',
    color: '#059669',
  },
  durationBadge: {
    fontSize: 12,
    fontWeight: '500',
    color: '#64748B',
  },
});
