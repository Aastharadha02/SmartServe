import os
import json

snapshot_path = os.path.join(os.path.dirname(__file__), "..", "backups", "category4_ac_appliance_electronics_repair_pre_change_snapshot.json")
with open(snapshot_path, "r", encoding="utf-8") as f:
    snap = json.load(f)

print(f"Total services in snapshot: {len(snap['services'])}")
by_sub = {}
for s in snap["services"]:
    sub = s["subcategory"]
    if sub not in by_sub:
        by_sub[sub] = []
    by_sub[sub].append({
        "id": s["id"],
        "name": s["name"],
        "price": s["base_price"],
        "addons": s["real_addons"],
        "distinct_features": s["distinct_features"]
    })

map_out = os.path.join(os.path.dirname(__file__), "..", "catalog_drafts", "cat4_reference_map.json")
os.makedirs(os.path.dirname(map_out), exist_ok=True)
with open(map_out, "w", encoding="utf-8") as f:
    json.dump(by_sub, f, indent=2, ensure_ascii=False)

print(f"Saved reference map to {map_out}")
for sub, svcs in sorted(by_sub.items()):
    print(f"{sub} ({len(svcs)} services):")
    for s in svcs:
        print(f"  - {s['name']} (ID: {s['id']}, Price: {s['price']}, Addons: {len(s['addons'])})")
