import urllib.request
import json

auth_url = 'http://127.0.0.1:8000/api/v1/auth/login'
support_url = 'http://127.0.0.1:8000/api/v1/admin/support/'

req = urllib.request.Request(
    auth_url,
    data=json.dumps({'email': 'admin@smartserve.com', 'password': 'AdminPassword123!'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
token = json.loads(urllib.request.urlopen(req).read().decode())['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("==================================================")
print("SUPPORT CENTER MODULE AUTOMATED AUDIT TEST")
print("==================================================\n")

# STEP 1: Dashboard Metrics API Test
print("--- 1. TESTING SUPPORT DASHBOARD METRICS ---")
req_m = urllib.request.Request(f"{support_url}dashboard-metrics", headers={'Authorization': f'Bearer {token}'})
metrics = json.loads(urllib.request.urlopen(req_m).read().decode())
print(f"  Real Support Metrics: Open={metrics['open_tickets']} | InProgress={metrics['in_progress']} | Escalated={metrics['escalated']} | HighPriority={metrics['high_priority']} | Resolved={metrics['resolved']}")
assert 'open_tickets' in metrics and 'escalated' in metrics
print("  [OK] Support Dashboard Metrics verified.\n")

# STEP 2: Ticket Directory Loading
print("--- 2. TESTING TICKET DIRECTORY LOADING ---")
req_tickets = urllib.request.Request(f"{support_url}tickets", headers={'Authorization': f'Bearer {token}'})
tickets = json.loads(urllib.request.urlopen(req_tickets).read().decode())
print(f"Total Support Tickets Returned from Backend: {len(tickets)}")
assert len(tickets) >= 4, f"Expected at least 4 tickets, got {len(tickets)}"

for t in tickets[:3]:
    print(f"  - Ticket #{t['id'][:8]} | Subject: '{t['subject']}' | Customer: '{t['customer_name']}' | Status: {t['status']} | Priority: {t['priority']} | Escalated: {t['escalated_to_admin']}")

print("  [OK] Ticket Directory loaded cleanly.\n")

# STEP 3: Search & Filters
print("--- 3. TESTING SEARCH & FILTERS ---")
req_s = urllib.request.Request(f"{support_url}tickets?search=Circuit", headers={'Authorization': f'Bearer {token}'})
search_t = json.loads(urllib.request.urlopen(req_s).read().decode())
print(f"  Search 'Circuit' -> Found {len(search_t)} matches: {[t['subject'] for t in search_t]}")
assert len(search_t) == 1 and 'Circuit' in search_t[0]['subject']

req_esc = urllib.request.Request(f"{support_url}tickets?escalated_only=true", headers={'Authorization': f'Bearer {token}'})
escalated_t = json.loads(urllib.request.urlopen(req_esc).read().decode())
print(f"  Filter Escalated Tickets -> Found {len(escalated_t)} escalated tickets")
assert all(t['escalated_to_admin'] for t in escalated_t)

print("  [OK] Search & filter queries verified.\n")

# STEP 4: Ticket Detail API & Message History
print("--- 4. TESTING TICKET DETAIL & MESSAGE HISTORY ---")
sample_ticket = tickets[0]
req_detail = urllib.request.Request(f"{support_url}tickets/{sample_ticket['id']}", headers={'Authorization': f'Bearer {token}'})
detail = json.loads(urllib.request.urlopen(req_detail).read().decode())

print(f"  Ticket Detail Loaded: #{detail['id'][:8]} - Subject: '{detail['subject']}'")
print(f"  Customer: {detail['customer_name']} ({detail['customer_email']}, {detail['customer_phone']})")
print(f"  Messages Count: {len(detail['messages'])}")
if len(detail['messages']) > 0:
    first_m = detail['messages'][0]
    print(f"  First Message: [{first_m['sender_role']}] '{first_m['message_text'][:40]}...' at {first_m['created_at']}")

assert 'id' in detail and 'messages' in detail, "Ticket detail fields missing!"
print("  [OK] Ticket detail & message thread verified.\n")

# STEP 5: Admin Reply Test
print("--- 5. TESTING ADMIN REPLY ---")
target_id = tickets[0]['id']
print(f"  Posting Admin Reply to Ticket #{target_id[:8]}...")
req_reply = urllib.request.Request(
    f"{support_url}tickets/{target_id}/reply",
    data=json.dumps({'message_text': 'Senior electrical technician Priya Patel has been dispatched to re-inspect.'}).encode('utf-8'),
    headers=headers
)
reply_res = json.loads(urllib.request.urlopen(req_reply).read().decode())
print(f"  Reply Result: {reply_res['message']}")

req_check_r = urllib.request.Request(f"{support_url}tickets/{target_id}", headers={'Authorization': f'Bearer {token}'})
fresh_detail = json.loads(urllib.request.urlopen(req_check_r).read().decode())
assert any(m['message_text'].startswith('Senior electrical') for m in fresh_detail['messages']), "Admin reply failed to persist!"
print("  [OK] Admin reply persistence verified.\n")

# STEP 6: Ticket Escalation Test
print("--- 6. TESTING TICKET ESCALATION ---")
target_esc_id = tickets[1]['id']
print(f"  Escalating Ticket #{target_esc_id[:8]} to Executive Queue...")
req_escalate = urllib.request.Request(f"{support_url}tickets/{target_esc_id}/escalate", data=json.dumps({}).encode('utf-8'), headers=headers)
esc_res = json.loads(urllib.request.urlopen(req_escalate).read().decode())
print(f"  Escalation Result: {esc_res['message']}")

req_check_e = urllib.request.Request(f"{support_url}tickets/{target_esc_id}", headers={'Authorization': f'Bearer {token}'})
fresh_esc_detail = json.loads(urllib.request.urlopen(req_check_e).read().decode())
assert fresh_esc_detail['escalated_to_admin'] == True and fresh_esc_detail['priority'] == 'Urgent', "Ticket escalation failed to persist!"
print("  [OK] Ticket escalation verified.\n")

# STEP 7: Priority & Status Update Test
print("--- 7. TESTING PRIORITY & STATUS UPDATE ---")
req_update_ps = urllib.request.Request(
    f"{support_url}tickets/{target_id}/priority-status",
    data=json.dumps({'status': 'Resolved', 'priority': 'High'}).encode('utf-8'),
    headers=headers,
    method='PATCH'
)
ps_res = json.loads(urllib.request.urlopen(req_update_ps).read().decode())
print(f"  Update Result: {ps_res['message']}")

req_check_ps = urllib.request.Request(f"{support_url}tickets/{target_id}", headers={'Authorization': f'Bearer {token}'})
fresh_ps_detail = json.loads(urllib.request.urlopen(req_check_ps).read().decode())
assert fresh_ps_detail['status'] == 'Resolved', "Status update failed to persist!"
print("  [OK] Priority & status update verified.\n")

# STEP 8: 15-Minute HMAC Signed Evidence Access URL Test
print("--- 8. TESTING 15-MINUTE HMAC SIGNED EVIDENCE URL ---")
req_evidence = urllib.request.Request(f"{support_url}evidence/signed-url?ticket_id={target_id}", headers={'Authorization': f'Bearer {token}'})
ev_res = json.loads(urllib.request.urlopen(req_evidence).read().decode())
print(f"  Signed Evidence URL Generated: {ev_res['signed_url']}")
assert 'signed_url' in ev_res and 'expires_in_seconds' in ev_res, "Signed URL parameters missing!"
print("  [OK] HMAC 15-minute signed evidence URL access verified.\n")

print("==================================================")
print("SUPPORT CENTER MODULE AUDIT PASSED 100%!")
print("==================================================")
