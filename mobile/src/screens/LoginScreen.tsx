import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import { useAuth, UserRole } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { SupportedLanguage } from '../i18n/translations';

export const LoginScreen = ({ navigation }: any) => {
  const { login } = useAuth();
  const { t, language, setLanguage } = useLanguage();
  const [role, setRole] = useState<UserRole>('customer');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [is2FaRequired, setIs2FaRequired] = useState(false);
  const [twoFactorCode, setTwoFactorCode] = useState('');
  const [isRecoveryMode, setIsRecoveryMode] = useState(false);

  const handleLogin = async () => {
    if (!email.trim() || !password.trim()) {
      setErrorMessage('Please enter both your email and password.');
      return;
    }
    if (is2FaRequired && !twoFactorCode.trim()) {
      setErrorMessage(isRecoveryMode ? 'Please enter your recovery code.' : 'Please enter your 6-digit authenticator code.');
      return;
    }
    setErrorMessage(null);
    setIsLoading(true);
    try {
      await login(
        email.trim(),
        password.trim(),
        role,
        is2FaRequired && !isRecoveryMode ? twoFactorCode.trim() : undefined,
        is2FaRequired && isRecoveryMode ? twoFactorCode.trim() : undefined
      );
    } catch (err: any) {
      const is2FaHeader = err.response?.headers?.['x-2fa-required'] === 'true';
      const detail = err.response?.data?.detail || '';
      const is2FaDetail = typeof detail === 'string' && (detail.includes('Two-factor') || detail.includes('2FA'));

      if (err.response?.status === 401 && (is2FaHeader || is2FaDetail) && !is2FaRequired) {
        setIs2FaRequired(true);
        setErrorMessage(null);
        return;
      }
      if (err.response?.data?.detail) {
        setErrorMessage(err.response.data.detail);
      } else if (err.message?.includes('Network Error') || !err.response) {
        setErrorMessage('Unable to connect to SmartServe backend. Please verify your network.');
      } else {
        setErrorMessage('Invalid credentials. Please verify and try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleFillDemo = (targetRole: UserRole) => {
    setRole(targetRole);
    if (targetRole === 'customer') {
      setEmail('demo.customer@smartserve.com');
      setPassword('DemoCustomer123!');
    } else {
      setEmail('demo.provider@smartserve.com');
      setPassword('DemoProvider123!');
    }
    setErrorMessage(null);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <KeyboardAvoidingView
        style={styles.container}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView contentContainerStyle={styles.scrollContent} keyboardShouldPersistTaps="handled">
          {/* Language Switcher Bar */}
          <View style={styles.langBar}>
            {(['en', 'hi', 'gu'] as SupportedLanguage[]).map((l) => (
              <TouchableOpacity
                key={l}
                onPress={() => setLanguage(l)}
                style={[styles.langChip, language === l && styles.langChipActive]}
              >
                <Text style={[styles.langChipText, language === l && styles.langChipTextActive]}>
                  {l === 'en' ? 'English' : l === 'hi' ? 'हिंदी' : 'ગુજરાતી'}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          {/* Header Branding */}
          <View style={styles.brandHeader}>
            <View style={styles.logoBadge}>
              <Text style={styles.logoLetter}>S</Text>
            </View>
            <View style={styles.wordmarkRow}>
              <Text style={styles.brandSmart}>Smart</Text>
              <Text style={styles.brandServe}>Serve</Text>
            </View>
            <Text style={styles.portalSubtitle}>
              {role === 'customer' ? 'Customer Portal' : 'Service Expert Partner Portal'}
            </Text>
          </View>

          {/* Role Selector Tabs */}
          <View style={styles.roleTabsContainer}>
            <TouchableOpacity
              style={[styles.roleTab, role === 'customer' && styles.roleTabActive]}
              onPress={() => {
                setRole('customer');
                setErrorMessage(null);
              }}
            >
              <Text style={[styles.roleTabText, role === 'customer' && styles.roleTabTextActive]}>
                {t('auth_role_customer')}
              </Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.roleTab, role === 'provider' && styles.roleTabActive]}
              onPress={() => {
                setRole('provider');
                setErrorMessage(null);
              }}
            >
              <Text style={[styles.roleTabText, role === 'provider' && styles.roleTabTextActive]}>
                {t('auth_role_provider')}
              </Text>
            </TouchableOpacity>
          </View>

          {/* Form Card */}
          <View style={styles.card}>
            <Text style={styles.cardTitle}>
              {is2FaRequired ? 'Two-Factor Verification' : t('auth_login_title')}
            </Text>
            <Text style={styles.cardDescription}>
              {is2FaRequired
                ? (isRecoveryMode
                    ? 'Enter your single-use backup recovery code.'
                    : 'Enter the 6-digit verification code from your authenticator app.')
                : `Enter your credentials to access as a ${role === 'customer' ? 'Customer' : 'Service Expert'}.`}
            </Text>

            {errorMessage ? (
              <View style={styles.errorBox}>
                <Text style={styles.errorText}>{errorMessage}</Text>
              </View>
            ) : null}

            {!is2FaRequired ? (
              <>
                <View style={styles.inputGroup}>
                  <Text style={styles.inputLabel}>{t('auth_email')}</Text>
                  <TextInput
                    style={styles.textInput}
                    value={email}
                    onChangeText={setEmail}
                    placeholder="name@example.com"
                    placeholderTextColor="#94A3B8"
                    keyboardType="email-address"
                    autoCapitalize="none"
                    autoCorrect={false}
                  />
                </View>

                <View style={styles.inputGroup}>
                  <View style={styles.labelRow}>
                    <Text style={styles.inputLabel}>{t('auth_password')}</Text>
                    <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
                      <Text style={styles.showHideText}>{showPassword ? 'Hide' : 'Show'}</Text>
                    </TouchableOpacity>
                  </View>
                  <TextInput
                    style={styles.textInput}
                    value={password}
                    onChangeText={setPassword}
                    placeholder="••••••••"
                    placeholderTextColor="#94A3B8"
                    secureTextEntry={!showPassword}
                    autoCapitalize="none"
                  />
                </View>
              </>
            ) : (
              <View style={styles.inputGroup}>
                <Text style={styles.inputLabel}>
                  {isRecoveryMode ? 'Backup Recovery Code' : 'Authenticator Code'}
                </Text>
                <TextInput
                  style={[styles.textInput, styles.codeField]}
                  value={twoFactorCode}
                  onChangeText={setTwoFactorCode}
                  placeholder={isRecoveryMode ? 'ABCD-EFGH-1234' : '123456'}
                  placeholderTextColor="#94A3B8"
                  keyboardType={isRecoveryMode ? 'default' : 'number-pad'}
                  maxLength={isRecoveryMode ? 24 : 6}
                  autoCapitalize="characters"
                />
                <TouchableOpacity
                  style={{ marginTop: 8 }}
                  onPress={() => setIsRecoveryMode(!isRecoveryMode)}
                >
                  <Text style={styles.recoveryToggleText}>
                    {isRecoveryMode ? 'Use Authenticator App OTP' : 'Use Backup Recovery Code'}
                  </Text>
                </TouchableOpacity>
              </View>
            )}

            <TouchableOpacity
              style={[styles.primaryButton, isLoading && styles.buttonDisabled]}
              onPress={handleLogin}
              disabled={isLoading}
              activeOpacity={0.8}
            >
              {isLoading ? (
                <ActivityIndicator color="#FFFFFF" />
              ) : (
                <Text style={styles.primaryButtonText}>
                  {is2FaRequired ? 'Verify & Continue' : t('auth_login_btn')}
                </Text>
              )}
            </TouchableOpacity>

            {/* Quick Demo Logins */}
            <View style={styles.demoBox}>
              <Text style={styles.demoLabel}>Demo Fast Fill:</Text>
              <View style={styles.demoRow}>
                <TouchableOpacity
                  style={styles.demoBtn}
                  onPress={() => handleFillDemo('customer')}
                >
                  <Text style={styles.demoBtnText}>Customer Demo</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={styles.demoBtn}
                  onPress={() => handleFillDemo('provider')}
                >
                  <Text style={styles.demoBtnText}>Expert Demo</Text>
                </TouchableOpacity>
              </View>
            </View>

            {role === 'customer' && !is2FaRequired && (
              <TouchableOpacity
                style={styles.secondaryLink}
                onPress={() => navigation.navigate('Signup')}
              >
                <Text style={styles.secondaryLinkText}>{t('auth_no_account')}</Text>
              </TouchableOpacity>
            )}
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#FAF9F5',
  },
  container: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100%',
  },
  langBar: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 16,
    alignSelf: 'center',
  },
  langChip: {
    paddingHorizontal: 12,
    paddingVertical: 5,
    borderRadius: 16,
    backgroundColor: '#F1F5F9',
    borderWidth: 1,
    borderColor: '#CBD5E1',
  },
  langChipActive: {
    backgroundColor: '#1E40AF',
    borderColor: '#1E40AF',
  },
  langChipText: {
    fontSize: 12,
    color: '#475569',
    fontWeight: '600',
  },
  langChipTextActive: {
    color: '#FFFFFF',
  },
  brandHeader: {
    alignItems: 'center',
    marginBottom: 20,
  },
  logoBadge: {
    width: 60,
    height: 60,
    borderRadius: 18,
    backgroundColor: '#1E40AF',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10,
    shadowColor: '#1E40AF',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 4,
  },
  logoLetter: {
    fontSize: 32,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  wordmarkRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  brandSmart: {
    fontSize: 26,
    fontWeight: '800',
    color: '#0F172A',
  },
  brandServe: {
    fontSize: 26,
    fontWeight: '800',
    color: '#1E40AF',
  },
  portalSubtitle: {
    fontSize: 13,
    color: '#64748B',
    fontWeight: '500',
    marginTop: 2,
  },
  roleTabsContainer: {
    flexDirection: 'row',
    backgroundColor: '#E2E8F0',
    borderRadius: 10,
    padding: 4,
    width: '100%',
    maxWidth: 380,
    marginBottom: 16,
  },
  roleTab: {
    flex: 1,
    paddingVertical: 8,
    alignItems: 'center',
    borderRadius: 8,
  },
  roleTabActive: {
    backgroundColor: '#FFFFFF',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  roleTabText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#64748B',
  },
  roleTabTextActive: {
    color: '#1E40AF',
  },
  card: {
    width: '100%',
    maxWidth: 380,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 22,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#0F172A',
    marginBottom: 4,
  },
  cardDescription: {
    fontSize: 13,
    color: '#64748B',
    marginBottom: 16,
    lineHeight: 18,
  },
  errorBox: {
    backgroundColor: '#FEE2E2',
    borderWidth: 1,
    borderColor: '#F87171',
    borderRadius: 8,
    padding: 10,
    marginBottom: 16,
  },
  errorText: {
    color: '#991B1B',
    fontSize: 13,
    fontWeight: '500',
  },
  inputGroup: {
    marginBottom: 14,
  },
  labelRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  inputLabel: {
    fontSize: 13,
    fontWeight: '600',
    color: '#334155',
    marginBottom: 6,
  },
  showHideText: {
    fontSize: 12,
    color: '#1E40AF',
    fontWeight: '600',
  },
  textInput: {
    borderWidth: 1,
    borderColor: '#CBD5E1',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 14,
    color: '#0F172A',
    backgroundColor: '#F8FAFC',
  },
  codeField: {
    fontSize: 18,
    letterSpacing: 4,
    textAlign: 'center',
    fontWeight: '700',
  },
  recoveryToggleText: {
    fontSize: 12,
    color: '#1E40AF',
    fontWeight: '500',
    textAlign: 'right',
  },
  primaryButton: {
    backgroundColor: '#1E40AF',
    borderRadius: 8,
    paddingVertical: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 8,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  primaryButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '700',
  },
  demoBox: {
    marginTop: 18,
    paddingTop: 14,
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
  },
  demoLabel: {
    fontSize: 11,
    fontWeight: '700',
    color: '#94A3B8',
    textTransform: 'uppercase',
    marginBottom: 6,
  },
  demoRow: {
    flexDirection: 'row',
    gap: 8,
  },
  demoBtn: {
    flex: 1,
    paddingVertical: 6,
    paddingHorizontal: 10,
    backgroundColor: '#F1F5F9',
    borderRadius: 6,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  demoBtnText: {
    fontSize: 11,
    fontWeight: '600',
    color: '#334155',
  },
  secondaryLink: {
    marginTop: 16,
    alignItems: 'center',
  },
  secondaryLinkText: {
    color: '#1E40AF',
    fontSize: 13,
    fontWeight: '600',
  },
});
