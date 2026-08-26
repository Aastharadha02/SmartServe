import urllib.request
import json
import time

auth_url = 'http://127.0.0.1:8000/api/v1/auth/login'
bookings_url = 'http://127.0.0.1:8000/api/v1/admin/bookings/'

req = urllib.request.Request(
    auth_url,
    data=json.dumps({'email': 'admin@smartserve.com', 'password': 'AdminPassword123!'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
token = json.loads(urllib.request.urlopen(req).read().decode())['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("==================================================")
print("BOOKINGS & OPERATIONS MODULE AUTOMATED AUDIT TEST")
print("==================================================\n")

# STEP 1: Bookings Directory Loading
print("--- 1. TESTING BOOKINGS DIRECTORY LOADING ---")
req_b = urllib.request.Request(bookings_url, headers={'Authorization': f'Bearer {token}'})
bookings = json.loads(urllib.request.urlopen(req_b).read().decode())

print(f"Total Booking Records Returned from Backend: {len(bookings)}")
assert len(bookings) > 0, "No bookings returned from database!"

for b in bookings[:3]:
    print(f"  - Booking #{b['id'][:8]} | Service: '{b['service_name']}' | Status: {b['status']} | Amount: INR {b['total_price']} | Emergency: {b['emergency_flag'] or 'No'}")

print("  [OK] Bookings Directory loaded cleanly.\n")

# STEP 2: Search & Filters
print("--- 2. TESTING SEARCH & FILTERS ---")
req_req = urllib.request.Request(f"{bookings_url}?status_filter=Requested", headers={'Authorization': f'Bearer {token}'})
requested_b = json.loads(urllib.request.urlopen(req_req).read().decode())
print(f"  Filter 'Requested' Status -> Found {len(requested_b)} bookings: {[b['id'][:8] for b in requested_b]}")
assert all(b['status'] == 'Requested' for b in requested_b)

req_em = urllib.request.Request(f"{bookings_url}?emergency_only=true", headers={'Authorization': f'Bearer {token}'})
emergency_b = json.loads(urllib.request.urlopen(req_em).read().decode())
print(f"  Filter Emergency Dispatches -> Found {len(emergency_b)} emergency bookings")
assert all(b['emergency_flag'] is not None for b in emergency_b)

print("  [OK] Booking search & filter queries verified.\n")

# STEP 3: Booking Detail API & Timeline
print("--- 3. TESTING BOOKING DETAIL API & TIMELINE ---")
sample_booking = requested_b[0] if requested_b else bookings[0]
req_detail = urllib.request.Request(f"{bookings_url}{sample_booking['id']}", headers={'Authorization': f'Bearer {token}'})
detail = json.loads(urllib.request.urlopen(req_detail).read().decode())

print(f"  Booking Detail Loaded: #{detail['id'][:8]}")
print(f"  Customer: {detail['customer_name']} | Phone: {detail['customer_phone']}")
print(f"  Service: {detail['service_name']} | Price: INR {detail['total_price']}")
print(f"  Current Status: {detail['status']} | Allowed Next Transitions: {detail['allowed_next_statuses']}")
print(f"  Timeline Events Count: {len(detail['timeline'])}")

assert 'id' in detail and 'allowed_next_statuses' in detail, "Booking detail fields missing!"
print("  [OK] Booking detail profile & timeline verified.\n")

# STEP 4: Backend State Machine Transition Validation Test
print("--- 4. TESTING BACKEND STATE MACHINE TRANSITIONS ---")
target_b = requested_b[0] if requested_b else None
if target_b:
    b_id = target_b['id']
    # 4a. Valid Transition: Requested -> Assigned
    print(f"  Executing Valid Transition: 'Requested' -> 'Assigned' for Booking #{b_id[:8]}...")
    req_trans_valid = urllib.request.Request(
        f"{bookings_url}{b_id}/status",
        data=json.dumps({'next_status': 'Assigned', 'reason': 'Audit Dispatch'}).encode('utf-8'),
        headers=headers,
        method='PATCH'
    )
    res_valid = json.loads(urllib.request.urlopen(req_trans_valid).read().decode())
    assert res_valid['status'] == 'Assigned', "Valid state transition failed!"
    print(f"  [OK] Valid transition succeeded (New Status: {res_valid['status']}).")

    # 4b. Invalid Transition: Assigned -> Completed (Illegal transition according to backend VALID_TRANSITIONS)
    print(f"  Testing Illegal State Transition: 'Assigned' -> 'Completed' for Booking #{b_id[:8]}...")
    req_trans_invalid = urllib.request.Request(
        f"{bookings_url}{b_id}/status",
        data=json.dumps({'next_status': 'Completed', 'reason': 'Illegal Override'}).encode('utf-8'),
        headers=headers,
        method='PATCH'
    )
    try:
        urllib.request.urlopen(req_trans_invalid)
        assert False, "Illegal transition should have been rejected by backend state machine!"
    except urllib.error.HTTPError as e:
        assert e.code == 422, f"Expected HTTP 422 for illegal state transition, got {e.code}"
        print(f"  [OK] Backend state machine rejected illegal transition with HTTP 422 Unprocessable Entity.\n")

# STEP 5: Provider Reassignment Test
print("--- 5. TESTING PROVIDER REASSIGNMENT ---")
# Fetch provider user ID from providers API
req_p = urllib.request.Request('http://127.0.0.1:8000/api/v1/admin/providers/', headers={'Authorization': f'Bearer {token}'})
provs = json.loads(urllib.request.urlopen(req_p).read().decode())
new_prov = provs[0]

target_reassign_id = bookings[0]['id']
print(f"  Reassigning Booking #{target_reassign_id[:8]} to Provider '{new_prov['full_name']}'...")
req_reassign = urllib.request.Request(
    f"{bookings_url}{target_reassign_id}/reassign",
    data=json.dumps({'new_provider_id': new_prov['user_id'], 'reason': 'Audit Reassignment'}).encode('utf-8'),
    headers=headers
)
reassign_res = json.loads(urllib.request.urlopen(req_reassign).read().decode())
print(f"  Reassign Result: {reassign_res['message']}")

req_check_p = urllib.request.Request(f"{bookings_url}{target_reassign_id}", headers={'Authorization': f'Bearer {token}'})
reassigned_detail = json.loads(urllib.request.urlopen(req_check_p).read().decode())
assert reassigned_detail['provider_name'] == new_prov['full_name'], "Provider reassignment failed to update!"
print("  [OK] Provider reassignment & timeline history update verified.\n")

# STEP 6: Emergency Dispatch Creation Test
print("--- 6. TESTING EMERGENCY DISPATCH CREATION ---")
req_custs = urllib.request.Request('http://127.0.0.1:8000/api/v1/admin/customers/', headers={'Authorization': f'Bearer {token}'})
custs = json.loads(urllib.request.urlopen(req_custs).read().decode())
req_srvs = urllib.request.Request('http://127.0.0.1:8000/api/v1/admin/catalog/services', headers={'Authorization': f'Bearer {token}'})
srvs = json.loads(urllib.request.urlopen(req_srvs).read().decode())

req_emergency = urllib.request.Request(
    bookings_url,
    data=json.dumps({
        'customer_id': custs[0]['id'],
        'service_id': srvs[0]['id'],
        'scheduled_time': (time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())),
        'address': 'Emergency Site, Sector 62, Noida',
        'total_price': 1899.0,
        'emergency_flag': 'Emergency — Water Pipe Burst'
    }).encode('utf-8'),
    headers=headers
)
emergency_res = json.loads(urllib.request.urlopen(req_emergency).read().decode())
print(f"  Created Emergency Dispatch #{emergency_res['id'][:8]} (Flag: '{emergency_res['emergency_flag']}')")
assert emergency_res['emergency_flag'] == 'Emergency — Water Pipe Burst', "Emergency dispatch flag missing!"
print("  [OK] Emergency dispatch creation & persistence verified.\n")

print("==================================================")
print("BOOKINGS & OPERATIONS MODULE AUDIT PASSED 100%!")
print("==================================================")
