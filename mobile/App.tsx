import React, { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { View, StyleSheet } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { AuthProvider } from './src/context/AuthContext';
import { AppNavigator } from './src/navigation/AppNavigator';
import { SplashScreen } from './src/components/common/SplashScreen';
import { ErrorBoundary } from './src/components/common/ErrorBoundary';

export default function App() {
  const [splashFinished, setSplashFinished] = useState(false);

  return (
    <SafeAreaProvider>
      <ErrorBoundary>
        <AuthProvider>
          <View style={styles.container}>
            <StatusBar style="dark" />
            <AppNavigator />
            {!splashFinished && (
              <SplashScreen onAnimationComplete={() => setSplashFinished(true)} />
            )}
          </View>
        </AuthProvider>
      </ErrorBoundary>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FAF9F5',
  },
});
