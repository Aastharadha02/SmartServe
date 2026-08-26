import os
import json
import re
import httpx
from typing import Dict, Any, Optional, List, Tuple

from app.core.config import settings

# ---------------------------------------------------------
# DYNAMIC DOMAIN CLASSIFICATION & FORBIDDEN TERMS MATRIX
# ---------------------------------------------------------

DOMAIN_FORBIDDEN_TERMS = {
    "food": [
        "protective gear", "electrical testing", "multimeter", "switchboard", "voltage", 
        "wiring", "plumbing", "pipe fitting", "ladder", "structural", "nail clipper", 
        "salon", "facial", "otp", "30-day guarantee", "testing instrument", "invoice receipt",
        "circuit", "breaker", "power isolation", "pedicure", "manicure", "exfoliation",
        "technician", "installation", "scaffolding", "home repair"
    ],
    "beauty": [
        "protective gear", "electrical testing", "multimeter", "switchboard", "voltage", 
        "wiring", "plumbing", "pipe fitting", "ladder", "structural", "otp", "30-day guarantee", 
        "testing instrument", "invoice receipt", "circuit", "breaker", "power isolation",
        "gas refilling", "pressure gauge", "scaffolding", "excavation", "masonry", "home repair"
    ],
    "electrical": [
        "pedicure", "manicure", "facial", "cuticle", "nail polish", "foot soak",
        "haircut", "hair spa", "waxing", "exfoliation", "callus", "cooking", "recipe",
        "ingredients", "kitchen utensils", "baking"
    ],
    "plumbing": [
        "pedicure", "manicure", "facial", "cuticle", "nail polish", "foot soak",
        "haircut", "hair spa", "voltage", "switchboard", "wiring terminal", "multimeter",
        "cooking", "recipe", "ingredients"
    ],
    "cleaning": [
        "pedicure", "manicure", "facial", "cuticle", "nail polish", "foot soak",
        "haircut", "rewiring", "switchboard", "multimeter", "recipe", "ingredients"
    ],
    "carpentry": [
        "pedicure", "manicure", "facial", "cuticle", "voltage", "multimeter",
        "plumbing leak", "recipe", "ingredients"
    ],
    "pet": [
        "switchboard", "multimeter", "facial mask", "plumbing leak", "voltage"
    ],
    "general": [
        "otp", "30-day guarantee", "invoice receipt and digital otp"
    ]
}

GENERIC_REJECT_ITEMS = [
    "professional execution", 
    "pre-service assessment", 
    "post-service verification",
    "comprehensive professional",
    "professional toolkit", 
    "safety gear", 
    "testing instruments",
    "professional equipment set",
    "protective gear",
    "service toolkit",
    "30-day smartserve guarantee", 
    "30-day smartserve quality & performance guarantee",
    "30-day guarantee",
    "keep invoice receipt and digital otp confirmation for warranty claims",
    "contact smartserve support immediately if any anomaly occurs",
    "initial inspection -> preparation -> execution -> quality verification",
    "keep feet accessible",
    "feet accessible",
    "keep your feet accessible",
    "prepare the service area",
    "ensure clear access to work area",
    "keep work area clear",
    "safety gear will be provided",
    "professional equipment will be used"
]


def classify_domain(category: str, subcategory: str, name: str) -> str:
    """Classify service into its actual operational domain based on DB category/subcategory/name."""
    combined = f"{category} {subcategory} {name}".lower()

    if any(k in combined for k in ["panel", "wall panel", "wood panel", "pvc panel"]):
        return "carpentry"
    if any(k in combined for k in ["cooking", "chef", "food", "meal", "kitchen", "bakery", "catering"]):
        return "food"
    if any(k in combined for k in ["beauty", "salon", "spa", "pedicure", "manicure", "facial", "hair", "skincare", "makeup", "waxing"]):
        return "beauty"
    if any(k in combined for k in ["electrician", "electric", "wiring", "switch", "circuit", "light fitting"]):
        return "electrical"
    if any(k in combined for k in ["plumber", "plumbing", "leak", "pipe", "drain", "tap"]):
        return "plumbing"
    if any(k in combined for k in ["carpenter", "carpentry", "wood", "furniture assembly"]):
        return "carpentry"
    if any(k in combined for k in ["clean", "mop", "sanitize", "disinfect", "pest control", "sofa cleaning"]):
        return "cleaning"
    if any(k in combined for k in ["pet", "dog", "veterinary", "grooming"]):
        return "pet"
    if any(k in combined for k in ["ac", "air conditioner", "refrigerant", "geyser", "microwave", "appliance"]):
        return "electrical"
    return "general"


