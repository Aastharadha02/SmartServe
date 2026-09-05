import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv('backend/.env')
p = urlparse(os.getenv('DATABASE_URL'))
conn = psycopg2.connect(dbname=p.path.lstrip('/'), user=p.username, password=p.password, host=p.hostname, port=p.port)
cur = conn.cursor()

cur.execute("""
    SELECT category, subcategory, name 
    FROM services 
    WHERE name ILIKE '%option%' OR name ILIKE '%variation%' OR name ~ '[0-9]+$'
    ORDER BY category, subcategory, name;
""")
rows = cur.fetchall()
print(f"Total services with generic or numbered patterns: {len(rows)}")
for cat, sub, name in rows[:30]:
    print(f"[{cat}] {sub} -> {name}")

cur.close()
conn.close()
