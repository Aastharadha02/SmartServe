"""
Removes the 2 stale stub rows from Category 8 that pre-dated our generation:
  - subcategory = 'Language Coaching'  (1 row)
  - subcategory = 'Test Preparation'   (1 row)
These are NOT part of the designed 30-service Category 8 set.
"""
import os, psycopg2
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv

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
cur = conn.cursor()

# Show them first
cur.execute("""
    SELECT id, name, subcategory FROM services
    WHERE category = '8. Education, Teachers & Coaching'
    AND subcategory IN ('Language Coaching', 'Test Preparation');
""")
rows = cur.fetchall()
print(f"Found {len(rows)} stale stub(s) to delete:")
for r in rows:
    print(f"  id={r[0]}  name={r[1]}  subcategory={r[2]}")

cur.execute("""
    DELETE FROM services
    WHERE category = '8. Education, Teachers & Coaching'
    AND subcategory IN ('Language Coaching', 'Test Preparation');
""")
print(f"\nDeleted {cur.rowcount} row(s).")
conn.commit()

# Verify
cur.execute("SELECT COUNT(*) FROM services WHERE category = '8. Education, Teachers & Coaching';")
print(f"Category 8 now has {cur.fetchone()[0]} services.")

cur.execute("SELECT COUNT(*) FROM services;")
print(f"Grand total: {cur.fetchone()[0]} services.")

conn.close()
