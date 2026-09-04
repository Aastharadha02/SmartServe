# SmartServe — Customer Web Application (`customer-frontend`)

[![CI](https://github.com/PushkarKanjani/SmartServe/actions/workflows/customer-frontend-ci.yml/badge.svg)](../../actions/workflows/customer-frontend-ci.yml)

The **Customer Web Application** for SmartServe is a production-grade, responsive customer-facing web dashboard built with React 18, TypeScript (strict mode, zero `any`), Vite, and Tailwind CSS. It visually and architecturally matches the existing SmartServe **Admin Dashboard**, consumes the FastAPI backend at `/api/v1/`, and maintains data-model parity with the Expo / React Native **Mobile App**.

---

## Tech Stack & Safety Net

- **Core UI Framework:** React 18 (with React Router DOM v7)
- **Language:** TypeScript 5.7 (Strict Mode, `noImplicitAny: true`, `noUncheckedIndexedAccess: true`)
- **Build Tool:** Vite 6
- **Styling:** Tailwind CSS v4 + `@tailwindcss/vite`
- **Testing & Safety Net:** Playwright (`@playwright/test`) E2E test suite (9 spec files)
- **CI/CD:** GitHub Actions pipeline (`customer-frontend-ci.yml` quality, build & E2E jobs)
- **HTTP Client:** Axios with JWT request & 401 response interceptors
- **Locale & Currency:** Indian Rupee (₹) via `Intl.NumberFormat('en-IN')`

---

## Setup & Running Locally

### 1. Prerequisites
- Node.js ≥ 18.x
- npm ≥ 9.x

### 2. Installation
```bash
cd customer-frontend

# Copy environment template
cp .env.example .env

# Install dependencies & Playwright browsers
npm install
npm run test:e2e:install
```

### 3. Run Development Server
```bash
npm run dev
```
The application will launch on **http://localhost:5174**.

### 4. Build, Typecheck & E2E Tests
```bash
# Run TypeScript type check
npm run typecheck

# Production build
npm run build

# Preview production bundle
npm run preview

# Run Playwright E2E Test Suite
npm run test:e2e
```

---

## Backend Connection Status & Mock Resilience

The customer frontend features a dev-only connection pulse indicator (`BackendStatusBadge`) that polls `/health` and customer endpoint availability every 60s via `useBackendStatus()`.

- 🟢 **`Backend Live (7/7 Endpoints)`**: All customer routes deployed and live.
- 🟡 **`Backend Live (X/7 Endpoints — Mock Fallback Active)`**: Partial backend deployment; frontend transparently uses mock fallbacks for missing routes.
- 🔴 **`Backend Unreachable — Mock Active`**: Backend offline/404; full mock fallback mode active.

> See [`INTEGRATION.md`](./INTEGRATION.md) and [`INTEGRATION_CHECKLIST.md`](./INTEGRATION_CHECKLIST.md) for the exact backend hand-off contract.

---

## Directory Structure

```
customer-frontend/
├── .env.example
├── .env
├── index.html
├── package.json
├── playwright.config.ts          # Playwright test runner configuration
├── INTEGRATION.md                # Full backend hand-off contract for Aastha
├── INTEGRATION_CHECKLIST.md      # Printable integration sign-off checklist
├── HANDOFF.md                    # Deployment hand-off report
├── e2e/                          # Playwright E2E spec files
│   ├── 01-auth.spec.ts
│   ├── 02-app-shell.spec.ts
│   ├── 03-discover.spec.ts
│   ├── 04-service-detail.spec.ts
│   ├── 05-booking-flow.spec.ts
│   ├── 06-support-flow.spec.ts
│   ├── 07-profile.spec.ts
│   ├── 08-design-tokens.spec.ts
│   └── 09-mobile-responsive.spec.ts
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── index.css
    ├── api/
    │   ├── client.ts              # Axios instance & JWT interceptors
    │   ├── health.ts              # Backend health pulse check
    │   ├── auth.ts                # Auth API endpoints
    │   ├── customer.ts            # Profile read/update
    │   ├── catalog.ts             # Service catalog & discovery
    │   ├── bookings.ts            # Booking creation & tracking
    │   ├── support.ts             # Support tickets & helpdesk
    │   ├── sessions.ts           # Active sessions management
    │   └── uploads.ts             # Image evidence handler
    ├── hooks/
    │   ├── useToast.ts
    │   └── useBackendStatus.ts    # Polling hook for backend health
    ├── components/
    │   ├── common/
    │   │   ├── ErrorBoundary.tsx
    │   │   ├── SplashScreen.tsx
    │   │   └── BackendStatusBadge.tsx # Dev-only connection indicator
    │   ├── ui/                    # Atomic design primitives
    │   ├── layout/                # App shell, header, sidebar
    │   ├── customer/              # Discovery components
    │   ├── booking/               # Booking components
    │   └── support/               # Support components
    └── pages/                     # Lazy-loaded page components
```

---

## API Contract Summary

The customer web app communicates with the following endpoints under `/api/v1/`:

| Endpoint | Method | Purpose |
|---|---|---|
| `/customer/auth/register` | POST | Register new customer account |
| `/customer/auth/login` | POST | Customer authentication login |
| `/customer/auth/me` | GET | Fetch current customer session |
| `/customer/auth/logout` | POST | Revoke current token session |
| `/customer/auth/forgot-password` | POST | Trigger password reset link |
| `/customer/auth/reset-password` | POST | Confirm new password reset |
| `/customer/catalog/categories` | GET | List service categories with counts |
| `/customer/catalog/services` | GET | Fetch paginated services with search & filters |
| `/customer/catalog/services/{id}` | GET | Fetch single service details, add-ons, FAQs |
| `/customer/bookings` | GET / POST | List customer bookings or create new booking |
| `/customer/bookings/{id}` | GET | Fetch single booking detail & timeline |
| `/customer/bookings/{id}/cancel` | POST | Cancel requested/assigned booking |
| `/customer/bookings/{id}/feedback` | POST | Submit rating & review for completed booking |
| `/customer/support/tickets` | GET / POST | List or create customer support tickets |
| `/customer/support/tickets/{id}` | GET | Support ticket detail & conversation thread |
| `/customer/support/tickets/{id}/messages` | POST | Post customer reply to support ticket |
| `/customer/profile` | GET / PATCH | Read or update customer profile details |
| `/customer/sessions` | GET | List active login sessions |
| `/customer/sessions/{id}/revoke` | POST | Revoke a single active login session |
| `/customer/sessions/revoke-all` | POST | Revoke all other active sessions |

---

## Mobile Parity & Cross-Platform Notes

- **Token Storage:** Customer Web uses `localStorage.setItem('smartserve_customer_token', ...)` while RN Expo app uses `AsyncStorage`. Both consume identical JWT token payloads from the backend.
- **Type Compatibility:** `BookingItem`, `ServiceItem`, `SupportTicket`, `FeedbackPayload` field structures match the React Native app's `mobile/src/api/...` definitions.
- **Code Extraction:** All browser-specific calls (`localStorage`, `window.location`) are annotated with `// platform:web` comments to simplify future React Native Web code sharing.

---

## Known Limitations / Future Work (V1.1)

1. **Backend Integration:** Customer backend endpoints under `/api/v1/customer/*` are currently mocked using client fallbacks until Aastha ships backend routes. See [`INTEGRATION.md`](./INTEGRATION.md) for the migration plan.
2. **AI Recommendations:** Endpoints (`/api/v1/customer/recommendations`) are scaffolded in UI (`RecommendedRow.tsx`). When backend AI models land, the UI will automatically consume real recommendations.
3. **WebSockets / Real-Time:** V1 relies on window focus polling and manual refresh for real-time status updates.
4. **Payment Modes:** Locked to Cash on Delivery (COD) for V1 per product specification.
