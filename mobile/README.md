# SmartServe Mobile Application (React Native + Expo)

A production-quality cross-platform mobile application built with **React Native** and **Expo SDK 57**, seamlessly integrated with the SmartServe FastAPI backend and PostgreSQL database.

---

## 📱 Features Overview

### 1. Unified Authentication & Role-Based Modes
- **Dual-Role Access:** Supports both **Customer** and **Service Expert (Partner)** modes within a single application.
- **Fast Demo Access:** Pre-fill buttons for Customer (`demo.customer@smartserve.com`) and Service Expert (`demo.provider@smartserve.com`).
- **Secure Token Management:** JWT access tokens securely stored using `expo-secure-store`.
- **2FA Support:** Handles two-factor authentication and single-use recovery code challenges.

### 2. Customer Experience
- **Home & Explore:** Category browsing, recommended home services, pricing, inclusions, and estimated durations.
- **Service Scheduling & Checkout:** Date & time window selection, address input with landmarks, and choice between **Cash on Delivery (COD)** and **Online UPI**.
- **Dynamic Server-Side Coupon Engine:** Real-time coupon code validation via `/api/v1/coupons/validate` with automated discount calculation.
- **Start Service OTP:** Generates and displays the customer's 6-digit Start OTP prominently on the booking confirmation and tracking screens so the customer can share it with their technician upon arrival.
- **Live Dispatch Tracking:** Step-by-step pipeline tracker (`Requested` → `Accepted` → `On The Way` → `Arrived` → `Started` → `Completed`) with live provider map updates.
- **Standardized 7-Day Labor Warranty:** Completed eligible services display the active 7-Day Warranty card with days remaining and a one-click **"Claim Free Rework"** workflow (₹0 inspection fee) calling `/api/v1/customer/bookings/{id}/warranty/claim`.
- **Offers & Spin-the-Wheel:** Gamified lucky spin wheel that mints promotional discount vouchers via `/api/v1/coupons/spin-reward` and an active coupon shelf with one-click code copy.

### 3. Service Expert Partner Portal
- **Dashboard & Statistics:** Real-time view of assigned jobs, completed services, aggregate rating, and total earnings via `/api/v1/providers/me/dashboard-stats`.
- **Job Lifecycle Operations:**
  - **"On The Way":** Marks technician en route and broadcasts live GPS dispatch to customer.
  - **"Arrived":** Notifies customer that the expert is outside their location.
  - **"Start Job":** Securely requires the customer's 6-digit Start OTP to begin work.
  - **Proof of Work Photos:** Native camera/photo picker via `expo-image-picker` uploading before-service and after-service proof photos to `/api/v1/providers/me/bookings/{id}/photos/*`.
  - **"Complete Job":** Verifies completion OTP and transitions status to `Completed`.
  - **Cash on Delivery (COD) Collection:** Modal reporting the exact cash collected and receipt note to `/api/v1/providers/me/bookings/{id}/report-cash-collected`.
- **Availability Management:** Day-by-day weekly availability toggles (09:00 AM - 06:00 PM) saved via `/api/v1/providers/me/availability`.

### 4. Internationalization & Localization (i18n)
- **Supported Languages:** English (`en`), Hindi (`hi`), Gujarati (`gu`).
- **Instant Persistence:** Language preferences persist across app restarts using `AsyncStorage`.
- **Full Coverage:** Navigation tabs, form inputs, status labels, error messages, and warranty badges localized.

---

## 🛠️ Project Structure

