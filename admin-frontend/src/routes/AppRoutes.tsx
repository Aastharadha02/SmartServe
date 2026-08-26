import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Login } from '../pages/Login';
import { Dashboard } from '../pages/admin/Dashboard';
import { AdminLayout } from '../components/layout/AdminLayout';

// Catalog 4-Level Information Architecture
import { CategoryListView } from '../pages/admin/catalog/CategoryListView';
import { SubcategoryListView } from '../pages/admin/catalog/SubcategoryListView';
import { ServiceListView } from '../pages/admin/catalog/ServiceListView';
import { ServiceDetailEditView } from '../pages/admin/catalog/ServiceDetailEditView';

// Providers Module
import { ProviderListView } from '../pages/admin/providers/ProviderListView';
import { ProviderDetailView } from '../pages/admin/providers/ProviderDetailView';

// Customers Module
import { CustomerListView } from '../pages/admin/customers/CustomerListView';
import { CustomerDetailView } from '../pages/admin/customers/CustomerDetailView';

// Admins & RBAC Module
import { AdminListView } from '../pages/admin/admins/AdminListView';
import { AdminDetailView } from '../pages/admin/admins/AdminDetailView';

// Bookings & Operations Module
import { BookingListView } from '../pages/admin/bookings/BookingListView';
import { BookingDetailView } from '../pages/admin/bookings/BookingDetailView';

// Support Center Module
import { SupportListView } from '../pages/admin/support/SupportListView';
import { SupportDetailView } from '../pages/admin/support/SupportDetailView';

// Email Center Module
import { EmailCenterView } from '../pages/admin/emails/EmailCenterView';

// Reports & Analytics Module
import { ReportsAnalyticsView } from '../pages/admin/reports/ReportsAnalyticsView';

// Security Center Module
import { SecurityCenterView } from '../pages/admin/security/SecurityCenterView';

// Settings & Admin Configuration Module
import { SettingsView } from '../pages/admin/settings/SettingsView';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const token = localStorage.getItem('smartserve_token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
};

export const AppRoutes: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        {/* Dashboard */}
        <Route
          path="/admin/dashboard"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <Dashboard />
              </AdminLayout>
            </ProtectedRoute>
          }
        />

        {/* Catalog 4-Level Information Architecture */}
        <Route
          path="/admin/catalog"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <CategoryListView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/catalog/category/:categoryName"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <SubcategoryListView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/catalog/category/:categoryName/subcategory/:subcategoryName"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <ServiceListView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/catalog/service/:serviceId"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <ServiceDetailEditView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />

        {/* Providers Module */}
        <Route
          path="/admin/providers"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <ProviderListView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/providers/:providerId"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <ProviderDetailView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />

        {/* Customers Module */}
        <Route
          path="/admin/customers"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <CustomerListView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/customers/:customerId"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <CustomerDetailView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />

        {/* Admins & RBAC Module */}
        <Route
          path="/admin/admins"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <AdminListView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/admins/:adminId"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <AdminDetailView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />

        {/* Bookings & Operations Module */}
        <Route
          path="/admin/bookings"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <BookingListView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/bookings/:bookingId"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <BookingDetailView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />

        {/* Support Center Module */}
        <Route
          path="/admin/support"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <SupportListView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/support/:ticketId"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <SupportDetailView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />

        {/* Email Center Module */}
        <Route
          path="/admin/emails"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <EmailCenterView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />

        {/* Reports & Analytics Module View */}
        <Route
          path="/admin/reports"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <ReportsAnalyticsView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />

        {/* Security & Risk Center Module View */}
        <Route
          path="/admin/security"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <SecurityCenterView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />

        {/* Settings & Configuration Module View */}
        <Route
          path="/admin/settings"
          element={
            <ProtectedRoute>
              <AdminLayout>
                <SettingsView />
              </AdminLayout>
            </ProtectedRoute>
          }
        />

        <Route path="/" element={<Navigate to="/admin/dashboard" replace />} />
        <Route path="*" element={<Navigate to="/admin/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
};
