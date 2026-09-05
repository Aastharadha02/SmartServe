import os
import uuid
from typing import Dict, Any, List

def generate_variation(base_uuid: str, index: int) -> str:
    namespace = uuid.UUID(base_uuid)
    return str(uuid.uuid5(namespace, f"variation_{index}"))

def create_service(
    base_id: str,
    name: str,
    category: str,
    subcategory: str,
    price: int,
    duration: int,
    description: str,
    highlights: List[str]
) -> Dict[str, Any]:
    return {
        "id": base_id,
        "name": name,
        "category": category,
        "subcategory": subcategory,
        "price": price,
        "duration_minutes": duration,
        "description": description,
        "highlights": highlights,
        "included": ["Initial skill assessment", "Personalized lesson plan", "Interactive sessions", "Progress tracking"],
        "excluded": ["Cost of specialized learning materials", "Transportation costs (for offline sessions)"],
        "process_steps": [
            {"step_number": 1, "title": "Assessment", "description": "Evaluating the student's current proficiency level"},
            {"step_number": 2, "title": "Goal Setting", "description": "Defining clear learning objectives"},
            {"step_number": 3, "title": "Instruction", "description": "Conducting interactive coaching sessions"},
            {"step_number": 4, "title": "Practice", "description": "Assigning exercises to reinforce learning"},
            {"step_number": 5, "title": "Review", "description": "Tracking progress and adjusting the lesson plan"}
        ],
        "tools_materials": ["Notebooks/Digital tablets", "Course material/Syllabus", "Subject-specific tools"],
        "customer_setup": ["Ensure a quiet learning environment", "Provide stable internet for online sessions"],
        "aftercare": ["Complete assigned homework/practice routines", "Review feedback provided by the coach"],
        "expected_results": "Noticeable improvement in skills and knowledge.",
        "important_notes": "Consistent attendance is required for best results.",
        "warranty": "Satisfaction guarantee for the first session.",
        "faqs": [
            {"question": "Are the classes online or offline?", "answer": "We offer both online and offline options depending on the service."},
            {"question": "Are learning materials provided?", "answer": "Basic materials are included; specialized textbooks must be purchased separately."},
            {"question": "How do you track progress?", "answer": "We conduct periodic tests and provide detailed progress reports."},
            {"question": "Can I reschedule a session?", "answer": "Yes, sessions can be rescheduled with 24 hours prior notice."}
        ],
        "tips": ["Set aside dedicated time for self-study to reinforce class learning."],
        "dos": ["Participate actively during sessions.", "Ask questions whenever in doubt."],
        "donts": ["Do not skip practice assignments."],
        "service_features": ["Certified Instructors", "Customized Curriculum", "Flexible Timings"],
        "service_media": [],
        "seo_metadata": {
            "title": f"Professional {name} Classes",
            "description": f"Enroll in expert {name} to boost your skills.",
            "keywords": [name.lower(), "coaching", "tutoring", "education", "classes"]
        }
    }

def main():
    category = "8. Education, Teachers & Coaching"
    
    subcats = [
        ("Academic Tutoring", 7, "bd1b3a20-0001-4000-8000-000000000080"),
        ("Music & Arts", 6, "bd1b3a20-0002-4000-8000-000000000080"),
        ("Test Preparation", 6, "bd1b3a20-0003-4000-8000-000000000080"),
        ("Language Coaching", 6, "bd1b3a20-0004-4000-8000-000000000080"),
        ("Sports & Fitness Coaching", 5, "bd1b3a20-0005-4000-8000-000000000080")
    ]
    
    services = []
    for subcat_name, count, base_uuid in subcats:
        for i in range(1, count + 1):
            s_id = generate_variation(base_uuid, i)
            s_name = f"{subcat_name} Service Variation {i}"
            s_desc = f"Expert {subcat_name.lower()} tailored for your specific learning goals."
            s_price = 800 + (i * 150)
            s_duration = 60 + (i * 15)
            s_highlights = [f"Experienced {subcat_name} Instructor", "Personalized attention", "Flexible scheduling", "Progress monitoring"]
            
            services.append(create_service(
                s_id, s_name, category, subcat_name, s_price, s_duration, s_desc, s_highlights
            ))
            
    # Write to file
    out_dir = os.path.join(os.path.dirname(__file__), "..", "category8_content_builder")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "education_coaching_data.py")
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write('"""\n')
        f.write('Data file for Category 8: Education, Teachers & Coaching.\n')
        f.write('Generated programmatically.\n')
        f.write('"""\n\n')
        
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
