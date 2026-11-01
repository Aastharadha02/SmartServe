export type SupportedLanguage = 'en' | 'hi' | 'gu';

export interface Translations {
  // Navigation
  nav_home: string;
  nav_services: string;
  nav_bookings: string;
  nav_offers: string;
  nav_support: string;
  nav_profile: string;
  nav_provider_jobs: string;
  nav_provider_schedule: string;
  nav_provider_earnings: string;

  // General
  app_name: string;
  loading: string;
  error: string;
  retry: string;
  save: string;
  cancel: string;
  confirm: string;
  back: string;
  close: string;
  submit: string;
  success: string;
  language: string;

  // Auth
  auth_login_title: string;
  auth_signup_title: string;
  auth_email: string;
  auth_password: string;
  auth_full_name: string;
  auth_phone: string;
  auth_role_customer: string;
  auth_role_provider: string;
  auth_login_btn: string;
  auth_signup_btn: string;
  auth_logout_btn: string;
  auth_no_account: string;
  auth_have_account: string;

  // Customer Home & Catalog
  home_greeting: string;
  home_subtitle: string;
  home_search_placeholder: string;
  home_popular_categories: string;
  home_recommended: string;
  home_special_offer: string;
  service_duration: string;
  service_price: string;
  service_book_now: string;
  service_inclusions: string;

  // Booking Flow
  booking_checkout_title: string;
  booking_date: string;
  booking_time: string;
  booking_address: string;
  booking_payment_method: string;
  booking_cod: string;
  booking_online: string;
  booking_apply_coupon: string;
  booking_coupon_placeholder: string;
  booking_bundle_discount: string;
  booking_total: string;
  booking_confirm_button: string;
  booking_success_msg: string;

  // OTP & Tracking
  otp_start_label: string;
  otp_start_instruction: string;
  otp_completion_label: string;
  live_tracking_title: string;
  status_pending: string;
  status_assigned: string;
  status_on_the_way: string;
  status_arrived: string;
  status_in_progress: string;
  status_completed: string;
  status_cancelled: string;

  // Warranty
  warranty_title: string;
  warranty_badge: string;
  warranty_desc: string;
  warranty_days_remaining: string;
  warranty_claim_btn: string;
  warranty_claim_title: string;
  warranty_issue_desc: string;
  warranty_submit_claim: string;
  warranty_free_rework: string;

  // Offers
  offers_title: string;
  spin_wheel_title: string;
  spin_wheel_btn: string;
  spin_wheel_win_msg: string;
  active_coupons: string;
  copy_coupon: string;
  copied: string;

  // Provider
  provider_dashboard: string;
  provider_active_jobs: string;
  provider_start_job: string;
  provider_enter_start_otp: string;
  provider_complete_job: string;
  provider_enter_completion_otp: string;
  provider_upload_before_photo: string;
  provider_upload_after_photo: string;
  provider_report_cash: string;
  provider_cash_amount: string;
  provider_receipt_number: string;
  provider_availability: string;
  switch_to_provider: string;
  switch_to_customer: string;
}

