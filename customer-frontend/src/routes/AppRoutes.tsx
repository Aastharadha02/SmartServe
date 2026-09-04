import React, { ReactNode } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../auth/useAuth';
import { CustomerLayout } from '../components/layout/CustomerLayout';

// Pages
import CustomerSplashView from '../pages/CustomerSplashView';
import CustomerLogin from '../pages/auth/CustomerLogin';
import CustomerRegister from '../pages/auth/CustomerRegister';
import CustomerHome from '../pages/CustomerHome';
import CustomerCatalog from '../pages/CustomerCatalog';
import CustomerServiceDetail from '../pages/CustomerServiceDetail';
import CustomerBookings from '../pages/CustomerBookings';
import CustomerBookingDetail from '../pages/CustomerBookingDetail';
import CustomerSupport from '../pages/CustomerSupport';
import CustomerSupportDetail from '../pages/CustomerSupportDetail';
import CustomerProfile from '../pages/CustomerProfile';

interface ProtectedRouteProps {
  children: ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { token, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center font-sans text-sm font-semibold text-slate-600">
        Verifying Customer Session...
      </div>
    );
  }

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* 1. Splash Screen Initial Landing */}
      <Route path="/" element={<CustomerSplashView />} />

      {/* 2. Public Auth Routes */}
      <Route path="/login" element={<CustomerLogin />} />
      <Route path="/register" element={<CustomerRegister />} />

      {/* 3. Customer Application Routes (Wrapped in CustomerLayout) */}
      <Route
        path="/home"
        element={
          <CustomerLayout>
            <CustomerHome />
          </CustomerLayout>
        }
      />

      <Route
        path="/catalog"
        element={
          <CustomerLayout>
            <CustomerCatalog />
          </CustomerLayout>
        }
      />

      <Route
        path="/service/:serviceId"
        element={
          <CustomerLayout>
            <CustomerServiceDetail />
          </CustomerLayout>
        }
      />

      {/* Protected Routes */}
      <Route
        path="/bookings"
        element={
          <ProtectedRoute>
            <CustomerLayout>
              <CustomerBookings />
            </CustomerLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/bookings/:bookingId"
        element={
          <ProtectedRoute>
            <CustomerLayout>
              <CustomerBookingDetail />
            </CustomerLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/support"
        element={
          <ProtectedRoute>
            <CustomerLayout>
              <CustomerSupport />
            </CustomerLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/support/:ticketId"
        element={
          <ProtectedRoute>
            <CustomerLayout>
              <CustomerSupportDetail />
            </CustomerLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <CustomerLayout>
              <CustomerProfile />
            </CustomerLayout>
          </ProtectedRoute>
        }
      />

      {/* Catch-all fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRoutes;
