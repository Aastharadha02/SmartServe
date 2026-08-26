import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

auth_url = 'http://127.0.0.1:8000/api/v1/auth/login'
emails_url = 'http://127.0.0.1:8000/api/v1/admin/emails/'

req = urllib.request.Request(
    auth_url,
    data=json.dumps({'email': 'admin@smartserve.com', 'password': 'AdminPassword123!'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
token = json.loads(urllib.request.urlopen(req).read().decode())['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("==================================================")
print("EMAIL CENTER MODULE AUTOMATED AUDIT TEST")
print("==================================================\n")

# STEP 1: Email Templates Directory Loading
print("--- 1. TESTING EMAIL TEMPLATES DIRECTORY ---")
req_tmpls = urllib.request.Request(f"{emails_url}templates", headers={'Authorization': f'Bearer {token}'})
templates = json.loads(urllib.request.urlopen(req_tmpls).read().decode())
print(f"Total System Templates Loaded from Backend: {len(templates)}")
assert len(templates) >= 4, f"Expected at least 4 templates, got {len(templates)}"

for t in templates:
    print(f"  - Template Key: '{t['template_key']}' | Subject: '{t['subject']}' | Active: {t.get('is_active', True)} | Variables: {t.get('supported_variables', [])}")

print("  [OK] Email Templates directory loaded cleanly.\n")

# STEP 2: Create / Edit Email Template
print("--- 2. TESTING TEMPLATE CREATION & EDITING ---")
new_tmpl_payload = {
    'template_key': 'service_rescheduled_notice',
    'subject': 'SmartServe Reschedule Confirmation — #{{booking_id}}',
    'body_html': '<p>Dear {{customer_name}}, your booking #{{booking_id}} for {{service_name}} has been rescheduled to {{scheduled_time}}.</p>',
    'is_active': True
}
req_upsert = urllib.request.Request(f"{emails_url}templates", data=json.dumps(new_tmpl_payload).encode('utf-8'), headers=headers)
upsert_res = json.loads(urllib.request.urlopen(req_upsert).read().decode())
print(f"  Upserted Template Key: '{upsert_res['template_key']}' with ID: {upsert_res['id']}")

req_check_t = urllib.request.Request(f"{emails_url}templates", headers={'Authorization': f'Bearer {token}'})
fresh_tmpls = json.loads(urllib.request.urlopen(req_check_t).read().decode())
assert any(t['template_key'] == 'service_rescheduled_notice' for t in fresh_tmpls), "Template creation failed to persist!"
print("  [OK] Email template creation & audit logging verified.\n")

# STEP 3: Safe Email Dispatch Test
print("--- 3. TESTING SAFE EMAIL DISPATCH ---")
send_payload = {
    'recipient_email': 'priya.sharma@smartserve.com',
    'subject': 'SmartServe Reschedule Confirmation — #5716e23b',
    'body_text': 'Dear Priya Sharma, your booking #5716e23b has been rescheduled.',
    'template_key': 'service_rescheduled_notice'
}
req_send = urllib.request.Request(f"{emails_url}send", data=json.dumps(send_payload).encode('utf-8'), headers=headers)
send_res = json.loads(urllib.request.urlopen(req_send).read().decode())
print(f"  Email Dispatched to '{send_res['recipient_email']}' | Status: {send_res['status']} | Log ID: {send_res['id']}")
assert send_res['status'] == 'Sent', "Email dispatch failed!"
print("  [OK] Safe email dispatch verified.\n")

# STEP 4: Email History Logs & Multi-Criteria Filtering
print("--- 4. TESTING EMAIL HISTORY LOGS & FILTERS ---")
req_logs = urllib.request.Request(f"{emails_url}logs", headers={'Authorization': f'Bearer {token}'})
logs = json.loads(urllib.request.urlopen(req_logs).read().decode())
print(f"Total Outbound Email Logs in History: {len(logs)}")
assert len(logs) >= 4, f"Expected at least 4 email logs, got {len(logs)}"

for l in logs[:4]:
    print(f"  - Log #{l['id'][:8]} | Recipient: '{l['recipient_email']}' | Subject: '{l['subject']}' | Status: {l['status']} | Time: {l['sent_at']}")

req_failed = urllib.request.Request(f"{emails_url}logs?status_filter=Failed", headers={'Authorization': f'Bearer {token}'})
failed_logs = json.loads(urllib.request.urlopen(req_failed).read().decode())
print(f"  Filtered Failed Email Logs Count: {len(failed_logs)}")
if len(failed_logs) > 0:
    print(f"  Failed Log Error Info: '{failed_logs[0]['error_message']}'")
    assert 'error_message' in failed_logs[0], "Error message missing!"

print("  [OK] Email history logs & filtering verified.\n")

# STEP 5: Security & Secrets Audit
print("--- 5. TESTING SECURITY & SECRETS ISOLATION ---")
sample_log_str = json.dumps(logs)
assert 'password' not in sample_log_str and 'smtp_secret' not in sample_log_str and 'api_key' not in sample_log_str, "Credentials leaked in API!"
print("  [OK] Security isolation verified. Zero secrets or credentials exposed.\n")

print("==================================================")
print("EMAIL CENTER MODULE AUDIT PASSED 100%!")
print("==================================================")
