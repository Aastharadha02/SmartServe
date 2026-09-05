"""
Rebuilds all 14 permanent category backups from PostgreSQL into backend/backups/
"""

import os
import json
import pandas as pd
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv('backend/.env')

db_url = os.getenv('DATABASE_URL')
p = urlparse(db_url)
conn = psycopg2.connect(
    dbname=p.path.lstrip('/'),
    user=p.username,
    password=p.password,
    host=p.hostname,
    port=p.port
)
cur = conn.cursor()

os.makedirs('backend/backups', exist_ok=True)

cur.execute("SELECT DISTINCT category FROM services ORDER BY category;")
categories = [r[0] for r in cur.fetchall()]

category_file_slugs = {
    "1. Beauty, Salon & Spa": "category1_beauty_salon_spa_FINAL",
    "2. Cleaning & Pest Control": "category2_cleaning_home_FINAL",
    "3. Painting, Waterproofing & Home Improvement": "category3_painting_home_improvement_FINAL",
    "4. AC, Appliance & Electronics Repair": "category4_ac_appliance_repair_FINAL",
    "5. Electrician, Plumber, Carpenter & Home Repairs": "category5_electrician_plumber_carpenter_FINAL",
    "6. Smart Home & Security": "category6_smart_home_security_FINAL",
    "7. Domestic Help & Cooking": "category7_domestic_help_cooking_FINAL",
    "8. Education, Teachers & Coaching": "category8_education_coaching_FINAL",
    "9. Health, Fitness & Wellness": "category9_health_fitness_wellness_FINAL",
    "10. Events, Photography & Entertainment": "category10_events_photography_entertainment_FINAL",
    "11. Pet Services": "category11_pet_services_FINAL",
    "12. Technology & Digital Services": "category12_technology_digital_services_FINAL",
    "13. Professional & Business Services": "category13_professional_business_services_FINAL",
    "14. Moving, Delivery & Local Assistance": "category14_moving_delivery_local_assistance_FINAL",
}

for cat in categories:
    cur.execute("SELECT id, category, subcategory, name, base_price, distinct_features FROM services WHERE category = %s ORDER BY subcategory, name;", (cat,))
    rows = cur.fetchall()
    
    cat_data = []
    for r in rows:
        feat_raw = r[5]
        if isinstance(feat_raw, dict):
            features = feat_raw
        elif isinstance(feat_raw, str):
            try:
                features = json.loads(feat_raw)
            except Exception:
                features = {}
        else:
            features = {}
            
        cat_data.append({
            "id": str(r[0]),
            "category": r[1],
            "subcategory": r[2],
            "name": r[3],
            "price": r[4],
            "description": features.get("description", "") if isinstance(features, dict) else "",
            "highlights": features.get("highlights", []) if isinstance(features, dict) else [],
            "included": features.get("included", []) if isinstance(features, dict) else [],
            "excluded": features.get("excluded", []) if isinstance(features, dict) else [],
            "faqs": features.get("faqs", []) if isinstance(features, dict) else [],
            "warranty": features.get("warranty", "") if isinstance(features, dict) else ""
        })
        
    slug = category_file_slugs.get(cat, f"category_{cat.split('.')[0]}_FINAL")
    json_path = f"backend/backups/{slug}.json"
    xlsx_path = f"backend/backups/{slug}.xlsx"
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cat_data, f, indent=2, ensure_ascii=False)
        
    df = pd.DataFrame(cat_data)
    df.to_excel(xlsx_path, index=False)
    
    print(f"Exported {len(cat_data)} services for '{cat}' to {slug}.json & .xlsx")

cur.close()
conn.close()
print("All backups rebuilt successfully!")
