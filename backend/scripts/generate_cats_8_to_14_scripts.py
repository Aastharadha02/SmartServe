"""
Generates pipeline scripts for Categories 8-14 in one shot.
Run once; re-run is safe (idempotent file writes).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _pipeline_generator import generate_scripts

BASE = os.path.dirname(os.path.abspath(__file__))

CATEGORIES = [
    {
        "cat_num": 8,
        "slug": "education_coaching",
        "label": "8. Education, Teachers & Coaching",
        "data_var": "EDUCATION_COACHING_SERVICES",
        "data_module": "education_coaching_data",
        "subcats": [
            ("School Tutoring (K-12)", 7),
            ("Competitive Exam Coaching", 7),
            ("Language & Communication", 5),
            ("Music & Arts Lessons", 5),
            ("Skills & Hobby Classes", 6),
        ],
    },
    {
        "cat_num": 9,
        "slug": "health_fitness_wellness",
        "label": "9. Health, Fitness & Wellness",
        "data_var": "HEALTH_FITNESS_SERVICES",
        "data_module": "health_fitness_data",
        "subcats": [
            ("Personal Training", 7),
            ("Yoga & Meditation", 6),
            ("Physiotherapy & Rehabilitation", 6),
            ("Nutrition & Diet Counselling", 5),
            ("Mental Wellness & Counselling", 6),
        ],
    },
    {
        "cat_num": 10,
        "slug": "events_photography_entertainment",
        "label": "10. Events, Photography & Entertainment",
        "data_var": "EVENTS_PHOTOGRAPHY_SERVICES",
        "data_module": "events_photography_data",
        "subcats": [
            ("Event Planning & Management", 6),
            ("Photography & Videography", 7),
            ("Catering & Food Services", 6),
            ("DJ & Sound Systems", 5),
            ("Decoration & Floral", 6),
        ],
    },
    {
        "cat_num": 11,
        "slug": "pet_services",
        "label": "11. Pet Services",
        "data_var": "PET_SERVICES",
        "data_module": "pet_services_data",
        "subcats": [
            ("Dog Grooming", 6),
            ("Pet Sitting & Boarding", 5),
            ("Veterinary & Health Checkup", 5),
            ("Dog Training", 5),
            ("Pet Accessories & Nutrition", 4),
        ],
    },
    {
        "cat_num": 12,
        "slug": "technology_digital_services",
        "label": "12. Technology & Digital Services",
        "data_var": "TECH_DIGITAL_SERVICES",
        "data_module": "technology_digital_data",
        "subcats": [
            ("Computer & Laptop Repair", 7),
            ("Networking & Wi-Fi Setup", 5),
            ("Website & App Development", 6),
            ("Data Recovery & Backup", 5),
            ("IT Support & Consultation", 7),
        ],
    },
    {
        "cat_num": 13,
        "slug": "professional_business_services",
        "label": "13. Professional & Business Services",
        "data_var": "PROFESSIONAL_BUSINESS_SERVICES",
        "data_module": "professional_business_data",
        "subcats": [
            ("Accounting & Tax Filing", 6),
            ("Legal Documentation", 5),
            ("Staffing & HR Services", 5),
            ("Marketing & Branding", 6),
            ("Business Consulting", 5),
            ("Virtual Assistant", 3),
        ],
    },
    {
        "cat_num": 14,
        "slug": "moving_delivery_local_assistance",
        "label": "14. Moving, Delivery & Local Assistance",
        "data_var": "MOVING_DELIVERY_SERVICES",
        "data_module": "moving_delivery_data",
        "subcats": [
            ("Home Shifting & Packing", 7),
            ("Vehicle Transport", 5),
            ("Last-Mile Delivery", 5),
            ("Junk Removal & Disposal", 5),
            ("Local Errands & Assistance", 5),
        ],
    },
]

if __name__ == "__main__":
    for cat in CATEGORIES:
        generate_scripts(
            cat_num=cat["cat_num"],
            slug=cat["slug"],
            label=cat["label"],
            data_var=cat["data_var"],
            data_module=cat["data_module"],
            subcats=cat["subcats"],
            base_dir=BASE,
        )
    print("All pipeline scripts generated successfully.")
