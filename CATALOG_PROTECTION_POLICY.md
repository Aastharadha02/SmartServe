# SmartServe Master Catalog Protection Policy
**Status**: ACTIVE, ENFORCED & EXPANDED (Categories 1, 2, 3, and 4)  
**Last Updated**: September 5, 2026  

---

## 1. Protected Scope (156 Total Services)

The following 156 services across Categories 1, 2, 3, and 4 are strictly **PROTECTED, PERSISTED, AND MONITORED**:

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
- **Category 3 Pre-Restore Backup**: `backend/backups/category3_painting_waterproofing_home_improvement_pre_restore.json`
- **Category 3 Post-Restore Backup**: `backend/backups/category3_painting_waterproofing_home_improvement_restored.json`
- **Category 4 Pre-Change Snapshot**: `backend/backups/category4_ac_appliance_electronics_repair_pre_change_snapshot.json`
- **Category 4 Final Checkpoints**: `backend/backups/category4_ac_appliance_electronics_repair_FINAL.{json,xlsx,sql}`
- **Machine-Readable Baseline (156 Services)**: `backend/catalog_baseline_156_protected.json` (SHA-256: `4f05518c17be8322bec2fdf2ef6a6c8f019d1d89bad0213e4167b231b0ba1528`)
