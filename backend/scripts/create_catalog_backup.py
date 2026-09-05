import os
import sys
import json
import argparse
import datetime
import hashlib
from urllib.parse import urlparse, unquote
import psycopg2
import psycopg2.extras
import requests

BACKUP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups"))
os.makedirs(BACKUP_DIR, exist_ok=True)

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres@localhost:5432/smartserve").replace("postgresql+psycopg2://", "postgresql://")
parsed = urlparse(DATABASE_URL)
DB_HOST = parsed.hostname or "localhost"
DB_PORT = str(parsed.port or "5432")
DB_NAME = parsed.path.lstrip("/") or "smartserve"
DB_USER = parsed.username or "postgres"
DB_PASS = unquote(parsed.password or "")

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

def get_db_connection():
    if DB_HOST not in ["localhost", "127.0.0.1"]:
        raise ValueError(f"SECURITY VIOLATION: Backups can only target local PostgreSQL, not '{DB_HOST}'")
    conn_params = {"host": DB_HOST, "port": DB_PORT, "dbname": DB_NAME, "user": DB_USER}
    if DB_PASS:
        conn_params["password"] = DB_PASS
    return psycopg2.connect(**conn_params)

def get_admin_token():
    try:
        admin_email = os.getenv("ADMIN_EMAIL", "admin@smartserve.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "")
        if not admin_password:
            return None
        res = requests.post(f"{API_BASE_URL}/auth/login", json={
            "email": admin_email,
            "password": admin_password
        }, timeout=5)
        if res.status_code == 200:
            return res.json()["access_token"]
    except Exception:
        pass
    return None

def export_catalog(category=None, subcategory=None, protected_only=False):
    timestamp_slug = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    query = """
        SELECT id, category, subcategory, name, base_price, max_demand_increase,
               max_discount, distinct_features, suggested_addons, is_active,
               created_at, updated_at
        FROM services
    """
    conditions = []
    params = []
    
    label = "catalog_export"
    if protected_only:
        conditions.append("""
            (category ILIKE %s OR category ILIKE %s OR (category ILIKE %s AND subcategory = 'Home Improvement'))
        """)
        params.extend(['%beauty%', '%clean%', '%painting%'])
        label = "protected_catalog_91_services"
    else:
        if category:
            conditions.append("category ILIKE %s")
            params.append(f"%{category}%")
            label = category.lower().replace(" ", "_").replace("&", "and")[:30]
        if subcategory:
            conditions.append("subcategory ILIKE %s")
            params.append(f"%{subcategory}%")
            label += f"_{subcategory.lower().replace(' ', '_')[:30]}"
            
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY category, subcategory, name;"
    
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    if not rows:
        print("No services found matching the criteria.")
        return None
        
    print(f"Exporting {len(rows)} services for '{label}'...")
    token = get_admin_token()
    
    records = []
    sql_updates = []
    for r in rows:
        svc_id = str(r["id"])
        rec = dict(r)
        rec["id"] = svc_id
        rec["created_at"] = rec["created_at"].isoformat() if rec["created_at"] else None
        rec["updated_at"] = rec["updated_at"].isoformat() if rec["updated_at"] else None
        
        # Real addons
        sa = rec.get("suggested_addons") or []
        real_addons = [a for a in sa if isinstance(a, dict) and not a.get("type")]
        rec["real_addons"] = real_addons
        
        # API verification if token available
        if token:
            try:
                api_res = requests.get(f"{API_BASE_URL}/admin/catalog/services/{svc_id}",
                                       headers={"Authorization": f"Bearer {token}"}, timeout=4)
                if api_res.status_code == 200:
                    api_data = api_res.json()
                    rec["api_unpacked_fields"] = {
                        "description": api_data.get("description"),
                        "highlights": api_data.get("highlights"),
                        "included": api_data.get("included"),
                        "excluded": api_data.get("excluded"),
                        "process_steps": api_data.get("process_steps"),
                        "tools_materials": api_data.get("tools_materials"),
                        "customer_setup": api_data.get("customer_setup"),
                        "aftercare": api_data.get("aftercare"),
                        "expected_results": api_data.get("expected_results"),
                        "important_notes": api_data.get("important_notes"),
                        "warranty": api_data.get("warranty"),
                        "faqs": api_data.get("faqs"),
                        "tips": api_data.get("tips"),
                        "dos": api_data.get("dos"),
                        "donts": api_data.get("donts")
                    }
            except Exception:
                pass
                
        records.append(rec)
        
        df_esc = json.dumps(r["distinct_features"]).replace("'", "''")
        sa_esc = json.dumps(r["suggested_addons"]).replace("'", "''")
        sql_updates.append(
            f"UPDATE services SET distinct_features = '{df_esc}'::jsonb, "
            f"suggested_addons = '{sa_esc}'::jsonb, updated_at = NOW() "
            f"WHERE id = '{svc_id}'::uuid;"
        )
        
    json_path = os.path.join(BACKUP_DIR, f"{label}_backup_{timestamp_slug}.json")
    sql_path = os.path.join(BACKUP_DIR, f"{label}_backup_{timestamp_slug}.sql")
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
        
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write(f"-- SmartServe Catalog Snapshot: {label}\n")
        f.write(f"-- Timestamp: {timestamp_slug} | Count: {len(records)} services\n\n")
        f.write("\n\n".join(sql_updates))
        f.write("\n")
        
    print(f"  [SUCCESS] JSON: {json_path} ({os.path.getsize(json_path):,} bytes)")
    print(f"  [SUCCESS] SQL:  {sql_path} ({os.path.getsize(sql_path):,} bytes)")
    return {"json": json_path, "sql": sql_path, "count": len(records)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create category or subcategory catalog backups")
    parser.add_argument("--category", help="Category name filter")
    parser.add_argument("--subcategory", help="Subcategory name filter")
    parser.add_argument("--protected", action="store_true", help="Export all currently protected catalog services")
    args = parser.parse_args()
    
    export_catalog(category=args.category, subcategory=args.subcategory, protected_only=args.protected)
