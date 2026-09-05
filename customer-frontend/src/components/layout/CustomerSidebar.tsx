import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../auth/useAuth';
import { BackendPulse } from '../common/BackendPulse';
import { 
  Home, 
  Grid, 
  CalendarCheck, 
  HelpCircle, 
  User, 
  LogOut, 
  X
} from 'lucide-react';

export interface CustomerSidebarProps {
  onClose?: () => void;
}

export const CustomerSidebar: React.FC<CustomerSidebarProps> = ({ onClose }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    if (onClose) onClose();
    await logout();
    navigate('/login', { replace: true });
  };

  const navItems = [
    { 
      label: 'Home', 
      path: '/home', 
      icon: Home,
      isActive: location.pathname === '/home' || location.pathname === '/'
    },
    { 
      label: 'Services', 
      path: '/catalog', 
      icon: Grid,
      isActive: location.pathname === '/catalog' || location.pathname.startsWith('/service/') || location.pathname.startsWith('/catalog/')
    },
    { 
      label: 'My Bookings', 
      path: '/bookings', 
      icon: CalendarCheck,
      isActive: location.pathname.startsWith('/bookings')
    },
    { 
      label: 'Support', 
      path: '/support', 
      icon: HelpCircle,
      isActive: location.pathname.startsWith('/support')
    },
    { 
      label: 'Profile', 
      path: '/profile', 
      icon: User,
      isActive: location.pathname.startsWith('/profile')
    },
  ];

  return (
    <div className="flex flex-col h-full bg-[#FAF7F0] border-r border-[#E5DEC9]">
      {/* 1. Brand Header */}
      <div className="h-20 flex items-center justify-between px-6 border-b border-[#E5DEC9] flex-shrink-0 bg-[#FAF7F0]">
        <Link 
          to={user ? "/home" : "/"} 
          onClick={onClose}
          className="flex items-center gap-3 group flex-shrink-0"
        >
          <div className="w-10 h-10 rounded-xl border border-[#E5DEC9] bg-[#FAF7F0] flex items-center justify-center shadow-xs p-1 flex-shrink-0 group-hover:scale-105 transition-transform">
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
              Customer Portal
            </span>
          </div>
        </Link>

        {onClose && (
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-[#1F2A1E]/50 hover:bg-[#F2EDE1] hover:text-[#1F2A1E] transition-colors lg:hidden cursor-pointer"
            aria-label="Close menu"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* 2. Navigation Links */}
      <nav className="flex-1 px-3.5 py-5 space-y-1.5 overflow-y-auto">
        <p className="px-3 text-[10px] font-bold uppercase tracking-wider text-[#1F2A1E]/40 mb-2">Main Menu</p>
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = item.isActive;
          return (
            <Link
              key={item.label}
              to={item.path}
              onClick={onClose}
              className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-[13.5px] font-semibold transition-all ${
                active
                  ? 'bg-[#2F5233] text-white shadow-xs font-bold'
                  : 'text-[#1F2A1E]/75 hover:bg-[#F2EDE1] hover:text-[#1F2A1E]'
              }`}
            >
              <Icon className={`w-4 h-4 flex-shrink-0 ${active ? 'text-white' : 'text-[#1F2A1E]/60'}`} />
              <span className="truncate">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* 3. Bottom Profile & Actions */}
      <div className="p-4 border-t border-[#E5DEC9] space-y-3 flex-shrink-0 bg-[#F2EDE1]/50">
        {/* Backend Pulse Live Indicator */}
        <div className="flex items-center justify-between px-3 py-2 rounded-xl bg-white/70 border border-[#E5DEC9]/80 text-xs font-semibold text-[#1F2A1E]/70">
          <span className="text-[11px] font-medium text-[#1F2A1E]/60">Platform Status</span>
          <BackendPulse />
        </div>

        {/* User Card */}
        {user ? (
          <div className="flex items-center justify-between p-2 rounded-2xl bg-white border border-[#E5DEC9] shadow-xs">
            <Link 
              to="/profile" 
              onClick={onClose} 
              className="flex items-center gap-2.5 min-w-0 flex-1 hover:opacity-80 transition-opacity"
            >
              <div className="w-8 h-8 rounded-full bg-[#2F5233] text-white font-bold text-xs flex items-center justify-center flex-shrink-0 uppercase">
                {user.full_name?.charAt(0) || user.email?.charAt(0) || 'C'}
              </div>
              <div className="min-w-0 text-xs">
                <p className="font-bold text-[#1F2A1E] truncate">{user.full_name || user.email?.split('@')[0] || 'Customer'}</p>
                <p className="text-[11px] text-[#1F2A1E]/50 truncate font-medium">Verified Customer</p>
              </div>
            </Link>
            <button
              onClick={handleLogout}
              title="Sign Out"
              className="p-1.5 text-[#1F2A1E]/40 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors cursor-pointer flex-shrink-0"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <div className="p-3 rounded-2xl bg-white border border-[#E5DEC9] shadow-xs space-y-2">
            <div>
              <p className="text-xs font-bold text-[#1F2A1E]">Welcome to SmartServe</p>
              <p className="text-[11px] text-[#1F2A1E]/60 font-medium leading-tight">Access bookings & personalized services.</p>
            </div>
            <Link
              to="/login"
              onClick={onClose}
              className="block text-center py-2 px-3 rounded-xl bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs shadow-xs transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              onClick={onClose}
              className="block text-center py-1.5 px-3 rounded-xl text-[#1F2A1E]/75 hover:bg-[#FAF7F0] font-semibold text-xs transition-colors"
            >
              Create Account
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default CustomerSidebar;
