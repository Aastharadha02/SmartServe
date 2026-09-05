import os, uuid

def gen_id(base_uuid, index):
    return str(uuid.uuid5(uuid.UUID(base_uuid), f"variation_{index}"))

STEPS_BIZ = [
    {"step_number": 1, "title": "Requirement Analysis", "description": "Understanding the business challenge or compliance requirement"},
    {"step_number": 2, "title": "Scope Definition", "description": "Defining deliverables, timelines, and pricing"},
    {"step_number": 3, "title": "Service Delivery", "description": "Executing the agreed professional service"},
    {"step_number": 4, "title": "Review & Revision", "description": "Incorporating client feedback and finalising output"},
    {"step_number": 5, "title": "Handover & Documentation", "description": "Delivering all outputs and supporting documentation"},
]

def make_service(sid, name, category, subcategory, price, duration):
    return {
        "id": sid, "name": name, "category": category, "subcategory": subcategory,
        "price": price, "duration_minutes": duration,
        "description": f"Professional {subcategory.lower()} service to help your business grow and stay compliant.",
        "highlights": [f"Experienced {subcategory} professionals", "Government-compliant processes", "Confidential and secure handling", "Dedicated account manager"],
        "included": ["Initial consultation and needs assessment", "Service delivery within agreed timeline", "One round of revisions", "Final documentation and handover"],
        "excluded": ["Government filing fees or registration charges", "Third-party software subscriptions"],
        "process_steps": STEPS_BIZ,
        "tools_materials": ["Professional software (Tally, MS Office, etc.)", "Legal databases", "Secure document portal", "CRM tools"],
        "customer_setup": ["Provide all relevant business documents upfront", "Assign a point of contact for queries", "Ensure digital access for required portals"],
        "aftercare": ["File all received documents securely", "Schedule follow-up compliance reviews annually"],
        "expected_results": "Compliant, efficient, and growth-ready business operations.",
        "important_notes": "All services are subject to applicable government regulations and timelines.",
        "warranty": "Free revision within 7 days if deliverables do not meet agreed specifications.",
        "faqs": [
            {"question": "Is my business data kept confidential?", "answer": "Yes, we follow strict NDAs and data privacy protocols for all client engagements."},
            {"question": "Do you work with startups?", "answer": "Yes, we offer affordable packages specifically designed for startups and SMEs."},
            {"question": "How long does service delivery take?", "answer": "Standard services take 3-7 business days; complex engagements may take longer."},
            {"question": "Can I get a custom package?", "answer": "Absolutely — contact us to build a custom bundle tailored to your business needs."},
        ],
        "tips": ["Keep your tax filings up to date to avoid penalties."],
        "dos": ["Share complete and accurate information for faster processing."],
        "donts": ["Do not delay statutory filings — late fees can be substantial."],
        "service_features": ["Qualified Professionals", "Confidential Handling", "Deadline Guarantee"],
        "service_media": [],
        "seo_metadata": {
            "title": f"Professional {name} Services",
            "description": f"Get expert {name.lower()} for your business.",
            "keywords": [name.lower(), "business services", "professional services", "consulting"],
        },
    }

def main():
    category = "13. Professional & Business Services"
    subcats = [
        ("Accounting & Tax Filing", 6, "bd1b3a20-0001-4000-8000-0000000000d0"),
        ("Legal Documentation",     5, "bd1b3a20-0002-4000-8000-0000000000d0"),
        ("Staffing & HR Services",  5, "bd1b3a20-0003-4000-8000-0000000000d0"),
        ("Marketing & Branding",    6, "bd1b3a20-0004-4000-8000-0000000000d0"),
        ("Business Consulting",     5, "bd1b3a20-0005-4000-8000-0000000000d0"),
        ("Virtual Assistant",       3, "bd1b3a20-0006-4000-8000-0000000000d0"),
    ]
    services = []
    for subcat_name, count, base_uuid in subcats:
        for i in range(1, count + 1):
            sid = gen_id(base_uuid, i)
            name = f"{subcat_name} Service Variation {i}"
            price = 1000 + i * 300
            duration = 60 + i * 30
            services.append(make_service(sid, name, category, subcat_name, price, duration))

    out_dir = os.path.join(os.path.dirname(__file__), "..", "category13_content_builder")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "professional_business_data.py")
    _write(out_file, "PROFESSIONAL_BUSINESS_SERVICES", services)
    print(f"Successfully generated {len(services)} services for Category 13.")

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
