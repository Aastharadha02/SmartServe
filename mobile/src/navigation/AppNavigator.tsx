import React from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Home, LayoutGrid, CalendarDays, Tag, User } from 'lucide-react-native';

import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';

// Auth screens
import { LoginScreen } from '../screens/LoginScreen';
import { SignupScreen } from '../screens/SignupScreen';

// Customer screens
import { HomeScreen } from '../screens/HomeScreen';
import { CatalogScreen } from '../screens/CatalogScreen';
import { SubcategoryListScreen } from '../screens/SubcategoryListScreen';
import { ServiceListScreen } from '../screens/ServiceListScreen';
import { ServiceDetailScreen } from '../screens/ServiceDetailScreen';
import { BookingModalScreen } from '../screens/BookingModalScreen';
import { BookingsListScreen } from '../screens/BookingsListScreen';
import { LiveTrackingScreen } from '../screens/LiveTrackingScreen';
import { OffersScreen } from '../screens/OffersScreen';
import { SupportScreen } from '../screens/SupportScreen';
import { SupportDetailScreen } from '../screens/SupportDetailScreen';
import { ProfileScreen } from '../screens/ProfileScreen';
import { WarrantyClaimModalScreen } from '../screens/WarrantyClaimModalScreen';

// Provider stack
import { ProviderNavigator } from './ProviderNavigator';

const RootStack = createNativeStackNavigator();
const AuthStack = createNativeStackNavigator();
const CatalogStack = createNativeStackNavigator();
const CustomerTab = createBottomTabNavigator();

const AuthNavigator = () => (
  <AuthStack.Navigator screenOptions={{ headerShown: false }}>
    <AuthStack.Screen name="Login" component={LoginScreen} />
    <AuthStack.Screen name="Signup" component={SignupScreen} />
  </AuthStack.Navigator>
);

const CatalogNavigator = () => (
  <CatalogStack.Navigator screenOptions={{ headerShown: false }}>
    <CatalogStack.Screen name="CatalogRoot" component={CatalogScreen} />
    <CatalogStack.Screen name="SubcategoryList" component={SubcategoryListScreen} />
    <CatalogStack.Screen name="ServiceList" component={ServiceListScreen} />
  </CatalogStack.Navigator>
);

const CustomerTabNavigator = () => {
  const { t } = useLanguage();

  return (
    <CustomerTab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarStyle: styles.tabBar,
        tabBarActiveTintColor: '#1E40AF',
        tabBarInactiveTintColor: '#94A3B8',
        tabBarLabelStyle: styles.tabBarLabel,
      }}
    >
      <CustomerTab.Screen
        name="HomeTab"
        component={HomeScreen}
        options={{
          tabBarLabel: t('nav_home'),
          tabBarIcon: ({ color, size }) => <Home size={22} color={color} />,
        }}
      />
      <CustomerTab.Screen
        name="CatalogTab"
        component={CatalogNavigator}
        options={{
          tabBarLabel: t('nav_services'),
          tabBarIcon: ({ color, size }) => <LayoutGrid size={22} color={color} />,
        }}
      />
      <CustomerTab.Screen
        name="BookingsTab"
        component={BookingsListScreen}
        options={{
          tabBarLabel: t('nav_bookings'),
          tabBarIcon: ({ color, size }) => <CalendarDays size={22} color={color} />,
        }}
      />
      <CustomerTab.Screen
        name="OffersTab"
        component={OffersScreen}
        options={{
          tabBarLabel: t('nav_offers'),
          tabBarIcon: ({ color, size }) => <Tag size={22} color={color} />,
        }}
      />
      <CustomerTab.Screen
        name="ProfileTab"
        component={ProfileScreen}
        options={{
          tabBarLabel: t('nav_profile'),
          tabBarIcon: ({ color, size }) => <User size={22} color={color} />,
        }}
      />
    </CustomerTab.Navigator>
  );
};

export const AppNavigator = () => {
  const { user, activeRole, isLoading } = useAuth();

  if (isLoading) {
    return (
      <View style={styles.splashContainer}>
        <View style={styles.splashLogo}>
          <Text style={styles.splashLogoText}>S</Text>
        </View>
        <Text style={styles.splashBrand}>SmartServe</Text>
        <ActivityIndicator color="#1E40AF" style={{ marginTop: 24 }} />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <RootStack.Navigator screenOptions={{ headerShown: false }}>
        {!user ? (
          <RootStack.Screen name="Auth" component={AuthNavigator} />
        ) : activeRole === 'provider' ? (
          <RootStack.Screen name="ProviderRoot" component={ProviderNavigator} />
        ) : (
          <>
            <RootStack.Screen name="Main" component={CustomerTabNavigator} />
            <RootStack.Screen
              name="ServiceDetail"
              component={ServiceDetailScreen}
              options={{ animation: 'slide_from_right' }}
            />
            <RootStack.Screen
              name="BookingModal"
              component={BookingModalScreen}
              options={{ presentation: 'modal', animation: 'slide_from_bottom' }}
            />
            <RootStack.Screen
              name="LiveTracking"
              component={LiveTrackingScreen}
              options={{ animation: 'slide_from_right' }}
            />
            <RootStack.Screen
              name="WarrantyClaim"
              component={WarrantyClaimModalScreen}
              options={{ presentation: 'modal', animation: 'slide_from_bottom' }}
            />
            <RootStack.Screen
              name="SupportDetail"
              component={SupportDetailScreen}
              options={{ animation: 'slide_from_right' }}
            />
          </>
        )}
      </RootStack.Navigator>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  tabBar: {
    backgroundColor: '#FFFFFF',
    borderTopWidth: 1,
    borderTopColor: '#E2E8F0',
    height: 64,
    paddingBottom: 8,
    paddingTop: 6,
    shadowColor: '#0F172A',
    shadowOffset: { width: 0, height: -2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 10,
  },
  tabBarLabel: {
    fontSize: 10,
    fontWeight: '600',
  },
  splashContainer: {
    flex: 1,
    backgroundColor: '#FAF9F5',
    alignItems: 'center',
    justifyContent: 'center',
  },
  splashLogo: {
    width: 72,
    height: 72,
    borderRadius: 20,
    backgroundColor: '#1E40AF',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
    shadowColor: '#1E40AF',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.25,
    shadowRadius: 16,
    elevation: 8,
  },
  splashLogoText: { fontSize: 36, fontWeight: '800', color: '#FFFFFF' },
  splashBrand: { fontSize: 28, fontWeight: '800', color: '#0F172A', letterSpacing: -0.5 },
});
