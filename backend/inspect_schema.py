import sys
import os
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
backend_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(backend_dir, ".env"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sqlalchemy import inspect
from app.repositories.db import engine

def main():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables in PostgreSQL:", tables)

    for table in sorted(tables):
        print(f"\n=== Table: {table} ===")
        cols = inspector.get_columns(table)
        for c in cols:
            pk = " [PK]" if c.get("primary_key") else ""
            nullable = "NULL" if c.get("nullable") else "NOT NULL"
            print(f"  - {c['name']}: {c['type']} {nullable}{pk}")
        fks = inspector.get_foreign_keys(table)
        if fks:
            for fk in fks:
                print(f"  -> FK ({', '.join(fk['constrained_columns'])}) references {fk['referred_table']}({', '.join(fk['referred_columns'])})")

if __name__ == "__main__":
    main()
