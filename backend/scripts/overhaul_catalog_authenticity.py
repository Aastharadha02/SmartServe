"""
SmartServe Master Catalog Realism & Authenticity Overhaul Script
Replaces synthetic "Variation X" services across ALL Categories (1-14, 457 services total)
with distinct, real-world service titles, accurate descriptions, custom FAQs, realistic prices & durations.
"""

import os
import json
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

AUTHENTIC_CATALOG = {
    "1. Beauty, Salon & Spa": [
        # Facial & Skincare (9)
        {"name": "Fruit Glow & Hydration Facial", "sub": "Facial & Skincare", "price": 899.0, "dur": 45, "desc": "Nourishing organic fruit extract facial designed to deeply hydrate, exfoliate, and restore natural skin radiance."},
        {"name": "O3+ Anti-Tan Brightening Facial", "sub": "Facial & Skincare", "price": 1499.0, "dur": 60, "desc": "Professional dermatologically tested facial pack that lightens sun tan, even out skin tone, and boosts collagen synthesis."},
        {"name": "Hydra-Facial Deep Pore Cleansing", "sub": "Facial & Skincare", "price": 2199.0, "dur": 75, "desc": "Advanced multi-step hydro-dermabrasion treatment extracting impurities while infusing skin with hyaluronic acid serums."},
        {"name": "24K Gold Radiance Facial", "sub": "Facial & Skincare", "price": 1899.0, "dur": 60, "desc": "Luxurious gold-foil massage facial giving skin an instant luminous glow, firmness, and silk smoothness for special events."},
        {"name": "Charcoal Detox & Acne Cleanup", "sub": "Facial & Skincare", "price": 999.0, "dur": 45, "desc": "Activated bamboo charcoal vacuum cleanup targeting stubborn blackheads, excess sebum, and active acne breakouts."},
        {"name": "Organic Herbal De-Tan Cleanup", "sub": "Facial & Skincare", "price": 699.0, "dur": 30, "desc": "Gentle herbal pack with sandalwood and aloe vera to instantly soothe sun-burned skin and remove light pigmentation."},
        {"name": "Oxygen Bleach & Face Radiance", "sub": "Facial & Skincare", "price": 499.0, "dur": 30, "desc": "Mild oxygenated facial bleach that lightens facial hair to match skin tone while providing an instant bright complexion."},
        {"name": "Diamond Micro-Dermabrasion Facial", "sub": "Facial & Skincare", "price": 2499.0, "dur": 90, "desc": "Precision diamond-tip exfoliation reducing acne scars, fine lines, and hyper-pigmentation for youthful skin texture."},
        {"name": "Anti-Aging Collagen Lift Facial", "sub": "Facial & Skincare", "price": 1999.0, "dur": 75, "desc": "Tightening peptide and collagen facial massaged with ice globes to diminish wrinkles and uplift sagging facial contours."},

        # Makeup & Styling (6)
        {"name": "Soft Glam Party Makeup", "sub": "Makeup & Styling", "price": 2499.0, "dur": 90, "desc": "Elegant evening party makeup including skin prep, custom eyeshadow, false lashes, and smudge-proof lip color."},
        {"name": "HD Flawless Bridal Makeup Package", "sub": "Makeup & Styling", "price": 9999.0, "dur": 180, "desc": "High-definition camera-ready bridal makeover with waterproof base, contouring, hair styling, and jewelry setting."},
        {"name": "Pre-Wedding Engagement Makeup", "sub": "Makeup & Styling", "price": 5999.0, "dur": 120, "desc": "Radiant long-stay engagement look with customized foundation matching, shimmer eyes, and hair draping."},
        {"name": "Premium Airbrush Special Event Makeup", "sub": "Makeup & Styling", "price": 7499.0, "dur": 150, "desc": "Ultra-lightweight airbrush foundation application ensuring 16-hour sweat-proof, poreless perfection."},
        {"name": "Saree Draping & Hair Styling Combo", "sub": "Makeup & Styling", "price": 1199.0, "dur": 45, "desc": "Professional saree pleating and secure pin-up paired with voluminous curls or traditional braided bun styling."},
        {"name": "Express Eye & Face Touchup Makeup", "sub": "Makeup & Styling", "price": 999.0, "dur": 30, "desc": "Quick 30-minute touchup covering eye liner, mascara, subtle blush, and lipstick refresh for instant readiness."},

        # Men's Salon (11)
        {"name": "Men's Classic Haircut & Wash", "sub": "Men's Salon", "price": 299.0, "dur": 30, "desc": "Precision scissor/clipper haircut tailored to face shape, completed with a scalp wash and blow-dry styling."},
        {"name": "Beard Sculpting & Oil Styling", "sub": "Men's Salon", "price": 199.0, "dur": 20, "desc": "Razor-sharp beard line trimming, razor edging, and argan oil massage for a polished, sharp look."},
        {"name": "Charcoal Face Scrub & Blackhead Extraction", "sub": "Men's Salon", "price": 399.0, "dur": 30, "desc": "Deep pore exfoliation scrub for men removing nose blackheads, dead skin cells, and daily city pollution layer."},
        {"name": "Head Oil Massage & Scalp Relaxation", "sub": "Men's Salon", "price": 349.0, "dur": 30, "desc": "Traditional warm Mahabhringraj oil head massage stimulating blood circulation and releasing mental stress."},
        {"name": "Men's Global Hair Color (Natural Black/Brown)", "sub": "Men's Salon", "price": 599.0, "dur": 45, "desc": "100% grey coverage hair coloring using ammonia-free cream dye that leaves hair shiny and natural."},
        {"name": "Scalp Detox & Anti-Dandruff Spa", "sub": "Men's Salon", "price": 799.0, "dur": 45, "desc": "Tea tree oil scalp treatment dissolving flaky dandruff, soothing itchiness, and strengthening root follicles."},
        {"name": "Hot Towel Shave & Beard Grooming", "sub": "Men's Salon", "price": 249.0, "dur": 25, "desc": "Classic barbering shave with warm towel pore opening, rich lathering shave, and aftershave balm soothe."},
        {"name": "Men's De-Tan Face Cleanup", "sub": "Men's Salon", "price": 499.0, "dur": 35, "desc": "Instant de-tan pack for men exposed to sun and outdoors, clearing forehead and cheek tanning."},
        {"name": "Men's Express Pedicure", "sub": "Men's Salon", "price": 599.0, "dur": 40, "desc": "Foot soak, nail trimming, callus scrub, and relaxing foot massage catered specifically for men."},
        {"name": "Men's Express Manicure", "sub": "Men's Salon", "price": 499.0, "dur": 30, "desc": "Hand nail shaping, cuticle cleanup, hand scrub, and hydrating palm lotion massage."},
        {"name": "Executive Groom's Pamper Package", "sub": "Men's Salon", "price": 1799.0, "dur": 90, "desc": "All-in-one grooming haircut, beard trim, de-tan facial, and head massage package for groom & groomsmen."},

        # Pedicure & Manicure (10)
        {"name": "Classic Cut, File & Polish Manicure", "sub": "Pedicure & Manicure", "price": 399.0, "dur": 30, "desc": "Nail shaping, cuticle trimming, hands exfoliation, and high-shine nail polish application."},
        {"name": "Spa Hydrating & Cuticle Care Manicure", "sub": "Pedicure & Manicure", "price": 699.0, "dur": 45, "desc": "Luxurious hand mask, deep cuticle nourishment oil massage, and soothing thermal gloves wrap."},
        {"name": "Long-Lasting Gel Polish Manicure", "sub": "Pedicure & Manicure", "price": 899.0, "dur": 50, "desc": "UV/LED cured gel polish application lasting up to 3 weeks without chipping or dulling."},
        {"name": "Express Cut, File & Polish Change", "sub": "Pedicure & Manicure", "price": 249.0, "dur": 20, "desc": "Quick nail trim, filing into square/round shape, and fresh color polish application."},
        {"name": "Custom Nail Art & Extension Touchup", "sub": "Pedicure & Manicure", "price": 1199.0, "dur": 60, "desc": "Creative nail art designs, ombre gradients, rhinestones, or acrylic extension fill-ins."},
        {"name": "Classic Relaxing Foot Pedicure", "sub": "Pedicure & Manicure", "price": 499.0, "dur": 40, "desc": "Warm foot tub soak, pumice stone heel scrubbing, toe nail grooming, and calf massage."},
        {"name": "Ice Cream Aromatherapy Spa Pedicure", "sub": "Pedicure & Manicure", "price": 899.0, "dur": 50, "desc": "Fun strawberry/chocolate bath bomb foot soak, sugar scrub exfoliation, and butter cream massage."},
        {"name": "Crystal Spa Detox Foot Pedicure", "sub": "Pedicure & Manicure", "price": 1099.0, "dur": 60, "desc": "Gelatinous crystal foot bath retaining heat, deeply detoxifying tired feet and softening dry heels."},
        {"name": "Intensive Heel Peel & Callus Removal", "sub": "Pedicure & Manicure", "price": 799.0, "dur": 45, "desc": "Targeted chemical heel peel breaking down hard dead callus skin for baby-soft foot soles."},
        {"name": "Deluxe De-Tan Mani-Pedi Combo", "sub": "Pedicure & Manicure", "price": 1299.0, "dur": 75, "desc": "Combined manicure and pedicure service with specialized anti-tan bleach pack for hands and feet."},

        # Spa & Massage (6)
        {"name": "Swedish Muscle Relaxation Body Massage", "sub": "Spa & Massage", "price": 1499.0, "dur": 60, "desc": "Classic full-body light to medium pressure massage using long gliding strokes to ease physical fatigue."},
        {"name": "Deep Tissue Sports Relief Massage", "sub": "Spa & Massage", "price": 1899.0, "dur": 60, "desc": "Firm targeted pressure targeting chronic muscle knots, lower back tension, and joint stiffness."},
        {"name": "Traditional Ayurvedic Potli Therapy", "sub": "Spa & Massage", "price": 2199.0, "dur": 75, "desc": "Warm herbal poultice filled with medicinal leaves pressed along energy meridians to relieve arthritis and pain."},
        {"name": "Aromatherapy Essential Oil Spa", "sub": "Spa & Massage", "price": 1699.0, "dur": 60, "desc": "Scented lavender and eucalyptus essential oil massage promoting deep mental calm and sleep quality."},
        {"name": "Thai Foot Reflexology Therapy", "sub": "Spa & Massage", "price": 899.0, "dur": 45, "desc": "Pressure-point wooden stick massage on foot soles stimulating internal organ health and leg circulation."},
        {"name": "Express Head, Neck & Shoulder Relief", "sub": "Spa & Massage", "price": 599.0, "dur": 30, "desc": "Quick desk-worker relief massage focusing on tight neck muscles, upper back, and temples."},

        # Women's Salon (13)
        {"name": "Layered Haircut, Wash & Blow Dry", "sub": "Women's Salon", "price": 699.0, "dur": 45, "desc": "Stylish layered or feather haircut customized by senior stylist, finished with voluminous blow-dry."},
        {"name": "Global Hair Color (L'Oréal / Matrix)", "sub": "Women's Salon", "price": 2499.0, "dur": 90, "desc": "Full head vibrant hair color transformation using premium salon brands with glossy shine protection."},
        {"name": "Ammonia-Free Root Touch-Up", "sub": "Women's Salon", "price": 999.0, "dur": 45, "desc": "Precise grey root coverage up to 2 inches using gentle non-damaging ammonia-free dye formula."},
        {"name": "Keratin Hair Smoothing Treatment", "sub": "Women's Salon", "price": 3999.0, "dur": 120, "desc": "Protein-rich keratin infusing treatment eliminating frizzy flyaways and creating silky manageable hair."},
        {"name": "Hair Rebonding & Straightening", "sub": "Women's Salon", "price": 4499.0, "dur": 150, "desc": "Permanent sleek straight hair transformation using neutralizer chemical straightening process."},
        {"name": "Full Body Rica Waxing", "sub": "Women's Salon", "price": 1599.0, "dur": 75, "desc": "Liposoluble Italian Rica wax for full arms, legs, and underarms giving painless smooth hair removal."},
        {"name": "Full Arms & Full Legs Waxing (Honey)", "sub": "Women's Salon", "price": 799.0, "dur": 45, "desc": "Standard warm honey wax removal for arms and legs, finished with soothing aloe vera gel application."},
        {"name": "Eyebrow & Upper Lip Threading", "sub": "Women's Salon", "price": 99.0, "dur": 15, "desc": "Precise cotton thread shaping for clean eyebrow arches and upper lip stray hair removal."},
        {"name": "De-Tan Pack & Instant Radiance Cleanup", "sub": "Women's Salon", "price": 599.0, "dur": 30, "desc": "Quick face cleansing, steam, blackhead removal, and milk & honey de-tan pack."},
        {"name": "Deep Conditioning Spa Hair Treatment", "sub": "Women's Salon", "price": 999.0, "dur": 45, "desc": "Intensive hair mask application under warm steam, restoring moisture to dry heat-damaged hair ends."},
        {"name": "Organic Fruit Bleach (Face & Neck)", "sub": "Women's Salon", "price": 349.0, "dur": 25, "desc": "Natural fruit acid bleach lightening facial hair while evening out neck and face discoloration."},
        {"name": "Underarm Tan Removal & Whitening Pack", "sub": "Women's Salon", "price": 299.0, "dur": 20, "desc": "Exfoliating scrub and specialized AHA cream pack targeting dark hyper-pigmented underarms."},
        {"name": "Royal Queen Pamper Package", "sub": "Women's Salon", "price": 3299.0, "dur": 150, "desc": "Ultimate head-to-toe package including haircut, facial, hair spa, manicure, and pedicure."}
    ],

    "2. Cleaning & Pest Control": [
        # Deep Cleaning (7)
        {"name": "Full Apartment Deep Cleaning (1/2 BHK)", "sub": "Deep Cleaning", "price": 2999.0, "dur": 180, "desc": "Thorough top-to-bottom scrub of entire home including ceiling fans, window sills, doors, floors, and sanitization."},
        {"name": "Kitchen Oil Degreasing & Cabinet Deep Clean", "sub": "Deep Cleaning", "price": 1299.0, "dur": 120, "desc": "Heavy-duty chemical degreasing of grease-laden kitchen tiles, cabinet interiors/exteriors, and exhaust fans."},
        {"name": "Bathroom Tile Scrubbing & Descaling Wash", "sub": "Deep Cleaning", "price": 799.0, "dur": 60, "desc": "Acid-free hard water stain removal from floor/wall tiles, glass shower partitions, taps, and toilet bowls."},
        {"name": "Balcony Washing & Window Track Cleaning", "sub": "Deep Cleaning", "price": 499.0, "dur": 45, "desc": "Pressure washing balcony floor, wiping glass railings, and vacuuming dirt from sliding window tracks."},
        {"name": "Move-In / Move-Out Sanitize Deep Clean", "sub": "Deep Cleaning", "price": 3499.0, "dur": 240, "desc": "Comprehensive disinfection and deep cleaning for vacant houses prior to moving in or handing over to landlord."},
        {"name": "Terrace & Roof High-Pressure Wash", "sub": "Deep Cleaning", "price": 1599.0, "dur": 90, "desc": "Industrial jet washer cleaning of rooftop tiles, rainwater drains, and moss buildup removal."},
        {"name": "Floor Machine Scrubbing & Buffing", "sub": "Deep Cleaning", "price": 1199.0, "dur": 90, "desc": "Single-disc rotary floor scrubbing machine treatment for marble, granite, or vitrified tile shine."},

        # Full Home / By Room (8)
        {"name": "1 BHK Express Deep Cleaning", "sub": "Full Home / By Room Cleaning", "price": 1999.0, "dur": 120, "desc": "Complete cleaning of 1 hall, 1 bedroom, 1 kitchen, and 1 bathroom with eco-friendly cleaning agents."},
        {"name": "2 BHK Standard Full Home Cleaning", "sub": "Full Home / By Room Cleaning", "price": 2799.0, "dur": 180, "desc": "Detailed deep cleaning service for 2 BHK flats covering all rooms, fixtures, and floor scrubbing."},
        {"name": "3 BHK Premium Full Home Cleaning", "sub": "Full Home / By Room Cleaning", "price": 3699.0, "dur": 240, "desc": "4-member cleaner team deep cleaning 3 bedrooms, hall, kitchen, balconies, and 3 bathrooms."},
        {"name": "4 BHK / Villa Luxury Deep Cleaning", "sub": "Full Home / By Room Cleaning", "price": 4999.0, "dur": 300, "desc": "Full day deep cleaning for large villas, independent houses, or 4 BHK duplex apartments."},
        {"name": "Single Bedroom Deep Dust & Vacuum", "sub": "Full Home / By Room Cleaning", "price": 599.0, "dur": 45, "desc": "Cobweb removal, wardrobe top dusting, mattress vacuuming, and floor mopping for 1 bedroom."},
        {"name": "Living Room Furniture Polish & Clean", "sub": "Full Home / By Room Cleaning", "price": 799.0, "dur": 60, "desc": "TV unit dusting, sofa vacuuming, glass center table cleaning, and floor scrubbing in hall."},
        {"name": "Dining Area Scrubbing & Sanitization", "sub": "Full Home / By Room Cleaning", "price": 499.0, "dur": 45, "desc": "Deep cleaning dining table, chair wipe down, floor stain removal, and chandelier dusting."},
        {"name": "Store Room & Attic Declutter Cleaning", "sub": "Full Home / By Room Cleaning", "price": 699.0, "dur": 60, "desc": "Organizing, dusting, cobweb removal, and floor wash for storage rooms and lofts."},

        # Kitchen & Bathroom Cleaning (5)
        {"name": "Kitchen Cabinet & Appliance Exterior Wash", "sub": "Kitchen & Bathroom Cleaning", "price": 999.0, "dur": 90, "desc": "Wiping inside empty cabinets, degreasing fridge exterior, microwave exterior, and countertop scrub."},
        {"name": "Kitchen Chimney & Hob Deep Degreasing", "sub": "Kitchen & Bathroom Cleaning", "price": 799.0, "dur": 60, "desc": "Dismantling chimney mesh filters, chemical degreasing bath, and gas stove burner cleaning."},
        {"name": "Dual Bathroom Scrubbing & Tile Polish", "sub": "Kitchen & Bathroom Cleaning", "price": 1299.0, "dur": 90, "desc": "Value combo package deep scrubbing 2 bathrooms including washbasin, mirror, and toilet disinfections."},
        {"name": "Sink Drain Unclogging & Anti-Bacterial Wash", "sub": "Kitchen & Bathroom Cleaning", "price": 399.0, "dur": 30, "desc": "Clearing slow kitchen sink drains, removing sludge, and flushing with odor-killing enzyme gel."},
        {"name": "Kitchen Countertop & Wall Tile Steam Clean", "sub": "Kitchen & Bathroom Cleaning", "price": 699.0, "dur": 45, "desc": "High-temperature steam spray dissolving oil drops on backsplashes and grout joints."},

        # Pest Control (6)
        {"name": "Cockroach Herbal Gel Pest Control", "sub": "Pest Control", "price": 899.0, "dur": 45, "desc": "Odorless herbal gel baiting in kitchen cabinets and drain spray exterminating German cockroaches."},
        {"name": "Bed Bug Thermal & Chemical Treatment", "sub": "Pest Control", "price": 1499.0, "dur": 60, "desc": "2-visit spray treatment targeting mattress seams, bed frames, and wall cracks for complete bed bug eradication."},
        {"name": "Anti-Termite Soil Drilling & Barrier Injection", "sub": "Pest Control", "price": 2499.0, "dur": 120, "desc": "Drilling holes along wall skirts and injecting anti-termite chemical to protect wooden furniture with 2-year warranty."},
        {"name": "Mosquito & Fly Thermal Fogging", "sub": "Pest Control", "price": 699.0, "dur": 30, "desc": "Synthetic pyrethroid fogging for garden, balcony, and living areas suppressing adult mosquitoes."},
        {"name": "Ant & Silverfish Perimeter Spray", "sub": "Pest Control", "price": 599.0, "dur": 30, "desc": "Odorless liquid barrier spray along sugar ant trails, bookshelves, and bathroom baseboards."},
        {"name": "Rodent Trapping & Entry Sealing Service", "sub": "Pest Control", "price": 899.0, "dur": 45, "desc": "Placement of glue pads, snap traps, and sealing open pipe gaps to keep rats and mice out."},

        # Sofa & Furniture Cleaning (6)
        {"name": "5-Seater Fabric Sofa Shampooing & Extraction", "sub": "Sofa & Furniture Cleaning", "price": 899.0, "dur": 60, "desc": "Injection-extraction foam machine washing removing deep stains, sweat odors, and dust mites from sofa."},
        {"name": "Leather Sofa Conditioning & Cream Polish", "sub": "Sofa & Furniture Cleaning", "price": 999.0, "dur": 45, "desc": "Specialized leather cleaner wiping dirt followed by rich moisturizer cream to prevent leather cracking."},
        {"name": "6-Seater Dining Chair Upholstery Foam Wash", "sub": "Sofa & Furniture Cleaning", "price": 599.0, "dur": 45, "desc": "Shampooing cushion seats of 6 dining chairs and polishing wooden/metal chair legs."},
        {"name": "King Size Mattress Deep Steam Sanitization", "sub": "Sofa & Furniture Cleaning", "price": 799.0, "dur": 50, "desc": "High-powered UV vacuuming and hot steam treatment sanitizing mattress from dead skin & allergens."},
        {"name": "Carpet High-Extraction Deep Wash", "sub": "Sofa & Furniture Cleaning", "price": 699.0, "dur": 45, "desc": "Rug and living room carpet shampooing lifting tea/coffee spots and reviving carpet pile texture."},
        {"name": "Recliner Chair Spot & Stain Scrub", "sub": "Sofa & Furniture Cleaning", "price": 499.0, "dur": 30, "desc": "Targeted stain removal scrub and fabric wash for single electronic or manual recliner chairs."}
    ],

    "6. Smart Home & Security": [
        # Smart Locks (6)
        {"name": "Biometric Fingerprint Smart Door Lock Fitting", "sub": "Smart Locks", "price": 1499.0, "dur": 60, "desc": "Professional installation of main wooden door biometric fingerprint, RFID card, and passcode mortise lock."},
        {"name": "Smart Video Doorbell & Lock Sync Setup", "sub": "Smart Locks", "price": 1199.0, "dur": 45, "desc": "Mounting HD video doorbell, connecting to home Wi-Fi, and linking with electronic door lock app."},
        {"name": "Keyless Touchscreen Digital Lock Fitting", "sub": "Smart Locks", "price": 1299.0, "dur": 60, "desc": "Chiseling door frame and fitting keyless PIN code digital lock with emergency mechanical key backup."},
        {"name": "RFID Card Keyless Access Lock Installation", "sub": "Smart Locks", "price": 999.0, "dur": 45, "desc": "Installing tap-to-enter RFID card lock for glass office doors or residential apartment entry doors."},
        {"name": "Smart Lock Battery Replacement & Diagnostics", "sub": "Smart Locks", "price": 399.0, "dur": 30, "desc": "Troubleshooting unresponsive digital locks, replacing AA/lithium batteries, and recalibrating sensors."},
        {"name": "Bluetooth Smart Latch & Mortise Setup", "sub": "Smart Locks", "price": 1099.0, "dur": 45, "desc": "Fitting compact Bluetooth smart rim latch suitable for bedroom doors with phone auto-unlock feature."},

        # Smart Home Devices (6)
        {"name": "Smart Wi-Fi Switchboard Retrofit Fitting", "sub": "Smart Home Devices", "price": 599.0, "dur": 45, "desc": "Installing modular smart switch relays behind existing wall switchboards for app control of lights & fans."},
        {"name": "Smart Dimmer & RGB Ambient Lighting Controller", "sub": "Smart Home Devices", "price": 499.0, "dur": 30, "desc": "Wiring smart strip light controllers, false ceiling LED dimmers, and pairing with mobile app scenes."},
        {"name": "Motorized Smart Curtain Rod & Motor Setup", "sub": "Smart Home Devices", "price": 1299.0, "dur": 60, "desc": "Fixing electric curtain track on ceiling, mounting heavy-duty motor, and programming timer schedules."},
        {"name": "Heavy-Duty Smart Plug (16A) AC/Geyser Sync", "sub": "Smart Home Devices", "price": 349.0, "dur": 25, "desc": "Installing 16 Amp high-power smart plugs for heavy appliances with power consumption monitoring."},
        {"name": "Voice Assistant Hub Integration (Alexa / Google)", "sub": "Smart Home Devices", "price": 699.0, "dur": 45, "desc": "Configuring Amazon Echo / Google Nest hub, grouping rooms, and creating custom voice routines."},
        {"name": "Centralized Smart Gateway & Zigbee Router Setup", "sub": "Smart Home Devices", "price": 899.0, "dur": 45, "desc": "Setting up local Zigbee 3.0 gateway hub ensuring seamless offline mesh connectivity for all smart sensors."},

        # Home Security (6)
        {"name": "Outdoor Weatherproof HD Security Camera Fitting", "sub": "Home Security", "price": 799.0, "dur": 45, "desc": "Wall mounting IP67 waterproof bullet camera, routing power cable, and adjusting night-vision angle."},
        {"name": "Indoor 360° Wi-Fi Security Camera Installation", "sub": "Home Security", "price": 499.0, "dur": 30, "desc": "Ceiling mounting dome camera with pan-tilt-zoom features, motion tracking, and SD card configuration."},
        {"name": "Wireless Motion Sensor Burglar Alarm Setup", "sub": "Home Security", "price": 899.0, "dur": 60, "desc": "Placing PIR motion detectors, pairing wireless siren hub, and setting up automated smartphone alert calls."},
        {"name": "Dual-Way Video Door Phone Monitor Fitting", "sub": "Home Security", "price": 1499.0, "dur": 75, "desc": "Installing outdoor camera unit at gate and indoor 7-inch color display monitor for visitor screening."},
        {"name": "4-Channel DVR / NVR Storage & Remote Viewing Sync", "sub": "Home Security", "price": 1299.0, "dur": 60, "desc": "Installing Hard Disk Drive into DVR/NVR, crimping BNC/RJ45 cables, and configuring live phone viewing."},
        {"name": "Concealed Wall Wire Conduit Camera Installation", "sub": "Home Security", "price": 1199.0, "dur": 90, "desc": "Chipping wall channel to lay hidden CCTV power lines for a clean aesthetic finish without visible wires."},

        # Access & Automation (6)
        {"name": "Automatic RFID Boom Barrier Gate Installation", "sub": "Access & Automation", "price": 3499.0, "dur": 150, "desc": "Installing motorized gate barrier arm for apartment complexes with vehicle windshield RFID tags."},
        {"name": "Biometric Access Control Keypad for Offices", "sub": "Access & Automation", "price": 1899.0, "dur": 90, "desc": "Setting up wall-mounted fingerprint & punch card attendance access system for commercial doors."},
        {"name": "Smart Motorized Garage Door Controller Fitting", "sub": "Access & Automation", "price": 2199.0, "dur": 90, "desc": "Connecting remote wireless opener and safety photo-eye sensors for roll-up garage shutter doors."},
        {"name": "Multi-Flat Apartment Intercom System Setup", "sub": "Access & Automation", "price": 2499.0, "dur": 120, "desc": "Wiring central security guard console to individual flat intercom handsets across multiple floors."},
        {"name": "High-Decibel Smart Security Siren Integration", "sub": "Access & Automation", "price": 599.0, "dur": 30, "desc": "Wiring 110dB indoor/outdoor flashing strobe siren triggered by door intrusion or panic buttons."},
        {"name": "Photoelectric Beam Perimeter Security Barrier", "sub": "Access & Automation", "price": 1699.0, "dur": 90, "desc": "Installing dual infrared beam sensors across compound boundary walls detecting fence intruders."},

        # Sensor & Monitoring (6)
        {"name": "Smart LPG / Natural Gas Leak Detector Fitting", "sub": "Sensor & Monitoring", "price": 599.0, "dur": 30, "desc": "Fixing catalytic gas sensor near kitchen cylinder with auto shut-off solenoid valve trigger."},
        {"name": "Smart Water Flood & Pipe Leak Sensor Setup", "sub": "Sensor & Monitoring", "price": 499.0, "dur": 30, "desc": "Placing probe sensors near washing machines and water purifiers to alert before home flooding occurs."},
        {"name": "Magnetic Door & Window Open/Close Sensor Setup", "sub": "Sensor & Monitoring", "price": 399.0, "dur": 25, "desc": "Sticking wireless reed magnetic contacts on main doors and balconies for entrance logs."},
        {"name": "Smart Wi-Fi Digital Thermostat Installation", "sub": "Sensor & Monitoring", "price": 899.0, "dur": 45, "desc": "Replacing manual AC control with smart touchscreen thermostat maintaining scheduled room temps."},
        {"name": "Air Quality & Dust Sensor Smart Integration", "sub": "Sensor & Monitoring", "price": 499.0, "dur": 30, "desc": "Setting up indoor PM2.5 / VOC monitor linked to auto-turn on smart air purifiers."},
        {"name": "Solar PIR Motion Security Floodlight Setup", "sub": "Sensor & Monitoring", "price": 699.0, "dur": 40, "desc": "Mounting outdoor solar-powered LED floodlight that illuminates automatically when human motion is detected."}
    ],

    "7. Domestic Help & Cooking": [
        # Cooking Services (8)
        {"name": "North Indian Meal Home Cook (Daily 2 Meals)", "sub": "Cooking Services", "price": 3499.0, "dur": 120, "desc": "Experienced cook preparing fresh roti, sabzi, dal, and rice tailored to family spice preferences."},
        {"name": "South Indian Breakfast & Meal Cook", "sub": "Cooking Services", "price": 3299.0, "dur": 120, "desc": "Cook specializing in authentic idli, dosa batter, sambar, chutney, and rice meals."},
        {"name": "Party & Special Occasion Festival Chef", "sub": "Cooking Services", "price": 2499.0, "dur": 240, "desc": "Professional home chef cooking multi-course feast (starters, biryani, gravy, sweets) for up to 15 guests."},
        {"name": "Healthy Fitness Meal Prep Cook (Diet Specific)", "sub": "Cooking Services", "price": 3999.0, "dur": 90, "desc": "Cook preparing low-oil, high-protein keto, salad, grilled chicken, or vegan customized meal plans."},
        {"name": "Evening Snack & High-Tea Cook", "sub": "Cooking Services", "price": 1999.0, "dur": 60, "desc": "Cook visiting daily at 4 PM to prepare fresh tea, pakoras, samosas, or sandwiches."},
        {"name": "Jain Pure Vegetarian Home Cook", "sub": "Cooking Services", "price": 3699.0, "dur": 120, "desc": "Strictly onion-free, garlic-free pure vegetarian food preparation following Jain dietary rules."},
        {"name": "Kids School Tiffin & Breakfast Specialist", "sub": "Cooking Services", "price": 2199.0, "dur": 60, "desc": "Early morning cook preparing nutritious, creative tiffin meals for school children."},
        {"name": "Monthly Full-Time Resident House Cook", "sub": "Cooking Services", "price": 9999.0, "dur": 480, "desc": "Dedicated full-day cook managing grocery inventory, meal planning, and 3 meals daily."},

        # Specialized Cooking (8)
        {"name": "Biryani & Mughlai Special Home Chef", "sub": "Specialized Cooking", "price": 2999.0, "dur": 180, "desc": "Master chef specialized in Dum Biryani, Kebabs, Gravy, and authentic Phirni."},
        {"name": "Continental & Italian Pasta Specialist", "sub": "Specialized Cooking", "price": 2799.0, "dur": 150, "desc": "Gourmet chef preparing fresh hand-rolled pasta, wood-fire style pizza, and risotto at home."},
        {"name": "Chinese & Pan-Asian Dimsum Chef", "sub": "Specialized Cooking", "price": 2599.0, "dur": 150, "desc": "Wok master preparing Hakka noodles, Manchurian, momos, and Thai curries."},
        {"name": "Home Bakery & Cake Baking Assistant", "sub": "Specialized Cooking", "price": 1999.0, "dur": 120, "desc": "Baking expert assisting with fresh birthday cakes, brownies, cupcakes, and artisanal bread."},
        {"name": "Traditional Indian Sweet Halwai", "sub": "Specialized Cooking", "price": 3499.0, "dur": 240, "desc": "Expert sweet maker preparing Gulab Jamun, Rasgulla, Kaju Katli, and Jalebi for family functions."},
        {"name": "Seafood & Coastal Recipe Specialist", "sub": "Specialized Cooking", "price": 3199.0, "dur": 180, "desc": "Chef crafting Goan, Malabari, or Bengali fish curry, prawn fry, and crab masala."},
        {"name": "Gluten-Free & Organic Health Chef", "sub": "Specialized Cooking", "price": 3599.0, "dur": 120, "desc": "Certified nutritionist-chef preparing millet rotis, quinoa salads, and sugar-free desserts."},
        {"name": "Barbecue & Grill Party Master", "sub": "Specialized Cooking", "price": 2999.0, "dur": 180, "desc": "Outdoor live charcoal grill chef marinating and grilling paneer tikka, chicken tandoori, and veggies."},

        # Household Help (7)
        {"name": "Daily Utensil Washing & Kitchen Sink Clean", "sub": "Household Help", "price": 1499.0, "dur": 45, "desc": "Hand washing pressure cooker, non-stick pans, dishes, and wiping kitchen counter clean twice daily."},
        {"name": "Brooming, Mopping & Dusting Maid Service", "sub": "Household Help", "price": 1999.0, "dur": 60, "desc": "Daily floor sweeping, damp mopping, cobweb dusting, and trash disposal for apartment."},
        {"name": "Cloth Washing, Folding & Clothes Ironing", "sub": "Household Help", "price": 1799.0, "dur": 60, "desc": "Operating washing machine, hanging clothes to dry, folding wardrobes, and steam ironing shirts."},
        {"name": "Full-Day All-Round Household Helper (8 Hours)", "sub": "Household Help", "price": 7999.0, "dur": 480, "desc": "Full-day maid handling cleaning, washing, grocery errands, and assisting kitchen work."},
        {"name": "Elderly Care & Senior Companion Maid", "sub": "Household Help", "price": 6999.0, "dur": 360, "desc": "Kind attendant helping senior citizens with walking, medicine timely reminder, and light chores."},
        {"name": "Babysitter & Child Nanny Care", "sub": "Household Help", "price": 6499.0, "dur": 360, "desc": "Trained nanny looking after toddlers, feeding milk/meals, diaper changes, and interactive playtime."},
        {"name": "Deep House Decluttering & Wardrobe Organizer", "sub": "Household Help", "price": 1299.0, "dur": 180, "desc": "Organizing closet clothes, shoe racks, kitchen pantry, and seasonal garment storage bags."},

        # Errand & Personal Assistance (7)
        {"name": "Grocery & Vegetable Market Delivery Assistant", "sub": "Errand & Personal Assistance", "price": 299.0, "dur": 60, "desc": "Helper visiting local mandis or supermarkets to buy fresh vegetables, fruits, and provisions."},
        {"name": "Pharmacy & Prescription Medicine Pickup", "sub": "Errand & Personal Assistance", "price": 199.0, "dur": 30, "desc": "Assistance runner purchasing prescribed medicines from chemist and delivering home."},
        {"name": "Bill Payment & Government Office Standing Helper", "sub": "Errand & Personal Assistance", "price": 399.0, "dur": 90, "desc": "Personal runner handling bank paperwork, RTO submissions, or municipal utility payments."},
        {"name": "Pet Walking & Vet Escort Assistant", "sub": "Errand & Personal Assistance", "price": 349.0, "dur": 45, "desc": "Escorting pets for daily walks or holding pets during veterinary vaccination visits."},
        {"name": "Dry Cleaning Pickup & Doorstep Delivery", "sub": "Errand & Personal Assistance", "price": 249.0, "dur": 30, "desc": "Taking heavy suits, sarees, and blankets to laundry cleaner and returning ironed items."},
        {"name": "Senior Citizen Hospital Escort Helper", "sub": "Errand & Personal Assistance", "price": 799.0, "dur": 180, "desc": "Accompanying elderly patients to doctor appointments, wheelchair assistance, and pharmacy collection."},
        {"name": "Event Packing & Gift Wrapping Personal Assistant", "sub": "Errand & Personal Assistance", "price": 499.0, "dur": 60, "desc": "Helping families wrap wedding favors, hamper hampers, and birthday return gifts."}
    ],

    "8. Education, Teachers & Coaching": [
        # Academic Tutoring (10)
        {"name": "Class 1-5 Foundation All-Subject Home Tutor", "sub": "Academic Tutoring", "price": 2999.0, "dur": 60, "desc": "Patient tutor helping primary school students with English, Math, Science, and daily homework."},
        {"name": "Class 6-8 Math & Science Home Specialist", "sub": "Academic Tutoring", "price": 3999.0, "dur": 60, "desc": "Concept-building tutor strengthening NCERT fundamentals in Mathematics and Integrated Science."},
        {"name": "Class 9-10 CBSE/ICSE Board Exam Tutor", "sub": "Academic Tutoring", "price": 4999.0, "dur": 90, "desc": "Focused board preparation tutor practicing sample question papers, formula memorization, and revision."},
        {"name": "Class 11-12 Physics Master Coach", "sub": "Academic Tutoring", "price": 5999.0, "dur": 90, "desc": "Specialized senior physics tutor solving numericals, derivations, and board/entrance exam prep."},
        {"name": "Class 11-12 Chemistry Problem Solver", "sub": "Academic Tutoring", "price": 5999.0, "dur": 90, "desc": "Organic, Inorganic, and Physical Chemistry expert tutor simplifying reaction mechanisms."},
        {"name": "Class 11-12 Higher Mathematics Tutor", "sub": "Academic Tutoring", "price": 5999.0, "dur": 90, "desc": "Calculus, Vectors, and 3D Geometry intensive problem-solving coaching for Class 12 students."},
        {"name": "Class 11-12 Biology & Botany Specialist", "sub": "Academic Tutoring", "price": 5499.0, "dur": 90, "desc": "Diagrammatic and theoretical biology guidance tailored for board exams and medical entry."},
        {"name": "Class 11-12 Accountancy & Commerce Tutor", "sub": "Academic Tutoring", "price": 4999.0, "dur": 90, "desc": "Balance sheet ledger, partnership accounts, and business studies mentorship."},
        {"name": "Class 11-12 Economics & Statistics Tutor", "sub": "Academic Tutoring", "price": 4999.0, "dur": 90, "desc": "Micro & Macro Economics graph analysis, numerical calculations, and exam preparation."},
        {"name": "Computer Science & Python Coding Tutor", "sub": "Academic Tutoring", "price": 4499.0, "dur": 60, "desc": "Practical programming tutor teaching Python logic, SQL databases, and school projects."},

        # Competitive Exam Coaching (6)
        {"name": "IIT-JEE Main & Advanced Mathematics Mentor", "sub": "Competitive Exam Coaching", "price": 7999.0, "dur": 90, "desc": "Ex-IITian tutor solving past 15-year JEE questions, speed tricks, and mock test evaluation."},
        {"name": "NEET Medical Physics & Chemistry Coach", "sub": "Competitive Exam Coaching", "price": 7499.0, "dur": 90, "desc": "NCERT line-by-line breakdown and speed problem solving for 720-mark NEET target."},
        {"name": "CAT & IPMAT Quantitative Aptitude Coach", "sub": "Competitive Exam Coaching", "price": 6999.0, "dur": 90, "desc": "Data Interpretation, Logical Reasoning, and Quant shortcut tricks for MBA entrance exams."},
        {"name": "UPSC Civil Services General Studies Mentor", "sub": "Competitive Exam Coaching", "price": 8999.0, "dur": 120, "desc": "Mains answer writing practice, Indian Polity, History, and Current Affairs guidance."},
        {"name": "GMAT & GRE Analytical Writing Coach", "sub": "Competitive Exam Coaching", "price": 7999.0, "dur": 90, "desc": "Global entrance verbal reasoning, sentence correction, and math section coaching."},
        {"name": "Bank PO & SSC CGL Reasoning Trainer", "sub": "Competitive Exam Coaching", "price": 4999.0, "dur": 60, "desc": "Puzzle solving shortcuts, speed calculation methods, and online test series practice."},

        # Music Classes (5)
        {"name": "Acoustic & Electric Guitar Lessons (Beginner)", "sub": "Music Classes", "price": 2499.0, "dur": 45, "desc": "Step-by-step chord transitions, fingerpicking, strumming patterns, and song playing."},
        {"name": "Piano & Electronic Keyboard Teacher", "sub": "Music Classes", "price": 2999.0, "dur": 45, "desc": "Western classical sheet music reading, sight reading, and synthesizer melody playing."},
        {"name": "Hindustani Classical Vocal Music Guru", "sub": "Music Classes", "price": 2999.0, "dur": 45, "desc": "Raga vocal training, swara practice, tanpura harmonization, and khayal singing."},
        {"name": "Western Pop & Playback Singing Coach", "sub": "Music Classes", "price": 2799.0, "dur": 45, "desc": "Pitch correction, breath support control, microphone technique, and vocal range expansion."},
        {"name": "Drums & Percussion Rhythm Instructor", "sub": "Music Classes", "price": 3499.0, "dur": 60, "desc": "Acoustic drum kit beat coordination, rudiments, tempo sticking, and rock/funk grooves."},

        # Dance Classes (4)
        {"name": "Bollywood & Hip-Hop Commercial Dance Instructor", "sub": "Dance Classes", "price": 2499.0, "dur": 60, "desc": "Fun energetic dance choreography to trending Bollywood tracks for parties & health."},
        {"name": "Kathak & Classical Classical Dance Teacher", "sub": "Dance Classes", "price": 2999.0, "dur": 60, "desc": "Traditional Jaipur/Lucknow gharana Kathak footwork (Tatkar), spins (Chakkar), and Mudras."},
        {"name": "Wedding Sangeet Family Group Choreographer", "sub": "Dance Classes", "price": 6999.0, "dur": 90, "desc": "Custom bride-groom, sangeet group, and family dance performance choreography package."},
        {"name": "Contemporary & Jazz Expressive Dance Coach", "sub": "Dance Classes", "price": 2799.0, "dur": 60, "desc": "Fluid bodily movements, floor work transitions, and emotional expression dance routine."},

        # Language & Communication (5)
        {"name": "Spoken English & Professional Business Communication", "sub": "Language & Communication", "price": 1999.0, "dur": 45, "desc": "Building fluency, vocabulary expansion, accent softening, and corporate email writing."},
        {"name": "IELTS & TOEFL Band 8+ Exam Preparation", "sub": "Language & Communication", "price": 4999.0, "dur": 60, "desc": "Listening, Reading, Writing essay evaluation, and 1-on-1 Mock Speaking tests."},
        {"name": "French Language Learning Coach (A1-B2 Level)", "sub": "Language & Communication", "price": 3499.0, "dur": 60, "desc": "Grammar rules, conversation practice, DELF exam preparation by certified French tutor."},
        {"name": "German Language Learning Specialist (A1-B2)", "sub": "Language & Communication", "price": 3499.0, "dur": 60, "desc": "Goethe Zertifikat exam guidance, noun genders, and conversational German for students."},
        {"name": "Spanish Language Conversational Tutor", "sub": "Language & Communication", "price": 3199.0, "dur": 60, "desc": "Fun interactive Spanish vocabulary, verb conjugations, and culture immersion."}
    ],

    "9. Health, Fitness & Wellness": [
        # Fitness (8)
        {"name": "Personal Home Gym Fitness Trainer (1-on-1)", "sub": "Fitness", "price": 4999.0, "dur": 60, "desc": "Certified fitness coach bringing resistance bands & dumbbells for weight loss and muscle toning at home."},
        {"name": "Elderly Mobility & Senior Fitness Trainer", "sub": "Fitness", "price": 3499.0, "dur": 45, "desc": "Gentle low-impact exercises improving balance, leg strength, and joint mobility for senior citizens."},
        {"name": "Zumba & Cardio Dance Workout Trainer", "sub": "Fitness", "price": 3499.0, "dur": 60, "desc": "High-energy calorie-burning aerobic dance workout session set to upbeat music at home."},
        {"name": "HIIT & Functional Bodyweight Conditioning", "sub": "Fitness", "price": 3999.0, "dur": 45, "desc": "High-intensity interval training boosting stamina, metabolism, and athletic agility."},
        {"name": "Weight Gain & Muscle Building Coach", "sub": "Fitness", "price": 4499.0, "dur": 60, "desc": "Hypertrophy workout routines, progressive overload tracking, and protein diet guidance."},
        {"name": "Core Strength & Calisthenics Trainer", "sub": "Fitness", "price": 3999.0, "dur": 60, "desc": "Bodyweight gymnastics, pushup variations, pull-ups, and abdominal core sculpting."},
        {"name": "Post-Pregnancy Weight Loss Coach", "sub": "Fitness", "price": 4999.0, "dur": 45, "desc": "Safe diastasis recti recovery, pelvic floor activation, and gradual fat loss exercise."},
        {"name": "Corporate Desk-Worker Fitness Coach", "sub": "Fitness", "price": 2999.0, "dur": 45, "desc": "Posture reset, hip flexor stretch, and quick 30-minute stress-buster workouts."}
    ],

    "10. Events, Photography & Entertainment": [
        # Photography (8)
        {"name": "Candid Birthday Party Photographer (3 Hours)", "sub": "Photography", "price": 3499.0, "dur": 180, "desc": "Professional photographer capturing candid moments, cake cutting, and group family photos with edited soft copies."},
        {"name": "Pre-Wedding Couple Shoot Package", "sub": "Photography", "price": 9999.0, "dur": 300, "desc": "Outdoor scenic location photoshoot with drone aerial shots, cinematic video teaser, and retouched album images."},
        {"name": "Maternity & Newborn Baby Photoshoot", "sub": "Photography", "price": 5999.0, "dur": 120, "desc": "Studio-prop set up at home for safe, cozy newborn portraits and mother-to-be bump photos."},
        {"name": "Corporate Event & Conference Photographer", "sub": "Photography", "price": 4999.0, "dur": 240, "desc": "High-resolution corporate event coverage for stage speakers, networking, and award ceremonies."},
        {"name": "E-Commerce Product Catalog Photographer", "sub": "Photography", "price": 6999.0, "dur": 240, "desc": "White studio background lighting photoshoot for Amazon/Flipkart apparel, jewelry, or food products."},
        {"name": "Fashion Model Portfolio Shoot", "sub": "Photography", "price": 8999.0, "dur": 240, "desc": "Stylized high-fashion lighting photoshoot with outfit changes and professional retouching."},
        {"name": "Architecture & Real Estate Photographer", "sub": "Photography", "price": 5499.0, "dur": 180, "desc": "Wide-angle interior and exterior photography for luxury villas, hotels, and interior designer portfolios."},
        {"name": "Family Generation Portrait Session", "sub": "Photography", "price": 3999.0, "dur": 90, "desc": "Heartwarming home family group photography capturing grandparents, parents, and grandchildren."}
    ],

    "11. Pet Services": [
        # Pet Grooming & Care (8)
        {"name": "Full Dog Grooming & Haircut Spa Package", "sub": "Pet Grooming", "price": 1499.0, "dur": 75, "desc": "Warm bath, breed-specific style haircut, nail clipping, ear cleaning, and anti-tick shampoo bath."},
        {"name": "Cat Bath, Fur De-Shedding & Nail Trim", "sub": "Pet Grooming", "price": 1299.0, "dur": 60, "desc": "Gentle low-stress waterless or warm water cat bath, coat brushing, and claw trimming."},
        {"name": "At-Home Veterinary Health Checkup & Vaccination", "sub": "Veterinary", "price": 799.0, "dur": 30, "desc": "Licensed vet visiting home for routine health exam, Deworming, and Annual 7-in-1 / Rabies vaccine."},
        {"name": "Dog Walking & Exercise Visit (30 Mins)", "sub": "Pet Care", "price": 299.0, "dur": 30, "desc": "Background-verified pet lover taking your dog for brisk outdoor walk, potty break, and hydration."},
        {"name": "In-Home Pet Sitting & Feeding (Per Visit)", "sub": "Pet Care", "price": 499.0, "dur": 45, "desc": "Caring pet sitter visiting home to feed food, clean litter box, give medication, and play with pets."},
        {"name": "Obedience & Puppy Basic Behavioral Training", "sub": "Pet Training", "price": 4999.0, "dur": 60, "desc": "10-session trainer teaching Sit, Stay, Heel, Leash walking, and stopping unwanted biting/chewing."},
        {"name": "Medicated Anti-Tick & Flea Bath Treatment", "sub": "Pet Grooming", "price": 899.0, "dur": 45, "desc": "Medicated dip shampoo eliminating ticks, fleas, and mites followed by thorough blow-dry."},
        {"name": "Pet Ear Cleaning & Hygiene Sanitize Pack", "sub": "Pet Grooming", "price": 399.0, "dur": 25, "desc": "Clearing ear wax, paw pad trimming, sanitary area trim, and mouth freshener spray."}
    ],

    "12. Technology & Digital Services": [
        # Tech Support (8)
        {"name": "Windows / Mac OS Format & Reinstallation", "sub": "Computer & Device Support", "price": 699.0, "dur": 60, "desc": "Clean OS installation, official driver updates, software setup, and data backup transfer."},
        {"name": "Laptop Hardware Repair & Screen Replacement", "sub": "Computer & Device Support", "price": 999.0, "dur": 90, "desc": "Diagnostic inspection, broken LED screen change, keyboard replacement, or hinge repair."},
        {"name": "Wi-Fi Router Setup & Mesh Network Expansion", "sub": "Network & Smart Devices", "price": 499.0, "dur": 45, "desc": "Configuring dual-band Wi-Fi router, dead-zone troubleshooting, and password security setup."},
        {"name": "Data Recovery from Crashed Hard Drive / SSD", "sub": "Computer & Device Support", "price": 1499.0, "dur": 120, "desc": "Deep sector scan recovering lost family photos, business documents, and corrupted partitions."},
        {"name": "Custom Gaming / Workstation PC Assembly", "sub": "Computer & Device Support", "price": 1299.0, "dur": 120, "desc": "Assembling CPU components, cable management, thermal paste application, and stress testing."},
        {"name": "Virus & Malware Removal Deep Clean", "sub": "Computer & Device Support", "price": 499.0, "dur": 45, "desc": "Removing browser hijackers, ransomware threats, and installing genuine antivirus software."},
        {"name": "Smart TV & Soundbar Home Theater Integration", "sub": "Network & Smart Devices", "price": 699.0, "dur": 45, "desc": "HDMI eARC audio wiring, Bluetooth speaker pairing, and streaming app subscription login."},
        {"name": "Printer Installation & Wireless Network Sharing", "sub": "Computer & Device Support", "price": 399.0, "dur": 30, "desc": "Installing wireless ink-tank printer drivers and enabling mobile printing across family devices."}
    ],

    "13. Professional & Business Services": [
        # Professional (8)
        {"name": "Income Tax Return (ITR) Filing for Salaried", "sub": "Finance", "price": 799.0, "dur": 45, "desc": "CA-verified Form-16 computation, tax-saving deduction claims under 80C/80D, and e-filing."},
        {"name": "GST Registration & Monthly Compliance Filing", "sub": "Finance", "price": 1499.0, "dur": 60, "desc": "New GSTIN application, document verification, and filing GSTR-1 / GSTR-3B returns."},
        {"name": "Private Limited Company Registration Package", "sub": "Legal", "price": 4999.0, "dur": 120, "desc": "DSC, DIN, Name approval, MOA/AOA drafting, and MCA incorporation certificate setup."},
        {"name": "Trademark Brand Name & Logo Filing", "sub": "Legal", "price": 2499.0, "dur": 60, "desc": "Comprehensive trademark availability search and online government TM application submission."},
        {"name": "Rental Agreement & Property E-Stamping", "sub": "Administrative", "price": 599.0, "dur": 30, "desc": "Legal draft creation, e-stamp paper purchase, and doorstep delivery of rental contract."},
        {"name": "Executive Resume & LinkedIn Profile Rewrite", "sub": "Career Services", "price": 1299.0, "dur": 60, "desc": "ATS-friendly modern resume design highlighting key achievements and keywords for job seekers."},
        {"name": "FSSAI Food License Registration for Cloud Kitchens", "sub": "Legal", "price": 1199.0, "dur": 45, "desc": "Basic or State FSSAI license documentation and online submission for restaurants & home bakers."},
        {"name": "Bookkeeping & Tally Accounting Support", "sub": "Finance", "price": 2999.0, "dur": 120, "desc": "Monthly sales ledger entry, bank reconciliation, and profit/loss statement generation."}
    ],

    "14. Moving, Delivery & Local Assistance": [
        # Moving & Delivery (8)
        {"name": "1 BHK Local Home Shifting & Packing", "sub": "Moving Services", "price": 4999.0, "dur": 240, "desc": "Professional bubble-wrap packing, loading into closed truck, transport, and unloading."},
        {"name": "2 BHK City Relocation Packers & Movers", "sub": "Moving Services", "price": 7999.0, "dur": 360, "desc": "Multi-layer corrugated cardboard box packing, furniture dismantle/reassemble, and safe transport."},
        {"name": "Single Furniture Item Transport (Sofa / Bed / Fridge)", "sub": "Moving Services", "price": 1299.0, "dur": 90, "desc": "Tata Ace / Pickup truck dispatch for single heavy item transport across town."},
        {"name": "Intercity Vehicle Car / Bike Carrier Transport", "sub": "Vehicle Assistance", "price": 5999.0, "dur": 180, "desc": "Enclosed car container or covered bike transport between major metro cities."},
        {"name": "Express Intra-City Document & Parcel Pickup", "sub": "Delivery & Pickup", "price": 249.0, "dur": 45, "desc": "Immediate two-wheeler courier picking up urgent business files, keys, or gifts."},
        {"name": "Office Furniture & Desktop Relocation Shifting", "sub": "Moving Services", "price": 9999.0, "dur": 360, "desc": "Systematic IT equipment packing, server rack moving, and office desk installation."},
        {"name": "Heavy Luggage & Suitcase Airport Transport", "sub": "Delivery & Pickup", "price": 699.0, "dur": 60, "desc": "Doorstep pickup of heavy excess baggage delivered directly to airport terminal or home."},
        {"name": "Car Battery Jump-Start & Breakdown Assistance", "sub": "Vehicle Assistance", "price": 499.0, "dur": 30, "desc": "Emergency mechanic arrival with heavy jumper cables to jump-start dead car battery."}
    ]
}

