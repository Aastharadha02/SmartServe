"""
Updates admin-frontend/src/utils/serviceImages.ts with exact image mappings for all authentic services
"""

import os

FILE_PATH = "admin-frontend/src/utils/serviceImages.ts"

# New mappings to insert into EXACT_SERVICE_IMAGE_MAP
NEW_EXACT_MAPPINGS = """
  // ================= Authentic Service Mappings =================
  // Beauty, Salon & Spa
  "Fruit Glow & Hydration Facial": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=800&q=80",
  "O3+ Anti-Tan Brightening Facial": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=800&q=80",
  "Hydra-Facial Deep Pore Cleansing": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80",
  "24K Gold Radiance Facial": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=800&q=80",
  "Charcoal Detox & Acne Cleanup": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=800&q=80",
  "Organic Herbal De-Tan Cleanup": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=800&q=80",
  "Oxygen Bleach & Face Radiance": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=800&q=80",
  "Diamond Micro-Dermabrasion Facial": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80",
  "Anti-Aging Collagen Lift Facial": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=800&q=80",

  "Soft Glam Party Makeup": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=800&q=80",
  "HD Flawless Bridal Makeup Package": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
  "Pre-Wedding Engagement Makeup": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=800&q=80",
  "Premium Airbrush Special Event Makeup": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
  "Saree Draping & Hair Styling Combo": "https://images.unsplash.com/photo-1562322140-8baeececf3df?auto=format&fit=crop&w=800&q=80",
  "Express Eye & Face Touchup Makeup": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=800&q=80",

  "Men's Classic Haircut & Wash": "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=800&q=80",
  "Beard Sculpting & Oil Styling": "https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=800&q=80",
  "Charcoal Face Scrub & Blackhead Extraction": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=800&q=80",
  "Head Oil Massage & Scalp Relaxation": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80",
  "Men's Global Hair Color (Natural Black/Brown)": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=800&q=80",
  "Scalp Detox & Anti-Dandruff Spa": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=800&q=80",
  "Hot Towel Shave & Beard Grooming": "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=800&q=80",
  "Men's De-Tan Face Cleanup": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=800&q=80",
  "Men's Express Pedicure": "https://images.unsplash.com/photo-1519415943484-9fa1873496d4?auto=format&fit=crop&w=800&q=80",
  "Men's Express Manicure": "https://images.unsplash.com/photo-1632345031435-8727f6897d53?auto=format&fit=crop&w=800&q=80",
  "Executive Groom's Pamper Package": "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=800&q=80",

  "Classic Cut, File & Polish Manicure": "https://images.unsplash.com/photo-1632345031435-8727f6897d53?auto=format&fit=crop&w=800&q=80",
  "Spa Hydrating & Cuticle Care Manicure": "https://images.unsplash.com/photo-1604654894610-df63bc536371?auto=format&fit=crop&w=800&q=80",
  "Long-Lasting Gel Polish Manicure": "https://images.unsplash.com/photo-1519014816548-bf5fe059798b?auto=format&fit=crop&w=800&q=80",
  "Express Cut, File & Polish Change": "https://images.unsplash.com/photo-1519014816548-bf5fe059798b?auto=format&fit=crop&w=800&q=80",
  "Custom Nail Art & Extension Touchup": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
  "Classic Relaxing Foot Pedicure": "https://images.unsplash.com/photo-1519415943484-9fa1873496d4?auto=format&fit=crop&w=800&q=80",
  "Ice Cream Aromatherapy Spa Pedicure": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80",
  "Crystal Spa Detox Foot Pedicure": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80",
  "Intensive Heel Peel & Callus Removal": "https://images.unsplash.com/photo-1519415943484-9fa1873496d4?auto=format&fit=crop&w=800&q=80",
  "Deluxe De-Tan Mani-Pedi Combo": "https://images.unsplash.com/photo-1632345031435-8727f6897d53?auto=format&fit=crop&w=800&q=80",

  "Swedish Muscle Relaxation Body Massage": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80",
  "Deep Tissue Sports Relief Massage": "https://images.unsplash.com/photo-1519824145371-296894a0dc91?auto=format&fit=crop&w=800&q=80",
  "Traditional Ayurvedic Potli Therapy": "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80",
  "Aromatherapy Essential Oil Spa": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80",
  "Thai Foot Reflexology Therapy": "https://images.unsplash.com/photo-1519415943484-9fa1873496d4?auto=format&fit=crop&w=800&q=80",
  "Express Head, Neck & Shoulder Relief": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80",

  "Layered Haircut, Wash & Blow Dry": "https://images.unsplash.com/photo-1562322140-8baeececf3df?auto=format&fit=crop&w=800&q=80",
  "Global Hair Color (L'Oréal / Matrix)": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=800&q=80",
  "Ammonia-Free Root Touch-Up": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=800&q=80",
  "Keratin Hair Smoothing Treatment": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
  "Hair Rebonding & Straightening": "https://images.unsplash.com/photo-1562322140-8baeececf3df?auto=format&fit=crop&w=800&q=80",
  "Full Body Rica Waxing": "https://images.unsplash.com/photo-1560750588-73207b1ef5b8?auto=format&fit=crop&w=800&q=80",
  "Full Arms & Full Legs Waxing (Honey)": "https://images.unsplash.com/photo-1560750588-73207b1ef5b8?auto=format&fit=crop&w=800&q=80",
  "Eyebrow & Upper Lip Threading": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=800&q=80",
  "De-Tan Pack & Instant Radiance Cleanup": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=800&q=80",
  "Deep Conditioning Spa Hair Treatment": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=800&q=80",
  "Organic Fruit Bleach (Face & Neck)": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=800&q=80",
  "Underarm Tan Removal & Whitening Pack": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=800&q=80",
  "Royal Queen Pamper Package": "https://images.unsplash.com/photo-1562322140-8baeececf3df?auto=format&fit=crop&w=800&q=80",

  // Cleaning & Home Cleaning
  "Full Apartment Deep Cleaning (1/2 BHK)": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=800&q=80",
  "Kitchen Oil Degreasing & Cabinet Deep Clean": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80",
  "Bathroom Tile Scrubbing & Descaling Wash": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80",
  "Balcony Washing & Window Track Cleaning": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80",
  "Move-In / Move-Out Sanitize Deep Clean": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
  "Terrace & Roof High-Pressure Wash": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80",
  "Floor Machine Scrubbing & Buffing": "https://images.unsplash.com/photo-1628177142898-93e36e4e3a50?auto=format&fit=crop&w=800&q=80",

  // Smart Home & Security
  "Biometric Fingerprint Smart Door Lock Fitting": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=800&q=80",
  "Smart Video Doorbell & Lock Sync Setup": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=800&q=80",
  "Keyless Touchscreen Digital Lock Fitting": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=800&q=80",
  "RFID Card Keyless Access Lock Installation": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=800&q=80",
  "Smart Lock Battery Replacement & Diagnostics": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=800&q=80",
  "Bluetooth Smart Latch & Mortise Setup": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=800&q=80",

  "Outdoor Weatherproof HD Security Camera Fitting": "https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&w=800&q=80",
  "Indoor 360° Wi-Fi Security Camera Installation": "https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&w=800&q=80",
  "Wireless Motion Sensor Burglar Alarm Setup": "https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&w=800&q=80",
  "Dual-Way Video Door Phone Monitor Fitting": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=800&q=80",

  // Domestic Help & Cooking
  "North Indian Meal Home Cook (Daily 2 Meals)": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=800&q=80",
  "South Indian Breakfast & Meal Cook": "https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?auto=format&fit=crop&w=800&q=80",
  "Party & Special Occasion Festival Chef": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=800&q=80",
  "Healthy Fitness Meal Prep Cook (Diet Specific)": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=800&q=80",
  "Biryani & Mughlai Special Home Chef": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=800&q=80",
"""

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

target_anchor = "export const EXACT_SERVICE_IMAGE_MAP: Record<string, string> = {"

if target_anchor in content:
    new_content = content.replace(target_anchor, target_anchor + "\n" + NEW_EXACT_MAPPINGS)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ Successfully updated serviceImages.ts with authentic mappings!")
else:
    print("❌ Anchor not found in serviceImages.ts")
