import uuid

# Smart Home & Security Services Data
# Category: 6. Smart Home & Security

SMART_HOME_SERVICES = [
    {
        "id": str(uuid.uuid4()),
        "name": "CCTV Camera Installation",
        "category": "6. Smart Home & Security",
        "subcategory": "Security Systems",
        "price": 1499.0,
        "description": "Professional installation and configuration of IP or Analog CCTV cameras, including optimal placement for blind-spot coverage, secure wiring routing, DVR/NVR setup, and mobile app pairing for remote live viewing.",
        "highlights": [
            "Optimal angle positioning to eliminate security blind spots",
            "Concealed or neatly clipped wiring to maintain home aesthetics",
            "DVR/NVR storage configuration for maximum video retention",
            "Mobile application setup for real-time remote monitoring",
            "Night vision and motion detection calibration"
        ],
        "included": [
            "Mounting of up to 4 CCTV cameras (Dome/Bullet)",
            "Routing and clipping of BNC/CAT6 cables up to 20 meters per camera",
            "Connection to DVR/NVR and power supply",
            "Configuration of recording settings (continuous/motion-based)",
            "Mobile app installation and pairing on up to 2 devices"
        ],
        "excluded": [
            "Supply of cameras, DVR/NVR, cables, or storage hard drives (labor only)",
            "Concealed internal wall wiring requiring masonry/chasing",
            "Setting up static IP configurations with ISP for older DVR models"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Site Assessment & Angle Planning",
                "description": "Technician surveys the property to identify critical entry points and determine the optimal mounting locations and angles for maximum coverage.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Camera Mounting & Wiring",
                "description": "Cameras are securely drilled and mounted. Cables are routed from the cameras to the central DVR/NVR location using wire clips or PVC casing.",
                "is_key_step": True
            },
            {
                "step_number": 3,
                "title": "System Connection & Power Up",
                "description": "BNC/RJ45 connectors are crimped and connected to the cameras and the recording unit. Power supplies are securely connected and tested.",
                "is_key_step": False
            },
            {
                "step_number": 4,
                "title": "DVR/NVR Configuration",
                "description": "The hard drive is formatted, and recording parameters (resolution, frame rate, motion triggers) are configured in the DVR/NVR interface.",
                "is_key_step": True
            },
            {
                "step_number": 5,
                "title": "Mobile App Pairing & Handover",
                "description": "The security system is connected to the home router, and the manufacturer's app is installed and paired on the customer's phone for live viewing.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Impact drill machine and masonry drill bits",
            "Cable crimping tools (RJ45/BNC) and wire strippers",
            "Digital multimeter for power testing",
            "Ladder, wire clips, rawl plugs, and mounting screws",
            "Portable test monitor for angle adjustments"
        ],
        "customer_setup": [
            "Ensure the cameras, DVR/NVR, hard drive, and cables are ready before the technician arrives",
            "Provide access to a working power socket near the DVR/NVR location",
            "Have your Wi-Fi password ready for network and mobile app configuration"
        ],
        "aftercare": [
            "Wipe camera lenses monthly with a microfiber cloth to ensure clear night vision",
            "Regularly check the DVR/NVR storage to ensure older footage is overwriting correctly",
            "Keep the DVR/NVR in a well-ventilated area to prevent hard drive overheating"
        ],
        "expected_results": [
            "All cameras firmly mounted with clear, unobstructed fields of view",
            "Continuous or motion-triggered video reliably recording to the hard drive",
            "Instant access to live camera feeds on the customer's smartphone"
        ],
        "important_notes": [
            "For heights exceeding 10 feet, the customer must arrange suitable scaffolding or safely secure long ladders",
            "Drilling through heavily reinforced concrete beams may require specialized equipment not covered in standard installation"
        ],
        "warranty": "30-day SmartServe warranty on wiring integrity and camera mounting stability",
        "faqs": [
            {
                "question": "Does this service include the cost of the CCTV cameras?",
                "answer": "No, this is an installation-only service. You must purchase the cameras, DVR/NVR, hard drive, and cables separately."
            },
            {
                "question": "Can the technician help me view the cameras on my TV?",
                "answer": "Yes, if your TV is near the DVR/NVR, the technician will connect it via HDMI/VGA. If it is in another room, additional long-distance cabling is required."
            },
            {
                "question": "What happens if the cable needs to run through a thick wall?",
                "answer": "Standard through-wall drilling (up to 8 inches) is included. However, deep core cutting or concealed in-wall routing is excluded."
            },
            {
                "question": "Is the mobile app viewing free?",
                "answer": "Most modern CCTV brands provide a free cloud P2P app for remote viewing. You only need an active internet connection at home."
            }
        ],
        "dos": [
            "Mount cameras high enough to prevent easy tampering or vandalism",
            "Use outdoor-rated (IP67) cameras for any exterior installations"
        ],
        "donts": [
            "Don't point cameras directly at bright light sources (like streetlights) which can cause glare",
            "Don't install the DVR/NVR in a locked, unventilated cabinet where it can overheat"
        ],
        "tips": [
            "Enable push notifications on your mobile app only for motion in specific critical zones to avoid alert fatigue.",
            "Install a small UPS for your DVR and router so cameras keep recording during power cuts."
        ]
    }
]

# We can add more services here following the exact same schema.
