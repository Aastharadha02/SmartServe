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
} from 'react-native';
import { catalogApi, ServiceItem } from '../api/catalog';
import { getServiceImage } from '../utils/serviceImages';
import { formatCategoryDisplayName } from '../utils/formatters';

export const SubcategoryListScreen = ({ route, navigation }: any) => {
  const { category } = route.params;
  const [subcategories, setSubcategories] = useState<Array<{ name: string; count: number }>>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadSubcategories();
  }, [category]);

  const loadSubcategories = async () => {
    try {
      const services = await catalogApi.getAllServices({ category });
      const map: Record<string, number> = {};
      services.forEach((s) => {
        const sub = s.subcategory || 'General';
        map[sub] = (map[sub] || 0) + 1;
      });
      const list = Object.entries(map).map(([name, count]) => ({ name, count }));
      setSubcategories(list);
    } catch (err) {
      console.warn('Failed to load subcategories', err);
    } finally {
      setIsLoading(false);
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
          <Text style={styles.backBtnText}>← Categories</Text>
        </TouchableOpacity>
        <Text style={styles.title}>{formatCategoryDisplayName(category)}</Text>
        <Text style={styles.subtitle}>{subcategories.length} specialized subcategories</Text>
      </View>

      <FlatList
        data={subcategories}
        keyExtractor={(item) => item.name}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
        renderItem={({ item }) => {
          const imgUrl = getServiceImage(category, item.name);

          return (
            <TouchableOpacity
              style={styles.card}
              activeOpacity={0.85}
              onPress={() =>
                navigation.navigate('ServiceList', {
                  category,
                  subcategory: item.name,
                })
              }
            >
              <Image source={{ uri: imgUrl }} style={styles.cardImage} />
              <View style={styles.cardOverlay}>
                <View>
                  <Text style={styles.cardTitle}>{item.name}</Text>
                  <Text style={styles.cardCount}>{item.count} services available</Text>
                </View>
                <Text style={styles.cardAction}>View Services →</Text>
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
    marginBottom: 8,
  },
  listContainer: {
    paddingHorizontal: 20,
    paddingTop: 8,
    paddingBottom: 24,
  },
  card: {
    height: 120,
    borderRadius: 16,
    overflow: 'hidden',
    marginBottom: 12,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#E2E8F0',
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  cardImage: {
    ...StyleSheet.absoluteFill,
    backgroundColor: '#E2E8F0',
  },
  cardOverlay: {
    ...StyleSheet.absoluteFill,
    backgroundColor: 'rgba(15, 23, 42, 0.55)',
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
  },
  cardTitle: {
    fontSize: 17,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  cardCount: {
    fontSize: 12,
    color: '#E2E8F0',
    marginTop: 2,
  },
  cardAction: {
    fontSize: 12,
    fontWeight: '600',
    color: '#93C5FD',
  },
});
