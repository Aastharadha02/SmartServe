import React, { ReactNode } from 'react';
import { CustomerNavbar } from './CustomerNavbar';
import { CustomerFooter } from './CustomerFooter';

interface CustomerLayoutProps {
  children: ReactNode;
}

export const CustomerLayout: React.FC<CustomerLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans selection:bg-[#2563EB] selection:text-white">
      <CustomerNavbar />
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      <CustomerFooter />
    </div>
  );
};

export default CustomerLayout;
