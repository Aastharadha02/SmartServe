# Kitchen Appliance Services Data (16 Services)
# Category: 4. AC, Appliance & Electronics Repair

KITCHEN_APPLIANCE_SERVICES = [
    # --- SUBCATEGORY: Chimney (3 Services) ---
    {
        "id": "0e679aa3-8060-41b3-99c9-a68403b381c9",
        "name": "Chimney Cleaning",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Chimney",
        "price": 499.0,
        "description": "Deep chemical degreasing and carbon removal service for kitchen chimneys including baffle and mesh filter immersion, blower turbine fan descaling, grease collection cup clearing, and stainless steel exterior polishing.",
        "highlights": [
            "Heavy-duty chemical immersion tank degreasing for baffle and mesh filters",
            "Blower turbine wheel and motor housing grease scraping and hot wash",
            "Oil collector tray de-sludging and anti-bacterial sanitization",
            "Duct pipe joint inspection and grease leakage sealing",
            "Exterior stainless steel and tempered glass canopy scratch-free buffing"
        ],
        "included": [
            "Baffle/mesh filter removal and caustic-free deep degreasing soak",
            "Suction blower impeller fan cleaning and static balance check",
            "Oil collector tray emptying and chemical sanitization",
            "Internal chimney motor chamber wipe down",
            "External canopy, touch panel, and LED housing polishing",
            "Airflow suction test and noise level verification"
        ],
        "excluded": [
            "Replacement of damaged exhaust flexible aluminum duct pipe",
            "Exhaust fan motor rewinding or electronic PCB touch sensor repair",
            "Civil wall cutting or exterior duct weather louvre replacement"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Suction & Motor Test",
                "description": "Technician tests chimney suction across all speed levels, checking motor hum and push-button/gesture sensor response.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Filter & Oil Cup Dismounting",
                "description": "Baffle filters and oil collector cups are dismounted and submerged in an intensive grease-dissolving solution.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Blower Turbine & Chamber Degreasing",
                "description": "Internal blower wheel is treated with professional degreaser foam to remove sticky oil deposits that cause motor drag.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Rinsing & Filter Drying",
                "description": "Filters and turbine wheel are high-pressure rinsed with hot water, dried, and inspected for complete oil clearance.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Reassembly & Suction Demonstration",
                "description": "Chimney is reassembled; technician demonstrates powerful suction recovery using a paper suction test sheet.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Commercial biodegradable food-safe degreaser concentrate",
            "Immersion soaking basin and brass bristle filter brushes",
            "Microfiber cloths and stainless steel polish",
            "Anemometer suction velocity gauge",
            "Protective work mat to shield the kitchen stovetop"
        ],
        "customer_setup": [
            "Clear items and cookware off the cooktop / gas stove directly beneath the chimney",
            "Provide access to hot running water in the kitchen sink",
            "Ensure electric power supply to the chimney is active"
        ],
        "aftercare": [
            "Wipe grease off baffle filters once every 15 days using warm soapy water",
            "Empty the transparent oil collection cup before it overflows",
            "Operate chimney on low speed for 5 minutes after cooking to purge residual fumes"
        ],
        "expected_results": [
            "Full restoration of rated suction capacity (up to 1200+ m3/hr)",
            "Noticeable reduction in motor strain and cooking smoke in the kitchen",
            "Sparkling, oil-free canopy surface and clean baffle airflow"
        ],
        "important_notes": [
            "Heavy commercial-grade deep frying may require monthly baffle filter soaking",
            "Auto-clean chimneys still require manual deep cleaning of the internal blower housing twice a year"
        ],
        "warranty": "30-day SmartServe service guarantee on cleaning quality and suction performance",
        "faqs": [
            {
                "question": "How often does a kitchen chimney need professional deep cleaning?",
                "answer": "For typical Indian cooking with spices and oils, deep cleaning is recommended once every 3 to 4 months."
            },
            {
                "question": "Does this service protect my gas stove and kitchen counter?",
                "answer": "Yes, our technicians lay heavy protective plastic sheets over your stove and counter before starting any degreasing."
            },
            {
                "question": "Does my auto-clean chimney still need manual cleaning?",
                "answer": "Yes. Auto-clean melts oil from the heating element into the collector, but filters, blower blades, and duct joints still accumulate sticky grease over time."
            },
            {
                "question": "How long does a chimney deep cleaning take?",
                "answer": "A thorough chimney deep degreasing service takes approximately 60 to 75 minutes."
            }
        ],
        "dos": [
            "Empty the oil collection cup regularly to avoid greasy drips onto your cooktop",
            "Turn on the chimney 1 minute before turning on gas burners to establish an upward air draft"
        ],
        "donts": [
            "Do not use abrasive steel scrubbers on delicate tempered glass or touch panels",
            "Do not operate the chimney without baffle filters firmly locked in position"
        ],
        "tips": [
            "Keep kitchen windows partially cracked open when running high-suction chimneys to maintain proper makeup air"
        ]
    },
    {
        "id": "a8349965-62cf-4087-9b75-c97f0c8b9cc5",
        "name": "Chimney Repair",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Chimney",
        "price": 459.0,
        "description": "Expert diagnostic and component repair for all chimney issues including motor failure to start, abnormal screeching noises, touch panel or gesture sensor malfunction, broken LED lamps, and weak suction.",
        "highlights": [
            "Multi-point diagnostic covering motor winding resistance and capacitor rating",
            "Touch panel, push button, and gesture control PCB circuit board troubleshooting",
            "Blower wheel alignment and bearing shaft replacement to eliminate grinding noises",
            "Auto-clean heating element and thermal fuse testing",
            "Genuine OEM replacement parts with transparent upfront pricing"
        ],
        "included": [
            "Thorough motor, PCB, and wiring harness inspection",
            "Run capacitor capacitance test and replacement recommendation",
            "Touch screen controller and optical gesture sensor calibration",
            "LED illumination bulb and transformer circuit check",
            "Blower housing clearance and blade balance adjustment",
            "Post-repair continuous run test under all speed settings"
        ],
        "excluded": [
            "Cost of new motor, PCB controller, or replacement glass canopy",
            "Replacement of external flexible exhaust ducting",
            "Masonry cutting or kitchen cabinet alterations"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Symptom Diagnosis & Electrical Safety Check",
                "description": "Technician tests supply voltage, grounds, and isolates whether fault originates in PCB, motor, or switch assembly.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "PCB & Sensor Continuity Testing",
                "description": "Digital multimeter tests touch membrane switches, wave sensors, and low-voltage DC power supply tracks.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Motor & Capacitor Health Probing",
                "description": "Starting capacitor microfarads and motor winding resistance are verified for electrical shorts or open circuits.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Defective Part Replacement & Calibration",
                "description": "Faulty components (capacitor, sensor, switch, or wiring) are replaced with genuine compatible parts.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Load Test & Customer Demonstration",
                "description": "Chimney is run across low, medium, and high speeds; zero vibration and smooth operation are confirmed.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital true-RMS multimeter and capacitance meter",
            "Precision insulated screwdriver set",
            "Heat shrink tubing and wire terminal crimpers",
            "Bearing puller and motor shaft alignment tools",
            "Suction verification paper sheet"
        ],
        "customer_setup": [
            "Clear stove below the chimney and make electrical socket accessible",
            "Keep appliance invoice or model number sticker accessible",
            "Describe when the fault first appeared (e.g. following a power surge or oil spill)"
        ],
        "aftercare": [
            "Avoid splashing water directly on touch controls while wiping the kitchen wall",
            "Service filters regularly to prevent grease from penetrating the motor bearings",
            "Use a surge protector if your area experiences voltage spikes"
        ],
        "expected_results": [
            "Immediate resolution of non-starting, noisy, or unresponsive chimney faults",
            "Smooth, quiet motor rotation without vibration or rattles",
            "Reliable touch and gesture control responsiveness"
        ],
        "important_notes": [
            "Replacement motors and proprietary PCBs are billed separately after quote approval",
            "Burned motor windings require full motor assembly replacement rather than on-site repair"
        ],
        "warranty": "30-day SmartServe warranty on repair labor and installed components",
        "faqs": [
            {
                "question": "Why is my chimney motor humming loudly but the fan does not spin?",
                "answer": "This is almost always caused by a blown starting capacitor or oil-seized motor bearings. Replacing the capacitor usually restores normal rotation."
            },
            {
                "question": "Why does my touch panel not respond to hand gestures?",
                "answer": "Gesture sensors fail when infrared lenses get coated in grease or when the control PCB suffers a voltage surge. Cleaning or sensor replacement resolves it."
            },
            {
                "question": "Can your technician repair my chimney on the same day?",
                "answer": "Yes, common repairs involving capacitors, switches, wiring, and standard sensors are completed on the same visit."
            },
            {
                "question": "Are replacement spare parts covered under warranty?",
                "answer": "Yes, all genuine replacement parts supplied by SmartServe carry a 30 to 90 day warranty."
            }
        ],
        "dos": [
            "Turn off the power switch immediately if you hear burning smells or grinding sounds",
            "Keep the chimney warranty card handy if within manufacturer warranty"
        ],
        "donts": [
            "Do not spray liquid cleaning agents directly into the motor housing",
            "Do not force stuck push buttons with heavy pressure"
        ],
        "tips": [
            "Clean filters regularly; heavy grease loads make the motor work twice as hard, cutting motor lifespan in half"
        ]
    },
    {
        "id": "16d73b61-3c7e-4c61-bc62-97b93a04ef7f",
        "name": "Installation",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Chimney",
        "price": 499.0,
        "description": "Professional wall-mounted or island kitchen chimney installation including precision template marking, structural masonry anchoring, exhaust duct pipe routing, electrical connection, and optimal height alignment above the cooktop.",
        "highlights": [
            "Laser-leveled wall bracket anchoring ensuring zero tilt and vibration-free mounting",
            "Optimal clearance calibration (65-75 cm above gas cooktop) for peak safety and suction",
            "Flexible aluminum exhaust duct pipe connection with air-tight foil tape sealing",
            "Stainless steel decorative cowl / chimney stack fitting and alignment",
            "Complete electrical grounding and full-speed suction airflow verification"
        ],
        "included": [
            "Unboxing and physical inspection of chimney unit and components",
            "Wall template marking and heavy-duty anchor drilling",
            "Mounting bracket installation and chimney body securement",
            "Exhaust duct pipe clamping to chimney blower outlet",
            "Connecting duct pipe to existing external wall exhaust hole",
            "Fitting decorative stainless steel duct cover cowl",
            "Full operational testing across all speeds and lighting modes"
        ],
        "excluded": [
            "Masonry core drilling for new 6-inch exterior wall exhaust hole",
            "Cost of flexible aluminum duct pipe or PVC exhaust cowls if not in box",
            "Carpentry cutting on overhead kitchen wooden cabinets",
            "Dedicated 6A/16A electrical switchboard installation"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Kitchen Site Inspection & Height Marking",
                "description": "Technician measures height above cooktop (recommended 65-75 cm), checks wall load capability, and marks hole positions using template.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Wall Bracket Anchoring",
                "description": "Masonry holes are drilled with rotary hammer; steel expansion anchors and mounting brackets are fixed with bubble-level alignment.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Chimney Mounting & Level Check",
                "description": "Chimney hood is hung on the brackets, verified for zero wobble, and locked in position with secondary safety screws.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Exhaust Duct Pipe Attachment",
                "description": "Flexible aluminum duct is clamped onto the one-way air flap valve and sealed with reinforced aluminum foil tape.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Decorative Cowl Fitting & Test Run",
                "description": "Telescopic stainless steel chimney stack is fitted; power is connected and smoke suction is demonstrated.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Rotary hammer drill and masonry carbide drill bits",
            "Precision spirit bubble level and measuring tape",
            "Stainless steel anchor fasteners and wall plugs",
            "Heavy-duty aluminum foil duct tape and worm-drive hose clamps",
            "Cooktop protective drop cloth"
        ],
        "customer_setup": [
            "Ensure chimney carton and unboxed unit are present in the kitchen",
            "Verify that a 6-inch exterior wall outlet hole already exists",
            "Ensure a grounded 6A/16A electrical socket is within 1 meter of mounting point"
        ],
        "aftercare": [
            "Allow silicone seals to cure for 2 hours before heavy frying",
            "Peel off any remaining blue protective plastic film from stainless steel surfaces",
            "Avoid placing high-flame burners directly below unshielded duct tape"
        ],
        "expected_results": [
            "Sturdy, completely vibration-free wall anchoring",
            "Maximum smoke and fume capture at the correct ergonomic height",
            "Clean, sleek aesthetic integration with kitchen cabinets"
        ],
        "important_notes": [
            "Mounting lower than 65 cm above a gas stove creates a severe fire hazard from high flames",
            "Duct runs longer than 10 feet or with more than two 90-degree bends will reduce suction efficiency"
        ],
        "warranty": "60-day SmartServe installation warranty covering mounting stability and duct joint seals",
        "faqs": [
            {
                "question": "What is the ideal height to install a kitchen chimney?",
                "answer": "For gas stoves, the ideal distance between the cooktop and chimney bottom is 65 cm to 75 cm (26 to 30 inches) to balance suction and fire safety."
            },
            {
                "question": "Does installation include drilling the wall exhaust hole?",
                "answer": "No, core drilling through exterior brick or concrete walls is a civil masonry service available as an optional add-on."
            },
            {
                "question": "Can a chimney be installed if I have overhead kitchen cabinets?",
                "answer": "Yes, but internal cabinet shelf cutouts must be completed prior to chimney mounting so the duct pipe can pass through."
            },
            {
                "question": "How long does chimney installation take?",
                "answer": "Standard wall-mounted chimney installation takes approximately 60 to 90 minutes."
            }
        ],
        "dos": [
            "Keep the flexible duct pipe as straight and short as possible for maximum suction",
            "Ensure an exterior louvered vent cap is fitted to stop birds and insects from entering"
        ],
        "donts": [
            "Do not install the chimney lower than 65 cm above gas burners",
            "Do not use fragile plastic tape to seal hot exhaust duct joints"
        ],
        "tips": [
            "Use rigid or semi-rigid aluminum ducting rather than corrugated plastic for superior airflow and lower noise"
        ]
    },

    # --- SUBCATEGORY: Microwave (3 Services) ---
    {
        "id": "fafbf501-0b2f-4079-b71d-965537fc5065",
        "name": "General Servicing",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Microwave",
        "price": 499.0,
        "description": "Comprehensive preventative maintenance and hygiene servicing for solo, grill, and convection microwave ovens including high-voltage safety inspection, microwave leakage radiation audit, turntable motor check, cavity descaling, and deodorization.",
        "highlights": [
            "Electronic microwave radiation leakage test around door perimeter seals",
            "High-voltage capacitor discharge and grounding safety audit",
            "Turntable roller guide, drive coupler, and motor torque check",
            "Mica waveguide cover inspection to prevent electrical arcing and sparking",
            "Food-grade steam cavity descaling and interior enamel sanitization"
        ],
        "included": [
            "High-frequency RF radiation leakage scan using calibrated detector",
            "Cavity interior deep cleaning and baked-on food splatter removal",
            "Turntable glass plate, roller ring, and rotating shaft servicing",
            "Cooling fan ventilation grill dust removal",
            "Door latch switch alignment and safety interlock test",
            "Convection heating element and fan blower test (if convection model)",
            "Post-service water heating performance test"
        ],
        "excluded": [
            "Replacement of failed magnetron tube, transformer, or main PCB",
            "Replacement of broken glass turntable or outer door glass",
            "Rust treatment or structural enamel re-coating"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Safety & Radiation Leakage Audit",
                "description": "Technician tests oven with a digital microwave survey meter to verify zero radiation escapes past door gaskets.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Cavity Food-Grade Steam Cleansing",
                "description": "Interior walls, ceiling, and quartz grill elements are treated with non-toxic citrus steam cleaner to dissolve stubborn grease.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Waveguide & Mica Plate Inspection",
                "description": "Mica waveguide cover is inspected for burns, grease saturation, or carbon marks that trigger dangerous sparking.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Turntable & Ventilation Servicing",
                "description": "Turntable drive motor coupler is cleaned and tested; cooling fan vents are blown clean of lint.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Standard Heating Benchmark Test",
                "description": "100ml water cup is boiled for 60 seconds; temperature rise is verified against factory wattage ratings.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Calibrated microwave RF radiation leakage detector",
            "High-voltage safety discharge probe",
            "Food-safe enzymatic cavity cleaning solution",
            "Digital thermometer and graduated water beaker",
            "Microfiber sanitizing cloths and vent cleaning brushes"
        ],
        "customer_setup": [
            "Provide clear counter space around the microwave",
            "Ensure power supply outlet is functional and grounded",
            "Remove personal food containers from the cavity"
        ],
        "aftercare": [
            "Always cover food with a microwave-safe ventilated lid to avoid ceiling splatters",
            "Wipe interior walls with a damp cloth immediately after heating greasy food",
            "Leave the door slightly ajar for 10 minutes after cooking to allow steam to vent"
        ],
        "expected_results": [
            "Certified radiation-safe kitchen operation",
            "Fast, even heating with zero food contamination or stale odors",
            "Smooth, silent turntable rotation without stuttering"
        ],
        "important_notes": [
            "Microwave ovens store lethal 2,000V+ charges in high-voltage capacitors even when unplugged; DIY internal opening is strictly hazardous",
            "A burnt or blackened mica sheet must be replaced immediately to protect the magnetron"
        ],
        "warranty": "30-day SmartServe service guarantee on servicing and radiation safety",
        "faqs": [
            {
                "question": "Can microwave radiation leak into my kitchen?",
                "answer": "Damaged door seals, loose hinges, or warped latches can cause micro-leakage. Our service includes an electronic RF radiation meter scan to confirm 100% containment."
            },
            {
                "question": "Why does my microwave spark when turned on?",
                "answer": "Sparking is commonly caused by metal foil, a burnt mica waveguide cover saturated with food oil, or chipped cavity enamel."
            },
            {
                "question": "How often should a microwave oven be serviced?",
                "answer": "A general safety and hygiene service is recommended annually for residential microwave ovens."
            },
            {
                "question": "How long does general microwave servicing take?",
                "answer": "General servicing and safety testing take approximately 30 to 45 minutes."
            }
        ],
        "dos": [
            "Use only certified microwave-safe glass, ceramic, or BPA-free plastic cookware",
            "Unplug the microwave if unusual buzzing or ozone electrical smells are noticed"
        ],
        "donts": [
            "Never operate the microwave when completely empty; this damages the magnetron",
            "Never insert metal utensils, aluminum foil, or gold-rimmed plates"
        ],
        "tips": [
            "Place a slice of lemon in a cup of water and microwave for 2 minutes to naturally loosen dried food grime before wiping"
        ]
    },
    {
        "id": "0757ef7e-c09f-4f78-8311-c056e7c6f2bf",
        "name": "Installation",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Microwave",
        "price": 499.0,
        "description": "Professional setup and installation of countertop, over-the-range, or built-in kitchen cabinetry microwave ovens including ventilation clearance validation, leveling, electrical grounding check, and complete feature demonstration.",
        "highlights": [
            "Precision bracket mounting for built-in or over-the-range microwave units",
            "Mandatory 10-15 cm ventilation clearance verification to prevent magnetron overheating",
            "Electrical line load and 16A grounding pin safety verification",
            "Turntable alignment, roller ring positioning, and door swing clearance check",
            "Complete operational demo of cooking, defrosting, and convection modes"
        ],
        "included": [
            "Unboxing and inspection for shipping damage or door seal warping",
            "Countertop positioning or built-in cabinet frame alignment",
            "Rear and side exhaust ventilation clearance check",
            "Turntable glass plate and roller guide assembly",
            "Dedicated 16A socket voltage and earthing test",
            "Initial heating test with water load",
            "Customer walkthrough of microwave controls, timers, and power levels"
        ],
        "excluded": [
            "Cabinet carpentry cutting or custom acrylic trim kit fabrication",
            "New dedicated 16A electrical socket wiring from MCB box",
            "Exhaust duct hole cutting for over-the-range ducted models"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Unboxing & Structural Inspection",
                "description": "Unit is inspected for transit dents, door hinge alignment, and secure latch engagement.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Ventilation Clearance & Placement",
                "description": "Microwave is set with adequate air gaps (at least 10 cm behind and above) to prevent cooling fan suffocation.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Electrical Supply & Earthing Check",
                "description": "Technician tests the 16A socket with a digital tester to ensure proper neutral and safety ground grounding.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Turntable Assembly & Heating Run",
                "description": "Roller ring and glass tray are assembled; microwave runs a 30-second water heat test to verify magnetron ignition.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Customer Demonstration & Handover",
                "description": "Technician explains power level adjustments, defrost settings, child lock, and recommended cookware.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital true-RMS electrical socket tester",
            "Spirit bubble level",
            "Microwave leakage radiation survey meter",
            "Precision screwdriver set",
            "Water testing beaker"
        ],
        "customer_setup": [
            "Have microwave unboxed or keep original box in the kitchen",
            "Provide a functioning, dedicated 16A 3-pin power socket nearby",
            "Clear kitchen countertop space or built-in cabinet cavity"
        ],
        "aftercare": [
            "Do not place decorative cloth covers directly over the top ventilation louvers",
            "Keep microwave at least 3 feet away from radios and TVs to prevent RF interference",
            "Ensure the 3-pin power plug is always plugged firmly into the socket"
        ],
        "expected_results": [
            "Safe, thermally stable installation with zero danger of electronic overheating",
            "Perfect door alignment and smooth latch release",
            "Clear understanding of all microwave cooking features and safety rules"
        ],
        "important_notes": [
            "Microwaves must never share an extension cord or multi-plug adapter with other heavy appliances",
            "Built-in models require adequate cabinet ventilation slots"
        ],
        "warranty": "60-day SmartServe installation warranty covering alignment and electrical connections",
        "faqs": [
            {
                "question": "Can I plug my microwave into a standard 5A household socket?",
                "answer": "No. Microwave ovens draw between 1100W and 2200W (especially convection models) and require a dedicated 16A power socket to avoid burnt plugs."
            },
            {
                "question": "Why is ventilation space around the microwave so important?",
                "answer": "The magnetron and high-voltage transformer generate significant heat. Inadequate ventilation causes premature thermal cutoff or component burnout."
            },
            {
                "question": "Does installation include building custom kitchen cabinetry?",
                "answer": "No, carpentry cabinet alterations must be handled by a carpenter before microwave installation."
            },
            {
                "question": "How long does installation take?",
                "answer": "Countertop installation and full customer demonstration take approximately 30 to 45 minutes."
            }
        ],
        "dos": [
            "Maintain at least 4 inches (10 cm) of air space above and behind the microwave",
            "Always operate using a dedicated 16A wall outlet with proper electrical grounding"
        ],
        "donts": [
            "Do not operate using flimsy extension power cords",
            "Do not place heat-generating toasters or electric kettles directly against the microwave vents"
        ],
        "tips": [
            "Activate the child safety lock feature when small children are around the kitchen"
        ]
    },
    {
        "id": "0b61170b-60c2-42a9-8aac-2b81439ac5c3",
        "name": "Microwave Repair",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Microwave",
        "price": 449.0,
        "description": "Expert diagnostic and component repair for all microwave oven malfunctions including failure to heat, sparking inside the cavity, dead display panel, un-rotating turntable, faulty door safety switches, and blown fuses.",
        "highlights": [
            "High-voltage system diagnostics: magnetron, high-voltage diode, and capacitor testing",
            "Sparking diagnosis and mica waveguide cover burn replacement",
            "Microcontroller PCB touch membrane and display repair",
            "Door interlock safety micro-switch alignment and replacement",
            "Turntable synchronous motor and drive coupler troubleshooting"
        ],
        "included": [
            "Complete electrical safety discharge and symptom diagnosis",
            "Magnetron cathode-to-anode continuity and filament resistance test",
            "High-voltage diode and capacitor capacitance verification",
            "Main electronic controller board input/output power probing",
            "Door interlock primary and secondary microswitch alignment",
            "Turntable motor voltage supply test",
            "Post-repair microwave radiation leakage and heating test"
        ],
        "excluded": [
            "Cost of replacement magnetron tube, transformer, or PCB assembly",
            "Turntable glass plate or door glass replacement",
            "Enamel cavity corrosion repainting"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Safety Discharge & Symptom Analysis",
                "description": "Technician isolates microwave from mains power and safely discharges high-voltage capacitor using 20kV grounding resistor.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "High-Voltage Circuit Probing",
                "description": "Magnetron, HV diode, and transformer windings are metered with high-range multimeter to isolate heating failure.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Interlock & Microswitch Audit",
                "description": "Door latch microswitches are inspected for pitted contact points or mechanical misalignments that prevent starting.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "Component Replacement & Waveguide Inspection",
                "description": "Defective components (magnetron, diode, fuse, switch, or mica sheet) are replaced with genuine compatible parts.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Radiation Leakage & Full Heat Test",
                "description": "Oven is reassembled; RF radiation detector confirms zero seal leakage; water heating test confirms rapid boiling.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Certified high-voltage discharge probe (20kV rated)",
            "True-RMS digital multimeter and HV diode tester",
            "Microwave RF radiation leakage survey meter",
            "Anti-static technician hand tools",
            "OEM-grade mica waveguide sheets and high-voltage fuses"
        ],
        "customer_setup": [
            "Describe the fault clearly (e.g. sparking, buzzing noise, runs but doesn't heat)",
            "Keep appliance invoice or model number accessible",
            "Ensure countertop workspace is well-lit and clear"
        ],
        "aftercare": [
            "Keep the interior clean and free of grease to prevent future high-voltage arcing",
            "Never run the microwave with metal utensils or twist ties",
            "Use a voltage stabilizer if your building suffers severe voltage drops"
        ],
        "expected_results": [
            "Restoration of rapid, uniform food heating capability",
            "Complete elimination of dangerous electrical arcing and sparking",
            "Safe, certified radiation-tight door seal operation"
        ],
        "important_notes": [
            "Replacement parts such as magnetrons, PCBs, and transformers are billed separately upon customer approval",
            "Never attempt DIY repair on microwave internals due to fatal high-voltage capacitor shock hazards"
        ],
        "warranty": "30-day SmartServe warranty on repair labor and installed components",
        "faqs": [
            {
                "question": "Why does my microwave run normally but not heat the food at all?",
                "answer": "This is the classic symptom of a failed magnetron, a shorted high-voltage diode, or a blown high-voltage fuse. Our technician can identify and replace the exact failed part."
            },
            {
                "question": "Is it worth repairing an older microwave or should I buy a new one?",
                "answer": "If the issue is a blown fuse, door microswitch, or diode, repair is very affordable. If the magnetron or PCB on a very old basic solo model fails, the technician will advise on cost effectiveness."
            },
            {
                "question": "Can your technician replace a sparking mica sheet on the spot?",
                "answer": "Yes, our technicians carry precut universal OEM-grade mica waveguide sheets for immediate on-site replacement."
            },
            {
                "question": "How long does a microwave repair take?",
                "answer": "Standard diagnostics and component replacements take approximately 40 to 60 minutes."
            }
        ],
        "dos": [
            "Unplug the microwave immediately if you see sparks or smell burning electronics",
            "Verify that technician tests radiation containment with an RF detector before leaving"
        ],
        "donts": [
            "Never attempt to open the microwave outer metal cabinet yourself",
            "Never bypass a blown high-voltage fuse with copper wire"
        ],
        "tips": [
            "Always wipe condensation off the door glass after boiling liquids to preserve the door seal gasket"
        ]
    },

    # --- SUBCATEGORY: RO / Water Purifier (5 Services) ---
    {
        "id": "f5ad4ddb-97be-4fdb-a832-3e92f0fd66d7",
        "name": "Filter Replacement",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "RO / Water Purifier",
        "price": 499.0,
        "description": "Complete scheduled multi-stage filter replacement for domestic RO water purifiers including sediment filter, activated carbon block, RO membrane, post-carbon / mineralizer cartridge, and UV lamp inspection to ensure 100% pure drinking water.",
        "highlights": [
            "Certified multi-stage filter replacement (Spun Polypropylene, Pre-Carbon, Post-Carbon)",
            "High-rejection semi-permeable thin-film composite (TFC) RO membrane installation",
            "Pre and post replacement digital TDS (Total Dissolved Solids) purity audit",
            "Booster pump operating pressure verification (ensuring 60-80 PSI for membrane longevity)",
            "Auto-cutoff float valve and high-pressure switch calibration"
        ],
        "included": [
            "Pre-filter spun candle extraction and bowl sanitization",
            "Sediment and activated carbon block filter replacement",
            "RO membrane housing descaling and new membrane insertion",
            "Post-carbon / mineral cartridge replacement",
            "UV chamber quartz tube cleaning and UV ballast check",
            "Digital input vs output water TDS measurement",
            "Internal leak pressure test across all quick-connect fittings"
        ],
        "excluded": [
            "Cost of physical replacement filter cartridges, membrane, and minerals (billed per package)",
            "Booster pump motor replacement or 24V/36V SMPS power adapter replacement",
            "Plumbing pipeline extensions or external tap additions"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Raw Water Quality & Pressure Check",
                "description": "Technician measures raw tap water TDS, hardness, and booster pump pressure before opening the system.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "System Depressurization & Filter Extraction",
                "description": "Water inlet valve is shut, storage tank drained, and expired sediment, carbon, and membrane cartridges removed.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Filter Housing Sanitization & New Insertion",
                "description": "Filter housings are sanitized, O-rings lubricated with food-grade silicone, and new certified filters installed.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Carbon Flush & Membrane Conditioning",
                "description": "New carbon filter is flushed to clear carbon black dust before connecting to the delicate RO membrane.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Purity Testing & Final TDS Handover",
                "description": "Purifier is run to fill initial tank; output TDS is adjusted to ideal 80-150 ppm range and verified with customer.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Calibrated digital TDS meter and pH testing drops",
            "RO booster pump hydraulic pressure gauge",
            "Filter housing spanner wrenches (10-inch and membrane housing)",
            "Food-grade silicone O-ring lubricant",
            "TDS adjuster valve micro-screwdriver"
        ],
        "customer_setup": [
            "Ensure raw municipal or borewell water supply is flowing",
            "Provide access to the purifier mounting location and electrical socket",
            "Keep a small bucket or basin handy for initial water drainage"
        ],
        "aftercare": [
            "Discard the first full storage tank of water after new filter installation",
            "Replace the external 5-micron pre-filter candle every 3 months in high-sediment areas",
            "Never run the purifier without water supply to avoid booster pump dry run damage"
        ],
        "expected_results": [
            "Crisp, sweet-tasting drinking water with optimal mineral balance",
            "Complete removal of heavy metals, pesticides, bacteria, and cysts",
            "Target output TDS maintained within healthy 80 - 150 ppm"
        ],
        "important_notes": [
            "Filter cartridges are billed separately based on brand and filtration package selected",
            "Borewell water with TDS above 1500 ppm requires high-rejection heavy-duty membranes"
        ],
        "warranty": "30-day SmartServe service warranty on filter installation and zero leakage",
        "faqs": [
            {
                "question": "How often should RO water purifier filters be replaced?",
                "answer": "External sediment pre-filters should be replaced every 3-4 months, carbon and sediment filters every 12 months, and the RO membrane every 18-24 months."
            },
            {
                "question": "What is the ideal TDS level for drinking water?",
                "answer": "According to health guidelines, a TDS level between 80 and 150 ppm provides the ideal balance of pure hydration and essential mineral content."
            },
            {
                "question": "Why does the first tank of water need to be discarded after filter replacement?",
                "answer": "Discarding the first tank flushes out sterile manufacturing preservatives and harmless fine carbon dust from brand-new filters."
            },
            {
                "question": "How long does full filter replacement take?",
                "answer": "Complete multi-stage filter replacement and TDS calibration take approximately 45 to 60 minutes."
            }
        ],
        "dos": [
            "Replace the outer sediment filter regularly to protect the costly inner RO membrane",
            "Verify input and output TDS readings with the technician's digital meter"
        ],
        "donts": [
            "Never connect hot water supply to an RO purifier (destroys membrane instantly)",
            "Do not allow output TDS to drop below 50 ppm, which depletes beneficial minerals"
        ],
        "tips": [
            "Routinely wipe the transparent storage tank clean to prevent algae formation"
        ]
    },
    {
        "id": "00210570-c55f-4a72-ac3d-d33a95001c32",
        "name": "Installation",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "RO / Water Purifier",
        "price": 499.0,
        "description": "Professional wall mounting and plumbing installation for all domestic RO, UV, and UF water purifiers including inlet water diverter valve fitting, drain reject water pipe routing, leak-free connection, and initial TDS tuning.",
        "highlights": [
            "Laser-leveled wall mounting bracket installation with zero vibration",
            "Inlet solid brass diverter valve connection to kitchen cold water line",
            "Neat, hygienic reject brine water tubing routing to drain",
            "Raw water pressure assessment and pressure reducer valve fitting (if required)",
            "Initial tank flush and digital TDS / pH output water calibration"
        ],
        "included": [
            "Unboxing and inspection of purifier and all plumbing accessories",
            "Wall template alignment and structural anchor drilling",
            "Brass feed water diverter valve installation on cold tap line",
            "Food-grade 1/4-inch or 3/8-inch PU tubing connection",
            "Reject drain water pipe hygienic routing to sink drain",
            "Electric power cord connection and low-pressure switch check",
            "Tank fill cycle test, auto-cutoff check, and TDS demonstration"
        ],
        "excluded": [
            "Cost of external pre-filter housing bowl or copper tap fittings (available as add-ons)",
            "External pressure reducing valve (PRV) for high-rise apartments with water pressure over 30 PSI",
            "Electrical wiring extension or new socket installation"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Site Inspection & Pressure Testing",
                "description": "Technician tests municipal/borewell water line pressure and confirms optimal mounting location near sink and power outlet.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Wall Bracket Mounting",
                "description": "Holes are drilled into tile or masonry wall using ceramic drill bits to avoid cracking tiles; mounting bracket is secured.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Plumbing Diverter & Tubing Hookup",
                "description": "Brass inlet diverter valve is connected to cold water tap; food-grade tubing is routed neatly to pre-filter and purifier inlet.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Reject Line Routing & Tank Power-Up",
                "description": "Drain line is secured into sink drain; electrical power is connected and booster pump begins initial tank fill.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Leak Check & Water TDS Verification",
                "description": "All push-fit joints are checked for zero micro-leaks; output water TDS is tested and demonstrated to customer.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Tile and masonry carbide drill bits",
            "Rotary drill and spirit bubble level",
            "Precision tubing cutter (for clean 90-degree burr-free cuts)",
            "Digital TDS meter and water pressure gauge",
            "Teflon sealing tape and locking clips for push-fit elbows"
        ],
        "customer_setup": [
            "Keep new RO purifier carton and all inbox parts in the kitchen",
            "Ensure a functional cold water tap and standard 6A/16A socket within 1.5 meters",
            "Clear kitchen counter space directly below the intended wall mounting area"
        ],
        "aftercare": [
            "Discard the first full storage tank of water before drinking",
            "Check tubing connections for any minor drips during the first 24 hours",
            "Collect reject water in a bucket for watering plants or mopping floors"
        ],
        "expected_results": [
            "Firm, stable wall mounting that will not sag when storage tank is full (8-10 kg)",
            "Completely leak-free plumbing connections with food-safe tubing",
            "Pure, healthy drinking water delivery at balanced mineral TDS levels"
        ],
        "important_notes": [
            "High-rise apartments with water pressure exceeding 30 PSI require a Pressure Reducing Valve (PRV) to prevent filter housing burst",
            "Never connect the RO inlet to a hot water line or geyser outlet"
        ],
        "warranty": "60-day SmartServe installation warranty covering mounting and leak-free plumbing joints",
        "faqs": [
            {
                "question": "Can the purifier be installed on kitchen tiles without cracking them?",
                "answer": "Yes. Our technicians use specialized sharp tile drill bits without hammer action to drill perfectly smooth holes without cracking glazed tiles."
            },
            {
                "question": "Why is an external pre-filter bowl recommended?",
                "answer": "An external pre-filter traps coarse mud, rust, and silt before water enters your purifier, doubling the lifespan of expensive internal filters."
            },
            {
                "question": "Can the wastewater from the RO purifier be reused?",
                "answer": "Yes, RO reject water is excellent for mopping floors, cleaning utensils, or watering plants, but should not be consumed."
            },
            {
                "question": "How long does RO purifier installation take?",
                "answer": "Standard wall mounting and plumbing connection take approximately 45 to 60 minutes."
            }
        ],
        "dos": [
            "Install an external pre-filter bowl to protect your internal RO components",
            "Ensure the drain pipe outlet is positioned above sink water level to prevent siphoning"
        ],
        "donts": [
            "Do not connect RO inlet to hot water lines",
            "Do not route tubing across high-heat cooking zones or sharp cabinet edges"
        ],
        "tips": [
            "Keep the RO user manual and warranty card in an accessible kitchen drawer for service tracking"
        ]
    },
    {
        "id": "1c8493ce-fa31-4673-80f1-d55e55e66a46",
        "name": "Repair",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "RO / Water Purifier",
        "price": 399.0,
        "description": "Comprehensive diagnostic and corrective repair for all water purifier faults including continuous water leakage, low or zero water flow, constant buzzing pump noise, auto-cutoff failure, bad water taste/smell, and dead power supply.",
        "highlights": [
            "Booster pump operating pressure and diaphragm leakage diagnostic",
            "SMPS power adapter and solenoid valve (SV) electronic continuity test",
            "Auto-cutoff float switch and high/low pressure switch troubleshooting",
            "Quick-connect push-fit elbow and tubing micro-leak elimination",
            "UV ballast choke and germicidal lamp replacement diagnostics"
        ],
        "included": [
            "Complete hydraulic pressure and electrical component diagnosis",
            "Solenoid valve opening/closing and bypass testing",
            "Booster pump motor vibration and pressure check",
            "Float microswitch tank cutoff testing",
            "Identification and repair of joint leaks and cracked fittings",
            "TDS meter test before and after repair",
            "Full cycle performance check"
        ],
        "excluded": [
            "Cost of replacement booster pump, SMPS adapter, or solenoid valve",
            "Full replacement filter cartridge kit (billed separately if needed)",
            "Storage tank replacement due to external physical cracks"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Symptom Analysis & Leak Inspection",
                "description": "Technician isolates whether the issue is electrical (no power, buzzing) or hydraulic (leakage, slow flow, bad taste).",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Electrical Circuit & SMPS Testing",
                "description": "24V/36V DC output from the SMPS power supply is tested with multimeter under full pump load.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Booster Pump & Solenoid Valve Audit",
                "description": "Pump pressure head (target 70-90 PSI) is measured; solenoid valve is checked for coil burn or stuck plunger.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Faulty Component Replacement & Tube Reseating",
                "description": "Defective electrical or plumbing components are replaced and push-fit tubes are cleanly recut and locked.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Auto-Cutoff & Purity Verification",
                "description": "Purifier is run to confirm automatic shutdown when tank fills; output water TDS is verified.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Hydraulic water pressure gauge with quick-connect tee",
            "Digital true-RMS multimeter",
            "Precision tubing cutter and push-fit extraction tools",
            "TDS meter and water hardness test kit",
            "Assorted food-grade replacement elbows, tees, and locking clips"
        ],
        "customer_setup": [
            "Ensure raw water supply valve is open and power is available",
            "Describe the symptom clearly (e.g. tank overflows, pump runs continuously, foul taste)",
            "Keep a towel or cloth handy for minor water drips during testing"
        ],
        "aftercare": [
            "Observe the purifier for 2 hours after repair to confirm zero slow weeping from joints",
            "If water taste changes suddenly, check input tap water quality before adjusting TDS",
            "Keep the purifier plugged in so UV and auto-flush systems function as designed"
        ],
        "expected_results": [
            "Complete elimination of annoying water leaks and puddle formation",
            "Proper automatic shutoff when storage tank is full, preventing water waste",
            "Restored pure, sweet drinking water flow"
        ],
        "important_notes": [
            "A constantly running purifier where the pump never stops indicates a failed high-pressure switch or choked membrane",
            "Replacement parts are quoted upfront before installation"
        ],
        "warranty": "30-day SmartServe warranty on repair labor and installed components",
        "faqs": [
            {
                "question": "Why is water continuously draining from the reject pipe even when the tank is full?",
                "answer": "This happens when the Solenoid Valve (SV) gets stuck in an open position or the High Pressure switch fails to signal the valve to close."
            },
            {
                "question": "Why does my purifier make a loud vibrating or buzzing noise?",
                "answer": "A loud vibrating noise usually points to air trapped in the pump head, worn booster pump bearings, or loose internal mounting screws."
            },
            {
                "question": "Can your technician fix all brands of water purifiers?",
                "answer": "Yes, our technicians service all major brands including Kent, Aquaguard, Pureit, Livpure, Havells, Blue Star, and assembled systems."
            },
            {
                "question": "How long does a water purifier repair take?",
                "answer": "Standard diagnostic and part replacement take approximately 30 to 50 minutes."
            }
        ],
        "dos": [
            "Turn off the inlet water valve immediately if you notice water pooling under the unit",
            "Check that the electrical socket is dry and free of moisture drips"
        ],
        "donts": [
            "Do not allow the booster pump to run continuously for hours without water",
            "Do not attempt to tighten push-fit plastic elbows with metal wrenches"
        ],
        "tips": [
            "Check your external sediment pre-filter monthly; a choked pre-filter is the #1 cause of booster pump burnout"
        ]
    },
    {
        "id": "1b4c3de4-2abd-4724-9f13-f3c5ed9a4083",
        "name": "RO Cleaning",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "RO / Water Purifier",
        "price": 499.0,
        "description": "Comprehensive internal tank and housing hygiene sanitization service for domestic water purifiers including chemical descaling of the storage tank, UV chamber cleaning, filter bowl de-sludging, and biofilm elimination.",
        "highlights": [
            "Storage tank food-grade sanitization and microbial biofilm removal",
            "UV sterilizer quartz sleeve descaling for 100% germicidal UV-C transmission",
            "Pre-filter sediment bowl scrubbing and algae purge",
            "Dispensing faucet valve dismantling and limescale clearing",
            "Post-cleaning pure water TDS and residual chlorine audit"
        ],
        "included": [
            "Purifier storage tank draining, scrubbing, and sanitizing with food-safe solution",
            "Tank cover gasket inspection and airtight seal check",
            "UV quartz glass tube extraction, acid descaling, and re-polishing",
            "External sediment bowl and filter housing internal rinse",
            "Dispensing tap / faucet flow clearing and sanitization",
            "Exterior canopy wipe-down and polished finish",
            "Digital TDS and output water clarity verification"
        ],
        "excluded": [
            "Cost of new filter cartridges or replacement RO membrane",
            "Replacement of cracked storage tank or broken dispensing tap",
            "Electrical repairs to SMPS or booster pump"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Tank Inspection & Water Drainage",
                "description": "Technician isolates the unit, drains the storage tank, and inspects walls for slimy bacterial biofilm or algae marks.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Food-Grade Sanitizing & Scrubbing",
                "description": "Storage tank is scrubbed with non-toxic, food-grade sanitizing agent to dissolve organic slime and hard-water scaling.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "UV Quartz Sleeve Descaling",
                "description": "The glass quartz sleeve surrounding the UV lamp is removed and cleaned of hard water mineral haze to ensure maximum UV-C penetration.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Dispensing Tap & Filter Bowl Rinse",
                "description": "The dispensing tap is dismounted and sanitized; external pre-filter housing is washed clean of red silt.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "System Flush & Water Quality Validation",
                "description": "Tank is refilled and rinsed; technician tests water clarity, odorless purity, and verifies TDS level.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Food-grade citric acid and tank sanitizing concentrate",
            "Specialized curved tank cleaning brushes and lint-free sponges",
            "Digital TDS meter and UV-C intensity test strip",
            "Sanitary gloves and food-safe wipe cloths",
            "Bucket and clean rinse siphon"
        ],
        "customer_setup": [
            "Provide running water source and power supply in kitchen",
            "Clear workspace around and beneath the wall-mounted purifier",
            "Inform technician if stored water had developed a foul smell or strange taste"
        ],
        "aftercare": [
            "Discard the first fresh tank of water post-cleaning before consumption",
            "Keep storage tank cover securely fastened to prevent dust entry",
            "Schedule tank sanitization every 6 months to prevent biofilm buildup"
        ],
        "expected_results": [
            "100% germ-free, odorless, and sweet-tasting drinking water",
            "Elimination of slimy bacterial film and green algae inside the tank",
            "Crystal-clear UV quartz sleeve ensuring complete bacterial sterilization"
        ],
        "important_notes": [
            "Tank cleaning is critical even if filters are new, as airborne microbes can colonize standing water in storage tanks",
            "Does not include replacement of expired filter cartridges"
        ],
        "warranty": "30-day SmartServe service guarantee on tank hygiene and leak-free reassembly",
        "faqs": [
            {
                "question": "Why does my RO purified water taste or smell stale?",
                "answer": "Even pure water develops a slimy microbial biofilm on storage tank walls after several months. Professional tank sanitization eliminates this odor completely."
            },
            {
                "question": "Why does the UV quartz sleeve need descaling?",
                "answer": "Hard water minerals form a white scale coating on the quartz glass. This blocks ultraviolet UV-C rays from reaching bacteria in the water."
            },
            {
                "question": "How frequently should the RO storage tank be cleaned?",
                "answer": "The storage tank should be professionally sanitized at least once every 6 months."
            },
            {
                "question": "How long does a thorough RO cleaning take?",
                "answer": "Complete tank dismantling, UV quartz descaling, and sanitization take approximately 40 to 50 minutes."
            }
        ],
        "dos": [
            "Ensure the tank cover seal is airtight to keep out insects and ants",
            "Clean the dispensing tap nozzle regularly with a clean damp cloth"
        ],
        "donts": [
            "Never use harsh household chemical bleach or detergents to clean the internal tank",
            "Do not touch the delicate UV lamp with bare oily fingers"
        ],
        "tips": [
            "If leaving home for a week, drain the storage tank completely to prevent stagnant water biofilm"
        ]
    },
    {
        "id": "baa77b5c-724a-496b-a9cc-a2dbebd51ea3",
        "name": "RO Service",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "RO / Water Purifier",
        "price": 499.0,
        "description": "Comprehensive seasonal preventative maintenance service for all RO + UV + UF water purifiers including filter health inspection, membrane rejection efficiency test, booster pump performance audit, tank sanitization, and TDS calibration.",
        "highlights": [
            "Complete 15-point seasonal performance and water quality health checkup",
            "Digital membrane salt-rejection efficiency calculation (ensuring 90%+ rejection)",
            "Booster pump pressure output and electrical SMPS voltage audit",
            "Auto-cutoff float switch and low pressure switch calibration",
            "Storage tank sanitization and leak prevention inspection"
        ],
        "included": [
            "Raw tap water vs purified water digital TDS audit",
            "Sediment filter, carbon block, and RO membrane flow check",
            "External pre-filter candle washing and bowl cleaning",
            "Booster pump operating pressure and sound audit",
            "Auto-cutoff float sensor test to prevent tank overflow",
            "Storage tank rinse and dispensing faucet check",
            "Tightening of all push-fit tube joints and elbow fittings"
        ],
        "excluded": [
            "Cost of new filter cartridges or RO membrane (billed separately if replacement needed)",
            "Replacement of booster pump or transformer power supply",
            "Major plumbing pipe relocation"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Raw vs Purified Water Quality Audit",
                "description": "Technician measures raw water TDS, purified water TDS, and calculates membrane rejection percentage.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Pre-Filter Candle Wash & Bowl Flush",
                "description": "External filter housing is unscrewed, mud and silt washed away, and pre-filter candle inspected for clogging.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Pump Pressure & Valve Health Check",
                "description": "Inlet solenoid valve response, booster pump working pressure (PSI), and SMPS voltage are tested.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Internal Tube & Tank Sanitization",
                "description": "Storage tank is rinsed, push-fit joints inspected for weepage, and mineral cartridge flow verified.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "TDS Fine-Tuning & Customer Report",
                "description": "TDS controller is calibrated to provide optimal 100-140 ppm drinking water; full health report is handed over.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital TDS meter and water pH testing kit",
            "Hydraulic pressure testing gauge",
            "Housing spanner wrench and tubing cutter",
            "True-RMS digital multimeter",
            "Sanitizing sponge and lint-free cloths"
        ],
        "customer_setup": [
            "Provide access to water purifier, kitchen sink, and power outlet",
            "Ensure water is flowing through the main supply tap",
            "Keep note of approximately when filters were last replaced"
        ],
        "aftercare": [
            "Discard first post-service tank of water if tank was sanitized",
            "Replace the external spun filter candle every 3 months",
            "Contact SmartServe if output flow rate drops significantly"
        ],
        "expected_results": [
            "Assurance of 100% safe, certified drinking water for your family",
            "Optimized water flow rate filling the tank in under 45 minutes",
            "Early identification of failing components before sudden breakdown"
        ],
        "important_notes": [
            "If the RO membrane salt rejection has dropped below 85%, membrane replacement will be recommended",
            "Filters are billed separately only if the customer elects to replace expired cartridges"
        ],
        "warranty": "30-day SmartServe service guarantee on servicing and workmanship",
        "faqs": [
            {
                "question": "What is the difference between RO Service and Filter Replacement?",
                "answer": "RO Service is a comprehensive checkup, tuning, sanitization, and diagnostic audit. Filter Replacement specifically includes the installation of new filter cartridges."
            },
            {
                "question": "How do I know if my RO membrane has failed?",
                "answer": "A failed membrane either results in a very high output TDS close to tap water, or severely reduced water flow where the tank takes hours to fill."
            },
            {
                "question": "How often should an RO water purifier be serviced?",
                "answer": "A comprehensive service checkup should be performed once every 6 months."
            },
            {
                "question": "How long does general RO servicing take?",
                "answer": "A full seasonal RO service takes approximately 40 to 50 minutes."
            }
        ],
        "dos": [
            "Keep your purifier connected to power to maintain UV disinfection ready",
            "Ensure the pre-filter candle is checked regularly"
        ],
        "donts": [
            "Do not ignore slow water dispensing or changes in water taste",
            "Do not attempt to adjust the TDS mixing screw without a digital meter"
        ],
        "tips": [
            "Test your drinking water TDS every 2 months using a simple handheld digital TDS meter"
        ]
    },

    # --- SUBCATEGORY: Refrigerator (5 Services) ---
    {
        "id": "9cd49b6b-f7eb-4dc7-99cc-06c7b9e185a7",
        "name": "Cooling Problem",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Refrigerator",
        "price": 499.0,
        "description": "Specialized diagnostic and restorative service for single-door, double-door, and side-by-side refrigerators suffering from no cooling, weak cooling in the fridge section, excessive freezer frost buildup, or thermal cycling failures.",
        "highlights": [
            "Defrost system diagnostic: bi-metal defrost thermostat, thermal fuse, and timer/sensor check",
            "Evaporator defrost heating element continuity and resistance testing",
            "Evaporator fan motor RPM and airflow circulation duct flap inspection",
            "Magnetic door gasket seal air-tightness testing to eliminate warm air infiltration",
            "Compressor pump performance, relay, and capillary tube restriction audit"
        ],
        "included": [
            "Freezer and fresh-food compartment temperature measurement",
            "Defrost heater, thermal fuse, and bi-metal sensor testing",
            "Evaporator fan motor airflow and damper flap inspection",
            "Condenser coil dust inspection and compressor heat audit",
            "Magnetic door gasket dollar-bill suction test",
            "Compressor starting relay and overload protector check",
            "Defrost timer or electronic control board defrost cycle trigger"
        ],
        "excluded": [
            "Cost of replacement parts such as defrost heater, thermostat, fan motor, or PCB",
            "Complete refrigerant gas recharge (billed separately under Gas Charging)",
            "Cabinet sheet metal dent repair or repainting"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Temperature Measurement & Airflow Audit",
                "description": "Technician measures exact temperatures in freezer (-18°C target) and fridge (+4°C target) and listens for fan operation.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Freezer Backplate Removal & Frost Inspection",
                "description": "Freezer back panel is removed; evaporator coil frost pattern is inspected to diagnose defrost vs refrigerant failure.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Defrost Circuit Continuity Testing",
                "description": "Multimeter tests defrost heating rod, thermal fuse, and defrost sensor for open circuits that cause ice choking.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Air Damper & Fan Motor Inspection",
                "description": "Circulation fan and motorized cold-air damper flap channeling cool air to the lower section are tested.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Component Replacement & Airflow Restoration",
                "description": "Defective defrost parts are replaced, excessive ice is melted with hot-air blower, and proper circulation is verified.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Digital true-RMS multimeter and thermocouple temperature probes",
            "Industrial hot-air defrosting blower",
            "Infrared laser thermometer",
            "Door gasket gap gauge",
            "Precision insulated hand tools"
        ],
        "customer_setup": [
            "Clear items out of the freezer and upper fridge shelves before technician arrives",
            "Keep the refrigerator plugged in so existing cooling behavior can be measured",
            "Keep model number sticker (usually inside fresh food compartment) accessible"
        ],
        "aftercare": [
            "Allow 6 to 12 hours for temperatures to completely normalize after defrosting repair",
            "Avoid packing shelves so tightly that air circulation vents become blocked",
            "Ensure door is fully closed and not propped open by oversized bottles"
        ],
        "expected_results": [
            "Restoration of crisp +3°C to +5°C chilling in the lower fresh-food compartment",
            "Solid -18°C freezing in the freezer without abnormal snow-like frost buildup",
            "Smooth, silent compressor and internal circulation fan operation"
        ],
        "important_notes": [
            "A solid wall of ice choking the evaporator coil is almost always a defrost circuit failure, not a gas leak",
            "Replacement defrost heaters or electronic sensors are quoted upfront"
        ],
        "warranty": "30-day SmartServe warranty on cooling restoration labor and installed parts",
        "faqs": [
            {
                "question": "Why is my freezer freezing solid while the fridge section below is warm?",
                "answer": "In frost-free refrigerators, this is the classic symptom of a failed defrost heater, sensor, or timer. Ice blocks the air duct, stopping cold air from flowing down to the fridge."
            },
            {
                "question": "Does weak cooling always mean the refrigerator needs gas?",
                "answer": "No. In over 70% of cases, cooling problems are caused by defrost circuit failures, failed circulation fan motors, or dirty condenser coils, not gas loss."
            },
            {
                "question": "How long does it take for a refrigerator to cool down after repair?",
                "answer": "After resolving a defrost blockage, it takes 4 to 8 hours for temperatures to stabilize throughout the fresh food compartment."
            },
            {
                "question": "How long does the cooling problem diagnostic and repair take?",
                "answer": "Thorough disassembly, coil defrosting, electrical testing, and part replacement take approximately 50 to 75 minutes."
            }
        ],
        "dos": [
            "Keep food 2 inches away from cold air vents on the rear interior wall",
            "Check that magnetic door gaskets seal tightly all the way around"
        ],
        "donts": [
            "Never chip away freezer ice using sharp knives or ice picks (punctures coil)",
            "Do not overload the refrigerator with warm, freshly cooked food"
        ],
        "tips": [
            "Perform the 'dollar bill test' on your door gasket: close door on a bill; if it pulls out with zero resistance, replace the gasket"
        ]
    },
    {
        "id": "094370ac-09a7-41f6-9748-0dd5ba0e332c",
        "name": "Gas Charging",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Refrigerator",
        "price": 499.0,
        "description": "Professional refrigerant leak repair, moisture dehydration vacuuming, copper line brazing, filter drier replacement, and precise refrigerant charging (R600a / R134a) for single and multi-door domestic refrigerators.",
        "highlights": [
            "Nitrogen pressure leak detection and ultrasonic joint leak testing",
            "Mandatory molecular sieve copper filter drier replacement before charging",
            "Deep dual-stage vacuum pump evacuation down to 250 microns to eliminate moisture",
            "Digital gram-scale precision refrigerant charging matching exact OEM label (R600a/R134a)",
            "Frost-line inspection across evaporator to guarantee uniform capillary feed"
        ],
        "included": [
            "Nitrogen pressure leak test on evaporator, condenser, and internal copper loops",
            "Brazing and sealing of identified pinhole leaks or flare joints",
            "Cutting out old filter drier and brazing new copper spun drier",
            "Deep vacuum pump moisture dehydration",
            "Precision refrigerant gas charging by digital weight scale",
            "Compressor operating current and back-pressure verification",
            "Frost line validation across the evaporator coil"
        ],
        "excluded": [
            "Replacement of completely seized or burnt compressor motor",
            "Replacement of internal foaming aluminum evaporator if internally corroded beyond repair",
            "Cabinet body repairs"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Pressure Gauging & Leak Localization",
                "description": "Technician pierces process tube, connects gauges, and uses dry nitrogen to locate copper or aluminum coil leak points.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Brazing Leak Repair & New Drier Installation",
                "description": "Pinhole leaks are brazed with specialized silver-copper rods; old saturated filter drier is replaced with a virgin unit.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Deep Vacuum Dehydration",
                "description": "High-vacuum rotary pump evacuates the sealed system below 500 microns to extract every trace of atmospheric moisture.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Precision Gram-Scale Gas Charging",
                "description": "Exact weight of virgin R600a or R134a is charged into the suction port per manufacturer cabinet badge specification.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Operating Pressure & Frost Line Validation",
                "description": "Refrigerator runs for 20 minutes; frost line extends fully across evaporator without sweating back to compressor.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital refrigerant manifold gauge and precision gram scale",
            "Dual-stage rotary vacuum pump",
            "Oxy-acetylene/LPG micro-brazing torch and silver-alloy rods",
            "Certified virgin R600a (Isobutane) or R134a canisters",
            "Copper spun molecular sieve filter drier"
        ],
        "customer_setup": [
            "Ensure stable electrical power supply is available for vacuum pump and compressor",
            "Clear floor area behind and around the refrigerator for brazing torch safety",
            "Keep original model number and serial badge accessible"
        ],
        "aftercare": [
            "Keep refrigerator plugged in and do not load warm food for the first 6 hours",
            "Ensure at least 3 inches of clearance between refrigerator back and the wall",
            "Listen for smooth, steady compressor hum without clicking or rattling"
        ],
        "expected_results": [
            "Immediate restoration of icy cold temperatures in freezer and fresh food sections",
            "Stable compressor cycling without overheating or continuous running",
            "Long-lasting cooling performance with factory-sealed integrity"
        ],
        "important_notes": [
            "Modern refrigerators use eco-friendly R600a (isobutane), which is flammable and requires certified safety spark-free brazing protocols",
            "A new filter drier must ALWAYS be installed whenever a refrigeration circuit is opened"
        ],
        "warranty": "60-day SmartServe warranty on gas charging and repaired brazed joints",
        "faqs": [
            {
                "question": "How do I know if my refrigerator has a gas leak?",
                "answer": "The compressor runs continuously without stopping, but the freezer is barely cool and the fresh food section is warm, while the exterior sides of the fridge feel cool instead of warm."
            },
            {
                "question": "Can gas simply be topped up in a refrigerator?",
                "answer": "No. Refrigerators have tiny sealed charges (often only 40-70 grams). Any gas loss requires fixing the leak, replacing the filter drier, vacuuming, and re-weighing the exact charge."
            },
            {
                "question": "What is R600a gas and is it safe?",
                "answer": "R600a is isobutane, the global environmentally-friendly standard for modern refrigerators. Our technicians follow strict safety protocols and use certified equipment."
            },
            {
                "question": "How long does refrigerator gas charging take?",
                "answer": "Leak testing, brazing, vacuuming, and precision charging take approximately 60 to 90 minutes."
            }
        ],
        "dos": [
            "Ensure the technician replaces the copper filter drier before charging gas",
            "Maintain proper air gap behind the refrigerator to allow heat rejection"
        ],
        "donts": [
            "Never allow a technician to charge gas without pulling a deep vacuum first",
            "Never poke sharp objects into the freezer compartment"
        ],
        "tips": [
            "Check that the exterior side walls of modern refrigerators feel warm during operation; this indicates normal heat rejection"
        ]
    },
    {
        "id": "3312efee-fc95-4a64-8aa3-f97e2d2709f0",
        "name": "General Servicing",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Refrigerator",
        "price": 499.0,
        "description": "Comprehensive preventative maintenance and hygiene servicing for all refrigerator types including condenser coil dust removal, drain pan and tube clearing, door gasket deep cleaning, thermostat calibration, and electrical health check.",
        "highlights": [
            "Rear/bottom condenser coil dust extraction and heat rejection optimization",
            "Compressor drain pan (water tray) de-sludging and anti-fungal treatment",
            "Defrost drain tube hot-water flush to eliminate ice and water pooling under crisper drawers",
            "Magnetic door gasket deep cleaning, antifungal sanitization, and seal alignment",
            "Compressor operating current, starting relay, and earth leakage audit"
        ],
        "included": [
            "External rear condenser coil and fan blower cleaning",
            "Compressor top drain tray removal, washing, and sanitization",
            "Internal defrost drain hole flushing with hot water",
            "Magnetic door rubber gasket cleaning and seating check",
            "Thermostat dial / digital control temperature verification",
            "Electrical plug, cord, and grounding inspection",
            "Performance report on cooling temperatures and motor health"
        ],
        "excluded": [
            "Refrigerant leak repair or gas charging",
            "Replacement of worn door rubber gaskets or plastic crisper drawers",
            "Internal shelving replacement"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Baseline Temperature & Noise Evaluation",
                "description": "Technician logs operating temperatures in both compartments and checks compressor running vibration.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Condenser Coil & Fan Power Brush",
                "description": "Dust, pet hair, and lint suffocating the rear or bottom condenser coils and cooling fan are thoroughly vacuumed and brushed.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Drain Line & Water Tray Cleaning",
                "description": "Compressor drain tray is sanitized; internal defrost drain tube is flushed with hot water to prevent water leaks under vegetable drawers.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Door Gasket Sanitization & Sealing",
                "description": "Magnetic gaskets are cleaned with antimicrobial cleanser, heated if warped, and aligned for airtight closure.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Electrical Audit & Thermostat Check",
                "description": "Running amps, earthing, and thermostat cutoff are verified; temperature recommendations provided.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Specialized flexible condenser coil brush and vacuum attachment",
            "Drain line hot-water flush syringe and snake",
            "Food-grade gasket sanitizing spray",
            "Digital true-RMS multimeter and infrared thermometer",
            "Microfiber cloths"
        ],
        "customer_setup": [
            "Pull refrigerator slightly forward if back access is tightly confined",
            "Ensure power supply is accessible",
            "Remove items from the bottom vegetable crisper box"
        ],
        "aftercare": [
            "Vacuum the condenser coils once every 6 months to maintain high energy efficiency",
            "Wipe door rubber gaskets with a warm damp cloth monthly to prevent sticking",
            "Avoid placing newspaper or plastic lining on shelves that blocks cold airflow"
        ],
        "expected_results": [
            "Up to 15-20% reduction in compressor running time and electrical consumption",
            "Complete elimination of foul water odors from the rear drain tray",
            "Zero water pooling underneath vegetable crisper drawers"
        ],
        "important_notes": [
            "Choked condenser coils cause compressors to run hot and fail prematurely; regular cleaning doubles compressor life",
            "Does not include deep interior food shelf washing"
        ],
        "warranty": "30-day SmartServe service guarantee on preventative maintenance and workmanship",
        "faqs": [
            {
                "question": "Why is water pooling under the vegetable crisper drawer in my fridge?",
                "answer": "This happens when the internal defrost drain hole becomes clogged with food debris, ice, or algae. Our service thoroughly flushes and clears this drain."
            },
            {
                "question": "Why do the condenser coils need cleaning?",
                "answer": "Condenser coils dissipate all the heat pulled from inside your fridge. When coated with dust, the compressor struggles, overheats, and consumes significantly more electricity."
            },
            {
                "question": "How often should a refrigerator receive general servicing?",
                "answer": "Preventative maintenance is recommended once every 12 months, especially for homes with pets or in dusty urban areas."
            },
            {
                "question": "How long does general refrigerator servicing take?",
                "answer": "A comprehensive maintenance service takes approximately 40 to 50 minutes."
            }
        ],
        "dos": [
            "Keep the refrigerator spaced at least 2-3 inches from the wall for proper air circulation",
            "Clean spilled milk or sticky liquids immediately to prevent drain clogging"
        ],
        "donts": [
            "Do not line refrigerator wire shelves with plastic sheets or paper",
            "Do not place heavy items on the top exterior of the refrigerator"
        ],
        "tips": [
            "Setting the thermostat to medium (approx 3-4°C) provides optimal food preservation without overworking the compressor"
        ]
    },
    {
        "id": "08ada0f0-4626-494f-9ae7-73cf8a5b322e",
        "name": "Installation",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Refrigerator",
        "price": 499.0,
        "description": "Professional unboxing, positioning, leveling, and setup of single-door, double-door, and multi-door refrigerators including transit lock removal, door swing adjustment, electrical grounding safety test, and stabilizer pairing.",
        "highlights": [
            "Precision leveling using adjustable front leveling legs to prevent door drift and ensure proper drainage",
            "Safe uncrating, transit packaging removal, and internal tape extraction",
            "Mandatory compressor oil settling wait-period advice and thermal stabilization protocol",
            "Electrical socket voltage stability, load capacity, and earthing verification",
            "Shelving, crisper, and door bin setup with complete customer operational guidance"
        ],
        "included": [
            "Careful unboxing and transit damage inspection",
            "Positioning refrigerator in desired kitchen or dining location with proper air gaps",
            "Adjusting front leveling feet using spirit level",
            "Removal of interior transport tapes, styrofoam blocks, and shipping brackets",
            "Power socket voltage and earthing test",
            "Water line connection for models with ice/water dispensers (standard kit)",
            "Complete walkthrough of temperature controls, convertible zones, and eco modes"
        ],
        "excluded": [
            "Carrying heavy side-by-side refrigerators up narrow staircases without elevator",
            "New electrical wall socket installation or civil masonry work",
            "Plumbing copper piping extensions exceeding standard connection kit"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Unboxing & Visual Inspection",
                "description": "Refrigerator is unboxed, checking cabinet sheet metal, door seals, and compressor compartment for transit damage.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Positioning with Thermal Clearance",
                "description": "Unit is moved into place ensuring at least 3 inches rear clearance and 1 inch side clearance for heat dissipation.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "Precision Leveling",
                "description": "Front adjustable threaded leveling feet are turned with spirit level so doors close naturally under gravity without swinging open.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Internal Shelving & Tape Removal",
                "description": "All interior shipping tape, foam blocks, glass shelves, and crisper bins are unpacked and locked into place.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Electrical Safety & Settling Handover",
                "description": "Socket voltage and earthing are checked; customer is guided on compressor oil settling time before turning power on.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Precision spirit bubble level",
            "Adjustable leveling wrench",
            "Digital true-RMS multimeter and socket tester",
            "Heavy-duty appliance moving straps",
            "Protective floor runner mats"
        ],
        "customer_setup": [
            "Have brand-new refrigerator carton present in the kitchen or dining area",
            "Clear a clean pathway from the entrance door to the kitchen",
            "Provide a grounded 6A/16A electrical socket within 1.5 meters"
        ],
        "aftercare": [
            "Wait at least 2 to 4 hours before turning on power if refrigerator was transported tilted",
            "Allow 8 to 12 hours of empty cooling before loading with perishable groceries",
            "Ensure exterior side walls have adequate ventilation"
        ],
        "expected_results": [
            "Perfect, wobble-free stability with self-closing door gravity bias",
            "Safe electrical grounding protecting against shocks",
            "Clean, orderly setup ready for decades of reliable cooling"
        ],
        "important_notes": [
            "Turning on a refrigerator immediately after tilting causes compressor oil to enter cooling lines, causing severe blockage",
            "Side-by-side models require measuring door frames beforehand to ensure passage"
        ],
        "warranty": "60-day SmartServe installation warranty on leveling stability and plumbing connections",
        "faqs": [
            {
                "question": "Why must I wait 2-4 hours before plugging in a new refrigerator?",
                "answer": "During moving, compressor lubricating oil sloshes into the cooling pipes. Waiting allows the oil to drain safely back into the compressor sump by gravity."
            },
            {
                "question": "How should a refrigerator be leveled?",
                "answer": "A refrigerator should be leveled side-to-side, but tilted very slightly backward (front legs 5mm higher) so the doors close shut on their own."
            },
            {
                "question": "Does installation include plumbing connection for water/ice dispensers?",
                "answer": "Yes, standard water line connection to an existing nearby water supply tap is included."
            },
            {
                "question": "How long does refrigerator installation take?",
                "answer": "Unboxing, positioning, leveling, and customer demo take approximately 35 to 50 minutes."
            }
        ],
        "dos": [
            "Always wait the recommended settling time before powering on for the first time",
            "Ensure a dedicated wall socket with functional electrical grounding"
        ],
        "donts": [
            "Never drag the refrigerator across wooden or tiled floors without protective pads",
            "Do not pack the refrigerator full of warm groceries on day one"
        ],
        "tips": [
            "Pair your refrigerator with an automatic voltage stabilizer to protect delicate digital inverter compressor boards"
        ]
    },
    {
        "id": "8e00bdff-6017-4a6b-a4ec-26aa0d633013",
        "name": "Refrigerator Repair",
        "category": "4. AC, Appliance & Electronics Repair",
        "subcategory": "Refrigerator",
        "price": 369.0,
        "description": "Expert diagnostic and component repair for all refrigerator breakdowns including compressor starting failure, continuous clicking sounds, electrical shock on cabinet, ice maker faults, interior light failure, and PCB motherboard errors.",
        "highlights": [
            "PTC starter relay, overload protector (OLP), and run capacitor testing",
            "Digital inverter compressor drive frequency and DC bus voltage diagnostic",
            "Main electronic control board (PCB) sensor and relay troubleshooting",
            "Cabinet electrical grounding audit to eliminate current leakage/shocks",
            "Genuine OEM replacement spare parts with transparent pricing"
        ],
        "included": [
            "Comprehensive symptom analysis and electrical fault diagnosis",
            "Compressor winding resistance and grounded terminal testing",
            "PTC relay and thermal overload protector inspection",
            "Internal thermostat switch and temperature sensor check",
            "Circulation fan motor and door switch continuity testing",
            "PCB motherboard voltage rail testing and fault isolation",
            "Post-repair functional load test"
        ],
        "excluded": [
            "Cost of replacement compressor, inverter PCB, or fan motor",
            "Refrigerant gas recharging or copper pipe brazing",
            "Cabinet body panel replacements"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Symptom Investigation & Electrical Safety",
                "description": "Technician tests for cabinet current leakage, measures power socket voltage, and listens for compressor clicking.",
                "is_key_step": False
            },
            {
                "step_number": 2,
                "title": "Starter Relay & Compressor Diagnostic",
                "description": "PTC starter relay is removed and shaken for rattle; compressor motor winding resistance is measured across all three pins.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "PCB & Sensor Continuity Check",
                "description": "Control board relays, door light switches, and defrost thermistors are tested for electronic failure.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Part Replacement & Testing",
                "description": "Defective components (starter relay, OLP, capacitor, sensor, or PCB) are replaced with certified OEM parts.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Full Load Cooling Run Test",
                "description": "Unit is powered up; compressor starts smoothly without clicking, and steady cooling initiation is confirmed.",
                "is_key_step": False
            }
        ],
        "tools_materials": [
            "Digital true-RMS multimeter and clamp ammeter",
            "Capacitance tester and infrared thermometer",
            "Compressor test cord and starter simulator",
            "Insulated technician hand tools",
            "OEM replacement PTC relays and overload protectors"
        ],
        "customer_setup": [
            "Describe the fault clearly (e.g. clicking noise every 2 minutes, dead display, shock on door)",
            "Keep refrigerator plugged in if safe to do so",
            "Provide workspace behind the refrigerator"
        ],
        "aftercare": [
            "Use a dedicated voltage stabilizer if power fluctuations caused the starter relay to burn",
            "Never plug the refrigerator into loose or sparking wall sockets",
            "Keep the compressor area clear of dust and stored bags"
        ],
        "expected_results": [
            "Rapid diagnosis and restoration of compressor operation",
            "Elimination of annoying clicking sounds and electrical trips",
            "Restored, reliable cooling preserving your household food"
        ],
        "important_notes": [
            "A repeated clicking sound every 2-3 minutes usually indicates a failed PTC relay or a locked compressor",
            "Inverter board replacements require model-matched OEM circuit boards"
        ],
        "warranty": "30-day SmartServe warranty on repair labor and installed replacement parts",
        "faqs": [
            {
                "question": "Why is my refrigerator making a clicking sound every few minutes?",
                "answer": "This clicking is the overload protector tripping because the compressor is failing to start. This is usually caused by a burned PTC starter relay, which is an easy, low-cost fix."
            },
            {
                "question": "Why do I feel a mild electric shock when touching the refrigerator door?",
                "answer": "Electric shock indicates a missing or broken electrical earth ground in your home socket, or insulation breakdown in the internal defrost heater."
            },
            {
                "question": "Can your technician fix inverter refrigerator circuit boards?",
                "answer": "Yes, our technicians diagnose and repair or replace faulty inverter drive PCBs on LG, Samsung, Whirlpool, Haier, Godrej, and other top brands."
            },
            {
                "question": "How long does a refrigerator repair take?",
                "answer": "Standard diagnostic and part replacement take approximately 40 to 60 minutes."
            }
        ],
        "dos": [
            "Turn off power immediately if you feel an electrical shock on the metal cabinet",
            "Maintain proper earthing on the 3-pin wall socket"
        ],
        "donts": [
            "Do not hit the compressor with hard objects to try to force it to start",
            "Do not bypass thermal overload switches with direct wires"
        ],
        "tips": [
            "If the refrigerator compressor clicks and fails to start, turn it off until a technician arrives to prevent motor winding damage"
        ]
    }
]
