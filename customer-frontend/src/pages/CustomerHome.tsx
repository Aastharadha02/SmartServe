import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../auth/useAuth';
import { getCatalogCategories, getCatalogServices, CategoryItem, ServiceItem } from '../api/catalog';
import { getCustomerBookings, BookingDetail } from '../api/bookings';
import { updateCustomerLocation, CustomerLocationPayload } from '../api/auth';
import { useToast } from '../hooks/useToast';
import { formatCurrencyINR } from '../utils/formatters';
import { getCategoryImageUrl, getServiceImage } from '../utils/serviceImages';
import { 
  Search, 
  ArrowRight, 
  Calendar, 
  Clock, 
  Star, 
  Loader2, 
  ChevronRight,
  MapPin,
  Navigation,
  X,
  Check,
  AlertCircle
} from 'lucide-react';

import { HomePromoCarousel } from '../components/home/HomePromoCarousel';

export const CustomerHome: React.FC = () => {
  const navigate = useNavigate();
  const { user, setUserLocation } = useAuth();
  const { showToast } = useToast();

  const [categories, setCategories] = useState<CategoryItem[]>([]);
  const [popularServices, setPopularServices] = useState<ServiceItem[]>([]);
  const [activeBookings, setActiveBookings] = useState<BookingDetail[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>('');

  const [guestLocation, setGuestLocation] = useState<CustomerLocationPayload | null>(() => {
    try {
      const saved = localStorage.getItem('smartserve_guest_location');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  // Location Management State
  const effectiveLocation = user?.location || guestLocation;
  const [showLocationModal, setShowLocationModal] = useState<boolean>(false);
  const [editAddress, setEditAddress] = useState<string>(effectiveLocation?.address || '');
  const [editCity, setEditCity] = useState<string>(effectiveLocation?.city || '');
  const [editPincode, setEditPincode] = useState<string>(effectiveLocation?.postal_code || '');
  const [editCoords, setEditCoords] = useState<{ latitude?: number; longitude?: number; source?: string }>({
    latitude: effectiveLocation?.latitude,
    longitude: effectiveLocation?.longitude,
    source: effectiveLocation?.source || 'manual',
  });
  const [locSaving, setLocSaving] = useState<boolean>(false);
  const [locGeoLoading, setLocGeoLoading] = useState<boolean>(false);
  const [locMessage, setLocMessage] = useState<{ text: string; type: 'success' | 'warning' } | null>(null);

  useEffect(() => {
    if (effectiveLocation) {
      if (effectiveLocation.address) setEditAddress(effectiveLocation.address);
      if (effectiveLocation.city) setEditCity(effectiveLocation.city);
      if (effectiveLocation.postal_code) setEditPincode(effectiveLocation.postal_code);
    }
  }, [effectiveLocation]);

  useEffect(() => {
    const fetchData = async () => {
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

  // Browser Geolocation handler inside dashboard
  const handleDetectCurrentLocation = () => {
    setLocMessage(null);
    if (!navigator.geolocation) {
      setLocMessage({
        text: 'Geolocation is not supported by your browser. Please enter your location manually.',
        type: 'warning'
      });
      return;
    }

    setLocGeoLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        setEditCoords({
          latitude: lat,
          longitude: lng,
          source: 'geolocation',
        });
        if (!editAddress) {
          setEditAddress(`Current Location (${lat.toFixed(4)}, ${lng.toFixed(4)})`);
        }
        setLocMessage({
          text: `Current GPS coordinates detected (${lat.toFixed(4)}, ${lng.toFixed(4)}).`,
          type: 'success'
        });
        setLocGeoLoading(false);
      },
      (error) => {
        let errText = 'Unable to detect location. Please enter your location manually.';
        if (error.code === error.PERMISSION_DENIED) {
          errText = 'Location permission was denied. You can enter your service location manually.';
        } else if (error.code === error.POSITION_UNAVAILABLE) {
          errText = 'Location information is currently unavailable.';
        } else if (error.code === error.TIMEOUT) {
          errText = 'Location detection timed out.';
        }
        setLocMessage({ text: errText, type: 'warning' });
        setLocGeoLoading(false);
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  };

  const handleSaveLocation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editAddress.trim() && !editCity.trim() && !editCoords.latitude) {
      setLocMessage({ text: 'Please enter a city or address to save your location.', type: 'warning' });
      return;
    }

    setLocSaving(true);
    const locPayload: CustomerLocationPayload = {
      address: editAddress.trim() || undefined,
      city: editCity.trim() || undefined,
      postal_code: editPincode.trim() || undefined,
      latitude: editCoords.latitude,
      longitude: editCoords.longitude,
      source: editCoords.source || 'manual',
    };

    try {
      if (user) {
        await updateCustomerLocation(locPayload);
      }
      setUserLocation(locPayload);
      localStorage.setItem('smartserve_guest_location', JSON.stringify(locPayload));
      setGuestLocation(locPayload);
      showToast(
        locPayload.city 
          ? `Service location set to ${locPayload.city}!` 
          : 'Service location updated successfully!', 
        'success'
      );
      setShowLocationModal(false);
    } catch {
      // Local fallback in case user is guest or offline
      setUserLocation(locPayload);
      localStorage.setItem('smartserve_guest_location', JSON.stringify(locPayload));
      setGuestLocation(locPayload);
      showToast('Service location updated locally.', 'success');
      setShowLocationModal(false);
    } finally {
      setLocSaving(false);
    }
  };

  const savedLocationDisplay = React.useMemo(() => {
    const loc = user?.location || guestLocation;
    if (!loc) return null;
    const { city, state, address } = loc;
    if (city && state) return `${city}, ${state}`;
    if (city) return city;
    if (address) return address;
    return null;
  }, [user, guestLocation]);

  return (
    <div className="space-y-8 font-sans max-w-7xl mx-auto">
      
      {/* ── 0. INCOMPLETE PROFILE REMINDER BANNER ── */}
      {user && user.is_profile_complete === false && (
        <div 
          data-testid="profile-incomplete-banner"
          className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-4 bg-amber-50/95 border border-amber-200 rounded-2xl text-amber-950 shadow-xs animate-in fade-in"
        >
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0 text-amber-800">
              <Clock className="w-4 h-4" />
            </div>
            <div>
              <p className="text-xs sm:text-sm font-bold text-amber-950">
                Your profile is not complete yet
              </p>
              <p className="text-[11px] sm:text-xs text-amber-800/90 font-medium">
                You can browse services, but required details (phone number) must be completed before placing an order.
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/complete-profile')}
            className="px-4 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs rounded-xl shadow-xs transition-all flex items-center gap-1.5 flex-shrink-0 cursor-pointer"
          >
            <span>Complete Profile</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* ── 0B. SERVICE LOCATION SECTION NEAR TOP OF DASHBOARD ── */}
      <div 
        data-testid="dashboard-location-bar"
        className="flex items-center justify-between p-3.5 sm:p-4 bg-white border border-[#E5DEC9] rounded-2xl shadow-xs"
      >
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-9 h-9 rounded-xl bg-[#2F5233]/10 text-[#2F5233] flex items-center justify-center flex-shrink-0">
            <MapPin className="w-5 h-5" />
          </div>
          <div className="min-w-0">
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#1F2A1E]/50 block">
              Service Location
            </span>
            {savedLocationDisplay ? (
              <p className="text-xs sm:text-sm font-bold text-[#1F2A1E] truncate">
                <span className="text-[#1F2A1E]/60 font-semibold mr-1">Your location:</span>
                <span className="text-[#2F5233]">{savedLocationDisplay}</span>
              </p>
            ) : (
              <p className="text-xs sm:text-sm font-semibold text-[#1F2A1E]/70 italic">
                Location not set · Choose your service location
              </p>
            )}
          </div>
        </div>
        <button
          onClick={() => {
            setEditAddress(user?.location?.address || '');
            setEditCity(user?.location?.city || '');
            setEditPincode(user?.location?.postal_code || '');
            setLocMessage(null);
            setShowLocationModal(true);
          }}
          data-testid="dashboard-location-action-btn"
          className="px-3.5 py-1.5 bg-[#FAF7F0] hover:bg-[#F2EDE1] text-[#2F5233] font-bold text-xs rounded-xl border border-[#E5DEC9] transition-all flex-shrink-0 cursor-pointer"
        >
          {savedLocationDisplay ? 'Change location' : 'Add Location'}
        </button>
      </div>

      {/* 1. AUTO-SCROLLING PROMOTIONAL CAROUSEL & SEARCH */}
      <div className="space-y-4">
        <HomePromoCarousel />

        <form onSubmit={handleSearchSubmit} className="flex items-center gap-2 p-2 bg-white rounded-2xl shadow-xs border border-[#E5DEC9] transition-all focus-within:border-[#2F5233]/60 focus-within:shadow-sm">
          <div className="flex-1 flex items-center gap-3 px-3">
            <Search className="w-5 h-5 text-[#1F2A1E]/40 flex-shrink-0" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search AC repair, salon, deep cleaning, electrician, plumbing, pest control..."
              className="w-full h-11 bg-transparent text-[#1F2A1E] placeholder-[#1F2A1E]/45 font-medium text-sm focus:outline-none"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-sm rounded-xl transition-all shadow-xs flex items-center gap-2 flex-shrink-0 cursor-pointer"
          >
            <span>Search</span>
            <ArrowRight className="w-4 h-4 text-[#C9A15A]" />
          </button>
        </form>
      </div>

      {/* ACTIVE BOOKINGS BANNER */}
      {activeBookings.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-serif text-2xl font-normal text-[#1F2A1E] tracking-tight flex items-center gap-2.5">
              <Calendar className="w-5 h-5 text-[#2F5233]" />
              <span>Your Active Bookings</span>
            </h3>
            <button onClick={() => navigate('/bookings')} className="text-xs font-bold text-[#2F5233] hover:text-[#3D6B42] hover:underline cursor-pointer">
              View All ({activeBookings.length})
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {activeBookings.map((b) => (
              <div 
                key={b.id}
                onClick={() => navigate(`/bookings/${b.id}`)}
                className="p-5 bg-white rounded-2xl border border-[#E5DEC9] hover:border-[#2F5233] shadow-xs hover:shadow-sm transition-all cursor-pointer flex items-center justify-between group"
              >
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded-full bg-[#FAF7F0] border border-[#E5DEC9] text-[#2F5233] text-[10px] font-bold tracking-wider uppercase">
                      {b.booking_reference}
                    </span>
                    <span className="text-xs font-semibold text-[#1F2A1E]/60">
                      {b.status}
                    </span>
                  </div>
                  <h4 className="font-bold text-[#1F2A1E] text-base group-hover:text-[#2F5233] transition-colors">
                    {b.service_name}
                  </h4>
                  <div className="flex items-center gap-4 text-xs text-[#1F2A1E]/60 font-medium">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5" />
                      {b.scheduled_date}
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      {b.scheduled_time}
                    </span>
                  </div>
                </div>
                <div className="w-8 h-8 rounded-full bg-[#FAF7F0] flex items-center justify-center text-[#1F2A1E]/40 group-hover:text-[#2F5233] group-hover:bg-[#2F5233]/10 transition-colors">
                  <ChevronRight className="w-4 h-4" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 2. CATEGORY TILES GRID */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-serif text-2xl font-normal text-[#1F2A1E] tracking-tight">Explore Top Categories</h3>
            <p className="text-xs text-[#1F2A1E]/60 font-medium mt-0.5">Verified home and lifestyle services at your doorstep</p>
          </div>
          <button onClick={() => navigate('/catalog')} className="text-xs font-bold text-[#2F5233] hover:text-[#3D6B42] hover:underline cursor-pointer">
            View All Services
          </button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
          {categories.map((cat) => {
            const imgUrl = cat.image || getCategoryImageUrl(cat.name);
            return (
              <div
                key={cat.id}
                onClick={() => navigate(`/catalog?category=${encodeURIComponent(cat.name)}`)}
                className="group p-3 bg-white rounded-2xl border border-[#E5DEC9] hover:border-[#2F5233] shadow-xs hover:shadow transition-all cursor-pointer flex flex-col items-center text-center space-y-2.5"
              >
                <div className="w-14 h-14 rounded-2xl overflow-hidden bg-[#FAF7F0] p-1 border border-[#E5DEC9]/60 group-hover:scale-105 transition-transform">
                  <img
                    src={imgUrl}
                    alt={cat.name}
                    className="w-full h-full object-cover rounded-xl"
                    loading="lazy"
                  />
                </div>
                <div className="space-y-0.5">
                  <span className="text-xs font-bold text-[#1F2A1E] group-hover:text-[#2F5233] transition-colors block line-clamp-1">
                    {cat.name}
                  </span>
                  <span className="text-[10px] text-[#1F2A1E]/50 font-medium block">
                    {cat.service_count ? `${cat.service_count} services` : 'Explore'}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 3. POPULAR FEATURED SERVICES */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-serif text-2xl font-normal text-[#1F2A1E] tracking-tight">Popular Home Services</h3>
            <p className="text-xs text-[#1F2A1E]/60 font-medium mt-0.5">Transparent upfront pricing with verified experts</p>
          </div>
          <button onClick={() => navigate('/catalog')} className="text-xs font-bold text-[#2F5233] hover:text-[#3D6B42] hover:underline cursor-pointer">
            Browse All ({popularServices.length})
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {popularServices.map((srv) => {
            const imgUrl = srv.image_url || getServiceImage(srv.name, srv.category);
            return (
              <div
                key={srv.id}
                onClick={() => navigate(`/service/${srv.id}`)}
                className="group bg-white rounded-3xl border border-[#E5DEC9] hover:border-[#2F5233] shadow-xs hover:shadow-md transition-all overflow-hidden flex flex-col justify-between cursor-pointer"
              >
                <div>
                  <div className="h-44 overflow-hidden relative bg-[#F2EDE1]">
                    <img
                      src={imgUrl}
                      alt={srv.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      loading="lazy"
                    />
                    <div className="absolute top-3 right-3 px-2.5 py-1 rounded-full bg-white/95 backdrop-blur-xs text-[#1F2A1E] text-xs font-bold shadow-xs flex items-center gap-1 border border-[#E5DEC9]">
                      <Star className="w-3.5 h-3.5 fill-[#C9A15A] text-[#C9A15A]" />
                      <span>{srv.rating || '4.8'}</span>
                    </div>
                  </div>

                  <div className="p-5 space-y-2">
                    <span className="text-[10px] font-bold text-[#2F5233] uppercase tracking-wider block">
                      {srv.category}
                    </span>
                    <h3 className="font-bold text-[#1F2A1E] text-base leading-snug group-hover:text-[#2F5233] transition-colors">
                      {srv.name}
                    </h3>
                    <p className="text-xs text-[#1F2A1E]/65 line-clamp-2 leading-relaxed font-normal">
                      {srv.description || 'Verified service delivered by trained professionals with standard service guarantee.'}
                    </p>
                  </div>
                </div>

                <div className="p-5 pt-0 flex items-center justify-between border-t border-[#E5DEC9]/50 mt-3">
                  <div>
                    <span className="text-[10px] text-[#1F2A1E]/50 font-semibold block uppercase">Fixed Rate</span>
                    <span className="font-serif text-lg font-normal text-[#1F2A1E]">{formatCurrencyINR(srv.base_price)}</span>
                  </div>
                  <button className="px-4 py-2 bg-[#FAF7F0] border border-[#E5DEC9] text-[#2F5233] font-bold text-xs rounded-xl hover:bg-[#2F5233] hover:text-white transition-colors cursor-pointer">
                    View Details
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* ── LOCATION SELECTION MODAL ── */}
      {showLocationModal && (
        <div className="fixed inset-0 z-50 bg-[#1F2A1E]/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="w-full max-w-md bg-white border border-[#E5DEC9] rounded-3xl p-6 sm:p-7 shadow-xl space-y-5 animate-in fade-in zoom-in-95">
            <div className="flex items-center justify-between border-b border-[#E5DEC9] pb-4">
              <div className="flex items-center gap-2">
                <MapPin className="w-5 h-5 text-[#2F5233]" />
                <h3 className="text-lg font-bold text-[#1F2A1E] tracking-tight">Choose Your Service Location</h3>
              </div>
              <button
                onClick={() => setShowLocationModal(false)}
                className="w-8 h-8 rounded-full hover:bg-[#FAF7F0] text-[#1F2A1E]/50 hover:text-[#1F2A1E] flex items-center justify-center transition-colors cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Geolocation Button */}
            <div>
              <button
                type="button"
                onClick={handleDetectCurrentLocation}
                disabled={locGeoLoading || locSaving}
                className="w-full h-11 flex items-center justify-center gap-2 bg-[#FAF7F0] hover:bg-[#F2EDE1] text-[#2F5233] font-bold text-xs rounded-xl border border-[#2F5233]/40 transition-all cursor-pointer disabled:opacity-60"
              >
                {locGeoLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-[#2F5233]" />
                    <span>Detecting current location...</span>
                  </>
                ) : (
                  <>
                    <Navigation className="w-4 h-4 text-[#2F5233]" />
                    <span>Use My Current Location</span>
                  </>
                )}
              </button>
            </div>

            {locMessage && (
              <div className={`p-2.5 rounded-xl text-xs font-medium border flex items-start gap-2 ${
                locMessage.type === 'success' 
                  ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
                  : 'bg-amber-50 border-amber-200 text-amber-800'
              }`}>
                {locMessage.type === 'success' ? (
                  <Check className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                ) : (
                  <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
                )}
                <span>{locMessage.text}</span>
              </div>
            )}

            {/* Manual Entry Form */}
            <form onSubmit={handleSaveLocation} className="space-y-4">
              <div>
                <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">
                  City / Region
                </label>
                <input
                  id="location-city-input"
                  type="text"
                  value={editCity}
                  onChange={(e) => setEditCity(e.target.value)}
                  placeholder="e.g. Ahmedabad, Gujarat or Noida"
                  className="w-full h-11 bg-white border border-[#E5DEC9] rounded-xl px-3.5 text-sm font-medium text-[#1F2A1E] focus:outline-none focus:border-[#2F5233]"
                  disabled={locSaving}
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">
                  Street Address / Society
                </label>
                <input
                  id="location-address-input"
                  type="text"
                  value={editAddress}
                  onChange={(e) => setEditAddress(e.target.value)}
                  placeholder="e.g., Flat 402, Sunshine Apartments"
                  className="w-full h-11 bg-white border border-[#E5DEC9] rounded-xl px-3.5 text-sm font-medium text-[#1F2A1E] focus:outline-none focus:border-[#2F5233]"
                  disabled={locSaving}
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">
                  Pincode
                </label>
                <input
                  type="text"
                  value={editPincode}
                  onChange={(e) => setEditPincode(e.target.value)}
                  placeholder="e.g., 380054"
                  className="w-full h-11 bg-white border border-[#E5DEC9] rounded-xl px-3.5 text-sm font-medium text-[#1F2A1E] focus:outline-none focus:border-[#2F5233]"
                  disabled={locSaving}
                />
              </div>

              <div className="pt-2 flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowLocationModal(false)}
                  className="px-4 py-2.5 text-xs font-bold text-[#1F2A1E]/60 hover:text-[#1F2A1E] rounded-xl transition-colors cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={locSaving}
                  className="px-6 py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs rounded-xl shadow-xs transition-all flex items-center gap-2 cursor-pointer disabled:opacity-60"
                >
                  {locSaving ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Check className="w-3.5 h-3.5" />}
                  <span>Save Location</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};

export default CustomerHome;
