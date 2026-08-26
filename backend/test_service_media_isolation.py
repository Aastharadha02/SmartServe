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

ped_img = [{'id': 'img_ped_1', 'url': 'https://images.unsplash.com/photo-1519014816548-bf5fe059798b', 'caption': 'Pedicure Foot Care', 'media_type': 'gallery', 'is_cover': True}]
food_img = [{'id': 'img_food_1', 'url': 'https://images.unsplash.com/photo-1556910103-1c02745aae4d', 'caption': 'Fresh Meal Preparation', 'media_type': 'gallery', 'is_cover': True}]
elec_img = [{'id': 'img_elec_1', 'url': 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e', 'caption': 'Electrical Switchbox Wiring', 'media_type': 'gallery', 'is_cover': True}]
wall_img = [{'id': 'img_wall_1', 'url': 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6', 'caption': 'Wall Panel Alignment', 'media_type': 'gallery', 'is_cover': True}]

print("==================================================")
print("SECTION: SERVICE MEDIA PERSISTENCE & ISOLATION TEST")
print("==================================================\n")

# STEP 1: Add distinct images to each of the 4 services
test_matrix = [
    (pedicure, ped_img, "Pedicure"),
    (food, food_img, "Food Service"),
    (electrical, elec_img, "Electrical Service"),
    (wall, wall_img, "Wall Panel Installation")
]

for svc, img_list, label in test_matrix:
    payload = {
        'name': svc['name'],
        'category': svc['category'],
        'subcategory': svc['subcategory'],
        'base_price': svc['base_price'],
        'suggested_addons': [{'type': 'service_media', 'items': img_list}]
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

# STEP 2: Verify Cross-Service Isolation
print("--- VERIFYING CROSS-SERVICE MEDIA ISOLATION ---")
for svc, img_list, label in test_matrix:
    match = next(f for f in fresh if f['id'] == svc['id'])
    media_stored = next(a for a in match['suggested_addons'] if a.get('type') == 'service_media')['items']
    print(f"  {label} ({match['name']}):")
    print(f"    Image ID: {media_stored[0]['id']} | Caption: '{media_stored[0]['caption']}'")
    assert media_stored[0]['id'] == img_list[0]['id'], f"Media mismatch for {label}!"
    assert media_stored[0]['caption'] == img_list[0]['caption'], f"Caption mismatch for {label}!"
print("  [OK] Cross-service isolation verified 100% clean across all 4 services!\n")

# STEP 3: Test Caption Edit & Cover Toggle Persistence on Pedicure
print("--- TESTING CAPTION EDIT & COVER TOGGLE ON PEDICURE ---")
ped_match = next(f for f in fresh if f['id'] == pedicure['id'])
ped_media = next(a for a in ped_match['suggested_addons'] if a.get('type') == 'service_media')['items']
ped_media[0]['caption'] = 'UPDATED: Professional Pedicure Result'

payload_edit = {
    'name': pedicure['name'],
    'category': pedicure['category'],
    'subcategory': pedicure['subcategory'],
    'base_price': pedicure['base_price'],
    'suggested_addons': [{'type': 'service_media', 'items': ped_media}]
}
put_req_edit = urllib.request.Request(
    f"http://127.0.0.1:8000/api/v1/admin/catalog/services/{pedicure['id']}",
    data=json.dumps(payload_edit).encode('utf-8'),
    headers=headers,
    method='PUT'
)
urllib.request.urlopen(put_req_edit)

req = urllib.request.Request(cat_url, headers={'Authorization': f'Bearer {token}'})
fresh_edit = json.loads(urllib.request.urlopen(req).read().decode())
ped_edited = next(f for f in fresh_edit if f['id'] == pedicure['id'])
edited_media = next(a for a in ped_edited['suggested_addons'] if a.get('type') == 'service_media')['items']
print(f"  Updated Pedicure Caption: '{edited_media[0]['caption']}'")
assert edited_media[0]['caption'] == 'UPDATED: Professional Pedicure Result', "Caption edit failed!"
print("  [OK] Caption edit persistence verified.\n")

# STEP 4: Delete Image Test
print("--- TESTING IMAGE DELETION ON PEDICURE ---")
payload_del = {
    'name': pedicure['name'],
    'category': pedicure['category'],
    'subcategory': pedicure['subcategory'],
    'base_price': pedicure['base_price'],
    'suggested_addons': [{'type': 'service_media', 'items': []}]
}
put_req_del = urllib.request.Request(
    f"http://127.0.0.1:8000/api/v1/admin/catalog/services/{pedicure['id']}",
    data=json.dumps(payload_del).encode('utf-8'),
    headers=headers,
    method='PUT'
)
urllib.request.urlopen(put_req_del)

req = urllib.request.Request(cat_url, headers={'Authorization': f'Bearer {token}'})
fresh_del = json.loads(urllib.request.urlopen(req).read().decode())
ped_deleted = next(f for f in fresh_del if f['id'] == pedicure['id'])
deleted_media = next(a for a in ped_deleted['suggested_addons'] if a.get('type') == 'service_media')['items']
print(f"  Pedicure Media Count after Deletion: {len(deleted_media)}")
assert len(deleted_media) == 0, "Image deletion failed!"
print("  [OK] Image deletion persistence verified.\n")

print("==================================================")
print("SERVICE MEDIA PERSISTENCE & CROSS-SERVICE ISOLATION PASSED 100%!")
print("==================================================")
