import os
import sys
import json
import uuid
import datetime
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.database import SessionLocal
from app.api.v1.catalog import get_service_item
from app.models.user import User

def persist_category5_draft():
    draft_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "catalog_drafts", "category5", "category5_electrician_plumber_carpenter_home_repairs_DRAFT.json"))
    with open(draft_path, "r", encoding="utf-8") as f:
        draft = json.load(f)
        
    services = draft["services"]
    print(f"Loaded {len(services)} validated draft services for Category 5.")
    assert len(services) == 39, f"Expected 39 draft services, got {len(services)}"
    
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
    conn.autocommit = False # Strictly transactional: one service at a time
    
    # SQLAlchemy session for Admin API verification
    db_session = SessionLocal()
    admin_user = db_session.query(User).filter(User.role.in_(["admin", "superadmin"])).first()
    assert admin_user is not None, "No admin user found in DB for API verification!"
    
    print("\n" + "=" * 80)
    print("PHASE 7: PERSISTING APPROVED DRAFT TO POSTGRESQL (ONE SERVICE AT A TIME)")
    print("=" * 80)
    
    success_count = 0
    
    for idx, s in enumerate(services, 1):
        sid = s["id"]
        sname = s["name"]
        subcat = s["subcategory"]
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Step 1: SELECT current PostgreSQL record
        cur.execute("""
            SELECT id, name, category, subcategory, base_price, is_active, 
                   distinct_features, suggested_addons, max_demand_increase, max_discount
            FROM services
            WHERE id = %s
        """, (sid,))
        current_db = cur.fetchone()
        
        if not current_db:
            conn.rollback()
            raise Exception(f"Service '{sname}' [{sid}] not found in PostgreSQL!")
            
        # Parity check
        assert current_db["name"] == sname, f"Name mismatch on {sid}: DB='{current_db['name']}' vs Draft='{sname}'"
        assert current_db["subcategory"] == subcat, f"Subcategory mismatch on {sid}"
        assert float(current_db["base_price"]) == float(s["price"]), f"Price mismatch on {sid}"
        assert current_db["is_active"] == s["active"], f"Active status mismatch on {sid}"
        
        # Step 2: Capture existing add-ons
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
            {"type": "warranty", "has_warranty": True if s.get("warranty") else False, "details": s.get("warranty")},
            {"type": "faqs", "items": s["faqs"]},
            {"type": "tips", "items": s["tips"]},
            {"type": "dos_donts", "dos": s.get("dos", []), "donts": s.get("donts", [])},
            {"type": "duration", "minutes": s.get("duration_minutes", 60)}
        ]
        
        # Combine real addons + typed metadata blocks (preserving real addons 100%)
        final_suggested_addons = list(existing_real_addons) + typed_blocks
        
        # distinct_features stores curated inclusions
        distinct_features = s["included"]
        
        # Step 4: Apply UPDATE inside transaction
        cur.execute("""
            UPDATE services
            SET distinct_features = %s,
                suggested_addons = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (json.dumps(distinct_features), json.dumps(final_suggested_addons), sid))
        
        # Step 5: Verify on fresh SELECT within same transaction
        cur.execute("""
            SELECT id, name, category, subcategory, base_price, is_active, 
                   distinct_features, suggested_addons, max_demand_increase, max_discount
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
        assert [a.get("name") for a in fresh_real_addons] == [a.get("name") for a in existing_real_addons], f"Add-on names changed on '{sname}' [{sid}]!"
        
        # Verify typed blocks present
        fresh_types = [a.get("type") for a in fresh_sa if isinstance(a, dict) and a.get("type")]
        assert len(fresh_types) == len(typed_blocks), f"Typed blocks count mismatch on '{sname}' [{sid}]!"
        
        # Verify identity and pricing unchanged
        assert verify_row["id"] == sid
        assert verify_row["name"] == sname
        assert verify_row["category"] == s["category"]
        assert verify_row["subcategory"] == subcat
        assert float(verify_row["base_price"]) == float(s["price"])
        assert verify_row["is_active"] == s["active"]
        
        # Step 6: COMMIT transaction for this service
        conn.commit()
        cur.close()
        
        # Step 7: Verify via Admin API
        # Expire session cache to ensure fresh query
        db_session.expire_all()
        api_item = get_service_item(sid, db=db_session, admin=admin_user)
        assert api_item.id == sid
        assert api_item.name == sname
        assert float(api_item.base_price) == float(s["price"])
        assert len(api_item.highlights) >= 4, f"API highlights count low on {sname}"
        assert len(api_item.process_steps) >= 4, f"API process steps count low on {sname}"
        assert len(api_item.addons) == len(existing_real_addons), f"API addons count mismatch on {sname}"
        
        success_count += 1
        print(f"[{idx:2d}/39] [PERSISTED, VERIFIED & COMMITTED] {subcat:15s} | {sname:32s} | Real Addons: {len(fresh_real_addons)} | Types: {len(fresh_types)}")
        
    conn.close()
    db_session.close()
    
    print("\n" + "=" * 80)
    print(f"SUCCESS: ALL {success_count} CATEGORY 5 SERVICES FULLY PERSISTED, COMMITTED & VERIFIED VIA ADMIN API!")
    print("=" * 80)
    return success_count

if __name__ == "__main__":
    persist_category5_draft()
