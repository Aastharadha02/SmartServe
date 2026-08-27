import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  Image,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  SafeAreaView,
} from 'react-native';
import { catalogApi, ServiceItem } from '../api/catalog';
import { getServiceImage } from '../utils/serviceImages';
import { formatRupee, formatCategoryDisplayName } from '../utils/formatters';

export const ServiceDetailScreen = ({ route, navigation }: any) => {
  const { serviceId } = route.params;
  const [service, setService] = useState<ServiceItem | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadService();
  }, [serviceId]);

  const loadService = async () => {
    try {
      const data = await catalogApi.getServiceById(serviceId);
      setService(data);
    } catch (err) {
      console.warn('Failed to load service detail', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading || !service) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#1E40AF" />
      </SafeAreaView>
    );
  }

  const imgUrl = getServiceImage(service.category, service.subcategory, service.name);
  const price = service.final_price || service.base_price;

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {/* Cover Image with Back Button */}
        <View style={styles.imageContainer}>
          <Image source={{ uri: imgUrl }} style={styles.coverImage} />
          <TouchableOpacity style={styles.floatingBackBtn} onPress={() => navigation.goBack()}>
            <Text style={styles.floatingBackText}>←</Text>
          </TouchableOpacity>
        </View>

        {/* Content Container */}
        <View style={styles.content}>
          <Text style={styles.categoryPath}>
            {formatCategoryDisplayName(service.category)} • {service.subcategory}
          </Text>
          <Text style={styles.title}>{service.name}</Text>

          {/* Key Metrics Row */}
          <View style={styles.metricsRow}>
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>Price</Text>
              <Text style={styles.metricValue}>{formatRupee(price)}</Text>
            </View>
            <View style={styles.metricDivider} />
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>Duration</Text>
              <Text style={styles.metricValue}>⏱ {service.duration_minutes} mins</Text>
            </View>
            <View style={styles.metricDivider} />
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>Warranty</Text>
              <Text style={styles.metricValue}>{service.warranty || '30-Day Guarantee'}</Text>
            </View>
          </View>

          {/* Description */}
          {service.description ? (
            <View style={styles.section}>
              <Text style={styles.sectionHeading}>About this Service</Text>
              <Text style={styles.descriptionText}>{service.description}</Text>
            </View>
          ) : null}

          {/* Included Features */}
          {service.includes && service.includes.length > 0 ? (
            <View style={styles.section}>
              <Text style={styles.sectionHeading}>What is Included</Text>
              {service.includes.map((inc, i) => (
                <View key={i} style={styles.bulletRow}>
                  <Text style={styles.checkIcon}>✓</Text>
                  <Text style={styles.bulletText}>{inc}</Text>
                </View>
              ))}
            </View>
          ) : null}

          {/* Excluded Features */}
          {service.excludes && service.excludes.length > 0 ? (
            <View style={styles.section}>
              <Text style={styles.sectionHeading}>What is Excluded</Text>
              {service.excludes.map((exc, i) => (
                <View key={i} style={styles.bulletRow}>
                  <Text style={styles.crossIcon}>✗</Text>
                  <Text style={styles.bulletText}>{exc}</Text>
                </View>
              ))}
            </View>
          ) : null}

          {/* FAQs */}
          {service.faqs && service.faqs.length > 0 ? (
            <View style={styles.section}>
              <Text style={styles.sectionHeading}>Frequently Asked Questions</Text>
              {service.faqs.map((faq, i) => (
                <View key={i} style={styles.faqCard}>
                  <Text style={styles.faqQ}>Q: {faq.question}</Text>
                  <Text style={styles.faqA}>{faq.answer}</Text>
                </View>
              ))}
            </View>
          ) : null}
        </View>
      </ScrollView>

      {/* Sticky Bottom Booking Bar */}
      <View style={styles.bottomBar}>
        <View>
          <Text style={styles.barPriceLabel}>Total Amount</Text>
          <Text style={styles.barPrice}>{formatRupee(price)}</Text>
        </View>
        <TouchableOpacity
          style={styles.bookNowBtn}
          activeOpacity={0.85}
          onPress={() => navigation.navigate('BookingModal', { service })}
        >
          <Text style={styles.bookNowText}>Book Service</Text>
        </TouchableOpacity>
      </View>
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
  scrollContent: {
    paddingBottom: 100,
  },
  imageContainer: {
    position: 'relative',
    height: 240,
    backgroundColor: '#E2E8F0',
  },
  coverImage: {
    width: '100%',
    height: '100%',
  },
  floatingBackBtn: {
    position: 'absolute',
    top: 20,
    left: 20,
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  floatingBackText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#0F172A',
  },
  content: {
    padding: 20,
    backgroundColor: '#FAF9F5',
  },
  categoryPath: {
    fontSize: 12,
    fontWeight: '600',
    color: '#2563EB',
    textTransform: 'uppercase',
    marginBottom: 4,
  },
  title: {
    fontSize: 24,
    fontWeight: '800',
    color: '#0F172A',
    marginBottom: 16,
  },
  metricsRow: {
    flexDirection: 'row',
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 20,
    justifyContent: 'space-around',
  },
  metricItem: {
    alignItems: 'center',
  },
  metricLabel: {
    fontSize: 11,
    color: '#94A3B8',
    fontWeight: '500',
    marginBottom: 4,
  },
  metricValue: {
    fontSize: 14,
    fontWeight: '700',
    color: '#0F172A',
  },
  metricDivider: {
    width: 1,
    backgroundColor: '#E2E8F0',
  },
  section: {
    marginBottom: 20,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  sectionHeading: {
    fontSize: 16,
    fontWeight: '700',
    color: '#0F172A',
    marginBottom: 10,
  },
  descriptionText: {
    fontSize: 14,
    color: '#475569',
    lineHeight: 22,
  },
  bulletRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  checkIcon: {
    color: '#059669',
    fontWeight: 'bold',
    marginRight: 8,
    fontSize: 14,
  },
  crossIcon: {
    color: '#DC2626',
    fontWeight: 'bold',
    marginRight: 8,
    fontSize: 14,
  },
  bulletText: {
    flex: 1,
    fontSize: 13,
    color: '#334155',
    lineHeight: 18,
  },
  faqCard: {
    backgroundColor: '#F8FAFC',
    borderRadius: 10,
    padding: 12,
    marginBottom: 8,
  },
  faqQ: {
    fontSize: 13,
    fontWeight: '700',
    color: '#0F172A',
    marginBottom: 4,
  },
  faqA: {
    fontSize: 13,
    color: '#64748B',
    lineHeight: 18,
  },
  bottomBar: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderTopWidth: 1,
    borderTopColor: '#E2E8F0',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -3 },
    shadowOpacity: 0.05,
    shadowRadius: 6,
    elevation: 8,
  },
  barPriceLabel: {
    fontSize: 11,
    color: '#64748B',
    fontWeight: '500',
  },
  barPrice: {
    fontSize: 20,
    fontWeight: '800',
    color: '#059669',
  },
  bookNowBtn: {
    backgroundColor: '#1E40AF',
    paddingHorizontal: 28,
    paddingVertical: 12,
    borderRadius: 12,
  },
  bookNowText: {
    color: '#FFFFFF',
    fontSize: 15,
    fontWeight: '700',
  },
});