```
mobile/
├── App.tsx                     # Main App Entry (SafeArea, Language, Auth, ErrorBoundary)
├── app.json                    # Expo configuration
├── package.json                # Dependencies & scripts
├── src/
│   ├── api/
│   │   ├── auth.ts             # Customer & Provider authentication endpoints
│   │   ├── bookings.ts         # Booking creation, tracking & cancellation
│   │   ├── catalog.ts          # Services & categories catalog
│   │   ├── client.ts           # Axios client with SecureStore Bearer interceptor
│   │   ├── coupons.ts          # Coupon validation & Spin-the-Wheel reward minting
│   │   ├── provider.ts         # Provider jobs, OTP verification, photos & COD reporting
│   │   └── warranty.ts         # Standardized 7-day warranty retrieval & claim filing
│   ├── components/
│   │   ├── common/             # ErrorBoundary, SplashScreen
│   │   └── MobileLiveMap.tsx   # Live Leaflet/WebView technician map
│   ├── config/
│   │   └── api.ts              # Intelligent multi-device API Base URL resolver
│   ├── context/
│   │   └── AuthContext.tsx     # Role-aware authentication context & SecureStore
│   ├── i18n/
│   │   ├── translations.ts     # EN, HI, GU dictionary mappings
│   │   └── LanguageContext.tsx # Language state provider & t() hook
│   ├── navigation/
│   │   ├── AppNavigator.tsx    # Root navigation switcher (Auth vs Customer vs Provider)
│   │   └── ProviderNavigator.tsx # Dedicated Provider tabs & stack
│   ├── screens/
│   │   ├── HomeScreen.tsx
│   │   ├── CatalogScreen.tsx
│   │   ├── ServiceListScreen.tsx
│   │   ├── ServiceDetailScreen.tsx
│   │   ├── BookingModalScreen.tsx       # Scheduling, COD/Online & server-side coupon validation
│   │   ├── BookingsListScreen.tsx      # All bookings, Start OTP pills & 7-day warranty claim button
│   │   ├── LiveTrackingScreen.tsx      # Live GPS dispatch tracking & OTP view
│   │   ├── OffersScreen.tsx            # Spin-the-Wheel game & active coupon shelf
│   │   ├── WarrantyClaimModalScreen.tsx# Free rework claim submission (7-day policy)
│   │   ├── ProfileScreen.tsx           # Profile info, language toggle & role mode switcher
│   │   ├── LoginScreen.tsx             # Dual-role sign in with demo shortcuts
│   │   ├── SignupScreen.tsx            # Customer registration
│   │   └── provider/
│   │       ├── ProviderDashboardScreen.tsx   # Metrics & assigned jobs feed
│   │       ├── ProviderJobDetailScreen.tsx   # OTP verification, photo uploads & cash reporting
│   │       └── ProviderAvailabilityScreen.tsx# Weekly schedule toggles
│   └── utils/
│       ├── formatters.ts       # Currency (₹) & category formatters
│       ├── secureStore.ts      # Hardware-backed SecureStore wrapper
│       └── serviceImages.ts    # Unsplash category imagery resolver
```

---

## ⚙️ Network Configuration

The app includes an intelligent automatic Base URL resolver in `src/config/api.ts`:
1. **Explicit `.env`:** Reads `EXPO_PUBLIC_API_BASE_URL` if defined.
2. **Physical Device (Expo Go):** Automatically detects the PC's host IP from Metro (`Constants.expoConfig?.hostUri`).
3. **Android Emulator:** Automatically defaults to `http://10.0.2.2:8000/api/v1`.
4. **iOS Simulator:** Automatically defaults to `http://127.0.0.1:8000/api/v1`.
5. **Fallback LAN IP:** Points to the developer PC's LAN IP (`http://172.20.10.2:8000/api/v1`).

---

## 🚀 How to Run Locally

### 1. Ensure Backend is Running
Verify that the FastAPI backend is listening on port 8000:
```powershell
cd backend
.\venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start Expo Metro Bundler
```powershell
cd mobile
npm start
```

### 3. Open on Device or Emulator
- **Physical Phone (Android/iOS):** Open the **Expo Go** app and scan the QR code displayed in the terminal. (Ensure your phone is connected to the same Wi-Fi network as your PC).
- **Android Emulator:** Press `a` in the terminal.
- **iOS Simulator:** Press `i` in the terminal.
- **Web Preview:** Press `w` in the terminal.

---

## 🧪 Testing & Verification
- **TypeScript Typecheck:** `npx.cmd tsc --noEmit` (passes with 0 errors).
- **Backend API Integration:** Fully connected to live FastAPI endpoints:
  - `POST /api/v1/customer/auth/login` & `POST /api/v1/auth/login`
  - `GET /api/v1/customer/catalog/services`
  - `POST /api/v1/coupons/validate` & `POST /api/v1/coupons/spin-reward`
  - `POST /api/v1/customer/bookings` & `GET /api/v1/customer/bookings`
  - `GET /api/v1/customer/bookings/{id}/warranty` & `POST .../warranty/claim`
  - `POST /api/v1/providers/me/bookings/{id}/start` & `POST .../complete`
  - `POST /api/v1/providers/me/bookings/{id}/photos/before` & `.../photos/after`
  - `POST /api/v1/providers/me/bookings/{id}/report-cash-collected`

