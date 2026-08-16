# SmartServe Team Ownership (50/50 Domain Split)

## Philosophy
Two business domains, each owned end-to-end.
But: ONE monorepo, ONE FastAPI app, ONE React app, ONE PostgreSQL DB.
Admin dashboard designed together after core booking works.

## Aastha - Customer Ecosystem
- Customer auth UI, dashboard, service discovery, filters
- AI provider recommendation (explainable)
- Booking creation, cancel, reschedule request
- Payments (COD now, Razorpay later), receipts, QR
- Reviews and ratings
- AI support (RAG, multilingual later), complaints
- Customer notifications
- Kafka events: BOOKING_CREATED, BOOKING_CANCELLED, PAYMENT_COMPLETED, REVIEW_SUBMITTED, COMPLAINT_CREATED
- Tables: customers, bookings, booking_status_history, payments, reviews, support_tickets, wallet (V3)

## Pushkar - Provider Ecosystem
- Provider auth UI, profile, certificates upload
- Availability calendar
- Booking accept/reject/start/complete
- Live tracking, geofencing, delay detection (V2)
- Provider chat, dashboard, analytics
- Provider AI: reliability score, demand forecast, pricing suggestions
- Provider notifications
- Kafka events: BOOKING_ACCEPTED, PROVIDER_ON_THE_WAY, ARRIVAL_DETECTED, SERVICE_STARTED, SERVICE_COMPLETED, DOCUMENT_VERIFIED
- Tables: providers, provider_services, certificates, availability, locations, provider_metrics

## Shared (Build Together First)
ERD, OpenAPI contract, JWT/RBAC, booking state machine, UI design system,
folder structure, Git workflow, Kafka topic naming, WebSocket events,
Docker Compose, Jenkins, Cloudflare, final testing

## Integration Points
- Booking request <-> Booking acceptance
- Booking status <-> Provider status
- Customer chat <-> Provider chat
- Payment confirmation <-> Service completion
- Review <-> Reliability update

## Hard Rules
- Booking state machine frozen before coding
- Migrations: single owner per table
- PR to develop with one review
- No direct push to main
- Branches: feature/customer-*, feature/provider-*, feature/shared-*
