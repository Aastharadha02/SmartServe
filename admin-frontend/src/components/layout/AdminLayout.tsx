import React, { useEffect, useState } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FolderTree, 
  Users, 
  CalendarCheck, 
  BarChart3, 
  HelpCircle, 
  ShieldAlert, 
  Settings, 
  LogOut, 
  Search, 
  Bell, 
  User as UserIcon,
  ShieldCheck,
  Mail
} from 'lucide-react';
import { getAuthenticatedAdmin } from '../../api/admins';
import type { SessionAdminInfo } from '../../api/admins';

interface AdminLayoutProps {
  children: React.ReactNode;
}

export const AdminLayout: React.FC<AdminLayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);

  useEffect(() => {
    getAuthenticatedAdmin()
      .then((session) => setAdminSession(session))
      .catch((err) => console.error('Failed to load admin session for layout.', err));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('smartserve_token');
    localStorage.removeItem('smartserve_user');
    setAdminSession(null);
    navigate('/login');
  };

  const navItems = [
    { label: 'Dashboard', path: '/admin/dashboard', icon: LayoutDashboard },
    { label: 'Catalog', path: '/admin/catalog', icon: FolderTree },
    { label: 'Providers', path: '/admin/providers', icon: Users },
    { label: 'Customers', path: '/admin/customers', icon: Users },
    { label: 'Admins & RBAC', path: '/admin/admins', icon: ShieldAlert },
    { label: 'Bookings', path: '/admin/bookings', icon: CalendarCheck },
    { label: 'Insights', path: '/admin/reports', icon: BarChart3 },
    { label: 'Support', path: '/admin/support', icon: HelpCircle },
    { label: 'Email Center', path: '/admin/emails', icon: Mail },
    { label: 'Security', path: '/admin/security', icon: ShieldAlert },
    { label: 'Settings', path: '/admin/settings', icon: Settings },
  ];

  const getPageTitle = () => {
    const active = navItems.find((item) => item.path === location.pathname);
    return active ? active.label : 'Operations Dashboard';
  };

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans text-slate-800">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col justify-between flex-shrink-0 z-20">
        <div>
          {/* Logo Header */}
          <div className="h-16 flex items-center px-6 border-b border-slate-100 gap-3">
            <div className="w-9 h-9 rounded-xl bg-[#5CA8FF] flex items-center justify-center text-white font-bold text-lg shadow-sm">
              S
            </div>
            <div>
              <h1 className="font-bold text-slate-900 leading-tight">SmartServe</h1>
              <span className="text-xs font-semibold text-[#5CA8FF] uppercase tracking-wider">Admin Console</span>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="p-4 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.label}
                  to={item.path}
                  className={({ isActive }: { isActive: boolean }) =>
                    `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-blue-50 text-[#5CA8FF] font-semibold'
                        : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                    }`
                  }
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Bottom User Info & Logout */}
        <div className="p-4 border-t border-slate-100 space-y-3">
          <div className="flex items-center gap-3 p-2 rounded-lg bg-slate-50 border border-slate-200/60">
            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-[#5CA8FF]">
              <UserIcon className="w-4 h-4" />
            </div>
            <div className="overflow-hidden text-xs">
              <p className="font-semibold text-slate-800 truncate">{adminSession?.email || 'admin@smartserve.com'}</p>
              <div className="flex items-center gap-1 text-slate-500">
                <ShieldCheck className="w-3 h-3 text-[#5CA8FF]" />
                <span className="capitalize">{adminSession?.role_name || 'super_admin'}</span>
              </div>
            </div>
          </div>

          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:bg-red-50 hover:text-red-600 border border-slate-200 transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Main Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 flex-shrink-0 z-10">
          <div className="flex items-center gap-4">
            <h2 className="text-xl font-bold text-slate-900">{getPageTitle()}</h2>
          </div>

          <div className="flex items-center gap-4">
            {/* Search Placeholder */}
            <div className="relative w-64">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Search bookings, providers..."
                className="w-full bg-slate-50 text-sm border border-slate-200 rounded-lg pl-9 pr-4 py-1.5 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 focus:border-[#5CA8FF] transition-all"
                disabled
              />
            </div>

            {/* Notification Bell */}
            <button className="relative p-2 rounded-lg text-slate-500 hover:bg-slate-100 transition-colors">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-[#5CA8FF] rounded-full"></span>
            </button>

            {/* Admin Badge */}
            <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
              <div className="w-8 h-8 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs font-bold">
                SA
              </div>
              <span className="text-xs font-semibold text-slate-700">Admin Console</span>
            </div>
          </div>
        </header>

        {/* Dynamic Page Content Area */}
        <main className="flex-1 overflow-y-auto p-8">
          {children}
        </main>
      </div>
    </div>
  );
};
