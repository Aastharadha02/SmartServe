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
food = next(s for s in svcs if 'cook' in s['name'].lower())
electrical = next(s for s in svcs if 'socket' in s['name'].lower() or 'switch' in s['name'].lower())
wall = next(s for s in svcs if 'panel' in s['name'].lower())

ped_faqs = [
    {"question": "What does the pedicure include?", "answer": "Includes warm foot soaking, toenail trimming & shaping, cuticle care, foot scrub exfoliation, foot massage, and nail buffing."},
    {"question": "Is nail polish included?", "answer": "Standard nail buffing and regular polish application are included. Gel polish or nail art requires add-on selection."},
    {"question": "How long does the pedicure take?", "answer": "Standard pedicure duration is approximately 45 minutes."},
    {"question": "Is callus care included?", "answer": "Gentle foot filing and callus smoothing are included as part of the scrub step."}
]

food_faqs = [
    {"question": "What does the cooking service include?", "answer": "Includes ingredient prep, custom meal cooking according to taste preferences, and stove/counter cleanup."},
    {"question": "Do I need to supply groceries and spices?", "answer": "Yes, customer provides raw ingredients, cooking oil, and spices."},
    {"question": "Can I request specific dietary preferences?", "answer": "Yes, inform the cook about spice levels, salt preferences, or food allergies before cooking begins."},
    {"question": "Does the cook wash dirty dishes in the sink?", "answer": "Service covers post-cooking stove and counter cleanup; heavy dishwashing can be booked separately."}
]

elec_faqs = [
    {"question": "Does the service fee cover replacement switches?", "answer": "The service fee covers installation labor; replacement switches or sockets are provided by customer or billed separately."},
    {"question": "Will the main power supply be switched off?", "answer": "Yes, electrician will temporarily isolate the main MCB breaker for safety during terminal wiring."},
    {"question": "How long does socket repair take?", "answer": "Standard repair takes approximately 30 to 45 minutes."},
    {"question": "Does the electrician test the socket after installation?", "answer": "Yes, electrician performs voltage and continuity testing using a digital multimeter before clearing the work."}
]

wall_faqs = [
    {"question": "Does the price include wall panel materials?", "answer": "Service covers installation labor; wall panels and border trims are provided by customer or billed separately."},
    {"question": "Do I need to prepare the wall surface beforehand?", "answer": "The installer will clean surface dust, but major wall dampness or plaster cracks should be repaired prior to installation."},
    {"question": "How long does installation take?", "answer": "Standard installation takes approximately 60 to 90 minutes depending on wall area."},
    {"question": "How long does panel adhesive take to cure?", "answer": "Allow panel adhesive to cure undisturbed for 24 hours post installation."}
]

test_cases = [
    (pedicure, ped_faqs, "Beauty (Pedicure)"),
    (food, food_faqs, "Food (Part-Time Cook)"),
    (electrical, elec_faqs, "Electrical (Socket Repair)"),
    (wall, wall_faqs, "Wall Panel Installation")
]

print("==================================================")
print("SECTION 12: MULTI-SERVICE FAQ AUDIT & PERSISTENCE TEST")
print("==================================================\n")

for svc, faqs_list, label in test_cases:
    payload = {
        'name': svc['name'],
        'category': svc['category'],
        'subcategory': svc['subcategory'],
        'base_price': svc['base_price'],
        'suggested_addons': [{'type': 'faqs', 'items': faqs_list}]
    }
    put_req = urllib.request.Request(
        f"http://127.0.0.1:8000/api/v1/admin/catalog/services/{svc['id']}",
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='PUT'
    )
    urllib.request.urlopen(put_req)

req = urllib.request.Request(cat_url, headers={'Authorization': f'Bearer {token}'})
fresh = json.loads(urllib.request.urlopen(req).read().decode())

for svc, faqs_list, label in test_cases:
    match = next(f for f in fresh if f['id'] == svc['id'])
    faqs_stored = next(a for a in match['suggested_addons'] if a.get('type') == 'faqs')['items']
    print(f"--- {label}: {match['name']} ---")
    print(f"  FAQ Count: {len(faqs_stored)}")
    for idx, f in enumerate(faqs_stored):
        print(f"   Q{idx+1}: {f['question']}")
        print(f"   A{idx+1}: {f['answer']}")
    assert len(faqs_stored) == 4, f"Expected 4 FAQs for {label}"
    print(f"  [OK] Service '{label}' passed 4-FAQ persistence & isolation inspection.\n")

# CRUD Test on Pedicure
print("--- TESTING PEDICURE FAQ EDIT & DELETION CRUD ---")
ped_edit = next(f for f in fresh if f['id'] == pedicure['id'])
ped_faqs_items = next(a for a in ped_edit['suggested_addons'] if a.get('type') == 'faqs')['items']

# 1. Edit Q3
ped_faqs_items[2]['answer'] = 'UPDATED: Pedicure session takes exactly 45 minutes.'
# 2. Add Q5
ped_faqs_items.append({"question": "Can I request a specific toenail shape?", "answer": "Yes, inform your aesthetician at the start of your service."})
# 3. Delete Q2
del ped_faqs_items[1]

payload_crud = {
    'name': pedicure['name'],
    'category': pedicure['category'],
    'subcategory': pedicure['subcategory'],
    'base_price': pedicure['base_price'],
    'suggested_addons': [{'type': 'faqs', 'items': ped_faqs_items}]
}
put_req_crud = urllib.request.Request(
    f"http://127.0.0.1:8000/api/v1/admin/catalog/services/{pedicure['id']}",
    data=json.dumps(payload_crud).encode('utf-8'),
    headers=headers,
    method='PUT'
)
urllib.request.urlopen(put_req_crud)

req = urllib.request.Request(cat_url, headers={'Authorization': f'Bearer {token}'})
fresh_crud = json.loads(urllib.request.urlopen(req).read().decode())
ped_crud = next(f for f in fresh_crud if f['id'] == pedicure['id'])
items_crud = next(a for a in ped_crud['suggested_addons'] if a.get('type') == 'faqs')['items']

print(f"Pedicure FAQs after Edit & Delete CRUD (Count: {len(items_crud)}):")
for idx, f in enumerate(items_crud):
    print(f"  Q{idx+1}: {f['question']}")

assert len(items_crud) == 4, "Expected 4 FAQs after CRUD"
assert items_crud[1]['answer'] == 'UPDATED: Pedicure session takes exactly 45 minutes.', "Edit failed"
print("\nSECTION 12 MULTI-SERVICE FAQ AUDIT & PERSISTENCE PASSED 100%!")
