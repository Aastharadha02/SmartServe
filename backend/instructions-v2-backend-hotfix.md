# SmartServe — Backend Stabilization & Customer Integration Reconciliation
## Master Build Instructions for Antigravity (AG) — v2

**Supersedes:** `instructions.md` (v1, "build the customer frontend"). Do not resume that work until Phase A below is complete — v1 assumed a stable, secure backend that no longer exists on `main`.

**Repo:** https://github.com/PushkarKanjani/SmartServe · **Team:** Pushkar Kanjani, Aastha (`Aastharadha02`)

Read this whole document before touching code. It is based on a direct audit of `main` at commit `55997d7` and a full branch/commit graph pull, not a guess.

---

## 1. What Changed and Why This Prompt Exists

On **2026-09-02**, Aastha pushed `55997d7 "fix: connect customer routes to production backend"` directly to `main`. It's a 41-file, ~2,800-line change. It does add real customer functionality (`backend/app/api/v1/customer.py`, 904 lines, 28 endpoints, with genuine `Customer`/`Booking`/`SupportTicket`/`TicketMessage`/`BookingFeedback` models and persistence) — that part is real progress and should be kept. But in the process it rewired `app/core/dependencies.py`, `app/core/security.py`, `app/api/v1/providers.py`, and the model layer in ways that **broke authentication for the entire platform and deleted or shadowed existing admin functionality**. This is not a customer-scope problem anymore; it's a whole-backend stability and security problem, and it's already on `main`.

Separately, there is unmerged work sitting on branches that never landed: `feat/customer-backend-routes`, `feat/customer-frontend-integration`, `feat/admin-customer-feedback-view`, `chore/integration-tests-and-docs` / `release/v1.0-customer-frontend` (all authored by Pushkar Kanjani, 2026-09-01), plus older `feature/provider-domain`, `feature/frontend-shell`, `feature/ui-light-theme`. Some of this may be a cleaner version of the same customer work that later got redone (differently, and worse in places) directly on `main`. **Diff these branches against current `main` before writing new code** — you may be able to recover better implementations of some of what's broken rather than rewriting from scratch.

---

## 2. Phase A — Stop the Bleeding (do this first, nothing else until it's done)

### A.1 Fix authentication — this is the highest priority item in the entire project
`app/core/dependencies.py`'s `get_current_user()` currently does this:
```python
if auth and auth.credentials:
    token = auth.credentials
    if "admin" in token:
        return AuthUser(id=..., role="admin", ...)   # fabricated, not verified
    elif "customer" in token:
        return AuthUser(id=..., role="customer", ...)  # fabricated, not verified
    else:
        return DUMMY_PROVIDER
return DUMMY_PROVIDER
```
It never decodes or verifies the JWT against anything. Any bearer token containing the substring `"admin"` grants admin access. Replace this with real verification: decode the token via `decode_access_token` (or restore JWT-based `verify_access_token` — see A.2), extract `sub`, look up the real `User` row, check `is_active`, and return that. No request without a valid, signed, non-expired token should ever reach a role check. `require_admin` must reject the request outright (401/403) when no valid admin user is resolved — it must never fall back to "any admin row in the table" or silently create one. Delete that fallback logic entirely.

