import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

auth_url = 'http://127.0.0.1:8000/api/v1/auth/login'
reports_url = 'http://127.0.0.1:8000/api/v1/admin/reports/'

req = urllib.request.Request(
    auth_url,
    data=json.dumps({'email': 'admin@smartserve.com', 'password': 'AdminPassword123!'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
token = json.loads(urllib.request.urlopen(req).read().decode())['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("==================================================")
print("REPORTS & ANALYTICS MODULE AUTOMATED AUDIT TEST")
print("==================================================\n")

# STEP 1: Summary Period Report API
print("--- 1. TESTING PERIOD SUMMARY REPORT ---")
req_summary = urllib.request.Request(f"{reports_url}summary?period=30days", headers={'Authorization': f'Bearer {token}'})
summary = json.loads(urllib.request.urlopen(req_summary).read().decode())

print(f"  Period: {summary['period']} | Total Rev: ₹{summary['total_revenue']} | Period Rev: ₹{summary['period_revenue']}")
print(f"  Bookings: Total={summary['total_bookings']} | Completed={summary['completed_bookings']} | InProgress={summary['in_progress_bookings']} | Cancelled={summary['cancelled_bookings']}")
print(f"  Rates: Completion={summary['completion_rate']}% | Cancellation={summary['cancellation_rate']}% | Avg Booking Val: ₹{summary['average_booking_value']}")
assert summary['total_revenue'] > 0 and summary['completed_bookings'] >= 0

if summary.get('ai_insight'):
    ai = summary['ai_insight']
    print(f"  AI-Assisted Insight: '{ai['title']}' ({ai['confidence_score']}% confidence)")
    assert 'title' in ai and 'confidence_score' in ai

print("  [OK] Summary period report & AI insight verified.\n")

# STEP 2: Date Range Filter Test
print("--- 2. TESTING DATE RANGE FILTERING ---")
req_7d = urllib.request.Request(f"{reports_url}summary?period=7days", headers={'Authorization': f'Bearer {token}'})
summary_7d = json.loads(urllib.request.urlopen(req_7d).read().decode())
print(f"  7 Days Period Revenue: ₹{summary_7d['period_revenue']} vs 30 Days: ₹{summary['period_revenue']}")
assert summary_7d['period_revenue'] != summary['period_revenue']
print("  [OK] Date range filtering verified.\n")

# STEP 3: Provider Performance Scorecard API
print("--- 3. TESTING PROVIDER PERFORMANCE REPORT ---")
req_prov = urllib.request.Request(f"{reports_url}provider-performance", headers={'Authorization': f'Bearer {token}'})
providers = json.loads(urllib.request.urlopen(req_prov).read().decode())
print(f"Total Providers Returned in Scorecard: {len(providers)}")
assert len(providers) >= 1, "Provider scorecard empty!"

for p in providers[:3]:
    print(f"  - Provider: '{p['provider_name']}' | Completed Jobs: {p['completed_jobs']}/{p['total_jobs']} ({p['completion_rate']}%) | Rating: ⭐{p['rating']} | Earnings: ₹{p['earnings']}")

print("  [OK] Provider performance report verified.\n")

# STEP 4: Service Demand Hotspots API
print("--- 4. TESTING SERVICE DEMAND HOTSPOTS REPORT ---")
req_serv = urllib.request.Request(f"{reports_url}service-demand", headers={'Authorization': f'Bearer {token}'})
services = json.loads(urllib.request.urlopen(req_serv).read().decode())
print(f"Total Service Categories Returned: {len(services)}")
assert len(services) >= 1, "Service demand report empty!"

for s in services[:3]:
    print(f"  - Category: '{s['category']}' | Service: '{s['service_name']}' | Bookings: {s['booking_count']} | Revenue: ₹{s['total_revenue']} | Trend: {s['demand_trend']}")

print("  [OK] Service demand hotspots report verified.\n")

# STEP 5: Excel Report Export Test
print("--- 5. TESTING EXCEL REPORT EXPORT ---")
req_excel = urllib.request.Request(f"{reports_url}export/excel", headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req_excel) as resp:
    excel_data = resp.read()
    content_disp = resp.headers.get('Content-Disposition')
    print(f"  Excel Downloaded Size: {len(excel_data)} bytes | Content-Disposition: {content_disp}")
    assert len(excel_data) > 1000 and 'filename=' in content_disp, "Excel report export invalid!"

print("  [OK] Real Excel report export verified.\n")

# STEP 6: PDF Executive Report Export Test
print("--- 6. TESTING EXECUTIVE PDF REPORT EXPORT ---")
req_pdf = urllib.request.Request(f"{reports_url}export/pdf", headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req_pdf) as resp:
    pdf_data = resp.read()
    content_disp = resp.headers.get('Content-Disposition')
    print(f"  PDF Downloaded Size: {len(pdf_data)} bytes | Header: {pdf_data[:5]} | Content-Disposition: {content_disp}")
    assert pdf_data.startswith(b'%PDF-') and 'filename=' in content_disp, "PDF report export invalid!"

print("  [OK] Real PDF executive report export verified.\n")

print("==================================================")
print("REPORTS & ANALYTICS MODULE AUDIT PASSED 100%!")
print("==================================================")
