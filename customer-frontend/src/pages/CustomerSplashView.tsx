import React from 'react';
import { useNavigate } from 'react-router-dom';
import { SplashScreen } from '../components/common/SplashScreen';
import { useAuth } from '../auth/useAuth';

export const CustomerSplashView: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleFinish = () => {
    if (user) {
      navigate('/home', { replace: true });
    } else {
      navigate('/login', { replace: true });
    }
  };

  return <SplashScreen onFinish={handleFinish} durationMs={8000} />;
};

export default CustomerSplashView;
