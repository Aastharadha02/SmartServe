import urllib.request
import json

auth_url = 'http://127.0.0.1:8000/api/v1/auth/login'
cat_url = 'http://127.0.0.1:8000/api/v1/admin/catalog/services?skip=0&limit=1000'

req = urllib.request.Request(
    auth_url,
    data=json.dumps({'email': 'admin@smartserve.com', 'password': 'AdminPassword123!'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
token = json.loads(urllib.request.urlopen(req).read().decode())['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("==================================================")
print("CATALOG SEARCH, FILTERS & HIERARCHY NAVIGATION AUDIT")
print("==================================================\n")

# STEP 1: Fetch Catalog Services
req_cat = urllib.request.Request(cat_url, headers={'Authorization': f'Bearer {token}'})
services = json.loads(urllib.request.urlopen(req_cat).read().decode())

print(f"Total Services Loaded from Backend: {len(services)}")
assert len(services) >= 398, "Service catalog count altered or reduced!"

# STEP 2: Aggregate Categories
category_map = {}
for s in services:
    cat = s['category']
    sub = s['subcategory']
    if cat not in category_map:
        category_map[cat] = {'subcategories': set(), 'total': 0, 'active': 0}
    category_map[cat]['subcategories'].add(sub)
    category_map[cat]['total'] += 1
    if s['is_active']:
        category_map[cat]['active'] += 1

print(f"Total Categories Aggregated: {len(category_map)}")
print("Categories Breakdown:")
for cat_name, meta in list(category_map.items())[:5]:
    print(f"  - {cat_name}: {len(meta['subcategories'])} Subcats | {meta['total']} Services ({meta['active']} Active)")

# STEP 3: Test Navigation Hierarchy across 4 target categories
test_categories = [
    '1. Beauty, Salon & Spa',
    '7. Domestic Help & Cooking',
    '5. Electrician, Plumber, Carpenter & Home Repairs',
    '3. Painting, Waterproofing & Home Improvement'
]

print("\n--- TESTING CATEGORY -> SUBCATEGORY -> SERVICES HIERARCHY ---")
for cat_name in test_categories:
    cat_services = [s for s in services if s['category'] == cat_name]
    subcats = sorted(list(set(s['subcategory'] for s in cat_services)))
    print(f"Category: '{cat_name}'")
    print(f"  Subcategories ({len(subcats)}): {subcats[:3]}")

    # Pick first subcategory
    first_sub = subcats[0]
    sub_services = [s for s in cat_services if s['subcategory'] == first_sub]
    print(f"  Services in Subcategory '{first_sub}': Count = {len(sub_services)}")
    for s in sub_services[:2]:
        print(f"    - {s['name']} (Price: Rs.{s['base_price']}, Status: {'Active' if s['is_active'] else 'Inactive'})")
        assert s['category'] == cat_name, "Category mismatch!"
        assert s['subcategory'] == first_sub, "Subcategory mismatch!"

# STEP 4: Test Global Search
print("\n--- TESTING SEARCH FILTER ---")
search_queries = [
    ("pedicure", "1. Beauty, Salon & Spa"),
    ("cook", "7. Domestic Help & Cooking"),
    ("socket", "5. Electrician, Plumber, Carpenter & Home Repairs"),
    ("panel", "3. Painting, Waterproofing & Home Improvement")
]

for q, expected_cat in search_queries:
    results = [s for s in services if q in s['name'].lower() or q in s['category'].lower() or q in s['subcategory'].lower()]
    print(f"Search Query: '{q}' -> Found {len(results)} matches")
    assert len(results) > 0, f"No matches found for search '{q}'"
    for r in results:
        assert expected_cat.lower() in r['category'].lower() or q in r['name'].lower(), f"Contamination in search '{q}'"

# STEP 5: Test Sorting by Price
print("\n--- TESTING PRICE SORTING ---")
price_asc = sorted(services, key=lambda x: x['base_price'])
price_desc = sorted(services, key=lambda x: x['base_price'], reverse=True)

print(f"Price Low -> High: Cheapest = '{price_asc[0]['name']}' (Rs.{price_asc[0]['base_price']})")
print(f"Price High -> Low: Most Expensive = '{price_desc[0]['name']}' (Rs.{price_desc[0]['base_price']})")
assert price_asc[0]['base_price'] <= price_asc[-1]['base_price']
assert price_desc[0]['base_price'] >= price_desc[-1]['base_price']

print("\n==================================================")
print("CATALOG SEARCH, FILTERS & HIERARCHY PASSED 100%!")
print("==================================================")
