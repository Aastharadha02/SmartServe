import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../auth/useAuth';
import { getCatalogCategories, getCatalogServices, CategoryItem, ServiceItem } from '../api/catalog';
import { getCustomerBookings, BookingDetail } from '../api/bookings';
import { formatCurrencyINR } from '../utils/formatters';
import { getCategoryImageUrl, getServiceImage } from '../utils/serviceImages';
import { 
  Search, 
  Sparkles, 
  ArrowRight, 
  Calendar, 
  Clock, 
  Star, 
  Loader2, 
  Tag,
  ChevronRight
} from 'lucide-react';

export const CustomerHome: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [categories, setCategories] = useState<CategoryItem[]>([]);
  const [popularServices, setPopularServices] = useState<ServiceItem[]>([]);
  const [activeBookings, setActiveBookings] = useState<BookingDetail[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState<string>('');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [catData, srvData] = await Promise.all([
          getCatalogCategories().catch(() => []),
          getCatalogServices().catch(() => [])
        ]);

        setCategories(catData.slice(0, 8));
        setPopularServices(srvData.slice(0, 6));

        if (user) {
          const bookingsData = await getCustomerBookings().catch(() => []);
          setActiveBookings(bookingsData.filter((b) => b.status.toLowerCase() !== 'completed' && b.status.toLowerCase() !== 'cancelled').slice(0, 2));
        }
      } catch (err) {
        console.error('Failed to load home marketplace data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/catalog?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const userName = user?.full_name ? user.full_name.split(' ')[0] : 'Guest';

  return (
    <div className="space-y-10 font-sans">
      
      {/* HERO BANNER & SEARCH */}
      <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-[#0A1128] via-[#0F1D40] to-[#1E293B] text-white p-8 sm:p-12 shadow-xl">
        <div className="relative z-10 max-w-2xl space-y-6">
          <span className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-400/30 text-xs font-bold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5" />
            Verified Home & Urban Services
          </span>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-[1.15]">
            Welcome back, {userName}! <br />
            <span className="text-blue-400">What service do you need today?</span>
          </h1>

          <p className="text-sm sm:text-base text-slate-300 font-normal leading-relaxed">
            Book verified expert technicians, deep cleaning teams, electricians, and beauty professionals with fixed upfront pricing.
          </p>

          <form onSubmit={handleSearchSubmit} className="flex items-center gap-2 p-2 bg-white rounded-2xl shadow-lg">
            <div className="flex-1 flex items-center gap-3 px-3">
              <Search className="w-5 h-5 text-slate-400 flex-shrink-0" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search AC repair, sofa cleaning, plumbing..."
                className="w-full h-12 bg-transparent text-slate-900 placeholder-slate-400 font-medium text-sm focus:outline-none"
              />
            </div>
            <button
              type="submit"
              className="px-6 py-3 bg-[#2563EB] hover:bg-blue-700 text-white font-bold text-sm rounded-xl transition-all shadow-xs flex items-center gap-2 flex-shrink-0"
            >
              <span>Search</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>
        </div>

        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl pointer-events-none"></div>
      </div>

      {/* ACTIVE BOOKINGS BANNER */}
      {activeBookings.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
              <Calendar className="w-5 h-5 text-[#2563EB]" />
              <span>Your Active Bookings</span>
            </h3>
            <button onClick={() => navigate('/bookings')} className="text-xs font-bold text-[#2563EB] hover:underline">
              View All ({activeBookings.length})
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {activeBookings.map((b) => (
              <div
                key={b.id}
                onClick={() => navigate(`/bookings/${b.id}`)}
                className="bg-white p-5 rounded-2xl border border-blue-200/80 shadow-xs hover:shadow-md transition-all cursor-pointer flex items-center justify-between gap-4"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded-full bg-blue-50 text-[#2563EB] text-[10px] font-bold uppercase border border-blue-100">
                      {b.status}
                    </span>
                    <span className="text-xs font-mono font-bold text-slate-500">{b.booking_reference}</span>
                  </div>
                  <h4 className="font-extrabold text-slate-900 text-base">{b.service_name}</h4>
                  <p className="text-xs text-slate-500 flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-slate-400" />
                    <span>{b.scheduled_date} at {b.scheduled_time}</span>
                  </p>
                </div>

                <div className="text-right flex-shrink-0">
                  <span className="text-lg font-extrabold text-slate-900 block font-mono">₹{b.total_price || b.total_amount}</span>
                  <ChevronRight className="w-5 h-5 text-slate-400 ml-auto mt-1" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* CATEGORY HIGHLIGHT GRID */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-extrabold text-slate-900 tracking-tight">Explore Categories</h2>
            <p className="text-xs text-slate-500 font-medium">Browse verified services managed in the SmartServe catalog.</p>
          </div>
          <button
            onClick={() => navigate('/catalog')}
            className="text-xs font-bold text-[#2563EB] hover:underline flex items-center gap-1"
          >
            <span>See Full Catalog</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        {loading ? (
          <div className="flex justify-center py-10">
            <Loader2 className="w-8 h-8 animate-spin text-[#2563EB]" />
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {categories.map((cat) => {
              const imgUrl = (cat.image && !cat.image.includes('photo-1621905251189-08b45d6a269e'))
                ? cat.image
                : getCategoryImageUrl(cat.name);
              return (
                <div
                  key={cat.id}
                  onClick={() => navigate(`/catalog?category=${encodeURIComponent(cat.name)}`)}
                  className="group relative rounded-2xl overflow-hidden border border-slate-200 shadow-2xs hover:shadow-md hover:border-blue-300 transition-all cursor-pointer h-36 flex flex-col justify-end p-4"
                >
                  <img
                    src={imgUrl}
                    alt={cat.name}
                    className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-950/85 via-slate-950/30 to-transparent"></div>
                  <div className="relative z-10 space-y-0.5">
                    <h3 className="font-extrabold text-white text-sm leading-snug drop-shadow-xs">
                      {cat.name}
                    </h3>
                    <span className="text-[10px] text-blue-200 font-semibold block">
                      {cat.service_count ? `${cat.service_count} Services` : 'Verified Professionals'}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* PROMOTIONAL DISCOUNT BANNER */}
      <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-blue-900 via-indigo-950 to-slate-950 text-white p-8 shadow-md">
        <div className="relative z-10 max-w-lg space-y-3">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 border border-blue-400/30 text-xs font-bold uppercase tracking-wider">
            <Tag className="w-3.5 h-3.5" />
            Limited Time Offer
          </span>
          <h3 className="text-2xl sm:text-3xl font-extrabold tracking-tight leading-tight">
            Up to 20% OFF Deep Home Cleaning & AC Servicing
          </h3>
          <p className="text-xs sm:text-sm text-slate-300 font-medium leading-relaxed">
            Sanitization, foam-jet AC cleaning, and kitchen scrubbing packages with guaranteed 30-day warranty.
          </p>
          <div className="pt-2">
            <button
              onClick={() => navigate('/catalog')}
              className="px-6 py-3 rounded-xl bg-[#2563EB] hover:bg-blue-600 text-white font-bold text-xs sm:text-sm shadow-sm transition-all inline-flex items-center gap-2"
            >
              <span>Explore Deals</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* POPULAR SERVICES GRID */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-extrabold text-slate-900 tracking-tight">Popular Home Services</h2>
            <p className="text-xs text-slate-500 font-medium">Top rated services booked across Noida & NCR</p>
          </div>
          <button
            onClick={() => navigate('/catalog')}
            className="text-xs font-bold text-[#2563EB] hover:underline"
          >
            View All Services
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {popularServices.map((srv) => {
            const imgUrl = (srv.image_url && !srv.image_url.includes('photo-1621905251189-08b45d6a269e'))
              ? srv.image_url
              : getServiceImage(srv.category, srv.subcategory, srv.name);
            return (
              <div
                key={srv.id}
                onClick={() => navigate(`/service/${srv.id}`)}
                className="group bg-white rounded-2xl border border-slate-200/90 shadow-2xs hover:shadow-md hover:border-blue-200 transition-all cursor-pointer overflow-hidden flex flex-col justify-between"
              >
                <div>
                  <div className="h-44 overflow-hidden relative bg-slate-100">
                    <img
                      src={imgUrl}
                      alt={srv.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    />
                    <div className="absolute top-3 right-3 px-2.5 py-1 rounded-full bg-white/90 backdrop-blur-xs text-slate-900 text-xs font-bold shadow-xs flex items-center gap-1">
                      <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                      <span>{srv.rating || '4.8'}</span>
                    </div>
                  </div>

                  <div className="p-5 space-y-2">
                    <span className="text-[11px] font-bold text-[#2563EB] uppercase tracking-wider block">
                      {srv.category}
                    </span>
                    <h3 className="font-extrabold text-slate-900 text-base leading-snug group-hover:text-[#2563EB] transition-colors">
                      {srv.name}
                    </h3>
                    <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed">
                      {srv.description || 'Professional service delivered by verified experts with 30-day warranty.'}
                    </p>
                  </div>
                </div>

                <div className="p-5 pt-0 flex items-center justify-between border-t border-slate-100 mt-3">
                  <div>
                    <span className="text-[10px] text-slate-400 font-semibold block">Fixed Price</span>
                    <span className="text-lg font-extrabold text-slate-900 font-mono">{formatCurrencyINR(srv.base_price)}</span>
                  </div>
                  <button className="px-4 py-2 bg-blue-50 text-[#2563EB] font-bold text-xs rounded-xl hover:bg-[#2563EB] hover:text-white transition-colors">
                    View Details
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
};

export default CustomerHome;
