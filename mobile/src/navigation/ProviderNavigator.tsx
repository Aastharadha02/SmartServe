import React from 'react';
import { StyleSheet } from 'react-native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Briefcase, CalendarDays, User } from 'lucide-react-native';

import { ProviderDashboardScreen } from '../screens/provider/ProviderDashboardScreen';
import { ProviderJobDetailScreen } from '../screens/provider/ProviderJobDetailScreen';
import { ProviderAvailabilityScreen } from '../screens/provider/ProviderAvailabilityScreen';
import { ProfileScreen } from '../screens/ProfileScreen';
import { useLanguage } from '../i18n/LanguageContext';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const ProviderTabNavigator = () => {
  const { t } = useLanguage();

  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarStyle: styles.tabBar,
        tabBarActiveTintColor: '#1E40AF',
        tabBarInactiveTintColor: '#94A3B8',
        tabBarLabelStyle: styles.tabBarLabel,
      }}
    >
      <Tab.Screen
        name="ProviderJobsTab"
        component={ProviderDashboardScreen}
        options={{
          tabBarLabel: t('nav_provider_jobs'),
          tabBarIcon: ({ color, size }) => <Briefcase size={22} color={color} />,
        }}
      />
      <Tab.Screen
        name="ProviderScheduleTab"
        component={ProviderAvailabilityScreen}
        options={{
          tabBarLabel: t('nav_provider_schedule'),
          tabBarIcon: ({ color, size }) => <CalendarDays size={22} color={color} />,
        }}
      />
      <Tab.Screen
        name="ProviderProfileTab"
        component={ProfileScreen}
        options={{
          tabBarLabel: t('nav_profile'),
          tabBarIcon: ({ color, size }) => <User size={22} color={color} />,
        }}
      />
    </Tab.Navigator>
  );
};

export const ProviderNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="ProviderTabs" component={ProviderTabNavigator} />
      <Stack.Screen
        name="ProviderJobDetail"
        component={ProviderJobDetailScreen}
        options={{ animation: 'slide_from_right' }}
      />
    </Stack.Navigator>
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
    elevation: 8,
  },
  tabBarLabel: {
    fontSize: 10,
    fontWeight: '600',
  },
});

