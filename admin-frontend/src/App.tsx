import React, { useState } from 'react';
import { AppRoutes } from './routes/AppRoutes';
import { SplashScreen } from './components/common/SplashScreen';
import { ErrorBoundary } from './components/common/ErrorBoundary';

export const App: React.FC = () => {
  const [splashDone, setSplashDone] = useState(() => {
    return sessionStorage.getItem('smartserve_splash_done') === 'true';
  });

  const handleFinish = () => {
    sessionStorage.setItem('smartserve_splash_done', 'true');
    setSplashDone(true);
  };

  return (
    <ErrorBoundary>
      <AppRoutes />
      {!splashDone && (
        <SplashScreen
          durationMs={8000}
          onFinish={handleFinish}
        />
      )}
    </ErrorBoundary>
  );
};

export default App;

