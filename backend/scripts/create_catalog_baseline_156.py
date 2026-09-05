import os
import sys
import json
import hashlib
import datetime
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv
import psycopg2

def create_baseline_156():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    db_url = os.getenv('DATABASE_URL')
    p = urlparse(db_url)
    conn = psycopg2.connect(
        dbname=p.path.lstrip('/'),
        user=p.username,
        password=unquote(p.password or ''),
        host=p.hostname,
        port=p.port
    )
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, category, subcategory, name, base_price, is_active, distinct_features, suggested_addons
        FROM services
        WHERE category ILIKE '%beauty%' 
           OR category ILIKE '%cleaning%' 
           OR category ILIKE '%painting%'
           OR category ILIKE '%appliance%'
        ORDER BY category, subcategory, name
    """)
    rows = cur.fetchall()
    conn.close()
    
    print(f"Total services fetched for baseline: {len(rows)} (expecting 156: 55 + 32 + 23 + 46)")
    assert len(rows) == 156, f"Expected 156 rows, got {len(rows)}"
    
    services_list = []
    for r in rows:
        sid, cat, subcat, name, price, active, df, sa = r
        addons = sa or []
        real_addons = [a for a in addons if isinstance(a, dict) and not a.get("type") and a.get("name")]
        typed_blocks = [a for a in addons if isinstance(a, dict) and a.get("type")]
        
        services_list.append({
            "id": str(sid),
            "name": name,
            "category": cat,
            "subcategory": subcat,
            "base_price": float(price) if price is not None else 0.0,
            "is_active": active,
            "distinct_features": df or [],
            "suggested_addons": sa or [],
            "real_addons": real_addons,
            "typed_blocks_count": len(typed_blocks)
        })
        
    canonical_json = json.dumps(services_list, sort_keys=True, ensure_ascii=False)
    sha256_hash = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    
    baseline_payload = {
        "baseline_name": "SmartServe Master Catalog Baseline (156 Protected Services)",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_services": len(services_list),
        "sha256_checksum": sha256_hash,
        "category_breakdown": {
            "Category 1 (Beauty, Salon & Spa)": sum(1 for s in services_list if "beauty" in s["category"].lower()),
            "Category 2 (Cleaning & Home Cleaning)": sum(1 for s in services_list if "cleaning" in s["category"].lower()),
            "Category 3 (Painting, Waterproofing & Home Improvement)": sum(1 for s in services_list if "painting" in s["category"].lower()),
            "Category 4 (AC, Appliance & Electronics Repair)": sum(1 for s in services_list if "appliance" in s["category"].lower())
        },
        "services": services_list
    }
    
    out_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "catalog_baseline_156_protected.json"))
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(baseline_payload, f, indent=2, ensure_ascii=False)
        
    print(f"Saved baseline to: {out_file}")
    print(f"Master SHA-256 Checksum: {sha256_hash}")
    for cat, count in baseline_payload["category_breakdown"].items():
        print(f"  * {cat}: {count} services")

if __name__ == "__main__":
    create_baseline_156()
