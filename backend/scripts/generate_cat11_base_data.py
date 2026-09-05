import os, uuid

def gen_id(base_uuid, index):
    return str(uuid.uuid5(uuid.UUID(base_uuid), f"variation_{index}"))

STEPS_PET = [
    {"step_number": 1, "title": "Pet Assessment", "description": "Evaluating the pet's breed, temperament, and specific needs"},
    {"step_number": 2, "title": "Service Preparation", "description": "Preparing equipment and a safe environment"},
    {"step_number": 3, "title": "Service Execution", "description": "Delivering the requested pet care service"},
    {"step_number": 4, "title": "Post-Service Check", "description": "Ensuring the pet is comfortable and healthy post-service"},
    {"step_number": 5, "title": "Owner Handover & Tips", "description": "Briefing the owner on aftercare and next steps"},
]

def make_service(sid, name, category, subcategory, price, duration):
    return {
        "id": sid, "name": name, "category": category, "subcategory": subcategory,
        "price": price, "duration_minutes": duration,
        "description": f"Professional {subcategory.lower()} service for the health and happiness of your pet.",
        "highlights": [f"Experienced {subcategory} specialists", "Safe and stress-free environment", "Breed-specific care", "Owner briefing post-service"],
        "included": ["Initial pet assessment", "Service execution by certified pet professional", "Post-service health check", "Owner care tips"],
        "excluded": ["Cost of specialty grooming products", "Veterinary medication costs"],
        "process_steps": STEPS_PET,
        "tools_materials": ["Professional grooming kit", "Pet-safe cleaning products", "First-aid kit", "Leash and harness"],
        "customer_setup": ["Ensure pet has been fed at least 2 hours before grooming", "Provide vaccination records if applicable", "Keep a calm environment during the visit"],
        "aftercare": ["Monitor pet behaviour for 24 hours post-service", "Follow any dietary or medication advice given"],
        "expected_results": "A clean, healthy, and happy pet with improved coat and behaviour.",
        "important_notes": "Aggressive pets may require additional handling precautions — please disclose temperament.",
        "warranty": "Free re-service if quality standards are not met on first visit.",
        "faqs": [
            {"question": "Do you handle all breeds?", "answer": "Yes, our professionals are trained to handle all dog and cat breeds."},
            {"question": "Are the products pet-safe?", "answer": "Absolutely — we only use vet-approved, non-toxic products."},
            {"question": "Can you handle anxious pets?", "answer": "Yes, our groomers are trained in gentle handling for anxious animals."},
            {"question": "Do you offer mobile pet grooming?", "answer": "Yes, we offer in-home mobile grooming services."},
        ],
        "tips": ["Regular grooming every 4-6 weeks keeps your pet's coat healthy."],
        "dos": ["Share your pet's medical history with the professional before each visit."],
        "donts": ["Do not bathe your dog immediately before a grooming appointment."],
        "service_features": ["Certified Pet Professionals", "Pet-Safe Products", "Mobile Service Available"],
        "service_media": [],
        "seo_metadata": {
            "title": f"Professional {name} Services",
            "description": f"Book expert {name.lower()} for your beloved pet.",
            "keywords": [name.lower(), "pet services", "grooming", "dog care"],
        },
    }

def main():
    category = "11. Pet Services"
    subcats = [
        ("Dog Grooming",                6, "bd1b3a20-0001-4000-8000-0000000000b0"),
        ("Pet Sitting & Boarding",      5, "bd1b3a20-0002-4000-8000-0000000000b0"),
        ("Veterinary & Health Checkup", 5, "bd1b3a20-0003-4000-8000-0000000000b0"),
        ("Dog Training",                5, "bd1b3a20-0004-4000-8000-0000000000b0"),
        ("Pet Accessories & Nutrition", 4, "bd1b3a20-0005-4000-8000-0000000000b0"),
    ]
    services = []
    for subcat_name, count, base_uuid in subcats:
        for i in range(1, count + 1):
            sid = gen_id(base_uuid, i)
            name = f"{subcat_name} Service Variation {i}"
            price = 500 + i * 200
            duration = 30 + i * 20
            services.append(make_service(sid, name, category, subcat_name, price, duration))

    out_dir = os.path.join(os.path.dirname(__file__), "..", "category11_content_builder")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "pet_services_data.py")
    _write(out_file, "PET_SERVICES", services)
    print(f"Successfully generated {len(services)} services for Category 11.")

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
