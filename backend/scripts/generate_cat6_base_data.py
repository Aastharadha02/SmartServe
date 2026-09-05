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
        "included": ["Standard installation", "Basic setup and testing", "Clean up post-service", "System demonstration"],
        "excluded": ["Major structural modifications", "Cost of equipment (unless specified)"],
        "process_steps": [
            {"step_number": 1, "title": "Inspection", "description": "Site inspection for optimal placement"},
            {"step_number": 2, "title": "Installation", "description": "Mounting and wiring of the device"},
            {"step_number": 3, "title": "Configuration", "description": "Connecting the device to the smart network"},
            {"step_number": 4, "title": "Testing", "description": "Functional testing and system verification"},
            {"step_number": 5, "title": "Handover", "description": "Demonstrating usage and safety guidelines to the customer"}
        ],
        "tools_materials": ["Drill machine", "Screwdrivers", "Wire strippers", "Mounting hardware"],
        "customer_setup": ["Ensure Wi-Fi availability", "Provide access to installation points"],
        "aftercare": ["Do not touch exposed wiring before setup is complete", "Keep devices clean from dust"],
        "expected_results": "Fully functional smart home system.",
        "important_notes": "Wi-Fi connectivity issues are not covered under installation warranty.",
        "warranty": "30 days service warranty.",
        "faqs": [
            {"question": "Do you provide the devices?", "answer": "No, this is an installation service only unless specified."},
            {"question": "How long does the installation take?", "answer": "Typically 1 to 2 hours depending on complexity."},
            {"question": "Do I need to be home during the service?", "answer": "Yes, someone needs to be present to grant access and verify the setup."},
            {"question": "Is the installation covered by warranty?", "answer": "Yes, we provide a 30-day service warranty on our work."}
        ],
        "tips": ["Change default passwords immediately after setup."],
        "dos": ["Connect devices to a secure network."],
        "donts": ["Do not expose indoor cameras to outdoor environments."],
        "service_features": ["Expert Technicians", "Secure Setup", "Guaranteed Quality"],
        "service_media": [],
        "seo_metadata": {
            "title": f"Professional {name} Services",
            "description": f"Book expert {name} services for your home.",
            "keywords": [name.lower(), "smart home", "installation"]
        }
    }

def main():
    category = "6. Smart Home & Security"
    
    subcats = [
        ("CCTV/Camera Installation", 7, "bd1b3a20-0001-4000-8000-000000000060"),
        ("Video Doorbells", 5, "bd1b3a20-0002-4000-8000-000000000060"),
        ("Smart Locks & Access Control", 6, "bd1b3a20-0003-4000-8000-000000000060"),
        ("Alarm & Sensor Systems", 7, "bd1b3a20-0004-4000-8000-000000000060"),
        ("Smart Lighting/Switches", 5, "bd1b3a20-0005-4000-8000-000000000060")
    ]
    
    services = []
    for subcat_name, count, base_uuid in subcats:
        for i in range(1, count + 1):
            s_id = generate_variation(base_uuid, i)
            s_name = f"{subcat_name} Service Variation {i}"
            s_desc = f"Professional {subcat_name.lower()} service for your smart home."
            s_price = 1000 + (i * 200)
            s_duration = 60 + (i * 15)
            s_highlights = [f"Expert {subcat_name} setup", "Secure configuration", "Post-installation demo", "24/7 Support available"]
            
            services.append(create_service(
                s_id, s_name, category, subcat_name, s_price, s_duration, s_desc, s_highlights
            ))
            
    # Write to file
    out_dir = os.path.join(os.path.dirname(__file__), "..", "category6_content_builder")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "smart_home_security_data.py")
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write('"""\n')
        f.write('Data file for Category 6: Smart Home & Security.\n')
        f.write('Generated programmatically.\n')
        f.write('"""\n\n')
        
        f.write("SMART_HOME_SERVICES = [\n")
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

    print(f"Successfully generated {len(services)} services for Category 6.")

if __name__ == "__main__":
    main()
