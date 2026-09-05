import os
import sys
import zipfile
import hashlib
import datetime

def create_backup_zip():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    backend_dir = os.path.join(base_dir, "backend")
    
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    zip_name = f"smartserve_complete_database_and_services_backup_{today_str}.zip"
    zip_path = os.path.join(base_dir, zip_name)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", zip_name)
    
    print(f"Creating backup zip package: {zip_path}")
    
    readme_content = f"""# SmartServe Complete Database & Services Content Backup Package
================================================================================
Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}
Authoritative Source: Local PostgreSQL (smartserve on localhost:5432)
Total Protected Services: 195 services across 5 completed categories
Total Database Rows: 620 rows across 20 base tables
================================================================================

PACKAGE CONTENTS & DIRECTORY STRUCTURE:

1. database_complete_backups/
   - smartserve_complete_backup_2026-09-05_05.sql: Full PostgreSQL plain-text database dump.
   - smartserve_complete_backup_2026-09-05_05.json: Complete JSON database dump (all 20 tables).
   - smartserve_complete_backup_2026-09-05_05.xlsx: Multi-sheet spreadsheet with all database tables.
   - smartserve_backup_manifest_2026-09-05_05.json: Database audit manifest with row counts and SHA-256 checksums.

2. category_final_backups/
   - Category 1 & 2: Permanent backup JSON & SQL (87 services).
   - Category 3: Home Improvement & Painting permanent backups (23 services).
   - Category 4: AC, Appliance & Electronics Repair final JSON, XLSX, and SQL (46 services).
   - Category 5: Electrician, Plumber, Carpenter & Home Repairs final JSON, XLSX, and SQL (39 services).

3. category_verification_reports/
   - Detailed database verification matrices (POPULATED / EMPTY / N/A) for Category 3, 4, and 5.

4. catalog_drafts/
   - Validated pre-persistence drafts (JSON & XLSX) for Category 4 and 5.

5. services_content_source/
   - Complete Python builder datasets for Category 3, Category 4, and Category 5.
   - Every service contains 16 rich structured fields (description, highlights, inclusions, exclusions, process steps, tools/materials, customer setup, aftercare, expected results, important notes, warranty, FAQs, dos, donts, tips, existing add-ons).

6. catalog_baselines/
   - catalog_baseline_195_protected.json: Master baseline covering all 195 protected services with SHA-256 hash.
   - catalog_baseline_156_protected.json: Baseline covering Categories 1-4.

7. tooling_and_restore_scripts/
   - Complete backup, verification, and transactional restoration scripts.

================================================================================
HOW TO RESTORE DATABASE FROM SQL DUMP:
1. Ensure PostgreSQL is running on localhost:5432
2. To restore the complete database:
   psql -U postgres -d smartserve -f database_complete_backups/smartserve_complete_backup_2026-09-05_05.sql
3. To restore a specific category (e.g. Category 5):
   psql -U postgres -d smartserve -f category_final_backups/category5_electrician_plumber_carpenter_home_repairs_FINAL.sql
================================================================================
"""

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add README
        zf.writestr("smartserve_backup_package/README.md", readme_content)
        
        # 1. Complete Database Backups
        backups_dir = os.path.join(backend_dir, "backups")
        full_backup_files = [
            "smartserve_complete_backup_2026-09-05_05.sql",
            "smartserve_complete_backup_2026-09-05_05.json",
            "smartserve_complete_backup_2026-09-05_05.xlsx",
            "smartserve_backup_manifest_2026-09-05_05.json"
        ]
        for f in full_backup_files:
            fp = os.path.join(backups_dir, f)
            if os.path.exists(fp):
                zf.write(fp, f"smartserve_backup_package/database_complete_backups/{f}")
                print(f"  + Added: database_complete_backups/{f}")
                
        # 2. Category Final Backups
        cat_final_files = [
            "category1_category2_87_services_permanent_backup.sql",
            "category1_category2_87_services_permanent_backup.json",
            "cleaning_services_32_fully_populated_verified.json",
            "category3_home_improvement_4_services_backup.sql",
            "category3_home_improvement_4_services_backup.json",
            "category3_painting_waterproofing_home_improvement_restored.json",
            "category4_ac_appliance_electronics_repair_FINAL.sql",
            "category4_ac_appliance_electronics_repair_FINAL.json",
            "category4_ac_appliance_electronics_repair_FINAL.xlsx",
            "category4_ac_appliance_electronics_repair_pre_change_snapshot.json",
            "category5_electrician_plumber_carpenter_home_repairs_FINAL.sql",
            "category5_electrician_plumber_carpenter_home_repairs_FINAL.json",
            "category5_electrician_plumber_carpenter_home_repairs_FINAL.xlsx",
            "category5_electrician_plumber_carpenter_home_repairs_pre_change_snapshot.json"
        ]
        for f in cat_final_files:
            fp = os.path.join(backups_dir, f)
            if os.path.exists(fp):
                zf.write(fp, f"smartserve_backup_package/category_final_backups/{f}")
                print(f"  + Added: category_final_backups/{f}")
                
        # 3. Category Verification Reports
        verif_files = [
            "category4_ac_appliance_electronics_repair_DATABASE_VERIFICATION.json",
            "category4_ac_appliance_electronics_repair_DATABASE_VERIFICATION.xlsx",
            "category5_electrician_plumber_carpenter_home_repairs_DATABASE_VERIFICATION.json",
            "category5_electrician_plumber_carpenter_home_repairs_DATABASE_VERIFICATION.xlsx"
        ]
        for f in verif_files:
            fp = os.path.join(backups_dir, f)
            if os.path.exists(fp):
                zf.write(fp, f"smartserve_backup_package/category_verification_reports/{f}")
                print(f"  + Added: category_verification_reports/{f}")
                
        cat3_verif = os.path.join(backend_dir, "catalog_verification", "category3_database_storage_verification.json")
        if os.path.exists(cat3_verif):
            zf.write(cat3_verif, "smartserve_backup_package/category_verification_reports/category3_database_storage_verification.json")
            print("  + Added: category_verification_reports/category3_database_storage_verification.json")

        # 4. Catalog Drafts
        drafts_dir = os.path.join(backend_dir, "catalog_drafts")
        if os.path.exists(drafts_dir):
            for root, _, files in os.walk(drafts_dir):
                for f in files:
                    fp = os.path.join(root, f)
                    rel_path = os.path.relpath(fp, drafts_dir)
                    zf.write(fp, f"smartserve_backup_package/catalog_drafts/{rel_path}")
                    print(f"  + Added: catalog_drafts/{rel_path}")
                    
        # 5. Services Content Source (Builders)
        content_files = [
            ("backend/category3_content_data.py", "smartserve_backup_package/services_content_source/category3_content_data.py"),
            ("backend/home_improvement_data.py", "smartserve_backup_package/services_content_source/home_improvement_data.py"),
        ]
        for src, dest in content_files:
            fp = os.path.join(base_dir, src)
            if os.path.exists(fp):
                zf.write(fp, dest)
                print(f"  + Added: {dest}")
                
        cat4_builder = os.path.join(backend_dir, "category4_content_builder")
        if os.path.exists(cat4_builder):
            for root, _, files in os.walk(cat4_builder):
                for f in files:
                    if not f.endswith(".pyc") and "__pycache__" not in root:
                        fp = os.path.join(root, f)
                        rel_path = os.path.relpath(fp, cat4_builder)
                        zf.write(fp, f"smartserve_backup_package/services_content_source/category4_content_builder/{rel_path}")
                        print(f"  + Added: services_content_source/category4_content_builder/{rel_path}")
                        
        cat5_builder = os.path.join(backend_dir, "category5_content_builder")
        if os.path.exists(cat5_builder):
            for root, _, files in os.walk(cat5_builder):
                for f in files:
                    if not f.endswith(".pyc") and "__pycache__" not in root:
                        fp = os.path.join(root, f)
                        rel_path = os.path.relpath(fp, cat5_builder)
                        zf.write(fp, f"smartserve_backup_package/services_content_source/category5_content_builder/{rel_path}")
                        print(f"  + Added: services_content_source/category5_content_builder/{rel_path}")

        # 6. Catalog Baselines
        baseline_files = [
            "catalog_baseline_195_protected.json",
            "catalog_baseline_156_protected.json",
            "catalog_baseline_110_protected.json"
        ]
        for f in baseline_files:
            fp = os.path.join(backend_dir, f)
            if os.path.exists(fp):
                zf.write(fp, f"smartserve_backup_package/catalog_baselines/{f}")
                print(f"  + Added: catalog_baselines/{f}")
                
        # 7. Tooling & Scripts
        scripts_dir = os.path.join(backend_dir, "scripts")
        if os.path.exists(scripts_dir):
            for root, _, files in os.walk(scripts_dir):
                for f in files:
                    if f.endswith(".py") and "__pycache__" not in root:
                        fp = os.path.join(root, f)
                        rel_path = os.path.relpath(fp, scripts_dir)
                        zf.write(fp, f"smartserve_backup_package/tooling_and_restore_scripts/{rel_path}")
                        print(f"  + Added: tooling_and_restore_scripts/{rel_path}")

    # Calculate SHA256 of zip
    sha256 = hashlib.sha256()
    with open(zip_path, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    zip_sha = sha256.hexdigest()
    zip_size = os.path.getsize(zip_path)
    
    # Also copy to Desktop for easy access
    try:
        import shutil
        shutil.copy2(zip_path, desktop_path)
        print(f"\n[COPIED TO DESKTOP] {desktop_path}")
    except Exception as e:
        print(f"Note: Could not copy to Desktop: {e}")
        
    print("\n" + "=" * 80)
    print("BACKUP ZIP ARCHIVE CREATED SUCCESSFULLY:")
    print(f"  Workspace File: {zip_path}")
    print(f"  Desktop File:   {desktop_path}")
    print(f"  File Size:      {zip_size:,} bytes ({zip_size / (1024*1024):.2f} MB)")
    print(f"  SHA-256:        {zip_sha}")
    print("=" * 80)
    return zip_path, desktop_path, zip_size, zip_sha

if __name__ == "__main__":
    create_backup_zip()
