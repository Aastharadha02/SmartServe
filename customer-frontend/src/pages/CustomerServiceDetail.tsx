import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getServiceDetail, ServiceItem } from '../api/catalog';
import { createBooking } from '../api/bookings';
import { useAuth } from '../auth/useAuth';
import { useToast } from '../hooks/useToast';
import { formatCurrencyINR } from '../utils/formatters';
import { getServiceImage, formatCategoryDisplayName } from '../utils/serviceImages';
import { 
  Clock, 
  Star, 
  ShieldCheck, 
  Calendar as CalendarIcon, 
  Loader2, 
  ArrowLeft,
  AlertCircle,
  Check,
  XCircle,
  AlertTriangle,
  ChevronRight,
  Sparkles,
  CheckCircle,
  Wrench,
  HelpCircle,
  Lightbulb,
  FileText,
  BadgeCheck,
  Ban,
  Camera,
  Tag
} from 'lucide-react';

export const CustomerServiceDetail: React.FC = () => {
  const { serviceId } = useParams<{ serviceId: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { showToast } = useToast();

  const [service, setService] = useState<ServiceItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Booking Modal State
  const [showBookingModal, setShowBookingModal] = useState<boolean>(false);
  const [bookingDate, setBookingDate] = useState<string>(
    new Date(Date.now() + 86400000).toISOString().split('T')[0] || ''
  );
  const [bookingTime, setBookingTime] = useState<string>('10:00 AM');
  const [address, setAddress] = useState<string>('Flat 402, Sunshine Apartments, Sector 62');
  const [city, setCity] = useState<string>('Noida');
  const [pincode, setPincode] = useState<string>('201301');
  const [notes, setNotes] = useState<string>('');
  const [selectedAddons, setSelectedAddons] = useState<string[]>([]);
  const [bookingLoading, setBookingLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchDetail = async () => {
      if (!serviceId) return;
      setLoading(true);
      setError(null);
      try {
        const data = await getServiceDetail(serviceId);
        setService(data);
        if (data) {
          document.title = data.seo_title || `${data.name} | SmartServe`;
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to load service details from backend.');
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [serviceId]);

  const toggleAddon = (addonId: string) => {
    if (selectedAddons.includes(addonId)) {
      setSelectedAddons((prev) => prev.filter((id) => id !== addonId));
    } else {
      setSelectedAddons((prev) => [...prev, addonId]);
    }
  };

  const calculateTotalPrice = () => {
    if (!service) return 0;
    let total = service.base_price;
    if (service.suggested_addons) {
      service.suggested_addons.forEach((addon) => {
        if (selectedAddons.includes(addon.addon_id)) {
          total += addon.price;
        }
      });
    }
    return total;
  };

  const handleConfirmBooking = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) {
      showToast('Please sign in to complete your booking.', 'info');
      navigate('/login');
      return;
    }

    if (!service) return;

    if (!service.is_active) {
      showToast('This service is currently inactive and cannot be booked.', 'error');
      return;
    }

    setBookingLoading(true);
    try {
      const newBooking = await createBooking({
        service_id: service.id,
        service_name: service.name,
        category: service.category,
        scheduled_date: bookingDate,
        scheduled_time: bookingTime,
        address_line1: `${address}, ${city} - ${pincode}`,
        city,
        pincode,
        notes: notes || 'Standard booking requested via Customer Web',
      });

      showToast(`Booking ${newBooking.booking_reference} confirmed!`, 'success');
      setShowBookingModal(false);
      navigate(`/bookings/${newBooking.id}`);
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to create booking. Please try again.', 'error');
    } finally {
      setBookingLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <Loader2 className="w-10 h-10 animate-spin text-[#2F5233]" />
        <p className="text-sm font-semibold text-[#1F2A1E]/70 font-sans">
          Retrieving live catalog service record...
        </p>
      </div>
    );
  }

  if (error || !service) {
    return (
      <div className="max-w-xl mx-auto my-16 p-8 sm:p-12 bg-white border border-[#E5DEC9] rounded-[28px] text-center space-y-5 shadow-[0_4px_24px_rgba(31,42,30,0.06)]">
        <div className="w-14 h-14 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center mx-auto border border-rose-200">
          <AlertCircle className="w-7 h-7" />
        </div>
        <div className="space-y-2">
          <h3 className="text-2xl font-bold font-serif-display text-[#1F2A1E]">Service Not Available</h3>
          <p className="text-sm text-[#1F2A1E]/70 max-w-md mx-auto">
            {error || 'The requested service does not exist or has been made inactive in the Admin Catalog.'}
          </p>
        </div>
        <button
          onClick={() => navigate('/catalog')}
          className="px-6 py-3 bg-[#2F5233] hover:bg-[#3D6B42] text-[#FAF7F0] font-bold text-xs uppercase tracking-wider rounded-full inline-flex items-center gap-2 shadow-sm transition-all"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Return to Catalog</span>
        </button>
      </div>
    );
  }

  const imgUrl = (service.image_url && !service.image_url.includes('photo-1621905251189-08b45d6a269e'))
    ? service.image_url
    : getServiceImage(service.category, service.subcategory, service.name);

  // Inclusions can be in distinct_features or included or features
  const allInclusions = (service.included && service.included.length > 0)
    ? service.included
    : (service.distinct_features && service.distinct_features.length > 0)
      ? service.distinct_features
      : service.features || [];

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-16">
      
      {/* 1. Breadcrumb Hierarchy Navigation */}
      <nav className="flex items-center gap-2 text-xs font-semibold text-[#1F2A1E]/60 flex-wrap">
        <Link to="/catalog" className="hover:text-[#2F5233] transition-colors">
          Catalog
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-[#1F2A1E]/30 flex-shrink-0" />
        <Link to={`/catalog?category=${encodeURIComponent(service.category)}`} className="hover:text-[#2F5233] transition-colors">
          {formatCategoryDisplayName(service.category)}
        </Link>
        {service.subcategory && (
          <>
            <ChevronRight className="w-3.5 h-3.5 text-[#1F2A1E]/30 flex-shrink-0" />
            <Link to={`/catalog?category=${encodeURIComponent(service.category)}&subcategory=${encodeURIComponent(service.subcategory)}`} className="hover:text-[#2F5233] transition-colors">
              {service.subcategory}
            </Link>
          </>
        )}
        <ChevronRight className="w-3.5 h-3.5 text-[#1F2A1E]/30 flex-shrink-0" />
        <span className="text-[#1F2A1E] font-bold truncate max-w-xs">{service.name}</span>
      </nav>

      {/* Main Grid: 2/3 Content, 1/3 Floating Sidebar */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        
        {/* Left Column (Catalog Information Sections) */}
        <div className="lg:col-span-2 space-y-7">
          
          {/* 2. Hero Cover Banner */}
          <div className="relative rounded-[28px] overflow-hidden h-80 sm:h-[400px] bg-[#F2EDE1] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.06)] group">
            <img
              src={imgUrl}
              alt={service.name}
              className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-[#1F2A1E]/90 via-[#1F2A1E]/30 to-transparent"></div>
            
            <div className="absolute top-5 right-5 flex items-center gap-2">
              {service.is_active ? (
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#10B981]/90 backdrop-blur-md text-white text-[11px] font-bold shadow-xs">
                  <BadgeCheck className="w-3.5 h-3.5" />
                  <span>Active Service</span>
                </span>
              ) : (
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-rose-600/90 backdrop-blur-md text-white text-[11px] font-bold shadow-xs">
                  <Ban className="w-3.5 h-3.5" />
                  <span>Service Suspended</span>
                </span>
              )}
            </div>

            <div className="absolute bottom-6 left-6 right-6 text-white space-y-2.5">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="px-3 py-1 rounded-full bg-[#2F5233]/90 border border-[#7A9E6E]/40 backdrop-blur-md text-[#FAF7F0] text-[11px] font-bold uppercase tracking-wider">
                  {formatCategoryDisplayName(service.category)}
                </span>
                {service.subcategory && (
                  <span className="px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-white text-[11px] font-semibold">
                    {service.subcategory}
                  </span>
                )}
              </div>
              <h1 className="text-2xl sm:text-4xl font-bold font-serif-display text-[#FAF7F0] tracking-tight leading-tight">
                {service.name}
              </h1>
            </div>
          </div>

          {/* Inactive Warning Alert */}
          {!service.is_active && (
            <div className="p-4 rounded-[20px] bg-rose-50 border border-rose-200 text-rose-800 flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-rose-600 flex-shrink-0 mt-0.5" />
              <div className="text-xs space-y-1">
                <p className="font-bold">This service is currently unavailable for new bookings</p>
                <p className="text-rose-700/80">
                  The service administrator has deactivated this service in the catalog. Information is displayed in read-only mode.
                </p>
              </div>
            </div>
          )}

          {/* 3. Description Section */}
          {service.description && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-3">
              <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Service Overview</h3>
              <p className="text-sm text-[#1F2A1E]/80 leading-relaxed font-sans">
                {service.description}
              </p>
              {service.keywords && service.keywords.length > 0 && (
                <div className="pt-2 flex items-center gap-1.5 flex-wrap border-t border-[#E5DEC9]/60">
                  <Tag className="w-3.5 h-3.5 text-[#1F2A1E]/40" />
                  {service.keywords.map((kw, idx) => (
                    <span key={idx} className="px-2.5 py-1 bg-[#F2EDE1]/60 text-[#1F2A1E]/70 rounded-lg text-[11px] font-medium border border-[#E5DEC9]">
                      #{kw}
                    </span>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* 4. Highlights */}
          {service.highlights && service.highlights.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#C9A15A]" />
                <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Service Highlights</h3>
              </div>
              <div className="flex flex-wrap gap-2.5">
                {service.highlights.map((hl, idx) => (
                  <span 
                    key={idx} 
                    className="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-[#FAF7F0] text-[#2F5233] border border-[#C9A15A]/40 rounded-full text-xs font-semibold"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-[#C9A15A]" />
                    <span>{hl}</span>
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* 4b. Distinct Features (Service Features) */}
          {service.service_features && service.service_features.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#2F5233]" />
                <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Distinct Features</h3>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {service.service_features.map((feat, idx) => (
                  <div key={idx} className="p-4 rounded-2xl bg-[#FAF7F0] border border-[#E5DEC9]/70 space-y-1">
                    <h4 className="text-sm font-bold text-[#1F2A1E] flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#C9A15A]" />
                      {feat.title}
                    </h4>
                    {feat.description && (
                      <p className="text-xs text-[#1F2A1E]/70 leading-relaxed font-sans">{feat.description}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 5. What's Included */}
          {allInclusions.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">What's Included</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 text-sm text-[#1F2A1E]">
                {allInclusions.map((feat, idx) => (
                  <div key={idx} className="flex items-start gap-2.5 font-medium bg-[#FAF7F0]/60 p-3 rounded-xl border border-[#E5DEC9]/50">
                    <div className="w-5 h-5 rounded-full bg-[#10B981]/15 text-[#10B981] flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Check className="w-3.5 h-3.5 stroke-[3]" />
                    </div>
                    <span className="text-xs sm:text-sm">{feat}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 6. What's Excluded */}
          {service.excluded && service.excluded.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">What's Excluded</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 text-sm text-[#1F2A1E]/80">
                {service.excluded.map((item, idx) => (
                  <div key={idx} className="flex items-start gap-2.5 font-medium bg-[#FDFCF7] p-3 rounded-xl border border-rose-100">
                    <div className="w-5 h-5 rounded-full bg-rose-50 text-rose-500 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <XCircle className="w-3.5 h-3.5 text-rose-500" />
                    </div>
                    <span className="text-xs sm:text-sm text-[#1F2A1E]/75">{item}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 7. Step-by-Step Process */}
          {service.process_steps && service.process_steps.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-5">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Standard Execution Process</h3>
                <span className="text-xs font-semibold text-[#1F2A1E]/60 bg-[#F2EDE1] px-2.5 py-1 rounded-full">
                  {service.process_steps.length} Steps
                </span>
              </div>
              <div className="space-y-3.5">
                {service.process_steps.map((step) => (
                  <div key={step.step_number} className="flex gap-4 p-4 rounded-2xl bg-[#FAF7F0] border border-[#E5DEC9]/70">
                    <div className="w-8 h-8 rounded-full bg-[#2F5233] text-[#FAF7F0] flex items-center justify-center font-bold text-xs flex-shrink-0 shadow-xs">
                      {step.step_number}
                    </div>
                    <div className="space-y-1 flex-1">
                      <div className="flex items-center justify-between gap-2 flex-wrap">
                        <div className="flex items-center gap-2 flex-wrap">
                          <h4 className="text-sm font-bold text-[#1F2A1E]">{step.title}</h4>
                          {step.is_key_step && (
                            <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-[#C9A15A]/15 text-[#8C6B28] text-[10px] font-bold uppercase tracking-wider border border-[#C9A15A]/30">
                              Key Step
                            </span>
                          )}
                        </div>
                        {step.duration_minutes && (
                          <span className="text-xs font-semibold text-[#1F2A1E]/60 flex items-center gap-1">
                            <Clock className="w-3 h-3 text-[#C9A15A]" />
                            {step.duration_minutes} mins
                          </span>
                        )}
                      </div>
                      {step.description && (
                        <p className="text-xs text-[#1F2A1E]/70 leading-relaxed">{step.description}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 7b. Service Media Gallery */}
          {service.service_media && service.service_media.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Camera className="w-4 h-4 text-[#2F5233]" />
                  <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Service Gallery & Media</h3>
                </div>
                <span className="text-xs font-semibold text-[#1F2A1E]/60 bg-[#F2EDE1] px-2.5 py-1 rounded-full">
                  {service.service_media.length} Photos
                </span>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {service.service_media.map((item, idx) => (
                  <div key={item.id || idx} className="group relative rounded-2xl overflow-hidden border border-[#E5DEC9] bg-[#FAF7F0] aspect-video">
                    <img
                      src={item.url}
                      alt={item.caption || `${service.name} gallery item ${idx + 1}`}
                      className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                    />
                    {item.caption && (
                      <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent p-2 text-white">
                        <p className="text-[11px] truncate font-medium">{item.caption}</p>
                      </div>
                    )}
                    {item.is_cover && (
                      <span className="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-[#2F5233]/90 backdrop-blur-xs text-[10px] font-bold text-white uppercase tracking-wider shadow-xs">
                        Cover
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 8. Products, Materials & Tools */}
          {service.tools_materials && service.tools_materials.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <div className="flex items-center gap-2">
                <Wrench className="w-4 h-4 text-[#7A9E6E]" />
                <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Products, Tools & Materials Used</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {service.tools_materials.map((tm, idx) => (
                  <span 
                    key={idx} 
                    className="px-3.5 py-1.5 bg-[#F2EDE1]/70 border border-[#E5DEC9] rounded-xl text-xs font-semibold text-[#1F2A1E]"
                  >
                    {tm}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* 9. Customer Preparation & Setup */}
          {service.customer_setup && service.customer_setup.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Customer Setup & Preparation</h3>
              <div className="space-y-2.5">
                {service.customer_setup.map((req, idx) => (
                  <div key={idx} className="flex items-start gap-3 text-xs sm:text-sm text-[#1F2A1E]/80 bg-[#FAF7F0] p-3 rounded-xl border border-[#E5DEC9]/60">
                    <span className="w-2 h-2 rounded-full bg-[#C9A15A] flex-shrink-0 mt-1.5" />
                    <span className="font-medium">{req}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 10. Aftercare & Precautions */}
          {service.aftercare && service.aftercare.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Aftercare & Precautions</h3>
              <div className="space-y-2.5">
                {service.aftercare.map((tip, idx) => (
                  <div key={idx} className="flex items-start gap-3 text-xs sm:text-sm text-[#1F2A1E] bg-[#FAF7F0] p-3.5 rounded-xl border border-[#C9A15A]/30">
                    <AlertTriangle className="w-4 h-4 text-[#C9A15A] flex-shrink-0 mt-0.5" />
                    <span className="font-medium">{tip}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 11. Expected Results */}
          {service.expected_results && service.expected_results.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Expected Results</h3>
              <div className="space-y-2.5">
                {service.expected_results.map((res, idx) => (
                  <div key={idx} className="flex items-center gap-3 text-xs sm:text-sm text-[#1F2A1E] bg-[#FAF7F0] p-3 rounded-xl border border-[#E5DEC9]/60">
                    <div className="w-2 h-2 rounded-full bg-[#10B981] flex-shrink-0" />
                    <span className="font-medium">{res}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 12. Important Notes */}
          {service.important_notes && service.important_notes.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-[#1F2A1E]/60" />
                <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Important Notes</h3>
              </div>
              <div className="space-y-2.5">
                {service.important_notes.map((note, idx) => (
                  <div key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm text-[#1F2A1E]/80 bg-[#FAF7F0] p-3.5 rounded-xl border border-[#E5DEC9]/70">
                    <AlertCircle className="w-4 h-4 text-[#1F2A1E]/50 flex-shrink-0 mt-0.5" />
                    <span className="font-medium">{note}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 13. Warranty & Guarantee */}
          {service.warranty && (
            <div className="bg-[#2F5233] text-[#FAF7F0] p-7 sm:p-8 rounded-[24px] border border-[#2F5233] shadow-[0_4px_24px_rgba(47,82,51,0.15)] space-y-3">
              <div className="flex items-center gap-2.5">
                <ShieldCheck className="w-6 h-6 text-[#C9A15A]" />
                <h3 className="text-xl font-bold font-serif-display text-[#FAF7F0]">Service Warranty & Guarantee</h3>
              </div>
              <p className="text-sm text-[#FAF7F0]/85 font-medium leading-relaxed">
                {service.warranty}
              </p>
            </div>
          )}

          {/* 14. Frequently Asked Questions */}
          {service.faqs && service.faqs.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <div className="flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-[#2F5233]" />
                <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Frequently Asked Questions</h3>
              </div>
              <div className="space-y-3">
                {service.faqs.map((faq, idx) => (
                  <div key={idx} className="p-4 rounded-2xl bg-[#FAF7F0] border border-[#E5DEC9]/70 space-y-1.5">
                    <h4 className="text-sm font-bold text-[#1F2A1E]">{faq.question}</h4>
                    <p className="text-xs text-[#1F2A1E]/70 leading-relaxed font-sans">{faq.answer}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 15. Professional Tips */}
          {service.tips && service.tips.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <div className="flex items-center gap-2">
                <Lightbulb className="w-4 h-4 text-[#C9A15A]" />
                <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Professional Tips</h3>
              </div>
              <div className="space-y-2.5">
                {service.tips.map((tip, idx) => (
                  <div key={idx} className="flex items-start gap-3 text-xs sm:text-sm text-[#1F2A1E] bg-[#FAF7F0] p-3.5 rounded-xl border border-[#C9A15A]/30">
                    <span className="w-5 h-5 rounded-full bg-[#C9A15A]/20 text-[#C9A15A] flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                      ★
                    </span>
                    <span className="font-medium">{tip}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 16. Dos & Don'ts */}
          {((service.dos && service.dos.length > 0) || (service.donts && service.donts.length > 0)) && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-5">
              <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Recommended Dos and Don'ts</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                {service.dos && service.dos.length > 0 && (
                  <div className="space-y-2.5">
                    <h4 className="text-xs font-bold text-[#2F5233] uppercase tracking-wider flex items-center gap-1.5">
                      <CheckCircle className="w-4 h-4 text-[#10B981]" />
                      Dos
                    </h4>
                    <div className="space-y-2">
                      {service.dos.map((item, idx) => (
                        <div key={idx} className="flex items-start gap-2 text-xs sm:text-sm text-[#1F2A1E] bg-[#FAF7F0] p-3 rounded-xl border border-[#10B981]/20">
                          <CheckCircle className="w-3.5 h-3.5 text-[#10B981] flex-shrink-0 mt-0.5" />
                          <span>{item}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {service.donts && service.donts.length > 0 && (
                  <div className="space-y-2.5">
                    <h4 className="text-xs font-bold text-rose-800 uppercase tracking-wider flex items-center gap-1.5">
                      <AlertCircle className="w-4 h-4 text-rose-600" />
                      Don'ts
                    </h4>
                    <div className="space-y-2">
                      {service.donts.map((item, idx) => (
                        <div key={idx} className="flex items-start gap-2 text-xs sm:text-sm text-rose-950 bg-[#FDFCF7] p-3 rounded-xl border border-rose-200">
                          <span className="text-rose-600 font-bold flex-shrink-0">✕</span>
                          <span>{item}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* 17. Recommended Add-Ons (Real Database Add-ons) */}
          {service.suggested_addons && service.suggested_addons.length > 0 && (
            <div className="bg-white p-7 sm:p-8 rounded-[24px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.04)] space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold font-serif-display text-[#1F2A1E]">Customizable Service Add-Ons</h3>
                  <p className="text-xs text-[#1F2A1E]/60">Select enhancements to bundle with your service request</p>
                </div>
                {selectedAddons.length > 0 && (
                  <span className="text-xs font-bold text-[#2F5233] bg-[#F2EDE1] px-2.5 py-1 rounded-full">
                    {selectedAddons.length} Selected
                  </span>
                )}
              </div>
              <div className="space-y-3">
                {service.suggested_addons.map((addon) => {
                  const isSelected = selectedAddons.includes(addon.addon_id);
                  return (
                    <div
                      key={addon.addon_id}
                      onClick={() => toggleAddon(addon.addon_id)}
                      className={`p-4 rounded-2xl border transition-all cursor-pointer flex items-center justify-between gap-4 ${
                        isSelected
                          ? 'border-[#2F5233] bg-[#FAF7F0] ring-1 ring-[#2F5233]'
                          : 'border-[#E5DEC9] hover:border-[#2F5233]/40 bg-white'
                      }`}
                    >
                      <div className="space-y-0.5">
                        <h4 className="font-bold text-[#1F2A1E] text-sm">{addon.name}</h4>
                        {addon.description && <p className="text-xs text-[#1F2A1E]/60">{addon.description}</p>}
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="font-bold text-[#1F2A1E] text-sm font-sans">+{formatCurrencyINR(addon.price)}</span>
                        <div className={`w-5 h-5 rounded-md border flex items-center justify-center transition-colors ${isSelected ? 'bg-[#2F5233] text-white border-[#2F5233]' : 'border-[#E5DEC9] bg-white'}`}>
                          {isSelected && <Check className="w-3.5 h-3.5" />}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

        </div>

        {/* Right Column: Sticky Pricing & Action Card */}
        <div className="space-y-6 sticky top-24">
          <div className="bg-white p-7 rounded-[28px] border border-[#E5DEC9] shadow-[0_4px_24px_rgba(31,42,30,0.06)] space-y-6">
            
            <div className="space-y-1.5 border-b border-[#E5DEC9]/80 pb-5">
              <span className="text-[11px] font-bold text-[#1F2A1E]/50 uppercase tracking-wider block">Total Service Price</span>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl sm:text-4xl font-bold font-serif-display text-[#1F2A1E]">
                  {formatCurrencyINR(calculateTotalPrice())}
                </span>
                {selectedAddons.length > 0 && (
                  <span className="text-xs font-semibold text-[#2F5233] bg-[#F2EDE1] px-2 py-0.5 rounded-full">
                    +{selectedAddons.length} Add-on(s)
                  </span>
                )}
              </div>
            </div>

            <div className="space-y-3.5 text-xs text-[#1F2A1E]/80">
              <div className="flex items-center justify-between">
                <span className="font-medium">Estimated Duration</span>
                <span className="font-bold text-[#1F2A1E] flex items-center gap-1.5">
                  <Clock className="w-4 h-4 text-[#C9A15A]" />
                  <span>{service.duration_minutes || 45} Minutes</span>
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="font-medium">Customer Rating</span>
                <span className="font-bold text-[#1F2A1E] flex items-center gap-1">
                  <Star className="w-3.5 h-3.5 fill-[#C9A15A] text-[#C9A15A]" />
                  {service.rating || '4.8'} ({service.review_count || 120} reviews)
                </span>
              </div>
              {service.max_demand_increase !== undefined && service.max_demand_increase > 0 && (
                <div className="flex items-center justify-between">
                  <span className="font-medium">Surge Protection Cap</span>
                  <span className="font-bold text-[#C9A15A] bg-[#FAF7F0] px-2 py-0.5 rounded-md border border-[#C9A15A]/30">
                    Max +{Math.round(service.max_demand_increase * 100)}%
                  </span>
                </div>
              )}
              {service.max_discount !== undefined && service.max_discount > 0 && (
                <div className="flex items-center justify-between">
                  <span className="font-medium">Max Promotional Discount</span>
                  <span className="font-bold text-[#10B981] bg-[#10B981]/10 px-2 py-0.5 rounded-md border border-[#10B981]/20">
                    Up to {Math.round(service.max_discount * 100)}%
                  </span>
                </div>
              )}
              <div className="flex items-center justify-between">
                <span className="font-medium">Cancellation Policy</span>
                <span className="font-bold text-[#10B981]">Free cancellation up to 2h prior</span>
              </div>
            </div>

            {service.is_active ? (
              <button
                onClick={() => setShowBookingModal(true)}
                className="w-full py-4 bg-[#2F5233] hover:bg-[#3D6B42] text-[#FAF7F0] font-bold rounded-full text-sm shadow-[0_4px_16px_rgba(47,82,51,0.2)] hover:shadow-md transition-all flex items-center justify-center gap-2"
              >
                <CalendarIcon className="w-4 h-4 text-[#C9A15A]" />
                <span>Book This Service</span>
              </button>
            ) : (
              <button
                disabled
                className="w-full py-4 bg-slate-100 text-slate-400 font-bold rounded-full text-sm cursor-not-allowed flex items-center justify-center gap-2 border border-slate-200"
              >
                <Ban className="w-4 h-4" />
                <span>Service Unavailable</span>
              </button>
            )}

            <div className="text-center pt-2">
              <span className="text-[11px] font-semibold text-[#1F2A1E]/50 flex items-center justify-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-[#10B981]" />
                <span>Verified Direct Booking via SmartServe Platform</span>
              </span>
            </div>
          </div>
        </div>

      </div>

      {/* BOOKING MODAL (Rendered with SmartServe Luxury Aesthetics) */}
      {showBookingModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#1F2A1E]/60 backdrop-blur-xs animate-in fade-in">
          <div className="bg-[#FAF7F0] rounded-[28px] max-w-lg w-full p-6 sm:p-8 space-y-6 shadow-2xl border border-[#E5DEC9] animate-in zoom-in-95 max-h-[90vh] overflow-y-auto">
            
            <div className="flex items-center justify-between border-b border-[#E5DEC9] pb-4">
              <div>
                <h3 className="text-xl font-bold font-serif-display text-[#1F2A1E]">Schedule Service Booking</h3>
                <p className="text-xs text-[#1F2A1E]/60 font-medium">{service.name}</p>
              </div>
              <button
                onClick={() => setShowBookingModal(false)}
                className="text-[#1F2A1E]/50 hover:text-[#1F2A1E] p-1.5 rounded-full hover:bg-black/5 text-sm font-bold transition-colors"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleConfirmBooking} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider mb-1.5">Preferred Date</label>
                <input
                  type="date"
                  value={bookingDate}
                  onChange={(e) => setBookingDate(e.target.value)}
                  className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl px-4 text-sm font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider mb-1.5">Preferred Time Slot</label>
                <select
                  value={bookingTime}
                  onChange={(e) => setBookingTime(e.target.value)}
                  className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl px-4 text-sm font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
                >
                  <option value="09:00 AM">09:00 AM - 11:00 AM</option>
                  <option value="10:00 AM">10:00 AM - 12:00 PM</option>
                  <option value="02:00 PM">02:00 PM - 04:00 PM</option>
                  <option value="05:00 PM">05:00 PM - 07:00 PM</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider mb-1.5">Street Address</label>
                <input
                  type="text"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="Flat / House No., Building Name, Street"
                  className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl px-4 text-sm font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider mb-1.5">City</label>
                  <input
                    type="text"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl px-4 text-sm font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider mb-1.5">Pincode</label>
                  <input
                    type="text"
                    value={pincode}
                    onChange={(e) => setPincode(e.target.value)}
                    className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl px-4 text-sm font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider mb-1.5">Special Instructions (Optional)</label>
                <input
                  type="text"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="e.g. Ring bell twice, specific parking instructions"
                  className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl px-4 text-sm font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
                />
              </div>

              <div className="pt-2 border-t border-[#E5DEC9] flex items-center justify-between text-sm">
                <span className="font-semibold text-[#1F2A1E]/70">Total Amount</span>
                <span className="text-xl font-bold font-serif-display text-[#1F2A1E]">{formatCurrencyINR(calculateTotalPrice())}</span>
              </div>

              <div className="pt-2 flex gap-3">
                <button
                  type="button"
                  onClick={() => setShowBookingModal(false)}
                  className="w-1/2 py-3.5 bg-white hover:bg-[#F2EDE1] font-bold text-[#1F2A1E] rounded-full text-xs uppercase tracking-wider border border-[#E5DEC9] transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={bookingLoading}
                  className="w-1/2 py-3.5 bg-[#2F5233] hover:bg-[#3D6B42] text-[#FAF7F0] font-bold rounded-full text-xs uppercase tracking-wider shadow-sm transition-all disabled:opacity-70 flex items-center justify-center gap-2"
                >
                  {bookingLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Booking...</span>
                    </>
                  ) : (
                    <span>Confirm Booking</span>
                  )}
                </button>
              </div>
            </form>

          </div>
        </div>
      )}

    </div>
  );
};

export default CustomerServiceDetail;