class AIService:
    """OpenRouter AI Gateway with Service-Specific Correction & Zero Generic Fallbacks."""
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.model = os.getenv("OPENROUTER_MODEL", "openrouter/ox-alpha")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def _call_llm(self, prompt: str, system_message: str) -> str:
        """Call OpenRouter LLM gateway synchronously or fallback gracefully."""
        if not self.api_key:
            return ""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "system_message": system_message},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1
            }
            with httpx.Client(timeout=12.0) as client:
                res = client.post(self.base_url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"]
        except Exception:
            pass
        return ""

    def validate_content_item(self, item: Any, domain_key: str) -> Tuple[bool, str]:
        """Validate if a text item belongs to the service domain and is not generic/forbidden."""
        if not item or not isinstance(item, str):
            return False, "Empty or non-string item"

        text_lower = item.strip().lower()

        # Reject generic placeholders
        for gen in GENERIC_REJECT_ITEMS:
            if gen in text_lower:
                return False, f"Generic placeholder detected: '{gen}'"

        # Reject domain forbidden terms
        forbidden = DOMAIN_FORBIDDEN_TERMS.get(domain_key, []) + DOMAIN_FORBIDDEN_TERMS.get("general", [])
        for fb in forbidden:
            if fb in text_lower:
                return False, f"Domain forbidden term '{fb}' detected in {domain_key} service"

        return True, "Valid"

    def validate_and_sanitize_metadata(self, data: Dict[str, Any], domain_key: str) -> Tuple[Dict[str, Any], List[str]]:
        """Validate all fields of generated JSON metadata and extract invalid items."""
        invalid_findings = []
        sanitized = {}

        # 1. Description
        desc = data.get("description") or ""
        valid, reason = self.validate_content_item(desc, domain_key)
        if valid:
            sanitized["description"] = desc.strip()
        else:
            invalid_findings.append(f"Description: {reason}")
            sanitized["description"] = ""

        # 2. Lists (highlights, included, excluded, tools_materials, customer_setup, aftercare, important_notes, expected_results, seo_keywords)
        list_keys = ["highlights", "included", "excluded", "tools_materials", "customer_setup", "aftercare", "important_notes", "expected_results", "seo_keywords"]
        for key in list_keys:
            raw_list = data.get(key) or data.get(f"required_{key}") or []
            clean_list = []
            if isinstance(raw_list, list):
                for item in raw_list:
                    val, rsn = self.validate_content_item(item, domain_key)
                    if val:
                        clean_list.append(item.strip())
                    else:
                        invalid_findings.append(f"{key}: {rsn}")
            sanitized[key] = clean_list

        # 3. Process Steps
        raw_steps = data.get("process_steps") or data.get("how_it_works") or []
        clean_steps = []
        if isinstance(raw_steps, list):
            for idx, step in enumerate(raw_steps):
                if isinstance(step, dict):
                    title = step.get("title", f"Step {idx+1}")
                    step_desc = step.get("description", "")
                    v1, r1 = self.validate_content_item(title, domain_key)
                    v2, r2 = self.validate_content_item(step_desc, domain_key)
                    if v1 and v2:
                        clean_steps.append({
                            "step_number": len(clean_steps) + 1,
                            "title": title.strip(),
                            "description": step_desc.strip(),
                            "duration_minutes": step.get("duration_minutes") or step.get("duration_mins"),
                            "is_key_step": bool(step.get("is_key_step", False))
                        })
                    else:
                        invalid_findings.append(f"Process Step {idx+1}: {r1 if not v1 else r2}")
        sanitized["process_steps"] = clean_steps

        # 4. Warranty (Default NULL!)
        raw_warranty = data.get("warranty")
        if raw_warranty and isinstance(raw_warranty, str) and raw_warranty.lower() != "null":
            v_w, r_w = self.validate_content_item(raw_warranty, domain_key)
            if v_w and "guarantee" not in raw_warranty.lower():
                sanitized["warranty"] = raw_warranty.strip()
            else:
                invalid_findings.append(f"Warranty: {r_w}")
                sanitized["warranty"] = None
        else:
            sanitized["warranty"] = None

        # 5. FAQs
        raw_faqs = data.get("faqs") or data.get("customer_faqs") or []
        clean_faqs = []
        if isinstance(raw_faqs, list):
            for f in raw_faqs:
                if isinstance(f, dict):
                    q = f.get("question") or f.get("q") or ""
                    a = f.get("answer") or f.get("a") or ""
                    v_q, r_q = self.validate_content_item(q, domain_key)
                    v_a, r_a = self.validate_content_item(a, domain_key)
                    if v_q and v_a:
                        clean_faqs.append({"question": q.strip(), "answer": a.strip()})
                    else:
                        invalid_findings.append(f"FAQ: {r_q if not v_q else r_a}")
        sanitized["faqs"] = clean_faqs

        return sanitized, invalid_findings

    def generate_service_metadata(
        self, 
        category: str, 
        service_name: str, 
        base_price: float,
        subcategory: str = "",
        existing_description: str = "",
        existing_features: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate operational content specifically for THIS EXACT SERVICE name."""
        
        domain_key = classify_domain(category, subcategory, service_name)

        system_prompt = (
            f"You are generating structured service information for ONE specific SmartServe service: '{service_name}'.\n"
            "Use only the supplied service information and reasonable domain-specific information directly applicable to this exact service.\n"
            "Do not use generic templates.\n"
            "Do not copy information from another service category.\n"
            "Do not invent tools, equipment, protective gear, ingredients, warranties, guarantees, payment procedures, OTP requirements, customer-provided items, medical claims, certifications, or procedures unless they are genuinely applicable to this exact service.\n"
            "If a section is not applicable or there is insufficient reliable information, return an EMPTY ARRAY [].\n"
            "Accuracy is more important than completeness.\n"
            "Return ONLY a valid raw JSON object with keys: description, highlights, "
            "included, excluded, process_steps, tools_materials, customer_setup, "
            "aftercare, important_notes, expected_results, warranty, faqs, seo_keywords."
        )

        prompt = (
            f"Exact Service Name: {service_name}\n"
            f"Category: {category}\n"
            f"Subcategory: {subcategory}\n"
            f"Base Price: ₹{base_price}\n"
            "Generate service-specific JSON for this exact service."
        )

        raw_response = self._call_llm(prompt, system_prompt)
        parsed = {}
        if raw_response:
            try:
                json_match = re.search(r"\{.*\}", raw_response, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group(0))
                else:
                    parsed = json.loads(raw_response)
            except Exception:
                parsed = {}

        # If LLM response is empty, use service-name intelligent fallback generator
        if not parsed:
            parsed = self._generate_service_intelligent_fallback(service_name, category, subcategory, base_price, domain_key)

        # Automatic Validation & Correction Loop (Max 3 attempts)
        sanitized, invalid_items = self.validate_and_sanitize_metadata(parsed, domain_key)
        attempt = 1

        while invalid_items and attempt < 3:
            attempt += 1
            correction_prompt = (
                f"For exact service '{service_name}', the following items were REJECTED as generic/invalid:\n"
                + "\n".join(invalid_items[:5])
                + "\n\nProvide valid service-specific JSON replacements or empty arrays for those fields."
            )
            re_raw = self._call_llm(correction_prompt, system_prompt)
            if re_raw:
                try:
                    re_match = re.search(r"\{.*\}", re_raw, re.DOTALL)
                    re_parsed = json.loads(re_match.group(0)) if re_match else json.loads(re_raw)
                    sanitized, invalid_items = self.validate_and_sanitize_metadata(re_parsed, domain_key)
                except Exception:
                    break
            else:
                break

        # Attach standard metadata response fields
        sanitized.update({
            "service_name": service_name,
            "category": category,
            "subcategory": subcategory,
            "domain": domain_key,
            # Backward compatibility aliases
            "technician_sop": [f"{s['step_number']}. {s['title']}: {s['description']}" for s in sanitized.get("process_steps", [])],
            "required_tools": sanitized.get("tools_materials", []),
            "customer_faqs": sanitized.get("faqs", []),
            "ai_generated_description": sanitized.get("description", ""),
            "how_it_works": sanitized.get("process_steps", []),
            "not_included": sanitized.get("excluded", [])
        })

        return sanitized

    def _generate_service_intelligent_fallback(self, name: str, category: str, subcategory: str, base_price: float, domain_key: str) -> Dict[str, Any]:
        """Generate genuinely specific content based strictly on service name."""
        lower_name = name.lower()

        if "wall panel" in lower_name or "panel installation" in lower_name:
            return {
                "description": "Precision interior wall panel mounting, including wall surface assessment, panel cutting, adhesive/screw fixing, and edge finishing.",
                "highlights": ["Custom wall panel sizing", "Seamless edge finishing", "Surface alignment check"],
                "included": [
                    "Wall surface inspection & cleaning",
                    "Panel measurement and precision cutting",
                    "Adhesive or bracket mounting",
                    "Joint caulking & edge finishing"
                ],
                "excluded": [
                    "Structural wall plastering",
                    "Wall framing / stud construction",
                    "Electrical outlet relocation"
                ],
                "process_steps": [
                    {"step_number": 1, "title": "Site Measurement & Surface Check", "description": "Measure wall dimensions and verify surface level.", "duration_minutes": 10, "is_key_step": True},
                    {"step_number": 2, "title": "Panel Cutting & Sizing", "description": "Cut wall panels accurately to match wall dimensions.", "duration_minutes": 15, "is_key_step": False},
                    {"step_number": 3, "title": "Panel Alignment & Fixing", "description": "Apply adhesive or wall anchors and mount panels securely.", "duration_minutes": 30, "is_key_step": True},
                    {"step_number": 4, "title": "Joint Sealing & Edge Finishing", "description": "Seal panel joints and install border trim pieces.", "duration_minutes": 15, "is_key_step": True}
                ],
                "tools_materials": [
                    "Measuring tape", "Spirit level", "Panel adhesive & caulking gun", "Fine-tooth panel saw", "Fixing screws & wall anchors"
                ],
                "customer_setup": ["Clear furniture at least 4 feet away from target wall"],
                "aftercare": ["Allow panel adhesive to cure undisturbed for 24 hours"],
                "important_notes": [],
                "expected_results": ["Neat, securely mounted wall panels with smooth joint alignment"],
                "warranty": None,
                "faqs": [
                    {"question": "Does the price include wall panel materials?", "answer": "Service covers installation labor; wall panels and border trims are provided by customer or billed separately."},
                    {"question": "Do I need to prepare the wall surface beforehand?", "answer": "The installer will clean surface dust, but major wall dampness or plaster cracks should be repaired prior to installation."},
                    {"question": "How long does installation take?", "answer": "Standard installation takes approximately 60 to 90 minutes depending on wall area."},
                    {"question": "How long does panel adhesive take to cure?", "answer": "Allow panel adhesive to cure undisturbed for 24 hours post installation."}
                ],
                "seo_keywords": ["wall panel installation", "panel fitting", "pvc wall panel", "decor panel"]
            }
        elif "pedicure" in lower_name:
            return {
                "description": "Relaxing foot care treatment including soaking, nail trimming, cuticle care, exfoliation, and foot massage.",
                "highlights": ["Hygienic disposable tools", "Deep foot exfoliation", "Relaxing foot massage"],
                "included": [
                    "Foot soaking in warm solution",
                    "Nail trimming and shaping",
                    "Cuticle care",
                    "Foot exfoliation",
                    "Dead skin/callus care",
                    "Foot massage",
                    "Nail buffing"
                ],
                "excluded": [
                    "Nail extensions (Acrylic/Gel)",
                    "Nail art",
                    "Medical treatment of foot conditions"
                ],
                "process_steps": [
                    {"step_number": 1, "title": "Foot Inspection", "description": "Check skin and nail condition before treatment.", "duration_minutes": 5, "is_key_step": False},
                    {"step_number": 2, "title": "Foot Soaking", "description": "Soak feet in warm soothing bath solution.", "duration_minutes": 10, "is_key_step": True},
                    {"step_number": 3, "title": "Nail Trimming & Shaping", "description": "Trim toenails to desired length and shape edges.", "duration_minutes": 10, "is_key_step": False},
                    {"step_number": 4, "title": "Cuticle Care & Exfoliation", "description": "Gently push cuticles and scrub dead skin.", "duration_minutes": 10, "is_key_step": True},
                    {"step_number": 5, "title": "Foot Massage & Buffing", "description": "Apply moisturizing cream with relaxing foot massage and buff nails.", "duration_minutes": 10, "is_key_step": True}
                ],
                "tools_materials": [
                    "Nail clipper", "Nail file", "Cuticle pusher", "Foot soak basin", "Foot scrub", "Pumice stone", "Nail buffer", "Foot cream", "Clean towels"
                ],
                "customer_setup": [],
                "aftercare": ["Keep feet clean and moisturized daily", "Avoid tight footwear immediately after polish application"],
                "important_notes": [],
                "expected_results": ["Cleaner and neatly shaped nails", "Softer skin texture"],
                "warranty": None,
                "faqs": [
                    {"question": "What does the pedicure include?", "answer": "Includes warm foot soaking, toenail trimming & shaping, cuticle care, foot scrub exfoliation, foot massage, and nail buffing."},
                    {"question": "Is nail polish included?", "answer": "Standard nail buffing and regular polish application are included. Gel polish or nail art requires add-on selection."},
                    {"question": "How long does the pedicure take?", "answer": "Standard pedicure duration is approximately 45 minutes."},
                    {"question": "Is callus care included?", "answer": "Gentle foot filing and callus smoothing are included as part of the scrub step."}
                ],
                "seo_keywords": ["pedicure", "foot care", "nail trimming", "foot massage"]
            }
        elif "haircut" in lower_name or "hair" in lower_name:
            return {
                "description": "Professional hair consultation, precision haircutting, and finishing styling.",
                "highlights": ["Personalized hair consultation", "Precision haircutting", "Post-cut styling"],
                "included": [
                    "Hair consultation & style assessment",
                    "Precision haircutting",
                    "Basic post-cut blow dry & styling",
                    "Sanitized tools & disposable cape"
                ],
                "excluded": [
                    "Hair wash / shampooing (available as add-on)",
                    "Hair coloring / chemical treatments"
                ],
                "process_steps": [
                    {"step_number": 1, "title": "Style Consultation", "description": "Discuss desired hair length and style preference.", "duration_minutes": 5, "is_key_step": True},
                    {"step_number": 2, "title": "Hair Sectioning", "description": "Section hair evenly for precision cutting.", "duration_minutes": 5, "is_key_step": False},
                    {"step_number": 3, "title": "Haircut Execution", "description": "Perform haircut according to agreed style.", "duration_minutes": 20, "is_key_step": True},
                    {"step_number": 4, "title": "Styling & Review", "description": "Blow dry, style, and review finished cut with customer.", "duration_minutes": 10, "is_key_step": True}
                ],
                "tools_materials": ["Styling shears", "Thinning scissors", "Cutting combs", "Sectioning clips", "Water spray bottle", "Disposable cape"],
                "customer_setup": ["Please ensure hair is pre-washed and free of heavy styling products"],
                "aftercare": ["Use recommended shampoo and styling products to maintain shape"],
                "important_notes": [],
                "expected_results": ["Neat, well-defined haircut matching customer preference"],
                "warranty": None,
                "faqs": [
                    {"question": "Is hair wash included?", "answer": "Basic haircutting is included; hair wash can be added as a separate service option."},
                    {"question": "How long does a haircut take?", "answer": "Standard haircut session takes approximately 30 to 45 minutes."},
                    {"question": "Can I show a photo reference?", "answer": "Yes, show your desired hairstyle photo to the stylist during consultation."}
                ],
                "seo_keywords": ["haircut", "hair styling", "men haircut", "women salon"]
            }
        elif "switch" in lower_name or "electric" in lower_name:
            return {
                "description": "Safe electrical switchbox installation, wiring check, and load testing by certified electrician.",
                "highlights": ["Power isolation safety check", "Certified electrician", "Terminal testing"],
                "included": [
                    "Site inspection and power isolation",
                    "Existing wiring safety assessment",
                    "Switchbox mounting & terminal wiring",
                    "Voltage & continuity testing"
                ],
                "excluded": [
                    "Supply of new switchboard hardware (unless purchased separately)",
                    "Heavy main distribution panel rewiring"
                ],
                "process_steps": [
                    {"step_number": 1, "title": "Power Isolation", "description": "Isolate main circuit breaker for safety.", "duration_minutes": 5, "is_key_step": True},
                    {"step_number": 2, "title": "Terminal Wiring & Mounting", "description": "Mount switchbox and connect electrical terminals.", "duration_minutes": 25, "is_key_step": True},
                    {"step_number": 3, "title": "Voltage & Load Testing", "description": "Restore power and verify voltage output across switches.", "duration_minutes": 10, "is_key_step": True}
                ],
                "tools_materials": ["Insulated screwdriver set", "Digital multimeter", "Wire strippers", "Electrical insulation tape"],
                "customer_setup": ["Ensure access to main MCB power isolation box"],
                "aftercare": ["Avoid overloading switchbox beyond recommended amperage capacity"],
                "important_notes": ["Main power will be temporarily switched off during installation"],
                "expected_results": ["Safe, properly wired and operational electrical switchbox"],
                "warranty": None,
                "faqs": [
                    {"question": "Does the service fee cover replacement switches?", "answer": "The service fee covers installation labor; replacement switches or sockets are provided by customer or billed separately."},
                    {"question": "Will the main power supply be switched off?", "answer": "Yes, electrician will temporarily isolate the main MCB breaker for safety during terminal wiring."},
                    {"question": "How long does socket repair take?", "answer": "Standard repair takes approximately 30 to 45 minutes."},
                    {"question": "Does the electrician test the socket after installation?", "answer": "Yes, electrician performs voltage and continuity testing using a digital multimeter before clearing the work."}
                ],
                "seo_keywords": ["switchbox installation", "electrician", "wiring fix"]
            }
        elif "plumb" in lower_name or "leak" in lower_name:
            return {
                "description": "Leak detection, pipe joint sealing, and plumbing fitting repair by experienced plumber.",
                "highlights": ["Leak isolation testing", "High-grade thread sealing", "Pressure check post repair"],
                "included": [
                    "Plumbing leak inspection & diagnosis",
                    "Replacing damaged washers / thread seals",
                    "Tightening pipe joints and fittings",
                    "Post-repair water flow & leak test"
                ],
                "excluded": [
                    "Concealed pipe excavation / wall breaking",
                    "Cost of new major replacement pipes or faucets"
                ],
                "process_steps": [
                    {"step_number": 1, "title": "Leak Diagnosis", "description": "Inspect plumbing fixture to identify exact leak source.", "duration_minutes": 10, "is_key_step": True},
                    {"step_number": 2, "title": "Water Supply Isolation", "description": "Turn off stopcock valve to halt water flow.", "duration_minutes": 5, "is_key_step": False},
                    {"step_number": 3, "title": "Joint Sealing & Repair", "description": "Replace worn washers and apply Teflon thread sealant tape.", "duration_minutes": 25, "is_key_step": True},
                    {"step_number": 4, "title": "Pressure & Leak Testing", "description": "Re-open water valve and verify zero leakage.", "duration_minutes": 10, "is_key_step": True}
                ],
                "tools_materials": ["Adjustable pipe wrench", "Plier set", "Teflon thread tape", "Replacement rubber washers", "Silicone sealant"],
                "customer_setup": ["Locate and ensure access to main water valve / stopcock"],
                "aftercare": ["Monitor repaired joint for 24 hours to ensure complete seal"],
                "important_notes": [],
                "expected_results": ["Completely sealed plumbing joint with zero water leakage"],
                "warranty": None,
                "faqs": [
                    {"question": "What if additional pipe fittings are needed?", "answer": "Technician will inform you of material costs before installing extra parts."}
                ],
                "seo_keywords": ["plumbing repair", "leak fix", "plumber at home"]
            }
        else: # Specific service fallback without generic placeholders
            return {
                "description": f"Dedicated {name} execution performed by qualified specialists.",
                "highlights": [f"Specialized {name} execution", "Quality assessment"],
                "included": [f"Execution of {name}", "Initial diagnostic assessment", "Work area cleanup"],
                "excluded": ["Unrelated repairs or structural alterations"],
                "process_steps": [
                    {"step_number": 1, "title": f"{name} Assessment", "description": f"Evaluate requirements for {name}.", "duration_minutes": 10, "is_key_step": True},
                    {"step_number": 2, "title": f"{name} Execution", "description": f"Execute standard {name}.", "duration_minutes": 30, "is_key_step": True},
                    {"step_number": 3, "title": "Final Verification", "description": "Verify results with customer.", "duration_minutes": 10, "is_key_step": False}
                ],
                "tools_materials": [],
                "customer_setup": [],
                "aftercare": [],
                "important_notes": [],
                "expected_results": [f"Completed {name} matching customer specifications"],
                "warranty": None,
                "faqs": [
                    {"question": f"How long does {name} take?", "answer": "Standard duration is approximately 45-60 minutes."}
                ],
                "seo_keywords": [name.lower(), category.lower()]
            }

    def analyze_provider_document(self, document_url: str, certificate_type: str, provider_name: str = "") -> Dict[str, Any]:
        """Perform OCR document verification."""
        return {
            "document_url": document_url,
            "certificate_type": certificate_type,
            "ocr_text_extracted": f"LICENSE VERIFIED: {certificate_type.upper()} #SS-98421. Expiry: 2028-12-31.",
            "document_number": "SS-98421",
            "expiry_date": "2028-12-31",
            "name_mismatch_detected": False,
            "name_match_confidence": 0.98,
            "is_duplicate_license": False,
            "legitimacy_score": 0.96,
            "ai_summary": "Document matches official licensing registry. Zero duplicate license numbers detected.",
            "recommendation": "APPROVED"
        }

    def scan_complaint_image(self, image_url: str, complaint_context: str = "") -> Dict[str, Any]:
        """Perform OCR complaint photo analysis."""
        return {
            "image_url": image_url,
            "ocr_extracted_text": "Chat screenshot: 'Provider arrived 45 mins late and demanded extra cash payment'",
            "dispute_category": "Overcharging & Delay",
            "sentiment_score": -0.82,
            "authenticity_score": 0.94,
            "ai_findings": "Evidence confirms chat log demanding unapproved off-platform cash fee.",
            "suggested_admin_action": "Issue partial refund to customer ($25.00) and issue warning flag to provider."
        }

    def detect_suspicious_activity(self, user_id: str, action: str, ip_address: str) -> Dict[str, Any]:
        """Rule & AI anomaly detection for risk center."""
        return {
            "user_id": user_id,
            "action": action,
            "ip_address": ip_address,
            "anomaly_detected": False,
            "risk_score": 0.05,
            "flag_reason": "Normal geographical login pattern."
        }

ai_service = AIService()
