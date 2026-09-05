# Home Electronics & Laundry Services Data (17 Services)
# Category: 4. AC, Appliance & Electronics Repair

HOME_ELECTRONICS_SERVICES = [
    # --- SUBCATEGORY: Air Cooler (3 Services) ---
    {
        "id": "3fc277a3-4be5-470d-add6-6581dc34933b",
        "name": "Cooler Repair",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Air Cooler",
        "price": 469.0,
        "description": "Expert diagnostic and component repair for desert, personal, and tower air coolers including submersible water pump failure, fan motor humming or jamming, swing louvre motor breakdown, wiring faults, and body water leakage.",
        "highlights": [
            "Submersible magnetic water pump diagnostic, impeller de-scaling, or replacement",
            "Heavy-duty copper-wound fan motor capacitor and bushing bearing inspection",
            "Oscillating synchronous swing motor and louvre linkage gear repair",
            "Rotary speed switch and electronic remote PCB circuit troubleshooting",
            "Water tank crack sealing and float valve overflow prevention"
        ],
        "included": [
            "Complete electrical motor and pump diagnostic inspection",
            "Fan motor starting capacitor test and replacement check",
            "Submersible water pump flow pressure test",
            "Oscillation swing louvre linkage alignment",
            "Wiring terminal check and earthing shock safety inspection",
            "Water distribution pipe unclogging and nozzle clearing",
            "Post-repair continuous cooling airflow run test"
        ],
        "excluded": [
            "Cost of replacement water pump, fan motor, or honeycomb cooling pads",
            "Complete plastic tank replacement due to catastrophic structural damage",
            "Ducting fabrication for window-fitted desert coolers"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Symptom Diagnosis & Electrical Safety",
                "description": "Technician tests power supply, checks for current leakage on metal/plastic body, and isolates pump vs fan motor issues.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Pump & Water Distribution Audit",
                "description": "Submersible pump is tested for impeller lock or burned coils; top water distribution channels are checked for scale blockages.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Fan Motor & Capacitor Testing",
                "description": "Fan motor shaft is checked for free spin, sleeve bearing wear, and capacitor capacitance microfarads.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Defective Component Replacement",
                "description": "Faulty pump, capacitor, swing motor, or speed switch is replaced with high-durability compatible parts.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Flow Verification & Handover",
                "description": "Cooler tank is filled; uniform water cascade across pads and powerful fan airflow are demonstrated.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital true-RMS multimeter and capacitance tester",
            "Submersible pump flow testing kit",
            "Motor shaft lubricant and bearing alignment tools",
            "Waterproof silicone sealant",
            "Insulated electrical screwdriver set"
        ],
        "customer_setup": [
            "Provide access to the air cooler and an electrical power point",
            "Have running tap water available to fill the tank for testing",
            "Describe the fault clearly (e.g. pump not pumping water, fan humming, water shock)"
        ],
        "aftercare": [
            "Never run the submersible pump with an empty water tank (causes instant coil burnout)",
            "Lubricate fan motor oiling ports with a few drops of machine oil once a month",
            "Drain tank water completely once a week to prevent mosquito breeding and mineral scaling"
        ],
        "expected_results": [
            "Smooth, powerful airflow with uniform cooling pad saturation",
            "Quiet, vibration-free fan rotation without annoying metallic screeching",
            "Safe electrical operation free from shock risks"
        ],
        "important_notes": [
            "Submersible water pumps cannot be repaired if windings are burnt; replacement is standard practice",
            "Hard water scaling can choke water pumps within a single season if not descaled"
        ],
        "warranty": "30-day SmartServe warranty on repair labor and installed components",
        "faqs": [
            {
                "question": "Why is the cooler fan humming loudly but not spinning?",
                "answer": "A humming fan indicates a blown run capacitor or seized motor sleeve bearings due to lack of lubrication. Replacing the capacitor and lubricating the shaft usually fixes it."
            },
            {
                "question": "Why is my air cooler blowing hot air even with the pump turned on?",
                "answer": "This happens when the submersible pump fails to lift water, or when the top water distributor channels are choked with hard water limescale."
            },
            {
                "question": "Can the technician replace worn-out honeycomb pads?",
                "answer": "Yes, high-density honeycomb cooling pad replacement is available as an add-on service."
            },
            {
                "question": "How long does cooler repair take?",
                "answer": "Standard diagnostic and part replacement take approximately 30 to 45 minutes."
            }
        ],
        "dos": [
            "Always turn off the pump switch when the water level is low",
            "Ensure the cooler has access to fresh outdoor air for proper evaporative cooling"
        ],
        "donts": [
            "Never operate the cooler in a completely sealed room with doors and windows closed (causes extreme humidity)",
            "Do not touch electrical switches with wet hands"
        ],
        "tips": [
            "Keep an opposite window open in the room to allow humid air to escape, maximizing evaporative cooling breeze"
        ]
    },
    {
        "id": "6e9d866e-68f0-4ab3-a022-711b2167f2f9",
        "name": "Cooler Service",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Air Cooler",
        "price": 499.0,
        "description": "Comprehensive pre-summer and post-season maintenance for air coolers including water tank de-sludging and sanitization, cooling pad descaling, water distribution channel unclogging, fan motor bearing lubrication, and electrical safety audit.",
        "highlights": [
            "Complete water tank high-pressure flushing, limescale scraping, and anti-mosquito sanitization",
            "Cooling pad (honeycomb/wood-wool) chemical descaling and airflow clearing",
            "Submersible pump impeller disassembly, cleaning, and flow rate calibration",
            "Fan motor front and rear bearing oiling and blade static balance check",
            "Top distribution manifold needle-clearing to ensure 100% uniform pad saturation"
        ],
        "included": [
            "Water reservoir tank draining, scrubbing, and chemical disinfection",
            "Cooling pad descaling with mild organic descaler to restore water absorption",
            "Submersible pump cleaning and intake filter clearing",
            "Fan motor lubrication with high-grade synthetic oil",
            "Fan blade alignment and balanced pitch verification",
            "Swing louvre gear inspection and free movement check",
            "Complete water cascade and airflow delivery test"
        ],
        "excluded": [
            "Cost of brand-new honeycomb cooling pads (if old pads are rotted)",
            "Replacement of burned pump motor or fan motor",
            "Fabrication of new external window sheet metal stands"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Tank Draining & Sludge Removal",
                "description": "Old standing water, algae, and mineral sediment in the bottom reservoir are drained and power-scrubbed clean.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Cooling Pad Descaling & Flush",
                "description": "Honeycomb or wood-wool pads are sprayed with descaling solution and pressure rinsed to reopen clogged air channels.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Submersible Pump & Pipe Servicing",
                "description": "Pump impeller is freed of lint and hair; top distribution manifold holes are cleared with a cleaning probe.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "Motor Lubrication & Electrical Check",
                "description": "Fan motor oil ports are lubricated; speed switch contacts and earthing ground wires are inspected.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Full Cascade Cooling Test",
                "description": "Fresh water is loaded; technician confirms even water curtain down all pads and clean, odorless cool breeze.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Portable low-pressure rinse sprayer",
            "Non-toxic citric acid cooling pad descaler",
            "Motor bearing synthetic lubricating oil",
            "Distribution pipe cleaning probe",
            "Scrubbing brushes and anti-microbial tank sanitizer"
        ],
        "customer_setup": [
            "Provide access to a garden hose or bathroom running water source",
            "Ensure electrical supply point is available",
            "Place cooler in an area where water can be drained freely"
        ],
        "aftercare": [
            "Drain and refill the water tank at least once a week during peak summer",
            "Add a few drops of citronella or neem oil to the water to repel mosquitoes naturally",
            "Store cooler dry with pads covered in breathable cloth during winter months"
        ],
        "expected_results": [
            "Crisp, refreshing, and completely odor-free cool air delivery",
            "Uniform water distribution across 100% of cooling pad surface area",
            "Smooth, whisper-quiet motor operation with optimized air throw"
        ],
        "important_notes": [
            "Rotted or crumbling wood-wool pads should be replaced rather than washed",
            "Proper ventilation is essential for evaporative coolers to reduce room temperature"
        ],
        "warranty": "30-day SmartServe service guarantee on cleaning quality and motor lubrication",
        "faqs": [
            {
                "question": "Why does my air cooler smell like wet grass or damp mold?",
                "answer": "Stagnant tank water and dirty cooling pads breed bacteria and algae. Deep descaling and tank sanitization eliminate this odor completely."
            },
            {
                "question": "How often should an air cooler be serviced?",
                "answer": "Air coolers should be thoroughly serviced twice a year: once before summer starts and once before winter storage."
            },
            {
                "question": "Can hard water scale on honeycomb pads be cleaned?",
                "answer": "Yes, our technicians treat honeycomb pads with specialized mild descalers that dissolve mineral crusts without damaging cellulose fibers."
            },
            {
                "question": "How long does air cooler servicing take?",
                "answer": "A full tank wash, pad descaling, and motor lubrication take approximately 40 to 50 minutes."
            }
        ],
        "dos": [
            "Keep the room well ventilated by keeping windows open when operating the cooler",
            "Clean the water tank regularly to keep the air fresh and healthy"
        ],
        "donts": [
            "Do not allow mineral sludge to sit in the tank over the winter months",
            "Do not spray water directly into the open motor vents"
        ],
        "tips": [
            "Add ice cubes to the top ice chamber during extreme heat waves for an instant blast of freezing air"
        ]
    },
    {
        "id": "56da76e5-940e-4166-8230-882c2221adc0",
        "name": "Installation",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Air Cooler",
        "price": 499.0,
        "description": "Professional assembly, window placement, or heavy metal stand mounting for portable and desert air coolers including duct sealing, water overflow drain pipe fitting, electrical earthing safety check, and airflow orientation.",
        "highlights": [
            "Secure window frame positioning or exterior heavy-duty metal stand mounting",
            "Weatherproof seal installation around window openings to block rain and hot air drafts",
            "Auto-fill float valve plumbing connection to cold water supply line",
            "Heavy-duty castors/wheels assembly for portable room coolers",
            "Electrical line load and 16A grounding safety verification"
        ],
        "included": [
            "Unboxing and assembly of cooler body, wheels, and cooling pads",
            "Window sill positioning or mounting on existing exterior iron stand",
            "Weather-stripping tape sealing around window gaps",
            "Float ball valve connection to water inlet hose (if auto-fill equipped)",
            "Water overflow pipe connection and routing",
            "Electrical plug, cable, and earthing continuity test",
            "Initial tank fill, pump priming, and airflow demonstration"
        ],
        "excluded": [
            "Fabrication of new welded exterior metal iron stands",
            "Masonry brick cutting or window grill alteration work",
            "New dedicated electrical wiring from switchboard"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Site Inspection & Airflow Planning",
                "description": "Technician evaluates window opening, checks exterior stand stability, and plans cross-ventilation path.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Cooler Assembly & Stand Mounting",
                "description": "Castor wheels or rubber pads are fitted; cooler is securely positioned on window sill or exterior metal frame.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Window Weather-Sealing",
                "description": "Side foam panels and weather-stripping are fitted to seal air gaps around the window frame.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Water Inlet & Overflow Hookup",
                "description": "Flexible water line is connected to auto-fill valve; overflow drain tube is directed safely away from wall.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Power-Up & Performance Demo",
                "description": "Tank is filled; pump and fan speeds are tested, confirming powerful cross-ventilation air throw.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Heavy-duty adjustable wrench and screwdriver set",
            "High-density weather-stripping foam tape",
            "Digital electrical socket and earthing tester",
            "Water hose connection clamps and Teflon tape",
            "Spirit bubble level"
        ],
        "customer_setup": [
            "Have new air cooler unboxed or keep original box in the room",
            "Ensure an exterior iron stand or suitable window frame is ready",
            "Provide water supply hose and grounded electrical power point"
        ],
        "aftercare": [
            "Check that window weather-stripping remains sealed against summer dust storms",
            "Ensure the overflow drain tube does not drip onto neighboring balconies",
            "Operate cooler with open cross-ventilation in the room"
        ],
        "expected_results": [
            "Sturdy, vibration-free cooler mounting that will not shift under high wind",
            "Airtight window sealing preventing hot drafts and insects from entering",
            "Effortless automated water filling without manual bucket refilling"
        ],
        "important_notes": [
            "Exterior window stands must be structurally sound and rust-free to prevent accidental falls",
            "Large desert coolers filled with water weigh over 60-80 kg; structural support is critical"
        ],
        "warranty": "60-day SmartServe installation warranty covering mounting stability and weather sealing",
        "faqs": [
            {
                "question": "Can a desert cooler be installed in a standard window?",
                "answer": "Yes, provided the window sill has adequate depth or an external iron support bracket is installed to support the weight of the water-filled cooler."
            },
            {
                "question": "What is auto-fill and how does it work?",
                "answer": "An auto-fill valve connects your cooler to a continuous water tap, automatically topping up the reservoir when water drops, eliminating manual bucket filling."
            },
            {
                "question": "Does installation include fabricating a new window iron frame?",
                "answer": "No, metal fabrication or welding of external iron frames is a specialized carpentry/welding service not included in standard installation."
            },
            {
                "question": "How long does cooler installation take?",
                "answer": "Standard unboxing, window positioning, and weather-sealing take approximately 40 to 60 minutes."
            }
        ],
        "dos": [
            "Ensure strong cross-ventilation by keeping a door or window open in the room",
            "Verify that the electrical socket has a certified earth connection"
        ],
        "donts": [
            "Do not mount a heavy desert cooler on loose or rusted window brackets",
            "Do not allow overflow water to splash against building exterior walls"
        ],
        "tips": [
            "Position the cooler on the shaded side of your home for cooler intake air"
        ]
    },

    # --- SUBCATEGORY: Geyser (4 Services) ---
    {
        "id": "3cf9a3b2-75bf-4eaf-a259-807b63997858",
        "name": "Geyser Repair",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Geyser",
        "price": 439.0,
        "description": "Expert diagnostic and component repair for storage and instant water heaters (geysers) including electric shock risks, water leaking from tank bottom, dripping pressure release valve (PRV), blown thermostat, and burnt heating element.",
        "highlights": [
            "Dual safety thermostat and thermal cutout (TCO) trip reset and calibration",
            "High-wattage copper / incoloy heating element continuity and resistance testing",
            "Multi-function safety valve (MFV) pressure relief and non-return valve check",
            "Electric shock and earth leakage current detection on bathroom pipework",
            "Internal tank flange gasket replacement to eliminate bottom water leakage"
        ],
        "included": [
            "Comprehensive electrical safety and hydraulic diagnostic inspection",
            "Heating element ohms resistance and ground insulation test",
            "Thermostat and safety thermal cutout testing",
            "Pressure release valve (PRV) testing for continuous dripping",
            "Flange gasket leak identification and seal replacement",
            "Inlet and outlet flexible connection hose inspection",
            "Post-repair full tank heating cycle test"
        ],
        "excluded": [
            "Cost of replacement heating element, thermostat, or safety valve",
            "Internal enamel glassline tank welding if inner tank has rusted through",
            "Bathroom concealed plumbing or tile replacement"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Safety Isolation & Earth Leakage Audit",
                "description": "Technician tests bathroom pipes and geyser body with multimeter to ensure zero dangerous electrical current leakage.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Thermostat & Thermal Cutout Probing",
                "description": "Thermostat continuity and temperature dial cutoff are tested; manual thermal cutoff reset button is checked.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Heating Element Insulation Test",
                "description": "Heating element terminals are metered for open circuits or grounded sheath breakdown that trips the household ELCB/MCB.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Component Replacement & Tank Sealing",
                "description": "Faulty thermostat, element, or safety valve is replaced; new rubber flange gasket is torqued securely.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Tank Refill & Hot Water Test",
                "description": "Tank is completely filled with water before powering on; rapid temperature rise and auto-cutoff are confirmed.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "True-RMS digital multimeter with megger insulation test",
            "Immersion heating element box spanner socket",
            "Pipe wrenches and Teflon sealing tape",
            "Universal replacement thermostats and safety thermal cutouts",
            "Food-grade heat-resistant flange rubber gaskets"
        ],
        "customer_setup": [
            "Turn off electric power switch to the geyser before technician arrives",
            "Ensure cold water supply to the bathroom is running",
            "Keep the bathroom floor dry and clear of toiletries directly beneath geyser"
        ],
        "aftercare": [
            "Never turn on geyser power if water supply is cut off (burns heating element in seconds)",
            "Set thermostat to 55-60°C to prevent excessive scale formation and conserve electricity",
            "Have sacrificial magnesium anode rod replaced every 2 years to stop tank corrosion"
        ],
        "expected_results": [
            "Immediate restoration of fast, scalding-hot water supply",
            "100% electrical safety with zero risk of bathroom shocks",
            "Complete elimination of tank leaks and dripping valves"
        ],
        "important_notes": [
            "If the inner steel tank has rusted through and cracked, replacement of the entire geyser is required",
            "Power must NEVER be turned on while the geyser tank is empty (dry heating hazard)"
        ],
        "warranty": "30-day SmartServe warranty on repair labor and installed replacement parts",
        "faqs": [
            {
                "question": "Why does my geyser trip the MCB / ELCB as soon as I switch it on?",
                "answer": "This happens when the outer copper or incoloy sheath of the heating element splits, allowing water to touch the live coil and creating a direct electrical earth leakage fault."
            },
            {
                "question": "Why is water continuously dripping from the small valve on the cold water pipe?",
                "answer": "That is the Multi-Function Safety Valve (MFV). Minor dripping during heating is normal as water expands. Continuous heavy dripping indicates high incoming water pressure or a failed valve."
            },
            {
                "question": "Can an instant geyser be repaired on-site?",
                "answer": "Yes, instant geysers follow similar heating element, thermostat, and microswitch principles and are repaired on-site."
            },
            {
                "question": "How long does geyser repair take?",
                "answer": "Standard diagnostic and element/thermostat replacement take approximately 40 to 60 minutes."
            }
        ],
        "dos": [
            "Turn off the geyser power switch after your bath to save power and extend element life",
            "Ensure the bathroom geyser circuit is protected by an ELCB / RCCB breaker"
        ],
        "donts": [
            "Never switch on the geyser without confirming water is flowing from the hot tap first",
            "Do not plug a geyser into a 5A light socket; always use a dedicated 16A industrial socket"
        ],
        "tips": [
            "Keep thermostat set around 55°C: heating water beyond 60°C accelerates limescale buildup by 300%"
        ]
    },
    {
        "id": "89a2501e-c463-4ca2-ad84-46b8b59da262",
        "name": "Geyser Service",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Geyser",
        "price": 499.0,
        "description": "Comprehensive annual preventative maintenance and descaling service for storage geysers including tank draining, heating element mineral descaling, magnesium anode rod inspection, pressure safety valve flush, and thermostat calibration.",
        "highlights": [
            "Complete geyser tank draining and hard-water white limescale sediment purge",
            "Heavy heating element chemical immersion descaling to restore fast heat transfer",
            "Sacrificial magnesium anode rod corrosion inspection (prevents tank rusting)",
            "Multi-function pressure safety valve flushing and anti-stick test",
            "Electrical terminal tightening and earthing safety verification"
        ],
        "included": [
            "Isolating power and draining internal storage tank",
            "Heating element assembly removal and mechanical/chemical descaling",
            "Internal tank sediment wash-out and limescale extraction",
            "Magnesium anode rod health check and replacement recommendation",
            "Thermostat dial calibration and high-temperature cutoff test",
            "Safety relief valve flush to prevent mineral sticking",
            "Refilling, pressure testing, and heating verification"
        ],
        "excluded": [
            "Cost of replacement magnesium anode rod or new heating element",
            "Replacement of rusted inlet/outlet braided connection hoses",
            "Concealed bathroom plumbing repairs"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Power Disconnect & Full Tank Drainage",
                "description": "Geyser is isolated from mains, water supply valve shut, and internal tank completely drained into collection bucket.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Heating Element Flange Removal",
                "description": "Bottom electrical cover and mounting flange bolts are unscrewed; scaled heating element is carefully extracted.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Immersion Descaling & Sediment Purge",
                "description": "Heating element is soaked in descaling solution to dissolve rock-hard calcium carbonate; tank interior is flushed clean of sediment.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Anode Rod Check & Reassembly",
                "description": "Magnesium anode is inspected; new flange seal gasket is installed and flange bolts torqued in cross pattern.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Tank Refill & Performance Validation",
                "description": "Tank is filled until water flows freely from hot tap; power is restored, and rapid water heating is demonstrated.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Heavy-duty immersion element box socket wrench",
            "Citric-acid food-safe limescale descaling solution",
            "Internal tank flushing hose and siphon bucket",
            "Digital true-RMS multimeter and thermometer",
            "High-temperature EPDM flange replacement gasket"
        ],
        "customer_setup": [
            "Turn off geyser electrical switch at least 2 hours before service so water is not boiling hot",
            "Ensure bathroom cold water supply is functioning",
            "Clear bathroom items underneath the geyser"
        ],
        "aftercare": [
            "Allow water to run for 1 minute from hot tap to clear any minor sediment before first bath",
            "Operate geyser at 55°C to minimize future limescale precipitation",
            "Schedule annual descaling in areas with hard water (TDS > 400)"
        ],
        "expected_results": [
            "Up to 30% faster water heating time through direct element-to-water heat transfer",
            "Substantial reduction in electricity bills by eliminating the insulating scale blanket",
            "Extended inner tank lifespan and prevention of premature tank rust-through"
        ],
        "important_notes": [
            "Hard water limescale acts as a thermal insulator; 3mm of scale increases electricity consumption by over 20%",
            "Does not include cost of new anode rod if existing rod is completely dissolved"
        ],
        "warranty": "30-day SmartServe service guarantee on descaling quality and leak-free flange seals",
        "faqs": [
            {
                "question": "Why does my geyser make a loud boiling or hissing kettle sound when heating?",
                "answer": "This kettle sound indicates a thick crust of hard-water limescale wrapped around the heating element. As water gets trapped beneath the scale, it boils into micro-steam pockets. Descaling fixes it."
            },
            {
                "question": "What is a magnesium anode rod and why is it important?",
                "answer": "The magnesium anode is a sacrificial metal rod inside the tank. It corrodes itself to protect the steel tank from rusting. It must be checked and replaced periodically."
            },
            {
                "question": "How often should a geyser be descaled?",
                "answer": "In hard water borewell areas, annual descaling is strongly recommended. In municipal soft water areas, once every 2 years is sufficient."
            },
            {
                "question": "How long does a complete geyser servicing take?",
                "answer": "Draining, element removal, acid descaling, sediment flushing, and refilling take approximately 50 to 65 minutes."
            }
        ],
        "dos": [
            "Service your geyser before the winter season begins for reliable daily hot water",
            "Ensure the cold water inlet tap remains fully open during use"
        ],
        "donts": [
            "Never attempt to remove the heating element while the geyser is full of scalding water",
            "Do not hammer the heating element with tools to chip off scale (punctures copper sheath)"
        ],
        "tips": [
            "Installing a simple polyphosphate water softener cartridge on the geyser inlet line reduces limescale by up to 70%"
        ]
    },
    {
        "id": "6440c245-da38-42e7-a8a9-8e8431e5b7e2",
        "name": "Heating Problem",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Geyser",
        "price": 499.0,
        "description": "Specialized diagnostic service targeting all water heating failures including geyser completely not heating, water remaining lukewarm despite hours of power, erratic temperature cutoff, or power indicator light on but zero hot water.",
        "highlights": [
            "Heating element open-circuit and resistance diagnostic (verifying approx 25-28 ohms for 2kW element)",
            "Dual-pole capillary thermostat temperature differential calibration",
            "Thermal overload cutout (TCO) trip verification and root cause isolation",
            "Supply voltage drop under load and 16A socket contact resistance check",
            "Cold water dip tube integrity check (ensuring cold water does not short-circuit to hot outlet)"
        ],
        "included": [
            "Comprehensive electrical circuit diagnosis under live load",
            "Heating element winding resistance and continuity test",
            "Thermostat switching and cutoff temperature test",
            "Manual reset thermal cutout inspection",
            "Power indicator lamps (red/green LED) circuit test",
            "Internal dip tube inspection to diagnose lukewarm water mixing",
            "Full heating cycle verification before handover"
        ],
        "excluded": [
            "Cost of replacement heating element, thermostat, or thermal cutoff",
            "Complete geyser replacement if tank has ruptured",
            "Electrical wiring extension or new circuit breaker installation"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Voltage & Current Load Test",
                "description": "Technician measures voltage at 16A wall socket and clamps ammeter around geyser cord to test if heating element is drawing current (target 8.5-9.0A).",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Thermostat & Thermal Cutout Inspection",
                "description": "Bottom panel is opened; technician checks if the safety thermal cutout has tripped or if thermostat contacts are pitted.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Heating Element Continuity Metering",
                "description": "Multimeter measures ohms across element terminals; open circuit (infinite ohms) indicates burnt element requiring replacement.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Component Replacement & Dip Tube Check",
                "description": "Defective electrical component is replaced with genuine OEM-rated part; internal plastic dip tube is checked for breakage.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Heating Verification & Thermostat Cutoff",
                "description": "Geyser runs for 15 minutes; technician verifies rapid temperature rise to 60°C and proper thermostat automatic cutoff.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital true-RMS clamp multimeter",
            "Immersion heating element wrench socket",
            "Infrared laser thermometer",
            "Terminal crimping tools and high-temperature fiberglass wiring",
            "OEM replacement thermostats and thermal cutouts"
        ],
        "customer_setup": [
            "Keep power switch on so technician can measure baseline current draw",
            "Ensure running water supply to bathroom is active",
            "Keep geyser purchase invoice accessible if unit is under warranty"
        ],
        "aftercare": [
            "Turn off geyser when leaving home for the day to avoid repeated dry cycling",
            "Keep thermostat set at 55-60°C for balanced heating speed and safety",
            "Contact SmartServe if the thermal cutout trips again"
        ],
        "expected_results": [
            "Immediate restoration of piping-hot water within 15-20 minutes",
            "Consistent automatic thermostat cutoff when target temperature is reached",
            "Energy-efficient heating with zero wasted electricity"
        ],
        "important_notes": [
            "If the power indicator lamp lights up but water never heats, the heating element or thermal cutout is almost certainly burned out",
            "Lukewarm water often indicates a broken internal dip tube that mixes incoming cold water directly into the hot outlet"
        ],
        "warranty": "30-day SmartServe warranty on heating repair labor and installed components",
        "faqs": [
            {
                "question": "Why does my geyser light turn on, but the water stays completely cold?",
                "answer": "The indicator lamp runs in parallel with the power circuit. A glowing light simply means electricity is reaching the geyser, but the heating element itself has burned out or the thermal cutout has tripped."
            },
            {
                "question": "Why is the hot water only lukewarm and runs out in 2 minutes?",
                "answer": "This is caused either by a broken internal cold water dip tube (causing cold water to siphon directly into the hot outlet) or extreme limescale coating the element."
            },
            {
                "question": "Can a tripped geyser thermal cutout be reset?",
                "answer": "Yes, thermal cutouts have a small red manual reset button. However, our technician must first diagnose why it overheated (usually a failed primary thermostat) to prevent dangerous re-tripping."
            },
            {
                "question": "How long does a heating problem repair take?",
                "answer": "Diagnostic testing and part replacement typically take 35 to 50 minutes."
            }
        ],
        "dos": [
            "Ensure the hot water tap is opened until a steady stream flows before turning on the power switch",
            "Keep the geyser electrical plug clean and free of bathroom moisture"
        ],
        "donts": [
            "Never bypass the safety thermal cutout with a direct wire (severe tank burst hazard)",
            "Do not set thermostat to maximum 75°C (creates dangerous scalding risks)"
        ],
        "tips": [
            "A 2000W geyser should heat a 15-liter tank from 20°C to 55°C in roughly 20 to 25 minutes"
        ]
    },
    {
        "id": "8c76bbb8-0e2e-4d4e-8683-faa8b06050fd",
        "name": "Installation",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Geyser",
        "price": 499.0,
        "description": "Professional wall mounting and plumbing installation for storage and instant water heaters including heavy masonry anchor drilling, Multi-Function Safety Valve (MFV) fitting, braided connection pipe hookup, and complete pressure leak testing.",
        "highlights": [
            "Heavy-duty steel expansion anchor bolt drilling tested for full tank weight (up to 45 kg)",
            "Multi-Function Safety Valve (MFV / PRV) installation on cold water inlet line",
            "Stainless steel braided flexible connection pipe fitting with leak-free Teflon seals",
            "Electrical plug connection and 16A grounding circuit continuity verification",
            "Complete water fill, air purge, and initial heating cycle demonstration"
        ],
        "included": [
            "Unboxing and inspection of new geyser unit, brackets, and accessories",
            "Wall template marking and heavy-duty expansion anchor drilling into masonry wall",
            "Geyser secure wall mounting and level verification",
            "Multi-function safety valve installation on inlet port",
            "Connection of cold inlet and hot outlet flexible connection pipes",
            "Tank water filling and complete internal air bleed through hot tap",
            "Initial heating test to verify thermostat cutoff and zero water leakage"
        ],
        "excluded": [
            "Cost of braided stainless steel connection pipes or brass nipple fittings (available as add-ons)",
            "Dedicated 16A electrical socket wiring or circuit breaker installation",
            "Tile drilling on fragile hollow drywall or partition board"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Site Inspection & Structural Weight Audit",
                "description": "Technician checks wall load-bearing capacity (solid brick or concrete required for 15-25L storage geysers) and marks anchor holes.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Heavy-Duty Expansion Anchor Drilling",
                "description": "Masonry holes are drilled with rotary hammer; heavy steel expansion anchor bolts are hammered and torqued into position.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Geyser Mounting & Leveling",
                "description": "Geyser is mounted on the anchor bolts, verified for zero wobble, and locked in position with lock nuts.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Safety Valve & Plumbing Pipe Connection",
                "description": "Multi-function safety valve is fitted with Teflon tape; stainless braided hoses are connected to cold and hot plumbing points.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Tank Priming & Heating Handover",
                "description": "Water is run until hot tap flows continuously (bleeding all air); power is switched on and hot water heating is confirmed.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Heavy rotary hammer drill and 12mm masonry carbide bits",
            "Steel expansion anchor bolts (12mm heavy-gauge)",
            "Pipe wrenches, adjustable spanners, and Teflon sealing tape",
            "Digital electrical multimeter and socket tester",
            "Spirit bubble level"
        ],
        "customer_setup": [
            "Keep new geyser unboxed or carton present in the bathroom",
            "Verify cold water supply and a 16A grounded power outlet are nearby",
            "Ensure bathroom wall space is clear of towel racks or mirrors"
        ],
        "aftercare": [
            "Verify that hot tap water flows clear before daily shower use",
            "Periodically test the safety valve lever to ensure it doesn't seize from limescale",
            "Always keep the cold water inlet tap open when using the geyser"
        ],
        "expected_results": [
            "Rock-solid wall anchoring that securely supports the full weight of water (up to 45 kg)",
            "Completely leak-free plumbing connections with food-safe braided pipes",
            "Rapid hot water delivery with certified electrical grounding safety"
        ],
        "important_notes": [
            "Storage geysers MUST NEVER be mounted on hollow plasterboard, gypsum walls, or thin partition panels",
            "Tank must be 100% full of water before turning on electricity to prevent burning the element"
        ],
        "warranty": "60-day SmartServe installation warranty covering mounting stability and plumbing joints",
        "faqs": [
            {
                "question": "Can a 25-liter storage geyser be safely mounted on tiled bathroom walls?",
                "answer": "Yes. Our technicians drill through the tile into the solid brick or concrete masonry behind it, anchoring with 12mm steel expansion bolts rated for over 80 kg."
            },
            {
                "question": "What is the Multi-Function Safety Valve (MFV) and is it mandatory?",
                "answer": "Yes, the MFV is mandatory. It acts as a pressure relief valve, non-return valve (preventing tank emptying), and vacuum breaker to protect the tank from rupture."
            },
            {
                "question": "Are connection pipes included in the geyser box?",
                "answer": "Most manufacturers do not include braided connection pipes in the box. High-pressure stainless steel braided pipes are available from our technician as an add-on."
            },
            {
                "question": "How long does geyser installation take?",
                "answer": "Complete wall drilling, mounting, plumbing connection, and heating test take approximately 45 to 60 minutes."
            }
        ],
        "dos": [
            "Always ensure the inner tank is full of water before turning on electric power for the first time",
            "Use heavy-gauge stainless steel braided connection pipes rated for high hot-water temperatures"
        ],
        "donts": [
            "Never install a storage geyser without the Multi-Function Safety Valve",
            "Do not mount heavy geysers on hollow drywall or false walls"
        ],
        "tips": [
            "Keep the geyser installed as close to the shower/bath area as practical to minimize heat loss through piping"
        ]
    },

    # --- SUBCATEGORY: Television (5 Services) ---
    {
        "id": "76a036b6-8076-4b34-bd89-b69c4e402739",
        "name": "Screen / Display Issue",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Television",
        "price": 499.0,
        "description": "Expert diagnostic and component repair for LED, QLED, and OLED television display problems including black screen with sound, vertical/horizontal colored lines, flickering backlight, dim picture, distorted colors, and ghosting.",
        "highlights": [
            "Full LED backlight array (LED strip) voltage and individual diode luminance testing",
            "T-CON (Timing Controller) board and LVDS ribbon cable signal inspection",
            "COF (Chip-on-Film) bonding and panel gate driver voltage (VGH, VGL, VDD) audit",
            "OLED pixel burn-in / panel refresh calibration diagnostics",
            "Transparent repair feasibility assessment with zero false component replacement"
        ],
        "included": [
            "Thorough optical and electronic display symptom diagnosis",
            "LED backlight strip current and voltage driver testing",
            "T-CON board input/output differential signal probing",
            "LVDS ribbon cable cleaning, reseating, and pin continuity check",
            "Mainboard display processor output HDMI/LVDS signal test",
            "Detailed fault report and part replacement quotation"
        ],
        "excluded": [
            "Physical cracked or shattered LCD/OLED glass panel replacement (uneconomical)",
            "Cost of replacement LED backlight strips, T-CON board, or mainboard",
            "Wall remounting onto a different wall location"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Flashlight Test & Symptom Analysis",
                "description": "Technician performs optical flashlight test on dark screen; if faint images are visible, the fault is isolated to LED backlights.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Back Panel Removal & Voltage Probing",
                "description": "TV is placed on soft protective mat; power supply LED driver voltage and T-CON voltages (VGH, VGL, VCOM) are measured.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "LVDS Cable & T-CON Reseating",
                "description": "High-density ribbon cables are unlatched, contacts cleaned of oxidation with contact cleaner, and re-seated.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "Component Replacement / Backlight Repair",
                "description": "Defective LED backlight array strips, T-CON board, or power supply driver components are replaced with OEM parts.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Color Pattern Test & Handover",
                "description": "RGB calibration and high-definition video loops are run to confirm uniform brightness, vivid colors, and zero lines.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital true-RMS multimeter and LED backlight strip tester (0-300V auto-sensing)",
            "Anti-static work mat and suction cup panel handlers",
            "Electronic contact cleaner and lint-free swabs",
            "Precision magnetic screwdriver set",
            "RGB test pattern video generator"
        ],
        "customer_setup": [
            "Ensure a flat table, bed, or floor space is available to lay the TV face-down safely",
            "Keep TV remote control and power cable accessible",
            "Describe when the issue began (e.g. following lightning, physical impact, or gradual dimming)"
        ],
        "aftercare": [
            "Keep TV back panel away from direct sunlight and heat sources",
            "Lower picture backlight setting from 100% to 75-80% to double LED lifespan",
            "Avoid wiping the TV display with wet cloths or liquid window cleaners"
        ],
        "expected_results": [
            "Restoration of bright, vibrant, and uniform picture quality",
            "Elimination of annoying flickering, dark zones, or horizontal lines",
            "Crisp high-definition picture performance matching factory clarity"
        ],
        "important_notes": [
            "A physically cracked screen with visible internal spiderweb cracks cannot be repaired economically, as replacement panel costs exceed 80% of a new TV",
            "Sound present with dark screen is almost always a repairable LED backlight failure"
        ],
        "warranty": "30-day SmartServe warranty on display repair labor and installed components",
        "faqs": [
            {
                "question": "My TV has sound but no picture (black screen). Can it be fixed?",
                "answer": "Yes! This is the most common TV fault and is almost always caused by failed LED backlight strips behind the screen. Replacing the LED strips fully restores the picture."
            },
            {
                "question": "Can vertical colored lines on the screen be repaired?",
                "answer": "If lines are caused by loose T-CON ribbon cables or board failure, they can be fixed. If caused by damaged internal panel COF bonding tabs, panel replacement may be required."
            },
            {
                "question": "Can a cracked TV screen be repaired?",
                "answer": "No. When the internal LCD glass is physically cracked, the entire display panel must be replaced, which is rarely cost-effective compared to buying a new TV."
            },
            {
                "question": "How long does TV display diagnostics take?",
                "answer": "Screen diagnostics and electrical probing take approximately 35 to 50 minutes."
            }
        ],
        "dos": [
            "Use a dedicated surge protector to shield sensitive TV display electronics",
            "Turn off the TV when not in use to prolong backlight LED diode life"
        ],
        "donts": [
            "Never press hard against the delicate display screen with fingers or objects",
            "Never spray liquid glass cleaners directly onto the screen (seeps into bottom COF tabs)"
        ],
        "tips": [
            "Reduce the backlight level in your TV picture settings to 75% to extend the life of the LED backlights by years"
        ]
    },
    {
        "id": "7767b956-6075-4da2-a14a-43f5a1eabfb6",
        "name": "Software Troubleshooting",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Television",
        "price": 499.0,
        "description": "Expert software, operating system, and firmware recovery for Smart TVs (Android TV, Google TV, WebOS, Tizen, Fire OS) resolving boot loops, frozen logos, app crashing, Wi-Fi disconnection, Bluetooth unpairing, and sluggish performance.",
        "highlights": [
            "Smart TV OS recovery from boot loops and stuck brand logo screens",
            "Official OEM USB firmware flashing and partition recovery",
            "Wi-Fi and Bluetooth module signal re-binding and driver cache reset",
            "App store crashing, Netflix / YouTube playback, and DRM certificate fixes",
            "Complete factory reset, memory optimization, and customer app setup"
        ],
        "included": [
            "Operating system diagnostics and boot sequence error isolation",
            "OEM official firmware update via USB recovery mode",
            "Recovery menu wipe cache and master factory reset",
            "Wi-Fi network connection and DNS IP optimization",
            "Bluetooth remote control re-pairing and voice assistant setup",
            "Streaming app installation and playback smoothness verification",
            "Picture and audio software profile optimization"
        ],
        "excluded": [
            "Hardware repairs for physically burnt eMMC flash memory chips or mainboard processors",
            "Subscription fees for third-party streaming services (Netflix, Prime, Disney+)",
            "Wi-Fi router replacement or home broadband ISP repairs"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Boot Sequence & OS Diagnostic",
                "description": "Technician analyzes boot failure symptoms (stuck on Android logo, restarting continuously, apps freezing).",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Hardware Recovery Key Combo Entry",
                "description": "TV is booted into OEM Recovery Mode using physical service button key combinations.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Firmware Flashing / Cache Clear",
                "description": "Corrupt system cache is wiped; certified OEM firmware is flashed via high-speed USB if system files are damaged.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Network & Wireless Subsystem Setup",
                "description": "Wi-Fi 2.4GHz/5GHz bands are configured with optimized DNS; Bluetooth remote is re-paired and calibrated.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "App Verification & User Profile Handover",
                "description": "Major streaming apps are launched to verify 4K playback smoothness; customer is guided through new settings.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "High-speed USB drives with official OEM firmware repositories",
            "Service remote control with factory menu access keys",
            "Wi-Fi signal strength analyzer and network speed tester",
            "Universal Bluetooth / IR pairing test remote",
            "Anti-static technician tools"
        ],
        "customer_setup": [
            "Keep your home Wi-Fi network name and password ready",
            "Have your original TV remote control with fresh batteries",
            "Ensure stable uninterrupted power during firmware installation"
        ],
        "aftercare": [
            "Close background apps periodically to keep Smart TV memory free",
            "Always install official app updates via the certified Google Play or OEM App Store",
            "Do not disconnect power while a system update is installing"
        ],
        "expected_results": [
            "Snappy, lag-free Smart TV navigation and menu responsiveness",
            "Zero boot loops, frozen logos, or unexpected app crashes",
            "Stable, high-speed Wi-Fi streaming with zero buffering"
        ],
        "important_notes": [
            "Power MUST NEVER be interrupted while firmware is writing to avoid bricking the motherboard",
            "Factory reset erases locally stored personal app logins; have passwords ready"
        ],
        "warranty": "30-day SmartServe software and firmware stability guarantee",
        "faqs": [
            {
                "question": "Why is my Smart TV stuck on the brand logo screen?",
                "answer": "This is called a boot loop, caused by corrupted system files or an interrupted automatic update. Reflashing official OEM firmware via USB restores it completely."
            },
            {
                "question": "Why does my Smart TV constantly disconnect from Wi-Fi?",
                "answer": "This can be caused by corrupt network cache, outdated firmware, or loose internal Wi-Fi module cables. Software reset and driver re-binding resolve it."
            },
            {
                "question": "Will factory resetting my Smart TV delete my streaming accounts?",
                "answer": "Yes, a factory reset clears locally saved passwords. You will simply need to log back into Netflix, YouTube, or Prime Video after the service."
            },
            {
                "question": "How long does Smart TV software troubleshooting take?",
                "answer": "Firmware flashing, cache clearing, and app re-configuration take approximately 30 to 45 minutes."
            }
        ],
        "dos": [
            "Ensure regular firmware updates from the manufacturer settings menu",
            "Keep your home Wi-Fi router within reasonable distance of the TV"
        ],
        "donts": [
            "Never unplug the TV from the wall while a system update is progressing",
            "Do not install unauthorized third-party APKs from unknown web sources"
        ],
        "tips": [
            "Reboot your Smart TV once a week by holding the remote power button for 5 seconds to clear system RAM"
        ]
    },
    {
        "id": "fe8a859a-f877-49a6-951e-1880e4d1df6b",
        "name": "TV Installation",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Television",
        "price": 409.0,
        "description": "Comprehensive unboxing, table-top stand assembly or wall bracket mounting, leveling, peripheral device hookup (set-top box, soundbar, gaming console), cable management, and complete picture/audio calibration for LED, OLED, and QLED TVs.",
        "highlights": [
            "Unboxing and physical screen panel transit integrity inspection",
            "Table-top base pedestal stand assembly or wall mount positioning",
            "Precision laser-level alignment to eliminate awkward viewing angles",
            "Clean HDMI/Optical audio connection to set-top box, soundbar, and gaming consoles",
            "Complete Smart TV initial setup, Wi-Fi pairing, and remote configuration"
        ],
        "included": [
            "Careful unboxing and transit damage check",
            "Base stand assembly or wall bracket mounting (bracket provided by customer or add-on)",
            "Precision spirit level alignment",
            "Connecting HDMI cables to set-top box and home theater",
            "Initial power-up, language, and network Wi-Fi setup",
            "Audio/video output test across all connected inputs",
            "Customer demo of remote control, smart features, and voice control"
        ],
        "excluded": [
            "Cost of metal wall mount bracket (fixed, tilt, or swivel available as add-on)",
            "Concealed in-wall cable chasing or masonry civil conduit plastering",
            "Dedicated electrical socket installation behind the TV"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Unboxing & Screen Inspection",
                "description": "TV is unboxed carefully; screen panel, bezels, and accessories are inspected for transit cracks or defects.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Base Stand Assembly or Bracket Attachment",
                "description": "Table stands are assembled with anti-scratch screws, or VESA mounting plate is fastened to rear of TV.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Placement & Spirit Leveling",
                "description": "TV is placed on entertainment unit or mounted on wall; spirit bubble level verifies 100% horizontal alignment.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Peripheral Hookup & Cable Organization",
                "description": "HDMI cables from DTH set-top box, gaming console, and soundbar eARC are connected and organized neatly.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Smart TV Setup & Customer Demo",
                "description": "Wi-Fi is connected, display settings calibrated for ambient lighting, and remote features demonstrated.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Precision laser and spirit bubble levels",
            "Rotary hammer drill and masonry carbide drill bits",
            "Heavy-duty expansion anchor fasteners and VESA screws",
            "Velcro cable ties and spiral cable wraps",
            "Soft anti-scratch screen handling gloves"
        ],
        "customer_setup": [
            "Have brand-new TV carton in the room",
            "Provide wall bracket if pre-purchased (or select as add-on from technician)",
            "Ensure set-top box, soundbar, and functional power socket are available"
        ],
        "aftercare": [
            "Clean screen using only a dry, clean microfiber cloth",
            "Keep TV spaced at least 2 inches away from wall for ventilation",
            "Do not place candles or liquid items on the TV cabinet directly beneath the screen"
        ],
        "expected_results": [
            "Safe, rock-solid TV positioning with zero wobble or tilt",
            "Crisp, vivid picture and clear cinematic audio across all inputs",
            "Neat, orderly cable routing with zero tangled wire mess"
        ],
        "important_notes": [
            "Mounting on hollow partition walls or gypsum board requires specialized toggle bolts",
            "Wall mount bracket hardware must match the TV's VESA bolt pattern (e.g. 200x200, 400x400)"
        ],
        "warranty": "60-day SmartServe installation warranty covering mounting stability and alignment",
        "faqs": [
            {
                "question": "Is the wall mount bracket included in the installation price?",
                "answer": "No. The base price covers installation labor. If you do not have a bracket, our technician carries standard fixed, tilting, and swivel brackets as affordable add-ons."
            },
            {
                "question": "What is the recommended height for wall mounting a TV?",
                "answer": "For optimal ergonomics, the center of the TV screen should sit at eye level when seated on your sofa, typically 40 to 45 inches from floor to screen center."
            },
            {
                "question": "Can your technician connect my soundbar and gaming console?",
                "answer": "Yes! Connecting all your external devices (set-top box, soundbar, gaming console) and verifying audio/video is included."
            },
            {
                "question": "How long does TV installation take?",
                "answer": "Complete unboxing, mounting, cable setup, and smart demonstration take approximately 40 to 50 minutes."
            }
        ],
        "dos": [
            "Mount the TV at comfortable eye level to avoid neck strain",
            "Use high-speed certified HDMI 2.1 cables for 4K 120Hz gaming consoles"
        ],
        "donts": [
            "Never attempt to lift large 55\"+ TVs alone without a second person",
            "Do not pinch or bend optical audio cables at sharp 90-degree angles"
        ],
        "tips": [
            "Enable HDMI-CEC in settings so turning on your set-top box or gaming console automatically powers on the TV"
        ]
    },
    {
        "id": "145c8516-3756-467a-a328-f7db5a07ce7b",
        "name": "TV Repair",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Television",
        "price": 539.0,
        "description": "Comprehensive component-level and board-level repair for LED, LCD, OLED, and Smart TVs covering no power (dead TV), standby light blinking, no sound with normal picture, HDMI port failure, and motherboard restarts.",
        "highlights": [
            "Power supply board (SMPS) secondary DC voltage output and capacitor diagnostic",
            "Main motherboard processor, RAM, and eMMC storage troubleshooting",
            "Class-D audio amplifier IC and speaker cone distortion testing",
            "HDMI port ESD protection diode and handshake signal testing",
            "Genuine OEM replacement boards and components with upfront pricing"
        ],
        "included": [
            "Complete electrical, signal, and power supply diagnosis",
            "SMPS power board voltage rail verification (12V, 24V, 3.3V standby)",
            "Motherboard regulator IC and standby circuit testing",
            "Audio output speaker impedance and amplifier chip test",
            "HDMI, AV, and optical port connectivity check",
            "Component-level soldering repair or replacement recommendation",
            "Post-repair continuous burn-in load test"
        ],
        "excluded": [
            "Cracked or shattered internal LCD/OLED glass panel replacement",
            "Cost of replacement mainboard, power board, or speaker set",
            "External remote control physical replacement"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Symptom Diagnosis & Standby Light Analysis",
                "description": "Technician analyzes standby LED blink codes to identify whether fault is located in power board or mainboard.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Chassis Removal & Power Supply Probing",
                "description": "Back cover is removed on a soft mat; SMPS output rails (12V, 24V, standby 3.3V) are metered with digital multimeter.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Motherboard & Audio IC Diagnostic",
                "description": "Mainboard processor power-on signal, voltage regulators, and audio amplifier ICs are checked for failure.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Component Repair / Board Replacement",
                "description": "Blown capacitors, shorted diodes, audio speakers, or entire boards are repaired or replaced with genuine OEM units.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Load Test & Video Demonstration",
                "description": "TV runs under continuous high-definition video and full volume for 20 minutes to confirm total stability.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital true-RMS multimeter and oscilloscope probe",
            "Temperature-controlled micro-soldering station",
            "Audio signal generator and speaker impedance tester",
            "Anti-static wrist strap and foam workstation mat",
            "Assorted low-ESR electrolytic capacitors and fast-recovery diodes"
        ],
        "customer_setup": [
            "Ensure a table or flat surface is available to lay the TV down safely",
            "Keep TV power cord and original remote control handy",
            "Describe the exact failure pattern (e.g. heard pop sound, red light blinks 5 times)"
        ],
        "aftercare": [
            "Plug TV into a quality voltage stabilizer or surge-protected power strip",
            "Avoid turning off TV by pulling the wall plug directly while playing",
            "Ensure rear ventilation slots remain dust-free"
        ],
        "expected_results": [
            "Rapid diagnosis and restoration of dead or malfunctioning televisions",
            "Crisp, clear audio without buzzing, crackling, or distortion",
            "Stable, reliable power-on response without blinking error codes"
        ],
        "important_notes": [
            "Replacement circuit boards (SMPS or mainboards) are quoted transparently before installation",
            "Power surge damage from lightning strikes may require both power board and mainboard replacement"
        ],
        "warranty": "30-day SmartServe warranty on repair labor and installed components",
        "faqs": [
            {
                "question": "Why is my TV completely dead with no standby light showing?",
                "answer": "A completely dead TV indicates that the SMPS power supply board has failed, usually due to a blown primary fuse, shorted bridge rectifier, or power surge."
            },
            {
                "question": "Why does my TV red light blink several times when I press power, but the TV doesn't turn on?",
                "answer": "Blinking lights are diagnostic error codes indicating an internal protection shutdown, commonly caused by a failing power rail or inverter backlight error."
            },
            {
                "question": "Why is my TV picture perfect, but there is zero sound or crackling sound?",
                "answer": "This indicates failed internal speaker cones (paper tearing from high volume) or a shorted Class-D audio amplifier IC on the motherboard."
            },
            {
                "question": "How long does a TV repair take?",
                "answer": "Diagnostics and standard component/board replacement take approximately 45 to 65 minutes."
            }
        ],
        "dos": [
            "Use a surge protector to shield delicate microprocessors from power line voltage spikes",
            "Keep external devices connected to the same grounding circuit as the TV"
        ],
        "donts": [
            "Never open the TV back cover while plugged into mains power (high voltage shock hazard)",
            "Do not keep TV volume at maximum 100% continuously (tears speaker cones)"
        ],
        "tips": [
            "Count how many times your TV's red standby light blinks in sequence; this error code helps technicians pinpoint the faulty circuit instantly"
        ]
    },
    {
        "id": "e5ff70a8-26b5-4b1f-bb8b-8cc69e6db5cf",
        "name": "Wall Mounting",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Television",
        "price": 499.0,
        "description": "Specialized heavy-duty wall bracket mounting service for 32-inch to 85-inch LED, OLED, and curved televisions including masonry expansion anchor bolting, VESA bracket alignment, spirit-level calibration, and load testing.",
        "highlights": [
            "Heavy-gauge steel bracket installation rated for up to 60 kg holding capacity",
            "Precision laser-level alignment to guarantee perfectly level screen viewing",
            "VESA pattern matching (100x100 up to 600x400) with correct thread pitch bolts",
            "Support for fixed, 15-degree tilt, and full-motion articulating swivel brackets",
            "Clean masonry drilling with dust containment and zero wall tile cracking"
        ],
        "included": [
            "Wall assessment and optimal viewing height consultation",
            "VESA bracket attachment to the rear of the television",
            "Wall template marking and heavy-duty expansion anchor drilling",
            "Wall bracket plate fastening and structural load test",
            "Hanging and locking television securely onto wall bracket",
            "Spirit level confirmation of 100% horizontal alignment",
            "Reconnecting existing HDMI and power cables"
        ],
        "excluded": [
            "Cost of physical wall bracket hardware (available as add-on if not supplied by customer)",
            "Concealed in-wall conduit wire chasing or drywall plaster repair",
            "Extension of power cables or cable TV coaxial cabling"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Ergonomic Viewing Height Marking",
                "description": "Technician consults on viewing distance and marks ideal eye-level height on the wall (center of screen approx 42 inches from floor).",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Rear VESA Plate Installation",
                "description": "Heavy-duty VESA mounting arms are fastened to the rear of the TV using manufacturer-recommended bolt lengths and spacers.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Masonry Drilling & Anchor Bolting",
                "description": "Masonry holes are drilled with rotary hammer; steel expansion anchors are secured into solid brick or concrete.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Structural Load & Level Test",
                "description": "Technician tests bracket rigidity under heavy downward force and confirms zero tilt with precision bubble level.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "TV Mounting & Safety Lock Engagement",
                "description": "TV is hung on the wall plate, safety locking screws tightened to prevent accidental dislodgement, and cables connected.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "High-power rotary hammer drill with 10mm/12mm carbide bits",
            "Precision spirit bubble level and measuring laser",
            "Heavy-duty steel expansion anchor fasteners and wall plugs",
            "Assorted VESA machine screws (M4, M6, M8) with nylon spacers",
            "Dust collection sleeve and drop cloth"
        ],
        "customer_setup": [
            "Decide on the preferred wall location and height before technician arrives",
            "Have wall mount bracket available (or request one from the technician)",
            "Ensure a power socket and set-top box are located within reach of TV cables"
        ],
        "aftercare": [
            "Tighten tilt adjustment knobs firmly if tilting the screen downward",
            "Never hang towels, clothes, or decorative items on the TV bracket",
            "Pull articulating swivel mounts by the bracket arm, not by pulling the delicate screen glass"
        ],
        "expected_results": [
            "Safe, rock-solid wall anchoring that eliminates the danger of TV tipping over",
            "Flawless horizontal alignment with comfortable ergonomic viewing",
            "Sleek, clutter-free room appearance freeing up entertainment tabletop space"
        ],
        "important_notes": [
            "Mounting on hollow plasterboard, gypsum board, or glass partition walls is not recommended for heavy TVs without backing studs",
            "Always use the correct length M8 screws on Samsung/LG TVs to avoid puncturing internal display electronics"
        ],
        "warranty": "60-day SmartServe installation warranty covering mounting stability and bracket anchoring",
        "faqs": [
            {
                "question": "Can my TV be mounted on tiles without cracking the tile?",
                "answer": "Yes! Our technicians use specialized diamond-tipped tile drill bits to pierce the glazed tile smoothly before using hammer action on the brick behind it."
            },
            {
                "question": "What type of wall bracket should I choose?",
                "answer": "Fixed brackets sit closest to the wall (ultra-slim). Tilt brackets allow 15-degree downward tilt (great for bedroom viewing). Swivel brackets let you angle the TV toward dining or living areas."
            },
            {
                "question": "What if I don't have a wall mount bracket?",
                "answer": "Our technician carries certified heavy-gauge universal brackets for all screen sizes from 32\" to 75\" available as affordable add-ons."
            },
            {
                "question": "How long does TV wall mounting take?",
                "answer": "Standard wall mounting, precision leveling, and safety testing take approximately 30 to 45 minutes."
            }
        ],
        "dos": [
            "Mount your TV at eye level to enjoy fatigue-free viewing during long movies",
            "Ensure cables have enough slack if using an articulating full-motion swivel bracket"
        ],
        "donts": [
            "Never attempt to mount a 55\"+ TV using basic plastic wall plugs; always use heavy steel expansion bolts",
            "Do not pull or swivel the TV by gripping the fragile screen edges"
        ],
        "tips": [
            "Choose an articulating swivel bracket for open-plan living rooms so you can pivot the TV toward the dining table"
        ]
    },

    # --- SUBCATEGORY: Washing Machine (5 Services) ---
    {
        "id": "b8d53a88-8701-41af-9638-955d1d622c74",
        "name": "Drainage Repair",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Washing Machine",
        "price": 349.0,
        "description": "Targeted diagnostic and repair service for washing machine drainage failures including water not draining (OE / E20 error), continuous water draining while filling, noisy drain pump, coin/lint trap blockages, and drain hose leaks.",
        "highlights": [
            "Magnetic drain pump motor impeller clearing, voltage test, and replacement",
            "Debris filter (coin trap) extraction, de-sludging, and sanitization",
            "Bellow drain hose unclogging to remove trapped coins, hairpins, and lint balls",
            "Drain valve rubber bellow seal and return spring replacement for semi-automatic units",
            "Drain pressure sensor (pressure switch) tube siphon inspection"
        ],
        "included": [
            "Symptom diagnosis and manual water drainage extraction",
            "Debris filter and coin trap cleaning and inspection",
            "Drain pump motor winding continuity and impeller rotation test",
            "Internal drain sump hose inspection for foreign object blockages",
            "Drain valve seal spring tension adjustment (semi-automatic)",
            "Pressure switch hose clearing to resolve false water level readings",
            "Full spin cycle drainage speed test"
        ],
        "excluded": [
            "Cost of replacement electric drain pump motor or drain valve assembly",
            "External household plumbing drain pipe unclogging",
            "Main electronic PCB repair if pump driver triac is blown"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Water Extraction & Error Code Check",
                "description": "Technician notes error code (e.g. OE, 5E, E20) and safely drains standing water using emergency drain hose.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Coin Trap & Debris Filter Inspection",
                "description": "Bottom debris trap is opened; coins, buttons, and lint masses choking the impeller are extracted.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Drain Pump Electrical & Mechanical Test",
                "description": "Drain pump motor winding resistance is tested with multimeter; impeller is inspected for broken or stripped fins.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Sump Hose & Siphon Inspection",
                "description": "Tub-to-pump rubber corrugated bellow hose is checked for trapped socks, collar stays, or foreign obstructions.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "High-Speed Drain & Spin Test",
                "description": "Machine runs a spin cycle; rapid water evacuation within 90 seconds and smooth high-speed spin are confirmed.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "True-RMS digital multimeter",
            "Flexible drain hose snake and long-reach needle pliers",
            "High-torque hose clamp pliers",
            "Water extraction basin and absorbent towels",
            "Replacement drain valve seals and pump impellers"
        ],
        "customer_setup": [
            "Clear items off the top and around the washing machine",
            "Provide a bucket and old towels for draining residual trapped water",
            "Ensure running water and electricity are available for testing"
        ],
        "aftercare": [
            "Clean the front bottom debris filter / coin trap once every month",
            "Always check clothing pockets for coins, keys, and hairpins before loading",
            "Ensure the external drain hose is not kinked, crushed, or submerged in standing water"
        ],
        "expected_results": [
            "Rapid, effortless water drainage within normal cycle times",
            "Elimination of drainage error codes (OE, 5E, E20)",
            "Smooth transition to high-speed spin drying without cycle abortion"
        ],
        "important_notes": [
            "A drain pump humming loudly without draining usually indicates an object (like a hairpin or coin) jammed in the impeller",
            "Drain pumps with stripped impellers or burnt windings require motor replacement"
        ],
        "warranty": "30-day SmartServe warranty on drainage repair labor and installed components",
        "faqs": [
            {
                "question": "Why is my front-load washing machine showing an 'OE' or '5E' error?",
                "answer": "OE or 5E indicates a drain error. Water is not pumping out within the programmed time limit, almost always caused by a blocked coin trap or a failed drain pump."
            },
            {
                "question": "Why does water drain out immediately as the machine fills?",
                "answer": "In front loaders, this happens when the drain hose is resting flat on the floor (siphon effect). In semi-automatics, it is caused by a coin stuck under the drain valve rubber seal."
            },
            {
                "question": "Can the technician remove stuck coins on-site?",
                "answer": "Yes, our technicians remove stuck coins, safety pins, and lint from the coin trap and internal sump hoses on-site."
            },
            {
                "question": "How long does washing machine drainage repair take?",
                "answer": "Diagnostics, water extraction, debris clearing, and testing take approximately 30 to 45 minutes."
            }
        ],
        "dos": [
            "Clean your washing machine's bottom coin trap filter monthly",
            "Empty all pants and shirt pockets before placing clothes in the wash"
        ],
        "donts": [
            "Do not allow the drain hose to be squeezed behind the machine against the wall",
            "Do not force open the front-load door when water is still visible inside the drum"
        ],
        "tips": [
            "Mount your front-load drain hose in a U-bend at least 65 cm off the floor to prevent gravity water siphoning"
        ]
    },
    {
        "id": "99bfd33d-7d8e-49dd-8eea-01081faa35ac",
        "name": "Drum Cleaning",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Washing Machine",
        "price": 499.0,
        "description": "Deep hygiene descaling and sanitization service for front-load and top-load washing machine drums including detergent drawer mold removal, rubber door bellow gasket disinfection, tub limescale dissolution, and odor elimination.",
        "highlights": [
            "High-potency eco-friendly descaling treatment to dissolve hidden outer-tub limescale",
            "Rubber door boot gasket (bellow) deep mold and mildew extraction",
            "Detergent dispenser drawer chemical de-sludging and siphon jet clearing",
            "Pulsator / drum baffle extraction and lint slime wash-out",
            "Hot water sanitization cycle to eliminate foul sewer-like odor and bacterial film"
        ],
        "included": [
            "Detergent dispenser drawer extraction and chemical sanitizing",
            "Front-load rubber door gasket mold scrubbing with anti-fungal agent",
            "Drum scale dissolution using professional descaling solution",
            "Coin trap and drain filter deep cleaning",
            "Pulsator cap wash (top-load) to remove hidden lint buildup",
            "High-temperature drum sanitization cycle execution",
            "Exterior cabinet wipe-down and chrome drum buffing"
        ],
        "excluded": [
            "Full physical drum extraction / mechanical teardown from outer tub",
            "Replacement of torn or severely blackened rubber door gaskets",
            "Motor, belt, or electronic component repairs"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Detergent Drawer & Siphon Descaling",
                "description": "Dispenser drawer is removed and soaked in sanitizing agent; crusty detergent buildup in siphon jets is dissolved.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Rubber Door Gasket Mold Scrubbing",
                "description": "The folds of the front-load rubber bellow gasket are treated with anti-fungal mildew remover and scrubbed clean.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Coin Trap & Debris Filter Wash",
                "description": "Bottom debris trap is cleared of lint, hair, and slimy detergent sludge.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "Deep Tub Descaling Cycle",
                "description": "Professional descaling compound is loaded into the drum; high-temperature tub clean cycle dissolves hidden scale between drums.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Drum Polish & Freshness Verification",
                "description": "Stainless steel inner drum is inspected for sparkling finish; odor-free clean operation is confirmed.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Professional non-corrosive washing machine descaling powder",
            "Anti-fungal rubber gasket mold cleanser",
            "Curved detail brushes and microfiber cloths",
            "Drain filter tray and cleaning basin",
            "Stainless steel drum polish"
        ],
        "customer_setup": [
            "Ensure electric power and continuous water supply are active",
            "Remove all laundry items from the washing machine drum",
            "Inform technician if clothes have been smelling musty after washing"
        ],
        "aftercare": [
            "Leave the washing machine door slightly ajar for 1 hour after each wash to air-dry the drum",
            "Wipe excess water from the bottom folds of the rubber door gasket with a cloth",
            "Run a tub clean cycle once every month using a washing machine descaler tablet"
        ],
        "expected_results": [
            "Complete elimination of musty, damp, or sour odors from freshly washed clothes",
            "Sparkling, mirror-finish stainless steel drum free from detergent scum",
            "Restored water heating efficiency and reduced motor drag"
        ],
        "important_notes": [
            "Severely blackened rubber gaskets with deep-set mold stained into the rubber may retain discoloration but will be sanitized",
            "Hard water limescale accumulates invisibly on the outside of the inner spin basket"
        ],
        "warranty": "30-day SmartServe service guarantee on hygiene and odor elimination",
        "faqs": [
            {
                "question": "Why do my freshly washed clothes smell musty or damp?",
                "answer": "This happens when detergent scum, lint, and body oils accumulate between the inner and outer drums, forming smelly bacterial biofilm. Professional drum cleaning completely clears it."
            },
            {
                "question": "How often should a washing machine drum be deep cleaned?",
                "answer": "A thorough descaling and sanitization service is recommended once every 3 to 6 months depending on water hardness and wash frequency."
            },
            {
                "question": "Can black mold on the front-load door rubber be cleaned?",
                "answer": "Yes, our technicians treat the rubber gasket with specialized anti-fungal cleansers that eradicate surface mold and slimy sludge."
            },
            {
                "question": "How long does washing machine drum cleaning take?",
                "answer": "Drawer cleaning, gasket treatment, filter cleaning, and running the descaling cycle take approximately 45 to 60 minutes."
            }
        ],
        "dos": [
            "Leave the door and detergent drawer slightly open after each wash to let moisture evaporate",
            "Use the correct amount of liquid detergent; excess powder leaves sticky soap residue"
        ],
        "donts": [
            "Do not leave damp clothes sitting inside the closed machine overnight",
            "Do not use harsh toilet cleaners or chlorine bleach that degrades the rubber gasket"
        ],
        "tips": [
            "Switch from powder detergent to liquid detergent to drastically reduce limescale and soap sludge inside the tub"
        ]
    },
    {
        "id": "73174aef-52e2-4cb3-964b-029014cf125f",
        "name": "General Servicing",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Washing Machine",
        "price": 499.0,
        "description": "Comprehensive preventative maintenance service for fully automatic and semi-automatic washing machines including drive belt tensioning, suspension damper check, inlet valve filter descaling, drain pump flush, and electrical safety audit.",
        "highlights": [
            "Complete 18-point mechanical and electrical operational health check",
            "Suspension shock absorber and damper spring bounce test (prevents banging/wobbling)",
            "Drive belt tension adjustment and motor pulley alignment",
            "Water inlet solenoid valve mesh filter descaling to restore fast water filling",
            "Drain pump and coin trap sludge clearing and flow verification"
        ],
        "included": [
            "Water inlet valve mesh filter cleaning to boost water fill speed",
            "Detergent dispenser tray wash and siphon check",
            "Drive motor belt tension check and alignment",
            "Suspension rods / shock absorbers bounce inspection",
            "Bottom coin trap and drain pump cleaning",
            "Electrical cord, plug, and earthing shock safety inspection",
            "Full wash, rinse, and spin cycle operational calibration"
        ],
        "excluded": [
            "Replacement of worn suspension shock absorbers or drive belt",
            "Electronic control board (PCB) micro-component repair",
            "Motor replacement or drum bearing overhaul"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Baseline Cycle & Vibration Inspection",
                "description": "Technician tests water filling speed, listens for motor hum, and evaluates spin cycle stability and vibration.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Inlet Valve Filter Descaling",
                "description": "Water inlet hoses are disconnected; fine mesh filters clogged with sand and rust scale are washed under pressure.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Drive Belt & Pulley Inspection",
                "description": "Back panel is opened; drive belt tension is checked for slackness, cracks, and proper pulley alignment.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Suspension Damper & Drum Play Audit",
                "description": "Top-load suspension rods or front-load hydraulic shock absorbers are tested for damping resistance to prevent unbalanced errors.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Drain Pump Clean & Electrical Audit",
                "description": "Coin trap is cleaned, earthing grounding verified, and a full test spin confirms smooth, quiet operation.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital true-RMS multimeter and clamp ammeter",
            "Drive belt tension gauge and pulley alignment tools",
            "Inlet valve filter cleaning brushes and descaling solution",
            "Precision spirit level for chassis leveling",
            "Microfiber cloths and lubricant spray"
        ],
        "customer_setup": [
            "Provide clear workspace around and behind the washing machine",
            "Ensure running tap water and electrical power are available",
            "Remove laundry from the drum"
        ],
        "aftercare": [
            "Ensure clothes are loaded evenly to prevent unbalanced spin cycles",
            "Check that inlet water hoses remain tightly connected without weeping",
            "Schedule annual general servicing to prevent sudden breakdown during monsoon"
        ],
        "expected_results": [
            "Noticeably faster water filling and shorter overall wash cycle times",
            "Smooth, stable high-speed spin without violent thumping or walking across floor",
            "Enhanced motor efficiency and lowered electricity and water consumption"
        ],
        "important_notes": [
            "Slow water intake is almost always caused by blocked inlet mesh filters, not low water pressure",
            "Worn suspension shock absorbers cause front loaders to bang violently on spin cycles"
        ],
        "warranty": "30-day SmartServe service guarantee on preventative maintenance and workmanship",
        "faqs": [
            {
                "question": "Why does my washing machine take so long to fill with water?",
                "answer": "Hard water, sand, and pipe rust accumulate in the tiny mesh filter inside the water inlet valve. Cleaning this filter restores full water flow immediately."
            },
            {
                "question": "Why does my washing machine shake and vibrate violently during spin?",
                "answer": "Excessive shaking is caused by un-leveled machine legs, worn-out suspension shock absorbers, or broken suspension springs. Our service checks and re-levels the machine."
            },
            {
                "question": "How often should a washing machine be serviced?",
                "answer": "Preventative maintenance is recommended once every 12 months to extend appliance lifespan and maintain energy efficiency."
            },
            {
                "question": "How long does general washing machine servicing take?",
                "answer": "A complete multi-point checkup, filter cleaning, and cycle test take approximately 40 to 50 minutes."
            }
        ],
        "dos": [
            "Ensure the washing machine is leveled on a flat, firm floor",
            "Clean the water inlet filter every 3 months in areas with muddy tap water"
        ],
        "donts": [
            "Do not overload the drum with heavy blankets exceeding rated capacity",
            "Do not wash waterproof raincoats or rubber mats on high-speed spin"
        ],
        "tips": [
            "Distribute heavy bedsheets evenly around the drum to prevent off-balance spin stops (UB/UE error codes)"
        ]
    },
    {
        "id": "7f4500a9-79f2-41bf-a213-a2534ec83be0",
        "name": "Installation",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Washing Machine",
        "price": 499.0,
        "description": "Professional unboxing, transit bolt removal, precision leveling, plumbing hookup (inlet and drain), and electrical safety setup for all front-load, top-load, and semi-automatic washing machines.",
        "highlights": [
            "Mandatory transit safety bolt extraction for front-load machines (prevents violent cabinet destruction)",
            "Precision leveling on all four corners with locking nut adjustment to prevent vibration",
            "Inlet hose connection to water tap with high-pressure threaded brass adapter",
            "Drain hose positioning with correct anti-siphon height curve",
            "Initial calibration cycle run, leak test, and customer operational guidance"
        ],
        "included": [
            "Careful unboxing and transit damage inspection",
            "Removal and handover of 4 rear shipping transit bolts (front-load)",
            "Placement and four-corner leveling with spirit bubble level",
            "Water inlet hose attachment to existing tap with clamp/threaded adapter",
            "Drain hose routing to floor drain or sink with anti-siphon bend",
            "16A grounded power socket electrical test",
            "Quick test wash/spin cycle to verify zero water leakage and stability"
        ],
        "excluded": [
            "Plumbing brass tap installation or new pipeline civil work",
            "Dedicated 16A electrical socket wiring from switchboard",
            "Metal trolley / movable stand supply (available as add-on)"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Unboxing & Transit Bolt Extraction",
                "description": "Machine is unboxed; technician removes the 4 heavy shipping transit bolts securing the drum suspension (front-load mandatory step).",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Positioning & Four-Corner Leveling",
                "description": "Machine is positioned on floor/stand; all 4 threaded rubber feet are adjusted using spirit level until rocking is 100% eliminated.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Inlet Water Hose Attachment",
                "description": "Inlet hose is connected to water tap using universal clamp or threaded adapter with watertight rubber seals.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Drain Hose Routing",
                "description": "Drain hose is secured into floor drain or elevated in U-bracket (65-100 cm) to prevent water siphoning.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Calibration Spin & Customer Walkthrough",
                "description": "Machine runs a calibration spin cycle; technician explains detergent usage, cycle selection, and maintenance tips.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Transit bolt spanner wrench",
            "Precision spirit bubble level",
            "Adjustable leveling foot wrench",
            "Digital true-RMS electrical socket tester",
            "Universal tap adapter kit and Teflon tape"
        ],
        "customer_setup": [
            "Have brand-new washing machine unboxed or in carton in the laundry area",
            "Ensure a cold water tap and functional grounded 16A socket are nearby",
            "Keep transit bolt plastic caps (found in manual packet) accessible"
        ],
        "aftercare": [
            "Store the 4 transit bolts safely in case you relocate your home in the future",
            "Check that all 4 leveling feet remain locked tightly against the floor",
            "Ensure water tap is turned off when away on vacations"
        ],
        "expected_results": [
            "Whisper-quiet, vibration-free operation even during maximum 1400 RPM spin",
            "Completely leak-free plumbing connections on inlet and drain hoses",
            "Safe, certified electrical grounding protecting family members"
        ],
        "important_notes": [
            "CRITICAL WARNING: Operating a front-load washing machine without removing transit bolts will violently destroy the drum suspension and shatter the machine",
            "Washing machines must never be operated on flimsy, unstable wheel trolleys with unlocked brakes"
        ],
        "warranty": "60-day SmartServe installation warranty covering leveling stability and plumbing joints",
        "faqs": [
            {
                "question": "What are transit bolts and why MUST they be removed?",
                "answer": "Transit bolts lock the heavy drum suspension rigid during shipping so it doesn't bounce in transit. If not removed before first use, the machine will violently jump, shake, and destroy itself."
            },
            {
                "question": "Can my washing machine be installed on a mobile trolley stand?",
                "answer": "Yes, but only on high-quality stands with locking rubber brakes. Flimsy wheel trolleys cause excessive vibration and premature bearing failure."
            },
            {
                "question": "Does installation include the water tap connection?",
                "answer": "Yes, connecting the inlet hose to your existing water tap and testing for zero leaks is included."
            },
            {
                "question": "How long does washing machine installation take?",
                "answer": "Unboxing, transit bolt removal, leveling, plumbing connection, and demo take approximately 35 to 45 minutes."
            }
        ],
        "dos": [
            "Store the transit bolts safely; they are mandatory if you ever move houses",
            "Keep the machine on a flat, solid floor for maximum spin stability"
        ],
        "donts": [
            "NEVER turn on a front-load washer before removing all 4 rear shipping bolts",
            "Do not place cardboard or wooden wedges under feet to level the machine"
        ],
        "tips": [
            "Lock the leveling foot nuts tightly against the chassis to keep the machine from vibrating out of level over time"
        ]
    },
    {
        "id": "597349ec-d076-44dd-ba55-6ebc09a88096",
        "name": "Washing Machine Repair",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Washing Machine",
        "price": 459.0,
        "description": "Comprehensive diagnostic and component-level repair for front-load, top-load, and semi-automatic washing machines including drum not spinning, loud jet-engine bearing noise, door lock error (dE), water overflow, and PCB motherboard faults.",
        "highlights": [
            "Heavy-duty drum tub bearing and oil seal diagnostic for loud roaring spin noise",
            "Door interlock safety switch (PTC/solenoid door lock) testing and replacement",
            "Water level pressure sensor (pressure transducer) frequency calibration",
            "Direct Drive / BLDC inverter motor hall sensor and stator coil testing",
            "Main PCB power relay, triac, and motor driver circuit repair"
        ],
        "included": [
            "Complete electrical, mechanical, and electronic fault diagnosis",
            "Motor capacitor, carbon brushes, or inverter stator continuity check",
            "Electronic door lock switch alignment and replacement check",
            "Water inlet valve and water level pressure switch test",
            "Drain pump motor and belt drive inspection",
            "Main electronic control board error code clearing",
            "Post-repair complete wash, rinse, and spin cycle verification"
        ],
        "excluded": [
            "Cost of replacement parts such as motor, PCB, tub bearings, or door lock",
            "Complete outer tub replacement if cracked from transit bolt neglect",
            "Cabinet repainting or sheet metal rust fabrication"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Error Code & Symptom Evaluation",
                "description": "Technician reads error code (e.g. dE, LE, UE, PE, tE), listens to drum bearing sound by hand-spin, and tests electrical supply.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Door Lock & Safety Interlock Probing",
                "description": "Door latch microswitch and thermal PTC solenoid are tested with multimeter to resolve door lock (dE) errors.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Motor & Inverter Drive Diagnostics",
                "description": "Motor windings, carbon brushes, or Direct Drive hall position sensors are tested for rotational failures.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Component Replacement & Wire Harness Repair",
                "description": "Defective door switch, pressure sensor, belt, drain pump, or PCB module is replaced with genuine OEM parts.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "High-Speed Spin & Agitation Verification",
                "description": "Machine is run through full agitation and 1200+ RPM spin cycles to confirm smooth, quiet, and fault-free operation.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital true-RMS multimeter and tachometer probe",
            "Bearing play dial indicator gauge",
            "Spring clamp expansion pliers for door bellow ring",
            "Nut driver and socket set (10mm, 13mm, 17mm)",
            "Assorted OEM door lock switches, pressure sensors, and drive belts"
        ],
        "customer_setup": [
            "Provide workspace around the machine and ensure water is available",
            "Describe the symptom clearly (e.g. loud roaring noise on spin, door won't unlock, drum won't rotate)",
            "Keep appliance model number and serial badge accessible"
        ],
        "aftercare": [
            "Avoid overloading the machine with excess heavy laundry that strains drum bearings",
            "Use recommended HE (high-efficiency) detergent to avoid motor over-sudsing",
            "Use a dedicated voltage stabilizer if your area suffers power surges"
        ],
        "expected_results": [
            "Immediate resolution of drum rotation, door locking, or water filling errors",
            "Quiet, balanced spin operation without grinding or roaring noises",
            "Reliable cycle completion without erratic pauses or mid-cycle resets"
        ],
        "important_notes": [
            "A loud roaring noise like a jet engine taking off during spin indicates failed drum tub bearings; requires bearing and seal replacement",
            "Replacement parts are quoted upfront before installation"
        ],
        "warranty": "30-day SmartServe warranty on repair labor and installed components",
        "faqs": [
            {
                "question": "Why does my washing machine sound like a jet engine taking off during spin?",
                "answer": "This loud roaring sound indicates that the inner tub water seal has failed, allowing soapy water into the metal drum bearings, causing them to rust and grind. Replacing the bearings and seal eliminates the noise."
            },
            {
                "question": "Why is the door stuck locked on my front-load washing machine?",
                "answer": "Front-load doors have a thermal safety lock that takes 2-3 minutes to release after the cycle ends. If it remains permanently stuck, the door lock solenoid has failed or water is still detected inside the drum."
            },
            {
                "question": "Why does the drum not spin even though the motor hums?",
                "answer": "In belt-driven machines, the drive belt has snapped or slipped off the pulley. In Direct Drive machines, a faulty hall sensor or capacitor prevents rotation."
            },
            {
                "question": "How long does washing machine repair take?",
                "answer": "Standard diagnostic and part replacement take approximately 40 to 60 minutes."
            }
        ],
        "dos": [
            "Wait 3 minutes after cycle completion before attempting to pull open the front-load door",
            "Spread out large towels and jeans so they don't form a single heavy ball in the drum"
        ],
        "donts": [
            "Do not force open a locked door handle with brute force (breaks plastic handle mechanism)",
            "Do not continue using a machine with roaring bearings (damages the outer drum)"
        ],
        "tips": [
            "If your front-load door is stuck with clean wet laundry inside, locate the emergency manual pull-cord inside the bottom drain filter compartment to unlock it"
        ]
    }
]
