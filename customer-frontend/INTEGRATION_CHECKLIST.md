# Customer Backend — Integration Checklist

For each endpoint below, mark ✅ when shipped, paste the live response sample, and re-run the E2E suite with `VITE_USE_MOCK_AUTH=false` to verify.

---

## Phase A — Auth (Unblocks Everything)
- [ ] `POST /api/v1/customer/auth/register` — Register customer
- [ ] `POST /api/v1/customer/auth/login` — Login & return JWT
- [ ] `GET  /api/v1/customer/auth/me` — Read current session profile
- [ ] `POST /api/v1/customer/auth/logout` — Revoke token session
- [ ] `POST /api/v1/customer/auth/forgot-password` — Send reset token
- [ ] `POST /api/v1/customer/auth/reset-password` — Confirm new password

---

## Phase B — Public Catalog
- [ ] `GET  /api/v1/customer/catalog/categories` — Category list with counts
- [ ] `GET  /api/v1/customer/catalog/services` — Filtered & searchable services
- [ ] `GET  /api/v1/customer/catalog/services/{id}` — Single service + add-ons & FAQs

---

## Phase C — Bookings Engine
- [ ] `GET  /api/v1/customer/bookings` — Customer booking history
- [ ] `POST /api/v1/customer/bookings` — Create new booking request
- [ ] `GET  /api/v1/customer/bookings/{id}` — Booking detail & timeline
- [ ] `POST /api/v1/customer/bookings/{id}/cancel` — Cancel requested/assigned booking
- [ ] `POST /api/v1/customer/bookings/{id}/feedback` — Submit rating & review

---

## Phase D — Support, Profile, Sessions & Uploads
- [ ] `GET  /api/v1/customer/support/tickets` — List customer support tickets
- [ ] `POST /api/v1/customer/support/tickets` — Create support ticket
- [ ] `GET  /api/v1/customer/support/tickets/{id}` — Ticket detail & messages
- [ ] `POST /api/v1/customer/support/tickets/{id}/messages` — Reply to ticket
- [ ] `GET  /api/v1/customer/profile` — Read customer profile stats
- [ ] `PATCH /api/v1/customer/profile` — Update name, email, phone
- [ ] `GET  /api/v1/customer/sessions` — Active login sessions list
- [ ] `POST /api/v1/customer/sessions/{id}/revoke` — Revoke single session
- [ ] `POST /api/v1/customer/sessions/revoke-all` — Revoke all other sessions
- [ ] `POST /api/v1/customer/uploads/image` — Upload image evidence

---

## Final Production Sign-off
- [ ] Set `VITE_USE_MOCK_AUTH=false` in production deployment environment
- [ ] Run full Playwright E2E suite (`npm run test:e2e`) — All spec files green
- [ ] Verify static site deployment on Render
