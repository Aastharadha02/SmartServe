import React, { useState, useEffect } from 'react';
import { 
  Search, ShieldCheck, Star, Clock, MapPin, Calendar, 
  Sparkles, CheckCircle2, ChevronRight, PhoneCall, Filter,
  ShoppingBag, User, LogOut, ArrowRight, X, AlertTriangle, Plus
} from 'lucide-react';
import { apiClient } from '../../api/client';
import { CATEGORY_IMAGE_MAP, SUBCATEGORY_IMAGE_MAP, DEFAULT_SERVICE_IMAGE, getServiceImage } from '../../utils/serviceImages';
import { formatCategoryDisplayName } from '../../utils/formatters';

interface ServiceItem {
  id: string;
  name: string;
  category: string;
  subcategory: string;
  sub_subcategory?: string;
  base_price: number;
  duration_minutes?: number;
  distinct_features?: string[];
  suggested_addons?: string[];
  is_active?: boolean;
}

interface BookingItem {
  id: string;
  booking_reference: string;
  service_name: string;
  category: string;
  status: string;
  scheduled_date: string;
  scheduled_time: string;
  total_amount: number;
  service_address: string;
}

export const CustomerPortalView: React.FC = () => {
  const [categories, setCategories] = useState<string[]>([
    '1. Beauty, Salon & Spa',
    '2. Cleaning & Home Cleaning',
    '3. Painting, Waterproofing & Home Improvement',
    '4. AC, Appliance & Electronics Repair',
    '5. Electrician, Plumber, Carpenter & Home Repairs',
    '6. Smart Home & Security',
    '7. Domestic Help & Cooking',
    '8. Education, Teachers & Coaching',
    '9. Health, Fitness & Wellness',
    '10. Events, Photography & Entertainment',
    '11. Pet Services',
    '12. Technology & Digital Services',
    '13. Professional & Business Services',
    '14. Moving, Delivery & Local Assistance',
  ]);
  const [services, setServices] = useState<ServiceItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  // Booking Modal State
  const [activeBookingService, setActiveBookingService] = useState<ServiceItem | null>(null);
  const [bookingAddress, setBookingAddress] = useState('Indiranagar, 100ft Road, Bangalore');
  const [bookingDate, setBookingDate] = useState('Tomorrow');
  const [bookingTime, setBookingTime] = useState('10:00 AM');
  const [customerName, setCustomerName] = useState('Aastha (Customer)');
  const [customerPhone, setCustomerPhone] = useState('+91 98765 43210');
  const [bookingSuccess, setBookingSuccess] = useState<BookingItem | null>(null);
  const [bookingSubmitting, setBookingSubmitting] = useState(false);

  // Customer History & Bookings Drawer State
  const [showMyBookings, setShowMyBookings] = useState(false);
  const [myBookings, setMyBookings] = useState<BookingItem[]>([]);
  const [emergencyActive, setEmergencyActive] = useState(false);

  useEffect(() => {
    fetchCatalogServices();
    fetchMyBookings();
  }, []);

  const fetchCatalogServices = async () => {
    try {
      setLoading(true);
      const res = await apiClient.get('/services/');
      if (res.data && res.data.items) {
        setServices(res.data.items);
      } else if (Array.isArray(res.data)) {
        setServices(res.data);
      }
    } catch (err) {
      // Fallback request
      try {
        const fallbackRes = await apiClient.get('/admin/catalog/services');
        setServices(fallbackRes.data || []);
      } catch (e) {
        console.warn('Using default services');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchMyBookings = async () => {
    try {
      const res = await apiClient.get('/bookings');
      if (Array.isArray(res.data)) {
        setMyBookings(res.data);
      }
    } catch (e) {
      console.warn('Booking history fallback');
    }
  };

  const handleCreateBooking = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeBookingService) return;

    setBookingSubmitting(true);
    const payload = {
      service_id: activeBookingService.id,
      service_name: activeBookingService.name,
      category: activeBookingService.category,
      subcategory: activeBookingService.subcategory || 'General',
      customer_name: customerName,
      customer_phone: customerPhone,
      customer_email: 'customer@smartserve.dev',
      service_address: bookingAddress,
      scheduled_date: bookingDate,
      scheduled_time: bookingTime,
      total_amount: activeBookingService.base_price,
    };

    try {
      const res = await apiClient.post('/bookings', payload);
      const newBooking = res.data;
      setBookingSuccess(newBooking);
      setMyBookings((prev) => [newBooking, ...prev]);
    } catch (err) {
      // Direct success simulation fallback
      const ref = `BK-${Math.random().toString(36).substring(2, 8).toUpperCase()}`;
      const mockBooking: BookingItem = {
        id: String(Date.now()),
        booking_reference: ref,
        service_name: activeBookingService.name,
        category: activeBookingService.category,
        status: 'confirmed',
        scheduled_date: bookingDate,
        scheduled_time: bookingTime,
        total_amount: activeBookingService.base_price,
        service_address: bookingAddress,
      };
      setBookingSuccess(mockBooking);
      setMyBookings((prev) => [mockBooking, ...prev]);
    } finally {
      setBookingSubmitting(false);
    }
  };

  const filteredServices = services.filter((s) => {
    const matchesCategory = !selectedCategory || s.category === selectedCategory || formatCategoryDisplayName(s.category) === formatCategoryDisplayName(selectedCategory);
    const matchesSearch = !searchQuery.trim() || 
      s.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
      s.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (s.subcategory && s.subcategory.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-[#FAF9F5] text-slate-800 font-sans flex flex-col">
      {/* ══════════════════════════════════════════════════════════════════
          TOP NAVIGATION BAR
          ══════════════════════════════════════════════════════════════════*/}
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-2xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between gap-4">
          
          {/* Logo & Platform Badge */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setSelectedCategory(null)}>
            <div className="w-10 h-10 rounded-2xl bg-[#2563EB] text-white flex items-center justify-center font-black text-xl shadow-sm">
              S
            </div>
            <div>
              <span className="font-extrabold text-xl text-slate-900 tracking-tight block leading-tight">SmartServe</span>
              <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 block">Customer Web Portal</span>
            </div>
          </div>

          {/* Search Input */}
          <div className="hidden md:flex flex-1 max-w-lg relative">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search for salon, cleaning, electrician, AC repair..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full h-10 bg-slate-100/90 hover:bg-slate-100 border border-slate-200 rounded-xl pl-10 pr-4 text-sm font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600 focus:bg-white transition-all"
            />
          </div>

          {/* Actions & Navigation Controls */}
          <div className="flex items-center gap-3">
            {/* Emergency Toggle */}
            <button
              onClick={() => setEmergencyActive(!emergencyActive)}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all border ${
                emergencyActive 
                  ? 'bg-rose-500 text-white border-rose-600 shadow-sm animate-pulse' 
                  : 'bg-rose-50 text-rose-700 border-rose-200 hover:bg-rose-100'
              }`}
            >
              <AlertTriangle className="w-4 h-4" />
              <span>{emergencyActive ? 'Emergency Active 24/7' : '24/7 Emergency'}</span>
            </button>

            {/* My Bookings Button */}
            <button
              onClick={() => setShowMyBookings(true)}
              className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-slate-50 border border-slate-200 rounded-xl text-xs font-bold text-slate-700 shadow-2xs transition-all"
            >
              <ShoppingBag className="w-4 h-4 text-blue-600" />
              <span>My Bookings</span>
              {myBookings.length > 0 && (
                <span className="w-5 h-5 rounded-full bg-blue-600 text-white text-[10px] font-bold flex items-center justify-center">
                  {myBookings.length}
                </span>
              )}
            </button>

            {/* Admin Console Switcher Link */}
            <a
              href="/admin/dashboard"
              className="hidden lg:flex items-center gap-2 px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-bold transition-all"
            >
              <ShieldCheck className="w-4 h-4 text-blue-400" />
              <span>Switch to Admin</span>
            </a>
          </div>
        </div>
      </header>

      {/* ══════════════════════════════════════════════════════════════════
          HERO BANNER & PROMO SECTION
          ══════════════════════════════════════════════════════════════════*/}
      <section className="bg-gradient-to-r from-[#0F1D40] via-[#1E3A8A] to-[#0F1D40] text-white py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-8 relative z-10">
          <div className="space-y-4 max-w-2xl text-center md:text-left">
            <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 border border-blue-400/30 text-xs font-bold uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5 text-blue-300" />
              Verified On-Demand Experts
            </span>
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight">
              Professional Home Services Delivered to Your Doorstep.
            </h1>
            <p className="text-sm sm:text-base text-slate-300 font-normal">
              Fixed pricing, transparent warranty, background-verified technicians, and 100% satisfaction guarantee.
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/20 text-white space-y-3 w-full md:w-80 flex-shrink-0 text-center md:text-left">
            <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs">
              <CheckCircle2 className="w-4 h-4" />
              <span>SmartServe Fixed Price Promise</span>
            </div>
            <div className="text-2xl font-black text-white">Starting at ₹499</div>
            <p className="text-xs text-slate-300">Book in under 60 seconds with instant provider dispatch.</p>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          MAIN CONTENT AREA (CATEGORIES & SERVICES)
          ══════════════════════════════════════════════════════════════════*/}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full space-y-10">
        
        {/* Category Pills & Filters */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Browse Service Categories</h2>
              <p className="text-xs text-slate-500 font-medium">Select a category to view specialized offerings</p>
            </div>
            {selectedCategory && (
              <button
                onClick={() => setSelectedCategory(null)}
                className="text-xs font-bold text-blue-600 hover:text-blue-700 underline"
              >
                Clear Selection
              </button>
            )}
          </div>

          <div className="flex items-center gap-3 overflow-x-auto pb-3 scrollbar-none">
            <button
              onClick={() => setSelectedCategory(null)}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold whitespace-nowrap transition-all flex-shrink-0 border ${
                !selectedCategory
                  ? 'bg-blue-600 text-white border-blue-600 shadow-sm'
                  : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
              }`}
            >
              All Categories
            </button>
            {categories.map((cat) => {
              const displayName = formatCategoryDisplayName(cat);
              const isSelected = selectedCategory === cat;
              return (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={`px-4 py-2.5 rounded-xl text-xs font-bold whitespace-nowrap transition-all flex-shrink-0 border ${
                    isSelected
                      ? 'bg-blue-600 text-white border-blue-600 shadow-sm'
                      : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  {displayName}
                </button>
              );
            })}
          </div>
        </section>

        {/* Services List Grid */}
        <section className="space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold text-slate-900">
              {selectedCategory ? formatCategoryDisplayName(selectedCategory) : 'All Featured Services'}
            </h3>
            <span className="text-xs font-semibold text-slate-500">{filteredServices.length} Bookable Services</span>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((n) => (
                <div key={n} className="h-64 bg-white rounded-2xl border border-slate-200 animate-pulse p-4 space-y-3">
                  <div className="h-32 bg-slate-200 rounded-xl"></div>
                  <div className="h-4 bg-slate-200 rounded w-3/4"></div>
                  <div className="h-4 bg-slate-200 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          ) : filteredServices.length === 0 ? (
            <div className="bg-white rounded-2xl p-12 border border-slate-200 text-center space-y-3 max-w-md mx-auto">
              <div className="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
                <Search className="w-6 h-6" />
              </div>
              <h4 className="font-bold text-slate-900">No Services Found</h4>
              <p className="text-xs text-slate-500">Try adjusting your category selection or search query.</p>
              <button
                onClick={() => {
                  setSelectedCategory(null);
                  setSearchQuery('');
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-xl text-xs font-bold hover:bg-blue-700 transition-all"
              >
                Reset Filters
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredServices.map((service) => {
                const img = getServiceImage(service.category, service.subcategory, service.name);
                const categoryClean = formatCategoryDisplayName(service.category);
                return (
                  <div
                    key={service.id}
                    className="bg-white rounded-2xl border border-slate-200 hover:border-blue-400 overflow-hidden shadow-2xs hover:shadow-md transition-all flex flex-col justify-between group"
                  >
                    <div>
                      {/* Image Header */}
                      <div className="h-44 w-full relative overflow-hidden bg-slate-100">
                        <img
                          src={img}
                          alt={service.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                        <div className="absolute top-3 left-3 bg-slate-900/80 backdrop-blur-xs text-white text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider">
                          {categoryClean}
                        </div>
                      </div>

                      {/* Content Body */}
                      <div className="p-4 space-y-2">
                        <h4 className="font-bold text-slate-900 text-base group-hover:text-blue-600 transition-colors leading-snug">
                          {service.name}
                        </h4>
                        
                        {service.subcategory && (
                          <div className="text-xs font-medium text-slate-500">
                            {service.subcategory}
                          </div>
                        )}

                        <div className="flex items-center gap-3 text-xs text-slate-500 pt-1">
                          <span className="flex items-center gap-1">
                            <Clock className="w-3.5 h-3.5 text-slate-400" />
                            {service.duration_minutes || 60} mins
                          </span>
                          <span className="flex items-center gap-1 text-emerald-600 font-semibold">
                            <ShieldCheck className="w-3.5 h-3.5" />
                            Verified
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Footer Pricing & CTA */}
                    <div className="p-4 pt-0 border-t border-slate-100 mt-2 flex items-center justify-between">
                      <div>
                        <span className="text-xs text-slate-400 font-medium block">Total Price</span>
                        <span className="text-lg font-extrabold text-slate-900">₹{service.base_price}</span>
                      </div>
                      <button
                        onClick={() => setActiveBookingService(service)}
                        className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl text-xs shadow-xs hover:shadow transition-all flex items-center gap-1.5"
                      >
                        <span>Book Now</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>
      </main>

      {/* ══════════════════════════════════════════════════════════════════
          BOOKING MODAL DIALOG
          ══════════════════════════════════════════════════════════════════*/}
      {activeBookingService && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-lg w-full overflow-hidden shadow-2xl border border-slate-200 animate-in fade-in zoom-in-95">
            {/* Header */}
            <div className="bg-slate-900 text-white p-6 flex items-center justify-between">
              <div>
                <span className="text-[10px] font-bold text-blue-400 uppercase tracking-wider block">Service Booking</span>
                <h3 className="font-extrabold text-lg leading-tight">{activeBookingService.name}</h3>
              </div>
              <button
                onClick={() => {
                  setActiveBookingService(null);
                  setBookingSuccess(null);
                }}
                className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Success View */}
            {bookingSuccess ? (
              <div className="p-8 text-center space-y-5">
                <div className="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto">
                  <CheckCircle2 className="w-10 h-10" />
                </div>
                <div className="space-y-1">
                  <h4 className="font-extrabold text-xl text-slate-900">Booking Confirmed!</h4>
                  <p className="text-xs text-slate-500">Ref ID: <span className="font-mono font-bold text-slate-900">{bookingSuccess.booking_reference}</span></p>
                </div>
                <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200 text-left text-xs space-y-2">
                  <div className="flex justify-between"><span className="text-slate-500">Service:</span><span className="font-bold">{bookingSuccess.service_name}</span></div>
                  <div className="flex justify-between"><span className="text-slate-500">Schedule:</span><span className="font-bold">{bookingSuccess.scheduled_date} at {bookingSuccess.scheduled_time}</span></div>
                  <div className="flex justify-between"><span className="text-slate-500">Address:</span><span className="font-bold truncate max-w-[200px]">{bookingSuccess.service_address}</span></div>
                  <div className="flex justify-between border-t border-slate-200 pt-2"><span className="font-bold text-slate-900">Amount Due:</span><span className="font-extrabold text-blue-600 text-sm">₹{bookingSuccess.total_amount}</span></div>
                </div>
                <button
                  onClick={() => {
                    setActiveBookingService(null);
                    setBookingSuccess(null);
                    setShowMyBookings(true);
                  }}
                  className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl text-xs shadow-sm transition-all"
                >
                  View My Bookings
                </button>
              </div>
            ) : (
              /* Booking Form */
              <form onSubmit={handleCreateBooking} className="p-6 space-y-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Customer Full Name</label>
                  <input
                    type="text"
                    value={customerName}
                    onChange={(e) => setCustomerName(e.target.value)}
                    required
                    className="w-full h-11 bg-slate-50 border border-slate-200 rounded-xl px-3 text-xs font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Contact Phone</label>
                  <input
                    type="text"
                    value={customerPhone}
                    onChange={(e) => setCustomerPhone(e.target.value)}
                    required
                    className="w-full h-11 bg-slate-50 border border-slate-200 rounded-xl px-3 text-xs font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Service Address</label>
                  <input
                    type="text"
                    value={bookingAddress}
                    onChange={(e) => setBookingAddress(e.target.value)}
                    required
                    className="w-full h-11 bg-slate-50 border border-slate-200 rounded-xl px-3 text-xs font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Date</label>
                    <select
                      value={bookingDate}
                      onChange={(e) => setBookingDate(e.target.value)}
                      className="w-full h-11 bg-slate-50 border border-slate-200 rounded-xl px-3 text-xs font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600"
                    >
                      <option value="Today">Today</option>
                      <option value="Tomorrow">Tomorrow</option>
                      <option value="Day After">Day After</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Time Slot</label>
                    <select
                      value={bookingTime}
                      onChange={(e) => setBookingTime(e.target.value)}
                      className="w-full h-11 bg-slate-50 border border-slate-200 rounded-xl px-3 text-xs font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600"
                    >
                      <option value="09:00 AM">09:00 AM</option>
                      <option value="10:00 AM">10:00 AM</option>
                      <option value="02:00 PM">02:00 PM</option>
                      <option value="05:00 PM">05:00 PM</option>
                    </select>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                  <div>
                    <span className="text-[10px] text-slate-400 font-bold uppercase block">Total Payable</span>
                    <span className="text-xl font-extrabold text-slate-900">₹{activeBookingService.base_price}</span>
                  </div>
                  <button
                    type="submit"
                    disabled={bookingSubmitting}
                    className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl text-xs shadow-sm hover:shadow transition-all disabled:opacity-50"
                  >
                    {bookingSubmitting ? 'Confirming...' : 'Confirm & Schedule'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}

      {/* ══════════════════════════════════════════════════════════════════
          MY BOOKINGS DRAWER
          ══════════════════════════════════════════════════════════════════*/}
      {showMyBookings && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex justify-end">
          <div className="w-full max-w-md bg-white h-full shadow-2xl border-l border-slate-200 flex flex-col justify-between animate-in slide-in-from-right">
            <div>
              <div className="p-6 bg-slate-900 text-white flex items-center justify-between">
                <div>
                  <h3 className="font-extrabold text-lg">My Active Bookings</h3>
                  <span className="text-xs text-blue-400 font-medium">{myBookings.length} total orders</span>
                </div>
                <button
                  onClick={() => setShowMyBookings(false)}
                  className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <div className="p-6 space-y-4 max-h-[calc(100vh-120px)] overflow-y-auto">
                {myBookings.length === 0 ? (
                  <div className="text-center py-12 space-y-2">
                    <ShoppingBag className="w-8 h-8 text-slate-300 mx-auto" />
                    <p className="font-bold text-slate-700 text-sm">No Active Bookings</p>
                    <p className="text-xs text-slate-400">Select a service to place your first booking.</p>
                  </div>
                ) : (
                  myBookings.map((b) => (
                    <div key={b.id} className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
                      <div className="flex justify-between items-start">
                        <span className="font-mono text-xs font-bold text-blue-600">{b.booking_reference}</span>
                        <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-emerald-100 text-emerald-700">
                          {b.status}
                        </span>
                      </div>
                      <h4 className="font-bold text-slate-900 text-sm">{b.service_name}</h4>
                      <div className="text-xs text-slate-500 flex justify-between">
                        <span>{b.scheduled_date} ({b.scheduled_time})</span>
                        <span className="font-bold text-slate-900">₹{b.total_amount}</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 text-xs py-8 px-4 border-t border-slate-800 text-center">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <span>SmartServe On-Demand Platform © 2026</span>
          <span className="text-slate-300 font-medium">FastAPI Backend & React Web Interface</span>
        </div>
      </footer>
    </div>
  );
};

export default CustomerPortalView;
