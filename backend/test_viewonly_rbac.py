import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_url = 'http://127.0.0.1:8000/api/v1'

print("==========================================================")
print("  FULL VIEW-ONLY NAVBAR & ACTION-LEVEL RBAC AUDIT SUITE")
print("==========================================================\n")

admin_credentials = [
    {'email': 'admin@smartserve.com', 'pwd': 'AdminPassword123!', 'role': 'super_admin'},
    {'email': 'priya.sharma@smartserve.com', 'pwd': 'AdminPassword123!', 'role': 'operations_admin'},
    {'email': 'vikram.patel@smartserve.com', 'pwd': 'AdminPassword123!', 'role': 'catalog_admin'},
    {'email': 'rahul.verma@smartserve.com', 'pwd': 'AdminPassword123!', 'role': 'support_admin'},
]

tokens = {}

# STEP 1: AUTHENTICATE ALL ADMIN ROLES
print("--- 1. AUTHENTICATING ALL ADMIN ROLES ---")
for u in admin_credentials:
    req = urllib.request.Request(
        f"{base_url}/auth/login",
        data=json.dumps({'email': u['email'], 'password': u['pwd']}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res = json.loads(urllib.request.urlopen(req).read().decode())
    tokens[u['email']] = res['access_token']
    print(f"  ✓ Login '{u['email']}': Role='{res['role_name']}' | Permissions count={len(res['permissions'])}")

print("  [OK] Tokens & Sessions successfully issued.\n")

# STEP 2: VERIFY ALL MODULE GET ENDPOINTS (VIEW-ONLY MODE) ARE ACCESSIBLE TO ALL ADMINS
view_endpoints = [
    '/admin/dashboard/overview',
    '/admin/catalog/services?limit=10',
    '/admin/providers/',
    '/admin/customers/',
    '/admin/admins/',
    '/admin/bookings/',
    '/admin/support/dashboard-metrics',
    '/admin/emails/templates',
    '/admin/reports/summary?period=30days',
    '/admin/security/summary',
    '/admin/security/audit-logs'
]

print("--- 2. VERIFYING NAVBAR MODULE GET ACCESSIBILITY FOR ALL ADMIN ROLES ---")
for u in admin_credentials:
    headers = {'Authorization': f"Bearer {tokens[u['email']]}"}
    for ep in view_endpoints:
        req = urllib.request.Request(f"{base_url}{ep}", headers=headers)
        resp = urllib.request.urlopen(req)
        assert resp.status == 200, f"Role {u['role']} failed to view {ep}"
    print(f"  ✓ Role '{u['role']}' ({u['email']}): 100% Navbar GET routes viewable (HTTP 200 OK)")

print("  [OK] View-only navbar data access confirmed for all admin roles.\n")

# STEP 3: VERIFY MUTATION RESTRICTIONS & 403 FORBIDDEN FOR UNAUTHORIZED ACTIONS
print("--- 3. VERIFYING BACKEND 403 FORBIDDEN ON UNAUTHORIZED MUTATIONS ---")

sup_headers = {'Authorization': f"Bearer {tokens['rahul.verma@smartserve.com']}"}
cat_headers = {'Authorization': f"Bearer {tokens['vikram.patel@smartserve.com']}"}

# Fetch a real service ID
req = urllib.request.Request(f"{base_url}/admin/catalog/services?limit=1", headers=sup_headers)
services = json.loads(urllib.request.urlopen(req).read().decode())
real_service_id = services[0]['id'] if services else '00000000-0000-0000-0000-000000000000'

# 1. support_admin trying to edit service catalog item (catalog:edit mutation)
try:
    req = urllib.request.Request(
        f"{base_url}/admin/catalog/services/{real_service_id}",
        data=json.dumps({'name': 'Unauthorized Edit Test', 'base_price': 999}).encode(),
        headers={**sup_headers, 'Content-Type': 'application/json'},
        method='PUT'
    )
    urllib.request.urlopen(req)
    assert False, "support_admin should NOT be allowed to update catalog service!"
except urllib.error.HTTPError as err:
    print(f"  ✓ support_admin PUT /admin/catalog/services/{real_service_id[:8]}...: HTTP {err.code} {err.reason}")
    assert err.code == 403

# 2. catalog_admin trying to create emergency booking (bookings:manage mutation)
try:
    req = urllib.request.Request(
        f"{base_url}/admin/bookings/",
        data=json.dumps({
            'customer_id': '00000000-0000-0000-0000-000000000000',
            'service_id': real_service_id,
            'scheduled_time': '2026-08-30T10:00:00',
            'address': 'Test Address',
            'total_price': 500
        }).encode(),
        headers={**cat_headers, 'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)
    assert False, "catalog_admin should NOT be allowed to create booking!"
except urllib.error.HTTPError as err:
    print(f"  ✓ catalog_admin POST /admin/bookings: HTTP {err.code} {err.reason}")
    assert err.code == 403

# 3. catalog_admin trying to revoke active session (security:manage mutation)
try:
    req = urllib.request.Request(
        f"{base_url}/admin/security/revoke-session/00000000-0000-0000-0000-000000000000",
        data=b'{}',
        headers={**cat_headers, 'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)
    assert False, "catalog_admin should NOT be allowed to revoke sessions!"
except urllib.error.HTTPError as err:
    print(f"  ✓ catalog_admin POST /admin/security/revoke-session: HTTP {err.code} {err.reason}")
    assert err.code == 403

print("  [OK] Backend 403 Forbidden enforcement confirmed for unauthorized mutations.\n")

# STEP 4: VERIFY UNAUTHENTICATED 401 UNAUTHORIZED
print("--- 4. VERIFYING UNAUTHENTICATED ACCESS (401 UNAUTHORIZED) ---")
try:
    req = urllib.request.Request(f"{base_url}/admin/dashboard/overview")
    urllib.request.urlopen(req)
    assert False, "Unauthenticated access should fail!"
except urllib.error.HTTPError as err:
    print(f"  ✓ Unauthenticated access cleanly rejected with HTTP {err.code}: {err.reason}")
    assert err.code == 401

print("==========================================================")
print("  FULL VIEW-ONLY NAVBAR & ACTION-LEVEL RBAC AUDIT PASSED 100%!")
print("==========================================================")
