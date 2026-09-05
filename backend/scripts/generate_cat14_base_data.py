import os, uuid

def gen_id(base_uuid, index):
    return str(uuid.uuid5(uuid.UUID(base_uuid), f"variation_{index}"))

STEPS_MOVE = [
    {"step_number": 1, "title": "Pre-Move Survey", "description": "Assessing volume, fragile items, and special requirements"},
    {"step_number": 2, "title": "Packing", "description": "Carefully packing all items with appropriate materials"},
    {"step_number": 3, "title": "Loading & Transport", "description": "Safely loading and transporting to the destination"},
    {"step_number": 4, "title": "Unloading & Placement", "description": "Unloading and placing items as per customer instructions"},
    {"step_number": 5, "title": "Final Check & Clean-Up", "description": "Verifying all items are delivered and removing packing waste"},
]

def make_service(sid, name, category, subcategory, price, duration):
    return {
        "id": sid, "name": name, "category": category, "subcategory": subcategory,
        "price": price, "duration_minutes": duration,
        "description": f"Reliable {subcategory.lower()} services for a smooth and stress-free move.",
        "highlights": [f"Trained {subcategory} professionals", "GPS-tracked vehicles", "Fully insured service", "Damage-free guarantee"],
        "included": ["Pre-move survey and planning", "Packing materials (basic)", "Loading, transport, and unloading", "Post-delivery clean-up"],
        "excluded": ["Cost of premium packing materials (bubble wrap, crates)", "Storage charges beyond 24 hours"],
        "process_steps": STEPS_MOVE,
        "tools_materials": ["Moving blankets and straps", "Trolleys and dollies", "Packing tape and boxes", "GPS-enabled truck"],
        "customer_setup": ["Sort and label boxes before the team arrives", "Disconnect appliances 24 hours before moving day", "Ensure parking access at both locations"],
        "aftercare": ["Check all items against inventory within 24 hours", "Report any damage within 48 hours for warranty claim"],
        "expected_results": "A damage-free, on-time move with all belongings safely delivered.",
        "important_notes": "Insurance coverage applies to standard household goods only; valuables should be declared upfront.",
        "warranty": "Free damage resolution within 48 hours of delivery if items are found damaged.",
        "faqs": [
            {"question": "Do you provide packing materials?", "answer": "Yes, basic packing materials are included; premium options are available at extra cost."},
            {"question": "Are my belongings insured during transit?", "answer": "Yes, all items are covered under transit insurance up to a declared value."},
            {"question": "Can you move heavy or oversized furniture?", "answer": "Yes, our teams are equipped to move all types of furniture and appliances."},
            {"question": "How do I track my shipment?", "answer": "You will receive a live GPS tracking link once the vehicle departs."},
        ],
        "tips": ["Label all boxes by room name to speed up unpacking."],
        "dos": ["Declare high-value items before the move for proper insurance coverage."],
        "donts": ["Do not overload boxes — it increases the risk of damage."],
        "service_features": ["GPS Tracked Vehicles", "Transit Insurance", "Damage-Free Guarantee"],
        "service_media": [],
        "seo_metadata": {
            "title": f"Professional {name} Services",
            "description": f"Book trusted {name.lower()} for a stress-free relocation.",
            "keywords": [name.lower(), "moving", "packers and movers", "delivery"],
        },
    }

def main():
    category = "14. Moving, Delivery & Local Assistance"
    subcats = [
        ("Home Shifting & Packing",    7, "bd1b3a20-0001-4000-8000-0000000000e0"),
        ("Vehicle Transport",          5, "bd1b3a20-0002-4000-8000-0000000000e0"),
        ("Last-Mile Delivery",         5, "bd1b3a20-0003-4000-8000-0000000000e0"),
        ("Junk Removal & Disposal",    5, "bd1b3a20-0004-4000-8000-0000000000e0"),
        ("Local Errands & Assistance", 5, "bd1b3a20-0005-4000-8000-0000000000e0"),
    ]
    services = []
    for subcat_name, count, base_uuid in subcats:
        for i in range(1, count + 1):
            sid = gen_id(base_uuid, i)
            name = f"{subcat_name} Service Variation {i}"
            price = 1000 + i * 400
            duration = 120 + i * 30
            services.append(make_service(sid, name, category, subcat_name, price, duration))

    out_dir = os.path.join(os.path.dirname(__file__), "..", "category14_content_builder")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "moving_delivery_data.py")
    _write(out_file, "MOVING_DELIVERY_SERVICES", services)
    print(f"Successfully generated {len(services)} services for Category 14.")

def _write(path, var_name, services):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f'"""\nData file auto-generated.\n"""\n\n{var_name} = [\n')
        for s in services:
            f.write("    {\n")
            for k, v in s.items():
                f.write(f'        "{k}": {repr(v)},\n')
            f.write("    },\n")
        f.write("]\n")

if __name__ == "__main__":
    main()
