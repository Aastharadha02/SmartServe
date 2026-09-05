import uuid
import datetime
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin, require_permission
from app.repositories.db import get_db
from app.repositories import service_repository, audit_repository
from app.models.user import User
from app.schemas.catalog import ServiceCreateRequest, ServiceUpdateRequest, ServiceResponse
from app.schemas.security import AuditLogResponse
from app.services import excel_service
from app.services.ai_service import ai_service

router = APIRouter(prefix="/admin/catalog", tags=["Admin Catalog Management"])

def safe_extract_service_response(s) -> ServiceResponse:
    addons = s.suggested_addons or []
    real_addons = [a for a in addons if isinstance(a, dict) and not a.get("type")]
    
    features_dict = s.distinct_features if isinstance(s.distinct_features, dict) else {}
    features_list = s.distinct_features if isinstance(s.distinct_features, list) else []
    
    # 1. Description
    desc_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") in ["description", "service_description"]), None)
    description = (desc_obj.get("text") or desc_obj.get("description") or desc_obj.get("content")) if desc_obj else (features_dict.get("description") or None)
    
    # 2. Highlights
    hl_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "highlights"), None)
    seo_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "seo_metadata"), None)
    highlights = None
    if hl_obj and isinstance(hl_obj.get("items"), list):
        highlights = hl_obj.get("items")
    elif seo_obj and isinstance(seo_obj.get("highlights"), list):
        highlights = seo_obj.get("highlights")
    elif features_dict.get("highlights") and isinstance(features_dict.get("highlights"), list):
        highlights = features_dict.get("highlights")
        
    # 3. Included & Distinct features (guaranteed List[str])
    if features_list:
        included = [str(x) for x in features_list]
        distinct_features_clean = included
    elif features_dict:
        inc = features_dict.get("included") or features_dict.get("highlights") or []
        if isinstance(inc, list):
            included = [str(x) for x in inc]
        else:
            included = [str(inc)] if inc else []
        distinct_features_clean = included
    else:
        included = []
        distinct_features_clean = []
    
    # 4. Excluded
    exc_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") in ["excluded_scope", "exclusions"]), None)
    excluded = (exc_obj.get("items") or exc_obj.get("exclusions")) if exc_obj else (features_dict.get("excluded") if isinstance(features_dict.get("excluded"), list) else None)
    
    # 5. Process Steps
    proc_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "process_steps"), None)
    process_steps = (proc_obj.get("steps") or proc_obj.get("items")) if proc_obj else None
    
    # 6. Aftercare
    ac_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "aftercare_precautions"), None)
    aftercare = (ac_obj.get("aftercare") or ac_obj.get("items") or ac_obj.get("precautions")) if ac_obj else None
    
    # 7. Tools & Materials
    tm_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "tools_materials"), None)
    tools_materials = (tm_obj.get("tools") or tm_obj.get("items") or tm_obj.get("materials")) if tm_obj else None
    
    # 8. Customer Setup
    cs_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "customer_setup"), None)
    customer_setup = (cs_obj.get("requirements") or cs_obj.get("items") or cs_obj.get("setup")) if cs_obj else None
    
    # 9. Expected Results
    er_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "expected_results"), None)
    expected_results = (er_obj.get("items") or er_obj.get("results")) if er_obj else None
    
    # 10. Important Notes
    in_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "important_notes"), None)
    important_notes = (in_obj.get("items") or in_obj.get("notes")) if in_obj else None
    
    # 11. Warranty
    w_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "warranty"), None)
    warranty = (w_obj.get("details") or w_obj.get("warranty")) if w_obj else (features_dict.get("warranty") or None)
    
    # 12. FAQs
    faq_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "faqs"), None)
    faqs = (faq_obj.get("items") or faq_obj.get("faqs")) if faq_obj else (features_dict.get("faqs") if isinstance(features_dict.get("faqs"), list) else None)
    
    # 13. Tips
    tips_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "tips"), None)
    tips = (tips_obj.get("items") or tips_obj.get("tips")) if tips_obj else None
    
    # 14. Dos & Don'ts
    dd_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "dos_donts"), None)
    dos = dd_obj.get("dos") if dd_obj else None
    donts = dd_obj.get("donts") if dd_obj else None
    
    # 15. Duration
    dur_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") in ["duration", "estimated_duration"]), None)
    duration_minutes = (dur_obj.get("minutes") or dur_obj.get("duration")) if dur_obj else None
    
    # 16. Service Media & Features & SEO
    sm_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "service_media"), None)
    service_media = sm_obj.get("items") if sm_obj else None
    sf_obj = next((a for a in addons if isinstance(a, dict) and a.get("type") == "service_features"), None)
    service_features = sf_obj.get("items") if sf_obj else None
    
    return ServiceResponse(
        id=str(s.id),
        category=s.category,
        subcategory=s.subcategory,
        name=s.name,
        base_price=s.base_price,
        max_demand_increase=s.max_demand_increase,
        max_discount=s.max_discount,
        distinct_features=distinct_features_clean,
        suggested_addons=s.suggested_addons or [],
        is_active=s.is_active,
        created_at=s.created_at.isoformat() if s.created_at else "",
        description=description,
        highlights=highlights,
        included=included,
        excluded=excluded,
        process_steps=process_steps,
        aftercare=aftercare,
        tools_materials=tools_materials,
        customer_setup=customer_setup,
        expected_results=expected_results,
        important_notes=important_notes,
        warranty=warranty,
        faqs=faqs,
        tips=tips,
        dos=dos,
        donts=donts,
        duration_minutes=int(duration_minutes) if duration_minutes is not None else None,
        addons=real_addons,
        service_media=service_media,
        service_features=service_features,
        seo_metadata=seo_obj
    )

