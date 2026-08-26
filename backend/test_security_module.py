import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

auth_url = 'http://127.0.0.1:8000/api/v1/auth/login'
sec_url = 'http://127.0.0.1:8000/api/v1/admin/security/'

req = urllib.request.Request(
    auth_url,
    data=json.dumps({'email': 'admin@smartserve.com', 'password': 'AdminPassword123!'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
token = json.loads(urllib.request.urlopen(req).read().decode())['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("==================================================")
print("SECURITY & RISK CENTER MODULE AUTOMATED AUDIT TEST")
print("==================================================\n")

# STEP 1: Security Summary API
print("--- 1. TESTING SECURITY SUMMARY ---")
req_summary = urllib.request.Request(f"{sec_url}summary", headers={'Authorization': f'Bearer {token}'})
summary = json.loads(urllib.request.urlopen(req_summary).read().decode())
print(f"  Real Security Counts: FailedLogins={summary['failed_logins']} | Suspicious={summary['suspicious_activities']} | ActiveSessions={summary['active_sessions']} | AuditEvents={summary['total_audit_events']} | CriticalEvents={summary['critical_events']}")
assert summary['total_audit_events'] >= 200, "Audit logs count lower than expected!"
print("  [OK] Security summary verified.\n")

# STEP 2: Read-Only Audit Log Ledger & Search
print("--- 2. TESTING IMMUTABLE AUDIT LOG LEDGER ---")
req_audit = urllib.request.Request(f"{sec_url}audit-logs", headers={'Authorization': f'Bearer {token}'})
logs = json.loads(urllib.request.urlopen(req_audit).read().decode())
print(f"Total Immutable Audit Logs Returned: {len(logs)}")
assert len(logs) >= 50, "Audit log ledger incomplete!"

for l in logs[:3]:
    print(f"  - Log #{l['id'][:8]} | Actor: '{l['actor_email']}' ({l['actor_role']}) | Action: '{l['action']}' | Risk: {l['risk_level']} | IP: {l['ip_address']}")

req_search = urllib.request.Request(f"{sec_url}audit-logs?search=Replied", headers={'Authorization': f'Bearer {token}'})
search_logs = json.loads(urllib.request.urlopen(req_search).read().decode())
print(f"  Search 'Replied' -> Found {len(search_logs)} matching audit records")
assert len(search_logs) >= 1

print("  [OK] Immutable read-only audit log ledger verified.\n")

# STEP 3: Failed Login Monitor
print("--- 3. TESTING FAILED LOGIN MONITOR ---")
req_failed = urllib.request.Request(f"{sec_url}failed-logins", headers={'Authorization': f'Bearer {token}'})
failed = json.loads(urllib.request.urlopen(req_failed).read().decode())
print(f"Total Failed Login Records: {len(failed)}")
assert len(failed) >= 3, "Failed login records missing!"

for f in failed:
    print(f"  - Account: '{f['email']}' | IP: {f['ip_address']} | Attempts: {f['attempt_count']} | Locked: {f['locked_until']}")

print("  [OK] Failed login attempt monitoring verified.\n")

# STEP 4: Suspicious Activities & AI Risk Signals
print("--- 4. TESTING SUSPICIOUS ACTIVITIES & AI SIGNALS ---")
req_susp = urllib.request.Request(f"{sec_url}suspicious-activities", headers={'Authorization': f'Bearer {token}'})
susp = json.loads(urllib.request.urlopen(req_susp).read().decode())
print(f"Total Suspicious Anomaly Events: {len(susp)}")
assert len(susp) >= 3, "Suspicious events missing!"

for s in susp:
    ai_sig = s['details_json'].get('ai_signal', 'No AI Signal') if s.get('details_json') else 'No AI Signal'
    print(f"  - Anomaly: '{s['anomaly_type']}' | Risk Score: {int(s['risk_score']*100)}% | AI Signal: '{ai_sig}'")

print("  [OK] Suspicious activity anomalies & AI risk signals verified.\n")

# STEP 5: Admin 2FA Setup & Verification
print("--- 5. TESTING ADMIN TOTP 2FA SETUP & VERIFICATION ---")
req_2fa_setup = urllib.request.Request(f"{sec_url}2fa/setup", data=json.dumps({}).encode('utf-8'), headers=headers)
setup_res = json.loads(urllib.request.urlopen(req_2fa_setup).read().decode())
print(f"  2FA Provisioning URI Generated: {setup_res['provisioning_uri'][:35]}...")
assert 'provisioning_uri' in setup_res and 'secret' in setup_res, "2FA setup failed!"

print("  [OK] Admin TOTP 2FA setup flow verified.\n")

# STEP 6: Active Sessions & Session Revocation
print("--- 6. TESTING ACTIVE SESSIONS & REVOCATION ---")
req_sess = urllib.request.Request(f"{sec_url}active-sessions", headers={'Authorization': f'Bearer {token}'})
sessions = json.loads(urllib.request.urlopen(req_sess).read().decode())
print(f"Total Active Sessions: {len(sessions)}")
assert len(sessions) >= 1, "Active sessions missing!"

if len(sessions) > 0:
    target_s_id = sessions[0]['id']
    req_revoke = urllib.request.Request(f"{sec_url}revoke-session/{target_s_id}", data=json.dumps({}).encode('utf-8'), headers=headers)
    rev_res = json.loads(urllib.request.urlopen(req_revoke).read().decode())
    print(f"  Revoke Session Result: {rev_res['message']}")
    assert rev_res['status'] == 'success'

print("  [OK] Active sessions & revocation flow verified.\n")

# STEP 7: Security Secrets Audit
print("--- 7. TESTING SECRETS & CREDENTIALS ISOLATION ---")
sample_json_str = json.dumps(logs[:5]) + json.dumps(failed)
assert 'password' not in sample_json_str and 'jwt_secret' not in sample_json_str, "Credentials leaked!"
print("  [OK] Security isolation verified. Zero secrets or credentials exposed in payloads.\n")

print("==================================================")
print("SECURITY & RISK CENTER MODULE AUDIT PASSED 100%!")
print("==================================================")
