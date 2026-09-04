import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Phone, Mail, MapPin } from 'lucide-react';

export const CustomerFooter: React.FC = () => {
  return (
    <footer className="bg-[#0A1128] text-white pt-14 pb-8 font-sans border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Top Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          
          {/* Brand Info (2 cols) */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-[#2563EB] flex items-center justify-center text-white font-black text-xl shadow-sm">
                S
              </div>
              <h3 className="font-extrabold text-xl tracking-tight text-white">SmartServe</h3>
            </div>
            <p className="text-slate-400 text-sm font-normal leading-relaxed max-w-sm">
              India's premier verified home services platform. Professional deep cleaning, AC maintenance, plumbing, electrical, and urban lifestyle services delivered to your doorstep.
            </p>
            <div className="pt-2 flex items-center gap-3 text-xs text-emerald-400 font-semibold">
              <ShieldCheck className="w-4 h-4" />
              <span>100% Verified Local Service Professionals</span>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-blue-400 uppercase tracking-wider">Quick Navigation</h4>
            <ul className="space-y-2 text-sm text-slate-300">
              <li><Link to="/home" className="hover:text-white transition-colors">Home Marketplace</Link></li>
              <li><Link to="/catalog" className="hover:text-white transition-colors">Full Catalog</Link></li>
              <li><Link to="/bookings" className="hover:text-white transition-colors">My Bookings</Link></li>
              <li><Link to="/support" className="hover:text-white transition-colors">Support Center</Link></li>
              <li><Link to="/profile" className="hover:text-white transition-colors">Account Profile</Link></li>
            </ul>
          </div>

          {/* Popular Categories */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-blue-400 uppercase tracking-wider">Top Categories</h4>
            <ul className="space-y-2 text-sm text-slate-300">
              <li><Link to="/catalog?category=Cleaning" className="hover:text-white transition-colors">Deep Cleaning</Link></li>
              <li><Link to="/catalog?category=AC" className="hover:text-white transition-colors">AC & Appliance Repair</Link></li>
              <li><Link to="/catalog?category=Electrician" className="hover:text-white transition-colors">Electrician Services</Link></li>
              <li><Link to="/catalog?category=Plumbing" className="hover:text-white transition-colors">Plumbing & Leakages</Link></li>
              <li><Link to="/catalog?category=Beauty" className="hover:text-white transition-colors">Salon & Spa at Home</Link></li>
            </ul>
          </div>

          {/* Contact & Support */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-blue-400 uppercase tracking-wider">Need Help?</h4>
            <ul className="space-y-2.5 text-xs text-slate-300">
              <li className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-blue-400 flex-shrink-0" />
                <span>+91 1800 200 4000 (Toll Free)</span>
              </li>
              <li className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-blue-400 flex-shrink-0" />
                <span>support@smartserve.in</span>
              </li>
              <li className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-blue-400 flex-shrink-0" />
                <span>SmartServe Tower, Noida Sector 62</span>
              </li>
            </ul>
          </div>

        </div>

        {/* Bottom copyright */}
        <div className="pt-8 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© {new Date().getFullYear()} SmartServe Marketplace Operations. All rights reserved.</p>
          <div className="flex items-center gap-6">
            <span className="hover:text-slate-400 cursor-pointer">Privacy Policy</span>
            <span className="hover:text-slate-400 cursor-pointer">Terms of Service</span>
            <span className="hover:text-slate-400 cursor-pointer">Refund Policy</span>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default CustomerFooter;
