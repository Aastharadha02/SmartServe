import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Alert,
} from 'react-native';
import { Globe, Repeat, LogOut, CheckCircle2 } from 'lucide-react-native';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { SupportedLanguage } from '../i18n/translations';
import { API_BASE_URL } from '../config/api';

export const ProfileScreen = () => {
  const { user, activeRole, switchRole, logout } = useAuth();
  const { t, language, setLanguage } = useLanguage();

  const handleLogout = () => {
    Alert.alert('Sign Out', 'Are you sure you want to sign out of SmartServe?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Sign Out', style: 'destructive', onPress: () => logout() },
    ]);
  };

  const handleToggleRole = () => {
    const nextRole = activeRole === 'customer' ? 'provider' : 'customer';
    switchRole(nextRole);
  };

  const displayName = user?.full_name || user?.email?.split('@')[0] || 'SmartServe User';
  const avatarLetter = displayName.charAt(0).toUpperCase();

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Profile Card */}
        <View style={styles.profileCard}>
          <View style={styles.avatarCircle}>
            <Text style={styles.avatarText}>{avatarLetter}</Text>
          </View>
          <Text style={styles.userName}>{displayName}</Text>
          <Text style={styles.userEmail}>{user?.email || ''}</Text>
          {user?.phone ? (
            <Text style={styles.userPhone}>{user.phone}</Text>
          ) : null}
          <View style={[styles.rolePill, activeRole === 'provider' && { backgroundColor: '#FEF3C7' }]}>
            <Text style={[styles.roleText, activeRole === 'provider' && { color: '#B45309' }]}>
              {activeRole === 'customer' ? 'Customer Account' : 'Service Expert Partner'}
            </Text>
          </View>
        </View>

        {/* Role Mode Switcher */}
        <TouchableOpacity style={styles.roleSwitchCard} onPress={handleToggleRole} activeOpacity={0.85}>
          <View style={styles.roleSwitchLeft}>
            <Repeat size={20} color="#1E40AF" />
            <View style={{ marginLeft: 10 }}>
              <Text style={styles.roleSwitchTitle}>
                {activeRole === 'customer' ? t('switch_to_provider') : t('switch_to_customer')}
              </Text>
              <Text style={styles.roleSwitchSub}>
                {activeRole === 'customer' ? 'Access assigned jobs & OTP verification' : 'Browse services & book home experts'}
              </Text>
            </View>
          </View>
        </TouchableOpacity>

        {/* Language Selection */}
        <View style={styles.sectionCard}>
          <View style={styles.sectionTitleRow}>
            <Globe size={18} color="#1E40AF" />
            <Text style={styles.sectionTitle}>{t('language')}</Text>
          </View>
          <View style={styles.langChipsRow}>
            {(['en', 'hi', 'gu'] as SupportedLanguage[]).map((l) => (
              <TouchableOpacity
                key={l}
                style={[styles.langChip, language === l && styles.langChipActive]}
                onPress={() => setLanguage(l)}
              >
                <Text style={[styles.langChipText, language === l && styles.langChipTextActive]}>
                  {l === 'en' ? 'English' : l === 'hi' ? 'हिंदी (Hindi)' : 'ગુજરાતી (Gujarati)'}
                </Text>
                {language === l && <CheckCircle2 size={14} color="#FFFFFF" style={{ marginLeft: 4 }} />}
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Account Info */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionTitle}>Account Details</Text>

          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Full Name</Text>
            <Text style={styles.infoValue}>{user?.full_name || 'N/A'}</Text>
          </View>
          <View style={styles.divider} />

          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Email</Text>
            <Text style={styles.infoValue} numberOfLines={1}>{user?.email || 'N/A'}</Text>
          </View>
          <View style={styles.divider} />

          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Role</Text>
            <Text style={styles.infoValue}>{activeRole === 'customer' ? 'Customer' : 'Provider'}</Text>
          </View>
        </View>

        {/* Application Info */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionTitle}>System Connection</Text>

          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Backend API</Text>
            <Text style={styles.infoValue} numberOfLines={1}>{API_BASE_URL}</Text>
          </View>
          <View style={styles.divider} />

          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Warranty Policy</Text>
            <Text style={[styles.infoValue, { color: '#059669' }]}>Standardized 7-Day Free Rework</Text>
          </View>
          <View style={styles.divider} />

          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Currency</Text>
            <Text style={styles.infoValue}>INR (₹)</Text>
          </View>
        </View>

        {/* Sign Out */}
        <TouchableOpacity style={styles.logoutBtn} activeOpacity={0.85} onPress={handleLogout}>
          <LogOut size={16} color="#DC2626" style={{ marginRight: 6 }} />
          <Text style={styles.logoutText}>{t('auth_logout_btn')}</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#FAF9F5' },
  scrollContent: { padding: 20, paddingBottom: 40 },
  profileCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    padding: 24,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 16,
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 8,
    elevation: 2,
  },
  avatarCircle: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: '#1E40AF',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  avatarText: { fontSize: 28, fontWeight: 'bold', color: '#FFFFFF' },
  userName: { fontSize: 20, fontWeight: '800', color: '#0F172A', marginBottom: 2 },
  userEmail: { fontSize: 13, color: '#64748B', marginBottom: 2 },
  userPhone: { fontSize: 13, color: '#64748B', marginBottom: 10 },
  rolePill: {
    backgroundColor: '#EFF6FF',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginTop: 8,
  },
  roleText: { fontSize: 12, fontWeight: '700', color: '#1E40AF', textTransform: 'uppercase' },
  roleSwitchCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 14,
    borderWidth: 1,
    borderColor: '#BFDBFE',
    marginBottom: 16,
  },
  roleSwitchLeft: { flexDirection: 'row', alignItems: 'center' },
  roleSwitchTitle: { fontSize: 14, fontWeight: '700', color: '#1E40AF' },
  roleSwitchSub: { fontSize: 11, color: '#64748B', marginTop: 1 },
  sectionCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    marginBottom: 16,
  },
  sectionTitleRow: { flexDirection: 'row', alignItems: 'center', gap: 6, marginBottom: 12 },
  sectionTitle: { fontSize: 15, fontWeight: '700', color: '#0F172A' },
  langChipsRow: { gap: 8 },
  langChip: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 10,
    backgroundColor: '#F8FAFC',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  langChipActive: { backgroundColor: '#1E40AF', borderColor: '#1E40AF' },
  langChipText: { fontSize: 13, color: '#334155', fontWeight: '600' },
  langChipTextActive: { color: '#FFFFFF' },
  infoRow: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 6 },
  infoLabel: { fontSize: 13, color: '#64748B' },
  infoValue: { fontSize: 13, fontWeight: '600', color: '#1E293B', maxWidth: '60%', textAlign: 'right' },
  divider: { height: 1, backgroundColor: '#F1F5F9', marginVertical: 4 },
  logoutBtn: {
    flexDirection: 'row',
    backgroundColor: '#FEF2F2',
    borderColor: '#FCA5A5',
    borderWidth: 1,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 8,
  },
  logoutText: { color: '#DC2626', fontSize: 14, fontWeight: '700' },
});
