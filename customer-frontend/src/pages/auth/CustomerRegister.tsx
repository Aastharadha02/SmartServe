import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  Mail, 
  Lock, 
  User, 
  Phone, 
  MapPin, 
  CheckCircle2, 
  ArrowRight, 
  ArrowLeft, 
  Loader2, 
  AlertCircle, 
  Sparkles, 
  ShieldCheck,
  Check
} from 'lucide-react';
import { getCatalogCategories, CategoryItem } from '../../api/catalog';
import { registerCustomer } from '../../api/auth';
import { useAuth } from '../../auth/useAuth';
import { useToast } from '../../hooks/useToast';
import { getCategoryImageUrl, CATEGORY_IMAGE_MAP } from '../../utils/serviceImages';
import { validateEmail, validatePhone } from '../../utils/validators';

export const CustomerRegister: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const { showToast } = useToast();

  const [step, setStep] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Form State across 5 steps
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [city, setCity] = useState('Noida');
  const [pincode, setPincode] = useState('201301');

  // Step 3: Top 3 Preferences Category Image Grid
  const [categories, setCategories] = useState<CategoryItem[]>([]);
  const [loadingCategories, setLoadingCategories] = useState<boolean>(false);
  const [selectedCategoryIds, setSelectedCategoryIds] = useState<string[]>([]);

  useEffect(() => {
    const fetchCategories = async () => {
      setLoadingCategories(true);
      try {
        const data = await getCatalogCategories();
        if (data && data.length > 0) {
          setCategories(data);
        } else {
          setCategories(
            Object.keys(CATEGORY_IMAGE_MAP).slice(0, 8).map((catName, idx) => ({
              id: `cat-${idx + 1}`,
              name: catName,
              slug: catName.toLowerCase().replace(/[^a-z0-9]/g, '-'),
              image: CATEGORY_IMAGE_MAP[catName]
            }))
          );
        }
      } catch {
        setCategories(
          Object.keys(CATEGORY_IMAGE_MAP).slice(0, 8).map((catName, idx) => ({
            id: `cat-${idx + 1}`,
            name: catName,
            slug: catName.toLowerCase().replace(/[^a-z0-9]/g, '-'),
            image: CATEGORY_IMAGE_MAP[catName]
          }))
        );
      } finally {
        setLoadingCategories(false);
      }
    };
    fetchCategories();
  }, []);

  const handleToggleCategory = (catId: string) => {
    if (selectedCategoryIds.includes(catId)) {
      setSelectedCategoryIds((prev) => prev.filter((id) => id !== catId));
    } else {
      if (selectedCategoryIds.length >= 3) {
        showToast('You can select a maximum of 3 top category preferences.', 'info');
        return;
      }
      setSelectedCategoryIds((prev) => [...prev, catId]);
    }
  };

  const handleNextStep1 = () => {
    setError(null);
    if (!validateEmail(email)) {
      setError('Please enter a valid email address.');
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    setStep(2);
  };

  const handleNextStep2 = () => {
    setError(null);
    if (!fullName.trim()) {
      setError('Please enter your full name.');
      return;
    }
    if (!validatePhone(phone)) {
      setError('Please enter a valid 10-digit mobile number.');
      return;
    }
    setStep(3);
  };

  const handleNextStep3 = () => {
    setError(null);
    if (selectedCategoryIds.length !== 3) {
      setError('Please select exactly 3 top service category preferences to continue.');
      return;
    }
    setStep(4);
  };

  const handleCompleteRegister = async () => {
    setError(null);
    setLoading(true);
    try {
      await registerCustomer({
        email,
        password,
        full_name: fullName,
        phone,
        preferences: selectedCategoryIds
      });

      await login({ email, password });
      showToast('Registration successful! Welcome to SmartServe.', 'success');
      setStep(5);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create customer account. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FAF7F0] flex items-center justify-center p-4 sm:p-6 lg:p-8 font-sans text-[#1F2A1E]">
      <div className="max-w-3xl w-full bg-white rounded-3xl border border-[#E5DEC9] shadow-xs overflow-hidden my-6">
        
        {/* Top Header & Progress Indicator (Matching Admin/Auth Visual Style) */}
        <div className="bg-[#FAF7F0] border-b border-[#E5DEC9] p-6 sm:p-8 space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {/* Authentic SmartServe Logo */}
              <div className="w-11 h-11 rounded-xl border border-[#E5DEC9] bg-[#FAF7F0] flex items-center justify-center shadow-xs p-1">
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
              <div>
                <div className="flex items-baseline font-serif">
                  <span className="text-xl font-bold text-[#2F5233] tracking-tight">Smart</span>
                  <span className="text-xl font-bold text-[#C9A15A] tracking-tight ml-0.5">Serve</span>
                </div>
                <span className="text-[11px] font-semibold text-[#1F2A1E]/60 uppercase tracking-wider block font-sans">
                  Customer Onboarding
                </span>
              </div>
            </div>
            <span className="px-3.5 py-1 rounded-full bg-[#2F5233] text-white text-xs font-bold uppercase tracking-wider shadow-xs">
              Step {step} of 5
            </span>
          </div>

          {/* 5-Step Progress Bar */}
          <div className="space-y-2">
            <div className="grid grid-cols-5 gap-2">
              {[1, 2, 3, 4, 5].map((s) => (
                <div
                  key={s}
                  className={`h-2 rounded-full transition-all ${
                    s <= step ? 'bg-[#2F5233]' : 'bg-[#E5DEC9]'
                  }`}
                />
              ))}
            </div>
            <div className="flex justify-between text-[11px] font-semibold text-[#1F2A1E]/40">
              <span className={step >= 1 ? 'text-[#2F5233] font-bold' : ''}>Credentials</span>
              <span className={step >= 2 ? 'text-[#2F5233] font-bold' : ''}>Personal Info</span>
              <span className={step >= 3 ? 'text-[#2F5233] font-bold' : ''}>3 Preferences</span>
              <span className={step >= 4 ? 'text-[#2F5233] font-bold' : ''}>Summary</span>
              <span className={step >= 5 ? 'text-[#2F5233] font-bold' : ''}>Complete</span>
            </div>
          </div>
        </div>

        {/* Form Body */}
        <div className="p-6 sm:p-10 space-y-6">
          
          {error && (
            <div className="flex items-start gap-3 p-3.5 bg-red-50 border border-red-200 rounded-xl text-red-800 text-xs sm:text-sm font-medium animate-in fade-in">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-red-600 mt-0.5" />
              <div className="flex-1">{error}</div>
            </div>
          )}

          {/* STEP 1 */}
          {step === 1 && (
            <div className="space-y-6 animate-in fade-in">
              <div className="space-y-1">
                <h3 className="text-2xl font-bold text-[#1F2A1E] tracking-tight">Step 1: Account Credentials</h3>
                <p className="text-sm text-[#1F2A1E]/60 font-medium">Enter your email and password for your SmartServe account.</p>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">Email Address</label>
                  <div className="relative">
                    <Mail className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="name@example.com"
                      className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-4 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">Password</label>
                  <div className="relative">
                    <Lock className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="At least 6 characters"
                      className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-4 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">Confirm Password</label>
                  <div className="relative">
                    <Lock className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                    <input
                      type="password"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="Repeat password"
                      className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-4 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                    />
                  </div>
                </div>
              </div>

              <div className="pt-4 flex justify-between items-center border-t border-[#E5DEC9]">
                <Link to="/login" className="text-sm font-semibold text-[#2F5233] hover:underline">
                  Already have an account? Sign in
                </Link>
                <button
                  onClick={handleNextStep1}
                  className="px-6 py-3 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-sm rounded-xl shadow-xs transition-all flex items-center gap-2 cursor-pointer"
                >
                  <span>Continue to Step 2</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* STEP 2 */}
          {step === 2 && (
            <div className="space-y-6 animate-in fade-in">
              <div className="space-y-1">
                <h3 className="text-2xl font-bold text-[#1F2A1E] tracking-tight">Step 2: Personal Details & Location</h3>
                <p className="text-sm text-[#1F2A1E]/60 font-medium">Provide your contact details so verified professionals can serve you.</p>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">Full Name</label>
                  <div className="relative">
                    <User className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                    <input
                      type="text"
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      placeholder="Rahul Sharma"
                      className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-4 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">Mobile Number</label>
                  <div className="relative">
                    <Phone className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                    <input
                      type="tel"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder="+91 98765 43210"
                      className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-4 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">City</label>
                    <div className="relative">
                      <MapPin className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                      <input
                        type="text"
                        value={city}
                        onChange={(e) => setCity(e.target.value)}
                        className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-4 text-sm font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">Pincode</label>
                    <input
                      type="text"
                      value={pincode}
                      onChange={(e) => setPincode(e.target.value)}
                      className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl px-4 text-sm font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                    />
                  </div>
                </div>
              </div>

              <div className="pt-4 flex justify-between items-center border-t border-[#E5DEC9]">
                <button
                  onClick={() => setStep(1)}
                  className="px-5 py-2.5 bg-[#F2EDE1] hover:bg-[#E5DEC9] text-[#1F2A1E] font-semibold text-sm rounded-xl transition-all flex items-center gap-1.5 cursor-pointer"
                >
                  <ArrowLeft className="w-4 h-4" />
                  <span>Back</span>
                </button>
                <button
                  onClick={handleNextStep2}
                  className="px-6 py-3 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-sm rounded-xl shadow-xs transition-all flex items-center gap-2 cursor-pointer"
                >
                  <span>Select 3 Preferences</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* STEP 3 */}
          {step === 3 && (
            <div className="space-y-6 animate-in fade-in">
              <div className="space-y-1">
                <div className="flex items-center justify-between">
                  <h3 className="text-2xl font-bold text-[#1F2A1E] tracking-tight">
                    Step 3: Choose Top 3 Category Preferences
                  </h3>
                  <span className="text-xs font-bold px-3 py-1 bg-[#2F5233]/10 text-[#2F5233] border border-[#2F5233]/20 rounded-full">
                    {selectedCategoryIds.length} / 3 Selected
                  </span>
                </div>
                <p className="text-sm text-[#1F2A1E]/60 font-medium">
                  Select <strong className="text-[#1F2A1E]">exactly 3 categories</strong> you are most interested in. (Customizes your home feed with no obligation).
                </p>
              </div>

              {loadingCategories ? (
                <div className="flex flex-col items-center justify-center py-12 space-y-3">
                  <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
                  <p className="text-sm font-semibold text-[#1F2A1E]/70">Loading catalog categories from database...</p>
                </div>
              ) : (
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 max-h-[380px] overflow-y-auto pr-1">
                  {categories.map((cat) => {
                    const isSelected = selectedCategoryIds.includes(cat.id);
                    const isDisabled = selectedCategoryIds.length >= 3 && !isSelected;
                    const imgUrl = cat.image || getCategoryImageUrl(cat.name);

                    return (
                      <div
                        key={cat.id}
                        data-testid="category-card"
                        onClick={() => !isDisabled && handleToggleCategory(cat.id)}
                        className={`group relative rounded-2xl overflow-hidden border transition-all cursor-pointer select-none flex flex-col justify-between h-36 ${
                          isSelected
                            ? 'border-[#2F5233] ring-2 ring-[#2F5233]/40 shadow-xs'
                            : isDisabled
                            ? 'opacity-40 border-[#E5DEC9] cursor-not-allowed grayscale'
                            : 'border-[#E5DEC9] hover:border-[#2F5233]/50 hover:shadow-xs'
                        }`}
                      >
                        <img
                          src={imgUrl}
                          alt={cat.name}
                          className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                        <div className={`absolute inset-0 bg-gradient-to-t ${isSelected ? 'from-[#1F2A1E]/95 via-[#2F5233]/60 to-transparent' : 'from-[#1F2A1E]/80 via-[#1F2A1E]/40 to-transparent'}`} />

                        <div className="relative z-10 p-3 flex justify-between items-start">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-white/90 bg-black/40 px-2 py-0.5 rounded-full backdrop-blur-xs">
                            {cat.service_count ? `${cat.service_count} Services` : 'Verified'}
                          </span>

                          <div className={`w-6 h-6 rounded-full flex items-center justify-center transition-transform ${isSelected ? 'bg-[#2F5233] text-white scale-110 shadow-xs' : 'bg-white/30 text-white'}`}>
                            {isSelected ? <Check className="w-4 h-4 stroke-[3]" /> : <span className="text-xs font-bold">+</span>}
                          </div>
                        </div>

                        <div className="relative z-10 p-3">
                          <h4 className="font-bold text-white text-xs sm:text-sm leading-snug drop-shadow-sm">
                            {cat.name}
                          </h4>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}

              <div className="pt-4 flex justify-between items-center border-t border-[#E5DEC9]">
                <button
                  onClick={() => setStep(2)}
                  className="px-5 py-2.5 bg-[#F2EDE1] hover:bg-[#E5DEC9] text-[#1F2A1E] font-semibold text-sm rounded-xl transition-all flex items-center gap-1.5 cursor-pointer"
                >
                  <ArrowLeft className="w-4 h-4" />
                  <span>Back</span>
                </button>
                <button
                  onClick={handleNextStep3}
                  disabled={selectedCategoryIds.length !== 3}
                  className="px-6 py-3 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-sm rounded-xl shadow-xs transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 cursor-pointer"
                >
                  <span>Continue to Summary</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* STEP 4 */}
          {step === 4 && (
            <div className="space-y-6 animate-in fade-in">
              <div className="space-y-1">
                <h3 className="text-2xl font-bold text-[#1F2A1E] tracking-tight">Step 4: Review & Complete Registration</h3>
                <p className="text-sm text-[#1F2A1E]/60 font-medium">Verify your details before creating your customer account in the database.</p>
              </div>

              <div className="bg-[#FAF7F0] p-5 rounded-2xl border border-[#E5DEC9] space-y-4 text-sm">
                <div className="grid grid-cols-2 gap-4 pb-3 border-b border-[#E5DEC9]">
                  <div>
                    <span className="text-[11px] font-bold text-[#1F2A1E]/50 uppercase tracking-wider block">Full Name</span>
                    <span className="font-bold text-[#1F2A1E]">{fullName}</span>
                  </div>
                  <div>
                    <span className="text-[11px] font-bold text-[#1F2A1E]/50 uppercase tracking-wider block">Email Address</span>
                    <span className="font-bold text-[#1F2A1E]">{email}</span>
                  </div>
                  <div>
                    <span className="text-[11px] font-bold text-[#1F2A1E]/50 uppercase tracking-wider block">Mobile Phone</span>
                    <span className="font-bold text-[#1F2A1E]">{phone}</span>
                  </div>
                  <div>
                    <span className="text-[11px] font-bold text-[#1F2A1E]/50 uppercase tracking-wider block">Location</span>
                    <span className="font-bold text-[#1F2A1E]">{city} - {pincode}</span>
                  </div>
                </div>

                <div>
                  <span className="text-[11px] font-bold text-[#1F2A1E]/50 uppercase tracking-wider block mb-2">Selected Top 3 Category Preferences</span>
                  <div className="flex flex-wrap gap-2">
                    {selectedCategoryIds.map((id) => {
                      const match = categories.find((c) => c.id === id);
                      return (
                        <span key={id} className="px-3 py-1 bg-white text-[#2F5233] font-bold text-xs rounded-lg border border-[#E5DEC9] flex items-center gap-1.5 shadow-2xs">
                          <CheckCircle2 className="w-3.5 h-3.5 text-[#2F5233]" />
                          <span>{match ? match.name : id}</span>
                        </span>
                      );
                    })}
                  </div>
                </div>
              </div>

              <div className="p-4 bg-[#F2EDE1]/70 border border-[#C9A15A]/40 rounded-xl text-[#1F2A1E] text-xs font-semibold flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-[#2F5233] flex-shrink-0" />
                <span>Notice: Creating your account saves your 3 preferences. Zero service bookings have been created.</span>
              </div>

              <div className="pt-4 flex justify-between items-center border-t border-[#E5DEC9]">
                <button
                  onClick={() => setStep(3)}
                  className="px-5 py-2.5 bg-[#F2EDE1] hover:bg-[#E5DEC9] text-[#1F2A1E] font-semibold text-sm rounded-xl transition-all flex items-center gap-1.5 cursor-pointer"
                >
                  <ArrowLeft className="w-4 h-4" />
                  <span>Back</span>
                </button>
                <button
                  onClick={handleCompleteRegister}
                  disabled={loading}
                  className="px-6 py-3 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-sm rounded-xl shadow-xs transition-all disabled:opacity-70 flex items-center gap-2 cursor-pointer"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Creating Account...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4 text-[#C9A15A]" />
                      <span>Create Account & Finish</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {/* STEP 5 */}
          {step === 5 && (
            <div className="text-center py-8 space-y-6 animate-in zoom-in-95">
              <div className="w-20 h-20 bg-emerald-50 text-[#2F5233] border border-emerald-200 rounded-3xl mx-auto flex items-center justify-center shadow-xs">
                <CheckCircle2 className="w-10 h-10 text-[#2F5233]" />
              </div>
              <div className="space-y-2 max-w-md mx-auto">
                <h3 className="text-3xl font-bold text-[#1F2A1E] tracking-tight">Step 5 of 5: Welcome to SmartServe!</h3>
                <p className="text-sm text-[#1F2A1E]/70 font-medium leading-relaxed">
                  Your customer account has been created in the database and your preferences have been configured.
                </p>
              </div>

              <div className="pt-4">
                <button
                  onClick={() => navigate('/home', { replace: true })}
                  className="px-8 py-4 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-base rounded-2xl shadow-xs transition-all inline-flex items-center gap-2 cursor-pointer"
                >
                  <span>Explore Marketplace Home</span>
                  <ArrowRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default CustomerRegister;