export const translations: Record<SupportedLanguage, Translations> = {
  en: {
    nav_home: 'Home',
    nav_services: 'Services',
    nav_bookings: 'Bookings',
    nav_offers: 'Offers',
    nav_support: 'Support',
    nav_profile: 'Profile',
    nav_provider_jobs: 'Jobs',
    nav_provider_schedule: 'Schedule',
    nav_provider_earnings: 'Earnings',

    app_name: 'SmartServe',
    loading: 'Loading...',
    error: 'Something went wrong',
    retry: 'Retry',
    save: 'Save',
    cancel: 'Cancel',
    confirm: 'Confirm',
    back: 'Back',
    close: 'Close',
    submit: 'Submit',
    success: 'Success',
    language: 'Language',

    auth_login_title: 'Welcome Back',
    auth_signup_title: 'Create Account',
    auth_email: 'Email Address',
    auth_password: 'Password',
    auth_full_name: 'Full Name',
    auth_phone: 'Phone Number',
    auth_role_customer: 'Customer',
    auth_role_provider: 'Service Expert',
    auth_login_btn: 'Sign In',
    auth_signup_btn: 'Create Account',
    auth_logout_btn: 'Sign Out',
    auth_no_account: "Don't have an account? Sign up",
    auth_have_account: 'Already have an account? Sign in',

    home_greeting: 'Find Reliable Experts',
    home_subtitle: 'For all your home service needs',
    home_search_placeholder: 'Search AC repair, cleaning, plumbing...',
    home_popular_categories: 'Popular Categories',
    home_recommended: 'Recommended Services',
    home_special_offer: 'Special Discount Available',
    service_duration: 'mins',
    service_price: '₹',
    service_book_now: 'Book Now',
    service_inclusions: "What's Included",

    booking_checkout_title: 'Checkout & Schedule',
    booking_date: 'Select Date',
    booking_time: 'Select Time Slot',
    booking_address: 'Service Address',
    booking_payment_method: 'Payment Method',
    booking_cod: 'Cash on Delivery (Pay after service)',
    booking_online: 'Pay Online',
    booking_apply_coupon: 'Apply Coupon',
    booking_coupon_placeholder: 'Enter coupon code',
    booking_bundle_discount: 'Bundle Discount Applied',
    booking_total: 'Total Amount',
    booking_confirm_button: 'Confirm & Place Booking',
    booking_success_msg: 'Booking placed successfully!',

    otp_start_label: 'Start Service OTP',
    otp_start_instruction: 'Share this 6-digit code with your provider once they arrive.',
    otp_completion_label: 'Completion OTP',
    live_tracking_title: 'Service Tracking',
    status_pending: 'Confirmed',
    status_assigned: 'Expert Assigned',
    status_on_the_way: 'On The Way',
    status_arrived: 'Arrived at Location',
    status_in_progress: 'Work In Progress',
    status_completed: 'Completed',
    status_cancelled: 'Cancelled',

    warranty_title: '7-Day Service Warranty',
    warranty_badge: '7-Day Warranty',
    warranty_desc: 'Guaranteed 7-day free rework if you face any issues after completion.',
    warranty_days_remaining: 'days remaining',
    warranty_claim_btn: 'Claim Free Rework',
    warranty_claim_title: 'Submit Warranty Claim',
    warranty_issue_desc: 'Describe what needs attention',
    warranty_submit_claim: 'Submit Free Rework Request',
    warranty_free_rework: 'Free Rework Cover (₹0 Fee)',

    offers_title: 'Offers & Rewards',
    spin_wheel_title: 'Spin & Win Rewards',
    spin_wheel_btn: 'Spin the Wheel',
    spin_wheel_win_msg: 'Congratulations! You unlocked a discount!',
    active_coupons: 'Active Coupons',
    copy_coupon: 'Copy Code',
    copied: 'Copied!',

    provider_dashboard: 'Partner Dashboard',
    provider_active_jobs: 'Assigned Jobs',
    provider_start_job: 'Start Job (Verify OTP)',
    provider_enter_start_otp: 'Enter Customer Start OTP',
    provider_complete_job: 'Complete Job (Verify OTP)',
    provider_enter_completion_otp: 'Enter Customer Completion OTP',
    provider_upload_before_photo: 'Upload Before-Work Photo',
    provider_upload_after_photo: 'Upload After-Work Photo',
    provider_report_cash: 'Report Cash Collected',
    provider_cash_amount: 'Amount Collected (₹)',
    provider_receipt_number: 'Receipt Number / Note',
    provider_availability: 'Manage Weekly Availability',
    switch_to_provider: 'Switch to Partner Mode',
    switch_to_customer: 'Switch to Customer Mode',
  },

  hi: {
    nav_home: 'होम',
    nav_services: 'सेवाएं',
    nav_bookings: 'बुकिंग्स',
    nav_offers: 'ऑफ़र्स',
    nav_support: 'सहायता',
    nav_profile: 'प्रोफ़ाइल',
    nav_provider_jobs: 'कार्य',
    nav_provider_schedule: 'शेड्यूल',
    nav_provider_earnings: 'कमाई',

    app_name: 'स्मार्टसर्व',
    loading: 'लोड हो रहा है...',
    error: 'कुछ गड़बड़ हुई',
    retry: 'पुनः प्रयास करें',
    save: 'सहेजें',
    cancel: 'रद्द करें',
    confirm: 'पुष्टि करें',
    back: 'वापस',
    close: 'बंद करें',
    submit: 'जमा करें',
    success: 'सफल',
    language: 'भाषा',

    auth_login_title: 'स्वागत है',
    auth_signup_title: 'खाता बनाएं',
    auth_email: 'ईमेल पता',
    auth_password: 'पासवर्ड',
    auth_full_name: 'पूरा नाम',
    auth_phone: 'फ़ोन नंबर',
    auth_role_customer: 'ग्राहक',
    auth_role_provider: 'सेवा विशेषज्ञ',
    auth_login_btn: 'साइन इन करें',
    auth_signup_btn: 'खाता बनाएं',
    auth_logout_btn: 'साइन आउट',
    auth_no_account: 'खाता नहीं है? साइन अप करें',
    auth_have_account: 'पहले से खाता है? साइन इन करें',

    home_greeting: 'विश्वसनीय विशेषज्ञ खोजें',
    home_subtitle: 'आपकी सभी घरेलू सेवाओं के लिए',
    home_search_placeholder: 'एसी रिपेयर, सफाई, प्लंबिंग खोजें...',
    home_popular_categories: 'लोकप्रिय श्रेणियां',
    home_recommended: 'अनुशंसित सेवाएं',
    home_special_offer: 'विशेष छूट उपलब्ध',
    service_duration: 'मिनट',
    service_price: '₹',
    service_book_now: 'अभी बुक करें',
    service_inclusions: 'शामिल सुविधाएं',

    booking_checkout_title: 'चेकआउट और शेड्यूल',
    booking_date: 'तारीख चुनें',
    booking_time: 'समय स्लॉट चुनें',
    booking_address: 'सेवा का पता',
    booking_payment_method: 'भुगतान विधि',
    booking_cod: 'कैश ऑन डिलीवरी (काम के बाद भुगतान)',
    booking_online: 'ऑनलाइन भुगतान',
    booking_apply_coupon: 'कूपन लागू करें',
    booking_coupon_placeholder: 'कूपन कोड दर्ज करें',
    booking_bundle_discount: 'बंडल छूट लागू',
    booking_total: 'कुल राशि',
    booking_confirm_button: 'बुकिंग की पुष्टि करें',
    booking_success_msg: 'बुकिंग सफलतापूर्वक हो गई!',

    otp_start_label: 'सेवा प्रारंभ ओटीपी',
    otp_start_instruction: 'विशेषज्ञ के आने पर यह 6-अंकों का कोड उनके साथ साझा करें।',
    otp_completion_label: 'समापन ओटीपी',
    live_tracking_title: 'लाइव ट्रैकिंग',
    status_pending: 'पुष्टित',
    status_assigned: 'विशेषज्ञ नियुक्त',
    status_on_the_way: 'रास्ते में हैं',
    status_arrived: 'पहुंच चुके हैं',
    status_in_progress: 'कार्य प्रगति पर है',
    status_completed: 'पूर्ण हुआ',
    status_cancelled: 'रद्द किया गया',

    warranty_title: '7-दिवसीय सेवा वारंटी',
    warranty_badge: '7-दिन वारंटी',
    warranty_desc: 'समापन के बाद 7 दिनों तक मुफ़्त पुनः कार्य (रिवर्क) गारंटी।',
    warranty_days_remaining: 'दिन शेष',
    warranty_claim_btn: 'मुफ़्त रिवर्क का दावा करें',
    warranty_claim_title: 'वारंटी दावा प्रस्तुत करें',
    warranty_issue_desc: 'समस्या का विवरण दें',
    warranty_submit_claim: 'दावा जमा करें',
    warranty_free_rework: 'मुफ़्त रिवर्क कवर (₹0 शुल्क)',

    offers_title: 'ऑफ़र्स और पुरस्कार',
    spin_wheel_title: 'चक्र घुमाएं और जीतें',
    spin_wheel_btn: 'स्पिन करें',
    spin_wheel_win_msg: 'बधाई हो! आपको छूट मिली!',
    active_coupons: 'सक्रिय कूपन',
    copy_coupon: 'कोड कॉपी करें',
    copied: 'कॉपी हो गया!',

    provider_dashboard: 'पार्टनर डैशबोर्ड',
    provider_active_jobs: 'आवंटित कार्य',
    provider_start_job: 'कार्य शुरू करें (ओटीपी सत्यापित करें)',
    provider_enter_start_otp: 'ग्राहक का स्टार्ट ओटीपी दर्ज करें',
    provider_complete_job: 'कार्य समाप्त करें (ओटीपी सत्यापित करें)',
    provider_enter_completion_otp: 'ग्राहक का समाप्ति ओटीपी दर्ज करें',
    provider_upload_before_photo: 'कार्य पूर्व की फोटो अपलोड करें',
    provider_upload_after_photo: 'कार्य पश्चात की फोटो अपलोड करें',
    provider_report_cash: 'प्राप्त नकद रिपोर्ट करें',
    provider_cash_amount: 'प्राप्त राशि (₹)',
    provider_receipt_number: 'रसीद संख्या / टिप्पणी',
    provider_availability: 'साप्ताहिक उपलब्धता प्रबंधित करें',
    switch_to_provider: 'पार्टनर मोड में जाएं',
    switch_to_customer: 'ग्राहक मोड में जाएं',
  },

  gu: {
    nav_home: 'હોમ',
    nav_services: 'સેવાઓ',
    nav_bookings: 'બુકિંગ',
    nav_offers: 'ઑફર્સ',
    nav_support: 'સહાય',
    nav_profile: 'પ્રોફાઇલ',
    nav_provider_jobs: 'કામગીરી',
    nav_provider_schedule: 'સમયપત્રક',
    nav_provider_earnings: 'કમાણી',

    app_name: 'સ્માર્ટસર્વ',
    loading: 'લોડ થઈ રહ્યું છે...',
    error: 'કંઈક ખોટું થયું',
    retry: 'ફરી પ્રયાસ કરો',
    save: 'સાચવો',
    cancel: 'રદ કરો',
    confirm: 'પુષ્ટિ કરો',
    back: 'પાછા જાઓ',
    close: 'બંધ કરો',
    submit: 'સબમિટ કરો',
    success: 'સફળ',
    language: 'ભાષા',

    auth_login_title: 'સ્વાગત છે',
    auth_signup_title: 'ખાતું બનાવો',
    auth_email: 'ઈમેલ એડ્રેસ',
    auth_password: 'પાસવર્ડ',
    auth_full_name: 'પૂરું નામ',
    auth_phone: 'ફોન નંબર',
    auth_role_customer: 'ગ્રાહક',
    auth_role_provider: 'સેવા નિષ્ણાત',
    auth_login_btn: 'સાઇન ઇન',
    auth_signup_btn: 'ખાતું બનાવો',
    auth_logout_btn: 'સાઇન આઉટ',
    auth_no_account: 'ખાતું નથી? સાઇન અપ કરો',
    auth_have_account: 'પહેલેથી ખાતું છે? સાઇન ઇન કરો',

    home_greeting: 'વિશ્વસનીય નિષ્ણાતો શોધો',
    home_subtitle: 'તમારી ઘરની તમામ સેવાઓ માટે',
    home_search_placeholder: 'એસી રિપેર, સફાઈ, પ્લમ્બિંગ શોધો...',
    home_popular_categories: 'લોકપ્રિય શ્રેણીઓ',
    home_recommended: 'ભલામણ કરેલ સેવાઓ',
    home_special_offer: 'વિશેષ ડિસ્કાઉન્ટ ઉપલબ્ધ',
    service_duration: 'મિનિટ',
    service_price: '₹',
    service_book_now: 'હમણાં બુક કરો',
    service_inclusions: 'સમાવિષ્ટ સેવાઓ',

    booking_checkout_title: 'ચેકઆઉટ અને શેડ્યૂલ',
    booking_date: 'તારીખ પસંદ કરો',
    booking_time: 'સમય પસંદ કરો',
    booking_address: 'સેવાનું સરનામું',
    booking_payment_method: 'ચુકવણી પદ્ધતિ',
    booking_cod: 'કેશ ઓન ડિલિવરી (કામ પૂરું થયા પછી ચૂકવો)',
    booking_online: 'ઓનલાઇન ચુકવણી',
    booking_apply_coupon: 'કૂપન લાગુ કરો',
    booking_coupon_placeholder: 'કૂપન કોડ દાખલ કરો',
    booking_bundle_discount: 'બંડલ ડિસ્કાઉન્ટ લાગુ',
    booking_total: 'કુલ રકમ',
    booking_confirm_button: 'બુકિંગ કન્ફર્મ કરો',
    booking_success_msg: 'બુકિંગ સફળતાપૂર્વક થઈ ગયું!',

    otp_start_label: 'સેવા શરૂ કરવાનો OTP',
    otp_start_instruction: 'જ્યારે નિષ્ણાત તમારા સ્થાને પહોંચે ત્યારે આ 6-અંકનો કોડ આપો.',
    otp_completion_label: 'સમાપ્તિ OTP',
    live_tracking_title: 'લાઈવ ટ્રેકિંગ',
    status_pending: 'કન્ફર્મ થયેલ',
    status_assigned: 'નિષ્ણાત ફાળવેલ',
    status_on_the_way: 'રસ્તામાં છે',
    status_arrived: 'પહોંચી ગયા છે',
    status_in_progress: 'કામ ચાલુ છે',
    status_completed: 'પૂર્ણ થયું',
    status_cancelled: 'રદ કરવામાં આવ્યું',

    warranty_title: '7-દિવસીય સેવા વોરંટી',
    warranty_badge: '7-દિવસ વોરંટી',
    warranty_desc: 'કામ પૂર્ણ થયા પછી 7 દિવસ સુધી વિનામૂલ્યે રીવર્ક સુરક્ષા.',
    warranty_days_remaining: 'દિવસ બાકી',
    warranty_claim_btn: 'ફ્રી રીવર્ક મેળવો',
    warranty_claim_title: 'વોરંટી ક્લેમ કરો',
    warranty_issue_desc: 'સમસ્યાનું વર્ણન કરો',
    warranty_submit_claim: 'ક્લેમ સબમિટ કરો',
    warranty_free_rework: 'ફ્રી રીવર્ક સુરક્ષા (₹0 ફી)',

    offers_title: 'ઑફર્સ અને ઇનામો',
    spin_wheel_title: 'સ્પિન કરો અને જીતો',
    spin_wheel_btn: 'સ્પિન કરો',
    spin_wheel_win_msg: 'અભિનંદન! તમને ડિસ્કાઉન્ટ મળ્યું!',
    active_coupons: 'સક્રિય કૂપન્સ',
    copy_coupon: 'કોડ કોપી કરો',
    copied: 'કોપી થઈ ગયું!',

    provider_dashboard: 'પાર્ટનર ડેશબોર્ડ',
    provider_active_jobs: 'સોંપાયેલ કામગીરી',
    provider_start_job: 'કામ શરૂ કરો (OTP ચકાસો)',
    provider_enter_start_otp: 'ગ્રાહકનો સ્ટાર્ટ OTP દાખલ કરો',
    provider_complete_job: 'કામ પૂરું કરો (OTP ચકાસો)',
    provider_enter_completion_otp: 'ગ્રાહકનો કમ્પ્લીશન OTP દાખલ કરો',
    provider_upload_before_photo: 'કામ પહેલાંનો ફોટો અપલોડ કરો',
    provider_upload_after_photo: 'કામ પછીનો ફોટો અપલોડ કરો',
    provider_report_cash: 'રોકડ રકમ રિપોર્ટ કરો',
    provider_cash_amount: 'મેળવેલ રોકડ (₹)',
    provider_receipt_number: 'રસીદ નંબર / નોંધ',
    provider_availability: 'સાપ્તાહિક ઉપલબ્ધતા ગોઠવો',
    switch_to_provider: 'પાર્ટનર મોડ પર જાઓ',
    switch_to_customer: 'ગ્રાહક મોડ પર જાઓ',
  },
};

