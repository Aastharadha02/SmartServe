import React, { useEffect, useState, useCallback } from 'react';
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
  MessageSquare, 
  ShieldCheck, 
  Mail, 
  Menu, 
  X as XIcon, 
  ChevronDown, 
  Sparkles, 
  ArrowUpRight 
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
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);

  useEffect(() => {
    getAuthenticatedAdmin()
      .then((session) => setAdminSession(session))
      .catch((err) => console.error('Failed to load admin session for layout.', err));
  }, []);

  // Close drawer when route changes
  useEffect(() => {
    setDrawerOpen(false);
    setUserDropdownOpen(false);
  }, [location.pathname]);

  // Close drawer on Escape key
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { 
      if (e.key === 'Escape') {
        setDrawerOpen(false);
        setUserDropdownOpen(false);
      }
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);

  // Prevent body scroll when drawer is open on mobile
  useEffect(() => {
    if (drawerOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => { document.body.style.overflow = ''; };
  }, [drawerOpen]);

  const handleLogout = useCallback(() => {
    localStorage.removeItem('smartserve_token');
    localStorage.removeItem('smartserve_user');
    setAdminSession(null);
    navigate('/login');
  }, [navigate]);

  const navItems = [
    { label: 'Dashboard', path: '/admin/dashboard', icon: LayoutDashboard },
    { label: 'Bookings', path: '/admin/bookings', icon: CalendarCheck },
    { label: 'My Services & Catalog', path: '/admin/catalog', icon: FolderTree },
    { label: 'Providers', path: '/admin/providers', icon: Users },
    { label: 'Customers', path: '/admin/customers', icon: Users },
    { label: 'Admins & RBAC', path: '/admin/admins', icon: ShieldAlert },
    { label: 'Insights & Reports', path: '/admin/reports', icon: BarChart3 },
    { label: 'Support & Tickets', path: '/admin/support', icon: HelpCircle },
    { label: 'Email Center', path: '/admin/emails', icon: Mail },
    { label: 'Security Center', path: '/admin/security', icon: ShieldCheck },
    { label: 'Settings', path: '/admin/settings', icon: Settings },
  ];

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/admin/catalog?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  /** Sidebar inner content */
  const SidebarContent = ({ onClose }: { onClose?: () => void }) => (
    <div className="flex flex-col h-full bg-[#FAF7F0] border-r border-[#E5DEC9]">
      {/* Brand Header */}
      <div className="h-20 flex items-center justify-between px-6 border-b border-[#E5DEC9] flex-shrink-0 bg-[#FAF7F0]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl border border-[#E5DEC9] bg-[#FAF7F0] flex items-center justify-center shadow-xs p-1 flex-shrink-0">
            <svg className="w-full h-full" viewBox="0 0 96 96" fill="none">
              <path
                d="M 48 6 L 72 6 A 18 18 0 0 1 90 24 L 90 72 A 18 18 0 0 1 72 90 L 24 90 A 18 18 0 0 1 6 72 L 6 24 A 18 18 0 0 1 24 6 L 48 6 Z"
                stroke="#C9A15A"
                strokeWidth={2.5}
                strokeLinecap="round"
                strokeLinejoin="round"
                fill="none"
              />
              <path
                d="M 62 30 C 62 23, 34 22, 34 38 C 34 54, 62 48, 62 64 C 62 80, 34 78, 34 70"
                stroke="#2F5233"
                strokeWidth={7}
                strokeLinecap="round"
                strokeLinejoin="round"
                fill="none"
              />
            </svg>
          </div>
          <div>
            <div className="flex items-baseline font-serif">
              <span className="font-bold text-[#2F5233] text-lg tracking-tight leading-none">Smart</span>
              <span className="font-bold text-[#C9A15A] text-lg tracking-tight leading-none ml-0.5">Serve</span>
            </div>
            <span className="text-[10px] font-bold text-[#1F2A1E]/60 tracking-wider uppercase mt-1 block font-sans">
              Admin Console
            </span>
          </div>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-[#1F2A1E]/50 hover:bg-[#F2EDE1] hover:text-[#1F2A1E] transition-colors lg:hidden cursor-pointer"
            aria-label="Close menu"
          >
            <XIcon className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3.5 py-5 space-y-1 overflow-y-auto">
        <p className="px-3 text-[10px] font-bold uppercase tracking-wider text-[#1F2A1E]/40 mb-2">Main Menu</p>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.label}
              to={item.path}
              className={({ isActive }: { isActive: boolean }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-[13.5px] font-semibold transition-all ${
                  isActive
                    ? 'bg-[#2F5233] text-white shadow-xs font-bold'
                    : 'text-[#1F2A1E]/75 hover:bg-[#F2EDE1] hover:text-[#1F2A1E]'
                }`
              }
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              <span className="truncate">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Bottom Promo & User Info */}
      <div className="p-4 border-t border-[#E5DEC9] space-y-3 flex-shrink-0 bg-[#F2EDE1]/50">
        {/* Become a Pro Card */}
        <div className="p-3.5 rounded-2xl bg-white border border-[#E5DEC9] shadow-xs">
          <div className="flex items-center justify-between mb-1.5">
            <div className="flex items-center gap-1.5 text-xs font-bold text-[#2F5233]">
              <Sparkles className="w-3.5 h-3.5 text-[#C9A15A]" />
              <span>Become a Pro</span>
            </div>
            <ArrowUpRight className="w-3.5 h-3.5 text-[#1F2A1E]/40" />
          </div>
          <p className="text-[11px] text-[#1F2A1E]/60 font-medium leading-relaxed mb-2.5">
            Register new service providers and unlock top partner earnings.
          </p>
          <NavLink
            to="/admin/providers"
            className="block text-center py-2 px-3 rounded-xl bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs shadow-xs transition-colors"
          >
            Manage Providers
          </NavLink>
        </div>

        {/* User Card */}
        <div className="flex items-center justify-between p-2 rounded-2xl bg-white border border-[#E5DEC9] shadow-xs">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-8 h-8 rounded-full bg-[#2F5233] text-white font-bold text-xs flex items-center justify-center flex-shrink-0">
              {adminSession?.email?.charAt(0).toUpperCase() || 'A'}
            </div>
            <div className="min-w-0 text-xs">
              <p className="font-bold text-[#1F2A1E] truncate">{adminSession?.email?.split('@')[0] || 'Admin'}</p>
              <p className="text-[11px] text-[#1F2A1E]/50 truncate capitalize">{adminSession?.role_name || 'super_admin'}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            title="Sign Out"
            className="p-1.5 text-[#1F2A1E]/40 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors cursor-pointer"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen bg-[#FAF7F0] overflow-hidden font-sans text-[#1F2A1E]">

      {/* DESKTOP SIDEBAR */}
      <aside className="hidden lg:flex w-[260px] bg-[#FAF7F0] border-r border-[#E5DEC9] flex-col flex-shrink-0 z-20 shadow-xs">
        <SidebarContent />
      </aside>

      {/* MOBILE DRAWER BACKDROP */}
      {drawerOpen && (
        <div
          className="fixed inset-0 z-40 bg-[#1F2A1E]/40 backdrop-blur-xs lg:hidden"
          onClick={() => setDrawerOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* MOBILE DRAWER */}
      <aside
        className={`
          fixed top-0 left-0 h-full w-72 bg-[#FAF7F0] border-r border-[#E5DEC9]
          z-50 flex flex-col shadow-xl
          transition-transform duration-300 ease-in-out
          lg:hidden
          ${drawerOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
        aria-modal="true"
        role="dialog"
      >
        <SidebarContent onClose={() => setDrawerOpen(false)} />
      </aside>

      {/* MAIN WRAPPER */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden bg-[#FAF7F0]">
        {/* TOP HEADER */}
        <header className="h-18 bg-[#FAF7F0]/90 backdrop-blur-md border-b border-[#E5DEC9] px-4 sm:px-6 lg:px-8 flex items-center justify-between flex-shrink-0 z-10">
          <div className="flex items-center gap-3 sm:gap-4 flex-1 max-w-2xl">
            <button
              onClick={() => setDrawerOpen(true)}
              className="p-2 rounded-xl text-[#1F2A1E]/70 hover:bg-[#F2EDE1] transition-colors lg:hidden flex-shrink-0 cursor-pointer"
              aria-label="Open navigation menu"
            >
              <Menu className="w-5 h-5" />
            </button>

            {/* Large Search Field */}
            <form onSubmit={handleSearchSubmit} className="relative flex-1 max-w-md">
              <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/40" />
              <input
                type="search"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search for services, bookings, providers..."
                className="w-full bg-white border border-[#E5DEC9] rounded-xl pl-10 pr-4 py-2 text-xs sm:text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/40 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all shadow-xs"
              />
            </form>
          </div>

          {/* Top Header Actions (Notifications, Messages, Avatar) */}
          <div className="flex items-center gap-2.5 sm:gap-3.5">
            <button
              onClick={() => navigate('/admin/bookings')}
              className="p-2.5 rounded-xl text-[#1F2A1E]/60 hover:bg-[#F2EDE1] hover:text-[#1F2A1E] transition-colors relative cursor-pointer"
              title="Bookings Notification"
            >
              <Bell className="w-4 h-4 sm:w-5 sm:h-5" />
              <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-[#C9A15A] ring-2 ring-[#FAF7F0]"></span>
            </button>

            <button
              onClick={() => navigate('/admin/support')}
              className="p-2.5 rounded-xl text-[#1F2A1E]/60 hover:bg-[#F2EDE1] hover:text-[#1F2A1E] transition-colors cursor-pointer"
              title="Support Tickets"
            >
              <MessageSquare className="w-4 h-4 sm:w-5 sm:h-5" />
            </button>

            <div className="h-6 w-px bg-[#E5DEC9] mx-1 hidden sm:block"></div>

            {/* Profile Dropdown */}
            <div className="relative">
              <button
                onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                className="flex items-center gap-2.5 p-1 sm:p-1.5 rounded-xl hover:bg-[#F2EDE1] transition-colors cursor-pointer"
              >
                <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-[#2F5233] text-white font-bold text-xs sm:text-sm flex items-center justify-center shadow-xs flex-shrink-0">
                  {adminSession?.email?.charAt(0).toUpperCase() || 'A'}
                </div>
                <div className="hidden sm:block text-left text-xs">
                  <p className="font-bold text-[#1F2A1E] leading-tight truncate max-w-[120px]">
                    {adminSession?.email?.split('@')[0] || 'Admin User'}
                  </p>
                  <p className="text-[11px] text-[#1F2A1E]/50 font-medium capitalize truncate">
                    {adminSession?.role_name || 'Super Admin'}
                  </p>
                </div>
                <ChevronDown className="w-3.5 h-3.5 text-[#1F2A1E]/40 hidden sm:block" />
              </button>

              {userDropdownOpen && (
                <div className="absolute right-0 mt-2 w-56 bg-white rounded-2xl border border-[#E5DEC9] shadow-lg p-2 z-50 space-y-1 animate-in fade-in zoom-in-95">
                  <div className="px-3 py-2 border-b border-[#E5DEC9] text-xs">
                    <p className="font-bold text-[#1F2A1E] truncate">{adminSession?.email}</p>
                    <span className="inline-block mt-0.5 px-2 py-0.5 rounded-full bg-[#F2EDE1] text-[#2F5233] text-[10px] font-bold uppercase">
                      {adminSession?.role_name || 'Admin'}
                    </span>
                  </div>
                  <NavLink
                    to="/admin/settings"
                    className="flex items-center gap-2.5 px-3 py-2 text-xs font-semibold text-[#1F2A1E]/80 hover:bg-[#F2EDE1] rounded-xl transition-colors"
                  >
                    <Settings className="w-3.5 h-3.5 text-[#1F2A1E]/40" />
                    <span>Account Settings</span>
                  </NavLink>
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-2.5 px-3 py-2 text-xs font-semibold text-rose-600 hover:bg-rose-50 rounded-xl transition-colors text-left cursor-pointer"
                  >
                    <LogOut className="w-3.5 h-3.5 text-rose-500" />
                    <span>Sign Out</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* MAIN SCROLLABLE CONTENT */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 bg-[#FAF7F0]">
          {children}
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;