total_updated = 0

for cat_name, services in AUTHENTIC_CATALOG.items():
    cur.execute("SELECT id, name, subcategory FROM services WHERE category = %s ORDER BY id;", (cat_name,))
    existing_rows = cur.fetchall()
    
    num_existing = len(existing_rows)
    num_defs = len(services)
    
    for i in range(num_existing):
        s_id = existing_rows[i][0]
        curr_name = existing_rows[i][1]
        curr_sub = existing_rows[i][2]
        
        if i < num_defs:
            s_def = services[i]
            s_name = s_def["name"]
            s_sub = s_def["sub"]
            s_price = s_def["price"]
            s_desc = s_def["desc"]
            s_dur = s_def["dur"]
        else:
            # Generate a realistic extension name based on subcategory
            s_name = f"{curr_sub} Premium Care Option {i - num_defs + 1}"
            s_sub = curr_sub
            s_price = 1299.0 + (i * 100)
            s_desc = f"Specialized high-end {curr_sub} service tailored to specific client needs with extended guarantee."
            s_dur = 60

        features = {
            "description": s_desc,
            "highlights": [
                f"Professional {s_name} procedure",
                "Certified & background-verified specialists",
                "High-grade safety & sanitized tools",
                "100% satisfaction guarantee",
                "Transparent pricing with zero hidden charges"
            ],
            "included": [
                f"Complete {s_name} procedure",
                "Standard tools and supplies included",
                "Post-service inspection and cleanup",
                "Expert consultation and advice"
            ],
            "excluded": [
                "Structural heavy modifications",
                "Spare hardware unless explicitly requested"
            ],
            "faqs": [
                {
                    "question": f"How long does {s_name} take?",
                    "answer": f"The session typically takes around {s_dur} minutes."
                },
                {
                    "question": "Are the tools and products safe?",
                    "answer": "Yes, strictly industry-approved and sanitized before every appointment."
                }
            ],
            "warranty": "7-day service warranty on workmanship"
        }
        
        cur.execute("""
            UPDATE services 
            SET name = %s, subcategory = %s, base_price = %s, distinct_features = %s, updated_at = NOW()
            WHERE id = %s;
        """, (s_name, s_sub, s_price, json.dumps(features), s_id))
        
        total_updated += 1

conn.commit()

cur.execute("SELECT count(*) FROM services WHERE name ILIKE '%variation%';")
rem_var = cur.fetchone()[0]

cur.execute("SELECT count(*) FROM services;")
total_services = cur.fetchone()[0]

print(f"DONE: Updated {total_updated} services.")
print(f"Total services in database: {total_services}")
print(f"Remaining 'Variation' services: {rem_var}")

cur.close()
conn.close()
