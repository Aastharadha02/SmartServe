import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Animated,
  Easing,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Tag, Sparkles, Gift, Clock, Copy, CheckCircle2 } from 'lucide-react-native';
import { couponsApi, CouponItem, SpinRewardResult } from '../api/coupons';
import { useLanguage } from '../i18n/LanguageContext';

export const OffersScreen = () => {
  const { t } = useLanguage();
  const [coupons, setCoupons] = useState<CouponItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSpinning, setIsSpinning] = useState(false);
  const [spinResult, setSpinResult] = useState<SpinRewardResult | null>(null);
  const [copiedCode, setCopiedCode] = useState<string | null>(null);

  // Animated rotation for wheel
  const spinValue = new Animated.Value(0);

  useEffect(() => {
    loadCoupons();
  }, []);

  const loadCoupons = async () => {
    setIsLoading(true);
    try {
      const data = await couponsApi.getActiveCoupons();
      setCoupons(data);
    } catch {
      // offline fallback
    } finally {
      setIsLoading(false);
    }
  };

  const handleSpinWheel = async () => {
    if (isSpinning) return;
    setIsSpinning(true);
    setSpinResult(null);

    // Run wheel animation
    spinValue.setValue(0);
    Animated.timing(spinValue, {
      toValue: 1,
      duration: 2500,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: true,
    }).start();

    try {
      // Request spin reward from backend
      const result = await couponsApi.spinReward('SERVE75');
      setTimeout(() => {
        setIsSpinning(false);
        setSpinResult(result);
        loadCoupons(); // refresh coupon list
      }, 2500);
    } catch (err: any) {
      setTimeout(() => {
        setIsSpinning(false);
        Alert.alert('Notice', err.response?.data?.detail || 'Spin wheel currently busy. Please try again.');
      }, 1000);
    }
  };

  const spinRotation = spinValue.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '1440deg'],
  });

  const handleCopy = (code: string) => {
    setCopiedCode(code);
    setTimeout(() => {
      setCopiedCode(null);
    }, 2500);
  };

  return (
    <SafeAreaView style={styles.safeArea} edges={['top']}>
      <ScrollView contentContainerStyle={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>{t('offers_title')}</Text>
          <Text style={styles.headerSubtitle}>Exclusive discounts and rewards for you</Text>
        </View>

        {/* Spin & Win Hero Banner */}
        <View style={styles.spinCard}>
          <View style={styles.spinHeader}>
            <Sparkles size={20} color="#F59E0B" />
            <Text style={styles.spinTitle}>{t('spin_wheel_title')}</Text>
          </View>
          <Text style={styles.spinSubtitle}>
            Spin the lucky wheel once every booking cycle to win up to ₹75 or 15% off!
          </Text>

          {/* Wheel Graphic */}
          <View style={styles.wheelContainer}>
            <Animated.View style={[styles.wheel, { transform: [{ rotate: spinRotation }] }]}>
              <View style={[styles.wheelSection, { backgroundColor: '#1E40AF' }]}>
                <Text style={styles.wheelText}>₹75 OFF</Text>
              </View>
              <View style={[styles.wheelSection, { backgroundColor: '#0284C7' }]}>
                <Text style={styles.wheelText}>10% OFF</Text>
              </View>
              <View style={[styles.wheelSection, { backgroundColor: '#0D9488' }]}>
                <Text style={styles.wheelText}>₹50 OFF</Text>
              </View>
              <View style={[styles.wheelSection, { backgroundColor: '#F59E0B' }]}>
                <Text style={styles.wheelText}>15% OFF</Text>
              </View>
            </Animated.View>
            <View style={styles.wheelCenterPin}>
              <Gift size={18} color="#FFFFFF" />
            </View>
          </View>

          {spinResult && (
            <View style={styles.resultBanner}>
              <CheckCircle2 size={18} color="#059669" />
              <View style={{ flex: 1, marginLeft: 8 }}>
                <Text style={styles.resultTitle}>{spinResult.message}</Text>
                <Text style={styles.resultCode}>Code: {spinResult.code} (Saved to your account)</Text>
              </View>
            </View>
          )}

          <TouchableOpacity
            style={[styles.spinButton, isSpinning && styles.buttonDisabled]}
            onPress={handleSpinWheel}
            disabled={isSpinning}
          >
            {isSpinning ? (
              <ActivityIndicator color="#FFFFFF" size="small" />
            ) : (
              <Text style={styles.spinButtonText}>{t('spin_wheel_btn')}</Text>
            )}
          </TouchableOpacity>
        </View>

        {/* Active Coupons Section */}
        <View style={styles.sectionHeader}>
          <Tag size={18} color="#1E40AF" />
          <Text style={styles.sectionTitle}>{t('active_coupons')}</Text>
        </View>

        {isLoading ? (
          <ActivityIndicator color="#1E40AF" style={{ marginVertical: 32 }} />
        ) : coupons.length === 0 ? (
          <View style={styles.emptyState}>
            <Text style={styles.emptyText}>No public coupons at this moment. Spin the wheel above to get one!</Text>
          </View>
        ) : (
          coupons.map((c) => {
            const isDiscountPercent = c.discount_type === 'PERCENTAGE';
            const isCopied = copiedCode === c.code;

            return (
              <View key={c.id || c.code} style={styles.couponCard}>
                <View style={styles.couponLeft}>
                  <View style={styles.discountBadge}>
                    <Text style={styles.discountBadgeText}>
                      {isDiscountPercent ? `${c.discount_value}% OFF` : `₹${c.discount_value} OFF`}
                    </Text>
                  </View>
                  <Text style={styles.couponCode}>{c.code}</Text>
                  <Text style={styles.couponDescription}>
                    {c.description || (c.min_order_amount > 0 ? `On orders above ₹${c.min_order_amount}` : 'Applicable on all services')}
                  </Text>
                  <View style={styles.validityRow}>
                    <Clock size={12} color="#94A3B8" />
                    <Text style={styles.validityText}>
                      Valid until {new Date(c.valid_until).toLocaleDateString()}
                    </Text>
                  </View>
                </View>

                <TouchableOpacity
                  style={[styles.copyButton, isCopied && styles.copyButtonActive]}
                  onPress={() => handleCopy(c.code)}
                >
                  {isCopied ? (
                    <Text style={styles.copyButtonTextActive}>{t('copied')}</Text>
                  ) : (
                    <>
                      <Copy size={13} color="#1E40AF" />
                      <Text style={styles.copyButtonText}>{t('copy_coupon')}</Text>
                    </>
                  )}
                </TouchableOpacity>
              </View>
            );
          })
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#FAF9F5',
  },
  container: {
    padding: 16,
    paddingBottom: 40,
  },
  header: {
    marginBottom: 16,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '800',
    color: '#0F172A',
  },
  headerSubtitle: {
    fontSize: 13,
    color: '#64748B',
    marginTop: 2,
  },
  spinCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 18,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 24,
    alignItems: 'center',
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 2,
  },
  spinHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 4,
  },
  spinTitle: {
    fontSize: 18,
    fontWeight: '800',
    color: '#0F172A',
  },
  spinSubtitle: {
    fontSize: 12,
    color: '#64748B',
    textAlign: 'center',
    marginBottom: 16,
    lineHeight: 16,
  },
  wheelContainer: {
    width: 140,
    height: 140,
    alignItems: 'center',
    justifyContent: 'center',
    marginVertical: 10,
  },
  wheel: {
    width: 130,
    height: 130,
    borderRadius: 65,
    borderWidth: 4,
    borderColor: '#F1F5F9',
    overflow: 'hidden',
    position: 'relative',
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  wheelSection: {
    width: 65,
    height: 65,
    alignItems: 'center',
    justifyContent: 'center',
  },
  wheelText: {
    color: '#FFFFFF',
    fontSize: 11,
    fontWeight: '800',
  },
  wheelCenterPin: {
    position: 'absolute',
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: '#0F172A',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 3,
    borderColor: '#FFFFFF',
    elevation: 4,
  },
  resultBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ECFDF5',
    borderWidth: 1,
    borderColor: '#A7F3D0',
    padding: 10,
    borderRadius: 8,
    marginTop: 14,
    width: '100%',
  },
  resultTitle: {
    fontSize: 12,
    fontWeight: '700',
    color: '#065F46',
  },
  resultCode: {
    fontSize: 11,
    color: '#047857',
    fontWeight: '600',
  },
  spinButton: {
    backgroundColor: '#1E40AF',
    paddingVertical: 12,
    paddingHorizontal: 28,
    borderRadius: 10,
    marginTop: 14,
    width: '100%',
    alignItems: 'center',
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  spinButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '700',
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#0F172A',
  },
  emptyState: {
    padding: 24,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  emptyText: {
    fontSize: 13,
    color: '#64748B',
    textAlign: 'center',
  },
  couponCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 14,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 1,
  },
  couponLeft: {
    flex: 1,
    marginRight: 10,
  },
  discountBadge: {
    backgroundColor: '#EFF6FF',
    alignSelf: 'flex-start',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
    marginBottom: 6,
  },
  discountBadgeText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#1E40AF',
  },
  couponCode: {
    fontSize: 16,
    fontWeight: '800',
    color: '#0F172A',
    letterSpacing: 0.5,
  },
  couponDescription: {
    fontSize: 12,
    color: '#64748B',
    marginTop: 2,
  },
  validityRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    marginTop: 6,
  },
  validityText: {
    fontSize: 11,
    color: '#94A3B8',
  },
  copyButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 10,
    paddingVertical: 7,
    borderRadius: 8,
    backgroundColor: '#EFF6FF',
    borderWidth: 1,
    borderColor: '#BFDBFE',
  },
  copyButtonActive: {
    backgroundColor: '#ECFDF5',
    borderColor: '#A7F3D0',
  },
  copyButtonText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#1E40AF',
  },
  copyButtonTextActive: {
    fontSize: 12,
    fontWeight: '700',
    color: '#059669',
  },
});

