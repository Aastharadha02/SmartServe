# V1 Plan

## V1 Includes
- Auth (customer/provider/admin) with JWT + RBAC
- Service catalog and provider search
- Provider profile, certificates, availability
- Booking lifecycle (RequestPlaced -> Accepted -> ServiceStarted -> ServiceCompleted -> Cancelled/Rejected)
- Pay-after-service payment and receipt
- Rating and review
- Basic admin verification and monitoring
- Explainable weighted provider ranking (rule-based AI)

## Not In V1 (Phased Backlog)
### V1.1 Realtime and Support Basics
WebSocket status updates, in-app notifications, basic chat, basic complaints, basic reschedule, safety complaint category

### V2 AI Intelligence Layer (Aastha input)
AI auto-assignment, personalized recommendations, AI delay detection, smart reschedule suggestions, provider AI insights, admin demand heat map, AI complaint prioritization, reliability scoring

### V3 Advanced Production Layer
Multilingual AI support, voice booking, SmartServe wallet and loyalty credits, Razorpay, WhatsApp notifications, RAG support agent, live GPS tracking, geofencing, fraud detection

## Shared Foundation First
ERD, OpenAPI contract, JWT auth, booking state machine, Docker, Git workflow

## Rules
- One repo, one FastAPI backend, one React app, one PostgreSQL DB
- /api/v1 prefix, UUID primary keys
- Kafka via outbox_events first, full Kafka later
