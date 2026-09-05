import os, uuid

def gen_id(base_uuid, index):
    return str(uuid.uuid5(uuid.UUID(base_uuid), f"variation_{index}"))

STEPS_EVENTS = [
    {"step_number": 1, "title": "Requirement Briefing", "description": "Understanding event theme, scale, and budget"},
    {"step_number": 2, "title": "Concept & Proposal", "description": "Presenting a tailored event concept and plan"},
    {"step_number": 3, "title": "Vendor Coordination", "description": "Arranging all required vendors and logistics"},
    {"step_number": 4, "title": "Event Execution", "description": "On-ground management and execution on the event day"},
    {"step_number": 5, "title": "Post-Event Wrap-Up", "description": "Clearing up and delivering any media or documentation"},
]

def make_service(sid, name, category, subcategory, price, duration):
    return {
        "id": sid, "name": name, "category": category, "subcategory": subcategory,
        "price": price, "duration_minutes": duration,
        "description": f"Professional {subcategory.lower()} services for unforgettable events.",
        "highlights": [f"Experienced {subcategory} professionals", "End-to-end event support", "Customised packages", "Post-event deliverables"],
        "included": ["Initial consultation and concept planning", "Day-of coordination and support", "Post-event cleanup / media delivery", "Customer satisfaction follow-up"],
        "excluded": ["Third-party vendor costs (unless in package)", "Venue booking charges"],
        "process_steps": STEPS_EVENTS,
        "tools_materials": ["Event planning software", "Professional equipment", "Logistics checklist", "Vendor contact directory"],
        "customer_setup": ["Provide venue details in advance", "Share guest list and requirements", "Confirm timeline and schedule"],
        "aftercare": ["Share feedback to improve future events", "Review delivered photos/videos within 7 days"],
        "expected_results": "A seamlessly executed event with lasting memories.",
        "important_notes": "Minimum advance booking of 7 days required for all events.",
        "warranty": "Reshoot or redo offered if service quality does not meet agreed standards.",
        "faqs": [
            {"question": "How far in advance should I book?", "answer": "At least 7 days in advance for standard events; 30 days for large gatherings."},
            {"question": "Do you handle outdoor events?", "answer": "Yes, we handle both indoor and outdoor events with appropriate equipment."},
            {"question": "Can I customise the package?", "answer": "Absolutely — all our packages are fully customisable to your needs."},
            {"question": "What if it rains on the event day?", "answer": "We have contingency plans and backup equipment for outdoor events."},
        ],
        "tips": ["Book early during wedding or festival season for best availability."],
        "dos": ["Share detailed event requirements upfront to avoid last-minute changes."],
        "donts": ["Do not make last-minute changes to guest count or venue without notice."],
        "service_features": ["Certified Professionals", "Custom Packages", "On-Time Delivery"],
        "service_media": [],
        "seo_metadata": {
            "title": f"Professional {name} Services",
            "description": f"Book top-rated {name.lower()} for your next event.",
            "keywords": [name.lower(), "events", "photography", "entertainment"],
        },
    }

def main():
    category = "10. Events, Photography & Entertainment"
    subcats = [
        ("Event Planning & Management", 6, "bd1b3a20-0001-4000-8000-0000000000a0"),
        ("Photography & Videography",   7, "bd1b3a20-0002-4000-8000-0000000000a0"),
        ("Catering & Food Services",    6, "bd1b3a20-0003-4000-8000-0000000000a0"),
        ("DJ & Sound Systems",          5, "bd1b3a20-0004-4000-8000-0000000000a0"),
        ("Decoration & Floral",         6, "bd1b3a20-0005-4000-8000-0000000000a0"),
    ]
    services = []
    for subcat_name, count, base_uuid in subcats:
        for i in range(1, count + 1):
            sid = gen_id(base_uuid, i)
            name = f"{subcat_name} Service Variation {i}"
            price = 2000 + i * 500
            duration = 120 + i * 30
            services.append(make_service(sid, name, category, subcat_name, price, duration))

    out_dir = os.path.join(os.path.dirname(__file__), "..", "category10_content_builder")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "events_photography_data.py")
    _write(out_file, "EVENTS_PHOTOGRAPHY_SERVICES", services)
    print(f"Successfully generated {len(services)} services for Category 10.")

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
