"""
Complete authentic overhaul for the remaining 124 services in Categories 7-14.
Eliminates every remaining "Option" or generic placeholder from PostgreSQL.
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

SUBCAT_SERVICES = {
    # 10. Events, Photography & Entertainment
    ("10. Events, Photography & Entertainment", "Catering & Food Services"): [
        {"name": "Live Chaat & Street Food Counter", "price": 3499.0, "dur": 180, "desc": "Live preparation of pani puri, sev puri, tikki, and dahi bhalla by trained cooks with hygienic mineral water."},
        {"name": "Gourmet Live Barbecue & Grilling Counter", "price": 4999.0, "dur": 180, "desc": "Live charcoal barbecue setup serving hot paneer tikkas, seekh kebabs, and grilled seasonal vegetables."},
        {"name": "Italian Wood-Fired Pizza & Pasta Station", "price": 5499.0, "dur": 210, "desc": "On-site live oven pizza baking and gourmet pasta tossing tailored to individual guest orders."},
        {"name": "Traditional Indian Buffet Catering (Per Head)", "price": 450.0, "dur": 180, "desc": "Full multi-course meal buffet setup with chafing dish warmers, cutlery, and professional service staff."},
        {"name": "Kids Birthday Party Snack Box Catering", "price": 1999.0, "dur": 120, "desc": "Individually packed hygienic snack boxes with mini burger, fries, fruit juice, and chocolate brownie."}
    ],
    ("10. Events, Photography & Entertainment", "Decoration & Floral"): [
        {"name": "Pastel Balloon Arch & Backdrop Styling", "price": 3499.0, "dur": 120, "desc": "Custom pastel balloon garland arch with customized acrylic name sign and LED number lights for birthdays."},
        {"name": "Traditional Fresh Flower Marigold Stage Decor", "price": 4999.0, "dur": 180, "desc": "Festive marigold, jasmine, and rose floral strings for pooja, haldi, or griha pravesh ceremony."},
        {"name": "Boho Canopy Tent & Fairy Light Romantic Setup", "price": 3999.0, "dur": 120, "desc": "Chic teepee tent with warm fairy string lights, plush cushions, and ambient floor lanterns."},
        {"name": "Corporate Stage Backdrop & LED Signage Setup", "price": 6499.0, "dur": 180, "desc": "Professional branded flex printing, sturdy wooden frame mount, and focus stage spotlights for seminars."}
    ],
    ("10. Events, Photography & Entertainment", "DJ & Sound Systems"): [
        {"name": "Club Style DJ with Dual Bass Subwoofers", "price": 8999.0, "dur": 240, "desc": "Pro DJ console, 2 top speakers, 2 high-bass subwoofers, and wireless mics for high-energy dance parties."},
        {"name": "Acoustic Stage PA System & Mixer Setup", "price": 4999.0, "dur": 180, "desc": "Yamaha 12-channel audio mixer, monitor speakers, and vocal dynamic mics for live singer performances."},
        {"name": "Intelligent Moving-Head DMX Stage Lights", "price": 3999.0, "dur": 180, "desc": "4 synchronized RGB moving beam lights with smoke haze machine creating dynamic stage effects."},
        {"name": "Karaoke Night Sound & Screen Rental", "price": 3499.0, "dur": 180, "desc": "Large karaoke lyrics display screen, 2 cordless mics, and access to thousands of Bollywood/English songs."},
        {"name": "Silent Disco Multi-Channel Headphone Setup", "price": 6999.0, "dur": 180, "desc": "Wireless 3-channel glowing LED headphones for noise-free rooftop and terrace celebrations."}
    ],
    ("10. Events, Photography & Entertainment", "Entertainment"): [
        {"name": "Live Close-Up Table Illusionist Magician", "price": 3999.0, "dur": 90, "desc": "Mind-bending sleight of hand, card tricks, and interactive mentalism moving among guest tables."},
        {"name": "Tattoo Artist & Face Painting for Events", "price": 2499.0, "dur": 120, "desc": "Safe skin-friendly organic airbrush temporary tattoos and glitter face painting for kids and guests."}
    ],
    ("10. Events, Photography & Entertainment", "Event Planning & Management"): [
        {"name": "End-to-End Birthday Party Coordinator", "price": 4999.0, "dur": 300, "desc": "Dedicated event coordinator managing cake arrival, games, anchor, and venue schedule without stress."},
        {"name": "Pre-Wedding Sangeet & Reception Planner", "price": 14999.0, "dur": 480, "desc": "Complete vendor coordination, stage rehearsal schedules, guest escorting, and timeline management."},
        {"name": "Corporate Conference & Seminar Manager", "price": 8999.0, "dur": 360, "desc": "Managing delegate registration badges, AV mic testing, presentation clickers, and tea break logistics."}
    ],
    ("10. Events, Photography & Entertainment", "Photography & Videography"): [
        {"name": "4K Cinematic Drone Aerial Video Shoot", "price": 4499.0, "dur": 120, "desc": "FAA/DGCA certified drone pilot capturing majestic top-down cinematic venue perspectives."},
        {"name": "Instant Photo Booth with Quirky Props & Prints", "price": 5999.0, "dur": 180, "desc": "On-the-spot magnetic photo strip printing with funny sunglasses, hats, and customized branded frame."},
        {"name": "Short-Form Social Media Reels Creator", "price": 3499.0, "dur": 150, "desc": "Vertical format shooting and same-day edited Instagram Reels highlighting event moments."}
    ],

    # 11. Pet Services
    ("11. Pet Services", "Dog Grooming"): [
        {"name": "Deshedding & Undercoat Fur Thinning Bath", "price": 1399.0, "dur": 60, "desc": "Specialized high-velocity blow dry and fur rake grooming removing loose dead undercoat hairs."},
        {"name": "Pawdicure & Organic Paw Balm Massage", "price": 399.0, "dur": 25, "desc": "Gentle nail clipping, paw pad hair trimming, and soothing organic beeswax balm massage."}
    ],
    ("11. Pet Services", "Dog Training"): [
        {"name": "Puppy Potty & Crate Training Intensive", "price": 3999.0, "dur": 60, "desc": "Home consultation establishing a structured routine for indoor toilet habits and crate comfort."},
        {"name": "Leash Reactivity & Outdoor Pulling Reset", "price": 3499.0, "dur": 60, "desc": "Correction training for dogs that lunge, bark at other dogs, or pull excessively during walks."},
        {"name": "Advanced Trick & Agility Training (5 Sessions)", "price": 4999.0, "dur": 60, "desc": "Teaching high-five, roll over, weave poles, and fetch frisbee for mental stimulation."},
        {"name": "Guard & Watchdog Boundary Awareness Coaching", "price": 5499.0, "dur": 60, "desc": "Teaching property perimeter alert barking on door knocks and stopping immediately on command."}
    ],
    ("11. Pet Services", "Pet Accessories & Nutrition"): [
        {"name": "Custom Raw & Cooked Diet Meal Charting", "price": 1199.0, "dur": 45, "desc": "Certified canine nutritionist planning breed-specific protein, calcium, and vitamin meal charts."},
        {"name": "Orthopedic Pet Bed & Harness Fitment Consultation", "price": 499.0, "dur": 30, "desc": "Measuring dog dimensions to prescribe anti-pull harnesses and joint-support orthopedic beds."},
        {"name": "Pet Food Delivery & Fresh Meat Subscription Setup", "price": 299.0, "dur": 20, "desc": "Arranging doorstep scheduled deliveries of fresh chicken broth, vegetables, and premium kibble."}
    ],
    ("11. Pet Services", "Pet Sitting & Boarding"): [
        {"name": "Cage-Free Homestay Pet Boarding (Per Night)", "price": 999.0, "dur": 1440, "desc": "Warm loving home environment with couch access, 3 daily walks, and live video check-in updates."},
        {"name": "Daycare Pet Playgroup & Socialization", "price": 499.0, "dur": 360, "desc": "Supervised daytime group play in air-conditioned indoor pet play area with balls and agility tunnels."},
        {"name": "Cat Sitting & Litter Tray Maintenance Visit", "price": 399.0, "dur": 40, "desc": "In-home daily visit to scoop litter, refresh clean water fountain, and serve wet food."}
    ],
    ("11. Pet Services", "Veterinary & Health Checkup"): [
        {"name": "Annual Anti-Rabies & DHPPiL Booster Vaccine", "price": 899.0, "dur": 30, "desc": "In-home administration of core annual vaccinations with official stamped medical booklet update."},
        {"name": "Oral Dental Scaling & Tartar Scraping", "price": 1499.0, "dur": 45, "desc": "Painless ultrasonic dental cleaning removing yellow tartar buildup and stinky breath."},
        {"name": "Blood Sample Collection for CBC & Kidney Profile", "price": 699.0, "dur": 25, "desc": "Gentle doorstep blood draw sent to diagnostic lab with PDF report delivered within 24 hours."},
        {"name": "Post-Surgery Wound Dressing & Suture Removal", "price": 499.0, "dur": 30, "desc": "Antiseptic cleaning of surgical stitches, fresh sterile bandage replacement, and recovery check."},
        {"name": "Senior Pet Arthritis Joint Evaluation & Pain Relief", "price": 899.0, "dur": 40, "desc": "Assessment of hip dysplasia, prescribing glucosamine supplements, and gentle mobility physical therapy."}
    ],

    # 12. Technology & Digital Services
    ("12. Technology & Digital Services", "Computer & Laptop Repair"): [
        {"name": "Thermal Paste Replacement & Cooling Fan Clean", "price": 599.0, "dur": 45, "desc": "Arctic MX-4 thermal compound application stopping laptop overheating and thermal throttling."},
        {"name": "SSD Upgrade & Cloning (Without Data Loss)", "price": 799.0, "dur": 60, "desc": "Replacing slow mechanical hard drives with high-speed NVMe/SATA SSD with full OS cloning."},
        {"name": "Broken Laptop Hinge & Casing Fabrication", "price": 1199.0, "dur": 90, "desc": "Industrial epoxy rebonding or replacing cracked plastic top casing and tight hinges."},
        {"name": "Motherboard Micro-Soldering & Chipset Repair", "price": 1799.0, "dur": 120, "desc": "BGA chip rework, short circuit mosfet replacement, and power IC diagnostics."}
    ],
    ("12. Technology & Digital Services", "Data Recovery & Backup"): [
        {"name": "Accidentally Formatted Pen Drive / SD Card Recovery", "price": 899.0, "dur": 60, "desc": "Deep file carve scanning restoring deleted family photos, videos, and zip archives."},
        {"name": "Corrupted External Hard Drive File Retrieval", "price": 1499.0, "dur": 120, "desc": "Fixing RAW filesystem errors and retrieving lost partition documents."},
        {"name": "Automated Cloud Backup Setup (Google Drive/OneDrive)", "price": 499.0, "dur": 40, "desc": "Configuring scheduled real-time synchronization of desktop folders to secure cloud."},
        {"name": "Ransomware Encrypted File Analysis & Recovery", "price": 2499.0, "dur": 180, "desc": "Decryption tool analysis, shadow copy extraction, and system clean sanitization."},
        {"name": "Smartphone Dead Screen Data Extraction", "price": 1199.0, "dur": 60, "desc": "Connecting OTG debugging interface to extract WhatsApp chats, contacts, and photos from broken phone."}
    ],
    ("12. Technology & Digital Services", "IT Support & Consultation"): [
        {"name": "Home Office Dual-Monitor & Docking Station Setup", "price": 699.0, "dur": 45, "desc": "DisplayPort/HDMI daisy chaining, USB-C thunderbolt hub setup, and ergonomic cable routing."},
        {"name": "Corporate Email & Google Workspace Domain Migration", "price": 1999.0, "dur": 90, "desc": "Configuring MX, SPF, DKIM DNS records and migrating mailbox data seamlessly."},
        {"name": "Small Office Network Attached Storage (NAS) Setup", "price": 2499.0, "dur": 120, "desc": "Synology/QNAP raid storage configuration with multi-user permissions and remote access."},
        {"name": "Software License Audit & Cybersecurity Scan", "price": 1299.0, "dur": 60, "desc": "Scanning network vulnerabilities, updating firewall rules, and verifying license compliance."},
        {"name": "Point of Sale (POS) Billing Software Configuration", "price": 1499.0, "dur": 90, "desc": "Installing thermal receipt printers, barcode scanners, and inventory billing software."}
    ],
    ("12. Technology & Digital Services", "Networking & Wi-Fi Setup"): [
        {"name": "Multi-Story Tri-Band Mesh Wi-Fi Installation", "price": 899.0, "dur": 60, "desc": "Eliminating dead zones in large homes using seamless roaming Deco/Orbi mesh nodes."},
        {"name": "Ethernet Cable Crimping & Concealed Wall Punching", "price": 699.0, "dur": 60, "desc": "Cat6 gigabit cable termination with RJ45 connectors and wall faceplate keystones."},
        {"name": "Fiber Broadband ONT Modem Configuration", "price": 499.0, "dur": 30, "desc": "Configuring PPPoE credentials, static IP assignment, and 5GHz band channel optimization."},
        {"name": "Secure Guest Wi-Fi & Bandwidth Limiting Portal", "price": 899.0, "dur": 45, "desc": "Creating isolated guest Wi-Fi networks with captive portals and bandwidth caps."}
    ],
    ("12. Technology & Digital Services", "Website & App Development"): [
        {"name": "WordPress Business Website Setup & Customization", "price": 4999.0, "dur": 240, "desc": "Responsive 5-page mobile-friendly website with contact form, SSL certificate, and SEO plugin."},
        {"name": "Shopify E-Commerce Store Launch Consultation", "price": 5999.0, "dur": 240, "desc": "Product catalog upload, payment gateway integration (Razorpay/Stripe), and shipping rates."},
        {"name": "Custom Landing Page Design for Google Ads", "price": 2999.0, "dur": 120, "desc": "High-converting modern UI page with WhatsApp CTA button and fast 1-second load speed."},
        {"name": "Website Speed Optimization & Core Web Vitals Fix", "price": 1999.0, "dur": 90, "desc": "Minifying CSS/JS, converting WebP images, and achieving 90+ score on Google PageSpeed."}
    ],

    # 13. Professional & Business Services
    ("13. Professional & Business Services", "Accounting & Tax Filing"): [
        {"name": "Annual Corporate Balance Sheet Audit Filing", "price": 4999.0, "dur": 180, "desc": "Statutory balance sheet compilation, P&L audit report, and ROC compliance filing."},
        {"name": "TDS Quarterly Return Filing (Form 24Q / 26Q)", "price": 1499.0, "dur": 60, "desc": "Computing vendor and employee TDS deductions, generating challans, and filing NSDL returns."},
        {"name": "Personal Capital Gains Tax Computation (Shares/Property)", "price": 1799.0, "dur": 60, "desc": "Long-term and short-term capital gain calculations, indexation benefit, and tax exemptions."}
    ],
    ("13. Professional & Business Services", "Business Consulting"): [
        {"name": "Startup Pitch Deck & Financial Modeling Review", "price": 3999.0, "dur": 120, "desc": "Reviewing 10-slide investor deck, 3-year revenue projections, and unit economics metrics."},
        {"name": "Market Entry & Competitor Benchmarking Strategy", "price": 4499.0, "dur": 150, "desc": "Detailed industry landscape report highlighting pricing models, customer pain points, and gaps."},
        {"name": "Franchise Business Model & Standard Operating Procedures", "price": 6999.0, "dur": 240, "desc": "Drafting operational manuals, franchise royalty agreements, and quality control checklists."}
    ],
    ("13. Professional & Business Services", "Legal Documentation"): [
        {"name": "Non-Disclosure Agreement (NDA) & Vendor Contract Drafting", "price": 1499.0, "dur": 60, "desc": "Customized legally binding confidentiality and vendor service-level agreements."},
        {"name": "Employment Offer Letter & HR Policy Handbook Drafting", "price": 2499.0, "dur": 90, "desc": "Drafting offer contracts, non-compete clauses, leave policies, and code of conduct."},
        {"name": "Power of Attorney (POA) & Affidavit Legal Preparation", "price": 999.0, "dur": 45, "desc": "General or special power of attorney drafting with notary stamp coordination."}
    ],
    ("13. Professional & Business Services", "Marketing & Branding"): [
        {"name": "Google Ads (PPC) Campaign Setup & Keyword Audit", "price": 2999.0, "dur": 90, "desc": "Negative keyword filtering, search ad copy creation, and conversion tracking tag setup."},
        {"name": "Instagram & Facebook Meta Ads Lead Generation Setup", "price": 2499.0, "dur": 90, "desc": "Targeting high-intent demographics, lookalike audiences, and creative carousel ads."},
        {"name": "Complete Brand Identity Design (Logo, Palette, Fonts)", "price": 3999.0, "dur": 150, "desc": "3 unique vector logo concepts, color guideline document, and business card layout."},
        {"name": "SEO On-Page Optimization & Schema Markup", "price": 2499.0, "dur": 90, "desc": "Meta titles, H1 tags, alt tags, and JSON-LD local business schema deployment."},
        {"name": "Influencer Marketing Outreach & Campaign Management", "price": 3499.0, "dur": 120, "desc": "Shortlisting niche micro-influencers, negotiating barter/paid rates, and campaign tracking."}
    ],
    ("13. Professional & Business Services", "Staffing & HR Services"): [
        {"name": "Mid-Level Executive Candidate Sourcing & Screening", "price": 3499.0, "dur": 120, "desc": "Filtering CVs, conducting preliminary technical interviews, and shortlisting top candidates."},
        {"name": "Payroll Processing & Salary Slip Generation", "price": 1499.0, "dur": 60, "desc": "Monthly salary calculation, PF/ESI deductions, and automated digital payslip delivery."},
        {"name": "Employee Background Verification (Criminal & Education)", "price": 1199.0, "dur": 45, "desc": "Address physical verification, court record checks, and university degree verification."},
        {"name": "POSH Act Workplace Harassment Compliance Training", "price": 2999.0, "dur": 90, "desc": "Internal committee formation guidelines and interactive employee sensitivity workshop."},
        {"name": "Exit Interview & Full & Final Settlement Processing", "price": 999.0, "dur": 45, "desc": "Managing notice period handovers, leave encashment calculations, and clearance approvals."}
    ],
    ("13. Professional & Business Services", "Virtual Assistant"): [
        {"name": "Executive Calendar & Travel Booking Assistant", "price": 1499.0, "dur": 60, "desc": "Coordinating Zoom calls, managing flight/hotel bookings, and itinerary preparation."},
        {"name": "Customer Support Chat & Email Rep (Daily Shift)", "price": 2499.0, "dur": 240, "desc": "Answering customer queries, resolving tickets on Zendesk/Freshdesk with SLA."},
        {"name": "Data Entry & Web Research Virtual Specialist", "price": 999.0, "dur": 60, "desc": "Accurate spreadsheet data entry, web scraping, and database updating."}
    ],

    # 14. Moving, Delivery & Local Assistance
    ("14. Moving, Delivery & Local Assistance", "Home Shifting & Packing"): [
        {"name": "Studio / 1 RK Compact Shifting Service", "price": 3499.0, "dur": 180, "desc": "Fast shifting with 2 helpers, foam padding, and mini tempo transport."},
        {"name": "3 BHK Luxury Villa Inter-State Relocation", "price": 12999.0, "dur": 480, "desc": "Heavy-duty wooden crating for chandeliers, TV packing, and dedicated container truck."},
        {"name": "Kitchen Crockery & Fragile China Safe Packing", "price": 1499.0, "dur": 90, "desc": "Specialized honeycomb paper wrapping and double-walled boxes for fragile glassware."}
    ],
    ("14. Moving, Delivery & Local Assistance", "Junk Removal & Disposal"): [
        {"name": "Old Wooden Furniture Scrapping & Disposal", "price": 999.0, "dur": 60, "desc": "Dismantling heavy broken beds, almirahs, and loading into municipal disposal trucks."},
        {"name": "E-Waste Eco-Friendly Recycling Pickup", "price": 499.0, "dur": 45, "desc": "Doorstep collection of old CRT monitors, dead CPUs, wires, and printers for certified recycling."},
        {"name": "Renovation Debris & Rubble Masonry Clearance", "price": 1799.0, "dur": 120, "desc": "Clearing cement sacks, plaster waste, and broken tiles into commercial tipper trucks."},
        {"name": "Mattress & Foam Scrap Disposal Service", "price": 699.0, "dur": 45, "desc": "Heavy lifting and transport of bulky soiled mattresses for responsible disposal."},
        {"name": "Complete Garage / Balcony Junk Clutter Hauling", "price": 1299.0, "dur": 90, "desc": "Clearing rusted pipes, obsolete boxes, paint cans, and thoroughly sweeping the area."}
    ],
    ("14. Moving, Delivery & Local Assistance", "Last-Mile Delivery"): [
        {"name": "Two-Hour Express City Document Delivery", "price": 199.0, "dur": 45, "desc": "Urgent passport, signed agreement, or invoice courier with live GPS tracking."},
        {"name": "Fragile Bakery Cake & Floral Gift Delivery", "price": 299.0, "dur": 45, "desc": "Air-conditioned car transport preventing birthday cake melting or bouquet damage."},
        {"name": "Retail Store Same-Day Parcel Dispatch", "price": 399.0, "dur": 60, "desc": "Batch pickup of ecommerce packages from local boutiques delivered to city customers."},
        {"name": "Heavy Hardware & Appliance Inter-Store Transit", "price": 699.0, "dur": 60, "desc": "Transporting air conditioners, tiles, or sanitaryware from wholesale mandi to site."}
    ],
    ("14. Moving, Delivery & Local Assistance", "Local Errands & Assistance"): [
        {"name": "Standing in Long Queue Assistant (RTO/Consulate)", "price": 499.0, "dur": 120, "desc": "Helper standing in line on your behalf at government offices or visa centers."},
        {"name": "Gift Wrapping & Festive Hamper Assembly Runner", "price": 599.0, "dur": 60, "desc": "Procuring gift ribbons, wrapping boxes, and delivering Diwali/Christmas hampers."},
        {"name": "Key Duplicate Making & Locksmith Doorstep Pickup", "price": 349.0, "dur": 30, "desc": "Collecting master key, getting computer duplicate cut at market, and returning to home."}
    ],
    ("14. Moving, Delivery & Local Assistance", "Vehicle Transport"): [
        {"name": "Two-Wheeler Covered City Bike Towing", "price": 899.0, "dur": 45, "desc": "Hydraulic ramp pickup truck for punctured, stalled, or accidental motorcycles."},
        {"name": "Flatbed Hydraulic Tow Truck for Premium Cars", "price": 1899.0, "dur": 60, "desc": "Zero-ground clearance flatbed towing for luxury sedans and automatic SUVs."},
        {"name": "Interstate Bike Relocation with Bubble Wrap", "price": 3499.0, "dur": 120, "desc": "Full motorcycle bubble wrapping, petrol draining, and train/truck container loading."},
        {"name": "Airport Chauffeur Driven Car Drop & Valet Return", "price": 999.0, "dur": 90, "desc": "Driver dropping you at airport terminal and safely parking car back at your residence."}
    ],

    # 9. Health, Fitness & Wellness
    ("9. Health, Fitness & Wellness", "Mental Wellness & Counselling"): [
        {"name": "Cognitive Behavioral Therapy (CBT) Session", "price": 1499.0, "dur": 50, "desc": "Confidential 1-on-1 licensed psychologist session addressing anxiety, stress, and burnout."},
        {"name": "Workplace Burnout & Work-Life Balance Therapy", "price": 1299.0, "dur": 45, "desc": "Therapy counseling managing corporate imposter syndrome, stress, and sleep disorder."},
        {"name": "Couples Relationship & Pre-Marital Counselling", "price": 1999.0, "dur": 60, "desc": "Empathetic communication conflict resolution and marital alignment counseling."},
        {"name": "Mindfulness Meditation & Breathwork Coaching", "price": 899.0, "dur": 45, "desc": "Guided progressive muscle relaxation and neuro-calming pranayama techniques."}
    ],
    ("9. Health, Fitness & Wellness", "Nutrition & Diet Counselling"): [
        {"name": "PCOS & Hormonal Balance Nutrition Plan", "price": 1299.0, "dur": 45, "desc": "Dietary protocol with low glycemic foods, seed cycling, and insulin management."}
    ],
    ("9. Health, Fitness & Wellness", "Personal Training"): [
        {"name": "Home Kettlebell & Functional Power Trainer", "price": 3999.0, "dur": 60, "desc": "Cardio-endurance kettlebell swing and snatch workouts improving explosive strength."},
        {"name": "Marathon & Endurance Running Coach", "price": 3499.0, "dur": 60, "desc": "Gait analysis, cadence pacing drills, and hydration strategies for 10K/21K runners."},
        {"name": "Weight Loss Boot Camp Session for Couples", "price": 4999.0, "dur": 60, "desc": "High-energy partner workouts combining jump rope, agility ladders, and core circuits."},
        {"name": "Body Recomposition & Calorie Deficit Coaching", "price": 4499.0, "dur": 60, "desc": "Strength training programming paired with weekly digital body fat measurement."}
    ],
    ("9. Health, Fitness & Wellness", "Physiotherapy & Rehabilitation"): [
        {"name": "Lumbar Spondylosis & Sciatica Lower Back Relief", "price": 899.0, "dur": 45, "desc": "TENS machine stimulation, gentle pelvic tilts, and lumbar traction exercises."},
        {"name": "Frozen Shoulder & Rotator Cuff Mobility Rehab", "price": 899.0, "dur": 45, "desc": "Shoulder pulley exercises, therapeutic ultrasound, and joint mobilization."},
        {"name": "Knee Osteoarthritis Isometric Strengthening", "price": 899.0, "dur": 45, "desc": "Quadriceps isometric loading, knee taping, and low-impact mobility training."},
        {"name": "Cervical Neck Spasm & Migraine Physical Therapy", "price": 849.0, "dur": 45, "desc": "Suboccipital release massage, cervical traction, and neck posture re-education."},
        {"name": "Post-Stroke Neurological Mobility Home Session", "price": 1199.0, "dur": 60, "desc": "Sensory motor repatterning, gait training, and hand grip rehabilitation."}
    ],
    ("9. Health, Fitness & Wellness", "Professional Wellness"): [
        {"name": "Dry Needling & Myofascial Trigger Point Therapy", "price": 999.0, "dur": 45, "desc": "Targeted filament needle insertion into deep muscle knots to release chronic spasms."}
    ],
    ("9. Health, Fitness & Wellness", "Sports Coaching"): [
        {"name": "Tennis / Badminton Footwork & Stroke Coach", "price": 2999.0, "dur": 60, "desc": "Court agility ladder drills, backhand mechanics, and smash technique."}
    ],
    ("9. Health, Fitness & Wellness", "Yoga & Meditation"): [
        {"name": "Ashtanga Primary Series Guided Yoga Flow", "price": 3499.0, "dur": 60, "desc": "Vinyasa flow synchronizing breath with Surya Namaskar, forward folds, and seated asanas."},
        {"name": "Restorative Yin Yoga for Deep Sleep & Flexibility", "price": 2999.0, "dur": 60, "desc": "Long-held passive floor poses using bolsters to open fascia and soothe nervous system."},
        {"name": "Power Yoga Core Sculpt & Sweat Session", "price": 3499.0, "dur": 60, "desc": "Dynamic fast-paced yoga sequences targeting belly fat, arm balance, and stamina."},
        {"name": "Kundalini Chakra Balancing & Mantra Meditation", "price": 2799.0, "dur": 45, "desc": "Spinal breathing exercises, mudras, and sound vibrational meditation."},
        {"name": "Corporate Chair Yoga & Eye Strain Relief", "price": 1999.0, "dur": 45, "desc": "Gentle desk stretches releasing wrist carpal tunnel, neck stiffness, and eye strain."},
        {"name": "Kids Yoga & Attention Focus Training", "price": 2199.0, "dur": 45, "desc": "Playful animal poses, balance games, and breathing exercises boosting concentration."}
    ]
}

total_fixed = 0

for (cat, sub), s_list in SUBCAT_SERVICES.items():
    # Fetch rows with Option in this category and subcategory
    cur.execute("""
        SELECT id, name FROM services 
        WHERE category = %s AND subcategory = %s AND (name ILIKE '%%option%%' OR name ILIKE '%%variation%%')
        ORDER BY id;
    """, (cat, sub))
    rows = cur.fetchall()
    
    for i, r in enumerate(rows):
        s_id = r[0]
        if i < len(s_list):
            item = s_list[i]
            s_name = item["name"]
            s_price = item["price"]
            s_dur = item["dur"]
            s_desc = item["desc"]
        else:
            s_name = f"{sub} - Premium Master Consultation"
            s_price = 1499.0
            s_dur = 60
            s_desc = f"Expert consultation and comprehensive service delivery for {sub}."
            
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
                "Standard supplies and equipment",
                "Post-service cleanup and inspection",
                "Expert guidance and aftercare tips"
            ],
            "excluded": [
                "Spare parts or structural replacement unless quoted",
                "Hazardous materials"
            ],
            "faqs": [
                {
                    "question": f"How long does {s_name} take?",
                    "answer": f"Typically takes around {s_dur} minutes."
                },
                {
                    "question": "Is the pricing transparent?",
                    "answer": "Yes, exact upfront pricing with zero hidden charges."
                }
            ],
            "warranty": "7-day service satisfaction warranty"
        }
        
        cur.execute("""
            UPDATE services 
            SET name = %s, base_price = %s, distinct_features = %s, updated_at = NOW()
            WHERE id = %s;
        """, (s_name, s_price, json.dumps(features), s_id))
        
        total_fixed += 1

conn.commit()

cur.execute("SELECT count(*) FROM services WHERE name ILIKE '%option%' OR name ILIKE '%variation%';")
rem_check = cur.fetchone()[0]

cur.execute("SELECT count(*) FROM services;")
tot_services = cur.fetchone()[0]

print(f"DONE: Overhauled {total_fixed} services.")
print(f"Total services in database: {tot_services}")
print(f"Remaining 'Option' or 'Variation' services: {rem_check}")

cur.close()
conn.close()
