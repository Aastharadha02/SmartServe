import json
import os
import psycopg2
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv

draft_path = 'catalog_drafts/category3_painting_waterproofing_home_improvement_DRAFT.json'
with open(draft_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Category:", data['category'])
print("Status:", data['status'])
print("Total subcategories:", data['total_subcategories'])
print("Total services:", data['total_services'])

contamination_words = [
    'salon', 'facial', 'makeup', 'waxing', 'pedicure', 'manicure', 
    'haircut', 'sofa shampoo', 'cockroach', 'pest control', 'ac service', 
    'refrigerant', 'electrician'
]

total_svcs = 0
for sc in data['subcategories']:
    sc_name = sc['subcategory']
    svcs = sc['services']
    print(f"  - Subcategory: {sc_name} ({len(svcs)} services)")
    for s in svcs:
        total_svcs += 1
        blob = json.dumps(s).lower()
        for cw in contamination_words:
            assert cw not in blob, f"Contamination found in {s['service_name']}: {cw}"

print("Total validated services in DRAFT:", total_svcs)
assert total_svcs == 23

# Check database row counts
load_dotenv()
p = urlparse(os.getenv('DATABASE_URL'))
conn = psycopg2.connect(
    dbname=p.path.lstrip('/'),
    user=p.username,
    password=unquote(p.password),
    host=p.hostname,
    port=p.port
)
cur = conn.cursor()
cur.execute('SELECT count(*) FROM services')
total_services_in_db = cur.fetchone()[0]
cur.execute("SELECT count(*) FROM services WHERE category ILIKE '%painting%'")
cat3_services_in_db = cur.fetchone()[0]

# Check audit logs or recent updates
cur.execute("""
    SELECT count(*) 
    FROM services 
    WHERE category ILIKE '%painting%' 
      AND updated_at > NOW() - INTERVAL '10 minutes'
""")
recent_updated_count = cur.fetchone()[0]

conn.close()

print(f"Total services in DB: {total_services_in_db} (must be 398)")
print(f"Category 3 services in DB: {cat3_services_in_db} (must be 23)")
print(f"Category 3 services updated in last 10 minutes: {recent_updated_count} (must be 0)")

assert total_services_in_db == 398, "Database services count altered!"
assert cat3_services_in_db == 23, "Category 3 count altered!"
assert recent_updated_count == 0, "Database records were modified!"

print("\n>>> ALL VALIDATION CHECKS PASSED: ZERO CONTAMINATION, DATABASE 100% UNMODIFIED! <<<")
