import os
import psycopg2
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
    
    cur.execute("DELETE FROM services WHERE category = '6. Smart Home & Security' AND subcategory = 'Security Systems';")
    print(f"Deleted {cur.rowcount} row(s).")
    conn.commit()
    conn.close()
except Exception as e:
    print(e)
