# Electrician Services Data (11 Services)
# Category: 5. Electrician, Plumber, Carpenter & Home Repairs

ELECTRICIAN_SERVICES = [
    {
        "id": "937e20d9-1920-4895-80cc-0a91e0f5e938",
        "name": "Appliance Electrical Connection",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Electrician",
        "price": 329.0,
        "description": "Certified high-amperage electrical hookup and safe power termination for major household appliances including heavy induction hobs, electric ovens, geysers, washing machines, dryers, and commercial kitchen appliances requiring 16A/25A dedicated supplies.",
        "highlights": [
            "Dedicated high-load copper cable gauge matching (2.5 sq mm to 4 sq mm)",
            "Heavy-duty 16A/25A industrial grade 3-pin plug and ceramic socket termination",
            "Individual DP (Double Pole) switch / MCB isolator integration for overload protection",
            "Comprehensive earthing resistance test and earth leakage fault checking",
            "Safe cable dressing through heat-resistant PVC conduits and cable gland clips"
        ],
        "included": [
            "Load capacity assessment of existing electrical feed circuit",
            "Stripping, crimping, and lugging copper multi-strand appliance power cables",
            "Terminating phase, neutral, and dedicated earth wires into terminal block or 16A plug",
            "Testing line-to-earth and line-to-neutral voltage levels under loaded state",
            "Securing power cables with fire-retardant saddle clips or PVC conduit",
            "Power-on cycle test and current draw measurement in amperes"
        ],
        "excluded": [
            "New concealed wall conduit channeling and plastering over 2 meters",
            "Appliance internal motherboard or compressor repairs",
            "Plumbing water inlet/drainage hookups"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Circuit Amperage & Load Audit",
                "description": "Electrician inspects appliance rated wattage, measures main line voltage, and checks distribution board breaker rating.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Power Isolation & Safety Lockout",
                "description": "Main sub-circuit breaker is switched off and tested with a non-contact neon tester to verify zero voltage.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Heavy-Duty Cable Termination",
                "description": "Appropriately sized copper wiring is fitted with insulated pin lugs and firmly bolted into the appliance terminal block.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Ground Continuity & Earthing Verification",
                "description": "Technician tests low-resistance earthing path to chassis using digital multimeter to eliminate electrical shock hazards.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Live Load Testing & Amperage Check",
                "description": "Power is re-energized; appliance is operated at maximum load while clamp meter confirms current draw is within safe limits.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "True-RMS digital clamp multimeter and insulation resistance tester",
            "Automatic wire stripper and heavy crimping plier kit",
            "Insulated VDE 1000V screwdrivers and socket spanners",
            "Heat shrink tubing, ferrules, and brass ring lugs",
            "Non-contact AC voltage sensor pen"
        ],
        "customer_setup": [
            "Keep the appliance placed near the designated 16A/25A power outlet",
            "Ensure access to the main circuit breaker / MCB distribution board",
            "Keep the manufacturer installation booklet and electrical spec sheet handy"
        ],
        "aftercare": [
            "Do not plug multiple high-wattage appliances into the same heavy-duty socket using adapters",
            "If the dedicated MCB trips frequently, discontinue use immediately and call for inspection",
            "Inspect the plug pins periodically for discoloration or overheating"
        ],
        "expected_results": [
            "Safe, fire-resistant power connection capable of continuous heavy-load operation",
            "Verified earth fault protection preventing electric shocks on metallic casings",
            "Neatly routed wiring with zero loose terminals or exposed copper strands"
        ],
        "important_notes": [
            "High-wattage appliances exceeding 2000W must never be operated on standard 6A lighting circuits",
            "Proper household earth bonding is mandatory for all metallic-chassis appliances"
        ],
        "warranty": "30-day SmartServe electrical service warranty on workmanship and circuit stability",
        "faqs": [
            {
                "question": "Can I connect my built-in oven or geyser to a normal 6A wall socket?",
                "answer": "No. High-wattage heating appliances draw 10A to 16A of continuous current and require dedicated 16A/20A wiring and sockets to prevent socket melting and fire hazards."
            },
            {
                "question": "Does this service include supplying the 16A power cord if my appliance came without one?",
                "answer": "The service covers complete termination labor. If heavy-duty 3-core copper cable or 16A plug tops are needed, our technician can supply certified branded materials at nominal standard rates."
            },
            {
                "question": "How do you test that the earthing is safe?",
                "answer": "We use digital multimeters to measure potential between neutral and earth (which should be under 2V-3V) and verify that chassis resistance to earth is near zero."
            },
            {
                "question": "What happens if my existing home wiring cannot support the appliance load?",
                "answer": "The technician will advise whether a dedicated new line from the distribution board is required before energizing the appliance."
            }
        ],
        "dos": [
            "Always operate heavy appliances through a dedicated MCB or Double Pole switch",
            "Report any sparking or warm plugs immediately"
        ],
        "donts": [
            "Never bypass the 3-pin earth pin or use cheap universal plug adapters",
            "Never run appliance power cables under carpets or across wet doorways"
        ],
        "tips": [
            "Having a dedicated 16A or 25A circuit directly from your MCB box extends appliance life and prevents nuisance tripping."
        ]
    },
    {
        "id": "29d435d1-c81a-46be-af60-5540588c83a2",
        "name": "Electrical Inspection",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Electrician",
        "price": 249.0,
        "description": "Comprehensive electrical safety audit and diagnostic health check of complete residential wiring, main distribution board, MCBs/RCCBs, earthing resistance, phase voltage balance, and high-load sockets to detect fire hazards, overloading, and current leaks.",
        "highlights": [
            "Main distribution panel thermal and mechanical screw-tightness audit",
            "RCCB / ELCB trip sensitivity and earth leakage tripping speed test",
            "Neutral-to-earth fault and live-to-neutral voltage balance verification",
            "Infrared thermal spotting for hot terminals, loose joints, and overloaded circuits",
            "Detailed written electrical safety diagnostic checklist and risk assessment"
        ],
        "included": [
            "Full inspection of main breaker panel, MCBs, RCCB, and isolator switches",
            "Digital multimeter testing across all electrical switchboards and heavy sockets",
            "Earth electrode resistance and grounding path continuity verification",
            "Testing RCCB trip button and simulated 30mA residual current trip test",
            "Visual check of concealed junction boxes, wire gauges, and cable insulation integrity",
            "Comprehensive verbal and written safety report with remediation recommendations"
        ],
        "excluded": [
            "Rewiring entire rooms or pulling new concealed conduits",
            "Replacing faulty electrical fixtures and distribution panels during the inspection",
            "Government electricity board meter or external pole service line repairs"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Distribution Board & Main Panel Audit",
                "description": "Technician removes distribution board fascia to inspect MCB busbar contacts, check for burning smells, and tighten loose terminal lugs.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Voltage Balance & Earthing Resistance Test",
                "description": "Multimeter measurements verify incoming phase voltage, line-to-neutral stability, and neutral-to-earth leakage levels.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "RCCB / ELCB Trip Functionality Verification",
                "description": "Residual current circuit breaker is tested using test button and instrumented leakage simulation to guarantee human shock protection.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Room-by-Room Switchboard & Socket Audit",
                "description": "Every accessible switchboard, power socket, and appliance outlet is checked for polarity, secure earthing, and physical wear.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Safety Report & Risk Rectification Consultation",
                "description": "Technician compiles identified vulnerabilities (overloaded MCBs, missing earthing, burnt terminals) and presents priority fixes.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital True-RMS multimeter and socket polarity tester",
            "Residual Current Device (RCD/RCCB) calibrated trip tester",
            "Infrared laser thermal thermometer for hot-spot detection",
            "VDE insulated 1000V tool kit and torque screwdriver",
            "Inspection diagnostic report clipboard"
        ],
        "customer_setup": [
            "Ensure clear, unobstructed access to the main MCB distribution box and sub-panels",
            "Provide entry to all rooms, balconies, and utility areas with switchboards",
            "Inform the technician about any past frequent tripping, flickering lights, or shocks"
        ],
        "aftercare": [
            "Implement high-priority electrical rectifications promptly, especially missing earthing or faulty RCCBs",
            "Schedule a routine electrical inspection once every 12 to 18 months",
            "Avoid daisy-chaining multi-plug extensions on inspected sockets"
        ],
        "expected_results": [
            "Complete peace of mind regarding household electrical safety and fire protection",
            "Accurate diagnosis of hidden electrical faults, parasitic leaks, or shock hazards",
            "Actionable prioritized blueprint for repairing worn or hazardous electrical components"
        ],
        "important_notes": [
            "A brief 10 to 15-minute complete power outage will occur during main panel and RCCB trip testing",
            "Inspection identifies safety risks; subsequent repair parts and extensive labor are quoted separately"
        ],
        "warranty": "30-day SmartServe diagnostic accuracy guarantee",
        "faqs": [
            {
                "question": "How often should a home undergo an electrical safety inspection?",
                "answer": "Residential properties should have a comprehensive electrical inspection every 1 to 2 years, or immediately before purchasing/renting a home or after noticing light flickers and shocks."
            },
            {
                "question": "Will power be cut off during the electrical inspection?",
                "answer": "Yes, short 5 to 10-minute power isolations are necessary to safely inspect internal breaker busbars and test RCCB trip mechanisms."
            },
            {
                "question": "What is the most dangerous electrical fault commonly discovered during inspections?",
                "answer": "Missing or disconnected earth wiring and malfunctioning RCCBs are the most critical, as they eliminate protection against fatal electric shocks from appliance metal casings."
            },
            {
                "question": "Does this inspection include testing the electricity board meter?",
                "answer": "We inspect incoming voltage and connection cables up to the main isolator. The official utility energy meter is sealed and managed exclusively by your local electricity board."
            }
        ],
        "dos": [
            "Test your distribution board RCCB monthly using the built-in 'T' (Test) push button",
            "Keep the area directly beneath your main electrical panel clear of storage items"
        ],
        "donts": [
            "Never ignore mild electric tingle sensations when touching metal appliances",
            "Never replace a tripping MCB with a higher amperage breaker without verifying wire gauge"
        ],
        "tips": [
            "A neutral-to-earth voltage higher than 3V indicates poor earth pit bonding that should be grounded immediately."
        ]
    },
    {
        "id": "af3b86b9-2977-4527-98df-8d508149f12c",
        "name": "Fan Installation",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Electrician",
        "price": 359.0,
        "description": "Professional electrical installation and wiring of ceiling fans, BLDC energy-saving fans, exhaust fans, and decorative chandelier fans including downrod wire threading, capacitor wiring, electronic regulator integration, and blade balancing.",
        "highlights": [
            "Complete electrical hookup for standard AC and modern BLDC remote-control ceiling fans",
            "Safe downrod wiring with heat-resistant copper conductors and split-pin safety lock",
            "Ceiling hook shackle insulator assembly to prevent electrical leakage to ceiling rebar",
            "Electronic rotary regulator or BLDC RF remote sensor frequency synchronization",
            "Precision dynamic blade angle balancing for silent, zero-wobble high-RPM airflow"
        ],
        "included": [
            "Assembling motor housing, downrod, canopy cups, and safety split-pin clamp",
            "Threading flexible 3-core copper wiring through the downrod and motor shaft",
            "Connecting phase, neutral, and earth terminals to the ceiling junction box",
            "Mounting fan shackle onto existing ceiling hook with rubber vibration dampener",
            "Fastening all aerodynamic blades with spring washers and torque screws",
            "Connecting wall switchboard step-type electronic regulator or BLDC bypass module",
            "Testing all speed steps, reverse airflow (if equipped), and remote control pairing"
        ],
        "excluded": [
            "Casting new heavy-duty ceiling anchor hooks into concrete ceiling (requires civil work)",
            "Concealed wall conduit wiring runs over 2 meters to the switchboard",
            "Supply of the ceiling fan unit itself or replacement remote controls"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Ceiling Hook & Power Isolation Verification",
                "description": "Electrician isolates the room circuit breaker, verifies ceiling hook structural strength, and tests junction wires for zero voltage.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Motor, Downrod & Wire Assembly",
                "description": "Downrod is secured to motor spindle with heavy lock-bolt, nut, and safety split-pin; internal copper wiring is threaded through.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Shackle Hooking & Electrical Termination",
                "description": "Fan is hung on ceiling hook with rubber isolation pads; phase, neutral, and earth are terminated into terminal block with wire nuts.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Blade Mounting & Pitch Alignment",
                "description": "Blades are fastened to motor rotor with torque-balanced screws and checked with a pitch gauge to prevent aerodynamic imbalance.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Regulator Wiring & High-Speed Run Test",
                "description": "Switchboard regulator or BLDC bypass is wired; fan is tested at full speed to ensure wobble-free, silent operation.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Heavy-duty adjustable step ladder with rubber feet",
            "VDE insulated 1000V screwdriver set and wire strippers",
            "Digital multimeter and neon circuit voltage tester",
            "Blade balancing weight kit and magnetic bubble level",
            "Heat-resistant wire connectors, split-pins, and rubber grommets"
        ],
        "customer_setup": [
            "Ensure the ceiling fan box, blades, downrod, and remote are unboxed in the room",
            "Verify that a ceiling hook and junction box are already present at the desired location",
            "Clear furniture directly under the ceiling installation point"
        ],
        "aftercare": [
            "Clean fan blades gently with a dry microfiber cloth without bending blade brackets",
            "If using a BLDC fan, operate speed exclusively via the remote rather than an old analog wall regulator",
            "Inspect split-pin and shackle bolts once a year for tightness"
        ],
        "expected_results": [
            "Smooth, silent, high-speed air circulation with zero motor hum or ceiling wobbling",
            "Complete electrical safety with properly insulated wiring and dedicated earth connection",
            "Seamless speed regulation from wall switchboard or BLDC remote"
        ],
        "important_notes": [
            "BLDC fans require either bypassing or setting the old rotary wall regulator to full speed to avoid motor humming",
            "False ceilings require specialized long threaded drop-rods anchored to the true RCC slab"
        ],
        "warranty": "60-day SmartServe installation warranty covering mounting stability and wiring connections",
        "faqs": [
            {
                "question": "Can an old analog wall regulator be used with a newly installed BLDC fan?",
                "answer": "No. BLDC fans have internal electronic inverters that need constant 230V input. Our electrician will safely bypass the old regulator and connect the fan switch directly for remote operation."
            },
            {
                "question": "Why is the split pin so important in ceiling fan installation?",
                "answer": "The split cotter pin prevents the shackle lock bolt and nut from unscrewing due to continuous rotational vibration over time, ensuring the fan cannot fall."
            },
            {
                "question": "Does this service include assembling and balancing the fan blades?",
                "answer": "Yes, complete aerodynamic blade assembly, screw torque tightening with spring washers, and dynamic balancing are fully included."
            },
            {
                "question": "What if my ceiling does not have an existing hook?",
                "answer": "If there is no hook in the concrete ceiling, anchor fastener installation can be performed if the RCC ceiling slab is accessible, subject to ceiling type."
            }
        ],
        "dos": [
            "Use the BLDC remote control for speed changes and timer settings",
            "Turn off the wall switch before cleaning dust from fan blades"
        ],
        "donts": [
            "Never bend or twist fan blade brackets while wiping, as this causes violent wobbling",
            "Never operate a fan if you hear scraping or mechanical grinding sounds"
        ],
        "tips": [
            "Ceiling fans should ideally hang between 8 and 9 feet from the floor for optimal airflow and cooling efficiency."
        ]
    },
    {
        "id": "6eda6ea6-d918-49a1-8375-ade18712d7ab",
        "name": "Inverter Installation",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Electrician",
        "price": 239.0,
        "description": "Safe installation, wiring, and commissioning of home inverters, UPS backup systems, and tubular/lithium battery banks including DC terminal lugging, AC mains input/output circuit separation, MCB changeover wiring, and inverter load segregation.",
        "highlights": [
            "High-current DC battery terminal crimping with petroleum jelly corrosion protection",
            "Segregation of emergency backup circuits from heavy appliance load lines",
            "AC mains bypass switch and changeover switch integration for uninterrupted power",
            "Inverter charging voltage and float charging rate calibration",
            "Clean cable routing with heavy 10-25 sq mm battery interconnect cables"
        ],
        "included": [
            "Positioning inverter unit and heavy battery bank on an acid-resistant trolley or stand",
            "Connecting positive and negative battery leads with brass lugs and spring washers",
            "Wiring inverter 230V AC input supply from dedicated 16A wall outlet",
            "Tracing and separating backed-up lighting/fan circuits at the distribution board",
            "Connecting inverter AC output line to the designated emergency load sub-circuit",
            "Testing mains cut-off switchover time and automatic battery charging cycle"
        ],
        "excluded": [
            "Supplying inverter unit, battery bank, or battery trolley",
            "Adding acid/distilled water to deeply drained unmaintained old batteries",
            "Concealed wall conduit rewiring across different floors"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Site Inspection & Backup Circuit Identification",
                "description": "Electrician assesses inverter location for ventilation, identifies light/fan circuits to be backed up, and checks total connected wattage.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Main Power Isolation & Safety Lockout",
                "description": "Main breaker is de-energized to allow safe terminal work on the distribution board without risk of back-feeding or short circuits.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "DC Battery Terminal Connection",
                "description": "Heavy-gauge copper DC cables are bolted securely to battery positive and negative terminals, torqued tight, and coated with protective petroleum jelly.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "AC Input & Output Circuit Integration",
                "description": "Inverter input is plugged into a dedicated 16A socket; inverter output neutral and phase are integrated into the distribution board backup bus.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Mains Failure Simulation & Switchover Test",
                "description": "Main power is switched off to test instantaneous inverter changeover, verify silent operation, and measure output voltage under backup load.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Heavy ring spanners and insulated socket wrench set for battery terminals",
            "Heavy hydraulic crimping tool and brass ring lugs",
            "Digital True-RMS multimeter and DC clamp meter",
            "Petroleum jelly / anti-corrosion battery terminal spray",
            "Heat shrink sleeves, insulation tape, and PVC saddle clips"
        ],
        "customer_setup": [
            "Keep the inverter unit, battery, and trolley placed in the desired well-ventilated location",
            "Ensure the battery is filled with electrolyte (for lead-acid tubular models)",
            "Clear access to the main distribution board"
        ],
        "aftercare": [
            "Keep the battery bank in a well-ventilated corner away from open sparks or flame",
            "Check distilled water levels in tubular batteries every 45 to 60 days",
            "Do not connect heavy heating appliances (geysers, irons, heaters) to inverter circuits"
        ],
        "expected_results": [
            "Instantaneous, flicker-free power backup during electrical grid outages",
            "Correct battery charging regulation extending overall battery operational lifespan",
            "Fully segregated circuits preventing inverter overloads and tripping"
        ],
        "important_notes": [
            "Lead-acid batteries emit hydrogen gas during charging; installation must be in a well-ventilated area",
            "Neutral looping between inverter output and raw utility grid must be properly isolated to prevent inverter failure"
        ],
        "warranty": "60-day SmartServe installation warranty covering wiring connections and changeover stability",
        "faqs": [
            {
                "question": "Can my inverter run an AC or refrigerator during a power cut?",
                "answer": "Standard 800VA-1500VA home inverters are designed for lights, fans, TVs, and routers. High-capacity 2.5kVA+ pure sine wave systems can run refrigerators, but heavy ACs require dedicated solar or high-capacity inverter setups."
            },
            {
                "question": "Why is anti-corrosion jelly applied to battery terminals?",
                "answer": "Lead-acid battery terminals produce acidic sulfate deposits when exposed to air. Applying petroleum jelly prevents terminal corrosion, voltage drops, and overheating."
            },
            {
                "question": "What is the benefit of a manual bypass switch on an inverter system?",
                "answer": "A bypass switch allows you to route grid electricity directly to your home circuits if the inverter unit itself ever develops a fault and needs repair."
            },
            {
                "question": "Does this service include wiring new backup lines inside the house?",
                "answer": "It includes connecting the inverter to your existing distribution board backup circuits. Adding extensive new conduit lines to distant rooms is charged as additional wiring."
            }
        ],
        "dos": [
            "Top up lead-acid tubular batteries only with pure distilled water, never tap or mineral water",
            "Ensure the inverter mode switch (UPS mode vs Normal mode) matches your computer usage requirements"
        ],
        "donts": [
            "Never connect heavy loads like electric water heaters or microwave ovens to inverter circuits",
            "Never place combustible materials or clothes on top of the inverter or battery"
        ],
        "tips": [
            "Setting your inverter to UPS mode ensures computers and Wi-Fi routers do not reboot during grid power outages."
        ]
    },
    {
        "id": "5a7fa17c-572d-47f4-aed7-5ce5d3050e76",
        "name": "Light Installation",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Electrician",
        "price": 459.0,
        "description": "Expert electrical installation, wiring, and mounting of all indoor and outdoor lighting fixtures including modern LED batten lights, false-ceiling recessed spotlights, magnetic track lights, designer pendant lamps, wall sconces, and chandeliers.",
        "highlights": [
            "Universal fixture electrical connection (LED battens, COB spot downlights, panel lights, chandeliers)",
            "Concealed wiring connection with fire-rated insulated terminal blocks",
            "Driver/transformer integration for low-voltage 12V/24V LED strip and magnetic track systems",
            "Laser level alignment for straight, symmetrical wall sconce and pendant mounting",
            "Load balancing and wall switch control integration with flicker-free operation"
        ],
        "included": [
            "Power isolation and testing existing ceiling or wall junction box wiring",
            "Assembling lighting fixture mounting brackets and decorative canopies",
            "Stripping and connecting live, neutral, and earth wires with insulated wire connectors",
            "Connecting internal or external constant-current LED drivers / electronic transformers",
            "Securing fixture to wall/ceiling using heavy-duty nylon rawl plugs and screws",
            "Installing LED bulbs or diffusers and testing light output across all switches"
        ],
        "excluded": [
            "Cutting new circular holes in false ceiling gypsum sheets (covered under specialized work)",
            "Concealed wall channelling over 2 meters to create new switch points",
            "Supply of designer decorative light fixtures, lamps, or chandeliers"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Switchboard Isolation & Circuit Check",
                "description": "Electrician turns off the room lighting switch and sub-breaker, verifying zero line voltage with a neon tester pen.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Mounting Bracket Fastening",
                "description": "Fixture mounting base or bracket is held to the junction box or drilled into concrete/drywall using precision anchors.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Driver & Wire Termination",
                "description": "Phase and neutral conductors are connected through terminal blocks; ground wire is securely bonded to metal fixtures.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Fixture Housing Attachment & Leveling",
                "description": "Light body is fixed to the bracket, checked with laser/spirit level for horizontal and vertical symmetry, and screws tightened.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Illumination & Current Check",
                "description": "Power is re-energized; light is switched on to verify instant start, flicker-free illumination, and proper driver temperature.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "VDE insulated screwdriver set and wire strippers",
            "Cordless hammer drill with masonry and drywall bits",
            "Laser leveling line and spirit bubble level",
            "Non-contact voltage detector and digital multimeter",
            "Heat-resistant Wago wire connectors, wall plugs, and screws"
        ],
        "customer_setup": [
            "Have the light fixtures, bulbs, and mounting hardware unboxed and ready",
            "Ensure access to the room switchboard and main lighting circuit breaker",
            "Clear furniture beneath the installation point to allow ladder placement"
        ],
        "aftercare": [
            "Always turn off the wall switch before replacing bulbs or dusting light diffusers",
            "Wipe glass globes and acrylic diffusers with a dry or lightly damp microfiber cloth",
            "Do not exceed the maximum wattage rating printed on the lamp holder socket"
        ],
        "expected_results": [
            "Stunning, uniform, flicker-free room illumination with perfect aesthetic alignment",
            "Rock-solid, flush fixture mounting with zero sagging or loose ceiling gaps",
            "Safe, fire-retardant electrical terminations preventing short circuits or overheating"
        ],
        "important_notes": [
            "Heavy chandeliers exceeding 10 kg require anchor fasteners bolted directly to RCC ceiling slab",
            "Low-voltage LED strip lights must be matched with properly rated DC power supply drivers"
        ],
        "warranty": "60-day SmartServe electrical installation warranty covering mounting stability and wiring connections",
        "faqs": [
            {
                "question": "Can this service install complex multi-arm crystal chandeliers?",
                "answer": "Yes. Our electricians install all varieties of chandeliers, assembling the frame, wiring internal branches, and securing heavy-duty ceiling anchor hooks."
            },
            {
                "question": "Why do my new LED lights flicker after being installed?",
                "answer": "Flickering usually occurs due to loose neutral connections, incompatible analog dimmers, or cheap uncertified LED drivers. Our installation guarantees stable, flicker-free power."
            },
            {
                "question": "Do I need to supply the mounting screws and wall anchors?",
                "answer": "Most light fixtures include basic screws, but our technicians carry industrial-grade nylon rawl plugs and heavy anchor fasteners for secure mounting."
            },
            {
                "question": "Can the electrician connect smart Wi-Fi lights that sync with an app?",
                "answer": "Yes, we handle electrical wiring and physical mounting of smart lighting fixtures, bulbs, and smart dimmer controllers."
            }
        ],
        "dos": [
            "Use warm white (2700K-3000K) or neutral white (4000K) lighting for comfortable living spaces",
            "Ensure light fixtures in bathrooms are rated at least IP44 for moisture resistance"
        ],
        "donts": [
            "Never use a bulb with higher wattage than the fixture's rated maximum limit",
            "Never hang heavy light fixtures from standard plaster false ceiling boards without slab anchoring"
        ],
        "tips": [
            "Installing constant-current LED drivers with built-in 2.5kV surge protection safeguards lights against monsoon voltage spikes."
        ]
    },
    {
        "id": "ed4cd512-a7d5-4001-b137-d152316de73f",
        "name": "MCB Repair",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Electrician",
        "price": 529.0,
        "description": "Diagnosis, repair, and replacement of malfunctioning Miniature Circuit Breakers (MCBs), Residual Current Circuit Breakers (RCCBs), and main distribution board isolators that trip repeatedly, fail to reset, exhibit loose busbar sparking, or cause room power loss.",
        "highlights": [
            "Identification of root causes behind nuisance MCB tripping (overload vs short circuit vs earth leak)",
            "Thermal busbar and terminal screw tightening with calibrated torque",
            "Precision amperage curve rating replacement (B-curve, C-curve, or D-curve matching)",
            "Residual Current Device (RCCB/ELCB) 30mA earth leakage trip verification",
            "DIN-rail mounting alignment and busbar comb connection re-insulation"
        ],
        "included": [
            "Main distribution box cover removal and thermal inspection of all breakers",
            "Isolating incoming utility power supply for safe panel maintenance",
            "Clamp meter current draw measurement on the affected circuit to check for overloading",
            "Extracting defective, burnt, or internally jammed MCB from the DIN rail",
            "Installing certified high-breaking-capacity replacement MCB (10kA rated)",
            "Retightening all neutral and phase terminal clamp screws to prevent arcing",
            "Live circuit testing under operating appliance load"
        ],
        "excluded": [
            "Complete distribution box enclosure replacement or embedded wall civil rewiring",
            "Repairing damaged external utility cables before the main electricity meter",
            "Appliance repair if the appliance itself is causing the short circuit"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Trip Symptom Analysis & Circuit Tracing",
                "description": "Electrician interviews homeowner, traces which room or appliance correlates with the tripped breaker, and tests for short circuits.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Distribution Panel Power Isolation",
                "description": "Main isolator switch is de-energized, verified with multimeter, and safety lockout precautions taken.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Busbar & Defective MCB Extraction",
                "description": "Burnt or mechanically worn MCB is disconnected from the copper busbar comb, unclipped from the DIN rail, and examined.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "New MCB Seating & Torque Termination",
                "description": "New correctly rated MCB (e.g. C16, C20, or C32) is clicked onto the DIN rail and wired with securely torqued terminal screws.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Re-energization & Clamp Meter Load Verification",
                "description": "Power is restored; appliances are turned on while digital clamp meter verifies operating amperage is safely below trip threshold.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "True-RMS digital clamp meter and insulation resistance megohmmeter",
            "VDE insulated 1000V screwdrivers (Pozidriv, Phillips, and slotted)",
            "Busbar cutting plier and copper ferrule crimping tool",
            "DIN-rail replacement clips and heat-resistant PVC terminal shrouds",
            "Non-contact voltage sensor and phase rotation tester"
        ],
        "customer_setup": [
            "Ensure clear access to the main electrical distribution board (DB box)",
            "Unplug sensitive electronic devices (computers, gaming consoles) prior to testing",
            "Have an emergency flashlight available during temporary panel power shutdown"
        ],
        "aftercare": [
            "If an MCB trips again, do not repeatedly force the switch lever up; unplug recently plugged devices",
            "Never operate multiple heavy heating appliances simultaneously on a single 16A circuit",
            "Schedule an electrical panel checkup every 12 months"
        ],
        "expected_results": [
            "Zero nuisance tripping under normal residential electrical loads",
            "Instant, reliable breaker trip protection in the event of genuine short circuits",
            "Elimination of burnt plastic odors, sparking, or warm breaker switches"
        ],
        "important_notes": [
            "Never replace a tripping 16A MCB with a 32A MCB without verifying the internal wall wire gauge, as this can burn internal wall wires",
            "RCCB tripping indicates an active earth leakage or insulation breakdown that must be isolated"
        ],
        "warranty": "30-day SmartServe warranty on repair labor and installed replacement parts",
        "faqs": [
            {
                "question": "Why does my MCB trip immediately every time I try to push the switch up?",
                "answer": "An immediate trip indicates a 'dead short circuit' (phase touching neutral or earth) or a welded internal breaker mechanism. It requires finding the short before forcing the breaker."
            },
            {
                "question": "What is the difference between an MCB and an RCCB?",
                "answer": "An MCB protects wires against current overload and short circuits. An RCCB protects human life against fatal electric shocks by detecting microscopic (30mA) leakage to ground."
            },
            {
                "question": "Can I replace a 10A MCB with a 25A MCB to stop it from tripping?",
                "answer": "No. The MCB is specifically sized to protect the copper wire behind your wall. Oversizing the breaker allows wires to overheat inside conduits, creating severe electrical fire hazards."
            },
            {
                "question": "Does this service include supplying the replacement MCB?",
                "answer": "The service fee covers complete diagnostic labor, replacement, and busbar testing. If a new MCB is needed, our technician provides genuine Schneider, Legrand, Havells, or L&T breakers at retail prices."
            }
        ],
        "dos": [
            "Always inspect what appliance was turned on right before the MCB tripped",
            "Maintain proper air circulation around your main distribution box"
        ],
        "donts": [
            "Never tape or physically wedge an MCB lever in the 'ON' position",
            "Never touch the internal metal terminals of an open distribution board"
        ],
        "tips": [
            "C-curve MCBs are best suited for inductive residential loads like ACs, pumps, and refrigerators, which draw high startup surge currents."
        ]
    },
    {
        "id": "6f3cde05-c2e6-4fc0-aeec-9db5ef4ca409",
        "name": "Short Circuit Repair",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Electrician",
        "price": 549.0,
        "description": "Urgent electrical fault tracing and hazardous short-circuit repair to locate, isolate, and remediate burnt wiring, phase-to-neutral contacts, melted junction boxes, arcing outlets, and dead ground faults that cause total power loss or breaker tripping.",
        "highlights": [
            "Systematic branch-circuit isolation and fault localization using digital megohmmeters",
            "Locating melted, carbonized, or chewed wiring inside concealed PVC conduits",
            "Extracting burnt wires and pulling fresh flame-retardant multi-strand copper conductors",
            "Eliminating dangerous high-resistance arcing joints in ceiling junction boxes",
            "Full insulation resistance and dielectric integrity testing before re-energization"
        ],
        "included": [
            "Emergency power isolation and hazard containment at main distribution board",
            "Point-by-point continuity and resistance testing across all branch lines",
            "Opening ceiling rose, wall junction boxes, and switchboards to inspect wire insulation",
            "Cutting out melted wire segments and pulling fresh heat-resistant copper wires",
            "Soldering / insulated ferrule twisting and dual-layer heat shrink joint sealing",
            "Megger testing to confirm minimum 1 Megaohm insulation resistance to ground",
            "Restoring power and monitoring circuit load stability"
        ],
        "excluded": [
            "Major wall structural demolition to excavate crushed metal conduit pipes",
            "Fixing broken home appliances that caused the short circuit (repaired under appliance services)",
            "Utility provider meter-box external supply repair"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Emergency De-energization & Visual Hazard Audit",
                "description": "Electrician isolates the tripping sub-circuit, checks for smoke, burnt plastic odors, or scorch marks around outlets and junction boxes.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Branch Circuit Disconnection & Isolation",
                "description": "All devices on the affected line are unplugged, switchboards opened, and branch wires disconnected to isolate the exact faulted leg.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Megohmmeter Insulation Resistance Testing",
                "description": "Using high-voltage insulation tester (Megger), technician injects test voltage to pinpoint the phase-to-neutral or phase-to-earth dead short.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Burnt Segment Extraction & Rewiring",
                "description": "Carbonized wires are pulled out using steel fish tape; new certified FRLS (Flame Retardant Low Smoke) copper wires are drawn through the conduit.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Verification & Safe Power Restoration",
                "description": "Insulation resistance is re-verified, switchboards reassembled, and the circuit energized under controlled step-by-step observation.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital 500V/1000V insulation resistance megohmmeter (Megger)",
            "True-RMS digital multimeter with audible continuity beeper",
            "Flexible nylon/steel conduit wire puller (fish tape)",
            "VDE insulated 1000V cutters, strippers, and nose pliers",
            "FRLS copper wiring, self-amalgamating insulating tape, and wire connectors"
        ],
        "customer_setup": [
            "Unplug all electronics and appliances connected to the tripping or dead circuit",
            "Provide unobstructed access to all switchboards, ceiling fans, and junction boxes in the affected area",
            "Ensure emergency lighting/flashlights are available while power is isolated"
        ],
        "aftercare": [
            "Do not plug in the specific appliance that was running when the short circuit initially occurred until it is inspected",
            "Keep water away from all switchboards, especially in kitchens and bathrooms",
            "Notify the electrician if any burning plastic odor returns"
        ],
        "expected_results": [
            "Total elimination of short-circuit hazards and restoration of reliable power",
            "Fresh, flame-retardant wiring joints with zero risk of arcing or overheating",
            "Complete electrical safety certified by rigorous insulation resistance testing"
        ],
        "important_notes": [
            "Short circuits cause extreme instantaneous heat that can weaken surrounding wire insulation; thorough branch inspection is mandatory",
            "Carbon deposits inside conduit pipes are conductive and must be thoroughly cleaned before pulling new wires"
        ],
        "warranty": "30-day SmartServe warranty on repaired wiring joints and fault resolution",
        "faqs": [
            {
                "question": "What causes a short circuit in domestic home wiring?",
                "answer": "Common causes include worn insulation, rodent damage inside conduits, moisture ingress in outdoor/bathroom junction boxes, loose arcing terminals, or an internal breakdown in a plugged-in appliance."
            },
            {
                "question": "Why did my short circuit cause black scorch marks on the wall?",
                "answer": "When phase and neutral wires touch directly, an intense electrical arc occurs in milliseconds, vaporizing a tiny amount of copper and leaving carbon residue on nearby plastic or plaster."
            },
            {
                "question": "Do you have to break open the walls to fix a short circuit?",
                "answer": "In 95% of cases, no wall breaking is required. We locate the faulty conduit run and use steel fish tape to pull new insulated wires through existing concealed PVC pipes."
            },
            {
                "question": "How do I know if the short circuit was caused by an appliance or the house wiring?",
                "answer": "Our technician isolates the house wiring from all plugged-in devices. If the circuit holds power with devices unplugged, the fault lies within a specific appliance."
            }
        ],
        "dos": [
            "Immediately turn off the main switch if you see sparks, smoke, or smell burning plastic",
            "Call a certified electrician instead of trying to reset an aggressively sparking breaker"
        ],
        "donts": [
            "Never use water to put out an electrical spark or fire",
            "Never touch a scorched switchboard with bare hands"
        ],
        "tips": [
            "Installing an RCCB (Residual Current Circuit Breaker) detects insulation decay before it escalates into a catastrophic dead short circuit."
        ]
    },
    {
        "id": "3748da9b-511c-4a96-9ef8-712cc063fbf8",
        "name": "Socket Repair",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Electrician",
        "price": 209.0,
        "description": "Repair and replacement of loose, sparking, scorched, or non-functioning 6A and 16A power sockets, modular wall outlets, AC power boxes, and multi-pin plugs including internal contact tensioning, terminal screw tightening, and grounding verification.",
        "highlights": [
            "Diagnosis of dead sockets, intermittent power connection, and arcing plug pins",
            "Restoring brass socket contact spring tension to eliminate loose plug wobbling",
            "Replacement of melted, burnt, or cracked modular socket inserts (6A / 16A / 25A)",
            "Dedicated earth wire loop continuity check for complete shock prevention",
            "Flush modular faceplate re-alignment and secure backbox anchoring"
        ],
        "included": [
            "Switchboard power isolation and voltage verification",
            "Unscrewing modular faceplate and extracting internal socket module",
            "Inspecting copper conductors for thermal discoloration or loose clamping",
            "Tightening phase, neutral, and earth brass screw terminals to manufacturer torque",
            "Replacing defective socket module with brand-compatible modular insert if damaged",
            "Re-anchoring loose metal/PVC concealed backbox inside the wall cavity",
            "Live plug insertion test, contact grip check, and polarity voltage verification"
        ],
        "excluded": [
            "Pulling extensive new wiring from the distribution board over 3 meters",
            "Plastering large damaged wall cavities around recessed backboxes",
            "Repair of faulty appliance plugs that damaged the socket"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Voltage Test & Power Isolation",
                "description": "Electrician tests the socket with a neon probe, then turns off the room sub-circuit breaker to ensure zero live voltage.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Faceplate Removal & Internal Audit",
                "description": "Modular cover plate is unclipped; technician inspects wire terminal screws for signs of overheating, arcing, or burnt insulation.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Contact Re-tensioning or Module Replacement",
                "description": "If brass internal contacts are loose or plastic housing is melted, a new modular socket module is snapped into the grid plate.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Terminal Rewiring & Secure Clamping",
                "description": "Copper conductors are freshly stripped, inserted deep into terminal sleeves, and torqued down firmly to prevent resistance heating.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Polarity & Grounding Verification Test",
                "description": "Power is restored; socket tester verifies correct phase (right pin), neutral (left pin), and grounding pin continuity under load.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Socket polarity tester with LED trip status indicators",
            "VDE insulated 1000V screwdriver set and wire strippers",
            "True-RMS digital multimeter for ground-fault voltage testing",
            "Replacement 6A / 16A modular socket inserts and backbox anchor screws",
            "Heat-shrink tubing and electrical insulating tape"
        ],
        "customer_setup": [
            "Unplug all devices from the malfunctioning socket prior to technician arrival",
            "Provide access to the room switchboard and the main distribution panel",
            "Keep the brand/model of existing modular plates known if replacement is desired"
        ],
        "aftercare": [
            "Do not yank power cords from the cord; always grasp the solid plug head to remove",
            "Avoid inserting oversized foreign pins or cheap universal adapters that bend internal brass clips",
            "Never exceed the 6A socket rating with high-draw appliances like heaters or electric kettles"
        ],
        "expected_results": [
            "Firm, solid plug grip with zero electrical sparking or intermittent connection",
            "Verified proper polarity and active earth protection preventing shock hazards",
            "Flush, wobble-free wall socket plate neatly aligned with wall surface"
        ],
        "important_notes": [
            "Loose socket contacts generate localized electrical arcing that can ignite surrounding drywall or wallpaper",
            "Heavy heating appliances must always be connected to 16A or 25A power sockets with thick 2.5/4 sq mm wiring"
        ],
        "warranty": "30-day SmartServe electrical service warranty on workmanship and socket stability",
        "faqs": [
            {
                "question": "Why does my plug spark every time I insert or remove it from the socket?",
                "answer": "Sparking occurs when the internal brass contact leaves inside the socket have lost their spring tension or when inserting a plug while the appliance switch is already turned on."
            },
            {
                "question": "Can I replace a 6A socket with a 16A socket on the same wires?",
                "answer": "Only if the existing wires behind the wall are at least 2.5 sq mm thick and backed by a 16A MCB. Putting a 16A socket on thin 1.0 sq mm lighting wires is a fire hazard."
            },
            {
                "question": "Why does my plug feel hot after using it for 15 minutes?",
                "answer": "A warm or hot plug indicates loose terminal clamping screws or worn socket contact leaves that create high electrical resistance. It must be serviced immediately."
            },
            {
                "question": "Do you carry replacement sockets that match my home's modular brand?",
                "answer": "Our electricians carry common standard modular socket modules (Anchor, Roma, Havells, Legrand, Crabtree). Replacement parts are billed transparently at retail prices."
            }
        ],
        "dos": [
            "Ensure the switch is turned 'OFF' before plugging in or unplugging heavy appliances",
            "Use child-safety shuttered sockets in children's bedrooms and living rooms"
        ],
        "donts": [
            "Never use a socket that has visible black burn marks or cracked plastic casing",
            "Never force a 3-pin plug into a socket by breaking off the top grounding pin"
        ],
        "tips": [
            "If a 3-pin plug feels loose or falls out by gravity, the socket's internal brass contacts have worn out and need replacement."
        ]
    },
    {
        "id": "be562fbb-6fee-4c8a-af0c-fd12098bbead",
        "name": "Switch Repair",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Electrician",
        "price": 439.0,
        "description": "Precision diagnostic repair and replacement for jammed, sparking, loose, or non-responsive wall light switches, 16A geyser/AC power switches, 2-way staircase switches, bell pushes, and dimmer switches across all major modular and traditional switchboard brands.",
        "highlights": [
            "Restoring crisp mechanical switch actuation and eliminating internal arcing",
            "Replacement of burnt or stuck rocker modules with brand-compatible modular switches",
            "2-way staircase and corridor multi-point switching circuit diagnosis and rewiring",
            "Rotary fan speed dimmer switch replacement and capacitor bypass",
            "Tightening loose terminal screws to eliminate flickering lights and burnt smell"
        ],
        "included": [
            "Switchboard power isolation at the distribution box",
            "Prying open decorative modular cover plate without scratching wall paint",
            "Multimeter continuity and voltage testing across the defective switch terminals",
            "Disconnecting phase loop wiring and removing burnt/faulty switch module",
            "Snapping in certified replacement modular switch (6A / 16A / 20A DP)",
            "Stripping copper ends cleanly and tightening terminal clamping screws",
            "Testing mechanical actuation, load continuity, and re-mounting faceplate"
        ],
        "excluded": [
            "Replacing entire multi-gang switchboard concealed wooden or metal backbox",
            "Concealed wall wiring over 3 meters between two-way switch locations",
            "Appliance internal electronic relay or PCB repairs"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Fault Diagnosis & Circuit Identification",
                "description": "Electrician tests switch response, checks connected light/appliance, and isolates the room breaker to safely de-energize the switchboard.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Plate Extraction & Visual Inspection",
                "description": "Switchboard plate is unclipped; wiring harness is inspected for melted insulation, loose phase looping, or carbon buildup.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Defective Switch Module Replacement",
                "description": "Burnt or mechanically jammed switch is unclipped from the grid plate; genuine modular replacement is seated into position.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Phase Loop & Load Wire Termination",
                "description": "Live phase jumper wire and load conductor are inserted into switch terminals and torqued down firmly.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Re-energization & Operational Verification",
                "description": "Power is reconnected; switch is toggled multiple times under live load to verify crisp action and instant electrical response.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Insulated VDE 1000V screwdrivers and slim precision drivers",
            "Digital multimeter with continuity beeper and voltage sensor",
            "Non-marring plastic faceplate pry tool",
            "Wire strippers and high-temperature copper terminal ferrules",
            "Replacement 6A / 16A modular switches and 2-way modules"
        ],
        "customer_setup": [
            "Identify which specific switches on the board are malfunctioning or sticking",
            "Provide access to the room breaker box to allow brief power isolation",
            "Keep the switchboard area clear of wall hangings or furniture"
        ],
        "aftercare": [
            "Press switches with gentle, normal finger pressure rather than aggressive slapping",
            "Never operate wall switches with wet or damp hands",
            "If a switch feels spongy or makes a buzzing sound, have it replaced immediately"
        ],
        "expected_results": [
            "Smooth, crisp tactile rocker click with instantaneous electrical contact",
            "Complete elimination of light flickering, internal buzzing, and sparking",
            "Clean, perfectly flush modular switchboard appearance with zero gaps"
        ],
        "important_notes": [
            "A buzzing sound inside a switch indicates micro-arcing between worn silver-alloy contact pads that can cause electrical fires",
            "16A and 20A heavy appliance switches feature double-break mechanisms and must not be replaced with standard 6A lighting switches"
        ],
        "warranty": "30-day SmartServe electrical service warranty on workmanship and switch stability",
        "faqs": [
            {
                "question": "Why does my light switch make a buzzing or crackling noise when turned on?",
                "answer": "Buzzing is caused by eroded electrical contacts inside the switch creating a tiny continuous electrical arc. The switch has reached the end of its lifespan and must be replaced."
            },
            {
                "question": "Can the technician replace just one broken switch without changing the whole board?",
                "answer": "Yes. Modern modular switchboards allow individual switch modules to be unclipped and replaced independently, saving significant cost."
            },
            {
                "question": "What is a 2-way switch and how does it work?",
                "answer": "A 2-way switch setup allows you to control a single light (such as in a staircase or bedroom entrance/bedside) from two different locations using specialized traveler wires."
            },
            {
                "question": "Are replacement switches included in the service cost?",
                "answer": "The service covers complete diagnostic and installation labor. If replacement switch modules are needed, our technician provides compatible branded modular units at standard retail prices."
            }
        ],
        "dos": [
            "Use heavy-duty 16A/20A switches for high-wattage devices like geysers, microwaves, and room heaters",
            "Keep switchboards clean and free of kitchen grease and moisture"
        ],
        "donts": [
            "Never toggle a jammed switch forcefully; internal spring mechanisms can shatter",
            "Never spray liquid cleaning sprays directly onto electrical switchboards"
        ],
        "tips": [
            "Wiping switchboards with a dry microfiber cloth and rubbing alcohol applied to the cloth (never sprayed on the board) keeps them spotless safely."
        ]
    },
    {
        "id": "56002ee0-4407-40bb-8b83-e046a8887126",
        "name": "Switchboard Installation",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Electrician",
        "price": 509.0,
        "description": "Complete assembly, wiring, and installation of new residential modular switchboards (2-module to 18-module configurations) including metal/PVC backbox fitting, modular grid plate assembly, switch/socket gang termination, phase looping, and neutral-earth busbar wiring.",
        "highlights": [
            "Custom modular grid plate configuration (switches, 6A/16A sockets, fan regulators, USB chargers, indicator lamps)",
            "Systematic color-coded copper wiring layout with dedicated phase jumpers",
            "Recessed metal backbox or surface-mounted PVC gang box precision anchoring",
            "Low-impedance earth terminal bonding for all grounded 3-pin socket modules",
            "Laser level alignment ensuring perfectly straight, flush wall integration"
        ],
        "included": [
            "Site planning and marking switchboard position at ergonomic wall height",
            "Power isolation and testing existing conduit wire leads",
            "Securing modular concealed backbox or surface-mount gang box to the wall",
            "Snapping desired switches, sockets, dimmers, and blank plates into the grid frame",
            "Wiring internal phase distribution jumpers using 1.5 sq mm / 2.5 sq mm copper wire",
            "Terminating incoming phase, neutral, earth, and load conductors into designated modules",
            "Fastening grid plate, snapping decorative front cover, and testing all points"
        ],
        "excluded": [
            "Extensive brick wall chiseling or plastering over 2 meters for new concealed boxes",
            "Concealed conduit installation across multiple rooms",
            "Supply of modular switches, sockets, and faceplates (can be supplied at retail prices)"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Circuit De-energization & Safety Verification",
                "description": "Electrician isolates the circuit at the main breaker panel and verifies that all incoming conduit wires are de-energized.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Backbox Anchoring & Alignment",
                "description": "Concealed metal backbox or surface-mount PVC gang box is secured to the wall using heavy anchors and checked with a spirit level.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Modular Grid Assembly",
                "description": "Switches, 6A/16A sockets, fan regulators, and indicators are clicked into the modular metal/polycarbonate grid plate frame.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "Phase Looping & Conductor Termination",
                "description": "Phase jumper bus is wired across switches; neutral and earth wires are terminated into sockets; load lines are connected to respective switch outputs.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Faceplate Mounting & Multi-Point Load Test",
                "description": "Plate is screwed to backbox, decorative fascia snapped on, power restored, and every switch and socket tested with a load tester.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "VDE insulated 1000V screwdriver set and torque drivers",
            "Automatic wire stripper, crimping plier, and cable cutters",
            "Spirit bubble level and laser alignment line",
            "Digital multimeter and socket polarity tester",
            "Modular backbox anchor screws, wire connectors, and PVC sleeves"
        ],
        "customer_setup": [
            "Have the desired modular plate, switches, sockets, and regulators on site",
            "Clear furniture away from the wall area where the switchboard will be installed",
            "Ensure access to the main electrical panel for temporary power shutoff"
        ],
        "aftercare": [
            "Do not spray water or chemical cleaners directly onto the new switchboard",
            "Ensure the maximum connected load across the switchboard does not exceed circuit breaker capacity",
            "Operate switches gently to preserve mechanical spring longevity"
        ],
        "expected_results": [
            "Modern, sleek, perfectly aligned switchboard flush with the finished wall",
            "Clean, organized, professional internal wiring with zero loose connections or fire risks",
            "Reliable, independent control over all room lighting, fans, and power appliances"
        ],
        "important_notes": [
            "High-power 16A sockets on the board must have dedicated 2.5 sq mm or 4.0 sq mm phase, neutral, and earth lines",
            "Never mix raw utility phase with inverter backup phase on the same physical switch"
        ],
        "warranty": "60-day SmartServe electrical installation warranty covering mounting stability and wiring connections",
        "faqs": [
            {
                "question": "What is the standard ergonomic height for installing a room switchboard?",
                "answer": "Standard light switchboards are installed at 1200mm to 1350mm (approx. 4 to 4.5 feet) above finished floor level for easy, comfortable reach."
            },
            {
                "question": "Can I have both regular grid power and inverter backup power on the same switchboard?",
                "answer": "Yes. Our electrician will separate the phase loops internally so that selected switches run on inverter backup while high-power sockets remain on the main grid line."
            },
            {
                "question": "How many modules can fit on a standard room switchboard?",
                "answer": "Modular plates come in 1, 2, 3, 4, 6, 8, 12, and 18-module sizes. A standard switch takes 1 module, while a 16A socket or fan regulator typically occupies 2 modules."
            },
            {
                "question": "Does this service include replacing an old wooden switchboard with a new modular plate?",
                "answer": "Yes. We can replace old wooden switchboards with modern surface-mount modular conversion boxes or retrofit modular plates."
            }
        ],
        "dos": [
            "Plan your switch and socket layout based on actual room appliance usage",
            "Use certified flame-retardant polycarbonate modular plates for long-lasting safety"
        ],
        "donts": [
            "Never overcrowd a small backbox with excessive thick wires, which causes overheating",
            "Never leave empty module slots uncovered; always install blank filler plates"
        ],
        "tips": [
            "Installing a switchboard with integrated USB-C charging ports eliminates bulky wall adapters beside your bed or study desk."
        ]
    },
    {
        "id": "33dee26e-c069-475d-92fe-a21278a5d020",
        "name": "Wiring Repair",
        "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
        "subcategory": "Electrician",
        "price": 369.0,
        "description": "Comprehensive electrical wiring diagnostic and restoration service to repair snapped, chewed, overheated, or severed copper wires inside concealed conduits, ceiling junction boxes, open surface casings, and distribution panels without damaging wall plaster.",
        "highlights": [
            "Conduit wire fault tracing and continuity mapping using signal tone generators",
            "Extracting damaged, rodent-chewed, or degraded aluminum/copper conductors",
            "Pulling high-conductivity FRLS (Flame Retardant Low Smoke) multi-strand copper wires",
            "Soldering / crimped copper ferrule splicing with double-layer heat-shrink insulation",
            "Insulation resistance (Megger) verification ensuring total dielectric strength"
        ],
        "included": [
            "Isolating circuit breaker and testing for zero line voltage",
            "Opening ceiling roses and wall junction boxes along the affected wiring run",
            "Using steel fish tape to locate blockages or severed wire points within conduits",
            "Drawing fresh multi-strand copper cables through existing conduit pathways",
            "Creating secure, low-resistance staggered splices with insulated compression ferrules",
            "Applying dual-wall heat-shrink tubing and high-grade electrical tape over joints",
            "Testing circuit continuity, phase-neutral resistance, and load operation"
        ],
        "excluded": [
            "Complete whole-house rewiring (quoted as a comprehensive civil/electrical project)",
            "Chiseling concrete slabs or structural beams to lay new conduit pipes",
            "Repair of burnt external utility pole service lines"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Circuit De-energization & Continuity Mapping",
                "description": "Electrician isolates the breaker, verifies zero voltage, and uses a digital multimeter to map open circuits and broken wire segments.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Junction Box Access & Wire Extraction",
                "description": "Intermediate junction boxes are opened; damaged or carbonized wires are disconnected and carefully extracted from the conduit.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Steel Fish Tape Pulling",
                "description": "Flexible steel fish tape is threaded through the conduit run, and new certified FRLS copper wires are securely hitched.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Permanent Splicing & Heat-Shrink Sealing",
                "description": "New conductors are spliced using staggered crimp ferrules and sealed with flame-retardant heat-shrink sleeves to prevent arcing.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Insulation Resistance & Re-energization Test",
                "description": "Megger testing confirms insulation resistance > 1 Megaohm; power is restored and voltage checked at all downstream fixtures.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital True-RMS multimeter and wire tracer / toner kit",
            "High-tensile flexible steel and nylon conduit fish tape",
            "VDE insulated 1000V wire strippers and ratcheting ferrule crimper",
            "Dual-wall adhesive-lined heat shrink tubing and industrial heat gun",
            "Certified FRLS multi-strand copper wiring (1.0, 1.5, 2.5, 4.0 sq mm)"
        ],
        "customer_setup": [
            "Clear access below ceiling junction boxes and wall switchboards in the affected area",
            "Turn off and unplug computers and sensitive electronics on the circuit",
            "Ensure alternative temporary lighting is available if repair spans evening hours"
        ],
        "aftercare": [
            "Do not exceed the designated circuit amperage rating with extra high-wattage appliances",
            "Keep moisture and water leakage away from walls containing electrical conduits",
            "Seal any visible conduit entry points in ceiling voids to prevent rodent entry"
        ],
        "expected_results": [
            "Flawless electrical continuity and stable voltage restored to all room outlets",
            "Elimination of intermittent power cuts, dimming lights, and sparking risks",
            "Safe, fire-retardant wiring joints complying with national electrical safety standards"
        ],
        "important_notes": [
            "Wire joints should ideally be housed inside accessible junction boxes rather than buried inaccessible inside conduits",
            "Rodent-damaged wires must be replaced entirely along the damaged segment, not simply patched with tape"
        ],
        "warranty": "30-day SmartServe electrical service warranty on repaired wiring joints and circuit stability",
        "faqs": [
            {
                "question": "How do you pull new wires through walls without damaging paint or plaster?",
                "answer": "We utilize existing concealed PVC conduit pipes embedded inside your walls. By attaching new cables to steel fish tape or the old wires, we draw them through cleanly without wall breaking."
            },
            {
                "question": "What is FRLS wire and why is it important?",
                "answer": "FRLS stands for Flame Retardant Low Smoke. In the event of an electrical short circuit, FRLS insulation resists catching fire and emits minimal toxic smoke, protecting home occupants."
            },
            {
                "question": "Why did my concealed wires get damaged inside the wall?",
                "answer": "Common reasons include continuous electrical overloading that melts insulation, moisture leaking from plumbing pipes into electrical conduits, or rats chewing through conduit wiring."
            },
            {
                "question": "Can aluminum wiring be connected directly to copper wiring?",
                "answer": "Directly twisting copper and aluminum wires causes galvanic corrosion and fire hazards. If transitioning between metals, specialized bi-metallic connector lugs must be used."
            }
        ],
        "dos": [
            "Always choose multi-strand electrolytic copper wiring with certified FRLS insulation",
            "Label your distribution board circuit breakers clearly for easy future identification"
        ],
        "donts": [
            "Never join wires using simple loose electrical tape twists without proper crimping or wire nuts",
            "Never run electrical wires inside the same conduit pipe as plumbing or gas lines"
        ],
        "tips": [
            "Using color-coded wiring (Red for Phase, Black for Neutral, Green for Earth) ensures fast, safe maintenance for years to come."
        ]
    }
]
