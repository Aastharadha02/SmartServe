import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  User, 
  Phone, 
  MapPin, 
  Navigation, 
  CheckCircle2, 
  ArrowRight, 
  Loader2, 
  AlertCircle, 
  Sparkles, 
  Check, 
  Clock,
  ShieldAlert
} from 'lucide-react';
import { completeCustomerProfile, skipCustomerProfile, CustomerLocationPayload } from '../../api/auth';
import { getCatalogCategories, CategoryItem } from '../../api/catalog';
import { useAuth } from '../../auth/useAuth';
import { useToast } from '../../hooks/useToast';
import { CATEGORY_IMAGE_MAP } from '../../utils/serviceImages';

export const CompleteProfile: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { setSessionFromTokenResponse, user } = useAuth();
  const { showToast } = useToast();

  const stateData = (location.state as any) || {};
  const initialTokenResponse = stateData.tokenResponse;
  const returnUrl = stateData.returnUrl || '/home';
  const redirectedFromBooking = Boolean(stateData.returnUrl || stateData.fromBooking || stateData.explanation);
  const bookingExplanation = stateData.explanation || 'Please complete your required profile details (mobile phone number) before placing a booking.';

  const savedFullName = initialTokenResponse?.full_name || user?.full_name || '';
  const [fullName, setFullName] = useState(savedFullName);
  const [phone, setPhone] = useState(initialTokenResponse?.phone || user?.phone || '');

  // Service Location Onboarding State
  const initialLoc = initialTokenResponse?.location || user?.location;
  const [address, setAddress] = useState(initialLoc?.address || '');
  const [city, setCity] = useState(initialLoc?.city || 'Noida');
  const [pincode, setPincode] = useState(initialLoc?.postal_code || '201301');
  const [coords, setCoords] = useState<{ latitude?: number; longitude?: number; source?: string }>({
    latitude: initialLoc?.latitude,
    longitude: initialLoc?.longitude,
    source: initialLoc?.source || 'manual',
  });
  const [geoLoading, setGeoLoading] = useState(false);
  const [geoMessage, setGeoMessage] = useState<{ text: string; type: 'success' | 'warning' | 'error' } | null>(null);

  // Optional Category Preferences
  const [selectedCategoryIds, setSelectedCategoryIds] = useState<string[]>([]);
  const [categories, setCategories] = useState<CategoryItem[]>([]);
  
  const [loading, setLoading] = useState(false);
  const [skipLoading, setSkipLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const data = await getCatalogCategories();
        if (data && data.length > 0) {
          setCategories(data);
        } else {
          setCategories(
            Object.keys(CATEGORY_IMAGE_MAP).slice(0, 6).map((catName, idx) => ({
              id: `cat-${idx + 1}`,
              name: catName,
              slug: catName.toLowerCase().replace(/[^a-z0-9]/g, '-'),
              image: CATEGORY_IMAGE_MAP[catName]
            }))
          );
        }
      } catch {
        setCategories(
          Object.keys(CATEGORY_IMAGE_MAP).slice(0, 6).map((catName, idx) => ({
            id: `cat-${idx + 1}`,
            name: catName,
            slug: catName.toLowerCase().replace(/[^a-z0-9]/g, '-'),
            image: CATEGORY_IMAGE_MAP[catName]
          }))
        );
      }
    };
    fetchCategories();
  }, []);

  const handleToggleCategory = (catId: string) => {
    if (selectedCategoryIds.includes(catId)) {
      setSelectedCategoryIds((prev) => prev.filter((id) => id !== catId));
    } else {
      if (selectedCategoryIds.length >= 3) {
        showToast('You can select a maximum of 3 top preferences.', 'info');
        return;
      }
      setSelectedCategoryIds((prev) => [...prev, catId]);
    }
  };

  // Browser Geolocation API Handler
  const handleUseCurrentLocation = () => {
    setGeoMessage(null);
    if (!navigator.geolocation) {
      setGeoMessage({
        text: 'Geolocation is not supported by your browser. Please enter your location manually below.',
        type: 'warning'
      });
      return;
    }

    setGeoLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        setCoords({
          latitude: lat,
          longitude: lng,
          source: 'geolocation',
        });
        if (!address) {
          setAddress(`Detected Location (${lat.toFixed(4)}, ${lng.toFixed(4)})`);
        }
        setGeoMessage({
          text: `Current coordinates detected (${lat.toFixed(4)}, ${lng.toFixed(4)}). You can adjust your street address below.`,
          type: 'success'
        });
        setGeoLoading(false);
      },
      (error) => {
        let errText = 'Unable to retrieve location. Please enter your service address manually.';
        if (error.code === error.PERMISSION_DENIED) {
          errText = 'Location permission was denied. You can safely enter your service address manually below.';
        } else if (error.code === error.POSITION_UNAVAILABLE) {
          errText = 'Location information is unavailable. Please enter your address manually.';
        } else if (error.code === error.TIMEOUT) {
          errText = 'Location request timed out. Please enter your address manually.';
        }
        setGeoMessage({ text: errText, type: 'warning' });
        setGeoLoading(false);
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  };

  const buildLocationPayload = (): CustomerLocationPayload | undefined => {
    if (!address && !coords.latitude) return undefined;
    return {
      address: address.trim() || undefined,
      city: city.trim() || undefined,
      postal_code: pincode.trim() || undefined,
      latitude: coords.latitude,
      longitude: coords.longitude,
      source: coords.source || 'manual',
    };
  };

  // 1. Action: Save and Continue
  const handleSaveAndContinue = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    const cleanName = fullName.trim();
    if (cleanName.length < 2) {
      setErrorMessage('Please enter your full name (at least 2 characters).');
      return;
    }

    const cleanPhone = phone.replace(/[^\d+]/g, '').trim();
    const digitsOnly = cleanPhone.replace(/\D/g, '');
    if (digitsOnly.length < 10) {
      setErrorMessage('Please enter a valid 10-digit mobile phone number.');
      return;
    }

    setLoading(true);
    try {
      const locPayload = buildLocationPayload();
      const updatedResponse = await completeCustomerProfile({
        full_name: cleanName,
        phone: cleanPhone,
        preferences: selectedCategoryIds.length > 0 ? selectedCategoryIds : undefined,
        location: locPayload,
      });

      setSessionFromTokenResponse(updatedResponse);
      showToast('Profile completed successfully! Welcome to SmartServe.', 'success');
      navigate(returnUrl, { replace: true });
    } catch (err: any) {
      const detail = err.response?.data?.detail || 'Failed to complete profile. Please verify your details and try again.';
      setErrorMessage(typeof detail === 'string' ? detail : JSON.stringify(detail));
    } finally {
      setLoading(false);
    }
  };

  // 2. Action: Skip for Now
  const handleSkipForNow = async () => {
    setErrorMessage(null);
    setSkipLoading(true);
    try {
      const cleanName = fullName.trim();
      const cleanPhone = phone.replace(/[^\d+]/g, '').trim();
      const digitsOnly = cleanPhone.replace(/\D/g, '');

      const locPayload = buildLocationPayload();
      const skippedResponse = await skipCustomerProfile({
        full_name: cleanName.length >= 2 ? cleanName : undefined,
        phone: digitsOnly.length >= 10 ? cleanPhone : undefined,
        preferences: selectedCategoryIds.length > 0 ? selectedCategoryIds : undefined,
        location: locPayload,
      });

      setSessionFromTokenResponse(skippedResponse);
      showToast('Profile completion skipped. You can browse services and complete your profile before ordering.', 'info');
      navigate(returnUrl, { replace: true });
    } catch (err: any) {
      const detail = err.response?.data?.detail || 'Failed to skip profile setup. Please try again.';
      setErrorMessage(typeof detail === 'string' ? detail : JSON.stringify(detail));
    } finally {
      setSkipLoading(false);
    }
  };

  const isNamePreFilled = Boolean(savedFullName && savedFullName.trim().length >= 2);

  return (
    <div className="min-h-screen bg-[#FAF7F0] font-sans text-[#1F2A1E] flex items-center justify-center p-4 sm:p-6 lg:p-8">
      <div className="w-full max-w-xl bg-white border border-[#E5DEC9] rounded-3xl p-6 sm:p-10 shadow-xs my-6">
        
        {/* Brand Header */}
        <div className="flex items-center gap-3 mb-6 justify-center">
          <div className="w-11 h-11 rounded-xl border border-[#E5DEC9] bg-[#FAF7F0] flex items-center justify-center p-1 shadow-xs">
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
            <span className="text-2xl font-bold text-[#2F5233] tracking-tight">Smart</span>
            <span className="text-2xl font-bold text-[#C9A15A] tracking-tight ml-0.5">Serve</span>
          </div>
        </div>

        {/* Dedicated Required Heading */}
        <div className="text-center mb-6">
          <h1 className="text-2xl sm:text-3xl font-bold text-[#1F2A1E] tracking-tight mb-2">
            Your profile is not complete yet
          </h1>
          <p className="text-xs sm:text-sm text-[#1F2A1E]/65 font-medium max-w-md mx-auto">
            Please provide your missing contact information and service location. Required details must be completed before placing service orders.
          </p>
        </div>

        {/* Redirect Notice if stopped from placing an order */}
        {redirectedFromBooking && (
          <div className="mb-6 flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-2xl text-amber-900 text-xs sm:text-sm font-medium animate-in fade-in">
            <ShieldAlert className="w-5 h-5 flex-shrink-0 text-amber-700 mt-0.5" />
            <div>
              <div className="font-bold">Profile completion required to order</div>
              <div className="text-amber-800/90 mt-0.5">{bookingExplanation}</div>
            </div>
          </div>
        )}

        {/* Error notification */}
        {errorMessage && (
          <div className="mb-5 flex items-start gap-3 p-3.5 bg-red-50 border border-red-200/80 rounded-xl text-red-800 text-xs font-medium animate-in fade-in">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-red-600 mt-0.5" />
            <span className="flex-1">{errorMessage}</span>
          </div>
        )}

        <form onSubmit={handleSaveAndContinue} className="space-y-6">
          
          {/* Missing vs Prefilled Details Section */}
          <div className="space-y-4">
            
            {/* Full Name */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider">
                  Full Name <span className="text-red-500">*</span>
                </label>
                {isNamePreFilled ? (
                  <span className="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                    <Check className="w-3 h-3" /> From your Google account
                  </span>
                ) : (
                  <span className="text-[10px] font-bold text-red-600 uppercase tracking-wider">
                    Missing · Required
                  </span>
                )}
              </div>
              <div className="relative">
                <User className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Your Full Name"
                  className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-4 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                  required
                  disabled={loading || skipLoading}
                />
              </div>
            </div>

            {/* Mobile Phone Number (Clearly Missing) */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider">
                  Mobile Phone Number <span className="text-red-500">*</span>
                </label>
                <span className="inline-flex items-center gap-1 text-[10px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200">
                  <AlertCircle className="w-3 h-3 text-amber-600" /> Missing · Required to order
                </span>
              </div>
              <div className="relative">
                <Phone className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="+91 9876543210"
                  className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-4 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                  required
                  disabled={loading || skipLoading}
                />
              </div>
              <p className="text-[11px] text-[#1F2A1E]/55 mt-1">
                Required for booking confirmation SMS, OTP arrival verification, and emergency dispatch.
              </p>
            </div>

          </div>

          {/* ── Section: Service Location Onboarding ── */}
          <div className="p-4 sm:p-5 rounded-2xl bg-[#FAF7F0]/60 border border-[#E5DEC9] space-y-4">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-[#2F5233]" />
                  <span className="text-xs font-bold uppercase tracking-wider text-[#1F2A1E]">Service Location Onboarding</span>
                </div>
                <p className="text-[11px] text-[#1F2A1E]/60 mt-0.5">
                  Set where you receive home services. You can change this anytime from the dashboard.
                </p>
              </div>
            </div>

            {/* Geolocation Button */}
            <div>
              <button
                type="button"
                onClick={handleUseCurrentLocation}
                disabled={geoLoading || loading || skipLoading}
                className="w-full h-11 flex items-center justify-center gap-2 bg-white hover:bg-[#FAF7F0] active:bg-[#F2EDE1] text-[#2F5233] font-bold text-xs rounded-xl border border-[#2F5233]/40 shadow-xs hover:border-[#2F5233] transition-all cursor-pointer disabled:opacity-60"
              >
                {geoLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-[#2F5233]" />
                    <span>Detecting location with permission...</span>
                  </>
                ) : (
                  <>
                    <Navigation className="w-4 h-4 text-[#2F5233]" />
                    <span>Use My Current Location</span>
                  </>
                )}
              </button>
            </div>

            {/* Geo Helper Message */}
            {geoMessage && (
              <div className={`p-2.5 rounded-xl text-xs font-medium border flex items-start gap-2 ${
                geoMessage.type === 'success' 
                  ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
                  : 'bg-amber-50 border-amber-200 text-amber-800'
              }`}>
                {geoMessage.type === 'success' ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                ) : (
                  <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
                )}
                <span>{geoMessage.text}</span>
              </div>
            )}

            {/* Manual Location Inputs */}
            <div className="space-y-3 pt-1">
              <div>
                <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1">
                  Street Address / Society / Flat
                </label>
                <input
                  type="text"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="e.g., 204, Palm Grove, SG Highway"
                  className="w-full h-10 bg-white border border-[#E5DEC9] rounded-xl px-3 text-xs font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:border-[#2F5233]"
                  disabled={loading || skipLoading}
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1">
                    City
                  </label>
                  <input
                    type="text"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    placeholder="Ahmedabad / Noida"
                    className="w-full h-10 bg-white border border-[#E5DEC9] rounded-xl px-3 text-xs font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:border-[#2F5233]"
                    disabled={loading || skipLoading}
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1">
                    Postal Code / Pincode
                  </label>
                  <input
                    type="text"
                    value={pincode}
                    onChange={(e) => setPincode(e.target.value)}
                    placeholder="380054"
                    className="w-full h-10 bg-white border border-[#E5DEC9] rounded-xl px-3 text-xs font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:border-[#2F5233]"
                    disabled={loading || skipLoading}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* ── Optional Service Preferences ── */}
          {categories.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider">
                  Service Preferences (Optional · Select up to 3)
                </label>
                <span className="text-[10px] text-[#2F5233] font-semibold flex items-center gap-1">
                  <Sparkles className="w-3 h-3" /> Personalized
                </span>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {categories.map((cat) => {
                  const isSelected = selectedCategoryIds.includes(cat.id);
                  return (
                    <button
                      key={cat.id}
                      type="button"
                      onClick={() => handleToggleCategory(cat.id)}
                      className={`p-2.5 rounded-xl border text-left text-xs font-medium transition-all cursor-pointer flex items-center justify-between ${
                        isSelected
                          ? 'border-[#2F5233] bg-[#2F5233]/5 text-[#2F5233] font-bold ring-1 ring-[#2F5233]'
                          : 'border-[#E5DEC9] bg-white text-[#1F2A1E]/80 hover:bg-[#FAF7F0]'
                      }`}
                    >
                      <span className="truncate">{cat.name}</span>
                      {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-[#2F5233] flex-shrink-0 ml-1" />}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* ── Two Clear Actions: Save and Continue & Skip for Now ── */}
          <div className="pt-2 space-y-3">
            <button
              type="submit"
              disabled={loading || skipLoading}
              className="w-full h-12 flex items-center justify-center gap-2 bg-[#2F5233] hover:bg-[#3D6B42] active:bg-[#244227] text-white font-bold rounded-xl text-sm shadow-xs hover:shadow transition-all disabled:opacity-70 disabled:cursor-not-allowed cursor-pointer"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Saving Profile & Location...</span>
                </>
              ) : (
                <>
                  <span>Save and Continue</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>

            <button
              type="button"
              onClick={handleSkipForNow}
              disabled={loading || skipLoading}
              className="w-full h-11 flex items-center justify-center gap-2 bg-transparent hover:bg-[#FAF7F0] text-[#1F2A1E]/70 hover:text-[#1F2A1E] font-semibold rounded-xl text-xs sm:text-sm border border-[#E5DEC9] transition-all disabled:opacity-60 cursor-pointer"
            >
              {skipLoading ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Skipping to Dashboard...</span>
                </>
              ) : (
                <>
                  <Clock className="w-3.5 h-3.5 text-[#1F2A1E]/50" />
                  <span>Skip for Now</span>
                </>
              )}
            </button>
          </div>

          <p className="text-[11px] text-center text-[#1F2A1E]/45">
            Skipping allows browsing services. Required profile details and service location will be required before confirming any booking.
          </p>
        </form>

      </div>
    </div>
  );
};

export default CompleteProfile;
