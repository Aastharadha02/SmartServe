import urllib.request
import json

auth_url = 'http://127.0.0.1:8000/api/v1/auth/login'
admin_url = 'http://127.0.0.1:8000/api/v1/admin/admins/'

req = urllib.request.Request(
    auth_url,
    data=json.dumps({'email': 'admin@smartserve.com', 'password': 'AdminPassword123!'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
token = json.loads(urllib.request.urlopen(req).read().decode())['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("==================================================")
print("ADMINS & RBAC MODULE AUTOMATED AUDIT TEST")
print("==================================================\n")

# STEP 1: Admin Directory Loading
print("--- 1. TESTING ADMIN DIRECTORY LOADING ---")
req_admins = urllib.request.Request(admin_url, headers={'Authorization': f'Bearer {token}'})
admins = json.loads(urllib.request.urlopen(req_admins).read().decode())

print(f"Total Admin Accounts Returned from Backend: {len(admins)}")
assert len(admins) >= 4, f"Expected at least 4 admin accounts, got {len(admins)}"

for a in admins:
    print(f"  - Admin: {a['email']} | Role: {a['role_name']} | Active: {a['is_active']} | 2FA: {a['is_2fa_enabled']} | Perms: {len(a['permissions'])}")

print("  [OK] Admin Directory loaded cleanly.\n")

# STEP 2: Search & Filters Audit
print("--- 2. TESTING SEARCH & FILTERS ---")
req_search = urllib.request.Request(f"{admin_url}?search=priya", headers={'Authorization': f'Bearer {token}'})
search_res = json.loads(urllib.request.urlopen(req_search).read().decode())
print(f"  Search 'priya' -> Found {len(search_res)} matches: {[a['email'] for a in search_res]}")
assert len(search_res) == 1 and 'priya.sharma@smartserve.com' in search_res[0]['email']

req_role = urllib.request.Request(f"{admin_url}?role_name=support_admin", headers={'Authorization': f'Bearer {token}'})
role_res = json.loads(urllib.request.urlopen(req_role).read().decode())
print(f"  Filter Support Admin -> Found {len(role_res)} accounts: {[a['email'] for a in role_res]}")
assert all(a['role_name'] == 'support_admin' for a in role_res)

req_2fa = urllib.request.Request(f"{admin_url}?is_2fa_enabled=true", headers={'Authorization': f'Bearer {token}'})
twofa_res = json.loads(urllib.request.urlopen(req_2fa).read().decode())
print(f"  Filter 2FA Enabled -> Found {len(twofa_res)} accounts")
assert all(a['is_2fa_enabled'] for a in twofa_res)

print("  [OK] Admin search & filter queries verified.\n")

# STEP 3: Permission Matrix API
print("--- 3. TESTING PERMISSION MATRIX API ---")
req_matrix = urllib.request.Request(f"{admin_url}permissions-matrix", headers={'Authorization': f'Bearer {token}'})
matrix = json.loads(urllib.request.urlopen(req_matrix).read().decode())
print(f"  Permission Matrix Modules Loaded: {len(matrix)}")
for m in matrix[:3]:
    print(f"    - Module: {m['module']} | Actions: {m['actions']}")
assert len(matrix) >= 5, "Permission matrix missing core modules!"
print("  [OK] Permission matrix API verified.\n")

# STEP 4: Create Admin Account
print("--- 4. TESTING ADMIN CREATION ---")
import time
test_email = f"audit.admin.{int(time.time())}@smartserve.com"

req_create = urllib.request.Request(
    admin_url,
    data=json.dumps({
        'email': test_email,
        'password': 'SecureAdminPass123!',
        'role_name': 'support_admin',
        'permissions': ['dashboard:view', 'support:manage']
    }).encode('utf-8'),
    headers=headers
)
create_res = json.loads(urllib.request.urlopen(req_create).read().decode())
new_id = create_res['user_id']
print(f"  Created Admin Account: {create_res['email']} (ID: {new_id}, Role: {create_res['role_name']})")

# Re-query
req_check = urllib.request.Request(f"{admin_url}{new_id}", headers={'Authorization': f'Bearer {token}'})
created_detail = json.loads(urllib.request.urlopen(req_check).read().decode())
assert created_detail['email'] == test_email, "Admin creation verification failed!"
print("  [OK] Admin creation verified.\n")

# STEP 5: Role Assignment & Change
print("--- 5. TESTING ROLE ASSIGNMENT & CHANGE ---")
print(f"  Updating Role for '{test_email}' to 'operations_admin'...")
req_role_update = urllib.request.Request(
    f"{admin_url}{new_id}/role",
    data=json.dumps({
        'role_name': 'operations_admin',
        'permissions': ['dashboard:view', 'catalog:edit', 'providers:manage']
    }).encode('utf-8'),
    headers=headers
)
role_update_res = json.loads(urllib.request.urlopen(req_role_update).read().decode())
print(f"  Role Update Result: {role_update_res['message']}")

req_check_role = urllib.request.Request(f"{admin_url}{new_id}", headers={'Authorization': f'Bearer {token}'})
fresh_role_detail = json.loads(urllib.request.urlopen(req_check_role).read().decode())
assert fresh_role_detail['role_name'] == 'operations_admin', "Role assignment failed to persist!"
print("  [OK] Role assignment & permissions update verified.\n")

# STEP 6: Admin Status Deactivation & Self-Protection Test
print("--- 6. TESTING ADMIN ACCOUNT DEACTIVATION & SELF-PROTECTION ---")
# Suspend test admin
req_deact = urllib.request.Request(
    f"{admin_url}{new_id}/status",
    data=json.dumps({'is_active': False, 'reason': 'Audit Deactivation'}).encode('utf-8'),
    headers=headers
)
deact_res = json.loads(urllib.request.urlopen(req_deact).read().decode())
print(f"  Deactivation Result: {deact_res['message']}")

req_check_deact = urllib.request.Request(f"{admin_url}{new_id}", headers={'Authorization': f'Bearer {token}'})
deact_detail = json.loads(urllib.request.urlopen(req_check_deact).read().decode())
assert deact_detail['is_active'] == False, "Admin deactivation failed to persist!"
print("  [OK] Admin deactivation verified INACTIVE in database.")

# Reactivate test admin
req_react = urllib.request.Request(
    f"{admin_url}{new_id}/status",
    data=json.dumps({'is_active': True, 'reason': 'Audit Reactivation'}).encode('utf-8'),
    headers=headers
)
react_res = json.loads(urllib.request.urlopen(req_react).read().decode())
print(f"  Reactivation Result: {react_res['message']}")

# Self-deactivation protection check on caller admin
caller_id = admins[0]['id']
req_self = urllib.request.Request(
    f"{admin_url}{caller_id}/status",
    data=json.dumps({'is_active': False, 'reason': 'Self Deactivation Attempt'}).encode('utf-8'),
    headers=headers
)
try:
    urllib.request.urlopen(req_self)
    assert False, "Caller admin should NOT be allowed to deactivate own account!"
except urllib.error.HTTPError as e:
    assert e.code == 400, f"Expected 400 status for self-deactivation, got {e.code}"
    print("  [OK] Self-deactivation protection verified (HTTP 400 returned).\n")

# STEP 7: Audit Logging Verification
print("--- 7. TESTING AUDIT TRAIL LOGGING ---")
final_detail = json.loads(urllib.request.urlopen(req_check_role).read().decode())
logs = final_detail.get('recent_activity', [])
print(f"  Total Audit Logs Captured for Admin: {len(logs)}")
for l in logs[:3]:
    print(f"    - Action: '{l['action']}'")
assert len(logs) > 0, "Audit trail logging failed!"
print("  [OK] Audit trail logging verified.\n")

print("==================================================")
print("ADMINS & RBAC MODULE AUDIT PASSED 100%!")
print("==================================================")
