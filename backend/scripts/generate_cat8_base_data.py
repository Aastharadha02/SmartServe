import os
import uuid
from typing import Dict, Any, List

def gen_id(base_uuid: str, index: int) -> str:
    return str(uuid.uuid5(uuid.UUID(base_uuid), f"variation_{index}"))

def make_service(sid, name, category, subcategory, price, duration, description, highlights) -> Dict[str, Any]:
    return {
        "id": sid,
        "name": name,
        "category": category,
        "subcategory": subcategory,
        "price": price,
        "duration_minutes": duration,
        "description": description,
        "highlights": highlights,
        "included": [
            "Personalised lesson plan preparation",
            "One-on-one or small group sessions",
            "Study material and notes",
            "Progress tracking and feedback reports",
        ],
        "excluded": [
            "Cost of textbooks or printed materials",
            "Examination registration fees",
        ],
        "process_steps": [
            {"step_number": 1, "title": "Initial Assessment", "description": "Evaluating the student's current level and learning goals"},
            {"step_number": 2, "title": "Lesson Planning", "description": "Customising a structured study plan"},
            {"step_number": 3, "title": "Teaching Sessions", "description": "Conducting focused, interactive lessons"},
            {"step_number": 4, "title": "Practice & Assignments", "description": "Providing exercises to reinforce concepts"},
            {"step_number": 5, "title": "Review & Feedback", "description": "Reviewing progress and adjusting the plan as needed"},
        ],
        "tools_materials": ["Whiteboard or digital board", "Reference textbooks", "Practice worksheets", "Online resources"],
        "customer_setup": [
            "Ensure a quiet study environment",
            "Have necessary stationery and books ready",
            "Share syllabus or exam board details upfront",
        ],
        "aftercare": [
            "Complete assigned homework before the next session",
            "Review notes within 24 hours of each session",
        ],
        "expected_results": "Measurable improvement in understanding, grades, and confidence.",
        "important_notes": "Minimum 4-session commitment recommended for meaningful progress.",
        "warranty": "Free rescheduling if tutor cancels; satisfaction guarantee on first session.",
        "faqs": [
            {"question": "Can I choose the tutor?", "answer": "Yes, you can browse tutor profiles and select based on expertise and availability."},
            {"question": "Are online sessions available?", "answer": "Yes, all tutoring services are available both online and in-home."},
            {"question": "What if I want to switch tutors?", "answer": "You can request a replacement tutor at no extra cost within the first session."},
            {"question": "Do you cater to competitive exam preparation?", "answer": "Yes, we have specialised tutors for JEE, NEET, UPSC, CAT, and other exams."},
        ],
        "tips": ["Revise notes within 24 hours to retain 80% more."],
        "dos": ["Attend every session punctually."],
        "donts": ["Do not skip assigned practice work between sessions."],
        "service_features": ["Verified Educators", "Personalised Curriculum", "Progress Reports"],
        "service_media": [],
        "seo_metadata": {
            "title": f"Expert {name} Services",
            "description": f"Book qualified {name.lower()} for your child or self.",
            "keywords": [name.lower(), "tutoring", "education", "coaching"],
        },
    }

def main():
    category = "8. Education, Teachers & Coaching"

    subcats = [
        ("School Tutoring (K-12)", 7, "bd1b3a20-0001-4000-8000-000000000080"),
        ("Competitive Exam Coaching", 7, "bd1b3a20-0002-4000-8000-000000000080"),
        ("Language & Communication", 5, "bd1b3a20-0003-4000-8000-000000000080"),
        ("Music & Arts Lessons", 5, "bd1b3a20-0004-4000-8000-000000000080"),
        ("Skills & Hobby Classes", 6, "bd1b3a20-0005-4000-8000-000000000080"),
    ]

    services = []
    for subcat_name, count, base_uuid in subcats:
        for i in range(1, count + 1):
            sid = gen_id(base_uuid, i)
            name = f"{subcat_name} Service Variation {i}"
            desc = f"Professional {subcat_name.lower()} coaching tailored to individual learning needs."
            price = 500 + i * 150
            duration = 60 + i * 15
            highlights = [
                f"Expert {subcat_name} instructor",
                "Customised lesson plans",
                "Flexible scheduling (online & in-home)",
                "Regular progress reports",
            ]
            services.append(make_service(sid, name, category, subcat_name, price, duration, desc, highlights))

    out_dir = os.path.join(os.path.dirname(__file__), "..", "category8_content_builder")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "education_coaching_data.py")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write('"""\nData file for Category 8: Education, Teachers & Coaching.\nGenerated programmatically.\n"""\n\n')
        f.write("EDUCATION_COACHING_SERVICES = [\n")
        for s in services:
            f.write("    {\n")
            for k, v in s.items():
                if isinstance(v, str):
                    f.write(f'        "{k}": "{v}",\n')
                elif isinstance(v, int):
                    f.write(f'        "{k}": {v},\n')
                else:
                    f.write(f'        "{k}": {repr(v)},\n')
            f.write("    },\n")
        f.write("]\n")

    print(f"Successfully generated {len(services)} services for Category 8.")

if __name__ == "__main__":
    main()
