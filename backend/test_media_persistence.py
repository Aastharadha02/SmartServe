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

ped_m1 = [{
    'id': 'm1',
    'url': 'https://images.unsplash.com/photo-1519014816548-bf5fe059798b',
    'caption': 'Pedicure Foot Soak',
    'media_type': 'gallery',
    'is_cover': True
}]

payload1 = {
    'name': pedicure['name'],
    'category': pedicure['category'],
    'subcategory': pedicure['subcategory'],
    'base_price': pedicure['base_price'],
    'suggested_addons': [{'type': 'service_media', 'items': ped_m1}]
}

put_req = urllib.request.Request(
    f"http://127.0.0.1:8000/api/v1/admin/catalog/services/{pedicure['id']}",
    data=json.dumps(payload1).encode('utf-8'),
    headers=headers,
    method='PUT'
)
urllib.request.urlopen(put_req)

req = urllib.request.Request(cat_url, headers={'Authorization': f'Bearer {token}'})
fresh1 = json.loads(urllib.request.urlopen(req).read().decode())
ped_fresh1 = next(f for f in fresh1 if f['id'] == pedicure['id'])
items1 = next(a for a in ped_fresh1['suggested_addons'] if a.get('type') == 'service_media')['items']
print('STEP 1: Added 1 image to Pedicure. URL:', items1[0]['url'])
assert items1[0]['caption'] == 'Pedicure Foot Soak', 'Caption failed'

ped_m1[0]['caption'] = 'UPDATED: Relaxing Pedicure Foot Soak'
payload2 = {
    'name': pedicure['name'],
    'category': pedicure['category'],
    'subcategory': pedicure['subcategory'],
    'base_price': pedicure['base_price'],
    'suggested_addons': [{'type': 'service_media', 'items': ped_m1}]
}
put_req2 = urllib.request.Request(
    f"http://127.0.0.1:8000/api/v1/admin/catalog/services/{pedicure['id']}",
    data=json.dumps(payload2).encode('utf-8'),
    headers=headers,
    method='PUT'
)
urllib.request.urlopen(put_req2)

req = urllib.request.Request(cat_url, headers={'Authorization': f'Bearer {token}'})
fresh2 = json.loads(urllib.request.urlopen(req).read().decode())
ped_fresh2 = next(f for f in fresh2 if f['id'] == pedicure['id'])
items2 = next(a for a in ped_fresh2['suggested_addons'] if a.get('type') == 'service_media')['items']
print('STEP 2: Updated caption to:', items2[0]['caption'])
assert items2[0]['caption'] == 'UPDATED: Relaxing Pedicure Foot Soak', 'Caption edit failed'

print('STEP 3: Checking Cross-Service Isolation across Food, Electrical, and Wall Panel...')
food_addons = next(f for f in fresh2 if f['id'] == food['id']).get('suggested_addons') or []
elec_addons = next(f for f in fresh2 if f['id'] == electrical['id']).get('suggested_addons') or []
wall_addons = next(f for f in fresh2 if f['id'] == wall['id']).get('suggested_addons') or []

food_media = next((a for a in food_addons if a.get('type') == 'service_media'), None)
elec_media = next((a for a in elec_addons if a.get('type') == 'service_media'), None)
wall_media = next((a for a in wall_addons if a.get('type') == 'service_media'), None)

assert food_media is None or food_media.get('items') != ped_m1, 'BLEEDING DETECTED IN FOOD'
assert elec_media is None or elec_media.get('items') != ped_m1, 'BLEEDING DETECTED IN ELECTRICAL'
assert wall_media is None or wall_media.get('items') != ped_m1, 'BLEEDING DETECTED IN WALL PANEL'
print('CROSS-SERVICE MEDIA ISOLATION VERIFIED 100% CLEAN!')

payload3 = {
    'name': pedicure['name'],
    'category': pedicure['category'],
    'subcategory': pedicure['subcategory'],
    'base_price': pedicure['base_price'],
    'suggested_addons': [{'type': 'service_media', 'items': []}]
}
put_req3 = urllib.request.Request(
    f"http://127.0.0.1:8000/api/v1/admin/catalog/services/{pedicure['id']}",
    data=json.dumps(payload3).encode('utf-8'),
    headers=headers,
    method='PUT'
)
urllib.request.urlopen(put_req3)

req = urllib.request.Request(cat_url, headers={'Authorization': f'Bearer {token}'})
fresh3 = json.loads(urllib.request.urlopen(req).read().decode())
ped_fresh3 = next(f for f in fresh3 if f['id'] == pedicure['id'])
items3 = next(a for a in ped_fresh3['suggested_addons'] if a.get('type') == 'service_media')['items']
print('STEP 4: Deleted image. Remaining count:', len(items3))
assert len(items3) == 0, 'Delete failed'

print('SECTION 16 MEDIA PERSISTENCE & CROSS-SERVICE ISOLATION PASSED 100%!')
