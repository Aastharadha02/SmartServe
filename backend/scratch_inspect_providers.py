from app.repositories.db import get_db
from sqlalchemy import text

db = next(get_db())
rows = db.execute(text("SELECT column_name, is_nullable, column_default FROM information_schema.columns WHERE table_name = 'providers'")).fetchall()
print("PostgreSQL 'providers' Table Columns:")
for r in rows:
    print(f"  {r[0]}: Nullable={r[1]}, Default={r[2]}")
