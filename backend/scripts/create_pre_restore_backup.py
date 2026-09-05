import os
import json
import datetime
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv
import psycopg2

def backup_pre_restore():
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
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, category, subcategory, name, base_price, max_demand_increase, max_discount, 
               distinct_features, suggested_addons, is_active, created_at, updated_at
        FROM services
        WHERE category ILIKE '%painting%'
        ORDER BY subcategory, name
    """)
    rows = cur.fetchall()
    
    services_list = []
    for r in rows:
        services_list.append({
            "id": str(r[0]),
            "category": r[1],
            "subcategory": r[2],
            "name": r[3],
            "base_price": float(r[4]) if r[4] is not None else 0.0,
            "max_demand_increase": float(r[5]) if r[5] is not None else 0.0,
            "max_discount": float(r[6]) if r[6] is not None else 0.0,
            "distinct_features": r[7] or [],
            "suggested_addons": r[8] or [],
            "is_active": r[9],
            "created_at": r[10].isoformat() if r[10] else None,
            "updated_at": r[11].isoformat() if r[11] else None
        })
    conn.close()
    
    backup_data = {
        "backup_type": "category3_pre_restore_backup",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_services": len(services_list),
        "category": "3. Painting, Waterproofing & Home Improvement",
        "services": services_list
    }
    
    os.makedirs("backups", exist_ok=True)
    out_file = os.path.join("backups", "category3_painting_waterproofing_home_improvement_pre_restore.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)
    print(f"Created pre-restore backup at {out_file} with {len(services_list)} services.")

if __name__ == "__main__":
    backup_pre_restore()
