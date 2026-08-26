import urllib.request
import json

auth_url = 'http://127.0.0.1:8000/api/v1/auth/login'
prov_url = 'http://127.0.0.1:8000/api/v1/admin/providers/'

req = urllib.request.Request(
    auth_url,
    data=json.dumps({'email': 'admin@smartserve.com', 'password': 'AdminPassword123!'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
token = json.loads(urllib.request.urlopen(req).read().decode())['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("==================================================")
print("PROVIDERS ADMIN MODULE AUTOMATED AUDIT TEST")
print("==================================================\n")

# STEP 1: Provider Directory Loading
print("--- 1. TESTING PROVIDER DIRECTORY LOADING ---")
req_prov = urllib.request.Request(prov_url, headers={'Authorization': f'Bearer {token}'})
providers = json.loads(urllib.request.urlopen(req_prov).read().decode())

print(f"Total Providers Returned from Backend: {len(providers)}")
assert len(providers) >= 6, f"Expected at least 6 providers, got {len(providers)}"

for p in providers[:3]:
    print(f"  - Provider: {p['full_name']} | Email: {p['email']} | Category: {p['category']} | Verified: {p['is_verified']} | Active: {p['is_active']}")

print("  [OK] Provider Directory loaded cleanly.\n")

# STEP 2: Search & Filter Audit
print("--- 2. TESTING SEARCH & FILTERS ---")
req_search = urllib.request.Request(f"{prov_url}?search=Rajesh", headers={'Authorization': f'Bearer {token}'})
search_res = json.loads(urllib.request.urlopen(req_search).read().decode())
print(f"  Search 'Rajesh' -> Found {len(search_res)} matches: {[p['full_name'] for p in search_res]}")
assert len(search_res) == 1 and search_res[0]['full_name'] == 'Rajesh Sharma'

req_ver = urllib.request.Request(f"{prov_url}?verification_status=verified", headers={'Authorization': f'Bearer {token}'})
ver_res = json.loads(urllib.request.urlopen(req_ver).read().decode())
print(f"  Filter Verified -> Found {len(ver_res)} verified providers")
assert all(p['is_verified'] for p in ver_res)

print("  [OK] Provider search & filter queries verified.\n")

# STEP 3: Provider Detail Profile API
print("--- 3. TESTING PROVIDER DETAIL API & AI OCR SIGNALS ---")
test_prov = providers[0]
req_detail = urllib.request.Request(f"{prov_url}{test_prov['id']}", headers={'Authorization': f'Bearer {token}'})
detail = json.loads(urllib.request.urlopen(req_detail).read().decode())

print(f"  Provider Profile Loaded: {detail['full_name']} (ID: {detail['id']})")
print(f"  Documents Uploaded: {len(detail['documents'])}")
if len(detail['documents']) > 0:
    doc = detail['documents'][0]
    print(f"  Doc Type: {doc['certificate_type']} | Status: {doc['verification_status']}")
    print(f"  AI OCR Scan Signal: {doc.get('ai_scan_signal')}")
    assert 'recommendation' in doc.get('ai_scan_signal', {}), "AI scan signal missing!"

print("  [OK] Provider Detail profile & AI OCR signals verified.\n")

# STEP 4: Provider Verification Action (Approve / Reject)
print("--- 4. TESTING PROVIDER VERIFICATION ACTION ---")
pending_prov = next((p for p in providers if not p['is_verified']), providers[0])
print(f"  Testing Verification Action on Provider '{pending_prov['full_name']}'...")

req_verify_app = urllib.request.Request(
    f"{prov_url}{pending_prov['id']}/verify",
    data=json.dumps({'verification_status': 'Approved', 'reason': 'Audit Test Approval'}).encode('utf-8'),
    headers=headers
)
verify_res = json.loads(urllib.request.urlopen(req_verify_app).read().decode())
print(f"  Approve Result: {verify_res['message']}")

# Re-query
req_check = urllib.request.Request(f"{prov_url}{pending_prov['id']}", headers={'Authorization': f'Bearer {token}'})
fresh_detail = json.loads(urllib.request.urlopen(req_check).read().decode())
assert fresh_detail['is_verified'] == True, "Verification status failed to persist!"
print("  [OK] Provider Verification action & persistence verified.\n")

# STEP 5: Provider Account Status Action (Suspend / Reactivate)
print("--- 5. TESTING PROVIDER ACCOUNT SUSPENSION / REACTIVATION ---")
target_prov = providers[0]
print(f"  Testing Suspension on Provider '{target_prov['full_name']}'...")

# Suspend
req_suspend = urllib.request.Request(
    f"{prov_url}{target_prov['id']}/status",
    data=json.dumps({'is_active': False, 'reason': 'Audit Test Suspension'}).encode('utf-8'),
    headers=headers
)
sus_res = json.loads(urllib.request.urlopen(req_suspend).read().decode())
print(f"  Suspend Result: {sus_res['message']}")

req_check_sus = urllib.request.Request(f"{prov_url}{target_prov['id']}", headers={'Authorization': f'Bearer {token}'})
sus_detail = json.loads(urllib.request.urlopen(req_check_sus).read().decode())
assert sus_detail['is_active'] == False, "Account suspension failed to persist!"
print("  [OK] Provider suspension verified INACTIVE in database.")

# Reactivate
req_react = urllib.request.Request(
    f"{prov_url}{target_prov['id']}/status",
    data=json.dumps({'is_active': True, 'reason': 'Audit Test Reactivation'}).encode('utf-8'),
    headers=headers
)
react_res = json.loads(urllib.request.urlopen(req_react).read().decode())
print(f"  Reactivate Result: {react_res['message']}")

req_check_react = urllib.request.Request(f"{prov_url}{target_prov['id']}", headers={'Authorization': f'Bearer {token}'})
react_detail = json.loads(urllib.request.urlopen(req_check_react).read().decode())
assert react_detail['is_active'] == True, "Account reactivation failed to persist!"
print("  [OK] Provider account restored to ACTIVE in database.\n")

# STEP 6: Provider Ranking & Dynamic ETA Test
print("--- 6. TESTING PROVIDER RANKING & DYNAMIC ETA ---")
req_rank = urllib.request.Request(f"{prov_url}ranking", headers={'Authorization': f'Bearer {token}'})
rankings = json.loads(urllib.request.urlopen(req_rank).read().decode())
print(f"  Provider Rankings Computed: Total Ranked = {len(rankings)}")
print(f"  #1 Ranked Provider: '{rankings[0]['full_name']}' (Score: {rankings[0]['composite_rank_score']}, Tier: {rankings[0]['rank_tier']})")

req_eta = urllib.request.Request(f"{prov_url}eta-estimate?provider_user_id={target_prov['id']}&distance_km=5.2", headers={'Authorization': f'Bearer {token}'})
eta_res = json.loads(urllib.request.urlopen(req_eta).read().decode())
print(f"  ETA Estimate Computed: Distance = {eta_res['distance_km']} km | Total ETA = {eta_res['total_eta_minutes']} mins | Window = {eta_res['estimated_arrival_window']}")
assert eta_res['total_eta_minutes'] > 0, "ETA estimate failed!"

print("\n==================================================")
print("PROVIDERS ADMIN MODULE AUDIT PASSED 100%!")
print("==================================================")
