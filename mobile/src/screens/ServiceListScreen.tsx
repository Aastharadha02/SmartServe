import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  FlatList,
  Image,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  SafeAreaView,
  TextInput,
} from 'react-native';
import { catalogApi, ServiceItem } from '../api/catalog';
import { getServiceImage } from '../utils/serviceImages';
import { formatRupee, formatCategoryDisplayName } from '../utils/formatters';

export const ServiceListScreen = ({ route, navigation }: any) => {
  const { category, subcategory, search } = route.params || {};
  const [services, setServices] = useState<ServiceItem[]>([]);
  const [filteredServices, setFilteredServices] = useState<ServiceItem[]>([]);
  const [searchQuery, setSearchQuery] = useState(search || '');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadServices();
  }, [category, subcategory]);

  const loadServices = async () => {
    try {
      const data = await catalogApi.getAllServices({
        category,
        subcategory,
      });
      setServices(data);
      if (search) {
        setFilteredServices(
          data.filter((s) => s.name.toLowerCase().includes(search.toLowerCase()))
        );
      } else {
        setFilteredServices(data);
      }
    } catch (err) {
      console.warn('Failed to load services', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (text: string) => {
    setSearchQuery(text);
    if (!text.trim()) {
      setFilteredServices(services);
    } else {
      const filtered = services.filter((s) =>
        s.name.toLowerCase().includes(text.toLowerCase()) ||
        (s.description && s.description.toLowerCase().includes(text.toLowerCase()))
      );
      setFilteredServices(filtered);
    }
  };

  if (isLoading) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#1E40AF" />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.header}>
        <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
          <Text style={styles.backBtnText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.title}>
          {subcategory || (category ? formatCategoryDisplayName(category) : 'All Services')}
        </Text>
        <Text style={styles.subtitle}>{filteredServices.length} services available</Text>

        <View style={styles.searchBox}>
          <Text style={styles.searchIcon}>🔍</Text>
          <TextInput
            style={styles.searchInput}
            placeholder="Search within services..."
            placeholderTextColor="#94A3B8"
            value={searchQuery}
            onChangeText={handleSearch}
          />
        </View>
      </View>

      <FlatList
        data={filteredServices}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
        renderItem={({ item }) => {
          const imgUrl = getServiceImage(item.category, item.subcategory, item.name);
          const price = item.final_price || item.base_price;

          return (
            <TouchableOpacity
              style={styles.card}
              activeOpacity={0.85}
              onPress={() => navigation.navigate('ServiceDetail', { serviceId: item.id })}
            >
              <Image source={{ uri: imgUrl }} style={styles.cardImage} />
              <View style={styles.cardContent}>
                <Text style={styles.categoryBadge}>{item.subcategory || formatCategoryDisplayName(item.category)}</Text>
                <Text style={styles.serviceName} numberOfLines={2}>{item.name}</Text>
                {item.description ? (
                  <Text style={styles.serviceDescription} numberOfLines={2}>
                    {item.description}
                  </Text>
                ) : null}

                <View style={styles.cardFooter}>
                  <View>
                    <Text style={styles.priceLabel}>Starting from</Text>
                    <Text style={styles.priceValue}>{formatRupee(price)}</Text>
                  </View>
                  <View style={styles.actionPill}>
                    <Text style={styles.actionText}>View & Book →</Text>
                  </View>
                </View>
              </View>
            </TouchableOpacity>
          );
        }}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#FAF9F5',
  },
  loadingContainer: {
    flex: 1,
    backgroundColor: '#FAF9F5',
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 12,
    paddingBottom: 8,
  },
  backBtn: {
    marginBottom: 8,
  },
  backBtnText: {
    fontSize: 14,
    color: '#2563EB',
    fontWeight: '600',
  },
  title: {
    fontSize: 22,
    fontWeight: '800',
    color: '#0F172A',
  },
  subtitle: {
    fontSize: 13,
    color: '#64748B',
    marginTop: 2,
    marginBottom: 10,
  },
  searchBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  searchIcon: {
    fontSize: 14,
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    fontSize: 14,
    color: '#0F172A',
  },
  listContainer: {
    paddingHorizontal: 20,
    paddingTop: 8,
    paddingBottom: 24,
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    overflow: 'hidden',
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
  },
  cardImage: {
    width: '100%',
    height: 150,
    backgroundColor: '#E2E8F0',
  },
  cardContent: {
    padding: 16,
  },
  categoryBadge: {
    fontSize: 11,
    fontWeight: '600',
    color: '#2563EB',
    textTransform: 'uppercase',
    marginBottom: 4,
  },
  serviceName: {
    fontSize: 17,
    fontWeight: '700',
    color: '#0F172A',
    marginBottom: 6,
  },
  serviceDescription: {
    fontSize: 13,
    color: '#64748B',
    lineHeight: 18,
    marginBottom: 12,
  },
  cardFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
  },
  priceLabel: {
    fontSize: 11,
    color: '#94A3B8',
    fontWeight: '500',
  },
  priceValue: {
    fontSize: 18,
    fontWeight: '800',
    color: '#059669',
  },
  actionPill: {
    backgroundColor: '#EFF6FF',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  actionText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#1E40AF',
  },
});
