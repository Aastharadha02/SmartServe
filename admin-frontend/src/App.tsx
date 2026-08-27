import React, { useState } from 'react';
import { AppRoutes } from './routes/AppRoutes';
import { SplashScreen } from './components/common/SplashScreen';
import { ErrorBoundary } from './components/common/ErrorBoundary';

export const App: React.FC = () => {
  const [splashDone, setSplashDone] = useState(false);

  return (
    <ErrorBoundary>
      <AppRoutes />
      {!splashDone && (
        <SplashScreen
          durationMs={5400}
          onFinish={() => setSplashDone(true)}
        />
      )}
    </ErrorBoundary>
  );
};

export default App;
