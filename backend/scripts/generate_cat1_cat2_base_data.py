import uuid
import os

CAT1_COUNTS = {
    "Facial & Skincare": 9,
    "Makeup & Styling": 6,
    "Men's Salon": 11,
    "Pedicure & Manicure": 10,
    "Spa & Massage": 6,
    "Women's Salon": 13
}

CAT2_COUNTS = {
    "Deep Cleaning": 7,
    "Full Home / By Room Cleaning": 8,
    "Kitchen & Bathroom Cleaning": 5,
    "Pest Control": 6,
    "Sofa & Furniture Cleaning": 6
}

def generate_service(name, category, subcategory):
    return f"""    {{
        "id": "{str(uuid.uuid4())}",
        "name": "{name}",
        "category": "{category}",
        "subcategory": "{subcategory}",
        "price": 999.0,
        "description": "Professional {name} services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the {subcategory} experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete {name} procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {{
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            }},
            {{
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            }},
            {{
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main {name} tasks with precision.",
                "is_key_step": True
            }},
            {{
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            }},
            {{
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }}
        ],
        "tools_materials": [
            "Standard {subcategory} tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality {name} completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {{
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            }},
            {{
                "question": "How long does {name} take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            }},
            {{
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            }},
            {{
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }}
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    }}"""

def write_data(cat_num, cat_name, subcats, output_file, var_name):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("import uuid\n\n")
        f.write(f"#{cat_name} Data\n\n")
        f.write(f"{var_name} = [\n")
        
        services = []
        for subcat, count in subcats.items():
            for i in range(1, count + 1):
                sname = f"{subcat} Service Variation {i}"
                services.append(generate_service(sname, cat_name, subcat))
                
        f.write(",\n".join(services))
        f.write("\n]\n")

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    cat1_file = os.path.join(base, "..", "category1_content_builder", "beauty_salon_spa_data.py")
    cat2_file = os.path.join(base, "..", "category2_content_builder", "cleaning_home_data.py")
    
    write_data(1, "1. Beauty, Salon & Spa", CAT1_COUNTS, cat1_file, "BEAUTY_SERVICES")
    write_data(2, "2. Cleaning & Pest Control", CAT2_COUNTS, cat2_file, "CLEANING_SERVICES")
    print("Successfully generated data files for Categories 1 and 2.")
