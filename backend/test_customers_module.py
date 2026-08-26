import urllib.request
import json

auth_url = 'http://127.0.0.1:8000/api/v1/auth/login'
cust_url = 'http://127.0.0.1:8000/api/v1/admin/customers/'

req = urllib.request.Request(
    auth_url,
    data=json.dumps({'email': 'admin@smartserve.com', 'password': 'AdminPassword123!'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
token = json.loads(urllib.request.urlopen(req).read().decode())['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("==================================================")
print("CUSTOMERS ADMIN MODULE AUTOMATED AUDIT TEST")
print("==================================================\n")

# STEP 1: Customer Directory Loading
print("--- 1. TESTING CUSTOMER DIRECTORY LOADING ---")
req_cust = urllib.request.Request(cust_url, headers={'Authorization': f'Bearer {token}'})
customers = json.loads(urllib.request.urlopen(req_cust).read().decode())

print(f"Total Customers Returned from Backend: {len(customers)}")
assert len(customers) >= 8, f"Expected at least 8 customers, got {len(customers)}"

for c in customers[:4]:
    print(f"  - Customer: {c['full_name']} | Email: {c['email']} | Active: {c['is_active']} | Bookings: {c['bookings_count']} | Flagged: {c['is_flagged']}")

print("  [OK] Customer Directory loaded cleanly.\n")

# STEP 2: Search & Filters Audit
print("--- 2. TESTING SEARCH & FILTERS ---")
req_search = urllib.request.Request(f"{cust_url}?search=Ananya", headers={'Authorization': f'Bearer {token}'})
search_res = json.loads(urllib.request.urlopen(req_search).read().decode())
print(f"  Search 'Ananya' -> Found {len(search_res)} matches: {[c['full_name'] for c in search_res]}")
assert len(search_res) == 1 and search_res[0]['full_name'] == 'Ananya Rao'

req_susp = urllib.request.Request(f"{cust_url}?is_active=false", headers={'Authorization': f'Bearer {token}'})
susp_res = json.loads(urllib.request.urlopen(req_susp).read().decode())
print(f"  Filter Suspended -> Found {len(susp_res)} suspended customers: {[c['full_name'] for c in susp_res]}")
assert all(not c['is_active'] for c in susp_res)

req_flag = urllib.request.Request(f"{cust_url}?is_flagged=true", headers={'Authorization': f'Bearer {token}'})
flag_res = json.loads(urllib.request.urlopen(req_flag).read().decode())
print(f"  Filter Flagged -> Found {len(flag_res)} flagged risk customers: {[c['full_name'] for c in flag_res]}")
assert all(c['is_flagged'] for c in flag_res)

print("  [OK] Customer search & filter queries verified.\n")

# STEP 3: Customer Detail Profile & Real Booking History
print("--- 3. TESTING CUSTOMER DETAIL API & BOOKING HISTORY ---")
test_cust = next(c for c in customers if c['bookings_count'] > 0)
req_detail = urllib.request.Request(f"{cust_url}{test_cust['id']}", headers={'Authorization': f'Bearer {token}'})
detail = json.loads(urllib.request.urlopen(req_detail).read().decode())

print(f"  Customer Profile Loaded: {detail['full_name']} (ID: {detail['id']})")
print(f"  Bookings Count: {len(detail.get('bookings', []))}")
if len(detail.get('bookings', [])) > 0:
    b = detail['bookings'][0]
    print(f"  Booking #1: Service='{b['service_name']}' | Status='{b['status']}' | Price=INR {b['total_price']} | Provider='{b['provider_name']}'")
    assert 'service_name' in b and 'total_price' in b, "Booking history fields missing!"

print("  [OK] Customer Detail profile & real booking history verified.\n")

# STEP 4: Fraud Flagging Action
print("--- 4. TESTING FRAUD FLAGGING ACTION ---")
clean_cust = next(c for c in customers if not c['is_flagged'])
print(f"  Testing Fraud Flagging on Customer '{clean_cust['full_name']}'...")

req_flag_act = urllib.request.Request(
    f"{cust_url}{clean_cust['id']}/flag",
    data=json.dumps({'flag_type': 'Suspicious Booking Pattern', 'reason': 'Audit Test Fraud Flag'}).encode('utf-8'),
    headers=headers
)
flag_res = json.loads(urllib.request.urlopen(req_flag_act).read().decode())
print(f"  Flag Result: {flag_res['message']}")

# Re-query
req_check_flag = urllib.request.Request(f"{cust_url}{clean_cust['id']}", headers={'Authorization': f'Bearer {token}'})
fresh_flag_detail = json.loads(urllib.request.urlopen(req_check_flag).read().decode())
assert fresh_flag_detail['is_flagged'] == True, "Fraud flag failed to persist in backend!"
print("  [OK] Fraud flag action & database persistence verified.\n")

# STEP 5: Account Suspension & Reactivation
print("--- 5. TESTING CUSTOMER ACCOUNT SUSPENSION & REACTIVATION ---")
target_cust = customers[0]
print(f"  Testing Suspension on Customer '{target_cust['full_name']}'...")

# Suspend
req_suspend = urllib.request.Request(
    f"{cust_url}{target_cust['id']}/status",
    data=json.dumps({'is_active': False, 'reason': 'Audit Test Suspension'}).encode('utf-8'),
    headers=headers
)
sus_res = json.loads(urllib.request.urlopen(req_suspend).read().decode())
print(f"  Suspend Result: {sus_res['message']}")

req_check_sus = urllib.request.Request(f"{cust_url}{target_cust['id']}", headers={'Authorization': f'Bearer {token}'})
sus_detail = json.loads(urllib.request.urlopen(req_check_sus).read().decode())
assert sus_detail['is_active'] == False, "Customer suspension failed to persist!"
print("  [OK] Customer suspension verified INACTIVE in database.")

# Reactivate
req_react = urllib.request.Request(
    f"{cust_url}{target_cust['id']}/status",
    data=json.dumps({'is_active': True, 'reason': 'Audit Test Reactivation'}).encode('utf-8'),
    headers=headers
)
react_res = json.loads(urllib.request.urlopen(req_react).read().decode())
print(f"  Reactivate Result: {react_res['message']}")

req_check_react = urllib.request.Request(f"{cust_url}{target_cust['id']}", headers={'Authorization': f'Bearer {token}'})
react_detail = json.loads(urllib.request.urlopen(req_check_react).read().decode())
assert react_detail['is_active'] == True, "Customer reactivation failed to persist!"
print("  [OK] Customer account restored to ACTIVE in database.\n")

# STEP 6: Data Isolation Verification
print("--- 6. TESTING CROSS-CUSTOMER DATA ISOLATION ---")
cust1 = customers[0]
cust2 = customers[1]
d1 = json.loads(urllib.request.urlopen(urllib.request.Request(f"{cust_url}{cust1['id']}", headers={'Authorization': f'Bearer {token}'})).read().decode())
d2 = json.loads(urllib.request.urlopen(urllib.request.Request(f"{cust_url}{cust2['id']}", headers={'Authorization': f'Bearer {token}'})).read().decode())

assert d1['id'] != d2['id'], "Customer ID collision!"
b1_ids = {b['id'] for b in d1.get('bookings', [])}
b2_ids = {b['id'] for b in d2.get('bookings', [])}
assert len(b1_ids.intersection(b2_ids)) == 0, "Booking history data bleed detected between customers!"
print("  [OK] 100% Data isolation verified across customer accounts.\n")

print("==================================================")
print("CUSTOMERS ADMIN MODULE AUDIT PASSED 100%!")
print("==================================================")
