import os, uuid
from typing import Dict, Any, List

def gen_id(base_uuid: str, index: int) -> str:
    return str(uuid.uuid5(uuid.UUID(base_uuid), f"variation_{index}"))

def make_service(sid, name, category, subcategory, price, duration, description,
                 highlights, included, excluded, steps, tools, setup, aftercare,
                 expected, notes, warranty, faqs, tips, dos, donts) -> Dict[str, Any]:
    return {
        "id": sid, "name": name, "category": category, "subcategory": subcategory,
        "price": price, "duration_minutes": duration, "description": description,
        "highlights": highlights, "included": included, "excluded": excluded,
        "process_steps": steps, "tools_materials": tools, "customer_setup": setup,
        "aftercare": aftercare, "expected_results": expected, "important_notes": notes,
        "warranty": warranty, "faqs": faqs, "tips": tips, "dos": dos, "donts": donts,
        "service_features": ["Certified Professionals", "Guaranteed Quality", "Flexible Scheduling"],
        "service_media": [],
        "seo_metadata": {
            "title": f"Professional {name} Services",
            "description": f"Book certified {name.lower()} for your health and wellness needs.",
            "keywords": [name.lower(), "health", "fitness", "wellness"],
        },
    }

STEPS_HEALTH = [
    {"step_number": 1, "title": "Initial Consultation", "description": "Assessing health goals, medical history, and current fitness level"},
    {"step_number": 2, "title": "Plan Design", "description": "Creating a customised programme tailored to specific needs"},
    {"step_number": 3, "title": "Session Execution", "description": "Conducting guided sessions with professional supervision"},
    {"step_number": 4, "title": "Progress Monitoring", "description": "Tracking improvements and adjusting the programme"},
    {"step_number": 5, "title": "Follow-Up & Review", "description": "Reviewing outcomes and setting next phase goals"},
]

def main():
    category = "9. Health, Fitness & Wellness"
    subcats = [
        ("Personal Training",            7, "bd1b3a20-0001-4000-8000-000000000090"),
        ("Yoga & Meditation",            6, "bd1b3a20-0002-4000-8000-000000000090"),
        ("Physiotherapy & Rehabilitation", 6, "bd1b3a20-0003-4000-8000-000000000090"),
        ("Nutrition & Diet Counselling", 5, "bd1b3a20-0004-4000-8000-000000000090"),
        ("Mental Wellness & Counselling", 6, "bd1b3a20-0005-4000-8000-000000000090"),
    ]
    services = []
    for subcat_name, count, base_uuid in subcats:
        for i in range(1, count + 1):
            sid = gen_id(base_uuid, i)
            name = f"{subcat_name} Service Variation {i}"
            desc = f"Professional {subcat_name.lower()} service designed for holistic well-being."
            price = 800 + i * 150
            duration = 45 + i * 15
            services.append(make_service(
                sid, name, category, subcat_name, price, duration, desc,
                highlights=[f"Certified {subcat_name} specialist", "Personalised programme", "Home or studio visits available", "Progress tracking included"],
                included=["Initial health assessment", "Customised session plan", "Post-session feedback", "Digital progress report"],
                excluded=["Gym membership or equipment costs", "Prescription medications"],
                steps=STEPS_HEALTH,
                tools=["Assessment forms", "Exercise equipment (as required)", "Nutritional guides", "Digital tracking tools"],
                setup=["Wear comfortable clothing", "Ensure adequate space for sessions", "Keep hydrated"],
                aftercare=["Follow post-session cool-down routines", "Adhere to recommended diet and rest"],
                expected="Improved fitness levels, reduced pain, and enhanced mental well-being.",
                notes="Please disclose any medical conditions before sessions begin.",
                warranty="Free rescheduling for trainer cancellations; first-session satisfaction guarantee.",
                faqs=[
                    {"question": "Do I need prior experience?", "answer": "No prior experience is needed; programmes are tailored to all fitness levels."},
                    {"question": "Can sessions happen at my home?", "answer": "Yes, we offer in-home, studio, and online sessions."},
                    {"question": "How soon will I see results?", "answer": "Most clients notice improvements within 4-6 weeks with consistent sessions."},
                    {"question": "Are the professionals certified?", "answer": "Yes, all our health professionals hold valid certifications from recognised bodies."},
                ],
                tips=["Stay consistent — even 3 sessions per week makes a significant difference."],
                dos=["Communicate openly about pain or discomfort during sessions."],
                donts=["Do not skip prescribed rest days."],
            ))

    out_dir = os.path.join(os.path.dirname(__file__), "..", "category9_content_builder")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "health_fitness_data.py")
    _write(out_file, "HEALTH_FITNESS_SERVICES", services)
    print(f"Successfully generated {len(services)} services for Category 9.")

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
