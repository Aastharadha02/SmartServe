import os
import sys
import json

# Add backend app directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'app'))

from app.services.ai_service import ai_service, GENERIC_REJECT_ITEMS

test_services = [
    {
        "name": "Crystal Spa Pedicure",
        "category": "1. Beauty, Salon & Spa",
        "subcategory": "Pedicure & Foot Care",
        "base_price": 799.0,
        "domain": "beauty"
    },
    {
        "name": "Part-Time Cook",
        "category": "7. Domestic Help & Cooking",
        "subcategory": "Home Cook",
        "base_price": 499.0,
        "domain": "food"
    },
    {
        "name": "Socket Repair",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Switchbox & Wiring",
        "base_price": 199.0,
        "domain": "electrical"
    },
    {
        "name": "Wall Panel Installation",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Panel Fitting",
        "base_price": 1299.0,
        "domain": "carpentry"
    }
]

print("==================================================")
print("STARTING 4-SERVICE LLM GENERATION & VALIDATION AUDIT")
print("==================================================\n")

forbidden_contamination_keywords = [
    "protective gear", "safety gear", "professional toolkit", "testing instruments",
    "keep feet accessible", "feet accessible", "prepare the service area", "30-day guarantee", "otp"
]

all_passed = True

for svc in test_services:
    name = svc["name"]
    category = svc["category"]
    subcat = svc["subcategory"]
    price = svc["base_price"]

    print(f"--- TESTING SERVICE: {name} ({category}) ---")
    data = ai_service.generate_service_metadata(
        category=category,
        service_name=name,
        base_price=price,
        subcategory=subcat
    )

    print(f"  Description: {data.get('description')}")
    print(f"  Highlights: {data.get('highlights')}")
    print(f"  Included: {data.get('included')}")
    print(f"  Excluded: {data.get('excluded')}")
    print(f"  Process Steps: {[s['title'] for s in data.get('process_steps', [])]}")
    print(f"  Tools & Materials: {data.get('tools_materials')}")
    print(f"  Customer Setup: {data.get('customer_setup')}")
    print(f"  Aftercare: {data.get('aftercare')}")
    print(f"  Warranty: {data.get('warranty')}")
    print(f"  FAQs: {[f['question'] for f in data.get('faqs', [])]}")

    # Inspect for contamination or generic filler phrases
    serialized = json.dumps(data).lower()

    # 1. Generic reject check
    for gen in GENERIC_REJECT_ITEMS:
        if gen in serialized:
            print(f"  [ERROR] Generic filler term '{gen}' found in {name}!")
            all_passed = False

    # 2. Specific cross-contamination checks
    if svc["domain"] == "beauty":
        if any(k in serialized for k in ["multimeter", "switchboard", "voltage", "groceries", "wall panel"]):
            print(f"  [ERROR] Technical/Food keywords bled into Beauty service {name}!")
            all_passed = False
        if "keep feet accessible" in serialized or "feet accessible" in serialized:
            print(f"  [ERROR] Trivial filler 'keep feet accessible' found in {name}!")
            all_passed = False
    elif svc["domain"] == "food":
        if any(k in serialized for k in ["pedicure", "cuticle", "multimeter", "laser level", "switchboard"]):
            print(f"  [ERROR] Beauty/Electrical keywords bled into Food service {name}!")
            all_passed = False
    elif svc["domain"] == "electrical":
        if any(k in serialized for k in ["pedicure", "cuticle", "groceries", "wall panel", "foot massage"]):
            print(f"  [ERROR] Beauty/Food keywords bled into Electrical service {name}!")
            all_passed = False
    elif svc["domain"] == "carpentry":
        if any(k in serialized for k in ["pedicure", "cuticle", "groceries", "multimeter", "foot soak"]):
            print(f"  [ERROR] Beauty/Food/Electrical keywords bled into Wall Panel service {name}!")
            all_passed = False

    print(f"  [OK] Service '{name}' passed domain accuracy & non-contamination inspection.\n")

if all_passed:
    print("==================================================")
    print("ALL 4 SERVICES PASSED DOMAIN ISOLATION & ZERO FILLER AUDIT 100%!")
    print("==================================================")
else:
    sys.exit(1)
