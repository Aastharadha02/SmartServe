import React, { ReactNode, useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { CustomerSidebar } from './CustomerSidebar';
import { CustomerFooter } from './CustomerFooter';
import { BackendPulse } from '../common/BackendPulse';
import { Menu } from 'lucide-react';

interface CustomerLayoutProps {
  children: ReactNode;
}

export const CustomerLayout: React.FC<CustomerLayoutProps> = ({ children }) => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const location = useLocation();

  // Close drawer on route change
  useEffect(() => {
    setDrawerOpen(false);
  }, [location.pathname]);

  // Close drawer on Escape key
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setDrawerOpen(false);
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);

  // Prevent body scroll when drawer is open
  useEffect(() => {
    if (drawerOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [drawerOpen]);

  return (
    <div className="flex min-h-screen bg-[#FAF7F0] font-sans text-[#1F2A1E] selection:bg-[#2F5233] selection:text-white">
      {/* 1. DESKTOP VERTICAL SIDEBAR (Fixed / Sticky Left) */}
      <aside className="hidden lg:flex w-[260px] bg-[#FAF7F0] border-r border-[#E5DEC9] flex-col flex-shrink-0 sticky top-0 h-screen z-20 shadow-xs">
        <CustomerSidebar />
      </aside>

      {/* 2. MOBILE DRAWER BACKDROP */}
      {drawerOpen && (
        <div
          className="fixed inset-0 z-40 bg-[#1F2A1E]/40 backdrop-blur-xs lg:hidden"
          onClick={() => setDrawerOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* 3. MOBILE RESPONSIVE DRAWER */}
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
        <CustomerSidebar onClose={() => setDrawerOpen(false)} />
      </aside>

      {/* 4. MAIN CONTENT AREA (Occupies Remaining Width) */}
      <div className="flex-1 flex flex-col min-w-0 min-h-screen bg-[#FAF7F0]">
        {/* Mobile Header (Only visible on screens < lg) */}
        <header className="lg:hidden h-16 bg-[#FAF7F0]/95 backdrop-blur-md border-b border-[#E5DEC9] px-4 flex items-center justify-between sticky top-0 z-30 flex-shrink-0">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setDrawerOpen(true)}
              className="p-2 rounded-xl text-[#1F2A1E]/70 hover:bg-[#F2EDE1] transition-colors cursor-pointer"
              aria-label="Open navigation menu"
            >
              <Menu className="w-5 h-5" />
            </button>
            <Link to="/home" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg border border-[#E5DEC9] bg-[#FAF7F0] flex items-center justify-center p-0.5">
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
              <span className="font-serif font-bold text-[#2F5233] text-base">
                Smart<span className="text-[#C9A15A]">Serve</span>
              </span>
            </Link>
          </div>
          <BackendPulse />
        </header>

        {/* Existing Customer Page Content */}
        <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
          {children}
        </main>

        {/* Customer Footer */}
        <CustomerFooter />
      </div>
    </div>
  );
};

export default CustomerLayout;
