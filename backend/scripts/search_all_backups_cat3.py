import os
import json
import re

backup_dir = "backups"
files = os.listdir(backup_dir)

print("Checking backup files for Category 3 service details...")
for f in files:
    path = os.path.join(backup_dir, f)
    if not os.path.isfile(path):
        continue
    
    # Check json files
    if f.endswith(".json"):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as jf:
                data = json.load(jf)
                
            # If it's a list
            svcs = []
            if isinstance(data, list):
                svcs = data
            elif isinstance(data, dict):
                if "services" in data and isinstance(data["services"], list):
                    svcs = data["services"]
                elif "subcategories" in data:
                    for sc in data["subcategories"]:
                        svcs.extend(sc.get("services", []))
                        
            # Check for painting / waterproofing
            cat3_count = 0
            populated_count = 0
            for s in svcs:
                cat = s.get("category", "")
                name = s.get("name") or s.get("service_name", "")
                if any(k in str(cat).lower() for k in ["painting", "waterproofing", "improvement"]):
                    cat3_count += 1
                    # Check if it has description or process_steps or highlights
                    has_desc = bool(s.get("description"))
                    has_proc = bool(s.get("process_steps"))
                    # check if suggested_addons has typed items
                    sa = s.get("suggested_addons", [])
                    typed_sa = [a for a in sa if isinstance(a, dict) and a.get("type")]
                    if has_desc or has_proc or typed_sa:
                        populated_count += 1
            if cat3_count > 0:
                print(f"File {f}: {cat3_count} Cat3 services, {populated_count} have metadata content")
        except Exception as e:
            # print(f"Error reading {f}: {e}")
            pass

    elif f.endswith(".sql"):
        # Search for painting in SQL file
        with open(path, "r", encoding="utf-8", errors="ignore") as sf:
            content = sf.read()
            count = len(re.findall(r"Painting, Waterproofing & Home Improvement", content))
            print(f"SQL file {f}: {count} occurrences of Category 3")