### A.2 Fix password hashing and token signing
`app/core/security.py` currently hashes passwords with unsalted SHA-256 under one hardcoded global salt, and falls back to constructing unsigned `mock.jwt.{role}.{user_id}.{expiry}` strings when `jwt` isn't importable. Both are unacceptable for anything resembling production, and both directly contradict the security design doc's own "Secure Authentication" section (strong hashing, never plaintext-equivalent).
- Restore real password hashing. The pre-`55997d7` version used `passlib` with Argon2 (bcrypt fallback) — that's a reasonable target to restore, or use `bcrypt` directly if you'd rather drop the passlib dependency; either is fine, unsalted single-round SHA-256 is not.
- Restore real JWT signing/verification (`python-jose` or `PyJWT` — pick one, use it consistently, don't leave a plaintext-token fallback path in the codebase at all, not even for local dev). If `PyJWT` needs to be added back to `requirements.txt`, add it.
- Remove the hardcoded backdoor passwords (`"AdminPassword123!"`, `"password"`) from `admin_login` entirely. No account should ever authenticate with anything other than its own correctly-verified password.
- Every existing password hash in any seed data / migration that assumed the old hashing scheme needs to be considered invalid once you switch schemes — note this in your summary; you may need to force a reset or re-seed.

### A.3 Fix `requirements.txt` so the backend actually boots
`openpyxl`, `reportlab`, and `pyotp` were removed from `requirements.txt` in `55997d7`, but `app/services/excel_service.py`, `app/services/pdf_service.py`, and `app/services/security_service.py` still import them, and those services are reachable from routers that are imported unconditionally at app startup (via `router.py`). Verify this by actually starting the app in a clean virtualenv with only `requirements.txt` installed — if it fails to boot, that confirms it. Fix by either restoring the dependencies to `requirements.txt` (if those features are still wanted for V1) or removing/stubbing the imports if they're genuinely being deprecated — don't leave the app in a state where a clean install can crash on startup. Do the same clean-install boot test after your other fixes in this phase, not just for this one.

### A.4 Reconcile the model layer — pick one `Booking`/`User`/`SupportTicket` schema, not two
`app/models/booking.py`, `app/models/user.py`, and `app/models/support.py` now just re-export different-shaped models from `app/models/customer.py`. The new `Booking` model dropped `provider_id`, `payment_status`, `timeline`, and changed `scheduled_time` from a real `DateTime` to a plain string, `address` to `address_line1`/`city`/`pincode`. Anything in the admin booking/support routers (`app/api/v1/bookings.py` admin router, `app/api/v1/support.py`) that references the old field names will now throw `AttributeError` at request time, not at import time — so this won't show up until someone clicks the relevant admin page.
- Audit every reference to `Booking.*`, `SupportTicket.*`, `User.*` fields across `app/api/v1/` and `app/services/` against the *current* model definitions in `app/models/customer.py`. List every mismatch you find.
- Design one coherent schema that serves both admin operations (which need `provider_id`, `payment_status`, a real timeline/audit trail, proper `DateTime` scheduling) and the new customer flows (which need the fields `customer.py`'s endpoints already use). This likely means extending the new model rather than reverting to the old one, since the new one is what's actually wired to real persistence for customers — but the decision is yours to make deliberately, not by accident.
- Write an Alembic migration for whatever the reconciled schema turns out to be. Don't leave two incompatible model definitions with the same table name coexisting.

### A.5 Restore the admin Provider Management API
`app/api/v1/providers.py` was fully replaced by a self-service provider API (`/providers/me`, `/providers/{id}/services`, `/providers/me/availability`, `/certificates`, no `/admin` prefix at all). The admin-facing endpoints that `admin-frontend`'s `pages/admin/providers/ProviderListView.tsx` and `ProviderDetailView.tsx` call (`GET/POST /admin/providers/...`, verify, suspend/reactivate) no longer exist anywhere in the codebase.
- These are two different, both-legitimate APIs — one for a provider managing their own profile/availability/certificates, one for an admin managing/verifying/suspending providers. **Keep both**, as two separate router files (e.g. `providers.py` stays admin-scoped as it originally was, and the new self-service logic moves to something like `provider_self.py` mounted without the admin prefix), rather than one replacing the other.
- Re-mount both in `router.py`/`main.py`. Verify `admin-frontend`'s Provider Workspace pages load and function against the restored admin endpoints.

### A.6 Re-mount the routers that silently disappeared
`feedback_router`, `emails_router`, and `ws_router` are imported in the pre-`55997d7` `main.py` but are absent from both the current `main.py` and `router.py`. Confirm whether this was intentional (a deliberate Phase-2 deferral — WebSockets are explicitly out of V1 scope per the design doc, so `ws_router` being dropped may be fine) or accidental (Email Center and AI feedback-scan are V1-scoped in the design doc and `admin-frontend` has live pages for both — `EmailCenterView.tsx`, the feedback view). Re-mount whichever are supposed to be live in V1; document clearly in your summary if you're deliberately leaving `ws_router` out per the V1 boundary.

### A.7 Reconcile the two customer-bookings surfaces
There are now two independent "customer bookings" APIs:
- `/api/v1/bookings` (the pre-existing `customer_bookings_router` in `bookings.py`) — still unauthenticated, still fabricates responses instead of persisting, as documented in the original audit. `mobile/src/api/bookings.ts` (or wherever mobile's booking calls live) points here.
- `/api/v1/customer/bookings` (new, in `customer.py`) — real, persisted, uses `get_current_customer`.

Pick one canonical path and deprecate the other. Given the new one is real and the old one is a non-functional stub, the right move is almost certainly: delete `customer_bookings_router` from `bookings.py` entirely (keep the admin `bookings.py` router untouched), make `/api/v1/customer/bookings` (or `/api/v1/bookings` if you'd rather rename the new router to that path for a shorter client-facing URL — your call, just pick one and be consistent) the only customer booking surface, and update `mobile`'s API client to point at it. State your choice explicitly in your summary since it changes the contract every client depends on.

### A.8 Clean up `customer.py` before it becomes load-bearing
A few things in the new file need attention now, before more is built on top of it:
- `MOCK_CATEGORIES`/`MOCK_SERVICES` are used as a fallback when the DB has no matching rows — reasonable for early dev, but several endpoints (`get_booking_by_id`, `cancel_booking`, `get_support_ticket_by_id`) fall back to **fabricated, hardcoded-looking-real data** (e.g. a specific address in Noida, `BK-1001`) when a record genuinely isn't found, rather than returning 404. This will silently mask real bugs and produce confusing UX (a customer requesting a booking that doesn't exist gets back what looks like a real one). Change all of these to proper `HTTPException(404)`.
- `login_customer` falls back to issuing a valid token for a hardcoded dev customer identity when credentials don't match a real user, instead of returning 401. This is an authentication bypass in its own right, independent of the ones in Phase A.1 — remove it. Real login failures must fail.
- `get_current_customer` in `dependencies.py` has the same problem: on any missing/invalid token, it falls back to fetching-or-creating a hardcoded dev customer (`pushkar@example.com`, fixed UUIDs) rather than raising 401. Remove this fallback; require a valid token unconditionally on every customer-scoped route.
- Ownership checks are present on most routes (`filter(Booking.customer_id == current_customer.id)`) — good, keep this pattern — but make sure it survives the removal of the fallback-identity logic above; some of these checks are currently meaningless because `current_customer` is so often a fabricated dev identity rather than the real authenticated caller.

---

## 3. Phase B — Verify, Then Resume Customer Frontend Work

Only start this once Phase A is done and verified.

1. Re-run the manual authorization test from the original audit on every customer endpoint in `customer.py`: log in as customer A, attempt to read/cancel/message customer B's booking/ticket by ID, confirm 403/404. Do this for real now that auth actually works.
2. Diff `feat/customer-frontend-integration` (`853949e`) and `release/v1.0-customer-frontend` (`615bb6e`) against current `main` — there may already be a customer-frontend scaffold, Playwright E2E suite, and CI workflow on those branches (`c345bcd feat(backend): add 27 customer endpoints, schemas, auth, and tests` suggests a near-identical prior attempt at the same 27ish endpoints now on `main`, possibly done more carefully). Decide whether to merge/rebase that work forward instead of continuing fresh against `main`'s current `customer.py`. If the branch version is cleaner, prefer it and port `main`'s few genuine improvements into it, rather than the reverse.
3. Once you've decided which customer backend to standardize on and it passes Phase A's security bar, resume the frontend build exactly as scoped in `instructions.md` v1 Sections 5–8 (design system porting, the five customer pages, mobile parity) — that scope and the five-page spec are still correct and don't need to be redone. What changed is the backend foundation underneath it, not the product requirements.
4. Update the API contracts in `instructions.md` v1 Section 5.3 / Section 7 to match whatever you land on for the canonical booking path (A.7) and the reconciled model shapes (A.4).

---

## 4. Non-Negotiables (unchanged from v1, restated because Phase A touches core files)

- Every protected endpoint under `/api/v1/` requires a real, verified JWT — no fallback identities, no dev-mode bypasses left reachable in the shipped code path (a `DEBUG`/`ENVIRONMENT=dev`-gated bypass that's structurally incapable of running in `ENVIRONMENT=production` is acceptable if you want one for local testing; an always-active bypass is not).
- UUID primary keys, `created_at`/`updated_at` timestamps, ownership checks server-side on every read/write of customer- or provider-owned data.
- Don't touch `admin-frontend`'s expectations without fixing the backend to match them (A.4, A.5) — it's described as "fully wired" and this audit shows it currently isn't, post-`55997d7`.
- Keep `admin_login` untouched in its actual security properties once Phase A is done (still admin-only, still real password verification) even though its surrounding code has clearly been edited.

---

## 5. What To Report Back

At the end of Phase A, before touching anything in Phase B, report:
- A clean-install boot confirmation (A.3) — did the app start with only `requirements.txt` installed, yes/no.
- Every field-mismatch you found in A.4, and the schema you chose to reconcile them.
- Confirmation that `get_current_user`/`require_admin`/`get_current_customer` no longer contain any unconditional fallback-identity logic (A.1, A.8), with the specific lines removed.
- Which customer-bookings path you standardized on (A.7) and what, if anything, needs updating in `mobile` as a result.
- Whether `ws_router`/`feedback_router`/`emails_router` were restored or deliberately left out, and why (A.6).
- A list of any branch work (Section 1, Section 3.2) you pulled forward instead of rewriting, so the team knows it's no longer just sitting unmerged.

Do not proceed to Phase B silently — stop and surface this report first, since some of these are judgment calls (A.4's schema reconciliation especially) that affect what the rest of the team builds against.
