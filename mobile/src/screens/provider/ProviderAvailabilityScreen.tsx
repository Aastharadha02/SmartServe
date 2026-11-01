import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Calendar, Clock, CheckCircle2 } from 'lucide-react-native';
import { providerApi, AvailabilitySlot } from '../../api/provider';
import { useLanguage } from '../../i18n/LanguageContext';

const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

export const ProviderAvailabilityScreen = () => {
  const { t } = useLanguage();
  const [slots, setSlots] = useState<AvailabilitySlot[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    loadAvailability();
  }, []);

  const loadAvailability = async () => {
    setIsLoading(true);
    try {
      const data = await providerApi.getAvailability();
      if (data && data.length > 0) {
        setSlots(data);
      } else {
        // Default initial week
        const defaults: AvailabilitySlot[] = DAYS.map((_, idx) => ({
          day_of_week: idx,
          start_time: '09:00',
          end_time: '18:00',
          is_available: idx >= 1 && idx <= 5, // Mon-Fri default
        }));
        setSlots(defaults);
      }
    } catch {
      // offline fallback
    } finally {
      setIsLoading(false);
    }
  };

  const toggleDay = async (dayIndex: number) => {
    const updated = slots.map((s) => {
      if (s.day_of_week === dayIndex) {
        return { ...s, is_available: !s.is_available };
      }
      return s;
    });
    setSlots(updated);

    const changedSlot = updated.find((s) => s.day_of_week === dayIndex);
    if (changedSlot) {
      try {
        await providerApi.updateAvailabilitySlot(changedSlot);
      } catch (err: any) {
        console.warn('Failed to update slot remotely', err);
      }
    }
  };

  return (
    <SafeAreaView style={styles.safeArea} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.title}>{t('provider_availability')}</Text>
        <Text style={styles.subtitle}>Set your working hours for incoming customer requests</Text>
      </View>

      <ScrollView contentContainerStyle={styles.container}>
        <View style={styles.infoBanner}>
          <Clock size={18} color="#1E40AF" />
          <Text style={styles.infoText}>
            Operating hours: 09:00 AM to 06:00 PM. Customers can only book slots during your active days.
          </Text>
        </View>

        {isLoading ? (
          <ActivityIndicator color="#1E40AF" style={{ marginTop: 40 }} />
        ) : (
          <View style={styles.daysList}>
            {DAYS.map((dayName, idx) => {
              const slot = slots.find((s) => s.day_of_week === idx) || {
                day_of_week: idx,
                start_time: '09:00',
                end_time: '18:00',
                is_available: false,
              };

              return (
                <View key={dayName} style={styles.dayCard}>
                  <View style={styles.dayLeft}>
                    <Text style={styles.dayName}>{dayName}</Text>
                    <Text style={[styles.dayTime, !slot.is_available && { color: '#94A3B8' }]}>
                      {slot.is_available ? `${slot.start_time} - ${slot.end_time}` : 'Unavailable / Day Off'}
                    </Text>
                  </View>
                  <Switch
                    value={slot.is_available}
                    onValueChange={() => toggleDay(idx)}
                    trackColor={{ false: '#CBD5E1', true: '#BFDBFE' }}
                    thumbColor={slot.is_available ? '#1E40AF' : '#F8FAFC'}
                  />
                </View>
              );
            })}
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#FAF9F5' },
  header: {
    paddingHorizontal: 20,
    paddingTop: 16,
    paddingBottom: 12,
  },
  title: { fontSize: 22, fontWeight: '800', color: '#0F172A' },
  subtitle: { fontSize: 12, color: '#64748B', marginTop: 2 },
  container: { padding: 16, paddingBottom: 40 },
  infoBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#EFF6FF',
    borderRadius: 10,
    padding: 12,
    borderWidth: 1,
    borderColor: '#BFDBFE',
    marginBottom: 16,
  },
  infoText: { fontSize: 12, color: '#1E40AF', flex: 1, lineHeight: 16 },
  daysList: { gap: 10 },
  dayCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 14,
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  dayLeft: { flex: 1 },
  dayName: { fontSize: 15, fontWeight: '700', color: '#0F172A' },
  dayTime: { fontSize: 12, color: '#059669', fontWeight: '500', marginTop: 2 },
});

