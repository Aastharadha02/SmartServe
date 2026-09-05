# SmartServe Master Catalog Protection Policy
**Status**: FROZEN & PROTECTED (Category 1 & Category 2)
**Date**: September 5, 2026

---

## 1. Protected Scope (87 Services)

The following 87 services across Category 1 and Category 2 are strictly **PROTECTED AND FROZEN**:

### Category 1: Beauty, Salon & Spa (55 Services)
- **Facial & Skincare** (9 services)
- **Makeup & Styling** (6 services)
- **Men's Salon** (11 services)
- **Pedicure & Manicure** (10 services)
- **Spa & Massage** (6 services)
- **Women's Salon** (13 services)

### Category 2: Cleaning & Home Cleaning (32 Services)
- **Deep Cleaning** (7 services)
- **Full Home / By Room Cleaning** (8 services)
- **Kitchen & Bathroom Cleaning** (5 services)
- **Pest Control** (6 services)
- **Sofa & Furniture Cleaning** (6 services)

---

## 2. Inviolable Protection Rules

1. **NO UNREQUESTED MODIFICATIONS**:
   - NO automated script, seed script, migration, bulk updater, or content-generation tool may modify or overwrite any record in Category 1 or Category 2 without explicit user instruction.
2. **NO CONTENT DELETION / OVERWRITE**:
   - Save operations must never turn populated fields (`description`, `highlights`, `excluded`, `process_steps`, `tools_materials`, `customer_setup`, `aftercare`, `expected_results`, `important_notes`, `warranty`, `faqs`, `tips`, `dos`, `donts`, `service_features`, `seo_metadata`) into empty strings or nulls.
3. **EXISTING ADD-ONS ARE IMMUTABLE**:
   - Existing real add-ons must never be deleted, copied between services, or auto-generated.
4. **SERVICE IDENTITY IS IMMUTABLE**:
   - Service IDs, names, base prices, categories, subcategories, and active statuses are fixed.
5. **LEGITIMATE ADMIN EDITING PRESERVED**:
   - An authenticated Admin user intentionally modifying a field through the UI is fully supported, but untouched fields must remain preserved upon save.

---

## 3. Recovery Points & Checksum Files

- **Baseline Checksum File**: `backend/catalog_baseline_87_protected.json`
- **Permanent JSON Backup**: `backend/backups/category1_category2_87_services_permanent_backup.json`
- **Permanent SQL Dump**: `backend/backups/category1_category2_87_services_permanent_backup.sql`
- **Verification Script**: `python backend/test_catalog_baseline_87.py`
- **UI Save Data-Loss Test**: `python backend/test_ui_save_data_loss_11_services.py`
