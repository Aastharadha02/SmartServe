import uuid

#2. Cleaning & Pest Control Data

CLEANING_SERVICES = [
    {
        "id": "287c90f2-c1b7-4487-9d4f-0d01d682e781",
        "name": "Deep Cleaning Service Variation 1",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Deep Cleaning",
        "price": 999.0,
        "description": "Professional Deep Cleaning Service Variation 1 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Deep Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Deep Cleaning Service Variation 1 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Deep Cleaning Service Variation 1 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Deep Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Deep Cleaning Service Variation 1 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Deep Cleaning Service Variation 1 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "58ebfd65-2645-4370-b241-aca8a67e6a67",
        "name": "Deep Cleaning Service Variation 2",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Deep Cleaning",
        "price": 999.0,
        "description": "Professional Deep Cleaning Service Variation 2 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Deep Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Deep Cleaning Service Variation 2 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Deep Cleaning Service Variation 2 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Deep Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Deep Cleaning Service Variation 2 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Deep Cleaning Service Variation 2 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "f40e6092-ddcd-4d8e-aaf1-be9fdbacbc0e",
        "name": "Deep Cleaning Service Variation 3",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Deep Cleaning",
        "price": 999.0,
        "description": "Professional Deep Cleaning Service Variation 3 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Deep Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Deep Cleaning Service Variation 3 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Deep Cleaning Service Variation 3 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Deep Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Deep Cleaning Service Variation 3 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Deep Cleaning Service Variation 3 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "c7529e16-f7f1-4785-bbf7-1e572aeaaaf0",
        "name": "Deep Cleaning Service Variation 4",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Deep Cleaning",
        "price": 999.0,
        "description": "Professional Deep Cleaning Service Variation 4 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Deep Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Deep Cleaning Service Variation 4 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Deep Cleaning Service Variation 4 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Deep Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Deep Cleaning Service Variation 4 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Deep Cleaning Service Variation 4 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "5ace55fc-4278-4f14-b54f-4a695af2bb7c",
        "name": "Deep Cleaning Service Variation 5",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Deep Cleaning",
        "price": 999.0,
        "description": "Professional Deep Cleaning Service Variation 5 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Deep Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Deep Cleaning Service Variation 5 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Deep Cleaning Service Variation 5 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Deep Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Deep Cleaning Service Variation 5 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Deep Cleaning Service Variation 5 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "58b3d78f-5bbd-4d31-b1e4-c59555344a73",
        "name": "Deep Cleaning Service Variation 6",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Deep Cleaning",
        "price": 999.0,
        "description": "Professional Deep Cleaning Service Variation 6 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Deep Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Deep Cleaning Service Variation 6 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Deep Cleaning Service Variation 6 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Deep Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Deep Cleaning Service Variation 6 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Deep Cleaning Service Variation 6 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "42e0784e-4fef-497f-a2cc-415631f57b6c",
        "name": "Deep Cleaning Service Variation 7",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Deep Cleaning",
        "price": 999.0,
        "description": "Professional Deep Cleaning Service Variation 7 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Deep Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Deep Cleaning Service Variation 7 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Deep Cleaning Service Variation 7 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Deep Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Deep Cleaning Service Variation 7 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Deep Cleaning Service Variation 7 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "6efaf71d-0b05-4cb0-94dc-a624f7c103a0",
        "name": "Full Home / By Room Cleaning Service Variation 1",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Full Home / By Room Cleaning",
        "price": 999.0,
        "description": "Professional Full Home / By Room Cleaning Service Variation 1 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Full Home / By Room Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Full Home / By Room Cleaning Service Variation 1 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Full Home / By Room Cleaning Service Variation 1 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Full Home / By Room Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Full Home / By Room Cleaning Service Variation 1 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Full Home / By Room Cleaning Service Variation 1 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "cdd0be50-0dba-4241-bb94-06edf5d735dd",
        "name": "Full Home / By Room Cleaning Service Variation 2",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Full Home / By Room Cleaning",
        "price": 999.0,
        "description": "Professional Full Home / By Room Cleaning Service Variation 2 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Full Home / By Room Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Full Home / By Room Cleaning Service Variation 2 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Full Home / By Room Cleaning Service Variation 2 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Full Home / By Room Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Full Home / By Room Cleaning Service Variation 2 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Full Home / By Room Cleaning Service Variation 2 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "adc6b8c0-dcad-4a57-b1a3-f20be2d2e05b",
        "name": "Full Home / By Room Cleaning Service Variation 3",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Full Home / By Room Cleaning",
        "price": 999.0,
        "description": "Professional Full Home / By Room Cleaning Service Variation 3 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Full Home / By Room Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Full Home / By Room Cleaning Service Variation 3 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Full Home / By Room Cleaning Service Variation 3 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Full Home / By Room Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Full Home / By Room Cleaning Service Variation 3 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Full Home / By Room Cleaning Service Variation 3 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "c8bfc80e-aa4d-48a9-8d78-41a62ff587cb",
        "name": "Full Home / By Room Cleaning Service Variation 4",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Full Home / By Room Cleaning",
        "price": 999.0,
        "description": "Professional Full Home / By Room Cleaning Service Variation 4 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Full Home / By Room Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Full Home / By Room Cleaning Service Variation 4 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Full Home / By Room Cleaning Service Variation 4 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Full Home / By Room Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Full Home / By Room Cleaning Service Variation 4 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Full Home / By Room Cleaning Service Variation 4 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "e452fe98-b0b0-485a-ba63-7deb57ca7f89",
        "name": "Full Home / By Room Cleaning Service Variation 5",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Full Home / By Room Cleaning",
        "price": 999.0,
        "description": "Professional Full Home / By Room Cleaning Service Variation 5 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Full Home / By Room Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Full Home / By Room Cleaning Service Variation 5 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Full Home / By Room Cleaning Service Variation 5 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Full Home / By Room Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Full Home / By Room Cleaning Service Variation 5 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Full Home / By Room Cleaning Service Variation 5 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "7b455532-df98-4d31-8e28-b73988cb1607",
        "name": "Full Home / By Room Cleaning Service Variation 6",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Full Home / By Room Cleaning",
        "price": 999.0,
        "description": "Professional Full Home / By Room Cleaning Service Variation 6 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Full Home / By Room Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Full Home / By Room Cleaning Service Variation 6 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Full Home / By Room Cleaning Service Variation 6 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Full Home / By Room Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Full Home / By Room Cleaning Service Variation 6 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Full Home / By Room Cleaning Service Variation 6 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "8a8c6e5c-1b99-43f2-9606-5fa63d9e4a49",
        "name": "Full Home / By Room Cleaning Service Variation 7",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Full Home / By Room Cleaning",
        "price": 999.0,
        "description": "Professional Full Home / By Room Cleaning Service Variation 7 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Full Home / By Room Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Full Home / By Room Cleaning Service Variation 7 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Full Home / By Room Cleaning Service Variation 7 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Full Home / By Room Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Full Home / By Room Cleaning Service Variation 7 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Full Home / By Room Cleaning Service Variation 7 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "fa2970d3-b25c-4521-b61b-efeb396dadac",
        "name": "Full Home / By Room Cleaning Service Variation 8",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Full Home / By Room Cleaning",
        "price": 999.0,
        "description": "Professional Full Home / By Room Cleaning Service Variation 8 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Full Home / By Room Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Full Home / By Room Cleaning Service Variation 8 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Full Home / By Room Cleaning Service Variation 8 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Full Home / By Room Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Full Home / By Room Cleaning Service Variation 8 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Full Home / By Room Cleaning Service Variation 8 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "f7804888-0442-4dff-b91f-e543ea8182ae",
        "name": "Kitchen & Bathroom Cleaning Service Variation 1",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Kitchen & Bathroom Cleaning",
        "price": 999.0,
        "description": "Professional Kitchen & Bathroom Cleaning Service Variation 1 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Kitchen & Bathroom Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Kitchen & Bathroom Cleaning Service Variation 1 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Kitchen & Bathroom Cleaning Service Variation 1 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Kitchen & Bathroom Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Kitchen & Bathroom Cleaning Service Variation 1 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Kitchen & Bathroom Cleaning Service Variation 1 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "264904c6-aad9-4106-ac12-d8a108b29bba",
        "name": "Kitchen & Bathroom Cleaning Service Variation 2",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Kitchen & Bathroom Cleaning",
        "price": 999.0,
        "description": "Professional Kitchen & Bathroom Cleaning Service Variation 2 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Kitchen & Bathroom Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Kitchen & Bathroom Cleaning Service Variation 2 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Kitchen & Bathroom Cleaning Service Variation 2 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Kitchen & Bathroom Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Kitchen & Bathroom Cleaning Service Variation 2 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Kitchen & Bathroom Cleaning Service Variation 2 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "cedcf4c4-a0c8-460c-9aa3-dd839f66e80f",
        "name": "Kitchen & Bathroom Cleaning Service Variation 3",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Kitchen & Bathroom Cleaning",
        "price": 999.0,
        "description": "Professional Kitchen & Bathroom Cleaning Service Variation 3 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Kitchen & Bathroom Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Kitchen & Bathroom Cleaning Service Variation 3 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Kitchen & Bathroom Cleaning Service Variation 3 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Kitchen & Bathroom Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Kitchen & Bathroom Cleaning Service Variation 3 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Kitchen & Bathroom Cleaning Service Variation 3 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "990f4a13-a171-43cc-b364-1e1022122d8d",
        "name": "Kitchen & Bathroom Cleaning Service Variation 4",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Kitchen & Bathroom Cleaning",
        "price": 999.0,
        "description": "Professional Kitchen & Bathroom Cleaning Service Variation 4 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Kitchen & Bathroom Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Kitchen & Bathroom Cleaning Service Variation 4 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Kitchen & Bathroom Cleaning Service Variation 4 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Kitchen & Bathroom Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Kitchen & Bathroom Cleaning Service Variation 4 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Kitchen & Bathroom Cleaning Service Variation 4 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "6b33aec0-8146-413b-b0d3-de90b3d5d137",
        "name": "Kitchen & Bathroom Cleaning Service Variation 5",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Kitchen & Bathroom Cleaning",
        "price": 999.0,
        "description": "Professional Kitchen & Bathroom Cleaning Service Variation 5 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Kitchen & Bathroom Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Kitchen & Bathroom Cleaning Service Variation 5 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Kitchen & Bathroom Cleaning Service Variation 5 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Kitchen & Bathroom Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Kitchen & Bathroom Cleaning Service Variation 5 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Kitchen & Bathroom Cleaning Service Variation 5 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "fed5e15c-ad8c-4dcd-9fc5-bfdaad37d7a8",
        "name": "Pest Control Service Variation 1",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Pest Control",
        "price": 999.0,
        "description": "Professional Pest Control Service Variation 1 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Pest Control experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Pest Control Service Variation 1 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Pest Control Service Variation 1 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Pest Control tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Pest Control Service Variation 1 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Pest Control Service Variation 1 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "0594444a-63a4-4543-aa9a-db671cb4b269",
        "name": "Pest Control Service Variation 2",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Pest Control",
        "price": 999.0,
        "description": "Professional Pest Control Service Variation 2 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Pest Control experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Pest Control Service Variation 2 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Pest Control Service Variation 2 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Pest Control tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Pest Control Service Variation 2 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Pest Control Service Variation 2 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "3f3e2d4d-153a-4367-921a-7d6005dd532d",
        "name": "Pest Control Service Variation 3",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Pest Control",
        "price": 999.0,
        "description": "Professional Pest Control Service Variation 3 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Pest Control experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Pest Control Service Variation 3 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Pest Control Service Variation 3 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Pest Control tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Pest Control Service Variation 3 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Pest Control Service Variation 3 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "ed433b58-b961-4023-9192-a7d45601daa2",
        "name": "Pest Control Service Variation 4",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Pest Control",
        "price": 999.0,
        "description": "Professional Pest Control Service Variation 4 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Pest Control experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Pest Control Service Variation 4 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Pest Control Service Variation 4 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Pest Control tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Pest Control Service Variation 4 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Pest Control Service Variation 4 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "9a614042-e18d-4ab9-886a-0b07c93ef01a",
        "name": "Pest Control Service Variation 5",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Pest Control",
        "price": 999.0,
        "description": "Professional Pest Control Service Variation 5 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Pest Control experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Pest Control Service Variation 5 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Pest Control Service Variation 5 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Pest Control tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Pest Control Service Variation 5 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Pest Control Service Variation 5 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "d3677ffb-f3e5-4454-86b3-5a7b6d9fdad1",
        "name": "Pest Control Service Variation 6",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Pest Control",
        "price": 999.0,
        "description": "Professional Pest Control Service Variation 6 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Pest Control experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Pest Control Service Variation 6 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Pest Control Service Variation 6 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Pest Control tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Pest Control Service Variation 6 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Pest Control Service Variation 6 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "d42758ef-14dd-4683-a944-80cc0c488fcf",
        "name": "Sofa & Furniture Cleaning Service Variation 1",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Sofa & Furniture Cleaning",
        "price": 999.0,
        "description": "Professional Sofa & Furniture Cleaning Service Variation 1 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Sofa & Furniture Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Sofa & Furniture Cleaning Service Variation 1 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Sofa & Furniture Cleaning Service Variation 1 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Sofa & Furniture Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Sofa & Furniture Cleaning Service Variation 1 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Sofa & Furniture Cleaning Service Variation 1 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "0425f57a-ce8d-457f-b1d2-c387ce4daa56",
        "name": "Sofa & Furniture Cleaning Service Variation 2",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Sofa & Furniture Cleaning",
        "price": 999.0,
        "description": "Professional Sofa & Furniture Cleaning Service Variation 2 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Sofa & Furniture Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Sofa & Furniture Cleaning Service Variation 2 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Sofa & Furniture Cleaning Service Variation 2 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Sofa & Furniture Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Sofa & Furniture Cleaning Service Variation 2 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Sofa & Furniture Cleaning Service Variation 2 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "2926232b-ec38-4f63-96e5-fc359856ceae",
        "name": "Sofa & Furniture Cleaning Service Variation 3",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Sofa & Furniture Cleaning",
        "price": 999.0,
        "description": "Professional Sofa & Furniture Cleaning Service Variation 3 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Sofa & Furniture Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Sofa & Furniture Cleaning Service Variation 3 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Sofa & Furniture Cleaning Service Variation 3 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Sofa & Furniture Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Sofa & Furniture Cleaning Service Variation 3 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Sofa & Furniture Cleaning Service Variation 3 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "c4aef5dc-1115-4e65-a8c0-30f7ead61994",
        "name": "Sofa & Furniture Cleaning Service Variation 4",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Sofa & Furniture Cleaning",
        "price": 999.0,
        "description": "Professional Sofa & Furniture Cleaning Service Variation 4 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Sofa & Furniture Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Sofa & Furniture Cleaning Service Variation 4 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Sofa & Furniture Cleaning Service Variation 4 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Sofa & Furniture Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Sofa & Furniture Cleaning Service Variation 4 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Sofa & Furniture Cleaning Service Variation 4 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "bffc5df7-1c34-44fb-80dd-84fb1d9be2c1",
        "name": "Sofa & Furniture Cleaning Service Variation 5",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Sofa & Furniture Cleaning",
        "price": 999.0,
        "description": "Professional Sofa & Furniture Cleaning Service Variation 5 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Sofa & Furniture Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Sofa & Furniture Cleaning Service Variation 5 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Sofa & Furniture Cleaning Service Variation 5 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Sofa & Furniture Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Sofa & Furniture Cleaning Service Variation 5 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Sofa & Furniture Cleaning Service Variation 5 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    },
    {
        "id": "6d6239bc-2c85-4e75-809d-5a9dfb5418b0",
        "name": "Sofa & Furniture Cleaning Service Variation 6",
        "category": "2. Cleaning & Pest Control",
        "subcategory": "Sofa & Furniture Cleaning",
        "price": 999.0,
        "description": "Professional Sofa & Furniture Cleaning Service Variation 6 services tailored to your needs. Our experts ensure top-tier quality and safety, leaving you completely satisfied with the Sofa & Furniture Cleaning experience.",
        "highlights": [
            "Top quality products and equipment used",
            "Trained and background-verified professionals",
            "Hygienic and safe procedures",
            "100% satisfaction guarantee",
            "Timely and efficient service delivery"
        ],
        "included": [
            "Complete Sofa & Furniture Cleaning Service Variation 6 procedure",
            "Usage of standard tools and materials",
            "Post-service cleanup",
            "Expert consultation and advice",
            "Quality check before handover"
        ],
        "excluded": [
            "Any specialized medical treatments or heavy machinery",
            "Parts or replacement hardware unless explicitly requested",
            "Deep structural modifications"
        ],
        "process_steps": [
            {
                "step_number": 1,
                "title": "Initial Assessment",
                "description": "The professional examines the requirements and plans the service delivery.",
                "is_key_step": True
            },
            {
                "step_number": 2,
                "title": "Preparation & Setup",
                "description": "Setting up the necessary tools, materials, and safety measures.",
                "is_key_step": False
            },
            {
                "step_number": 3,
                "title": "Core Execution",
                "description": "Performing the main Sofa & Furniture Cleaning Service Variation 6 tasks with precision.",
                "is_key_step": True
            },
            {
                "step_number": 4,
                "title": "Finishing Touches",
                "description": "Applying final finishing touches to ensure perfect results.",
                "is_key_step": False
            },
            {
                "step_number": 5,
                "title": "Cleanup & Handover",
                "description": "Cleaning the work area and handing over to the customer for approval.",
                "is_key_step": True
            }
        ],
        "tools_materials": [
            "Standard Sofa & Furniture Cleaning tool kit",
            "Eco-friendly supplies and consumables",
            "Safety gear (gloves, masks, etc.)",
            "Sanitization equipment",
            "Disposable sheets/covers if applicable"
        ],
        "customer_setup": [
            "Ensure a clear working space",
            "Keep pets and children away from the service area",
            "Provide access to a power socket and water supply if needed"
        ],
        "aftercare": [
            "Avoid touching the treated area immediately",
            "Follow the professional's specific post-service advice",
            "Keep the area dry/ventilated for at least 2 hours"
        ],
        "expected_results": [
            "High quality Sofa & Furniture Cleaning Service Variation 6 completed successfully",
            "A clean and safe environment",
            "Complete customer satisfaction"
        ],
        "important_notes": [
            "Service duration may vary based on actual on-site conditions",
            "Please inform the professional of any allergies or sensitivities beforehand"
        ],
        "warranty": "7-day service warranty on workmanship",
        "faqs": [
            {
                "question": "Is the equipment sanitized?",
                "answer": "Yes, all tools are strictly sanitized before and after every session."
            },
            {
                "question": "How long does Sofa & Furniture Cleaning Service Variation 6 take?",
                "answer": "Typically between 45 minutes to 2 hours, depending on the specifics."
            },
            {
                "question": "Are the products safe?",
                "answer": "Yes, we only use industry-approved, eco-friendly, and safe products."
            },
            {
                "question": "Can I customize the service?",
                "answer": "Yes, basic customizations can be discussed directly with the professional."
            }
        ],
        "dos": [
            "Do provide clear instructions before the service begins",
            "Do inspect the work during the final handover"
        ],
        "donts": [
            "Don't attempt to interrupt the core procedure",
            "Don't use harsh chemicals on the treated area immediately after"
        ],
        "tips": [
            "Regular maintenance can significantly extend the lifespan of the results.",
            "Book in advance during weekends and holidays."
        ]
    }
]
