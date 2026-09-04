import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getServiceDetail, ServiceItem } from '../api/catalog';
import { createBooking } from '../api/bookings';
import { useAuth } from '../auth/useAuth';
import { useToast } from '../hooks/useToast';
import { formatCurrencyINR } from '../utils/formatters';
import { getServiceImage } from '../utils/serviceImages';
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
  CheckCircle
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
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3 font-sans">
        <Loader2 className="w-10 h-10 animate-spin text-[#2563EB]" />
        <p className="text-sm font-semibold text-slate-600">Loading service details from database...</p>
      </div>
    );
  }

  if (error || !service) {
    return (
      <div className="max-w-xl mx-auto my-12 p-8 bg-white border border-slate-200 rounded-3xl text-center space-y-4 shadow-sm font-sans">
        <AlertCircle className="w-10 h-10 text-rose-500 mx-auto" />
        <h3 className="text-xl font-bold text-slate-900">Service Not Found</h3>
        <p className="text-sm text-slate-600">{error || 'The requested service does not exist in the backend database.'}</p>
        <button
          onClick={() => navigate('/catalog')}
          className="px-5 py-2.5 bg-[#2563EB] text-white font-bold text-xs rounded-xl inline-flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Catalog</span>
        </button>
      </div>
    );
  }

  const imgUrl = (service.image_url && !service.image_url.includes('photo-1621905251189-08b45d6a269e'))
    ? service.image_url
    : getServiceImage(service.category, service.subcategory, service.name);

  return (
    <div className="space-y-8 font-sans max-w-5xl mx-auto">
      
      {/* Breadcrumb Hierarchy Navigation */}
      <nav className="flex items-center gap-2 text-xs font-bold text-slate-500 flex-wrap">
        <Link to="/catalog" className="hover:text-[#2563EB] transition-colors">
          All Categories
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
        <Link to={`/catalog?category=${encodeURIComponent(service.category)}`} className="hover:text-[#2563EB] transition-colors">
          {service.category}
        </Link>
        {service.subcategory && (
          <>
            <ChevronRight className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
            <Link to={`/catalog?category=${encodeURIComponent(service.category)}&subcategory=${encodeURIComponent(service.subcategory)}`} className="hover:text-[#2563EB] transition-colors">
              {service.subcategory}
            </Link>
          </>
        )}
        <ChevronRight className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
        <span className="text-slate-900 font-extrabold">{service.name}</span>
      </nav>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Service Image Header */}
          <div className="relative rounded-3xl overflow-hidden h-72 sm:h-96 bg-slate-100 border border-slate-200 shadow-sm">
            <img
              src={imgUrl}
              alt={service.name}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent"></div>
            
            <div className="absolute bottom-6 left-6 right-6 text-white space-y-2">
              <div className="flex items-center gap-2">
                <span className="px-3 py-1 rounded-full bg-blue-600/90 backdrop-blur-xs text-white text-xs font-extrabold uppercase tracking-wider">
                  {service.category}
                </span>
                {service.subcategory && (
                  <span className="px-3 py-1 rounded-full bg-white/20 backdrop-blur-xs text-white text-xs font-semibold uppercase">
                    {service.subcategory}
                  </span>
                )}
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">{service.name}</h1>
            </div>
          </div>

          {/* Description */}
          {service.description && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">Service Description</h3>
              <p className="text-sm text-slate-600 leading-relaxed font-normal">
                {service.description}
              </p>
            </div>
          )}

          {/* Highlights */}
          {service.highlights && service.highlights.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">Service Highlights</h3>
              <div className="flex flex-wrap gap-2">
                {service.highlights.map((hl, idx) => (
                  <span key={idx} className="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-blue-50 text-blue-700 border border-blue-200/80 rounded-xl text-xs font-bold">
                    <Sparkles className="w-3.5 h-3.5 text-blue-500" />
                    <span>{hl}</span>
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Features Included */}
          {((service.included && service.included.length > 0) || (service.features && service.features.length > 0)) && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">What's Included</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm text-slate-700">
                {(service.included && service.included.length > 0 ? service.included : service.features || []).map((feat, idx) => (
                  <div key={idx} className="flex items-center gap-2.5 font-medium">
                    <div className="w-5 h-5 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center flex-shrink-0">
                      <Check className="w-3.5 h-3.5 stroke-[3]" />
                    </div>
                    <span>{feat}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Excluded Scope */}
          {service.excluded && service.excluded.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">What's Excluded</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm text-slate-700">
                {service.excluded.map((item, idx) => (
                  <div key={idx} className="flex items-center gap-2.5 font-medium text-slate-600">
                    <div className="w-5 h-5 rounded-full bg-rose-50 text-rose-500 flex items-center justify-center flex-shrink-0">
                      <XCircle className="w-3.5 h-3.5 text-rose-500" />
                    </div>
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Process Steps / How It Works */}
          {service.process_steps && service.process_steps.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-5">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-extrabold text-slate-900">How It Works</h3>
                <span className="text-xs font-semibold text-slate-500">{service.process_steps.length} Steps Workflow</span>
              </div>
              <div className="space-y-3">
                {service.process_steps.map((step) => (
                  <div key={step.step_number} className="flex gap-4 p-4 rounded-2xl bg-slate-50/80 border border-slate-100">
                    <div className="w-8 h-8 rounded-xl bg-[#2563EB] text-white flex items-center justify-center font-bold text-sm flex-shrink-0">
                      {step.step_number}
                    </div>
                    <div className="space-y-1 flex-1">
                      <div className="flex items-center justify-between">
                        <h4 className="text-sm font-bold text-slate-900">{step.title}</h4>
                        {step.duration_minutes && (
                          <span className="text-xs font-semibold text-slate-500 flex items-center gap-1">
                            <Clock className="w-3 h-3 text-slate-400" />
                            {step.duration_minutes} mins
                          </span>
                        )}
                      </div>
                      {step.description && (
                        <p className="text-xs text-slate-600 leading-relaxed">{step.description}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Aftercare & Precautions */}
          {service.aftercare && service.aftercare.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">Aftercare & Precautions</h3>
              <div className="space-y-2.5">
                {service.aftercare.map((tip, idx) => (
                  <div key={idx} className="flex items-start gap-3 text-sm text-slate-700 bg-amber-50/50 p-3.5 rounded-xl border border-amber-200/50">
                    <AlertTriangle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
                    <span className="font-medium">{tip}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tools & Materials */}
          {service.tools_materials && service.tools_materials.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">Tools & Materials</h3>
              <div className="flex flex-wrap gap-2">
                {service.tools_materials.map((tm, idx) => (
                  <span key={idx} className="px-3 py-1.5 bg-slate-100 rounded-xl text-xs font-semibold text-slate-700">
                    {tm}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Customer Preparation & Setup */}
          {service.customer_setup && service.customer_setup.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">Customer Preparation & Setup</h3>
              <div className="space-y-2">
                {service.customer_setup.map((req, idx) => (
                  <div key={idx} className="flex items-center gap-2.5 text-sm text-slate-700">
                    <div className="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0" />
                    <span className="font-medium">{req}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Warranty & Guarantee */}
          {service.warranty && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-2">
              <h3 className="text-lg font-extrabold text-slate-900 flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-emerald-600" />
                <span>Service Warranty & Guarantee</span>
              </h3>
              <p className="text-sm text-slate-700 font-medium">{service.warranty}</p>
            </div>
          )}

          {/* Frequently Asked Questions */}
          {service.faqs && service.faqs.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">Frequently Asked Questions</h3>
              <div className="space-y-3">
                {service.faqs.map((faq, idx) => (
                  <div key={idx} className="p-4 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
                    <h4 className="text-sm font-bold text-slate-900">{faq.question}</h4>
                    <p className="text-xs text-slate-600 leading-relaxed font-normal">{faq.answer}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Suggested Addons */}
          {service.suggested_addons && service.suggested_addons.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">Recommended Add-Ons</h3>
              <div className="space-y-3">
                {service.suggested_addons.map((addon) => {
                  const isSelected = selectedAddons.includes(addon.addon_id);
                  return (
                    <div
                      key={addon.addon_id}
                      onClick={() => toggleAddon(addon.addon_id)}
                      className={`p-4 rounded-2xl border transition-all cursor-pointer flex items-center justify-between gap-4 ${
                        isSelected
                          ? 'border-[#2563EB] bg-blue-50/50 ring-1 ring-[#2563EB]'
                          : 'border-slate-200 hover:border-slate-300'
                      }`}
                    >
                      <div className="space-y-0.5">
                        <h4 className="font-bold text-slate-900 text-sm">{addon.name}</h4>
                        {addon.description && <p className="text-xs text-slate-500">{addon.description}</p>}
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="font-extrabold text-slate-900 text-sm font-mono">+₹{addon.price}</span>
                        <div className={`w-5 h-5 rounded-lg border flex items-center justify-center ${isSelected ? 'bg-[#2563EB] text-white border-[#2563EB]' : 'border-slate-300 bg-white'}`}>
                          {isSelected && <Check className="w-3.5 h-3.5" />}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Expected Results */}
          {service.expected_results && service.expected_results.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">Expected Results</h3>
              <div className="space-y-2">
                {service.expected_results.map((res, idx) => (
                  <div key={idx} className="flex items-center gap-2.5 text-sm text-slate-700">
                    <div className="w-2 h-2 rounded-full bg-emerald-500 flex-shrink-0" />
                    <span className="font-medium">{res}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Important Notes */}
          {service.important_notes && service.important_notes.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">Important Notes</h3>
              <div className="space-y-2">
                {service.important_notes.map((note, idx) => (
                  <div key={idx} className="flex items-start gap-2.5 text-sm text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100">
                    <AlertCircle className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
                    <span className="font-medium">{note}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Professional Tips */}
          {service.tips && service.tips.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">Professional Tips</h3>
              <div className="space-y-2">
                {service.tips.map((tip, idx) => (
                  <div key={idx} className="flex items-start gap-2.5 text-sm text-slate-700 bg-blue-50/40 p-3 rounded-xl border border-blue-100/60">
                    <span className="w-5 h-5 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">💡</span>
                    <span className="font-medium">{tip}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Dos & Don'ts */}
          {((service.dos && service.dos.length > 0) || (service.donts && service.donts.length > 0)) && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-2xs space-y-4">
              <h3 className="text-lg font-extrabold text-slate-900">Dos and Don'ts</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {service.dos && service.dos.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-emerald-800 uppercase tracking-wider flex items-center gap-1.5">
                      <CheckCircle className="w-4 h-4 text-emerald-600" />
                      Dos
                    </h4>
                    <div className="space-y-1.5">
                      {service.dos.map((item, idx) => (
                        <div key={idx} className="flex items-start gap-2 text-xs sm:text-sm text-emerald-950 bg-emerald-50/50 p-2.5 rounded-xl border border-emerald-100/80">
                          <CheckCircle className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0 mt-0.5" />
                          <span>{item}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {service.donts && service.donts.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-rose-800 uppercase tracking-wider flex items-center gap-1.5">
                      <AlertCircle className="w-4 h-4 text-rose-600" />
                      Don'ts
                    </h4>
                    <div className="space-y-1.5">
                      {service.donts.map((item, idx) => (
                        <div key={idx} className="flex items-start gap-2 text-xs sm:text-sm text-rose-950 bg-rose-50/50 p-2.5 rounded-xl border border-rose-100/80">
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

        </div>

        {/* Right Column */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-3xl border border-slate-200/90 shadow-md space-y-6 sticky top-24">
            
            <div className="space-y-1 border-b border-slate-100 pb-4">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Service Fixed Price</span>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-slate-900 font-mono">
                  {formatCurrencyINR(calculateTotalPrice())}
                </span>
                {selectedAddons.length > 0 && (
                  <span className="text-xs font-semibold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full">
                    Includes {selectedAddons.length} Add-on(s)
                  </span>
                )}
              </div>
            </div>

            <div className="space-y-3 text-xs text-slate-600">
              <div className="flex items-center justify-between">
                <span>Est. Service Duration</span>
                <span className="font-bold text-slate-900 flex items-center gap-1.5">
                  <Clock className="w-4 h-4 text-[#2563EB]" />
                  <span>{service.duration_minutes || 45} Minutes</span>
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Customer Rating</span>
                <span className="font-bold text-slate-900 flex items-center gap-1">
                  <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                  {service.rating || '4.8'} ({service.review_count || 120} reviews)
                </span>
              </div>
              {service.max_demand_increase !== undefined && service.max_demand_increase > 0 && (
                <div className="flex items-center justify-between">
                  <span>Surge Protection Cap</span>
                  <span className="font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded-md border border-amber-200/60">
                    Max +{Math.round(service.max_demand_increase * 100)}%
                  </span>
                </div>
              )}
              {service.max_discount !== undefined && service.max_discount > 0 && (
                <div className="flex items-center justify-between">
                  <span>Max Promotional Discount</span>
                  <span className="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200/60">
                    Up to {Math.round(service.max_discount * 100)}%
                  </span>
                </div>
              )}
              <div className="flex items-center justify-between">
                <span>Cancellation Policy</span>
                <span className="font-bold text-emerald-600">Free until 2h prior</span>
              </div>
            </div>

            <button
              onClick={() => setShowBookingModal(true)}
              className="w-full py-4 bg-[#2563EB] hover:bg-blue-700 text-white font-bold rounded-2xl text-base shadow-sm hover:shadow transition-all flex items-center justify-center gap-2"
            >
              <CalendarIcon className="w-5 h-5" />
              <span>Book This Service</span>
            </button>

            <div className="text-center">
              <span className="text-[11px] font-semibold text-slate-400 flex items-center justify-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
                <span>Guaranteed Direct Dispatch via SmartServe API</span>
              </span>
            </div>
          </div>
        </div>

      </div>

      {/* BOOKING MODAL */}
      {showBookingModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 space-y-6 shadow-2xl border border-slate-200 animate-in zoom-in-95 max-h-[90vh] overflow-y-auto">
            
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div>
                <h3 className="text-xl font-extrabold text-slate-900">Schedule Service Booking</h3>
                <p className="text-xs text-slate-500 font-medium">{service.name}</p>
              </div>
              <button
                onClick={() => setShowBookingModal(false)}
                className="text-slate-400 hover:text-slate-600 p-1 text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleConfirmBooking} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Scheduled Date</label>
                <input
                  type="date"
                  value={bookingDate}
                  onChange={(e) => setBookingDate(e.target.value)}
                  className="w-full h-12 bg-slate-50 border border-slate-200 rounded-xl px-4 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Preferred Time Slot</label>
                <select
                  value={bookingTime}
                  onChange={(e) => setBookingTime(e.target.value)}
                  className="w-full h-12 bg-slate-50 border border-slate-200 rounded-xl px-4 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
                >
                  <option value="09:00 AM">09:00 AM - 11:00 AM</option>
                  <option value="10:00 AM">10:00 AM - 12:00 PM</option>
                  <option value="02:00 PM">02:00 PM - 04:00 PM</option>
                  <option value="05:00 PM">05:00 PM - 07:00 PM</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Service Street Address</label>
                <input
                  type="text"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="Flat No., Building Name, Street"
                  className="w-full h-12 bg-slate-50 border border-slate-200 rounded-xl px-4 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">City</label>
                  <input
                    type="text"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    className="w-full h-12 bg-slate-50 border border-slate-200 rounded-xl px-4 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Pincode</label>
                  <input
                    type="text"
                    value={pincode}
                    onChange={(e) => setPincode(e.target.value)}
                    className="w-full h-12 bg-slate-50 border border-slate-200 rounded-xl px-4 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Special Instructions (Optional)</label>
                <input
                  type="text"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="e.g. Ring bell twice, bring ladder"
                  className="w-full h-12 bg-slate-50 border border-slate-200 rounded-xl px-4 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
                />
              </div>

              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-sm">
                <span className="font-semibold text-slate-600">Total Payable</span>
                <span className="text-xl font-extrabold text-slate-900 font-mono">{formatCurrencyINR(calculateTotalPrice())}</span>
              </div>

              <div className="pt-2 flex gap-3">
                <button
                  type="button"
                  onClick={() => setShowBookingModal(false)}
                  className="w-1/2 py-3.5 bg-slate-100 hover:bg-slate-200 font-bold text-slate-700 rounded-xl text-sm transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={bookingLoading}
                  className="w-1/2 py-3.5 bg-[#2563EB] hover:bg-blue-700 text-white font-bold rounded-xl text-sm shadow-sm transition-all disabled:opacity-70 flex items-center justify-center gap-2"
                >
                  {bookingLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Processing...</span>
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
