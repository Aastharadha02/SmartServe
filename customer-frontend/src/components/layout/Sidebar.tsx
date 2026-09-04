import { FC } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../auth/useAuth';
import { useToast } from '../../hooks/useToast';
import { Home, Compass, CalendarCheck, LifeBuoy, User, LogOut, X } from 'lucide-react';

export interface SidebarProps {
  isOpenMobile?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: FC<SidebarProps> = ({
  isOpenMobile = false,
  onCloseMobile,
}) => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { showToast } = useToast();

  const navItems = [
    { label: 'Home', path: '/home', icon: <Home className="h-5 w-5" /> },
    { label: 'Explore', path: '/explore', icon: <Compass className="h-5 w-5" /> },
    { label: 'Bookings', path: '/bookings', icon: <CalendarCheck className="h-5 w-5" /> },
    { label: 'Support', path: '/support', icon: <LifeBuoy className="h-5 w-5" /> },
    { label: 'Profile', path: '/profile', icon: <User className="h-5 w-5" /> },
  ];

  const handleLogout = async () => {
    try {
      await logout();
      showToast('Signed out successfully', 'info');
      navigate('/login', { replace: true });
    } catch {
      showToast('Failed to sign out', 'error');
    }
  };

  const navContent = (
    <div className="flex h-full flex-col justify-between p-4 bg-white border-r border-slate-200">
      <div>
        {/* Mobile Header in Drawer */}
        <div className="flex items-center justify-between lg:hidden pb-4 mb-4 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#2563EB] text-white">
              <svg className="h-5 w-5" viewBox="0 0 100 100" fill="none">
                <path d="M68 32C68 25.3726 62.6274 20 56 20H38C30.268 20 24 26.268 24 34C24 41.732 30.268 48 38 48H62C69.732 48 76 54.268 76 62C76 69.732 69.732 76 62 76H44C37.3726 76 32 70.6274 32 64" stroke="currentColor" strokeWidth="12" strokeLinecap="round" />
              </svg>
            </div>
            <span className="font-extrabold text-slate-900 text-lg">SmartServe</span>
          </div>
          <button
            onClick={onCloseMobile}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 transition"
            aria-label="Close menu"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="space-y-1.5">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={onCloseMobile}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold transition-all duration-150 ${
                  isActive
                    ? 'bg-[#EFF6FF] text-[#2563EB] shadow-xs'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                }`
              }
            >
              {item.icon}
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      {/* Logout Action */}
      <div className="pt-4 border-t border-slate-100">
        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold text-rose-600 hover:bg-rose-50 transition active:scale-[0.98]"
        >
          <LogOut className="h-5 w-5" />
          <span>Log out</span>
        </button>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Static Rail */}
      <aside className="hidden lg:block w-[260px] shrink-0 h-[calc(100vh-72px)] sticky top-[72px]">
        {navContent}
      </aside>

      {/* Mobile Drawer */}
      {isOpenMobile && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div
            className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs transition-opacity animate-fade-in"
            onClick={onCloseMobile}
          />
          <div className="fixed inset-y-0 left-0 w-72 max-w-[80vw] bg-white shadow-2xl animate-fade-in z-10">
            {navContent}
          </div>
        </div>
      )}
    </>
  );
};
