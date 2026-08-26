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

req = urllib.request.Request(cat_url, headers={'Authorization': f'Bearer {token}'})
svcs = json.loads(urllib.request.urlopen(req).read().decode())

pedicure = next(s for s in svcs if 'pedicure' in s['name'].lower())
wall = next(s for s in svcs if 'panel' in s['name'].lower())

print("==================================================")
print("SECTION 17: ACTIVITY & CHANGE HISTORY AUDIT TEST")
print("==================================================\n")

# 1. Perform changes on Pedicure
print("--- 1. PERFORMING AUDITABLE CHANGES ON PEDICURE ---")
orig_price = pedicure['base_price']
new_price = orig_price + 50.0

# Change Price & Status
payload1 = {
    'name': pedicure['name'],
    'category': pedicure['category'],
    'subcategory': pedicure['subcategory'],
    'base_price': new_price,
    'is_active': False
}
put_req1 = urllib.request.Request(
    f"http://127.0.0.1:8000/api/v1/admin/catalog/services/{pedicure['id']}",
    data=json.dumps(payload1).encode('utf-8'),
    headers=headers,
    method='PUT'
)
urllib.request.urlopen(put_req1)
print(f"  Changed Price: Rs.{orig_price} -> Rs.{new_price} | Status: Inactive")

# Reactivate & Reset Price
payload2 = {
    'name': pedicure['name'],
    'category': pedicure['category'],
    'subcategory': pedicure['subcategory'],
    'base_price': orig_price,
    'is_active': True
}
put_req2 = urllib.request.Request(
    f"http://127.0.0.1:8000/api/v1/admin/catalog/services/{pedicure['id']}",
    data=json.dumps(payload2).encode('utf-8'),
    headers=headers,
    method='PUT'
)
urllib.request.urlopen(put_req2)
print(f"  Reset Price: Rs.{new_price} -> Rs.{orig_price} | Status: Active\n")

# 2. Fetch Pedicure Audit Logs
print("--- 2. FETCHING PEDICURE AUDIT LOGS ---")
audit_url_ped = f"http://127.0.0.1:8000/api/v1/admin/catalog/services/{pedicure['id']}/audit-logs"
req_audit_ped = urllib.request.Request(audit_url_ped, headers={'Authorization': f'Bearer {token}'})
logs_ped = json.loads(urllib.request.urlopen(req_audit_ped).read().decode())

print(f"  Total Pedicure Audit Records Found: {len(logs_ped)}")
for idx, log in enumerate(logs_ped[:3]):
    print(f"  Log #{idx+1}: {log['action']}")
    print(f"    Actor: {log['actor_email']} ({log['actor_role']})")
    print(f"    Timestamp: {log['created_at']}")
    summary = str(log.get('metadata_json', {}).get('changes_summary', '')).replace('₹', 'Rs.')
    print(f"    Changes: {summary}")

assert len(logs_ped) >= 2, "Expected at least 2 audit log entries for Pedicure"
assert logs_ped[0]['actor_email'] == 'admin@smartserve.com', "Actor identity mismatch"
print("  [OK] Pedicure audit log persistence & details verified.\n")

# 3. Cross-Service Isolation Check on Wall Panel Installation
print("--- 3. VERIFYING CROSS-SERVICE AUDIT ISOLATION ON WALL PANEL ---")
audit_url_wall = f"http://127.0.0.1:8000/api/v1/admin/catalog/services/{wall['id']}/audit-logs"
req_audit_wall = urllib.request.Request(audit_url_wall, headers={'Authorization': f'Bearer {token}'})
logs_wall = json.loads(urllib.request.urlopen(req_audit_wall).read().decode())

print(f"  Total Wall Panel Audit Records: {len(logs_wall)}")
ped_log_ids = [l['id'] for l in logs_ped]
for wall_log in logs_wall:
    assert wall_log['id'] not in ped_log_ids, "Cross-service audit log leakage detected!"

print("  [OK] Cross-service audit log isolation verified 100% clean!\n")

print("==================================================")
print("SECTION 17 ACTIVITY & CHANGE HISTORY PASSED 100%!")
print("==================================================")
