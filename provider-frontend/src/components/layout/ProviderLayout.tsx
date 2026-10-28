import React, { useState, useEffect, useRef, useCallback } from 'react';
import { NavLink, useNavigate, Outlet, Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Briefcase,
  Calendar,
  User as UserIcon,
  LifeBuoy,
  LogOut,
  Menu,
  X,
  Star,
  ShieldCheck,
  ChevronDown,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useTranslation } from 'react-i18next';
import { apiClient } from '../../api/client';
import { BackendPulse } from '../common/BackendPulse';
import { AISupportAssistant } from '../common/AISupportAssistant';
import { LanguageSelector } from '../common/LanguageSelector';
import { ProviderNotificationSystem } from '../notifications/ProviderNotificationSystem';

export const ProviderLayout: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [profile, setProfile] = useState<any>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const res = await apiClient.get('/providers/me');
        setProfile(res.data);
      } catch (err) {
        console.error('Failed to load profile in layout', err);
      }
    };
    if (user) {
      loadProfile();
    }
  }, [user]);

  // Close drawer and dropdown on route change
  useEffect(() => {
    setDrawerOpen(false);
    setUserDropdownOpen(false);
  }, [location.pathname]);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setUserDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = useCallback(() => {
    logout();
    navigate('/login');
  }, [logout, navigate]);

  const { t } = useTranslation();

  const navItems = [
    { label: t('nav.dashboard', { defaultValue: 'Dashboard' }), path: '/dashboard', icon: LayoutDashboard },
    { label: t('nav.services', { defaultValue: 'My Services' }), path: '/services', icon: Briefcase },
    { label: t('nav.availability', { defaultValue: 'Availability' }), path: '/availability', icon: Calendar },
    { label: t('nav.profile', { defaultValue: 'Profile & Trust' }), path: '/profile', icon: UserIcon },
    { label: t('nav.support', { defaultValue: 'Support Tickets' }), path: '/support', icon: LifeBuoy },
  ];

  const providerName = profile?.full_name || (user?.email ? user.email.split('@')[0] : 'Partner');
  const providerCategory = profile?.category || 'General Services';
  const rating = profile?.rating || 4.9;

  return (
    <div className="min-h-screen bg-[#FAF7F0] flex font-sans text-[#1F2A1E]">
      {/* ── Mobile Sidebar Backdrop ── */}
      {drawerOpen && (
        <div
          className="drawer-backdrop lg:hidden"
          onClick={() => setDrawerOpen(false)}
        />
      )}

      {/* ══════════════════════════════════════════════════
          SIDEBAR NAVIGATION (Desktop: Fixed Sticky, Mobile: Drawer)
          ════════════════════════════════════════════════*/}
      <aside
        className={`fixed top-0 bottom-0 left-0 h-screen w-72 bg-white/95 backdrop-blur-md border-r border-[#E5DEC9] z-40 flex flex-col justify-between transition-transform duration-300 ease-in-out ${
          drawerOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div>
          {/* Brand Logo & Wordmark Header */}
          <div className="h-20 flex items-center justify-between px-6 border-b border-[#E5DEC9]">
            <Link to="/dashboard" className="flex items-center gap-3 group">
              <div className="w-11 h-11 rounded-xl border border-[#E5DEC9] bg-[#FAF7F0] flex items-center justify-center shadow-xs p-1 flex-shrink-0 group-hover:scale-105 transition-transform">
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
                  <span className="text-xl font-bold text-[#2F5233] tracking-tight">Smart</span>
                  <span className="text-xl font-bold text-[#C9A15A] tracking-tight ml-0.5">Serve</span>
                </div>
                <span className="block text-[10px] text-[#7A9E6E] font-semibold uppercase tracking-wider -mt-0.5">
                  Partner Console
                </span>
              </div>
            </Link>

            {/* Mobile close button */}
            <button
              onClick={() => setDrawerOpen(false)}
              className="lg:hidden p-2 rounded-xl text-[#1F2A1E]/50 hover:bg-[#FAF7F0] hover:text-[#1F2A1E]"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation Links */}
          <nav className="p-4 space-y-1.5 overflow-y-auto max-h-[calc(100vh-190px)]">
            <div className="text-[10px] font-bold text-[#1F2A1E]/40 uppercase tracking-widest px-3 py-2">
              Workspace Menu
            </div>

            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-3 rounded-2xl text-xs sm:text-sm transition-all duration-200 ${
                    isActive
                      ? 'bg-[#2F5233] text-white font-bold shadow-xs shadow-[#2F5233]/20'
                      : 'text-[#1F2A1E]/75 font-semibold hover:bg-[#F2EDE1] hover:text-[#2F5233]'
                  }`
                }
              >
                <item.icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        {/* Partner Trust & User Footer in Sidebar */}
        <div className="p-4 border-t border-[#E5DEC9] bg-[#FAF7F0]/60">
          <div className="p-3 bg-white rounded-2xl border border-[#E5DEC9] flex items-center justify-between shadow-2xs">
            <div className="flex items-center gap-2.5 overflow-hidden">
              <div className="w-9 h-9 rounded-xl bg-[#2F5233] text-white flex items-center justify-center font-bold text-sm shrink-0 shadow-xs">
                {providerName.charAt(0)}
              </div>
              <div className="overflow-hidden">
                <p className="text-xs font-bold text-[#1F2A1E] truncate">{providerName}</p>
                <div className="flex items-center gap-1 text-[10px] font-semibold text-emerald-700">
                  <ShieldCheck className="w-3 h-3 text-emerald-600 shrink-0" />
                  <span className="truncate">Verified Partner</span>
                </div>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="p-2 text-[#1F2A1E]/40 hover:text-red-600 hover:bg-red-50 rounded-xl transition-colors shrink-0"
              title="Sign Out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* ══════════════════════════════════════════════════
          MAIN CONTENT AREA
          ════════════════════════════════════════════════*/}
      <div className="flex-1 flex flex-col min-w-0 lg:pl-72">
        {/* Top Header Navbar */}
        <header className="sticky top-0 z-30 bg-[#FAF7F0]/95 backdrop-blur-md border-b border-[#E5DEC9] h-20 flex items-center justify-between px-4 sm:px-8">
          <div className="flex items-center gap-4">
            {/* Mobile menu toggle button */}
            <button
              onClick={() => setDrawerOpen(true)}
              className="lg:hidden p-2 rounded-xl border border-[#E5DEC9] bg-white text-[#1F2A1E] hover:bg-[#F2EDE1]"
              aria-label="Open navigation menu"
            >
              <Menu className="w-5 h-5" />
            </button>

            {/* Live API Pulse Indicator */}
            <BackendPulse />
          </div>

          {/* Right Header Controls */}
          <div className="flex items-center gap-3">
            {/* Real-time Booking Notification Dropdown & Popup */}
            <ProviderNotificationSystem />

            {/* Rating / Tier Badge */}
            <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 bg-white rounded-xl border border-[#E5DEC9] text-xs font-bold shadow-2xs">
              <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
              <span>{rating}</span>
              <span className="text-slate-400 font-normal">(Elite Tier)</span>
            </div>

            {/* Verification Status Pill */}
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border shadow-xs bg-emerald-50 text-emerald-700 border-emerald-200">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse" />
              <span>{t('common.verified_partner', { defaultValue: 'Verified Partner' })}</span>
            </span>

            {/* Language Selector */}
            <LanguageSelector />

            {/* Profile Dropdown */}
            <div className="relative" ref={dropdownRef}>
              <button
                onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                className="flex items-center gap-2 p-1.5 rounded-xl border border-[#E5DEC9] bg-white hover:bg-[#F2EDE1] transition-colors"
                aria-label="Partner account menu"
              >
                <div className="w-8 h-8 rounded-lg bg-[#2F5233] text-white flex items-center justify-center font-bold text-xs">
                  {providerName.charAt(0)}
                </div>
                <ChevronDown className="w-3.5 h-3.5 text-[#1F2A1E]/60 hidden sm:block mr-1" />
              </button>

              {userDropdownOpen && (
                <div className="absolute right-0 mt-2 w-56 bg-white rounded-2xl border border-[#E5DEC9] shadow-lg p-2 z-50 text-xs animate-in fade-in">
                  <div className="p-3 border-b border-[#E5DEC9]/60">
                    <p className="font-bold text-[#1F2A1E] truncate">{providerName}</p>
                    <p className="text-[11px] text-[#1F2A1E]/60 truncate font-mono mt-0.5">{user?.email}</p>
                    <span className="inline-block mt-1.5 text-[10px] font-bold text-[#2F5233] bg-[#F2EDE1] px-2 py-0.5 rounded-md border border-[#E5DEC9]">
                      {providerCategory}
                    </span>
                  </div>
                  <div className="py-1">
                    <Link
                      to="/profile"
                      className="flex items-center gap-2 px-3 py-2 rounded-xl text-[#1F2A1E]/80 hover:bg-[#FAF7F0] font-semibold transition-colors"
                    >
                      <UserIcon className="w-4 h-4 text-[#2F5233]" />
                      <span>Profile & Trust Score</span>
                    </Link>
                    <Link
                      to="/services"
                      className="flex items-center gap-2 px-3 py-2 rounded-xl text-[#1F2A1E]/80 hover:bg-[#FAF7F0] font-semibold transition-colors"
                    >
                      <Briefcase className="w-4 h-4 text-[#2F5233]" />
                      <span>Manage Services</span>
                    </Link>
                    <Link
                      to="/support"
                      className="flex items-center gap-2 px-3 py-2 rounded-xl text-[#1F2A1E]/80 hover:bg-[#FAF7F0] font-semibold transition-colors"
                    >
                      <LifeBuoy className="w-4 h-4 text-[#2F5233]" />
                      <span>Partner Support</span>
                    </Link>
                  </div>
                  <div className="pt-1 border-t border-[#E5DEC9]/60">
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-red-600 hover:bg-red-50 font-bold transition-colors text-left"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Sign Out</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Dynamic Page Outlet */}
        <main className="flex-1 p-4 sm:p-8 max-w-7xl w-full mx-auto">
          <Outlet />
        </main>

        {/* Floating AI Support Assistant */}
        <AISupportAssistant role="provider" />
      </div>
    </div>
  );
};

export default ProviderLayout;