@router.get("/services", response_model=List[ServiceResponse])
def list_catalog_services(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Retrieve full catalog services hierarchy with metadata unpacked."""
    services = service_repository.get_services(db, skip=skip, limit=limit, category=category, subcategory=subcategory)
    return [safe_extract_service_response(s) for s in services]

@router.get("/services/{service_id}", response_model=ServiceResponse)
def get_service_item(
    service_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Retrieve a single service item by ID with full metadata unpacked."""
    try:
        s_uuid = uuid.UUID(service_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid service ID format")

    service = service_repository.get_service_by_id(db, s_uuid)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return safe_extract_service_response(service)

@router.post("/services", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service_item(
    req: ServiceCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("catalog:create"))
):
    """Create a new service catalog item."""
    distinct_features = list(req.distinct_features or [])
    if req.included:
        for inc in req.included:
            if inc not in distinct_features:
                distinct_features.append(inc)

    suggested_addons = list(req.suggested_addons or [])
    if req.description:
        suggested_addons.append({"type": "description", "text": req.description})
    if req.highlights:
        suggested_addons.append({"type": "highlights", "items": req.highlights})
    if req.excluded:
        suggested_addons.append({"type": "excluded_scope", "items": req.excluded})
    if req.process_steps:
        suggested_addons.append({"type": "process_steps", "steps": req.process_steps})
    if req.aftercare:
        suggested_addons.append({"type": "aftercare_precautions", "aftercare": req.aftercare})
    if req.tools_materials:
        suggested_addons.append({"type": "tools_materials", "tools": req.tools_materials})
    if req.customer_setup:
        suggested_addons.append({"type": "customer_setup", "requirements": req.customer_setup})
    if req.expected_results:
        suggested_addons.append({"type": "expected_results", "items": req.expected_results})
    if req.important_notes:
        suggested_addons.append({"type": "important_notes", "items": req.important_notes})
    if req.warranty:
        suggested_addons.append({"type": "warranty", "has_warranty": True, "details": req.warranty})
    if req.faqs:
        suggested_addons.append({"type": "faqs", "items": req.faqs})
    if req.tips:
        suggested_addons.append({"type": "tips", "items": req.tips})
    if req.dos or req.donts:
        suggested_addons.append({"type": "dos_donts", "dos": req.dos or [], "donts": req.donts or []})
    if req.duration_minutes:
        suggested_addons.append({"type": "duration", "minutes": req.duration_minutes})
    if req.service_media:
        suggested_addons.append({"type": "service_media", "items": req.service_media})
    if req.service_features:
        suggested_addons.append({"type": "service_features", "items": req.service_features})
    if req.seo_metadata:
        suggested_addons.append(req.seo_metadata)

    service = service_repository.create_service(
        db,
        category=req.category,
        subcategory=req.subcategory,
        name=req.name,
        base_price=req.base_price,
        max_demand_increase=req.max_demand_increase,
        max_discount=req.max_discount,
        distinct_features=distinct_features,
        suggested_addons=suggested_addons,
        is_active=req.is_active
    )

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Created Service Catalog Item '{service.name}'", target_resource=str(service.id)
    )

    return safe_extract_service_response(service)

@router.put("/services/{service_id}", response_model=ServiceResponse)
def update_service_item(
    service_id: str,
    req: ServiceUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("catalog:edit"))
):
    """Safely update existing service pricing, features, or metadata without overwriting unspecified data."""
    try:
        s_uuid = uuid.UUID(service_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid service ID format")

    service = service_repository.get_service_by_id(db, s_uuid)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # Capture fields explicitly supplied in the request payload
    fields_set = getattr(req, "model_fields_set", set())

    # Snapshot previous state for rollback and versioned audit trail
    old_price = service.base_price
    old_active = service.is_active
    old_name = service.name
    old_snapshot = {
        "name": service.name,
        "category": service.category,
        "subcategory": service.subcategory,
        "base_price": service.base_price,
        "is_active": service.is_active,
        "distinct_features": list(service.distinct_features or []),
        "suggested_addons": list(service.suggested_addons or [])
    }

    # Core attribute updates (preserve existing if field was omitted)
    new_name = req.name if "name" in fields_set and req.name is not None and req.name.strip() else service.name
    new_cat = req.category if "category" in fields_set and req.category is not None and req.category.strip() else service.category
    new_subcat = req.subcategory if "subcategory" in fields_set and req.subcategory is not None and req.subcategory.strip() else service.subcategory
    new_price = req.base_price if "base_price" in fields_set and req.base_price is not None and req.base_price > 0 else service.base_price
    new_demand = req.max_demand_increase if "max_demand_increase" in fields_set and req.max_demand_increase is not None else service.max_demand_increase
    new_discount = req.max_discount if "max_discount" in fields_set and req.max_discount is not None else service.max_discount
    new_active = req.is_active if "is_active" in fields_set and req.is_active is not None else service.is_active

    # 1. Non-destructive distinct_features (Inclusions)
    distinct_features = list(service.distinct_features or [])
    if "included" in fields_set and req.included is not None:
        if len(req.included) > 0 or not distinct_features:
            distinct_features = list(req.included)
    elif "distinct_features" in fields_set and req.distinct_features is not None:
        if len(req.distinct_features) > 0 or not distinct_features:
            distinct_features = list(req.distinct_features)

    # 2. Extract existing addons and typed metadata blocks
    existing_addons = list(service.suggested_addons or [])
    existing_real_addons = [a for a in existing_addons if isinstance(a, dict) and not a.get("type")]
    existing_typed_blocks = [a for a in existing_addons if isinstance(a, dict) and a.get("type")]
    blocks_by_type = {a.get("type"): dict(a) for a in existing_typed_blocks}

    # 3. Real Add-ons Preservation (NEVER silently clear existing real add-ons)
    if "addons" in fields_set and req.addons is not None and len(req.addons) > 0:
        final_real_addons = list(req.addons)
    elif "suggested_addons" in fields_set and req.suggested_addons is not None:
        incoming_real_addons = [a for a in req.suggested_addons if isinstance(a, dict) and not a.get("type")]
        final_real_addons = incoming_real_addons if incoming_real_addons else existing_real_addons
    else:
        final_real_addons = existing_real_addons

    def is_block_meaningfully_empty(b: dict) -> bool:
        if not isinstance(b, dict):
            return True
        b_type = b.get("type")
        if not b_type:
            return False
        if b_type in ("description", "service_description"):
            txt = b.get("text") or b.get("description") or b.get("content")
            return not bool(txt and str(txt).strip())
        if b_type == "highlights":
            items = b.get("items") or b.get("highlights")
            return not bool(items and len(items) > 0)
        if b_type in ("excluded_scope", "exclusions"):
            items = b.get("items") or b.get("exclusions")
            return not bool(items and len(items) > 0)
        if b_type == "process_steps":
            steps = b.get("steps") or b.get("items")
            return not bool(steps and len(steps) > 0)
        if b_type == "aftercare_precautions":
            items = b.get("aftercare") or b.get("items") or b.get("precautions")
            return not bool(items and len(items) > 0)
        if b_type == "tools_materials":
            tools = b.get("tools") or b.get("items")
            materials = b.get("materials")
            return not bool((tools and len(tools) > 0) or (materials and len(materials) > 0))
        if b_type == "customer_setup":
            items = b.get("requirements") or b.get("items") or b.get("setup")
            return not bool(items and len(items) > 0)
        if b_type == "expected_results":
            items = b.get("items") or b.get("results")
            return not bool(items and len(items) > 0)
        if b_type == "important_notes":
            items = b.get("items") or b.get("notes")
            return not bool(items and len(items) > 0)
        if b_type == "warranty":
            return not bool(b.get("has_warranty") or (b.get("details") and str(b.get("details")).strip()))
        if b_type == "faqs":
            items = b.get("items") or b.get("faqs")
            return not bool(items and len(items) > 0)
        if b_type == "tips":
            items = b.get("items") or b.get("tips")
            return not bool(items and len(items) > 0)
        if b_type == "dos_donts":
            dos = b.get("dos")
            donts = b.get("donts")
            return not bool((dos and len(dos) > 0) or (donts and len(donts) > 0))
        if b_type == "service_media":
            items = b.get("items")
            return not bool(items and len(items) > 0)
        if b_type == "service_features":
            items = b.get("items")
            return not bool(items and len(items) > 0)
        if b_type == "seo_metadata":
            return not bool(b.get("seo_title") or b.get("seo_description") or b.get("keywords") or b.get("highlights"))
        return False

    # 4. Typed Metadata Blocks Safe Non-destructive Merge
    if "description" in fields_set and req.description is not None:
        if req.description.strip():
            blocks_by_type["description"] = {"type": "description", "text": req.description.strip()}

    if "highlights" in fields_set and req.highlights is not None:
        if len(req.highlights) > 0:
            blocks_by_type["highlights"] = {"type": "highlights", "items": req.highlights}
            if "seo_metadata" in blocks_by_type:
                seo = dict(blocks_by_type["seo_metadata"])
                seo["highlights"] = req.highlights
                blocks_by_type["seo_metadata"] = seo

    if "excluded" in fields_set and req.excluded is not None:
        if len(req.excluded) > 0:
            blocks_by_type["excluded_scope"] = {"type": "excluded_scope", "items": req.excluded}

    if "process_steps" in fields_set and req.process_steps is not None:
        if len(req.process_steps) > 0:
            blocks_by_type["process_steps"] = {"type": "process_steps", "steps": req.process_steps}

    if "aftercare" in fields_set and req.aftercare is not None:
        if len(req.aftercare) > 0:
            blocks_by_type["aftercare_precautions"] = {"type": "aftercare_precautions", "aftercare": req.aftercare}

    if "tools_materials" in fields_set and req.tools_materials is not None:
        if len(req.tools_materials) > 0:
            existing_tm = blocks_by_type.get("tools_materials", {})
            existing_mat = existing_tm.get("materials", []) if isinstance(existing_tm, dict) else []
            blocks_by_type["tools_materials"] = {"type": "tools_materials", "tools": req.tools_materials, "materials": existing_mat}

    if "customer_setup" in fields_set and req.customer_setup is not None:
        if len(req.customer_setup) > 0:
            blocks_by_type["customer_setup"] = {"type": "customer_setup", "requirements": req.customer_setup}

    if "expected_results" in fields_set and req.expected_results is not None:
        if len(req.expected_results) > 0:
            blocks_by_type["expected_results"] = {"type": "expected_results", "items": req.expected_results}

    if "important_notes" in fields_set and req.important_notes is not None:
        if len(req.important_notes) > 0:
            blocks_by_type["important_notes"] = {"type": "important_notes", "items": req.important_notes}

    if "warranty" in fields_set and req.warranty is not None:
        if req.warranty.strip():
            blocks_by_type["warranty"] = {
                "type": "warranty",
                "has_warranty": True,
                "details": req.warranty.strip()
            }
        else:
            blocks_by_type["warranty"] = {
                "type": "warranty",
                "has_warranty": False,
                "details": None
            }

    if "faqs" in fields_set and req.faqs is not None:
        if len(req.faqs) > 0:
            blocks_by_type["faqs"] = {"type": "faqs", "items": req.faqs}

    if "tips" in fields_set and req.tips is not None:
        if len(req.tips) > 0:
            blocks_by_type["tips"] = {"type": "tips", "items": req.tips}

    if ("dos" in fields_set and req.dos is not None) or ("donts" in fields_set and req.donts is not None):
        existing_dd = blocks_by_type.get("dos_donts", {})
        cur_dos = req.dos if ("dos" in fields_set and req.dos is not None) else (existing_dd.get("dos", []) if isinstance(existing_dd, dict) else [])
        cur_donts = req.donts if ("donts" in fields_set and req.donts is not None) else (existing_dd.get("donts", []) if isinstance(existing_dd, dict) else [])
        if cur_dos or cur_donts:
            blocks_by_type["dos_donts"] = {"type": "dos_donts", "dos": cur_dos, "donts": cur_donts}

    if "duration_minutes" in fields_set and req.duration_minutes is not None:
        blocks_by_type["duration"] = {"type": "duration", "minutes": req.duration_minutes}

    if "service_media" in fields_set and req.service_media is not None:
        if len(req.service_media) > 0:
            blocks_by_type["service_media"] = {"type": "service_media", "items": req.service_media}

    if "service_features" in fields_set and req.service_features is not None:
        if len(req.service_features) > 0:
            blocks_by_type["service_features"] = {"type": "service_features", "items": req.service_features}

    if "seo_metadata" in fields_set and req.seo_metadata is not None:
        if req.seo_metadata:
            blocks_by_type["seo_metadata"] = req.seo_metadata

    # Merge incoming suggested_addons for any custom blocks not updated by explicit top-level fields
    explicit_types_passed = {
        "description": "description" in fields_set,
        "highlights": "highlights" in fields_set,
        "excluded_scope": "excluded" in fields_set,
        "process_steps": "process_steps" in fields_set,
        "aftercare_precautions": "aftercare" in fields_set,
        "tools_materials": "tools_materials" in fields_set,
        "customer_setup": "customer_setup" in fields_set,
        "expected_results": "expected_results" in fields_set,
        "important_notes": "important_notes" in fields_set,
        "warranty": "warranty" in fields_set,
        "faqs": "faqs" in fields_set,
        "tips": "tips" in fields_set,
        "dos_donts": ("dos" in fields_set or "donts" in fields_set),
        "duration": "duration_minutes" in fields_set,
        "service_media": "service_media" in fields_set,
        "service_features": "service_features" in fields_set,
        "seo_metadata": "seo_metadata" in fields_set
    }
    if "suggested_addons" in fields_set and req.suggested_addons is not None:
        for b in req.suggested_addons:
            if isinstance(b, dict) and b.get("type"):
                b_type = b.get("type")
                if not explicit_types_passed.get(b_type, False):
                    # Never overwrite existing non-empty block with an empty block
                    if b_type in blocks_by_type and is_block_meaningfully_empty(b) and not is_block_meaningfully_empty(blocks_by_type[b_type]):
                        continue
                    if not is_block_meaningfully_empty(b):
                        blocks_by_type[b_type] = b

    # Clean out any empty placeholder blocks
    clean_blocks = [b for b in blocks_by_type.values() if not is_block_meaningfully_empty(b)]
    final_suggested_addons = list(final_real_addons) + clean_blocks

    # Transaction safety: execute update with verification and rollback
    try:
        service.name = new_name
        service.category = new_cat
        service.subcategory = new_subcat
        service.base_price = new_price
        service.max_demand_increase = new_demand
        service.max_discount = new_discount
        service.distinct_features = distinct_features
        service.suggested_addons = final_suggested_addons
        service.is_active = new_active

        db.commit()
        db.refresh(service)

        # Fresh SELECT to verify database write
        updated = service_repository.get_service_by_id(db, s_uuid)
        if not updated:
            db.rollback()
            raise HTTPException(status_code=500, detail="Service update verification failed on fresh SELECT")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database update transaction failed: {str(e)}")

    # SQLite parity sync
    try:
        import sqlite3, json, os
        sqlite_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "smartserve_dev.db"))
        if os.path.exists(sqlite_file):
            conn = sqlite3.connect(sqlite_file)
            cur = conn.cursor()
            cur.execute("""
                UPDATE services
                SET name = ?, category = ?, subcategory = ?, base_price = ?,
                    max_demand_increase = ?, max_discount = ?, distinct_features = ?,
                    suggested_addons = ?, is_active = ?
                WHERE id = ? OR id = ?
            """, (
                updated.name, updated.category, updated.subcategory, updated.base_price,
                updated.max_demand_increase, updated.max_discount,
                json.dumps(updated.distinct_features or []),
                json.dumps(updated.suggested_addons or []),
                1 if updated.is_active else 0,
                str(updated.id),
                str(updated.id).replace("-", "")
            ))
            conn.commit()
            conn.close()
    except Exception:
        pass

    changes = []
    if old_price != updated.base_price:
        changes.append(f"Price updated from ₹{old_price} to ₹{updated.base_price}")
    if old_active != updated.is_active:
        changes.append(f"Status changed from {'Active' if old_active else 'Inactive'} to {'Active' if updated.is_active else 'Inactive'}")
    if old_name != updated.name:
        changes.append(f"Name updated from '{old_name}' to '{updated.name}'")

    change_desc = ", ".join(changes) if changes else "Service details updated"

    audit_repository.create_audit_log(
        db,
        actor_id=admin.id,
        actor_email=admin.email,
        actor_role=admin.role,
        action=f"Updated Service Item '{updated.name}'",
        target_resource=str(updated.id),
        risk_level="Info",
        metadata_json={
            "service_id": str(updated.id),
            "service_name": updated.name,
            "operation_type": "CATALOG_UPDATE",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "fields_modified": list(fields_set),
            "old_price": old_price,
            "new_price": updated.base_price,
            "old_active": old_active,
            "new_active": updated.is_active,
            "changes_summary": change_desc,
            "changes": changes,
            "previous_state": old_snapshot,
            "new_state": {
                "name": updated.name,
                "category": updated.category,
                "subcategory": updated.subcategory,
                "base_price": updated.base_price,
                "is_active": updated.is_active,
                "distinct_features": list(updated.distinct_features or []),
                "suggested_addons": list(updated.suggested_addons or [])
            }
        }
    )

    return safe_extract_service_response(updated)


