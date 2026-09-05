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

def persist_category9_draft():
    draft_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "catalog_drafts", "category9", "category9_health_fitness_wellness_DRAFT.json"))
    with open(draft_path, "r", encoding="utf-8") as f:
        draft = json.load(f)
        
    services = draft["services"]
    print(f"Loaded {len(services)} validated draft services for Category 9.")
    
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
    
    print("\n" + "=" * 80)
    print("PHASE 7: PERSISTING APPROVED DRAFT TO POSTGRESQL (ONE SERVICE AT A TIME)")
    print("=" * 80)
    
    success_count = 0
    
    for idx, s in enumerate(services, 1):
        sid = s["id"]
        sname = s["name"]
        subcat = s["subcategory"]
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Build structured metadata blocks for persistence
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
        
        final_suggested_addons = typed_blocks
        distinct_features = s["included"]
        
        # INSERT or UPDATE depending on if it exists
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
        
        conn.commit()
        print(f"[{idx}/{len(services)}] Successfully persisted '{sname}' [{sid}]")
        success_count += 1
        
    conn.close()
    print("\n" + "=" * 80)
    print(f"DONE. {success_count} Category 9 services successfully inserted/updated in PostgreSQL.")
    print("=" * 80)

if __name__ == "__main__":
    persist_category9_draft()
