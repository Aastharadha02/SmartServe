import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../auth/useAuth';
import { BackendPulse } from '../common/BackendPulse';
import { 
  Home, 
  Grid, 
  Calendar, 
  HelpCircle, 
  LogOut, 
  Search, 
  Menu, 
  X,
  Sparkles
} from 'lucide-react';

export const CustomerNavbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/catalog?q=${encodeURIComponent(searchQuery.trim())}`);
      setSearchQuery('');
    }
  };

  const navLinks = [
    { label: 'Home', path: '/home', icon: Home },
    { label: 'Services', path: '/catalog', icon: Grid },
    { label: 'My Bookings', path: '/bookings', icon: Calendar },
    { label: 'Support', path: '/support', icon: HelpCircle },
  ];

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-40 bg-[#FAF7F0]/95 backdrop-blur-md border-b border-[#E5DEC9] shadow-2xs font-sans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20 gap-4">
          
          {/* 1. Brand Logo */}
          <Link to={user ? "/home" : "/"} className="flex items-center gap-3 group flex-shrink-0">
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
                Marketplace
              </span>
            </div>
          </Link>

          {/* 2. Global Search Bar */}
          <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-md mx-4 relative">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/40" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search AC repair, cleaning, plumbing..."
              className="w-full h-10 bg-[#F2EDE1]/60 border border-[#E5DEC9] rounded-xl pl-10 pr-4 text-xs font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/40 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] focus:bg-white transition-all"
            />
          </form>

          {/* 3. Navigation Links & Backend Pulse */}
          <div className="hidden lg:flex items-center gap-6">
            <nav className="flex items-center gap-1">
              {navLinks.map((link) => {
                const Icon = link.icon;
                const isActive = location.pathname === link.path || (link.path !== '/home' && location.pathname.startsWith(link.path));
                return (
                  <Link
                    key={link.path}
                    to={link.path}
                    className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${
                      isActive
                        ? 'bg-[#2F5233] text-white shadow-xs font-bold'
                        : 'text-[#1F2A1E]/75 hover:text-[#1F2A1E] hover:bg-[#F2EDE1]'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{link.label}</span>
                  </Link>
                );
              })}
            </nav>

            <BackendPulse />

            {/* Auth Buttons / Profile */}
            {user ? (
              <div className="flex items-center gap-3 pl-2 border-l border-[#E5DEC9]">
                <Link
                  to="/profile"
                  className="flex items-center gap-2.5 p-1.5 pr-3 rounded-xl hover:bg-[#F2EDE1] transition-colors"
                >
                  <div className="w-8 h-8 rounded-full bg-[#2F5233] text-white font-bold text-xs flex items-center justify-center border border-[#3D6B42] uppercase">
                    {user.full_name ? user.full_name.charAt(0) : 'C'}
                  </div>
                  <div className="text-left">
                    <span className="text-xs font-bold text-[#1F2A1E] block truncate max-w-[110px]">{user.full_name || 'Customer'}</span>
                    <span className="text-[10px] text-[#1F2A1E]/50 font-medium block">Verified Customer</span>
                  </div>
                </Link>

                <button
                  onClick={handleLogout}
                  title="Sign Out"
                  className="p-2 text-[#1F2A1E]/50 hover:text-rose-600 hover:bg-rose-50 rounded-xl transition-colors cursor-pointer"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2.5 pl-2 border-l border-[#E5DEC9]">
                <Link
                  to="/login"
                  className="px-4 py-2 text-xs font-bold text-[#1F2A1E] hover:text-[#2F5233] transition-colors"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs rounded-xl shadow-xs transition-colors flex items-center gap-1.5"
                >
                  <Sparkles className="w-3.5 h-3.5 text-[#C9A15A]" />
                  <span>Get Started</span>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Toggle Button */}
          <div className="flex lg:hidden items-center gap-2">
            <BackendPulse />
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-[#1F2A1E] hover:bg-[#F2EDE1] rounded-xl cursor-pointer"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-[#E5DEC9] bg-[#FAF7F0] p-4 space-y-4 shadow-lg animate-in slide-in-from-top-2">
          <form onSubmit={handleSearch} className="relative">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/40" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search services..."
              className="w-full h-10 bg-[#F2EDE1] border border-[#E5DEC9] rounded-xl pl-10 pr-4 text-sm font-medium text-[#1F2A1E] focus:outline-none"
            />
          </form>

          <nav className="space-y-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname === link.path;
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold transition-colors ${
                    isActive ? 'bg-[#2F5233] text-white' : 'text-[#1F2A1E] hover:bg-[#F2EDE1]'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{link.label}</span>
                </Link>
              );
            })}
          </nav>

          <div className="pt-3 border-t border-[#E5DEC9]">
            {user ? (
              <div className="space-y-2">
                <Link
                  to="/profile"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-3 p-3 bg-[#F2EDE1] rounded-xl"
                >
                  <div className="w-9 h-9 rounded-full bg-[#2F5233] text-white font-bold flex items-center justify-center">
                    {user.full_name ? user.full_name.charAt(0) : 'C'}
                  </div>
                  <div>
                    <span className="font-bold text-[#1F2A1E] text-sm block">{user.full_name}</span>
                    <span className="text-xs text-[#1F2A1E]/50 block">{user.email}</span>
                  </div>
                </Link>
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    handleLogout();
                  }}
                  className="w-full py-3 bg-rose-50 text-rose-600 font-bold rounded-xl text-sm flex items-center justify-center gap-2 cursor-pointer"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Sign Out</span>
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-2">
                <Link
                  to="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="py-3 text-center bg-[#F2EDE1] font-bold text-[#1F2A1E] rounded-xl text-sm hover:bg-[#E5DEC9]"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="py-3 text-center bg-[#2F5233] font-bold text-white rounded-xl text-sm hover:bg-[#3D6B42]"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

export default CustomerNavbar;