@router.get("/services/{service_id}/audit-logs", response_model=List[AuditLogResponse])
def get_service_audit_history(
    service_id: str,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Retrieve immutable change history & audit trail for a specific service item."""
    logs = audit_repository.get_audit_logs_for_service(db, service_id, skip=skip, limit=limit)
    return [
        AuditLogResponse(
            id=str(l.id),
            actor_email=l.actor_email,
            actor_role=l.actor_role,
            action=l.action,
            target_resource=l.target_resource,
            ip_address=l.ip_address,
            risk_level=l.risk_level,
            created_at=l.created_at.isoformat() if l.created_at else "",
            metadata_json=l.metadata_json or {}
        ) for l in logs
    ]

@router.get("/export-excel")
def export_catalog_excel(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Export filtered or complete service catalog to Excel spreadsheet (.xlsx)."""
    excel_bytes = excel_service.generate_catalog_excel(db, category=category, subcategory=subcategory, search=search)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=SmartServe_Catalog_Export.xlsx"}
    )

@router.post("/preview-import-excel")
async def preview_import_catalog_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Preview and validate uploaded Excel catalog spreadsheet without modifying database."""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx) are supported")

    contents = await file.read()
    preview_data = excel_service.preview_import_catalog_excel(db, contents)
    return preview_data

@router.post("/import-excel")
async def import_catalog_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("catalog:import"))
):
    """Bulk import or update catalog items from an uploaded Excel spreadsheet (.xlsx)."""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx) are supported")

    contents = await file.read()
    inserted, updated, errors = excel_service.parse_and_import_catalog_excel(db, contents, admin.email)

    return {
        "status": "success",
        "inserted": inserted,
        "updated": updated,
        "errors": errors
    }

class BulkStatusPayload(BaseModel):
    service_ids: List[str]
    is_active: bool

@router.post("/services/bulk-status")
def bulk_update_service_status(
    payload: BulkStatusPayload,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("catalog:edit"))
):
    """Bulk activate or deactivate selected service items."""
    updated_count = 0
    for sid in payload.service_ids:
        try:
            s_uuid = uuid.UUID(sid)
            service = service_repository.get_service_by_id(db, s_uuid)
            if service:
                service_repository.update_service(db, service, is_active=payload.is_active)
                updated_count += 1
        except ValueError:
            pass

    status_str = "Activated" if payload.is_active else "Deactivated"
    audit_repository.create_audit_log(
        db,
        actor_id=admin.id,
        actor_email=admin.email,
        actor_role=admin.role,
        action=f"Bulk Service Status Change: {updated_count} services {status_str}",
        risk_level="Info",
        metadata_json={
            "service_ids": payload.service_ids,
            "is_active": payload.is_active,
            "updated_count": updated_count
        }
    )

    return {
        "status": "success",
        "updated_count": updated_count,
        "is_active": payload.is_active
    }

@router.post("/services/{service_id}/ai-generate-metadata")
def generate_ai_service_metadata(
    service_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """AI Generator for SEO keywords, technician SOPs, and customer FAQs using OpenRouter."""
    try:
        s_uuid = uuid.UUID(service_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid service ID format")

    service = service_repository.get_service_by_id(db, s_uuid)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    meta = ai_service.generate_service_metadata(
        category=service.category, 
        service_name=service.name, 
        base_price=service.base_price,
        subcategory=service.subcategory,
        existing_features=service.distinct_features or []
    )

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Generated AI Metadata for Service '{service.name}'", target_resource=service_id
    )

    return meta
