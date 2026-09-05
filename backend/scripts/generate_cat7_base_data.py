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
        "included": ["Initial consultation and assessment", "Professional service execution", "Basic background verified personnel", "Service guarantee"],
        "excluded": ["Cost of groceries or special equipment", "Transportation costs for special errands"],
        "process_steps": [
            {"step_number": 1, "title": "Requirement Gathering", "description": "Understanding specific household needs"},
            {"step_number": 2, "title": "Personnel Matching", "description": "Assigning the right professional for the task"},
            {"step_number": 3, "title": "Service Execution", "description": "Carrying out the requested domestic duties"},
            {"step_number": 4, "title": "Quality Check", "description": "Ensuring the service meets SmartServe standards"},
            {"step_number": 5, "title": "Feedback", "description": "Collecting customer feedback for continuous improvement"}
        ],
        "tools_materials": ["Standard household cleaning tools", "Basic cooking utensils (provided by customer)"],
        "customer_setup": ["Provide access to the premises", "Ensure a safe working environment", "Provide necessary groceries/materials"],
        "aftercare": ["Provide clear instructions for future visits", "Maintain communication regarding preferences"],
        "expected_results": "Reliable and high-quality domestic assistance.",
        "important_notes": "All personnel are background verified for safety and security.",
        "warranty": "Satisfaction guarantee; replacement provided if unsatisfied.",
        "faqs": [
            {"question": "Are the professionals background checked?", "answer": "Yes, all our domestic helpers undergo strict background verification."},
            {"question": "What if I am not satisfied with the service?", "answer": "We offer a replacement guarantee to ensure you get the right match."},
            {"question": "Do I need to provide meals for the helper?", "answer": "No, it is not mandatory to provide meals."},
            {"question": "Can I request the same professional every time?", "answer": "Yes, you can request recurring services with the same professional."}
        ],
        "tips": ["Communicate your specific preferences clearly on the first day."],
        "dos": ["Provide a safe and respectful working environment."],
        "donts": ["Do not request services outside the agreed scope."],
        "service_features": ["Verified Professionals", "Replacement Guarantee", "Flexible Scheduling"],
        "service_media": [],
        "seo_metadata": {
            "title": f"Reliable {name} Services",
            "description": f"Book verified {name} services for your household.",
            "keywords": [name.lower(), "domestic help", "maid", "cook", "babysitter"]
        }
    }

def main():
    category = "7. Domestic Help & Cooking"
    
    subcats = [
        ("Cooks / Chefs", 7, "bd1b3a20-0001-4000-8000-000000000070"),
        ("Maids / Housekeepers", 7, "bd1b3a20-0002-4000-8000-000000000070"),
        ("Nannies / Babysitters", 6, "bd1b3a20-0003-4000-8000-000000000070"),
        ("Elder Care / Patient Care", 6, "bd1b3a20-0004-4000-8000-000000000070"),
        ("Drivers", 4, "bd1b3a20-0005-4000-8000-000000000070")
    ]
    
    services = []
    for subcat_name, count, base_uuid in subcats:
        for i in range(1, count + 1):
            s_id = generate_variation(base_uuid, i)
            s_name = f"{subcat_name} Service Variation {i}"
            s_desc = f"Professional {subcat_name.lower()} service for your household needs."
            s_price = 500 + (i * 100)
            s_duration = 120 + (i * 30)
            s_highlights = [f"Experienced {subcat_name}", "Background verified", "Punctual and reliable", "Replacement guarantee"]
            
            services.append(create_service(
                s_id, s_name, category, subcat_name, s_price, s_duration, s_desc, s_highlights
            ))
            
    # Write to file
    out_dir = os.path.join(os.path.dirname(__file__), "..", "category7_content_builder")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "domestic_help_cooking_data.py")
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write('"""\n')
        f.write('Data file for Category 7: Domestic Help & Cooking.\n')
        f.write('Generated programmatically.\n')
        f.write('"""\n\n')
        
        f.write("DOMESTIC_HELP_SERVICES = [\n")
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

    print(f"Successfully generated {len(services)} services for Category 7.")

if __name__ == "__main__":
    main()
