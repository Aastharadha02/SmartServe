import os
import sys
import json
import uuid
import datetime
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

def persist_category4_draft():
    draft_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "catalog_drafts", "category4", "category4_ac_appliance_electronics_repair_DRAFT.json"))
    with open(draft_path, "r", encoding="utf-8") as f:
        draft = json.load(f)
        
    services = draft["services"]
    print(f"Loaded {len(services)} validated draft services for Category 4.")
    assert len(services) == 46, f"Expected 46 draft services, got {len(services)}"
    
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres@localhost:5432/smartserve")
    p = urlparse(db_url)
    
    conn = psycopg2.connect(
        dbname=p.path.lstrip('/'),
        user=p.username,
        password=unquote(p.password or ''),
        host=p.hostname or 'localhost',
        port=p.port or 5432
    )
    conn.autocommit = False # Strictly transactional
    
    print("\n" + "=" * 80)
    print("PHASE 7: PERSISTING APPROVED DRAFT TO POSTGRESQL (ONE SERVICE AT A TIME)")
    print("=" * 80)
    
    success_count = 0
    
    for idx, s in enumerate(services, 1):
        sid = s["id"]
        sname = s["name"]
        subcat = s["subcategory"]
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Step 1: SELECT current PostgreSQL record (to preserve existing real add-ons)
        cur.execute("""
            SELECT id, name, category, subcategory, base_price, is_active, 
                   distinct_features, suggested_addons, max_demand_increase, max_discount
            FROM services
            WHERE id = %s
        """, (sid,))
        current_db = cur.fetchone()
        
        existing_real_addons = []
        if current_db:
            db_sa = current_db["suggested_addons"] or []
            existing_real_addons = [a for a in db_sa if isinstance(a, dict) and not a.get("type") and a.get("name") and a.get("name") != "None"]
        
        # Step 3: Build structured metadata blocks for persistence
        typed_blocks = [
            {"type": "description", "text": s["description"]},
            {"type": "highlights", "items": s["highlights"]},
            {"type": "excluded_scope", "items": s["excluded"]},
            {"type": "process_steps", "steps": s["process_steps"]},
            {"type": "aftercare_precautions", "aftercare": s["aftercare"]},
            {"type": "tools_materials", "tools": s["tools_materials"], "materials": []},
            {"type": "customer_setup", "requirements": s["customer_setup"]},
            {"type": "expected_results", "items": s["expected_results"]},
            {"type": "important_notes", "items": s["important_notes"]},
            {"type": "warranty", "has_warranty": True, "details": s["warranty"]},
            {"type": "faqs", "items": s["faqs"]},
            {"type": "tips", "items": s["tips"]},
            {"type": "dos_donts", "dos": s.get("dos", []), "donts": s.get("donts", [])},
            {"type": "duration", "minutes": s.get("duration_minutes", 60)}
        ]
        
        # Combine real addons + typed metadata blocks
        final_suggested_addons = list(existing_real_addons) + typed_blocks
        
        # distinct_features stores curated inclusions
        distinct_features = s["included"]
        
        # Step 4: Apply INSERT or UPDATE inside transaction
        cur.execute("""
            INSERT INTO services (id, name, category, subcategory, base_price, is_active, distinct_features, suggested_addons, max_demand_increase, max_discount, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                category = EXCLUDED.category,
                subcategory = EXCLUDED.subcategory,
                base_price = EXCLUDED.base_price,
                is_active = EXCLUDED.is_active,
                distinct_features = EXCLUDED.distinct_features,
                suggested_addons = EXCLUDED.suggested_addons,
                updated_at = NOW()
        """, (
            sid, sname, s["category"], subcat, s["price"], s["active"], 
            json.dumps(distinct_features), json.dumps(final_suggested_addons), 
            20.0, 10.0
        ))
        
        # Step 5: Verify on fresh SELECT within same transaction
        cur.execute("""
            SELECT id, name, category, subcategory, base_price, is_active, 
                   distinct_features, suggested_addons
            FROM services
            WHERE id = %s
        """, (sid,))
        verify_row = cur.fetchone()
        
        if not verify_row or not verify_row["suggested_addons"]:
            conn.rollback()
            raise Exception(f"Fresh SELECT verification failed for service '{sname}' [{sid}]!")
            
        # Verify add-ons intact
        fresh_sa = verify_row["suggested_addons"]
        fresh_real_addons = [a for a in fresh_sa if isinstance(a, dict) and not a.get("type") and a.get("name")]
        assert len(fresh_real_addons) == len(existing_real_addons), f"Add-on count changed on '{sname}' [{sid}]!"
        
        # Verify typed blocks present
        fresh_types = [a.get("type") for a in fresh_sa if isinstance(a, dict) and a.get("type")]
        assert len(fresh_types) == len(typed_blocks), f"Typed blocks count mismatch on '{sname}' [{sid}]!"
        
        # Step 6: COMMIT transaction for this service
        conn.commit()
        cur.close()
        
        success_count += 1
        print(f"[{idx:2d}/46] [PERSISTED & VERIFIED] {subcat:20s} | {sname:32s} | Addons: {len(fresh_real_addons)} | Types: {len(fresh_types)}")
        
    conn.close()
    
    print("\n" + "=" * 80)
    print(f"SUCCESS: ALL {success_count} CATEGORY 4 SERVICES FULLY PERSISTED & COMMITTED!")
    print("=" * 80)
    return success_count

if __name__ == "__main__":
    persist_category4_draft()
