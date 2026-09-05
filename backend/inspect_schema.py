import os

database_url = os.getenv("DATABASE_URL", "postgresql://postgres@localhost:5432/smartserve")
conn = psycopg2.connect(database_url)
cur = conn.cursor()

cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
""")
tables = cur.fetchall()
print('Tables in Postgres:', [t[0] for t in tables])

cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'services'
""")
columns = cur.fetchall()
print('\nColumns in services table:')
for c in columns:
    print(f' - {c[0]}: {c[1]} (nullable: {c[2]})')

cur.execute("SELECT * FROM services WHERE name ILIKE '%Recliner Cleaning%'")
row = cur.fetchone()
print('\nRecliner Cleaning full row:')
for col, val in zip([c[0] for c in columns], row):
    print(f'  {col}: {val}')

conn.close()
