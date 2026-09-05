# SmartServe Master Catalog Protection Policy
**Status**: ACTIVE, ENFORCED & COMPLETE (All 14 Categories)  
**Last Updated**: September 5, 2026  

---

## 1. Protected Scope (457 Total Services — DB Verified)

All 457 services across all 14 Categories are strictly **PROTECTED, PERSISTED, AND MONITORED**:

### Category 1: Beauty, Salon & Spa (55 Services)
*(Regenerated Sep 5, 2026 after original Neon data became inaccessible due to network transfer suspension - resets Oct 1, 2026)*
- **Facial & Skincare** (9 services)
- **Makeup & Styling** (6 services)
- **Men's Salon** (11 services)
- **Pedicure & Manicure** (10 services)
- **Spa & Massage** (6 services)
- **Women's Salon** (13 services)

### Category 2: Cleaning & Home Cleaning (32 Services)
*(Regenerated Sep 5, 2026 after original Neon data became inaccessible due to network transfer suspension - resets Oct 1, 2026)*
- **Deep Cleaning** (7 services)
- **Full Home / By Room Cleaning** (8 services)
- **Kitchen & Bathroom Cleaning** (5 services)
- **Pest Control** (6 services)
- **Sofa & Furniture Cleaning** (6 services)

### Category 3: Painting, Waterproofing & Home Improvement (23 Services)
- **Home Improvement** (4 services)
- **Home Painting** (9 services)
- **Specialized Painting** (5 services)
- **Waterproofing & Grouting** (5 services)

### Category 4: AC, Appliance & Electronics Repair (46 Services)
- **AC** (7 services)
- **Air Cooler** (3 services)
- **Chimney** (3 services)
- **Geyser** (4 services)
- **Microwave** (3 services)
- **RO / Water Purifier** (5 services)
- **Refrigerator** (5 services)
- **Television** (5 services)
- **Variants** (6 services)
- **Washing Machine** (5 services)

### Category 5: Electrician, Plumber, Carpenter & Home Repairs (39 Services)
- **Carpenter Services** (12 services)
- **Electrician Services** (15 services)
- **Plumber Services** (12 services)

### Category 6: Smart Home & Security (30 Services)
- **Alarm & Sensor Systems** (7 services)
- **CCTV/Camera Installation** (7 services)
- **Smart Lighting/Switches** (5 services)
- **Smart Locks & Access Control** (6 services)
- **Video Doorbells** (5 services)

### Category 7: Domestic Help & Cooking (30 Services)
- **Cooks / Chefs** (7 services)
- **Drivers** (4 services)
- **Elder Care / Patient Care** (6 services)
- **Maids / Housekeepers** (7 services)
- **Nannies / Babysitters** (6 services)

### Category 8: Education, Teachers & Coaching (30 Services)
- **Competitive Exam Coaching** (7 services)
- **Language & Communication** (5 services)
- **Music & Arts Lessons** (5 services)
- **School Tutoring (K-12)** (7 services)
- **Skills & Hobby Classes** (6 services)

### Category 9: Health, Fitness & Wellness (30 Services)
- **Mental Wellness & Counselling** (6 services)
- **Nutrition & Diet Counselling** (5 services)
- **Personal Training** (7 services)
- **Physiotherapy & Rehabilitation** (6 services)
- **Yoga & Meditation** (6 services)

### Category 10: Events, Photography & Entertainment (30 Services)
- **Catering & Food Services** (6 services)
- **Decoration & Floral** (6 services)
- **DJ & Sound Systems** (5 services)
- **Event Planning & Management** (6 services)
- **Photography & Videography** (7 services)

### Category 11: Pet Services (25 Services)
- **Dog Grooming** (6 services)
- **Dog Training** (5 services)
- **Pet Accessories & Nutrition** (4 services)
- **Pet Sitting & Boarding** (5 services)
- **Veterinary & Health Checkup** (5 services)

### Category 12: Technology & Digital Services (30 Services)
- **Computer & Laptop Repair** (7 services)
- **Data Recovery & Backup** (5 services)
- **IT Support & Consultation** (7 services)
- **Networking & Wi-Fi Setup** (5 services)
- **Website & App Development** (6 services)

### Category 13: Professional & Business Services (30 Services)
- **Accounting & Tax Filing** (6 services)
- **Business Consulting** (5 services)
- **Legal Documentation** (5 services)
- **Marketing & Branding** (6 services)
- **Staffing & HR Services** (5 services)
- **Virtual Assistant** (3 services)

### Category 14: Moving, Delivery & Local Assistance (27 Services)
- **Home Shifting & Packing** (7 services)
- **Junk Removal & Disposal** (5 services)
- **Last-Mile Delivery** (5 services)
- **Local Errands & Assistance** (5 services)
- **Vehicle Transport** (5 services)

