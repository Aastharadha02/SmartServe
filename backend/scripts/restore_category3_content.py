import os
import sys
import json
import datetime
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from category3_content_data import ALL_CATEGORY3_SERVICES

def restore_category3():
    print("=" * 80)
    print("RESTORING CATEGORY 3 CATALOG CONTENT WITH TRANSACTION SAFETY")
    print("=" * 80)
    
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')
    p = urlparse(db_url)
    conn = psycopg2.connect(
        dbname=p.path.lstrip('/'),
        user=p.username,
        password=unquote(p.password),
        host=p.hostname,
        port=p.port
    )
    # Autocommit off for explicit transaction control
    conn.autocommit = False
    cur = conn.cursor()
    
    restored_services = []
    
    try:
        for s in ALL_CATEGORY3_SERVICES:
            sid = s["id"]
            sname = s["name"]
            subcat = s["subcategory"]
            
            # Step 1: Load existing service
            cur.execute("""
                SELECT id, category, subcategory, name, base_price, is_active, distinct_features, suggested_addons
                FROM services
                WHERE id = %s
            """, (sid,))
            row = cur.fetchone()
            
            db_sa = []
            db_df = []
            if row:
                db_id, db_cat, db_subcat, db_name, db_price, db_active, db_df, db_sa = row
            
            # Extract existing real addons
            existing_sa = db_sa or []
            existing_real_addons = [a for a in existing_sa if isinstance(a, dict) and not a.get("type") and a.get("name") and a.get("name") != "None"]
            
            # Build structured metadata blocks for persistence
            typed_blocks = []
            
            # 1. Description
            if s.get("description"):
                typed_blocks.append({"type": "description", "text": s["description"]})
                
            # 2. Highlights
            if s.get("highlights"):
                typed_blocks.append({"type": "highlights", "items": s["highlights"]})
                
            # 3. Excluded
            if s.get("excluded"):
                typed_blocks.append({"type": "excluded_scope", "items": s["excluded"]})
                
            # 4. Process Steps
            if s.get("process_steps"):
                typed_blocks.append({"type": "process_steps", "steps": s["process_steps"]})
                
            # 5. Aftercare
            if s.get("aftercare"):
                typed_blocks.append({"type": "aftercare_precautions", "aftercare": s["aftercare"]})
                
            # 6. Tools & Materials
            if s.get("tools_materials"):
                typed_blocks.append({"type": "tools_materials", "tools": s["tools_materials"], "materials": []})
                
            # 7. Customer Setup
            if s.get("customer_setup"):
                typed_blocks.append({"type": "customer_setup", "requirements": s["customer_setup"]})
                
            # 8. Expected Results
            if s.get("expected_results"):
                typed_blocks.append({"type": "expected_results", "items": s["expected_results"]})
                
            # 9. Important Notes
            if s.get("important_notes"):
                typed_blocks.append({"type": "important_notes", "items": s["important_notes"]})
                
            # 10. Warranty
            if s.get("warranty"):
                typed_blocks.append({
                    "type": "warranty",
                    "has_warranty": True,
                    "details": s["warranty"]
                })
                
            # 11. FAQs
            if s.get("faqs"):
                typed_blocks.append({"type": "faqs", "items": s["faqs"]})
                
            # 12. Tips
            if s.get("tips"):
                typed_blocks.append({"type": "tips", "items": s["tips"]})
                
            # 13. Dos & Don'ts
            if s.get("dos") or s.get("donts"):
                typed_blocks.append({
                    "type": "dos_donts",
                    "dos": s.get("dos", []),
                    "donts": s.get("donts", [])
                })
                
            # 14. Duration
            if s.get("duration_minutes"):
                typed_blocks.append({"type": "duration", "minutes": s["duration_minutes"]})
                
            # 15. Service Features
            if s.get("service_features"):
                typed_blocks.append({"type": "service_features", "items": s["service_features"]})
                
            # 16. Service Media
            if s.get("service_media"):
                typed_blocks.append({"type": "service_media", "items": s["service_media"]})
                
            # 17. SEO Metadata
            if s.get("seo_metadata"):
                seo = dict(s["seo_metadata"])
                seo["type"] = "seo_metadata"
                typed_blocks.append(seo)
                
            # Combine real addons + typed metadata blocks
            final_suggested_addons = list(existing_real_addons) + typed_blocks
            
            # distinct_features stores the curated inclusions
            distinct_features = s.get("included") or db_df or []
            
            # Step 2: Update in transaction
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
                sid, sname, s["category"], subcat, s["price"], s.get("active", True), 
                json.dumps(distinct_features), json.dumps(final_suggested_addons), 
                20.0, 10.0
            ))
            
            # Step 3: Verification on fresh SELECT within transaction
            cur.execute("""
                SELECT distinct_features, suggested_addons
                FROM services
                WHERE id = %s
            """, (sid,))
            verify_row = cur.fetchone()
            if not verify_row or not verify_row[1]:
                raise Exception(f"Verification failed for service {sname} [{sid}]!")
                
            restored_services.append({
                "id": sid,
                "name": sname,
                "subcategory": subcat,
                "price": float(s["price"]),
                "active": s.get("active", True),
                "distinct_features_count": len(verify_row[0] or []),
                "suggested_addons_count": len(verify_row[1] or []),
                "real_addons_count": len(existing_real_addons)
            })
            print(f"[OK] Restored & Verified: [{subcat}] '{sname}' (Inclusions: {len(distinct_features)}, Addons/Blocks: {len(final_suggested_addons)})")

        # Step 4: Commit entire batch transaction
        conn.commit()
        print("\nAll 23 services successfully committed to PostgreSQL!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] Transaction rolled back due to error: {e}")
        conn.close()
        raise e
        
    conn.close()
    
    # Create Phase 9 post-restore backup file
    out_backup = {
        "backup_type": "category3_post_restore_verified",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_restored": len(restored_services),
        "services": restored_services
    }
    
    os.makedirs("backups", exist_ok=True)
    post_restore_path = os.path.join("backups", "category3_painting_waterproofing_home_improvement_restored.json")
    with open(post_restore_path, "w", encoding="utf-8") as f:
        json.dump(out_backup, f, indent=2, ensure_ascii=False)
    print(f"Saved post-restore backup to: {post_restore_path}")

if __name__ == "__main__":
    restore_category3()
