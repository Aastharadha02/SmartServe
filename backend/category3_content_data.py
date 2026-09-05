"""
Category 3: Painting, Waterproofing & Home Improvement
Complete, authoritative content dataset for all 23 services across 4 subcategories.
Preserves existing DB data, real add-ons, and image mappings without database alteration.
"""

from home_improvement_data import HOME_IMPROVEMENT_SERVICES

HOME_PAINTING_SERVICES = [
    {
        "id": "a737ceca-8a81-4f4f-880a-0a73242239f4",
        "name": "1 BHK Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Home Painting",
        "price": 16249.0,
        "duration_minutes": 720,
        "description": "Full interior repaint for a 1 BHK apartment (1 bedroom, hall, kitchen, and bathroom ceiling/trims up to ~550 sq.ft. carpet area). Includes complete furniture masking, wall surface inspection, minor crack filling, 1 undercoat primer, and 2 finish coats of washable, low-VOC interior emulsion for a uniform, vibrant finish.",
        "highlights": [
            "Complete wall & ceiling coverage for standard 1 BHK layouts up to 550 sq.ft.",
            "Heavy-duty floor protection sheets and furniture plastic dust masking",
            "Double-coat acrylic putty application on uneven patches and nail holes",
            "Odorless, low-VOC, anti-fungal interior emulsion in your selected shades",
            "Post-paint site cleanup with edge de-masking and paint spot wiping"
        ],
        "included": [
            "Painting of all interior walls and ceilings in 1 bedroom, hall, and kitchen",
            "Floor masking with protective plastic and cardboard runners",
            "Furniture covering with drop cloths and lightweight plastic wrap",
            "Surface preparation including scraping loose flakes and sandpaper smoothing",
            "Filling minor hairline cracks and nail holes with acrylic wall putty",
            "1 coat of interior primer to seal porous wall surfaces",
            "2 full top coats of premium interior emulsion paint using rollers and trim brushes",
            "Final walkthrough, masking tape removal, and floor sweep"
        ],
        "excluded": [
            "Major structural plaster repair or re-plastering of hollow brickwork",
            "External balcony or facade exterior wall painting",
            "Door and window enamel painting (available as add-on)",
            "Deep civil seepage rectification or rising damp membrane installation",
            "Heavy furniture shifting requiring specialized movers"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Room Masking & Furniture Shielding",
                "description": "Floors, switch plates, skirting, and movable furniture are covered with protective plastic and masking tape.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Wall Assessment & Surface Prep",
                "description": "Loose peeling paint is scraped down; walls are sanded with 120-grit paper to remove grit and oil residues.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Patch Putty & Hairline Crack Filling",
                "description": "Acrylic wall putty is applied over nail holes, hairline fissures, and surface depressions, followed by drying.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "Fine Sanding & Primer Undercoat",
                "description": "Putty patches are smoothed with 220-grit sandpaper and a uniform coat of acrylic primer is rolled on.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Topcoat Application",
                "description": "First coat of washable emulsion is rolled on walls and cut neatly into corners using angled sash brushes.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Topcoat & Quality Inspection",
                "description": "After a 4-hour drying interval, the second coat is applied for seamless color depth, opacity, and sheen.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "De-masking & Final Site Cleanup",
                "description": "Masking tape and floor sheets are peeled away, paint splatters are cleaned, and furniture is repositioned.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Microfiber 9-inch paint rollers & roller extension poles",
            "Synthetic angled sash trim brushes (1.5-inch & 2.5-inch)",
            "120-grit and 220-grit silicon carbide sanding sheets",
            "Heavy-duty 50-micron polythene drop sheets & masking tape",
            "Putty blade knives and stainless steel hawk plates",
            "Low-VOC washable interior emulsion and acrylic wall primer"
        ],
        "customer_setup": [
            "Keep personal valuables, fragile curios, and electronic accessories safely stored in wardrobes or cupboards.",
            "Ensure continuous electrical supply for lighting and ceiling fan operation during application and drying.",
            "Provide access to clean running water for brush cleaning and surface preparation."
        ],
        "aftercare": [
            "Allow walls to cure undisturbed for at least 48 to 72 hours before hanging heavy wall frames or clocks.",
            "Maintain gentle room ventilation by keeping windows slightly ajar during the first 24 hours.",
            "Do not scrub or wash walls with damp cloths for at least 14 days until the acrylic film fully cures."
        ],
        "expected_results": [
            "Flawless, streak-free interior walls with uniform color depth and rich matte/sheen texture.",
            "Clean edge cut-ins around electrical fixtures, ceiling borders, and door jambs.",
            "Fresh, odorless indoor ambiance with low-VOC eco-certified paint finishes."
        ],
        "important_notes": [
            "Covers standard carpet area up to 550 sq.ft.; units with high ceilings (>10 ft) or extra utility balconies may require incremental quotes.",
            "Dark color transformations from existing deep shades may require a tinted base primer coat."
        ],
        "warranty": "1-year SmartServe service warranty covering paint flaking or bubbling not caused by internal water leakage.",
        "faqs": [
            {
                "question": "How long does it take to paint a 1 BHK apartment?",
                "answer": "A standard 1 BHK interior repaint typically takes 1.5 to 2 working days depending on wall condition and drying humidity."
            },
            {
                "question": "Are the paints smelly or hazardous for kids and pets?",
                "answer": "No. We exclusively use low-VOC, odorless, water-based acrylic emulsions that are completely safe for households with kids and pets."
            },
            {
                "question": "Do I need to move heavy furniture myself?",
                "answer": "Our team assists in moving standard furniture to the center of each room and securely covering it with protective plastic film."
            },
            {
                "question": "Are doors, windows, and grills covered in this package?",
                "answer": "This package covers interior walls and ceilings. Wood polish or enamel painting for doors, windows, and grills can be added as add-ons."
            },
            {
                "question": "What happens if there are damp patches on the walls?",
                "answer": "Our painters inspect moisture levels before painting. Active seepage must be treated with our Waterproofing service before paint application."
            }
        ],
        "dos": [
            "Do choose and finalize your color shade cards before the painting crew arrives on day one.",
            "Do ensure ceiling fans and ACs are turned off during sanding to minimize airborne dust drift.",
            "Do inspect all walls during the final walkthrough alongside the crew lead."
        ],
        "donts": [
            "Don't touch or lean against fresh walls within the first 6 hours of paint application.",
            "Don't turn on high-humidity steam appliances or indoor drying racks near newly painted walls.",
            "Don't apply pressure adhesives or stick-on hooks for at least 14 days."
        ],
        "tips": [
            "Opting for light pastel tones in a 1 BHK makes compact rooms look brighter and visually expansive."
        ],
        "service_features": [
            {"title": "Complete 1 BHK Coverage", "description": "All bedroom, living, kitchen, and passageway walls & ceilings"},
            {"title": "Dust-Shield Masking", "description": "Edge-to-edge floor plastic shielding and furniture shrink wrapping"},
            {"title": "Dual-Coat Roller Finish", "description": "Even, uniform opacity with washable premium acrylic emulsion"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "1 BHK Interior Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["1 BHK painting", "home painting 1 BHK", "apartment painting", "interior wall paint"],
            "seo_title": "1 BHK Home Painting Services | Professional Interior Painting",
            "seo_description": "Transform your 1 BHK apartment with professional dual-coat interior painting, dust masking, minor wall repairs, and low-VOC paints.",
            "highlights": ["Complete 1 BHK coverage", "Dust-shield masking", "Dual-coat roller finish"]
        }
    },
    {
        "id": "71c0c65e-263e-42bf-8fd1-c1da9031975b",
        "name": "2 BHK Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Home Painting",
        "price": 5159.0,
        "duration_minutes": 1080,
        "description": "Comprehensive interior painting service for standard 2 BHK homes (2 bedrooms, hall, dining, kitchen, and corridors up to ~850 sq.ft. carpet area). Professional crew handles furniture shifting, protective dust wrapping, hairline crack rectification, primer application, and two coats of smooth washable interior emulsion.",
        "highlights": [
            "Full interior painting for 2 BHK configurations up to 850 sq.ft. carpet area",
            "Complete floor protection with heavy-duty masking film and drop cloths",
            "Minor crack filling and two coats of spot putty smoothing on blemishes",
            "Low-VOC premium emulsion paint in custom selected shades",
            "Structured multi-day schedule minimizing domestic disruption"
        ],
        "included": [
            "Interior walls and ceilings across 2 bedrooms, living hall, dining area, and kitchen",
            "Shifting furniture to center of rooms and covering with dust-proof plastic",
            "Taping baseboards, switchboards, and door trims with professional painters tape",
            "Surface scraping of chalky or loose paint followed by abrasive sanding",
            "Filling hairline cracks and minor nail holes with acrylic joint compound",
            "1 coat of alkali-resistant interior primer on patched areas",
            "2 full topcoats of rich washable interior emulsion",
            "Complete post-completion cleaning, masking removal, and furniture realignment"
        ],
        "excluded": [
            "Exterior facade walls or external service balconies",
            "Wood polishing on doors, wardrobes, and furniture (available as add-on)",
            "Metal grill or gate enamel coating (available as add-on)",
            "Structural civil masonry repairs or deep damp seepage waterproofing",
            "Removal of heavy wall-mounted mirrors or large anchored TV units"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Site Masking & Surface Protection",
                "description": "Furniture is clustered away from walls and draped in protective sheeting; floors and switches are masked.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Surface Scraping & Defect Inspection",
                "description": "Walls are scraped with putty blades and inspected with bright work lights for hollows, dents, and cracks.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Putty Touch-ups & Hairline Crack Sealing",
                "description": "Two coats of fine acrylic putty are troweled over imperfections to produce a level substrate.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Fine Sanding & Primer Sealer",
                "description": "Cured putty is hand-sanded with 220-grit paper; high-adhesion primer is applied over all prepped areas.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Coat Emulsion Rolling",
                "description": "First topcoat is applied evenly using lint-free rollers, with precise brush cutting along ceilings and corners.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Finish Coat Application",
                "description": "After a minimum 4-hour cure, the second coat is laid down for rich color consistency and washability.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "De-masking, Detailing & Handover",
                "description": "Masking tape is carefully stripped, floors are swept and wiped, and the space is handed over after a final walkthrough.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "9-inch lint-free microfiber paint rollers with extension handles",
            "Angled 2-inch and 3-inch synthetic cutting brushes",
            "Abrasive sanding pads (150 and 220 grit)",
            "Polythene masking sheets and professional blue masking tape",
            "Acrylic wall putty and interior primer sealer",
            "Zero/low-VOC premium acrylic emulsion paints"
        ],
        "customer_setup": [
            "Pack away delicate decorative items, wall hangings, and loose paperwork into cupboards.",
            "Ensure electrical and water connections are active for work lighting and washing tools.",
            "Keep one room accessible for phasing work if the apartment remains occupied."
        ],
        "aftercare": [
            "Keep doors and windows partially open for 24-48 hours to facilitate airflow and uniform drying.",
            "Avoid wiping or touching painted surfaces for the first 3 days.",
            "Use only a soft, damp microfiber cloth without harsh abrasive cleaners if cleaning walls after 2 weeks."
        ],
        "expected_results": [
            "Seamless wall color uniformity with zero lap marks or roller streaks.",
            "Sharp, laser-clean separation lines between ceilings, walls, and trim woodwork.",
            "Durable, stain-resistant surface that withstands light everyday household cleaning."
        ],
        "important_notes": [
            "Base rate applies to homes up to 850 sq.ft. carpet area; larger duplex or extended floorplans quoted proportionately.",
            "Major dampness or salt efflorescence must be addressed before painting to ensure paint adhesion."
        ],
        "warranty": "1-year SmartServe warranty against paint peeling and bubbling under standard domestic conditions.",
        "faqs": [
            {
                "question": "Can we stay in the 2 BHK while painting is underway?",
                "answer": "Yes. Our team executes work in phases, typically completing one bedroom first so your family can comfortably occupy the remaining space."
            },
            {
                "question": "How many days will 2 BHK painting take?",
                "answer": "It generally takes 2 to 3 working days depending on wall repair requirements and prevailing humidity."
            },
            {
                "question": "Can we choose different colors for each room?",
                "answer": "Yes! You can choose distinct color shades for each bedroom, living hall, and kitchen at no additional charge."
            },
            {
                "question": "What brand of paint is used?",
                "answer": "We use leading tier-1 eco-friendly washable emulsions such as Asian Paints, Berger, or Dulux as per selected specifications."
            },
            {
                "question": "Do painters cover switchboards and lights?",
                "answer": "Yes, all switchplates, AC units, wall sconces, and ceiling fans are thoroughly masked with painter's tape and protective plastic."
            }
        ],
        "dos": [
            "Do decide accent wall shades and finishes ahead of the project start date.",
            "Do clear tabletops and open shelves of loose items prior to crew arrival.",
            "Do inspect the rooms in natural daylight before signing off the final handover."
        ],
        "donts": [
            "Don't lean heavy furniture against walls until the paint has cured for at least 72 hours.",
            "Don't use solvent or acid-based cleaners on fresh emulsion paint.",
            "Don't leave windows locked tight right after painting; gentle airflow prevents condensation."
        ],
        "tips": [
            "Warm off-white or soft beige in the living room creates a welcoming ambiance while vibrant pastels refresh bedrooms."
        ],
        "service_features": [
            {"title": "2 BHK Full Coverage", "description": "2 bedrooms, living hall, dining, kitchen, and passage walls & ceilings"},
            {"title": "Phased Execution", "description": "Room-by-room painting allowing family members to stay comfortably"},
            {"title": "Dust-Controlled Sanding", "description": "Clean surface preparation minimizing airborne dust drift"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "2 BHK Home Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["2 BHK painting", "home painting 2 BHK", "interior emulsion painting", "apartment wall painting"],
            "seo_title": "2 BHK Home Painting Services | Quality Interior House Painting",
            "seo_description": "Book hassle-free 2 BHK home painting. Complete surface preparation, furniture masking, low-VOC washable paint, and 1-year warranty.",
            "highlights": ["2 BHK full coverage", "Phased execution", "Dust-controlled sanding"]
        }
    },
    {
        "id": "26d2121b-eae7-49f5-b2e2-535b170cea5a",
        "name": "3 BHK Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Home Painting",
        "price": 12939.0,
        "duration_minutes": 1440,
        "description": "Complete interior repainting solution for spacious 3 BHK apartments and flats (3 bedrooms, large living hall, dining room, kitchen, and utility foyers up to ~1350 sq.ft. carpet area). Multi-painter crew ensures swift completion with full furniture masking, detailed wall repair, primer undercoating, and two rich coats of premium emulsion.",
        "highlights": [
            "Dedicated painting crew for 3 BHK homes up to 1350 sq.ft. carpet area",
            "Comprehensive protective covering of furniture, electronics, and tiled floors",
            "Precision surface leveling with double-coat putty and crack repair",
            "Premium washable low-VOC emulsion paints with high opacity and stain resistance",
            "Accent wall color pairing guidance and clean post-job cleanup"
        ],
        "included": [
            "All interior walls and ceilings across 3 bedrooms, hall, dining area, and kitchen",
            "Full room furniture shifting to center and complete shrink-wrap/tarp masking",
            "Floor protection using heavy gauge drop cloths across all work zones",
            "Scraping, wire brushing, and mechanical/hand sanding of wall surfaces",
            "Hairline crack filling and hole sealing with acrylic joint compound",
            "Application of primer undercoat over patched and repaired surfaces",
            "Two uniform topcoats of premium washable interior emulsion paint",
            "Complete de-masking, detailed trim cleaning, and debris removal"
        ],
        "excluded": [
            "Exterior balcony exterior walls or building facades",
            "Polishing of solid wooden doors, wardrobes, and modular cabinets (available as add-on)",
            "Balcony safety grill or window frame enamel painting (available as add-on)",
            "Civil re-plastering of damaged structural brickwork or water seepage repairs",
            "Dismantling heavy built-in gym or entertainment unit fixtures"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Comprehensive Masking & Floor Covering",
                "description": "All floors, switches, chandeliers, and centered furniture pieces are securely masked with film and tape.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Surface Scraping & Wall Leveling Inspection",
                "description": "Old peeling paint is scraped off; walls are checked with raking light for dents and micro-cracks.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Acrylic Putty & Crack Filling",
                "description": "Two coats of fine acrylic putty are applied to fill pinholes and hairline fractures, followed by drying.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Sanding & Primer Sealer Application",
                "description": "Walls are sanded smooth with 220-grit paper and wiped clean before rolling on an alkali-resistant primer.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Topcoat Application",
                "description": "First coat of washable emulsion is rolled on ceilings and walls with clean edge cut-in borders.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Finish Coat & Accent Wall Styling",
                "description": "Second coat is rolled on all rooms, ensuring full color saturation, even sheen, and zero patchy shadows.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "De-masking, Floor Wipe & Final Signoff",
                "description": "Tape is peeled off cleanly, paint spots are wiped down, furniture is reset, and a joint walkthrough is completed.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "High-density microfiber paint rollers and telescopic extension poles",
            "Angled sash cutting brushes (1.5-inch to 3-inch)",
            "Sanding blocks and 180/220-grit sanding paper sheets",
            "Heavy 60-micron polythene protective sheets and painter's blue tape",
            "Acrylic wall putty, crack filling compound, and interior primer",
            "Premium washable low-VOC interior emulsion paint"
        ],
        "customer_setup": [
            "Remove personal items, clothes, and precious curios from tabletop surfaces and bedside tables.",
            "Ensure steady electrical power and water supply throughout the project duration.",
            "Keep one room designated as a temporary family holding zone as work rotates through the home."
        ],
        "aftercare": [
            "Allow walls to cure undisturbed for 48 hours before repositioning heavy furniture tight against walls.",
            "Keep ceiling fans on low speed with windows slightly open for smooth, uniform curing.",
            "Avoid using wet scrubbers or cleaning chemicals on fresh paint for 14 days."
        ],
        "expected_results": [
            "Immaculate, velvety smooth wall finish with uniform sheen and vivid shade representation.",
            "Crisp geometric cutting along crown moldings, skirting, and door frames.",
            "Zero residual paint odor or messy splatters on your tiled or hardwood flooring."
        ],
        "important_notes": [
            "Standard scope covers carpet area up to 1350 sq.ft.; high-ceiling duplexes or larger villas are assessed on carpet area.",
            "Any pre-existing damp seepage must be treated with waterproofing before paint application."
        ],
        "warranty": "1-year SmartServe service warranty against paint peeling, flaking, or blistering.",
        "faqs": [
            {
                "question": "How long will 3 BHK painting take?",
                "answer": "With our multi-painter crew, a 3 BHK interior repainting typically takes 3 to 4 working days."
            },
            {
                "question": "Can we stay in the house during painting?",
                "answer": "Yes. We operate on a phased room-by-room schedule so you and your family always have quiet, functional rooms available."
            },
            {
                "question": "Can I pick different color themes for each of the 3 bedrooms?",
                "answer": "Absolutely! You can customize individual shades and sheen levels for each bedroom, living area, and dining space."
            },
            {
                "question": "Are doors, window sills, and balcony grills included?",
                "answer": "This service covers interior walls and ceilings. Wood polishing and metal enamel painting are convenient optional add-ons."
            },
            {
                "question": "Do you help choose color schemes?",
                "answer": "Yes, our supervisor carries physical shade cards and can advise on complementary palettes and accent wall pairings."
            }
        ],
        "dos": [
            "Do approve room color selections and accent wall placements prior to paint procurement.",
            "Do inspect wall surfaces during day hours with natural illumination.",
            "Do notify our crew of any hidden wiring or fragile wall-mounted items."
        ],
        "donts": [
            "Don't lean ladders or heavy furniture against freshly coated walls for 72 hours.",
            "Don't seal off rooms completely; mild ventilation is vital for paint film formation.",
            "Don't wash or scrub walls during the first 2 weeks after service completion."
        ],
        "tips": [
            "Feature accent walls in the master bedroom and living room create an elegant focal point without overwhelming the space."
        ],
        "service_features": [
            {"title": "Spacious 3 BHK Coverage", "description": "3 bedrooms, living hall, dining area, kitchen, and corridors"},
            {"title": "Multi-Painter Team", "description": "Organized crew delivering faster turnaround with minimal disruption"},
            {"title": "Premium Washable Emulsion", "description": "Stain-resistant, odorless, and durable interior paint finish"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "3 BHK Interior Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["3 BHK painting", "full home painting 3 BHK", "interior house painting", "apartment wall painters"],
            "seo_title": "3 BHK Full Home Painting Services | Expert Interior Painters",
            "seo_description": "Upgrade your 3 BHK home with professional interior painting. Complete dust protection, patch putty, low-VOC emulsion, and 1-year warranty.",
            "highlights": ["Spacious 3 BHK coverage", "Multi-painter team", "Premium washable emulsion"]
        }
    },
    {
        "id": "3604ea54-6170-4f40-86cc-3de4e6c5d84e",
        "name": "4 BHK+ Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Home Painting",
        "price": 21509.0,
        "duration_minutes": 1800,
        "description": "Executive interior painting service for large 4 BHK, 5 BHK, duplex, and penthouse residences (up to ~2200 sq.ft. carpet area). Managed by a dedicated project supervisor and master painter crew, this service offers end-to-end furniture shrink-wrapping, extensive plaster rectifications, dual-coat acrylic putty skimming, and luxury sheen emulsion application.",
        "highlights": [
            "Full interior coverage for luxury 4 BHK+ homes and duplexes up to 2200 sq.ft.",
            "Dedicated on-site painting supervisor overseeing daily quality benchmarks",
            "Advanced dust-containment masking for fine furniture, electronics, and artworks",
            "Double-coat putty smoothing and precision laser-aligned edge cut-ins",
            "High-scrub luxury interior emulsion in bespoke designer palettes"
        ],
        "included": [
            "Interior walls and ceilings across 4+ bedrooms, expansive hall, family lounge, dining, and kitchen",
            "Complete furniture shifting, shrink-wrapping, and heavy-duty floor corrugated roll protection",
            "Thorough surface degreasing, loose paint scraping, and orbital sander preparation",
            "Double-coat acrylic putty application for a level, mirror-smooth wall foundation",
            "Deep hairline crack and plaster fissure bridging with elastomeric compound",
            "1 coat of high-opacity interior primer sealer",
            "2 full topcoats of luxury interior emulsion with uniform sheen and color consistency",
            "Full site de-masking, floor vacuuming, furniture reset, and supervisor signoff"
        ],
        "excluded": [
            "External building facades or private terrace parapet painting",
            "Extensive wooden furniture and paneling PU polish (available as add-on)",
            "Metal balcony grill, railing, or gate enamel painting (available as add-on)",
            "Major civil structural re-plastering or external roof waterproofing",
            "Dismantling permanent architectural wall partitions or heavy gym equipment"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Comprehensive Site Masking & Floor Armoring",
                "description": "Corrugated cardboard and plastic sheets are taped across all floors; all furniture and fixtures are shrink-wrapped.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Surface Scraping & Laser Level Inspection",
                "description": "Old flaking paint is mechanically scraped; high-intensity inspection lamps reveal wall undulations.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Crack Sealing & Double-Coat Putty Skimming",
                "description": "Acrylic wall putty is troweled in two cross-coats over all walls to eliminate minor surface irregularities.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Orbital Sanding & Primer Sealer Application",
                "description": "Putty is smoothed using 220-grit sanding blocks, dusted, and coated with an alkali-resistant primer.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Luxury Emulsion Topcoat",
                "description": "First coat of luxury emulsion is applied with high-density rollers, cutting sharp edges around moldings.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Finish Coat & Accent Detailing",
                "description": "Second coat is rolled on with uniform pressure, ensuring rich color depth, soft luster, and zero roller overlap marks.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "Supervisor Audit, De-masking & Handover",
                "description": "Supervisor inspects walls with raking light; team strips masking, deep cleans floor borders, and resets furniture.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Pro-grade 9-inch microfiber rollers and lightweight carbon-fiber poles",
            "Precision synthetic filament trim brushes (1-inch, 2-inch, 3-inch)",
            "Heavy-duty corrugated floor protector rolls & 50-micron poly masking wrap",
            "Silicon carbide sanding discs, orbital sanding blocks, and tack cloths",
            "Acrylic joint putty, elastomeric crack sealant, and high-opacity primer",
            "Luxury washable low-VOC interior acrylic emulsion paint"
        ],
        "customer_setup": [
            "Store precious jewelry, delicate artwork, and small valuables in locked safes or cabinets.",
            "Ensure reliable three-phase power or adequate circuit capacity for work lighting and ventilation fans.",
            "Allow the on-site supervisor to review existing wall condition with you before work commences."
        ],
        "aftercare": [
            "Allow 72 hours for paint film polymerization before mounting heavy decorative fixtures or wall televisions.",
            "Ensure continuous gentle airflow throughout large rooms by keeping cross-ventilation windows ajar.",
            "Avoid washing or wiping walls with chemical detergents for at least 14 days."
        ],
        "expected_results": [
            "Pristine, luxury hotel-grade wall smoothness with flawless light diffusion.",
            "Crisp architectural lines along crown moldings, ceiling coffers, and door architraves.",
            "Long-lasting, washable wall protection resistant to daily fingerprints and scuff marks."
        ],
        "important_notes": [
            "Base package covers up to 2200 sq.ft. carpet area; larger penthouses and villas quoted proportionately based on measured area.",
            "Any dampness detected above 15% moisture content must receive specialized waterproofing prior to topcoat application."
        ],
        "warranty": "1-year SmartServe comprehensive warranty covering paint peeling, flaking, or premature color fading.",
        "faqs": [
            {
                "question": "How many days does a 4 BHK+ painting project take?",
                "answer": "A standard 4 BHK+ interior repaint generally takes 4 to 6 working days, managed efficiently by our multi-painter crew and supervisor."
            },
            {
                "question": "Can we live in our duplex/penthouse during the painting process?",
                "answer": "Yes. Our supervisor coordinates phased zone execution, completing private bedrooms first so daily family routines remain uninterrupted."
            },
            {
                "question": "Do you provide luxury finishes like velvet or silk sheens?",
                "answer": "Yes, we offer premium matte, silk, satin, and soft-sheen luxury emulsions tailored to your lighting and design aesthetic."
            },
            {
                "question": "Are doors, trims, and wooden paneling included in this price?",
                "answer": "This service covers all interior walls and ceilings. Wood melamine/PU polishing and metal grill painting are available as discounted add-ons."
            },
            {
                "question": "Who oversees the quality on-site?",
                "answer": "A dedicated SmartServe painting supervisor is stationed on-site to inspect surface preparation, ensure timeline adherence, and lead final audits."
            }
        ],
        "dos": [
            "Do walk through the home with the site supervisor on day one to mark accent walls and special finish areas.",
            "Do ensure air conditioning filters are cleaned after full project completion.",
            "Do inspect all completed rooms under both daylight and warm evening artificial lighting."
        ],
        "donts": [
            "Don't push heavy wardrobes or beds flush against fresh paint within the first 3 days.",
            "Don't allow domestic cleaning staff to wipe walls with wet rags during the first 2 weeks.",
            "Don't place adhesive stickers or mounting tape on freshly painted surfaces."
        ],
        "tips": [
            "Contrasting satin ceiling white with subtle warm grey or greige walls elevates the ceiling height in large luxury apartments."
        ],
        "service_features": [
            {"title": "Luxury 4 BHK+ Scale", "description": "Large-scale coverage up to 2200 sq.ft. with dedicated supervisor"},
            {"title": "Floor Armor Protection", "description": "Corrugated protective rolls preventing heavy foot-traffic scratches"},
            {"title": "High-Scrub Emulsion", "description": "Resilient, stain-resistant topcoat with rich color retention"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "4 BHK+ Luxury Home Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["4 BHK painting", "luxury home painting", "villa interior painting", "penthouse painters"],
            "seo_title": "4 BHK+ Luxury Home Painting Services | Premium Interior Painting",
            "seo_description": "Exclusive interior painting for large 4 BHK+ homes, villas, and penthouses. Dedicated supervisor, floor armor masking, and luxury emulsion finish.",
            "highlights": ["Luxury 4 BHK+ scale", "Floor armor protection", "High-scrub emulsion"]
        }
    },
    {
        "id": "656fdd6b-9d26-4f17-bfe8-886c33d588f4",
        "name": "Exterior Full Home Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Home Painting",
        "price": 13249.0,
        "duration_minutes": 2160,
        "description": "High-durability exterior weather-proof painting for independent bungalows, villas, and residential facades (up to ~1200 sq.ft. exterior surface area). Features high-pressure jet washing to strip algae and efflorescence, polymer crack filling, anti-fungal exterior primer, and two coats of weather-shield acrylic emulsion offering UV, rain, and fungal resistance.",
        "highlights": [
            "Complete exterior weather-shield coating for independent homes and villas",
            "High-pressure pressure washer jetting to eradicate moss, algae, and soot",
            "Heavy-duty acrylic crack filler applied to structural exterior surface fissures",
            "Anti-fungal, alkali-resistant exterior base primer for maximum adhesion",
            "Dual-coat elastomeric exterior emulsion with UV protection and rain resistance"
        ],
        "included": [
            "Exterior facade walls, parapet exterior faces, sunshades, and boundary pillars (up to 1200 sq.ft.)",
            "High-pressure water washing of all exterior masonry surfaces to remove grime and spores",
            "Wire brushing and scraping of peeling, flaking, or calcified old paint",
            "Filling exterior cracks up to 4mm with polymer-modified exterior crack filler",
            "1 coat of exterior penetrative primer formulated for weather-exposed substrates",
            "2 full topcoats of weather-guard exterior acrylic emulsion with anti-dirt pickup technology",
            "Masking of exterior windows, glass balustrades, and outdoor light fixtures",
            "Post-painting debris removal, scaffold dismantling, and garden/driveway cleanup"
        ],
        "excluded": [
            "Roof terrace horizontal slab waterproofing (available as a specialized service)",
            "External MS gates, safety grills, and boundary railings (available as add-ons)",
            "Deep civil replastering of crumbling external concrete beams or brick walls",
            "Rope access / cradle rigging for multi-story towers above 3 floors",
            "Exterior landscape illumination or drainage pipe replacement"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Site Setup & High-Pressure Jet Wash",
                "description": "Exterior surfaces are power-washed using 120-bar water jets to blast away algae, dirt, and loose coatings.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Scraping & Biocidal Anti-Algae Wash",
                "description": "Remaining flakes are scraped with wire brushes; an anti-fungal biocidal wash is applied to kill fungal roots.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Crack V-Grooving & Polymer Filling",
                "description": "External cracks are widened into a V-groove, cleaned, and packed with flexible acrylic exterior crack sealant.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Anti-Alkali Exterior Primer Application",
                "description": "A deep-penetrating exterior primer is applied to seal porous plaster and prevent efflorescence leaching.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Weather-Shield Topcoat",
                "description": "First coat of elastomeric exterior emulsion is rolled and brushed onto walls, pillars, and window reveals.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Finish Topcoat Application",
                "description": "After a 6-hour cure, the second heavy topcoat is applied for superior film thickness and UV reflectivity.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "De-masking & Ground Site Cleanup",
                "description": "Masking tape on window glass is peeled away, ladders/scaffolds are packed, and ground driveways are washed.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Commercial high-pressure water jet washer (120-140 bar)",
            "Heavy-duty exterior long-nap 9-inch rollers and telescopic aluminum poles",
            "Stiff stainless steel wire brushes and mechanical scrapers",
            "Heavy-gauge drop sheets and outdoor masking film for windows",
            "Polymer-modified exterior crack filler and exterior penetrative primer",
            "Elastomeric 100% acrylic exterior emulsion with anti-fungal protection"
        ],
        "customer_setup": [
            "Ensure an outdoor water tap with sufficient continuous water flow for the pressure jet washer.",
            "Keep all windows, external vents, and doors securely locked during pressure jet washing.",
            "Park vehicles away from exterior facade walls to avoid water spray and paint mist."
        ],
        "aftercare": [
            "Allow the exterior paint film to cure completely for 48 hours before washing surrounding driveways.",
            "Inspect exterior walls annually before monsoon to clean drainage spouts and avoid water pooling.",
            "Trim tree branches touching exterior walls to prevent abrasive scraping against the paint film."
        ],
        "expected_results": [
            "Resilient, weather-resistant facade shielding against heavy rain, intense sun, and fungal regrowth.",
            "Vibrant, fade-resistant exterior colors with excellent dirt-repellence and washability.",
            "Sealed exterior hairline fissures preventing water ingress into interior living spaces."
        ],
        "important_notes": [
            "Service schedule is weather-dependent; exterior painting cannot be carried out during active rain or high monsoon humidity.",
            "Covers up to 1200 sq.ft. of exterior wall area; taller structures or larger bungalows are measured on-site."
        ],
        "warranty": "3-year SmartServe exterior performance warranty against flaking, peeling, and biological fungal growth.",
        "faqs": [
            {
                "question": "Can exterior painting be done during the monsoon season?",
                "answer": "No. Exterior surfaces must be completely dry for proper paint bonding. We schedule exterior painting during dry weather windows."
            },
            {
                "question": "How long will the exterior paint last?",
                "answer": "Our high-performance weather-shield exterior paint systems are formulated to last 5 to 7 years depending on local climatic exposure."
            },
            {
                "question": "Will pressure washing damage the plaster?",
                "answer": "No. Our technicians calibrate pressure nozzles specifically for residential masonry, removing only algae and loose paint without eroding sound plaster."
            },
            {
                "question": "Are boundary walls and exterior gates included?",
                "answer": "External boundary walls can be included within the measured square footage. Metal gate and grill enamel painting is available as an add-on."
            },
            {
                "question": "Do you arrange scaffolding?",
                "answer": "Yes, standard mobile aluminum tower scaffolding and safety ladders for up to two-story residences are arranged by our team."
            }
        ],
        "dos": [
            "Do prune garden shrubs and foliage growing directly against exterior walls prior to start.",
            "Do close all window glass tightly on pressure-washing days.",
            "Do choose exterior paint shades with high UV reflectance for better thermal comfort inside the home."
        ],
        "donts": [
            "Don't spray water from garden hoses onto exterior walls within 72 hours of topcoat completion.",
            "Don't allow terrace drainage downspouts to discharge directly against freshly painted vertical walls.",
            "Don't drill into external walls without sealing the fixture with silicone sealant."
        ],
        "tips": [
            "Pairing a darker base color on the lowest 3 feet of the exterior wall prevents ground splash stains during heavy rain."
        ],
        "service_features": [
            {"title": "Weather-Shield Protection", "description": "100% acrylic elastomeric paint resisting intense sun, rain, and algae"},
            {"title": "Pressure Jet Washing", "description": "Deep bio-clean stripping stubborn black mold and calcified deposits"},
            {"title": "3-Year Exterior Warranty", "description": "Guaranteed protection against peeling, flaking, and fungal growth"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Exterior Full Home Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["exterior home painting", "weatherproof house painting", "exterior wall paint", "villa painting"],
            "seo_title": "Exterior Full Home Painting Services | Weather-Proof House Painting",
            "seo_description": "Protect your home with professional exterior painting. Pressure washing, crack sealing, anti-fungal primer, and 3-year warranty.",
            "highlights": ["Weather-shield protection", "Pressure jet washing", "3-year exterior warranty"]
        }
    },
    {
        "id": "9a86bdbb-830a-42de-9a77-6933fdb6a4f6",
        "name": "Furnished Full Home Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Home Painting",
        "price": 12029.0,
        "duration_minutes": 1440,
        "description": "Specialized white-glove interior painting engineered for occupied, fully-furnished homes. Features meticulous multi-layer plastic and bubble wrapping for furniture, electronics, and curios, edge-to-edge floor protection, low-dust hand sanding, zero-VOC odorless paint, and phased room completion so your family lives comfortably throughout the project.",
        "highlights": [
            "White-glove service designed specifically for occupied, furnished residences",
            "Full plastic shrink-wrap and bubble-wrap protection for furniture and electronics",
            "Edge-to-edge floor protection with taped seams preventing paint seepage",
            "Low-dust sanding techniques keeping living areas clean and breathable",
            "100% odorless zero-VOC paints safe for kids, seniors, and indoor pets"
        ],
        "included": [
            "Full interior painting of walls and ceilings across all furnished rooms (up to 1100 sq.ft.)",
            "Careful relocation of furniture to room center with complete shrink-wrap protection",
            "Double-layer protective sheeting over sofas, dining tables, beds, and audio/video systems",
            "Full masking of switchboards, chandeliers, AC indoor units, and wall sconces",
            "Surface preparation, nail hole filling, and hairline crack sealing with acrylic putty",
            "Spot primer undercoating over repaired wall zones",
            "Two full coats of premium washable, odorless interior emulsion",
            "Daily interim cleanup, final de-masking, floor wiping, and furniture repositioning"
        ],
        "excluded": [
            "Packing and moving fine jewelry, personal papers, and wardrobe clothing",
            "Balcony safety grill and window metal enamel painting (available as add-on)",
            "Polishing of fitted wooden wardrobes and modular kitchen cabinets (available as add-on)",
            "Structural civil repairs or breaking tilework for plumbing fixes",
            "Deep cleaning of soft upholstery or mattress shampooing"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "White-Glove Furniture Masking & Shielding",
                "description": "Sofas, beds, cabinets, and electronics are moved inwards and wrapped in heavy plastic and bubble sheets.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Floor & Architectural Detailing Masking",
                "description": "Cardboard runners and floor film are taped wall-to-wall; switches, door hardware, and ACs are sealed.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Low-Dust Surface Scraping & Putty Prep",
                "description": "Loose paint is scraped with vacuum assist; nail holes and hairline cracks are filled with acrylic compound.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "Fine Sanding & Spot Priming",
                "description": "Putty patches are sanded smooth with fine 220-grit paper and wiped with tack cloths before spot-priming.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Topcoat Rolling & Precision Cutting",
                "description": "Odorless washable emulsion is rolled on walls and cut neatly around crown moldings and trims.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Finish Topcoat Application",
                "description": "After a 4-hour drying interval, the second coat is laid down for rich color uniformity and silky sheen.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "De-masking, Sanitized Cleanup & Furniture Reset",
                "description": "Masking plastic is removed, floors are swept and mopped, and all furniture is returned to original positions.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Static plastic masking rolls and multi-layer bubble wrap protection",
            "Blue painter's clean-release tape and floor boundary masking runners",
            "Low-splatter microfiber paint rollers and synthetic sash brushes",
            "Dustless sanding blocks and electrostatic micro-fiber tack cloths",
            "Zero-VOC, odorless, anti-bacterial washable interior emulsion",
            "Acrylic patch putty and high-adhesion spot primer"
        ],
        "customer_setup": [
            "Store precious jewelry, cash, laptops, and important documents safely inside locked cupboards.",
            "Remove fragile glassware, picture frames, and personal knick-knacks from open display shelves.",
            "Confirm daily room schedule with the supervisor so personal routines remain undisrupted."
        ],
        "aftercare": [
            "Keep ceiling fans running on medium speed for 24 hours to accelerate uniform acrylic curing.",
            "Avoid placing sofas or heavy headboards tight against fresh walls for at least 48 hours.",
            "Wipe any accidental spills with a dry or barely damp microfiber cloth; avoid chemical soaps for 2 weeks."
        ],
        "expected_results": [
            "Completely refreshed interior walls without a trace of paint splatter on your valuable furniture.",
            "Zero lingering paint odor, headaches, or airborne dust residue in living spaces.",
            "Impeccable cut-ins around delicate fixtures, built-in wardrobes, and architraves."
        ],
        "important_notes": [
            "Work is scheduled in phases (e.g. Master Bedroom completed first, followed by Living & Dining).",
            "Heavier items like piano units or stone dining tables are masked in-place without lifting."
        ],
        "warranty": "1-year SmartServe service warranty covering paint flaking or bubbling under normal living conditions.",
        "faqs": [
            {
                "question": "Can we live at home while the painters work?",
                "answer": "Yes, absolutely! The entire workflow is designed for occupied homes. We complete one section at a time so you always have private living space."
            },
            {
                "question": "Will my furniture and electronics get dusty or stained?",
                "answer": "No. We use heavy plastic wrap and bubble wrap sealed with painters tape. Nothing is exposed to paint splatters or sanding dust."
            },
            {
                "question": "Does the paint smell bad?",
                "answer": "Not at all. We exclusively use certified zero-VOC, odorless interior emulsions that let you sleep in the home comfortably the same night."
            },
            {
                "question": "Do your painters help move the furniture?",
                "answer": "Yes, our crew carefully moves all sofas, tables, chairs, and beds to room center and returns them upon completion."
            },
            {
                "question": "How long does a furnished full home repaint take?",
                "answer": "Depending on home size (typically 2 to 3 BHK), the phased furnished process takes 3 to 5 working days."
            }
        ],
        "dos": [
            "Do pack away fragile tabletop curios and cosmetics into drawers before start day.",
            "Do inspect masked furniture with the team lead before painting commences.",
            "Do open windows during daytime to let in fresh ambient air."
        ],
        "donts": [
            "Don't remove protective plastic wrapping yourself until the room painting is fully completed.",
            "Don't press damp clothing or towels against walls during the first 3 days.",
            "Don't scrub fresh paint with abrasive scouring pads."
        ],
        "tips": [
            "Zero-VOC paint is especially beneficial for bedrooms of young infants, elderly family members, or individuals with asthma."
        ],
        "service_features": [
            {"title": "White-Glove Masking", "description": "Comprehensive shrink-wrapping of furniture, televisions, and electronics"},
            {"title": "Zero-VOC & Odorless", "description": "Safe, non-toxic paints allowing family occupancy throughout the project"},
            {"title": "Phased Room Turnover", "description": "Step-by-step room completion keeping living disruption to a minimum"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Furnished Full Home Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["furnished home painting", "occupied house painting", "odorless paint service", "white glove painters"],
            "seo_title": "Furnished Full Home Painting Services | Zero-Hassle Painting",
            "seo_description": "Paint your occupied home without stress. Multi-layer furniture masking, dust containment, zero-VOC odorless paint, and phased execution.",
            "highlights": ["White-glove masking", "Zero-VOC & odorless", "Phased room turnover"]
        }
    },
    {
        "id": "20286e18-2436-443a-8215-0d65b1567160",
        "name": "Room Combinations",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Home Painting",
        "price": 3399.0,
        "duration_minutes": 480,
        "description": "Flexible bundled painting package for any two interconnected or independent rooms (e.g. Living + Dining, or Master Bedroom + Kids Bedroom up to ~350 sq.ft. carpet area combined). Perfect for mini-makeovers, this service includes furniture masking, wall surface repairs, primer undercoat, and dual-coat washable emulsion with custom color combinations.",
        "highlights": [
            "Custom 2-room painting package tailored to your makeover priorities",
            "Coverage up to 350 sq.ft. carpet area across any two selected rooms",
            "Includes complete furniture and floor masking with protective sheets",
            "Hairline crack sealing and two coats of acrylic spot putty",
            "Dual-coat washable interior emulsion with optional feature accent wall"
        ],
        "included": [
            "Interior walls and ceilings of any two chosen rooms (e.g. Hall + Dining, or 2 Bedrooms)",
            "Moving furniture to room center and covering with clean plastic drop cloths",
            "Floor edge masking with painter's tape along skirting boards",
            "Wall scraping of loose flakes and sanding with 180-grit paper",
            "Patch repair of nail holes and hairline cracks with acrylic putty",
            "Primer application on repaired patches to seal surface absorption",
            "Two topcoats of premium washable interior emulsion paint",
            "Full site de-masking, basic floor sweep, and furniture repositioning"
        ],
        "excluded": [
            "Painting additional rooms outside the selected 2-room bundle",
            "Doors, window frames, and metallic grill painting (available as add-ons)",
            "External balcony or facade wall painting",
            "Structural civil masonry replastering or deep seepage waterproofing",
            "Dismantling heavy fitted wall units or large fixed wardrobes"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Room Masking & Furniture Centering",
                "description": "Furniture in both selected rooms is shifted inwards and covered with protective plastic sheeting.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Surface Scraping & Defect Inspection",
                "description": "Old paint blisters are scraped away and walls are inspected for dents, holes, and crack lines.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Acrylic Putty & Crack Repair",
                "description": "Wall putty is troweled over imperfections and allowed to dry to create a flat, sound substrate.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Fine Sanding & Primer Undercoat",
                "description": "Putty patches are sanded smooth with 220-grit paper and coated with high-bonding primer.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Topcoat Application",
                "description": "First coat of washable emulsion is rolled on walls and ceilings with sharp brush cut-ins.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Finish Coat & Accent Shading",
                "description": "Second coat is applied across all walls, ensuring smooth color depth, opacity, and satin finish.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "De-masking & Room Reset",
                "description": "Tape is peeled off, floors are wiped of stray paint specks, and furniture is reset.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Microfiber 9-inch paint rollers and telescopic extension poles",
            "Precision cutting sash brushes (1.5-inch and 2.5-inch)",
            "180-grit and 220-grit silicon carbide sanding sheets",
            "Heavy-gauge drop sheets and clean-release painter's tape",
            "Acrylic joint putty and interior wall primer sealer",
            "Washable, low-VOC acrylic interior emulsion paint"
        ],
        "customer_setup": [
            "Clear personal items, clothing, and small decorations from both selected rooms.",
            "Ensure electrical supply for fans and work lights is active.",
            "Confirm color shades and accent wall choices before painters start rolling."
        ],
        "aftercare": [
            "Keep room windows partially open for 24 hours to allow smooth paint curing.",
            "Wait at least 48 hours before re-hanging wall art, mirrors, or heavy clocks.",
            "Do not wash or wipe walls with wet sponges for the first 14 days."
        ],
        "expected_results": [
            "Two beautifully refreshed rooms with seamless wall color and crisp edging.",
            "Covered minor surface flaws, nail holes, and scuff marks.",
            "Fresh, pleasant indoor environment with zero harsh chemical odors."
        ],
        "important_notes": [
            "Covers two rooms up to a combined carpet area of 350 sq.ft. (e.g. Master Bedroom + Living Room).",
            "If walls exhibit high dampness or salt efflorescence, waterproofing is recommended prior to painting."
        ],
        "warranty": "1-year SmartServe service warranty against paint flaking and peeling under normal conditions.",
        "faqs": [
            {
                "question": "Can I pick any two rooms in my home for this package?",
                "answer": "Yes! You can combine any two rooms, such as Living + Dining, Master Bedroom + Kids Room, or Guest Bedroom + Study."
            },
            {
                "question": "Can each room have a different color?",
                "answer": "Yes, you can choose completely different color shades for each of the two rooms without any extra fee."
            },
            {
                "question": "How long does it take to paint two rooms?",
                "answer": "Painting two standard rooms typically takes 1 to 1.5 working days."
            },
            {
                "question": "Are doors and windows included?",
                "answer": "Doors, windows, and metal grills can be added as add-on services during booking."
            },
            {
                "question": "Do painters cover my bed and wardrobe?",
                "answer": "Yes, all furniture, beds, and wardrobes are shifted inwards and securely covered with plastic drop sheets."
            }
        ],
        "dos": [
            "Do choose complementary shades that harmonize between connecting living and dining areas.",
            "Do keep pets in an alternate room while painting is underway.",
            "Do inspect corners and ceiling edges during final handover."
        ],
        "donts": [
            "Don't touch walls within the first 4 hours of paint application.",
            "Don't lean heavy furniture against freshly painted surfaces for 48 hours.",
            "Don't use abrasive scrubbing pads on newly applied emulsion."
        ],
        "tips": [
            "Using a slightly deeper accent shade on the TV feature wall in the living room adds dimension and visual depth."
        ],
        "service_features": [
            {"title": "Custom 2-Room Package", "description": "Choose any 2 rooms up to 350 sq.ft. combined carpet area"},
            {"title": "Furniture & Floor Masking", "description": "Complete protection against paint splatters and dust"},
            {"title": "Dual-Coat Roller Finish", "description": "Even, uniform opacity with washable low-VOC emulsion"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Room Combinations Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["2 room painting", "room combinations painting", "bedroom and living room paint", "room makeover paint"],
            "seo_title": "2 Room Combinations Painting Service | Flexible Home Painting",
            "seo_description": "Refresh any 2 rooms in your home with professional interior painting. Complete masking, patch repair, dual-coat emulsion, and 1-year warranty.",
            "highlights": ["Custom 2-room package", "Furniture & floor masking", "Dual-coat roller finish"]
        }
    },
    {
        "id": "b1a4a36e-a516-4682-832e-2e7f7d8cba1f",
        "name": "Room Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Home Painting",
        "price": 2449.0,
        "duration_minutes": 360,
        "description": "Dedicated single-room interior painting service (up to ~180 sq.ft. carpet area). Ideal for bedroom refreshes, nursery makeovers, home office revamps, or dining room accents. Includes furniture centering, floor masking, surface sanding, nail hole putty repair, primer undercoat, and two full coats of smooth washable interior emulsion.",
        "highlights": [
            "Full interior painting for a single room up to 180 sq.ft. carpet area",
            "Includes ceiling, all 4 walls, and window/door perimeter trims",
            "Complete floor masking with drop cloths and furniture plastic wrapping",
            "Surface preparation with sandpaper smoothing and acrylic putty patch repairs",
            "Two finish coats of washable low-VOC interior emulsion in your chosen shade"
        ],
        "included": [
            "Interior walls and ceiling of one dedicated room (up to 180 sq.ft.)",
            "Moving furniture to room center and covering with plastic dust sheets",
            "Taping skirting, switchboards, and window trim with painters tape",
            "Scraping loose paint flakes and sanding wall surfaces with 180-grit paper",
            "Filling minor nail holes and hairline cracks with acrylic wall putty",
            "Spot primer application over filled and sanded patches",
            "Two full topcoats of rich washable interior emulsion",
            "De-masking, floor wiping, and furniture repositioning"
        ],
        "excluded": [
            "Painting adjoining hallways, passages, or other rooms",
            "Door and window wooden polish or enamel painting (available as add-ons)",
            "External balcony or facade wall painting",
            "Civil plaster repairs or treating deep active dampness",
            "Dismantling large wall-mounted shelving or heavy television brackets"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Room Masking & Protection",
                "description": "Bed, desk, and furniture are moved to center; floors and switchplates are masked with tape and drop sheets.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Wall Scraping & Defect Inspection",
                "description": "Loose flakes are scraped down; nail holes and plaster hairline cracks are identified for repair.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Putty Application & Smoothing",
                "description": "Acrylic wall putty is applied over nail holes and blemishes, then allowed to dry completely.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Sanding & Spot Primer",
                "description": "Putty patches are sanded flush with 220-grit paper and coated with an acrylic primer.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Topcoat Application",
                "description": "First coat of washable emulsion is rolled on walls and ceiling with neat angled edge brushwork.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Finish Coat Application",
                "description": "After a 3 to 4-hour drying gap, the second coat is applied for rich color saturation and uniform sheen.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "De-masking & Cleanup",
                "description": "Masking tape and floor drop sheets are removed, stray paint spots are wiped, and furniture is reset.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "9-inch lint-free microfiber paint rollers and extension handles",
            "Angled 2-inch synthetic cutting brushes for trims and corners",
            "180-grit and 220-grit silicon carbide sanding sheets",
            "Plastic drop sheets and clean-peel painter's masking tape",
            "Acrylic joint putty and interior wall primer sealer",
            "Washable, low-VOC acrylic interior emulsion paint"
        ],
        "customer_setup": [
            "Clear small personal items, laptop, and cosmetics from desks and bedside tables.",
            "Ensure electrical supply is available for fan operation during drying.",
            "Keep the room door closed to the rest of the house during sanding to prevent dust drift."
        ],
        "aftercare": [
            "Keep ceiling fan on low speed for 12-24 hours to help paint cure evenly.",
            "Wait at least 48 hours before hanging picture frames or wall clocks.",
            "Avoid wiping or cleaning walls with wet sponges for the first 14 days."
        ],
        "expected_results": [
            "Fresh, uniform wall finish with vibrant color reproduction and zero lap marks.",
            "Covered nail holes, scuffs, and hairline cracks.",
            "Clean, odorless room ready for use within 24 hours."
        ],
        "important_notes": [
            "Covers a single room up to 180 sq.ft. carpet area (e.g. 12x15 ft bedroom or study).",
            "Dark to light dramatic color shifts may require a full base primer coat."
        ],
        "warranty": "1-year SmartServe warranty covering paint flaking or bubbling under normal domestic use.",
        "faqs": [
            {
                "question": "Can single room painting be completed in one day?",
                "answer": "Yes! A single room painting project is typically completed in 6 to 8 hours on the same day."
            },
            {
                "question": "Can I sleep in the room the same night?",
                "answer": "Yes, our low-VOC, odorless water-based paints dry quickly and emit no toxic fumes, making the room safe to sleep in by night."
            },
            {
                "question": "Can I choose an accent wall with a different color?",
                "answer": "Yes! You can choose one accent wall in a contrasting shade at no additional service cost."
            },
            {
                "question": "Do painters move the bed and wardrobe?",
                "answer": "Our crew moves beds and movable furniture to room center and covers them with plastic sheeting."
            },
            {
                "question": "Is the ceiling included in the room painting?",
                "answer": "Yes, the room ceiling is included and is typically painted in bright ceiling white or matched to your wall shade."
            }
        ],
        "dos": [
            "Do remove personal valuables and electronics from open shelves before crew arrival.",
            "Do verify the color shade swatch on a small wall patch before full rolling.",
            "Do keep ceiling fans running on medium speed after painting to assist drying."
        ],
        "donts": [
            "Don't lean against freshly painted walls for at least 6 hours.",
            "Don't press heavy furniture against walls for 48 hours.",
            "Don't use abrasive cleaners on the new paint film."
        ],
        "tips": [
            "A light pastel shade with an eggshell or satin finish makes small bedrooms look noticeably larger and brighter."
        ],
        "service_features": [
            {"title": "Single Room Focus", "description": "Complete walls and ceiling painting up to 180 sq.ft. in 1 day"},
            {"title": "Dust-Controlled Prep", "description": "Centering furniture and protecting floors with drop cloths"},
            {"title": "Odorless Quick-Dry", "description": "Low-VOC washable emulsion safe for immediate same-night use"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Single Room Interior Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["room painting", "single room painting", "bedroom painting", "interior wall paint"],
            "seo_title": "Single Room Painting Service | 1-Day Bedroom & Study Painting",
            "seo_description": "Refresh any single room in 1 day with professional painting. Furniture masking, nail hole repair, dual-coat emulsion, and 1-year warranty.",
            "highlights": ["Single room focus", "Dust-controlled prep", "Odorless quick-dry"]
        }
    },
    {
        "id": "cb2af0c1-c185-44c1-8e21-ee6f185fbe13",
        "name": "Unfurnished Full Home Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Home Painting",
        "price": 5989.0,
        "duration_minutes": 960,
        "description": "Rapid, high-efficiency full interior painting package tailored for vacant, unfurnished apartments before move-in or after tenant handover (up to ~900 sq.ft. carpet area). With zero furniture obstruction, our crew works swiftly through all bedrooms, hall, kitchen, and ceilings, delivering full wall sanding, nail hole filling, primer coat, and two coats of smooth washable emulsion.",
        "highlights": [
            "Fast-turnaround full interior painting for empty apartments up to 900 sq.ft.",
            "Complete wall & ceiling coverage across all bedrooms, living hall, and kitchen",
            "Total surface scraping, nail hole filling, and sandpaper smoothing",
            "Odorless, premium low-VOC emulsion paint in your selected shade palette",
            "Ideal for new homeowners moving in or landlords preparing for new tenants"
        ],
        "included": [
            "All interior walls and ceilings across bedrooms, living area, kitchen, and passages",
            "Floor masking along skirting and covering switchboards with painter's tape",
            "Comprehensive wall scraping of old flaking paint, cobwebs, and grease marks",
            "Filling transit scratches, picture hook nail holes, and minor cracks with acrylic putty",
            "1 uniform coat of interior primer across patched and repaired wall sections",
            "2 full topcoats of premium washable interior emulsion with roller finish",
            "Post-painting cleanup, floor sweep, masking removal, and site handover"
        ],
        "excluded": [
            "External building facade or exterior balcony wall painting",
            "Wood polishing on doors, window frames, and cabinets (available as add-ons)",
            "Metal safety grill and gate enamel painting (available as add-ons)",
            "Civil re-plastering of damaged masonry or deep moisture waterproofing",
            "Handling or shifting existing tenant furniture (applicable under Furnished package)"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Site Inspection & Skirting Masking",
                "description": "Apartment floors and electrical switches are masked with tape; walls are inspected under bright work lights.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Rapid Surface Scraping & Degreasing",
                "description": "Old peeling paint, stubborn stickers, and transit marks are scraped down; walls are sanded with 150-grit paper.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Nail Hole & Fissure Putty Filling",
                "description": "Acrylic wall putty is troweled over nail holes, anchor holes, and hairline plaster cracks.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Sanding & Primer Application",
                "description": "Putty patches are sanded flush with 220-grit paper and coated with an alkali-resistant primer.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Topcoat Roller Application",
                "description": "First coat of washable emulsion is rolled swiftly across open walls and ceiling bays with clean edge cutting.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Finish Coat Application",
                "description": "After a 3 to 4-hour drying interval, the second coat is laid down for rich color consistency and sheen.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "De-masking & Final Sweep",
                "description": "Masking tape is stripped, floor edges are wiped clean of splatters, and keys are handed over.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "High-speed 9-inch microfiber paint rollers with telescopic poles",
            "Synthetic trim brushes for crisp edge work (2-inch and 3-inch)",
            "Sanding blocks and 150/220-grit silicon carbide sanding sheets",
            "Professional painter's tape and plastic skirting protective runners",
            "Acrylic joint putty and interior wall primer sealer",
            "Premium low-VOC odorless emulsion paint applied"
        ],
        "customer_setup": [
            "Ensure the apartment is completely vacant and free of furniture, boxes, or debris.",
            "Ensure active electricity and water supply for work lighting and roller washing.",
            "Provide apartment access keys to the painting supervisor at the agreed start time."
        ],
        "aftercare": [
            "Keep apartment windows slightly open to allow natural cross-ventilation and uniform drying.",
            "Wait at least 48 to 72 hours before moving in heavy furniture or appliances.",
            "Do not wash or scrub newly painted walls with wet cloths for at least 14 days."
        ],
        "expected_results": [
            "Spotless, freshly painted interior walls ready for immediate tenant or owner move-in.",
            "Complete elimination of old nail holes, scuffs, and discolored patch marks.",
            "Bright, clean ambiance throughout all rooms with zero residual chemical paint odors."
        ],
        "important_notes": [
            "Premium low-VOC odorless emulsion paint applied.",
            "Standard package covers up to 900 sq.ft. carpet area; larger multi-story duplexes measured on-site."
        ],
        "warranty": "Standard 30-day SmartServe Guarantee",
        "faqs": [
            {
                "question": "How fast can an unfurnished home be painted?",
                "answer": "Since there is no furniture to move or mask, a standard 2 BHK unfurnished apartment can be completed in just 1.5 to 2 days."
            },
            {
                "question": "Can I get this done between tenant move-out and move-in?",
                "answer": "Yes! This service is specifically designed for quick tenant turnover with fast surface prep and odorless quick-drying paint."
            },
            {
                "question": "Are ceilings included in the unfurnished painting package?",
                "answer": "Yes, all room ceilings, living area ceilings, and kitchen ceilings are included."
            },
            {
                "question": "Can we choose different colors for each room?",
                "answer": "Yes, you can customize color shades for each room or choose a uniform neutral rental palette."
            },
            {
                "question": "What if there are minor seepage spots?",
                "answer": "Our supervisor inspects walls on arrival. Minor dampness can be treated, but active plumbing leaks require waterproofing prior to paint."
            }
        ],
        "dos": [
            "Do ensure the apartment is completely empty before the scheduled start date.",
            "Do hand over shade card selections and keys on morning one for fast turnaround.",
            "Do inspect the empty rooms in daylight during final handover."
        ],
        "donts": [
            "Don't schedule movers to deliver furniture on the same day painting finishes.",
            "Don't keep doors and windows locked tight; gentle airflow speeds up acrylic curing.",
            "Don't drill wall anchors into fresh paint within the first 48 hours."
        ],
        "tips": [
            "Regression verification tip for Unfurnished Full Home Painting",
            "Using a neutral warm white or light ivory across an unfurnished rental home appeals to prospective tenants and maximizes natural light."
        ],
        "service_features": [
            {"title": "Rapid Empty-Home Turnaround", "description": "Unobstructed painting completed in 1.5 to 2 days"},
            {"title": "All-Room Coverage", "description": "Walls and ceilings across all bedrooms, living room, and kitchen"},
            {"title": "Move-In Ready", "description": "Clean, odorless washable emulsion ready for immediate occupancy"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Unfurnished Full Home Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["unfurnished home painting", "empty apartment painting", "tenant turnover painting", "rental home painting"],
            "seo_title": "Unfurnished Full Home Painting Services | Fast Apartment Painting",
            "seo_description": "Rapid interior painting for empty apartments before move-in. Complete wall & ceiling coverage, nail hole repair, and low-VOC odorless paint.",
            "highlights": ["Rapid empty-home turnaround", "All-room coverage", "Move-in ready"]
        }
    }
]

SPECIALIZED_PAINTING_SERVICES = [
    {
        "id": "1d8ea162-8e72-4920-8eae-7dee95f031be",
        "name": "Ceiling Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Specialized Painting",
        "price": 3579.0,
        "duration_minutes": 360,
        "description": "Specialized overhead ceiling restoration and painting for living rooms, bedrooms, or hallways (up to ~300 sq.ft. ceiling area). Features heavy floor and chandelier masking, scraping of soot, cobwebs, and flaking paint, stain-blocking primer over moisture/fan discoloration, and two coats of ultra-flat non-reflective ceiling white paint engineered to resist roller spatter and conceal ceiling imperfections.",
        "highlights": [
            "Dedicated overhead ceiling painting for areas up to 300 sq.ft.",
            "Ultra-flat non-reflective ceiling white finish concealing plaster waves",
            "Stain-blocking primer sealing soot, ceiling fan grease, and smoke stains",
            "Complete floor, wall, and lighting chandelier protection with drop cloths",
            "Anti-spatter high-opacity emulsion minimizing messy roller drips"
        ],
        "included": [
            "Complete painting of ceilings in selected rooms (up to 300 sq.ft. area)",
            "Covering all floors, furniture, and lower wall perimeters with drop sheets",
            "Masking ceiling fans, hanging lights, recessed spotlights, and AC vents",
            "Scraping flaking paint, soot build-up, and ceiling hairline cracks",
            "Patching cracks and joints with lightweight non-shrinking acrylic spackle",
            "1 coat of stain-blocking undercoat primer on stained or repaired zones",
            "2 full topcoats of non-reflective flat ceiling white emulsion",
            "Clean de-masking, floor sweeping, and chandelier dust wipe"
        ],
        "excluded": [
            "Painting vertical wall surfaces (available as separate wall painting service)",
            "Ceiling fan or chandelier electrical rewiring or mechanical repair",
            "Treating active terrace/roof water leakage dripping through concrete slab",
            "Replacement of damaged gypsum board or POP false ceiling frameworks",
            "External balcony ceiling soffit painting exposed to heavy rain"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Floor & Light Fixture Masking",
                "description": "Floors are draped in heavy drop cloths; chandeliers, ceiling fans, and spotlights are wrapped in plastic sheeting.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Ceiling Scraping & Cleaning",
                "description": "Soot, cobwebs, and loose flaking paint around fans and corners are scraped down and vacuumed.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Crack Filling & Joint Spackling",
                "description": "Hairline cracks and ceiling joint fissures are filled with non-shrinking acrylic spackle and leveled.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Fine Sanding & Stain-Block Primer",
                "description": "Repaired areas are sanded smooth overhead and sealed with a stain-blocking primer to lock in grease and smoke stains.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Topcoat Application",
                "description": "First coat of ultra-flat ceiling white is rolled in one direction with crisp perimeter brush cutting.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Cross-Coat Application",
                "description": "Second coat is rolled perpendicular to the first coat to guarantee zero roller lap marks and total light diffusion.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "De-masking & Lighting Inspection",
                "description": "Protective plastic is removed from light fixtures, floors are cleaned, and ceiling is inspected under room lights.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Low-spatter 9-inch microfiber rollers and sturdy telescopic extension poles",
            "Angled sash trim cutting brushes (2-inch & 2.5-inch)",
            "Overhead sanding pads with 180/220-grit abrasive sheets",
            "Heavy-duty floor drop sheets and fixture masking bags",
            "Non-shrinking acrylic spackling paste and stain-blocking undercoat primer",
            "Ultra-flat, high-opacity non-reflective ceiling white emulsion paint"
        ],
        "customer_setup": [
            "Turn off ceiling fans and recessed spotlight circuits before technicians arrive.",
            "Remove small fragile decor and glassware from tables directly under ceiling work areas.",
            "Ensure a clear working path beneath the ceiling for ladder positioning."
        ],
        "aftercare": [
            "Leave ceiling fans turned off for at least 6 hours after painting to allow the paint film to set evenly.",
            "Keep room windows open for gentle cross-ventilation during drying.",
            "Do not wipe ceiling surfaces with wet cloths; use only a dry feather duster for future maintenance."
        ],
        "expected_results": [
            "Bright, uniformly white overhead ceiling that maximizes natural room illumination.",
            "Zero visible lap marks, roller stipple shadows, or residual fan soot rings.",
            "Crisp, clean separation lines where ceilings meet wall crowns and cornices."
        ],
        "important_notes": [
            "Covers standard ceiling height up to 10.5 feet; double-height ceilings or vaulted areas require special staging scaffolding.",
            "If brown water rings are caused by active rooftop plumbing leakage, waterproofing must precede ceiling repainting."
        ],
        "warranty": "1-year SmartServe warranty against paint peeling or flaking not caused by active water seepage.",
        "faqs": [
            {
                "question": "Why use specialized ceiling paint instead of regular wall paint?",
                "answer": "Ceiling paint is formulated with an ultra-flat matte sheen that diffuses overhead light without glare, concealing plaster waves and roller marks."
            },
            {
                "question": "How do you protect my ceiling fan and lights?",
                "answer": "We completely wrap all ceiling fans, chandeliers, pendant lamps, and recessed spotlights with protective plastic before opening paint cans."
            },
            {
                "question": "Will paint drip onto my furniture and flooring?",
                "answer": "No. We cover all floors and furniture with thick drop cloths, and our anti-spatter rollers prevent dripping during overhead rolling."
            },
            {
                "question": "How long does ceiling painting take?",
                "answer": "A standard room ceiling typically takes 4 to 6 hours including surface prep, two coats, and cleanup."
            },
            {
                "question": "Can you paint false ceilings with cove lights?",
                "answer": "Yes, our technicians carefully cut into false ceiling recesses and cove lighting channels using specialized angled trim brushes."
            }
        ],
        "dos": [
            "Do clean ceiling fan blades with a dry cloth the day before to prevent accumulated dust from falling.",
            "Do ensure light bulbs are cool and turned off before painter arrives.",
            "Do inspect the ceiling with full room lighting turned on before signing off."
        ],
        "donts": [
            "Don't turn on ceiling fans at high speed immediately after painting; the draft causes uneven drying patterns.",
            "Don't touch freshly painted ceiling cornices for at least 6 hours.",
            "Don't use wet sponges to clean flat ceiling paint in the future."
        ],
        "tips": [
            "Painting the ceiling pure flat white makes the entire room feel taller, more spacious, and noticeably brighter."
        ],
        "service_features": [
            {"title": "Ultra-Flat Non-Reflective White", "description": "Eliminates overhead light glare and hides subtle plaster imperfections"},
            {"title": "Anti-Spatter Overhead Rolling", "description": "Specially formulated paint avoiding messy roller drips on floors"},
            {"title": "Complete Fixture Protection", "description": "Full shrink-wrapping of fans, spotlights, chandeliers, and cornices"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Ceiling Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["ceiling painting", "false ceiling paint", "overhead painting", "flat white ceiling paint"],
            "seo_title": "Ceiling Painting Services | Professional Overhead Painting",
            "seo_description": "Restore your overhead ceilings with non-reflective flat white paint. Complete fixture masking, stain blocking, anti-spatter rolling, and 1-year warranty.",
            "highlights": ["Ultra-flat non-reflective white", "Anti-spatter overhead rolling", "Complete fixture protection"]
        }
    },
    {
        "id": "dc2848cb-fd07-434b-8569-58b8a3deda8e",
        "name": "Metal Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Specialized Painting",
        "price": 1559.0,
        "duration_minutes": 300,
        "description": "Protective anti-corrosion and decorative enamel painting for wrought iron, mild steel, and galvanized metal fixtures (up to ~80 sq.ft. surface area). Perfect for window safety grills, main entry gates, balcony railings, spiral staircases, and metal doors. Features intensive wire brushing to eliminate rust flakes, zinc chromate / red oxide anti-rust primer, and two coats of high-gloss or satin polyurethane enamel.",
        "highlights": [
            "Anti-rust protective coating for metal grills, gates, railings, and doors",
            "Intensive manual and mechanical wire brushing to eradicate loose rust",
            "Red oxide / zinc chromate corrosion-inhibiting primer undercoat",
            "Two finish coats of high-gloss or satin polyurethane synthetic enamel",
            "Superior weather resistance against monsoon humidity and oxidation"
        ],
        "included": [
            "Painting of metal grills, gates, railings, or frames up to 80 sq.ft. surface area",
            "Floor and wall masking around metal fixtures to prevent enamel overspray/drips",
            "Wire brushing and coarse emery cloth sanding to remove existing rust scale",
            "Solvent degreasing to remove oil, grease, and particulate matter",
            "1 full coat of anti-corrosion red oxide or zinc phosphate primer",
            "2 topcoats of premium polyurethane-reinforced synthetic enamel paint",
            "Masking tape removal, paint splatter scraping on surrounding glass, and cleanup"
        ],
        "excluded": [
            "Major structural welding or replacing rusted-through hollow metal pipes",
            "Powder coating requiring off-site industrial baking ovens",
            "Painting adjoining masonry walls or wooden window frames",
            "Sandblasting heavy industrial machinery or bridge structures",
            "Replacement of locks, hinges, or decorative brass hardware"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Surrounding Masking & Shielding",
                "description": "Floor tiles, adjoining wall plaster, and window glass panes are masked with tape and protective cardboard.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Rust Scraping & Emery Sanding",
                "description": "Wire brushes and 80-grit emery paper are used to scrape off loose rust scale, bubbling paint, and oxidation.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Solvent Wipe & Surface Degreasing",
                "description": "Metal bars are wiped down with mineral spirits to remove grease, fine rust dust, and oily residues.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "Anti-Rust Primer Application",
                "description": "A continuous coat of red oxide or zinc chromate anti-corrosion primer is brushed into all welds and joints.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "First Synthetic Enamel Coat",
                "description": "First coat of high-durability polyurethane enamel is applied evenly with fine bristle detail brushes.",
                "is_key_step": False
            },
            {
                "step_number": 6,
                "title": "Second Finish Enamel Coat",
                "description": "After an 8-hour drying interval, the second coat is laid down for rich color depth, gloss, and weather protection.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "Glass Cleaning & De-masking",
                "description": "Masking tape is stripped, glass razor blades clean any stray enamel specks, and work area is swept clean.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "High-tensile steel wire brushes and abrasive emery cloth rolls (80 and 150 grit)",
            "Natural hog-bristle enamel brushes (1-inch, 1.5-inch, 2-inch) and radiator mini-rollers",
            "Glass scraper razor blades and painter's blue masking tape",
            "Solvent degreaser / mineral turpentine for surface wipe down",
            "Red oxide / zinc chromate anti-rust primer undercoat",
            "High-gloss or satin polyurethane synthetic enamel paint"
        ],
        "customer_setup": [
            "Ensure safe access to window grills, gates, or balcony railings by removing curtains or potted plants.",
            "Keep pets and children away from the work area while solvent-based enamel is drying.",
            "Ensure window glass is clean to allow secure masking tape adhesion."
        ],
        "aftercare": [
            "Allow the enamel paint to dry completely undisturbed for at least 12 to 24 hours.",
            "Avoid opening or closing gates forcefully until the paint film has fully hardened.",
            "Wipe metal railings occasionally with a dry or lightly oiled cloth to preserve gloss."
        ],
        "expected_results": [
            "Sleek, glossy metal finish with total rust eradication and clean joint coverage.",
            "Heavy-duty protective shield preventing future oxidation and moisture corrosion.",
            "Zero enamel runs, drips, or brush marks on surrounding walls or window glass."
        ],
        "important_notes": [
            "Enamel paint requires longer drying times (6 to 8 hours per coat) compared to water-based wall paints.",
            "If structural metal has rusted completely through, welding repair must be done prior to painting."
        ],
        "warranty": "1-year SmartServe warranty against rust recurrence and enamel paint flaking on sound metal substrates.",
        "faqs": [
            {
                "question": "Can you paint rusted window safety grills?",
                "answer": "Yes! We scrape off all loose rust with wire brushes, wipe the metal clean, and apply an anti-rust primer before enamel painting."
            },
            {
                "question": "What finish options are available for metal gates and grills?",
                "answer": "We offer High-Gloss, Semi-Gloss, and Matte/Satin finishes in black, white, bronze, grey, and custom shade cards."
            },
            {
                "question": "Will the enamel smell inside the house?",
                "answer": "Enamel paint has a distinct solvent aroma during application. We keep windows well-ventilated; the odor dissipates within 24 hours."
            },
            {
                "question": "How do you prevent paint from getting on window glass?",
                "answer": "We tape all glass panes along the grill edges and use fine detail brushes, cleaning any accidental specks with a glass razor."
            },
            {
                "question": "How long will metal painting last outdoors?",
                "answer": "With anti-rust primer and dual enamel topcoats, our metal painting lasts 3 to 5 years even in humid outdoor balcony settings."
            }
        ],
        "dos": [
            "Do open balcony doors or windows to provide steady cross-ventilation during application.",
            "Do inspect metal welds and joints to ensure 100% primer coverage.",
            "Do wipe dust from painted grills with a soft microfiber duster once fully cured."
        ],
        "donts": [
            "Don't touch freshly painted grills or gates for at least 8 hours.",
            "Don't lean heavy cycles or ladders against painted railings until 48 hours have passed.",
            "Don't spray water or pressure wash painted metal during the first 7 days."
        ],
        "tips": [
            "Applying a high-gloss black or dark charcoal enamel to balcony grills provides superior UV resistance and looks pristine for years."
        ],
        "service_features": [
            {"title": "Anti-Rust Primer Shield", "description": "Zinc chromate / red oxide base stopping active oxidation and rust scale"},
            {"title": "Polyurethane Enamel", "description": "High-durability topcoat resisting monsoon rain and harsh sunlight"},
            {"title": "Clean Glass Edging", "description": "Precise tape masking protecting window glass and masonry borders"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Metal Grill and Gate Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["metal painting", "window grill painting", "iron gate paint", "anti rust paint", "balcony railing paint"],
            "seo_title": "Metal Painting Services | Anti-Rust Grill, Gate & Railing Painting",
            "seo_description": "Protect window grills, gates, and railings from rust with professional enamel painting. Wire brushing, anti-rust primer, and 1-year warranty.",
            "highlights": ["Anti-rust primer shield", "Polyurethane enamel", "Clean glass edging"]
        }
    },
    {
        "id": "608d5de2-0e84-410c-baa2-3b382d1f9c7c",
        "name": "Texture Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Specialized Painting",
        "price": 2309.0,
        "duration_minutes": 480,
        "description": "Bespoke decorative texture and accent wall design service (up to ~120 sq.ft. feature wall area). Master decorative artisans create stunning visual textures (such as Metallic, Stucco, Dune, Spatula, Rustic, or Royale Play patterns) using specialized trowels, patterned rollers, and combs. Includes surface skim putty, basecoat application, textured material modeling, and protective glaze topcoat.",
        "highlights": [
            "Designer accent wall texture application for areas up to 120 sq.ft.",
            "Wide portfolio of premium patterns: Metallic, Stucco, Spatula, Dune, and Rustic",
            "Skilled master decorative artisan with specialized texturing tools",
            "Multi-layer system: primer undercoat, texture modeling compound, and metallic glaze",
            "Washable, durable, and fade-resistant high-impact feature wall finish"
        ],
        "included": [
            "Complete texturing and styling of one feature/accent wall (up to 120 sq.ft.)",
            "Floor and adjacent wall masking with precision edge painter's tape",
            "Surface preparation, nail hole filling, and skim putty leveling",
            "1 coat of high-adhesion base primer/undercoat matched to texture tone",
            "Application of specialized acrylic texturing compound using trowels, sponges, or rollers",
            "Manual artisan pattern modeling to achieve chosen design pattern",
            "1 to 2 protective coats of tinted metallic, pearl, or matte topcoat glaze",
            "Full site cleanup, de-masking, and final design walkthrough"
        ],
        "excluded": [
            "Painting remaining plain walls in the room (available as Room Painting service)",
            "Civil demolition or major brick wall replastering",
            "Treating active dampness or wall water seepage (requires Waterproofing service)",
            "Exterior textured facade coatings requiring scaffolding",
            "Mounting decorative wall lighting or architectural wall moldings"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Perimeter Masking & Floor Shielding",
                "description": "Floors, adjacent perpendicular walls, and ceiling junctions are taped with precision sharp-edge masking tape.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Wall Leveling & Surface Sanding",
                "description": "Wall is sanded flat with 220-grit paper; surface depressions are filled with acrylic putty to ensure a flat canvas.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Basecoat Application",
                "description": "A high-adhesion colored basecoat is rolled evenly across the wall to create background contrast and depth.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Texture Compound Application",
                "description": "Specialized heavy-bodied acrylic texture material is troweled or rolled onto the wall in controlled sections.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Artisan Pattern Modeling",
                "description": "Master artisan models the design using specialized texturing combs, spatula trowels, sea sponges, or patterned rollers.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Protective Metallic / Pearl Glaze Coat",
                "description": "After texture drying, a metallic or pearl glaze topcoat is applied to accentuate 3D relief and provide washability.",
                "is_key_step": False
            },
            {
                "step_number": 7,
                "title": "Precision De-masking & Lighting Review",
                "description": "Tape is peeled off at a 45-degree angle for laser-sharp borders, floor is cleaned, and pattern is reviewed.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Italian stainless steel Venetian trowels and spatula knives",
            "Patterned texture rollers, graining combs, and natural sea sponges",
            "Precision low-tack blue painter's tape and heavy-duty floor drop sheets",
            "Fine 220-grit sanding blocks and tack cloths",
            "High-adhesion acrylic wall primer and tinted basecoat emulsion",
            "Heavy-bodied acrylic texture modeling compound and protective pearl/metallic top glaze"
        ],
        "customer_setup": [
            "Select and confirm your desired texture design pattern and metallic shade from our digital/physical catalog.",
            "Move furniture at least 5 feet away from the accent wall to allow the artisan adequate working clearance.",
            "Ensure wall lighting or spotlights are working to appreciate the 3D texture depth as it is applied."
        ],
        "aftercare": [
            "Allow the texture and protective glaze to cure undisturbed for 48 hours before touching or placing furniture nearby.",
            "Do not hang heavy paintings or drill into the textured wall for at least 7 days.",
            "Clean occasionally using a dry feather duster or barely damp microfiber cloth; avoid harsh scrubbing."
        ],
        "expected_results": [
            "Breathtaking 3D decorative accent wall that instantly transforms the visual luxury of the room.",
            "Rich textural depth and luminous light reflections that shift elegantly with changing room lighting.",
            "Durable, washable protective glaze resisting light domestic scuffs and color fading."
        ],
        "important_notes": [
            "Texture patterns are handcrafted artisan creations; subtle handcrafted organic variations are an inherent design hallmark.",
            "Wall must be completely dry and free from any dampness or efflorescence before texture application."
        ],
        "warranty": "1-year SmartServe warranty against texture chipping, peeling, or adhesion failure under normal indoor conditions.",
        "faqs": [
            {
                "question": "Can texture paint be applied on any wall in my house?",
                "answer": "Yes! Living room TV walls, master bedroom headboard walls, dining feature walls, and foyers are the most popular choices."
            },
            {
                "question": "Is texture paint washable?",
                "answer": "Yes, our textures are sealed with a protective acrylic glaze that makes them resistant to dust and easily cleanable with a damp cloth."
            },
            {
                "question": "How long does it take to texture a feature wall?",
                "answer": "A standard feature wall (up to 120 sq.ft.) typically takes 6 to 8 hours to complete including basecoat, modeling, and glaze."
            },
            {
                "question": "What happens if I want to remove or change the texture in the future?",
                "answer": "When you want to change it, the wall can simply be sanded down and skimmed with two coats of wall putty to restore a smooth canvas."
            },
            {
                "question": "Do I get to choose the metallic sheen and color?",
                "answer": "Yes, you can choose from silver, gold, copper, bronze, champagne, or pearl glaze sheens paired with any base wall color."
            }
        ],
        "dos": [
            "Do examine texture pattern swatches in your room's natural and artificial lighting before choosing.",
            "Do position warm spotlights or accent sconces to highlight the 3D relief of the finished texture.",
            "Do inspect the texture wall alongside the artisan upon completion."
        ],
        "donts": [
            "Don't touch or run fingers over wet texture material during application or the first 12 hours.",
            "Don't place adhesive stickers, cello tape, or heavy sticky hooks on textured walls.",
            "Don't clean the textured surface with wire brushes or harsh scouring powders."
        ],
        "tips": [
            "Warm golden or champagne metallic glazes on deep charcoal or teal base coats create a stunning, five-star luxury hotel ambiance."
        ],
        "service_features": [
            {"title": "Master Artisan Crafting", "description": "Handcrafted 3D decorative patterns with Italian trowels and combs"},
            {"title": "Protective Metallic Glaze", "description": "Luminous pearl or metallic topcoat offering washability and depth"},
            {"title": "High-Impact Feature Wall", "description": "Complete visual transformation of your living room or bedroom"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Decorative Texture Wall Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["texture painting", "wall texture design", "accent wall painting", "metallic wall texture", "royale play texture"],
            "seo_title": "Decorative Texture Painting Services | Designer Accent Wall Finishes",
            "seo_description": "Transform your room with luxury decorative wall texture painting. Metallic, stucco, and spatula finishes by master artisans with 1-year warranty.",
            "highlights": ["Master artisan crafting", "Protective metallic glaze", "High-impact feature wall"]
        }
    },
    {
        "id": "beae6816-da85-4e6e-a66d-184ad2be03b1",
        "name": "Wall Painting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Specialized Painting",
        "price": 2539.0,
        "duration_minutes": 360,
        "description": "Focused interior wall repainting service for specific individual walls, accent walls, or high-traffic areas (up to ~200 sq.ft. surface area). Ideal for refreshing stained hallway walls, touching up scuffed living areas, or creating new contrasting color themes. Includes floor masking, nail hole putty repair, fine sanding, primer undercoat, and two coats of premium washable emulsion.",
        "highlights": [
            "Targeted wall painting for individual walls up to 200 sq.ft. area",
            "Fast 1-day turnaround with minimal household disruption",
            "Floor and adjoining edge masking with clean-release painter's tape",
            "Surface preparation with nail hole filling and hairline crack repair",
            "Two finish coats of premium washable, stain-resistant interior emulsion"
        ],
        "included": [
            "Complete painting of specific interior walls up to 200 sq.ft. area",
            "Floor masking with heavy drop cloths along the base of the wall",
            "Taping side wall corners, ceiling borders, and skirting boards",
            "Scraping loose paint, old stickers, and grease marks",
            "Filling nail holes and minor hairline cracks with acrylic joint putty",
            "1 coat of primer undercoat over patched and repaired wall sections",
            "2 full topcoats of premium washable interior emulsion in selected shade",
            "Tape removal, edge cleanup, and paint spot wiping"
        ],
        "excluded": [
            "Painting adjoining ceilings or unselected walls in the room",
            "Wood door, window, or skirting polish/enamel painting",
            "External balcony or facade exterior wall painting",
            "Treating structural masonry cracks or active water dampness",
            "Dismantling heavy anchored entertainment or storage wall units"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Edge Masking & Floor Protection",
                "description": "Floor drop sheets are laid along the wall; ceiling line, side corners, and switches are masked with tape.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Wall Scraping & Defect Inspection",
                "description": "Loose flakes are scraped down; nail holes, anchor holes, and surface scuffs are identified.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Acrylic Putty Patch Repair",
                "description": "Acrylic wall putty is applied over nail holes and surface dents, then allowed to dry completely.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Fine Sanding & Spot Priming",
                "description": "Putty patches are hand-sanded with 220-grit paper and coated with an acrylic primer sealer.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Topcoat Rolling",
                "description": "First coat of washable emulsion is rolled on with neat edge cutting along borders.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Finish Coat Application",
                "description": "After a 3 to 4-hour drying interval, the second coat is applied for rich color depth and uniform sheen.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "De-masking & Clean Signoff",
                "description": "Masking tape is cleanly stripped at a 45-degree angle, floor is swept, and the wall is inspected.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "9-inch lint-free microfiber paint rollers with extension handles",
            "Precision synthetic trim sash cutting brushes (1.5-inch & 2.5-inch)",
            "180-grit and 220-grit silicon carbide sanding sheets",
            "Clean-release painter's blue masking tape and drop cloths",
            "Acrylic joint putty and interior wall primer sealer",
            "Premium washable, low-VOC acrylic interior emulsion paint"
        ],
        "customer_setup": [
            "Move furniture at least 4 feet away from the wall to provide adequate painter movement space.",
            "Remove all wall frames, calendars, and wall-hung items prior to technician arrival.",
            "Confirm the exact shade code and sheen level before rolling begins."
        ],
        "aftercare": [
            "Allow the paint to cure for at least 24 hours before moving furniture back near the wall.",
            "Wait at least 48 to 72 hours before re-hanging heavy pictures, mirrors, or wall clocks.",
            "Wipe accidental stains gently with a soft microfiber cloth; avoid harsh detergents for 14 days."
        ],
        "expected_results": [
            "Pristine, smooth wall finish with rich color consistency and zero roller streaks.",
            "Laser-sharp edge cut-ins against ceiling line, adjacent walls, and skirting boards.",
            "Complete concealment of old nail holes, scuff marks, and grease spots."
        ],
        "important_notes": [
            "Covers up to 200 sq.ft. of wall surface (equivalent to two standard 10x10 ft walls or one large 20x10 ft wall).",
            "If wall has active damp seepage, waterproofing treatment is required prior to painting."
        ],
        "warranty": "1-year SmartServe warranty covering paint flaking or peeling under normal indoor conditions.",
        "faqs": [
            {
                "question": "Can I paint just one accent wall in my living room?",
                "answer": "Yes! This service is specifically designed for individual walls, accent feature walls, or targeted room touch-ups."
            },
            {
                "question": "Can you match my existing wall color?",
                "answer": "Yes, our painters carry color fan decks and can match your existing wall shade or help you choose a contrasting tone."
            },
            {
                "question": "How long does it take to paint a single wall?",
                "answer": "A single wall up to 200 sq.ft. takes approximately 4 to 6 hours including surface prep, two coats, and cleanup."
            },
            {
                "question": "Will there be paint splatters on my floor or adjoining walls?",
                "answer": "No. We carefully tape all side borders, ceilings, and baseboards, and cover the floor with protective drop cloths."
            },
            {
                "question": "Is the paint washable?",
                "answer": "Yes, we use premium washable emulsions that allow light domestic stains to be gently wiped away with a damp cloth."
            }
        ],
        "dos": [
            "Do remove all hanging art, nails, and wall anchors before work starts.",
            "Do keep room windows open for gentle ventilation during drying.",
            "Do inspect the wall surface under room lighting during the final handover."
        ],
        "donts": [
            "Don't touch freshly rolled paint within the first 4 hours of application.",
            "Don't push heavy chairs or sofas flush against the wall for at least 48 hours.",
            "Don't use solvent or acid-based cleaners on the finished wall."
        ],
        "tips": [
            "A rich contrasting accent wall behind your living room television or bed headboard adds warmth and elegance to the entire room."
        ],
        "service_features": [
            {"title": "Targeted Wall Makeover", "description": "Focused painting for specific walls up to 200 sq.ft. in a few hours"},
            {"title": "Precision Masking", "description": "Laser-sharp border lines against ceilings and adjoining walls"},
            {"title": "Washable Emulsion", "description": "Durable, stain-resistant topcoat with uniform color depth"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Interior Wall Painting"
            }
        ],
        "seo_metadata": {
            "keywords": ["wall painting", "accent wall paint", "interior wall painting", "feature wall painters", "wall color painting"],
            "seo_title": "Targeted Interior Wall Painting Services | Accent & Feature Walls",
            "seo_description": "Paint specific interior walls or create a stunning accent wall. Complete edge masking, nail hole repair, dual-coat washable emulsion, and 1-year warranty.",
            "highlights": ["Targeted wall makeover", "Precision masking", "Washable emulsion"]
        }
    },
    {
        "id": "5e42fcf8-7454-4da3-8587-5b9e77197799",
        "name": "Wood Painting / Polishing",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Specialized Painting",
        "price": 3739.0,
        "duration_minutes": 480,
        "description": "Professional wood restoration, staining, and protective coating service for timber doors, door frames, window sills, wooden wall paneling, and solid wood furniture (up to ~60 sq.ft. surface area). Master polishers strip old cracked varnish, execute progressive grit sanding (80 to 320 grit), apply wood grain filler and rich natural wood stains, and seal with two to three coats of clear PU (Polyurethane) or Melamine polish in Gloss, Satin, or Matte finish.",
        "highlights": [
            "Master wood polishing and painting for surfaces up to 60 sq.ft.",
            "Progressive multi-stage sandpaper smoothing from 80 to 320 grit",
            "Natural wood stain infusion highlighting rich timber grain patterns",
            "Multi-coat protective PU (Polyurethane) or Melamine clear finish",
            "Superior resistance against moisture, heat rings, and domestic scratches"
        ],
        "included": [
            "Wood polishing or painting for doors, doorframes, window frames, or furniture (up to 60 sq.ft.)",
            "Floor, wall, and glass masking around wooden fixtures with protective film",
            "Chemical or manual scraping to strip deteriorated old polish/varnish",
            "Progressive mechanical and hand sanding with 80, 150, 220, and 320-grit papers",
            "Application of color-matched wood grain filler on dents, knots, and cracks",
            "Application of rich natural wood stain in customer's selected timber tone",
            "2 to 3 coats of clear protective PU / Melamine polish (Gloss, Satin, or Matte)",
            "Final fine-buffing, de-masking, glass cleaning, and work area cleanup"
        ],
        "excluded": [
            "Carpentry repairs requiring structural timber replacement or hinge realignment",
            "Polishing laminate / Sunmica sheets (laminates cannot absorb wood stains/polish)",
            "Exterior wooden pergolas exposed to direct monsoon downpours",
            "Upholstery fabric cleaning or leather cushion restoration",
            "Antique museum-grade historical timber preservation"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Perimeter & Hardware Masking",
                "description": "Adjoining wall plaster, floor tiles, and metal locks/handles are taped securely with protective tape.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Old Finish Stripping & Coarse Sanding",
                "description": "Deteriorated old lacquer is stripped; wood is sanded with 80/120-grit paper down to bare sound timber.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Wood Grain Filling & Void Sealing",
                "description": "Specially formulated wood grain filler matched to timber color is squeegeed across the grain to fill pores.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "Progressive Fine Sanding & Tack Cleaning",
                "description": "Cured filler is hand-sanded with 220 and 320-grit papers until silky smooth, then wiped with solvent tack cloths.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Wood Stain Application",
                "description": "Natural wood stain (Teak, Walnut, Rosewood, Mahogany, or Oak) is hand-rubbed evenly into the grain.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Base Sealer & Topcoat PU / Melamine",
                "description": "First coat of wood sealer is applied, followed by dual coats of premium clear PU or Melamine finish.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "Fine Buffing & De-masking",
                "description": "Once dry, the surface is buffed for smooth luster; masking tape is removed, and hardware is cleaned.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Silicon carbide sandpaper sheets (80, 120, 220, and 320 grit) and orbital sanding blocks",
            "Soft cotton polishing pads (malmal cloth) and fine camel-hair varnish brushes",
            "Solvent tack cloths, painter's blue masking tape, and floor protective drop sheets",
            "Color-matched acrylic wood grain filler and wood putty",
            "Natural oil/spirit-based timber stains (Teak, Walnut, Rosewood, Mahogany)",
            "Two-component clear PU (Polyurethane) or Melamine wood polish (Gloss / Satin / Matte)"
        ],
        "customer_setup": [
            "Clear items off wooden tabletops or remove items hanging behind doors before technicians arrive.",
            "Ensure steady room ventilation to disperse solvent fumes during polishing.",
            "Keep pets and children away from the polishing area until the surface is completely dry."
        ],
        "aftercare": [
            "Allow the clear polish to cure undisturbed for at least 24 hours before using tables or handling doors.",
            "Always use coasters under hot beverage cups or cold iced glasses to prevent condensation marks.",
            "Wipe wooden surfaces only with a soft dry or slightly damp cotton cloth; never use ammonia or harsh chemical sprays."
        ],
        "expected_results": [
            "Rich, glowing wood finish accentuating natural timber grain with smooth, touchable luster.",
            "Complete elimination of old surface scratches, cup rings, and sun-faded patches.",
            "Durable protective shield resisting moisture penetration, everyday spills, and surface scuffs."
        ],
        "important_notes": [
            "Applicable only to natural solid wood or wood veneer; synthetic laminates and PVC surfaces cannot be polished.",
            "PU and Melamine polishes emit a noticeable solvent odor during application; good ventilation is essential."
        ],
        "warranty": "1-year SmartServe warranty against polish peeling, flaking, or crazing on natural timber surfaces.",
        "faqs": [
            {
                "question": "Can you polish laminate or Sunmica modular cabinets?",
                "answer": "No. Wood polish and stains require porous natural timber or veneer to absorb. Synthetic laminates and Sunmica cannot be polished."
            },
            {
                "question": "What is the difference between PU polish and Melamine polish?",
                "answer": "PU (Polyurethane) offers superior scratch and UV resistance with high flexibility, while Melamine provides an economical, hard glossy finish."
            },
            {
                "question": "Can you change the shade of my existing wooden doors?",
                "answer": "Yes! By sanding down to bare wood, we can apply lighter or darker timber stains such as Teak, Walnut, Mahogany, or Dark Oak."
            },
            {
                "question": "How long does door polishing take?",
                "answer": "A standard main door and frame take approximately 6 to 8 hours across multiple sanding, staining, and sealing coats."
            },
            {
                "question": "Can water cup marks and heat rings be removed?",
                "answer": "Yes. Our deep progressive sanding removes existing surface moisture rings and water stains before re-staining and sealing."
            }
        ],
        "dos": [
            "Do confirm your preferred timber stain shade and sheen (Gloss vs. Satin vs. Matte) with the supervisor.",
            "Do keep room windows wide open during application for optimal drying and ventilation.",
            "Do inspect the door edges and frame corners during final handover."
        ],
        "donts": [
            "Don't touch freshly polished wood for at least 12 hours.",
            "Don't place hot cookware or wet glasses directly on polished wood without coasters.",
            "Don't use solvent or alcohol-based sanitizing wipes on polished timber surfaces."
        ],
        "tips": [
            "A Satin or Matte PU finish on main wooden doors provides an understated, contemporary look while resisting visible fingerprints."
        ],
        "service_features": [
            {"title": "Progressive Grit Sanding", "description": "Deep multi-stage smoothing removing old stains down to bare timber"},
            {"title": "Rich Timber Staining", "description": "Natural grain-enhancing stains in Teak, Walnut, Rosewood, and Oak"},
            {"title": "Dual-Coat PU / Melamine", "description": "Tough, water-resistant clear coat in Gloss, Satin, or Matte finish"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1538688525198-9b88f6f53126?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Wood Painting and Polishing"
            }
        ],
        "seo_metadata": {
            "keywords": ["wood polishing", "wood painting", "door polishing", "PU wood polish", "melamine polish", "furniture polishing"],
            "seo_title": "Wood Painting & Polishing Services | Door & Furniture PU Polish",
            "seo_description": "Restore natural wooden doors, frames, and furniture. Multi-stage sanding, rich timber staining, PU/Melamine clear finish, and 1-year warranty.",
            "highlights": ["Progressive grit sanding", "Rich timber staining", "Dual-coat PU / Melamine"]
        }
    }
]

WATERPROOFING_GROUTING_SERVICES = [
    {
        "id": "9b61bcd6-f23c-42de-970b-909d17481d59",
        "name": "Bathroom Waterproofing",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Waterproofing & Grouting",
        "price": 1839.0,
        "duration_minutes": 360,
        "description": "Non-destructive, specialized bathroom waterproofing and joint seal treatment (for standard bathrooms up to ~60 sq.ft. floor area). Designed to permanently halt water seepage leaking into adjoining bedroom walls, peeling baseboards, or downstairs neighbor ceilings without breaking existing tiles. Features mechanical tile joint raking, chemical cleaning, crystalline polymer slurry injection around drain collars and plumbing traps, followed by 100% waterproof epoxy grout joint sealing.",
        "highlights": [
            "Non-invasive bathroom waterproofing without breaking or replacing existing tiles",
            "Stops chronic moisture seepage leaking into adjoining bedroom walls",
            "Pressure penetration sealing around floor drain collars and sanitary trap pipes",
            "Mechanical joint raking and 100% waterproof epoxy resin grout packing",
            "Anti-fungal, chemical-resistant seal impervious to bath soaps and detergents"
        ],
        "included": [
            "Complete floor and lower 2-foot wall splash zone waterproofing (up to 60 sq.ft. bathroom)",
            "Mechanical raking out of old discolored, cracked, or porous cement grout to 4mm depth",
            "Chemical deep-cleaning and vacuuming of tile joints to remove soap scum and mold spores",
            "Injection of crystalline acrylic polymer waterproof slurry along sanitary penetrations and drain traps",
            "Application of flexible polyurethane sealant along perimeter wall-floor coving joints",
            "Packing all floor tile joints with 100% waterproof two-part epoxy resin grout",
            "Sponging off tile surface haze and restoring sparkling clean tile finish",
            "Full site cleanup, joint inspection, and curing guidelines"
        ],
        "excluded": [
            "Breaking and replacing bathroom floor tiles or concrete civil demolition",
            "Fixing ruptured concealed pressurized copper or CPVC water supply pipes",
            "Replacing bathroom sanitaryware (toilets, washbasins, shower cubicles)",
            "Waterproofing areas outside the designated single bathroom",
            "Re-painting adjoining bedroom walls damaged by historical dampness (booked separately)"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Moisture Assessment & Drain Trap Inspection",
                "description": "Technician measures moisture levels along baseboards and inspects floor drain collars, shower corners, and joints.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Mechanical Joint Raking & Cleaning",
                "description": "Old deteriorated cement grout is raked out to a depth of 3-5mm using specialized diamond oscillating grout saws.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Joint Degreasing & Industrial Vacuuming",
                "description": "Raked joints are chemically treated to dissolve body oils and soap residue, followed by high-suction vacuuming.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "Drain Collar Polymer Slurry Sealing",
                "description": "Hydrophobic crystalline polymer slurry is injected around drain pipe collars and sanitary traps to block sub-tile voids.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Perimeter PU Joint Sealing",
                "description": "A continuous bead of flexible moisture-curing polyurethane sealant is tooled along wall-to-floor junctions.",
                "is_key_step": False
            },
            {
                "step_number": 6,
                "title": "Two-Part Epoxy Grout Packing",
                "description": "High-performance two-component waterproof epoxy grout is forced deeply into all tile joints using rubber floats.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "Tile De-hazing & Final Cleanup",
                "description": "Surplus epoxy is emulsified with neutral detergent sponges, tiles are buffed dry, and curing instructions provided.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Electric oscillating grout rake tools and diamond-grit carbide hand scrapers",
            "Wet/dry industrial vacuum cleaner with crevice nozzle",
            "Hard rubber epoxy grout float squeegees and non-abrasive cellulose emulsifying pads",
            "Two-part waterproof epoxy resin grout (Resin + Hardener + Color Quartz Filler)",
            "Deep-penetrating acrylic crystalline polymer waterproofing slurry",
            "High-flexibility moisture-curing polyurethane perimeter sealant"
        ],
        "customer_setup": [
            "Keep the bathroom completely dry and unused for at least 12 hours prior to service appointment.",
            "Remove personal shampoo bottles, bathmats, buckets, and toiletries from the bathroom floor.",
            "Ensure the main electrical supply and running water are available for cleaning equipment."
        ],
        "aftercare": [
            "Do not use the bathroom or run water onto the floor for at least 24 hours after completion.",
            "Allow the epoxy grout to achieve full chemical cure for 48 hours before using floor cleaners.",
            "Avoid using strong hydrochloric acid on bathroom tiles; clean only with mild liquid soap."
        ],
        "expected_results": [
            "Immediate halt of water seepage through bathroom floor into adjacent room walls or lower flats.",
            "Solid, impermeable epoxy tile joints that will never crumble, crack, or harbor black mold.",
            "Sparkling, hygienic tile floor with fresh, uniform grout lines matching your tile color."
        ],
        "important_notes": [
            "This non-destructive treatment cures joint and drain collar seepage; if plumbing pipes inside the concrete slab are cracked or leaking under constant pressure, plumbing repairs must precede waterproofing.",
            "Standard package covers bathroom floor up to 60 sq.ft."
        ],
        "warranty": "2-year SmartServe waterproofing warranty against joint leakage and grout displacement.",
        "faqs": [
            {
                "question": "Can you waterproof my bathroom without breaking the tiles?",
                "answer": "Yes! Our specialized non-invasive treatment removes porous cement grout and seals all joints, drain collars, and junctions with 100% waterproof epoxy and crystalline polymers without breaking a single tile."
            },
            {
                "question": "How long does bathroom waterproofing take?",
                "answer": "The complete non-destructive waterproofing process takes approximately 4 to 6 hours for a standard bathroom."
            },
            {
                "question": "How soon can we use the bathroom after service?",
                "answer": "The bathroom must remain completely dry for 24 hours after service to allow the epoxy grout and polymer barriers to fully cure."
            },
            {
                "question": "Will this stop the paint peeling on the bedroom wall behind the bathroom?",
                "answer": "Yes. Most bedroom wall peeling is caused by moisture seeping through porous bathroom tile joints. Once sealed, the adjacent wall will dry out permanently."
            },
            {
                "question": "Does epoxy grout turn yellow or discolored over time?",
                "answer": "No. Unlike traditional cement grout, two-part epoxy grout is non-porous, stain-resistant, and 100% waterproof, so it never turns black or molds."
            }
        ],
        "dos": [
            "Do keep the bathroom dry for 12 hours before our technician arrives.",
            "Do inform the technician of any known leakage points or moisture patches in adjacent rooms.",
            "Do follow the 24-hour dry curing period strictly for maximum long-term durability."
        ],
        "donts": [
            "Don't pour water onto the bathroom floor within 24 hours of service completion.",
            "Don't clean bathroom tiles with unbuffered muriatic acid; use neutral pH detergents.",
            "Don't scrape or pick at freshly placed epoxy joints while curing."
        ],
        "tips": [
            "Matching epoxy grout to your tile color creates a sleek, seamless look while creating a 100% water-impermeable floor pan."
        ],
        "service_features": [
            {"title": "Zero Tile Breakage", "description": "Non-destructive treatment saving huge demolition costs and downtime"},
            {"title": "100% Waterproof Epoxy", "description": "Impermeable two-part epoxy grout impervious to water and mold"},
            {"title": "2-Year Seepage Warranty", "description": "Guaranteed protection against bathroom floor water seepage"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Bathroom Waterproofing"
            }
        ],
        "seo_metadata": {
            "keywords": ["bathroom waterproofing", "tile joint waterproofing", "stop bathroom seepage", "epoxy grout waterproofing", "non invasive waterproofing"],
            "seo_title": "Bathroom Waterproofing Services | Non-Destructive Tile Sealing",
            "seo_description": "Stop bathroom water seepage without breaking tiles. Mechanical joint raking, drain collar sealing, 100% waterproof epoxy grout, and 2-year warranty.",
            "highlights": ["Zero tile breakage", "100% waterproof epoxy", "2-year seepage warranty"]
        }
    },
    {
        "id": "8ad896e9-77bb-4478-8daf-13ab2c62bba1",
        "name": "Leakage Treatment",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Waterproofing & Grouting",
        "price": 3339.0,
        "duration_minutes": 360,
        "description": "Targeted diagnostic and remedial treatment for active water seepage, damp patches, and ceiling drips in residential apartments and homes (up to ~100 sq.ft. affected area). Features non-destructive digital moisture mapping, acoustic acoustic/pressure pipe testing to isolate the seepage origin, high-pressure polyurethane (PU) injection grouting or crystalline slurry barrier treatment, and water-repellent protective plaster patching.",
        "highlights": [
            "Accurate diagnostic moisture mapping to pinpoint hidden leak sources",
            "High-pressure polyurethane (PU) foam injection grouting for active fissures",
            "Crystalline barrier treatment penetrating deep into porous concrete capillaries",
            "Permanent stoppage of damp patches, ceiling drips, and efflorescence salt blooms",
            "Fast-acting hydrophobic polymers expanding up to 20x to seal pressurized voids"
        ],
        "included": [
            "Diagnostic moisture mapping of affected walls and ceilings (up to 100 sq.ft. area)",
            "Acoustic and thermal dampness source investigation across adjacent wet areas",
            "Chipping loose, efflorescence-damaged plaster to expose underlying concrete/brick substrate",
            "Drilling injection ports and installing mechanical packers along crack pathways",
            "High-pressure injection of hydrophobic expanding polyurethane (PU) resin grout",
            "Application of anti-efflorescence chemical salt neutralizer wash",
            "Plastering repaired area with water-resistant polymer-modified mortar",
            "Site cleanup, packer removal, and joint moisture verification walkthrough"
        ],
        "excluded": [
            "Concealed main plumbing pipe replacement requiring heavy floor excavation",
            "Final decorative wall painting (recommended after 7 days of moisture evaporation)",
            "External high-rise building facade rope access waterproofing above 3 floors",
            "Structural civil replacement of rusted steel reinforcement bars",
            "Whole-roof membrane installation (available under Terrace Waterproofing)"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Moisture Mapping & Source Diagnosis",
                "description": "Digital moisture meters and thermal imaging identify the exact path, saturation gradient, and source of water ingress.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Plaster Chipping & Crack Channel Opening",
                "description": "Blistered paint and hollow plaster are chipped away to expose structural cracks and wet concrete joints.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Injection Port Drilling & Packer Placement",
                "description": "Holes are drilled at a 45-degree angle intersecting the crack; high-pressure mechanical packers are tightened in place.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "High-Pressure PU Injection Grouting",
                "description": "Hydrophobic polyurethane resin is pumped at high pressure, reacting with water to expand 20x and seal all voids.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Packer Removal & Anti-Salpetre Wash",
                "description": "Packers are snapped off once cured; an anti-efflorescence chemical wash is applied to neutralize mineral salts.",
                "is_key_step": False
            },
            {
                "step_number": 6,
                "title": "Polymer Waterproof Mortar Patching",
                "description": "The chipped area is skimmed with water-resistant polymer-modified cement mortar flush with the surrounding wall.",
                "is_key_step": False
            },
            {
                "step_number": 7,
                "title": "Cleanup & Moisture Handover",
                "description": "Debris is bagged and removed, floor is swept, and post-injection moisture readings are recorded for warranty records.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital pinless moisture meter and thermal dampness sensor",
            "High-pressure electric airless injection pump (up to 4000 PSI capacity)",
            "Heavy-duty rotary hammer drill and mechanical brass/steel injection packers",
            "Hydrophobic single/two-component expanding polyurethane (PU) injection resin",
            "Anti-efflorescence chemical wash solution (salt neutralizer)",
            "Polymer-modified water-resistant repair mortar and troweling tools"
        ],
        "customer_setup": [
            "Clear furniture and storage items away from the damp wall or ceiling drip zone.",
            "Coordinate with upstairs neighbor if ceiling leakage originates from their bathroom or balcony plumbing.",
            "Provide uninterrupted electrical power for heavy-duty drill and injection pump operation."
        ],
        "aftercare": [
            "Allow the polymer-modified patch to cure for 48 to 72 hours.",
            "Wait at least 7 to 10 days for residual dampness within the masonry to evaporate before repainting.",
            "Notify SmartServe immediately if any abnormal dampness persists past 14 days."
        ],
        "expected_results": [
            "Complete and permanent stoppage of active water dripping, oozing, and damp capillary migration.",
            "Dry, stable concrete substrate free from efflorescence salt crystals and toxic mold spores.",
            "Smooth, water-resistant patched wall surface prepared for final decorative painting."
        ],
        "important_notes": [
            "Residual moisture already trapped inside brickwork will take 7 to 14 days to fully evaporate to room air.",
            "If leakage is caused by a continuously leaking pressurized municipal water pipe, the pipe fitting must be repaired alongside grouting."
        ],
        "warranty": "2-year SmartServe warranty covering recurrence of leakage at the treated injection site.",
        "faqs": [
            {
                "question": "How does PU injection grouting stop active water leaks?",
                "answer": "Polyurethane resin is pumped under high pressure into the crack. When it encounters water, it chemically reacts and expands 20 times into a tough, flexible waterproof foam that permanently seals every microscopic void."
            },
            {
                "question": "My ceiling is dripping from the flat above. Can this be treated from inside my flat?",
                "answer": "Yes! PU pressure injection grouting is applied from the negative side (your ceiling) into the concrete slab, sealing water channels within the slab without requiring entry into the flat above."
            },
            {
                "question": "When can I repaint the wall after leakage treatment?",
                "answer": "We recommend waiting 7 to 10 days. While the leak is stopped immediately, trapped moisture within the masonry must evaporate before primer and paint are applied."
            },
            {
                "question": "What causes white chalky powder (efflorescence) on damp walls?",
                "answer": "As water travels through brick and concrete, it dissolves mineral salts. When water evaporates on the wall surface, it leaves white salt deposits. We apply an anti-efflorescence chemical wash to permanently neutralize them."
            },
            {
                "question": "How long does the leakage treatment take?",
                "answer": "A standard targeted treatment takes approximately 4 to 6 hours depending on crack length and number of injection packers installed."
            }
        ],
        "dos": [
            "Do report active leaks promptly to prevent structural rusting of internal steel reinforcement bars.",
            "Do keep room well-ventilated after injection to accelerate moisture evaporation from surrounding plaster.",
            "Do inspect the repaired area under day lighting during the final signoff."
        ],
        "donts": [
            "Don't apply putty or paint over damp walls immediately; always allow 7-10 days for trapped moisture to dissipate.",
            "Don't scrape injection ports with sharp metal screwdrivers while curing.",
            "Don't ignore musty odors or damp patches on walls bordering bathrooms."
        ],
        "tips": [
            "Addressing minor damp patches early prevents costly structural concrete deterioration and black mold contamination inside bedrooms."
        ],
        "service_features": [
            {"title": "High-Pressure PU Injection", "description": "Expanding resin sealing active leaks deep inside concrete slabs"},
            {"title": "Diagnostic Moisture Mapping", "description": "Accurate detection of hidden water ingress pathways and saturation"},
            {"title": "2-Year Leakage Warranty", "description": "Guaranteed protection against seepage recurrence at the treated site"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Leakage Treatment"
            }
        ],
        "seo_metadata": {
            "keywords": ["leakage treatment", "stop water leakage", "ceiling dampness repair", "PU injection grouting", "seepage repair"],
            "seo_title": "Leakage Treatment Services | PU Injection Grouting for Seepage",
            "seo_description": "Stop active water leakage and ceiling dampness permanently. High-pressure PU injection grouting, moisture mapping, and 2-year warranty.",
            "highlights": ["High-pressure PU injection", "Diagnostic moisture mapping", "2-year leakage warranty"]
        }
    },
    {
        "id": "7f783def-48ea-41dd-8897-b543b23bb353",
        "name": "Terrace Waterproofing",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Waterproofing & Grouting",
        "price": 1099.0,
        "duration_minutes": 720,
        "description": "High-performance multi-layer elastomeric waterproofing system for open rooftops, terraces, and building parapets (priced per unit / ~100 sq.ft. area). Engineered to withstand heavy monsoon pooling, extreme solar UV radiation, and thermal expansion cycles. Features high-pressure water jet cleaning, crack opening and flexible polyurethane filling, coving at parapet slab junctions, and application of a heavy-duty reinforced elastomeric waterproof membrane.",
        "highlights": [
            "Multi-layer elastomeric waterproofing for open rooftops and terraces",
            "High elongation membrane bridging active structural thermal expansion cracks",
            "Heavy-duty UV resistance reflecting solar heat and lowering indoor room temperatures",
            "High-pressure pressure washer bio-wash removing embedded algae and dirt",
            "Reinforced non-woven polyester mesh reinforcement over critical slab joints"
        ],
        "included": [
            "Terrace rooftop slab and vertical parapet wall coving waterproofing (measured area)",
            "High-pressure water washing (120-bar) to strip calcified dust, algae, and loose coatings",
            "Chipping and widening active terrace cracks into a V-groove configuration",
            "Packing structural cracks with high-flexibility polyurethane joint sealant",
            "Constructing rounded polymer-mortar coving along wall-to-floor 90-degree junctions",
            "1 coat of deep-penetrative acrylic rooftop primer",
            "2 heavy coats of elastomeric liquid waterproof membrane with polyester mesh embedded at critical joints",
            "Full site cleanup, rainwater drain unclogging, and ponding test guidance"
        ],
        "excluded": [
            "Civil re-casting of crumbling structural RCC concrete slabs",
            "Laying protective brick-bat coba or heavy ceramic terrace tiling",
            "Waterproofing overhead water storage tanks (available as a separate tank service)",
            "Replacing rooftop solar panel metal mounting framework",
            "Plumbing replacement of damaged rainwater downpipes"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Pressure Jet Washing & Debris Removal",
                "description": "Rooftop surface is deep cleaned with 120-bar water jets to blast off moss, dirt, and decayed old coatings.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Crack V-Grooving & Surface Prep",
                "description": "All slab cracks are widened into a 6mm V-groove with angle grinders and dusted clean with blowers.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Polyurethane Crack Packing",
                "description": "Cracks are filled flush with high-elongation polyurethane elastomer sealant to accommodate structural expansion.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Parapet Coving & Primer Base",
                "description": "Parapet junctions receive rounded polymer coving; high-bonding rooftop primer is rolled across the slab.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "First Elastomeric Coat & Mesh Laying",
                "description": "First heavy coat of elastomeric liquid membrane is applied; non-woven polyester mesh is embedded over joints.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Second Cross-Coat Membrane Application",
                "description": "Second thick coat of elastomeric membrane is applied perpendicular to form a seamless, joint-free rubberized blanket.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "Drain Inspection & Ponding Test Advisory",
                "description": "Rainwater outlets are detailed with sealant and client is advised on 48-hour cure and ponding test schedule.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Commercial high-pressure power washer (120-140 bar)",
            "Angle grinders with diamond masonry cutting blades and wire cup wheels",
            "Heavy-duty texture rollers, long-handle squeegees, and vulcanized rubber sealant guns",
            "Non-woven polyester reinforcing mesh (45 GSM to 60 GSM)",
            "High-elongation moisture-cured polyurethane elastomeric crack sealant",
            "100% acrylic elastomeric liquid waterproofing membrane with UV reflective polymers"
        ],
        "customer_setup": [
            "Ensure access to an outdoor water connection with continuous water flow for pressure jet washing.",
            "Clear terrace floor of flower pots, disused furniture, and loose storage items before start.",
            "Ensure continuous electricity supply on the rooftop for power tools and washing machines."
        ],
        "aftercare": [
            "Allow the elastomeric membrane to cure undisturbed for at least 72 hours before walking on it.",
            "Keep rooftop rainwater downpipe strainers clear of fallen leaves and plastic debris.",
            "Do not drag heavy sharp metal objects or furniture across the finished membrane."
        ],
        "expected_results": [
            "100% monolithic, seamless rubberized waterproof barrier preventing monsoon roof leaks.",
            "High solar reflectance (SRI) lowering top-floor room temperatures by 3 to 5 degrees Celsius.",
            "Flexible crack-bridging membrane absorbing intense seasonal thermal expansion without tearing."
        ],
        "important_notes": [
            "Terrace waterproofing requires dry weather conditions during application; cannot be executed during active rain.",
            "Rate applies per measured area unit (~100 sq.ft.); full terrace scale quoted after on-site laser measurement."
        ],
        "warranty": "3-year SmartServe terrace waterproofing warranty against monsoon rainwater penetration.",
        "faqs": [
            {
                "question": "How does elastomeric terrace waterproofing handle summer heat and monsoon cold?",
                "answer": "Our elastomeric liquid membrane has over 300% elongation flexibility, expanding and contracting with seasonal temperature shifts without cracking or tearing."
            },
            {
                "question": "Can I walk on the terrace after waterproofing?",
                "answer": "Yes, our heavy-duty elastomeric system is formulated for regular residential foot traffic once fully cured after 72 hours."
            },
            {
                "question": "Will terrace waterproofing help reduce heat in top-floor rooms?",
                "answer": "Yes! Our high-reflectance white membrane reflects up to 80% of solar radiation, reducing top-floor ceiling temperatures by 3 to 5°C."
            },
            {
                "question": "How long will terrace waterproofing last?",
                "answer": "When applied properly with crack sealing, mesh reinforcement, and dual coats, our terrace waterproofing system lasts 5 to 7+ years."
            },
            {
                "question": "Do you perform a ponding test after completion?",
                "answer": "Yes, after a 72-hour cure, the terrace can be ponded with 2-3 inches of water for 24 hours to verify 100% watertight integrity."
            }
        ],
        "dos": [
            "Do inspect and clear rooftop drainage spouts before each monsoon season.",
            "Do clear flower pots and rooftop clutter onto stands to allow water to drain freely.",
            "Do walk through the rooftop with the supervisor to verify parapet coving coverage."
        ],
        "donts": [
            "Don't drag sharp metal furniture, ladders, or satellite dish stands across the membrane.",
            "Don't puncture or drill into the waterproofed terrace slab without applying sealant.",
            "Don't allow stagnant water to pool due to clogged leaves in rainwater drainage pipes."
        ],
        "tips": [
            "Waterproofing your terrace with an elastomeric white membrane not only stops rain leaks but significantly cuts your summer AC electricity bills."
        ],
        "service_features": [
            {"title": "Seamless Elastomeric Blanket", "description": "Over 300% elongation bridging structural expansion cracks"},
            {"title": "Solar Heat Reflective", "description": "High-SRI white finish lowering top-floor room temperatures"},
            {"title": "3-Year Monsoon Warranty", "description": "Guaranteed protection against monsoon rooftop water ingress"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Terrace Waterproofing"
            }
        ],
        "seo_metadata": {
            "keywords": ["terrace waterproofing", "roof waterproofing", "rooftop seepage solution", "elastomeric roof coating", "monsoon waterproofing"],
            "seo_title": "Terrace Waterproofing Services | Elastomeric Rooftop Protection",
            "seo_description": "Protect your rooftop against monsoon leaks and heat. Pressure washing, crack sealing, reinforced elastomeric membrane, and 3-year warranty.",
            "highlights": ["Seamless elastomeric blanket", "Solar heat reflective", "3-year monsoon warranty"]
        }
    },
    {
        "id": "b819bd35-4ec8-4bde-b51d-49ef5cc66ba9",
        "name": "Tile Grouting",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Waterproofing & Grouting",
        "price": 2029.0,
        "duration_minutes": 360,
        "description": "Precision restoration and high-performance regrouting for floor and wall tile joints in bathrooms, kitchens, balconies, and living spaces (up to ~120 sq.ft. surface area). Mechanical diamond rakes strip out discolored, crumbled, or mold-infested old cement grout to 3-5mm depth, followed by antimicrobial sanitization and packing with premium stain-resistant two-part epoxy or polymer-modified waterproof grout flush with tile bevels.",
        "highlights": [
            "Professional tile regrouting for floors and walls up to 120 sq.ft. area",
            "Mechanical diamond raking removing disintegrated, mildewed cement grout",
            "100% waterproof and stain-resistant two-part epoxy resin grout packing",
            "Permanent prevention of water seepage between tile joints into underlying slabs",
            "Wide palette of shade matching options complementing all ceramic and vitrified tiles"
        ],
        "included": [
            "Complete tile joint raking and regrouting for up to 120 sq.ft. of tiled area",
            "Masking of adjoining non-tiled fixtures, wooden thresholds, and drains",
            "Precision mechanical raking of old grout lines to an optimal 3-5mm depth",
            "High-suction vacuuming to extract all pulverised cement dust and debris",
            "Antifungal chemical wash neutralizing hidden mold and bacterial colonies",
            "Deep packing of tile joints with premium two-part waterproof epoxy grout",
            "Multi-stage tile surface sponging, de-hazing, and streak-free buffing",
            "Final joint inspection, debris removal, and post-service care handover"
        ],
        "excluded": [
            "Replacing cracked, broken, or hollow loose ceramic/vitrified tiles",
            "Civil demolition or full tile replacement re-tiling work",
            "Treating pressurized plumbing pipe leaks concealed beneath concrete slab",
            "Polishing natural Italian marble or granite slabs (available as stone polishing)",
            "Grouting swimming pools or industrial commercial kitchen facilities"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Site Inspection & Tile Adhesion Check",
                "description": "Technician taps tiles to confirm solid adhesion and selects the matching epoxy grout color shade.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Mechanical Joint Raking",
                "description": "Diamond oscillating blades rake out old crumbling cement grout cleanly to 3-5mm depth without chipping tile edges.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Dust Extraction & Anti-Mold Wash",
                "description": "High-suction vacuum extracts dust from joint cavities; an antifungal biocidal wash sterilizes joint channels.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "Epoxy Grout Blending & Preparation",
                "description": "Two-part epoxy resin, hardener, and color-matched silica quartz filler are mixed to a creamy homogeneous paste.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Full-Depth Joint Packing",
                "description": "Epoxy grout is packed diagonally across joints with hard rubber floats, eliminating air pockets and voids.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Emulsification & Surface De-hazing",
                "description": "Surplus epoxy is emulsified with cellulose sponges and warm water; tile faces are wiped completely clean.",
                "is_key_step": True
            },
            {
                "step_number": 7,
                "title": "Final Inspection & Curing Guidelines",
                "description": "Grout lines are checked for uniform flush profile, surrounding area is cleaned, and curing instructions provided.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Electric oscillating multi-tools with diamond grout-removal blades",
            "Manual carbide-tipped grout rakes for tight corners and edges",
            "Industrial HEPA vacuum cleaner for deep joint dust extraction",
            "Hard rubber epoxy grout floats and non-abrasive cellulose emulsifying sponges",
            "Two-part waterproof epoxy resin grout (Resin, Hardener, and Color Quartz)",
            "Antifungal biocidal joint sterilizer and epoxy haze remover"
        ],
        "customer_setup": [
            "Keep the tiled floor dry and clean for 12 hours prior to technician arrival.",
            "Remove rugs, floor mats, and loose floor items from the work area.",
            "Ensure steady running water and electrical outlets are accessible for equipment."
        ],
        "aftercare": [
            "Keep the newly grouted area dry and avoid walking on it for 24 hours.",
            "Wait 48 hours before using chemical floor cleaners or scrubbing the tile joints.",
            "Clean tiled floors with neutral pH floor cleaners; avoid strong unbuffered acids."
        ],
        "expected_results": [
            "Flawless, uniform grout lines completely flush with tile edges, restoring a brand-new floor look.",
            "100% water-impermeable barrier preventing sub-tile moisture seepage into underlying concrete.",
            "Stain-proof, mold-proof joints that resist discoloration from soaps, oils, and foot traffic."
        ],
        "important_notes": [
            "Covers up to 120 sq.ft. of floor or wall tile area (sufficient for 1-2 standard bathrooms or a kitchen).",
            "Tiles must be firmly bonded to the floor; loose or drummy tiles should be re-fixed before grouting."
        ],
        "warranty": "2-year SmartServe warranty against epoxy grout cracking, peeling, or displacement.",
        "faqs": [
            {
                "question": "Why should I choose epoxy grout over regular cement grout?",
                "answer": "Cement grout is porous, absorbing water, soap scum, and breeding black mold over time. Epoxy grout is 100% non-porous, waterproof, chemical-resistant, and never discolors or cracks."
            },
            {
                "question": "Will mechanical raking damage my existing tiles?",
                "answer": "No. Our technicians use precision oscillating diamond blades that vibrate within the grout channel, cleanly extracting the old grout without touching or chipping the tile glaze."
            },
            {
                "question": "How long does tile regrouting take?",
                "answer": "A standard bathroom or kitchen area (up to 120 sq.ft.) takes approximately 4 to 6 hours from raking to final sponge cleanup."
            },
            {
                "question": "Can I choose the color of the new grout?",
                "answer": "Yes! We offer a full spectrum of colors including White, Ivory, Beige, Grey, Anthracite, Brown, and Terracotta to match your tile shades."
            },
            {
                "question": "How soon can we walk on the floor after grouting?",
                "answer": "Light foot traffic is safe after 24 hours. Full water immersion and chemical washing should wait 48 hours for complete chemical curing."
            }
        ],
        "dos": [
            "Do wipe spills promptly to keep tile surfaces looking pristine.",
            "Do select a grout shade that complements your tile edge bevels.",
            "Do respect the 24-hour dry curing period before running water."
        ],
        "donts": [
            "Don't pour harsh toilet acids or unbuffered hydrochloric acid over fresh epoxy grout.",
            "Don't walk on freshly grouted joints with muddy footwear during the first 24 hours.",
            "Don't use steel wool or metal scrapers to scrub grout lines in the future."
        ],
        "tips": [
            "Regrouting your bathroom or kitchen floor every few years prevents sub-tile water accumulation and restores a hygienic, hotel-quality appearance."
        ],
        "service_features": [
            {"title": "Diamond Blade Raking", "description": "Clean removal of old crumbling grout to 4mm depth without tile damage"},
            {"title": "100% Waterproof Epoxy", "description": "Non-porous resin preventing water penetration, staining, and mold"},
            {"title": "2-Year Displacement Warranty", "description": "Guaranteed long-lasting joint adhesion and color stability"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Tile Grouting"
            }
        ],
        "seo_metadata": {
            "keywords": ["tile grouting", "epoxy tile grouting", "bathroom regrouting", "waterproof tile grout", "floor tile grout repair"],
            "seo_title": "Professional Tile Grouting Services | Waterproof Epoxy Regrouting",
            "seo_description": "Restore discolored or leaking tile joints with professional epoxy grouting. Diamond raking, mold eradication, waterproof finish, and 2-year warranty.",
            "highlights": ["Diamond blade raking", "100% waterproof epoxy", "2-year displacement warranty"]
        }
    },
    {
        "id": "78a149af-2c4c-4f28-abca-7ae6126a647a",
        "name": "Wall Waterproofing",
        "category": "3. Painting, Waterproofing & Home Improvement",
        "subcategory": "Waterproofing & Grouting",
        "price": 2999.0,
        "duration_minutes": 480,
        "description": "Comprehensive interior and exterior wall dampness eradication and barrier treatment (up to ~150 sq.ft. wall area). Targets rising damp, peeling wall baseboards, bubbling plaster, and efflorescence salt blooms. Features chipping affected plaster down to masonry, applying anti-salpetre chemical neutralizer wash, dual-coat penetrative crystalline polymer waterproofing barrier, and skimming with water-resistant acrylic polymer putty ready for painting.",
        "highlights": [
            "Complete wall dampness and efflorescence eradication for up to 150 sq.ft.",
            "Permanent barrier against rising damp, baseboard seepage, and external moisture",
            "Chemical anti-salpetre wash neutralizing corrosive salt crystals in brickwork",
            "Dual-coat penetrative crystalline polymer waterproof membrane application",
            "Water-resistant polymer putty skim creating a smooth, paint-ready surface"
        ],
        "included": [
            "Waterproofing treatment for interior or exterior damp walls (up to 150 sq.ft.)",
            "Floor masking with heavy-duty drop cloths along the treatment perimeter",
            "Chipping blistered paint, crumbly plaster, and salt-damaged mortar down to bare masonry",
            "Mechanical wire brushing to remove efflorescence crystals from brick/block joints",
            "Application of anti-salpetre chemical wash to neutralize subsurface mineral salts",
            "2 full coats of penetrative crystalline acrylic polymer waterproof barrier",
            "Skimming with water-resistant polymer putty to restore a smooth wall finish",
            "Site cleanup, plaster debris disposal, and post-cure painting guidelines"
        ],
        "excluded": [
            "Decorative final painting (recommended after 7 days of moisture evaporation)",
            "Structural reconstruction of cracked or sunken load-bearing foundations",
            "Fixing actively leaking concealed plumbing pipes (plumbing repair must precede)",
            "External facade waterproofing above 3 floors requiring specialized cradle rigs",
            "Treating horizontal roof slabs (covered under Terrace Waterproofing)"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Moisture Profiling & Area Masking",
                "description": "Digital moisture meters delineate the damp zone boundaries; surrounding floors and switches are masked.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Chipping Damaged Plaster",
                "description": "Bubbling paint, hollow plaster, and salt-rotted mortar are chipped away with masonry chisels down to bare brickwork.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Wire Brushing & Anti-Salpetre Wash",
                "description": "Exposed masonry is wire-brushed; an anti-efflorescence chemical wash is applied to neutralize subsurface salt crystals.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "First Crystalline Polymer Barrier Coat",
                "description": "Deep-penetrating acrylic crystalline polymer slurry is brushed deeply into open brick and mortar pores.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Second Waterproof Polymer Membrane Coat",
                "description": "After a 4-hour cure, the second heavy coat is applied perpendicular to form an unbroken moisture-barrier shield.",
                "is_key_step": True
            },
            {
                "step_number": 6,
                "title": "Water-Resistant Polymer Putty Skim",
                "description": "The treated zone is skimmed flush with surrounding walls using waterproof polymer putty, creating a smooth finish.",
                "is_key_step": False
            },
            {
                "step_number": 7,
                "title": "Site Cleanup & Curing Handover",
                "description": "Chipped debris is bagged and cleared, work area is swept, and advice on drying time before painting is provided.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital pinless moisture meter and masonry inspection tools",
            "Masonry chisels, rotary chipping hammers, and heavy wire scratch brushes",
            "Heavy-duty floor protective tarpaulins and debris collection bags",
            "Anti-salpetre efflorescence neutralizing chemical solution",
            "Deep-penetrating crystalline acrylic waterproofing polymer slurry",
            "Water-resistant polymer-modified wall putty and stainless steel trowels"
        ],
        "customer_setup": [
            "Move furniture at least 4 feet away from the damp wall to provide clear workspace.",
            "Remove baseboards, electrical outlet faceplates, or wall hangings in the affected zone.",
            "Allow access to running water and electricity for mixing polymer mortars."
        ],
        "aftercare": [
            "Allow the polymer barrier and putty skim to cure undisturbed for 48 hours.",
            "Wait 7 to 10 days for residual wall moisture to evaporate before applying final decorative paint.",
            "Avoid drilling anchors directly into the newly waterproofed barrier zone without silicone sealant."
        ],
        "expected_results": [
            "Complete elimination of bubbling paint, crumbling plaster, and musty damp odors.",
            "Impenetrable crystalline barrier blocking capillary moisture and salt efflorescence migration.",
            "Smooth, stable, water-resistant wall surface ready for long-lasting decorative painting."
        ],
        "important_notes": [
            "Covers up to 150 sq.ft. of wall surface area (sufficient for 1 to 2 damp walls).",
            "Residual moisture already trapped inside deep brickwork needs 7 to 10 days of normal airflow to fully dry before topcoat painting."
        ],
        "warranty": "2-year SmartServe warranty against moisture breakthrough and dampness recurrence on treated wall sections.",
        "faqs": [
            {
                "question": "Why does paint keep peeling and bubbling on my lower walls?",
                "answer": "This is typically caused by rising damp or capillary moisture migration from soil, foundation slabs, or adjacent wet areas. Water dissolves minerals and forces paint off the wall. Our crystalline polymer treatment stops moisture from ever reaching the surface."
            },
            {
                "question": "Do you chip the wall all the way to the brick?",
                "answer": "Yes. Chipping away salt-saturated, hollow plaster is necessary because waterproofing chemicals must penetrate directly into the bare masonry pores to form an effective barrier."
            },
            {
                "question": "Can I paint the wall immediately after waterproofing?",
                "answer": "We recommend waiting 7 to 10 days after waterproofing. While the moisture barrier is formed immediately, trapped moisture within the brickwork needs time to evaporate before primer and paint are applied."
            },
            {
                "question": "Will the white powder (efflorescence) come back?",
                "answer": "No. Our treatment includes an anti-salpetre chemical wash that neutralizes salt crystals, followed by crystalline polymers that permanently seal the pores through which salts migrate."
            },
            {
                "question": "How long does wall waterproofing take?",
                "answer": "A standard wall waterproofing project up to 150 sq.ft. takes approximately 6 to 8 hours to complete."
            }
        ],
        "dos": [
            "Do keep the room well-ventilated with open windows after treatment to help residual moisture evaporate.",
            "Do inspect the outer side of exterior damp walls to ensure garden sprinklers are not spraying directly onto masonry.",
            "Do wait the recommended 7-10 days before final painting for best results."
        ],
        "donts": [
            "Don't apply quick-fix paint directly over bubbling plaster without chipping and chemical barrier treatment.",
            "Don't push cupboards or heavy beds flush against damp walls; allow at least 2 inches for air circulation.",
            "Don't wash or wet the newly skimmed polymer putty during the first 48 hours."
        ],
        "tips": [
            "Ensuring at least 2 inches of air gap between wardrobes and exterior walls prevents condensation dampness and mold growth."
        ],
        "service_features": [
            {"title": "Crystalline Polymer Barrier", "description": "Deep-penetrating crystals sealing microscopic pores inside masonry"},
            {"title": "Anti-Efflorescence Neutralizer", "description": "Eliminates white salt bloom powder and halts plaster decay"},
            {"title": "2-Year Wall Warranty", "description": "Guaranteed protection against dampness recurrence and paint bubbling"}
        ],
        "service_media": [
            {
                "url": "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?auto=format&fit=crop&w=800&q=80",
                "type": "image",
                "title": "Wall Waterproofing"
            }
        ],
        "seo_metadata": {
            "keywords": ["wall waterproofing", "rising damp treatment", "stop wall dampness", "efflorescence treatment", "damp wall repair"],
            "seo_title": "Wall Waterproofing Services | Stop Rising Damp & Peeling Plaster",
            "seo_description": "Permanently cure damp walls, bubbling paint, and white efflorescence salts. Chipping, crystalline polymer barrier, and 2-year warranty.",
            "highlights": ["Crystalline polymer barrier", "Anti-efflorescence neutralizer", "2-year wall warranty"]
        }
    }
]

ALL_CATEGORY3_SERVICES = HOME_IMPROVEMENT_SERVICES + HOME_PAINTING_SERVICES + SPECIALIZED_PAINTING_SERVICES + WATERPROOFING_GROUTING_SERVICES