---

## 2. Inviolable Protection Policy (11 Mandatory Rules)

1. **Master Source of Truth**: The Admin Catalog in the local PostgreSQL database is the single authoritative master catalog.
2. **Customer Application Read-Only**: The Customer frontend and backend are strictly read-only consumers of catalog data. No catalog write or mutation API exists on the customer application.
3. **Authorized Admin Persistence Path**: Catalog writes and modifications occur exclusively through the authorized, authenticated Admin API persistence path (`/api/v1/admin/catalog/*`) requiring admin privileges.
4. **No Automated Overwrite by AI/Scripts**: AI-generated scripts, background agents, and migrations must never automatically rewrite catalog records without explicit, verified user authorization.
5. **Safe Merge for Partial Updates**: All partial updates (`PUT /admin/catalog/services/{id}`) must safely merge incoming fields with existing database metadata. Omitted fields must remain 100% untouched.
6. **No Silent Data Loss**: Existing populated metadata (`description`, `highlights`, `included`, `excluded`, `process_steps`, `tools_materials`, `customer_setup`, `aftercare`, `expected_results`, `important_notes`, `warranty`, `faqs`, `tips`, `dos`, `donts`, `service_features`, `service_media`, `seo_metadata`) can never be silently cleared or replaced by empty defaults (`""`, `[]`, `null`, `{}`).
7. **Real Add-ons Immutability**: Existing real database add-ons are strictly immutable; they cannot be regenerated, deleted, or overwritten during metadata edits.
8. **Explicit Authorization for Bulk Operations**: Any batch catalog modification requires prior review and explicit user confirmation.
9. **Pre-Write Backup Mandate**: Every batch or single-category catalog modification must automatically generate a timestamped local backup prior to execution.
10. **Post-Write DB Read-Back Verification**: Every catalog transaction must perform an immediate fresh `SELECT` query from PostgreSQL to verify that data was properly committed before returning success.
11. **Immediate Transaction Abort on Mutation Anomaly**: Any unexpected metadata corruption, type mismatch, or deletion anomaly must trigger an immediate `ROLLBACK` and halt execution.

---

## 3. Technical Safeguards Implemented

- **Pydantic Field Tracking**: Uses `req.model_fields_set` in `app/api/v1/catalog.py` to distinguish explicitly provided fields from omitted fields.
- **Empty-Block Overwrite Protection**: Filters out empty placeholder objects from incoming payloads and ensures non-empty existing blocks are never overwritten by empty structures.
- **Transactional Atomicity**: Database writes use ACID transactions with rollback on verification error.
- **Versioned Audit Logging**: Each edit captures `previous_state`, `new_state`, and `fields_modified` in the immutable `audit_logs` table.

---

## 4. Checkpoint Artifacts & Baselines

- **Category 1 & 2 Permanent Backup**: `backend/backups/category1_category2_87_services_permanent_backup.json`
- **Category 3 Post-Restore Backup**: `backend/backups/category3_painting_waterproofing_home_improvement_restored.json`
- **Category 4 Final Checkpoints**: `backend/backups/category4_ac_appliance_electronics_repair_FINAL.{json,xlsx,sql}`
- **Category 5 Final Backup**: `backend/backups/category5_electrician_plumber_carpenter_FINAL.{json,xlsx}`
- **Category 6 Final Backup**: `backend/backups/category6_smart_home_security_FINAL.{json,xlsx}`
- **Category 7 Final Backup**: `backend/backups/category7_domestic_help_cooking_FINAL.{json,xlsx}`
- **Category 8 Final Backup**: `backend/backups/category8_education_coaching_FINAL.{json,xlsx}`
- **Category 9 Final Backup**: `backend/backups/category9_health_fitness_wellness_FINAL.{json,xlsx}`
- **Category 10 Final Backup**: `backend/backups/category10_events_photography_entertainment_FINAL.{json,xlsx}`
- **Category 11 Final Backup**: `backend/backups/category11_pet_services_FINAL.{json,xlsx}`
- **Category 12 Final Backup**: `backend/backups/category12_technology_digital_services_FINAL.{json,xlsx}`
- **Category 13 Final Backup**: `backend/backups/category13_professional_business_services_FINAL.{json,xlsx}`
- **Category 14 Final Backup**: `backend/backups/category14_moving_delivery_local_assistance_FINAL.{json,xlsx}`
- **DB Verified Count (Sep 5, 2026)**: 457 services across all 14 categories confirmed in local PostgreSQL
  *(2 stale stubs deleted from Cat 8 via cleanup_cat8_stubs.py)*
