import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Phone, Mail, MapPin } from 'lucide-react';

export const CustomerFooter: React.FC = () => {
  return (
    <footer className="bg-[#1F2A1E] text-[#FAF7F0] pt-14 pb-8 font-sans border-t border-[#2F5233]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Top Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          
          {/* Brand Info (2 cols) */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl border border-[#C9A15A]/40 bg-[#FAF7F0] flex items-center justify-center shadow-xs p-1 flex-shrink-0">
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
              <div className="flex items-baseline font-serif">
                <span className="font-bold text-white text-xl tracking-tight leading-none">Smart</span>
                <span className="font-bold text-[#C9A15A] text-xl tracking-tight leading-none ml-0.5">Serve</span>
              </div>
            </div>
            <p className="text-[#FAF7F0]/70 text-sm font-normal leading-relaxed max-w-sm">
              India's premier verified home and urban services marketplace. Professional salon, deep cleaning, AC repair, plumbing, electrical, and lifestyle services delivered to your doorstep.
            </p>
            <div className="pt-2 flex items-center gap-3 text-xs text-emerald-400 font-semibold">
              <ShieldCheck className="w-4 h-4" />
              <span>100% Verified Service Professionals & Standard Upfront Pricing</span>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-[#C9A15A] uppercase tracking-wider">Quick Navigation</h4>
            <ul className="space-y-2 text-sm text-[#FAF7F0]/75">
              <li><Link to="/home" className="hover:text-white transition-colors">Home Marketplace</Link></li>
              <li><Link to="/catalog" className="hover:text-white transition-colors">Full Catalog</Link></li>
              <li><Link to="/bookings" className="hover:text-white transition-colors">My Bookings</Link></li>
              <li><Link to="/support" className="hover:text-white transition-colors">Support Center</Link></li>
              <li><Link to="/profile" className="hover:text-white transition-colors">Account Profile</Link></li>
            </ul>
          </div>

          {/* Popular Categories */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-[#C9A15A] uppercase tracking-wider">Top Categories</h4>
            <ul className="space-y-2 text-sm text-[#FAF7F0]/75">
              <li><Link to="/catalog?category=Cleaning" className="hover:text-white transition-colors">Deep Cleaning</Link></li>
              <li><Link to="/catalog?category=AC" className="hover:text-white transition-colors">AC & Appliance Repair</Link></li>
              <li><Link to="/catalog?category=Electrician" className="hover:text-white transition-colors">Electrician & Repairs</Link></li>
              <li><Link to="/catalog?category=Plumbing" className="hover:text-white transition-colors">Plumbing Solutions</Link></li>
              <li><Link to="/catalog?category=Beauty" className="hover:text-white transition-colors">Salon & Spa at Home</Link></li>
            </ul>
          </div>

          {/* Contact & Support */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-[#C9A15A] uppercase tracking-wider">Need Help?</h4>
            <ul className="space-y-2.5 text-xs text-[#FAF7F0]/75">
              <li className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-[#C9A15A] flex-shrink-0" />
                <span>+91 1800 200 4000 (Toll Free)</span>
              </li>
              <li className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-[#C9A15A] flex-shrink-0" />
                <span>support@smartserve.in</span>
              </li>
              <li className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-[#C9A15A] flex-shrink-0" />
                <span>SmartServe Tower, Noida Sector 62</span>
              </li>
            </ul>
          </div>

        </div>

        {/* Bottom copyright */}
        <div className="pt-8 border-t border-[#FAF7F0]/10 flex flex-col sm:flex-row items-center justify-between text-xs text-[#FAF7F0]/50 gap-4">
          <p>© {new Date().getFullYear()} SmartServe Marketplace Operations. All rights reserved.</p>
          <div className="flex items-center gap-6">
            <span className="hover:text-[#FAF7F0] cursor-pointer">Privacy Policy</span>
            <span className="hover:text-[#FAF7F0] cursor-pointer">Terms of Service</span>
            <span className="hover:text-[#FAF7F0] cursor-pointer">Refund Policy</span>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default CustomerFooter;
