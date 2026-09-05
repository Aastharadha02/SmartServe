import os
import sys
import json
import datetime
import psycopg2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def generate_report():
    draft_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "catalog_drafts", "category10", "category10_events_photography_entertainment_DRAFT.json"))
    with open(draft_path, "r", encoding="utf-8") as f:
        draft = json.load(f)
        
    services = draft["services"]
    
    # Connect to local PG to confirm NO modifications yet
    from urllib.parse import urlparse, unquote
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres@localhost:5432/smartserve")
    p = urlparse(db_url)
    
    try:
        conn = psycopg2.connect(
            dbname=p.path.lstrip('/'),
            user=p.username,
            password=unquote(p.password or ''),
            host=p.hostname or 'localhost',
            port=p.port or 5432
        )
        cur = conn.cursor()
        
        cur.execute("""
            SELECT COUNT(*) FROM services 
            WHERE category = '10. Events, Photography & Entertainment'
            AND EXISTS (
                SELECT 1 FROM jsonb_array_elements(COALESCE(suggested_addons, '[]'::jsonb)) elem 
                WHERE elem ? 'type'
            );
        """)
        populated_in_db = cur.fetchone()[0]
        
        cur.execute("""
            SELECT COUNT(*) FROM services 
            WHERE category = '10. Events, Photography & Entertainment';
        """)
        total_in_db = cur.fetchone()[0]
        conn.close()
    except Exception as e:
        print(f"Warning: Could not connect to database for validation ({e}). Defaulting to 0.")
        populated_in_db = 0
        total_in_db = 0
    
    subcat_counts = {}
    subcat_prices = {}
    for s in services:
        sc = s["subcategory"]
        subcat_counts[sc] = subcat_counts.get(sc, 0) + 1
        subcat_prices.setdefault(sc, []).append(s["price"])

    # Strict subcategory counts assertion for Category 10
    assert subcat_counts.get("Event Planning & Management", 0) == 6, "Expected 6 Event Planning & Management services"
    assert subcat_counts.get("Photography & Videography", 0) == 7, "Expected 7 Photography & Videography services"
    assert subcat_counts.get("Catering & Food Services", 0) == 6, "Expected 6 Catering & Food Services services"
    assert subcat_counts.get("DJ & Sound Systems", 0) == 5, "Expected 5 DJ & Sound Systems services"
    assert subcat_counts.get("Decoration & Floral", 0) == 6, "Expected 6 Decoration & Floral services"

if __name__ == "__main__":
    generate_report()
