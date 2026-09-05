import os, uuid

def gen_id(base_uuid, index):
    return str(uuid.uuid5(uuid.UUID(base_uuid), f"variation_{index}"))

STEPS_TECH = [
    {"step_number": 1, "title": "Diagnosis", "description": "Identifying the root cause of the technical issue"},
    {"step_number": 2, "title": "Solution Planning", "description": "Outlining the fix or upgrade path"},
    {"step_number": 3, "title": "Service Execution", "description": "Carrying out repairs, setup, or development work"},
    {"step_number": 4, "title": "Testing & Verification", "description": "Confirming the solution works correctly"},
    {"step_number": 5, "title": "User Handover", "description": "Demonstrating the fix and advising on best practices"},
]

def make_service(sid, name, category, subcategory, price, duration):
    return {
        "id": sid, "name": name, "category": category, "subcategory": subcategory,
        "price": price, "duration_minutes": duration,
        "description": f"Expert {subcategory.lower()} service to resolve your technology challenges swiftly.",
        "highlights": [f"Certified {subcategory} technician", "On-site and remote support available", "No fix, no charge policy", "Data safety guaranteed"],
        "included": ["Remote or on-site diagnosis", "Service execution and testing", "30-day follow-up support", "Basic user training"],
        "excluded": ["Cost of replacement hardware or parts", "Software licensing fees"],
        "process_steps": STEPS_TECH,
        "tools_materials": ["Diagnostic software", "Screwdriver kit", "Anti-static tools", "Network analyser"],
        "customer_setup": ["Back up important data before the visit", "Ensure stable power supply", "Provide access to router/modem if networking issue"],
        "aftercare": ["Keep OS and software updated regularly", "Use a UPS to prevent power surge damage"],
        "expected_results": "A fully functional device with improved performance and security.",
        "important_notes": "Data loss due to hardware failure is not covered unless data recovery service is booked.",
        "warranty": "30-day service warranty on all repairs; free revisit if same issue reoccurs.",
        "faqs": [
            {"question": "Do you offer remote support?", "answer": "Yes, many issues can be resolved remotely via secure screen-sharing."},
            {"question": "What if the problem cannot be fixed?", "answer": "We follow a no-fix, no-charge policy for diagnosis visits."},
            {"question": "Are my data and privacy safe?", "answer": "Yes, our technicians follow strict data privacy protocols."},
            {"question": "Do you repair all brands?", "answer": "Yes, we service all major brands — Apple, Dell, HP, Lenovo, and more."},
        ],
        "tips": ["Always back up your data weekly to avoid permanent loss."],
        "dos": ["Describe error messages or symptoms clearly to speed up diagnosis."],
        "donts": ["Do not attempt DIY fixes before the technician arrives — it may void the warranty."],
        "service_features": ["Certified Technicians", "Data Safe Guarantee", "Remote & On-Site Support"],
        "service_media": [],
        "seo_metadata": {
            "title": f"Professional {name} Services",
            "description": f"Get reliable {name.lower()} from certified tech experts.",
            "keywords": [name.lower(), "tech support", "IT services", "computer repair"],
        },
    }

def main():
    category = "12. Technology & Digital Services"
    subcats = [
        ("Computer & Laptop Repair", 7, "bd1b3a20-0001-4000-8000-0000000000c0"),
        ("Networking & Wi-Fi Setup",  5, "bd1b3a20-0002-4000-8000-0000000000c0"),
        ("Website & App Development", 6, "bd1b3a20-0003-4000-8000-0000000000c0"),
        ("Data Recovery & Backup",    5, "bd1b3a20-0004-4000-8000-0000000000c0"),
        ("IT Support & Consultation", 7, "bd1b3a20-0005-4000-8000-0000000000c0"),
    ]
    services = []
    for subcat_name, count, base_uuid in subcats:
        for i in range(1, count + 1):
            sid = gen_id(base_uuid, i)
            name = f"{subcat_name} Service Variation {i}"
            price = 500 + i * 200
            duration = 60 + i * 20
            services.append(make_service(sid, name, category, subcat_name, price, duration))

    out_dir = os.path.join(os.path.dirname(__file__), "..", "category12_content_builder")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "technology_digital_data.py")
    _write(out_file, "TECH_DIGITAL_SERVICES", services)
    print(f"Successfully generated {len(services)} services for Category 12.")

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
