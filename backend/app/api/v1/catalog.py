import uuid
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

@router.get("/services", response_model=List[ServiceResponse])
def list_catalog_services(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Retrieve full catalog services hierarchy."""
    services = service_repository.get_services(db, skip=skip, limit=limit, category=category, subcategory=subcategory)
    return [
        ServiceResponse(
            id=str(s.id),
            category=s.category,
            subcategory=s.subcategory,
            name=s.name,
            base_price=s.base_price,
            max_demand_increase=s.max_demand_increase,
            max_discount=s.max_discount,
            distinct_features=s.distinct_features or [],
            suggested_addons=s.suggested_addons or [],
            is_active=s.is_active,
            created_at=s.created_at.isoformat()
        ) for s in services
    ]

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

    return ServiceResponse(
        id=str(service.id),
        category=service.category,
        subcategory=service.subcategory,
        name=service.name,
        base_price=service.base_price,
        max_demand_increase=service.max_demand_increase,
        max_discount=service.max_discount,
        distinct_features=service.distinct_features or [],
        suggested_addons=service.suggested_addons or [],
        is_active=service.is_active,
        created_at=service.created_at.isoformat(),
        description=req.description,
        included=req.included,
        excluded=req.excluded,
        process_steps=req.process_steps,
        aftercare=req.aftercare,
        warranty=req.warranty,
        faqs=req.faqs
    )

@router.put("/services/{service_id}", response_model=ServiceResponse)
def update_service_item(
    service_id: str,
    req: ServiceUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("catalog:edit"))
):
    """Update existing service pricing, demand increase limits, or features."""
    try:
        s_uuid = uuid.UUID(service_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid service ID format")

    service = service_repository.get_service_by_id(db, s_uuid)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    old_price = service.base_price
    old_active = service.is_active
    old_name = service.name

    distinct_features = req.distinct_features if req.distinct_features is not None else service.distinct_features
    if req.included is not None:
        distinct_features = req.included

    suggested_addons = list(req.suggested_addons if req.suggested_addons is not None else (service.suggested_addons or []))
    if any([req.description, req.excluded is not None, req.process_steps is not None, req.aftercare is not None, req.tools_materials is not None, req.customer_setup is not None, req.expected_results is not None, req.important_notes is not None, req.warranty is not None, req.faqs is not None, req.tips is not None, req.dos is not None, req.donts is not None, req.duration_minutes is not None]):
        types_to_replace = set()
        if req.description: types_to_replace.add("description")
        if req.excluded is not None: types_to_replace.add("excluded_scope")
        if req.process_steps is not None: types_to_replace.add("process_steps")
        if req.aftercare is not None: types_to_replace.add("aftercare_precautions")
        if req.tools_materials is not None: types_to_replace.add("tools_materials")
        if req.customer_setup is not None: types_to_replace.add("customer_setup")
        if req.expected_results is not None: types_to_replace.add("expected_results")
        if req.important_notes is not None: types_to_replace.add("important_notes")
        if req.warranty is not None: types_to_replace.add("warranty")
        if req.faqs is not None: types_to_replace.add("faqs")
        if req.tips is not None: types_to_replace.add("tips")
        if req.dos is not None or req.donts is not None: types_to_replace.add("dos_donts")
        if req.duration_minutes is not None: types_to_replace.add("duration")

        filtered = [a for a in suggested_addons if not (isinstance(a, dict) and a.get("type") in types_to_replace)]
        if req.description:
            filtered.append({"type": "description", "text": req.description})
        if req.excluded is not None:
            filtered.append({"type": "excluded_scope", "items": req.excluded})
        if req.process_steps is not None:
            filtered.append({"type": "process_steps", "steps": req.process_steps})
        if req.aftercare is not None:
            filtered.append({"type": "aftercare_precautions", "aftercare": req.aftercare})
        if req.tools_materials is not None:
            filtered.append({"type": "tools_materials", "tools": req.tools_materials})
        if req.customer_setup is not None:
            filtered.append({"type": "customer_setup", "requirements": req.customer_setup})
        if req.expected_results is not None:
            filtered.append({"type": "expected_results", "items": req.expected_results})
        if req.important_notes is not None:
            filtered.append({"type": "important_notes", "items": req.important_notes})
        if req.warranty is not None:
            filtered.append({"type": "warranty", "has_warranty": bool(req.warranty.strip()), "details": req.warranty})
        if req.faqs is not None:
            filtered.append({"type": "faqs", "items": req.faqs})
        if req.tips is not None:
            filtered.append({"type": "tips", "items": req.tips})
        if req.dos is not None or req.donts is not None:
            filtered.append({"type": "dos_donts", "dos": req.dos or [], "donts": req.donts or []})
        if req.duration_minutes is not None:
            filtered.append({"type": "duration", "minutes": req.duration_minutes})
        suggested_addons = filtered

    updated = service_repository.update_service(
        db,
        service=service,
        name=req.name,
        category=req.category,
        subcategory=req.subcategory,
        base_price=req.base_price,
        max_demand_increase=req.max_demand_increase,
        max_discount=req.max_discount,
        distinct_features=distinct_features,
        suggested_addons=suggested_addons,
        is_active=req.is_active
    )

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
            "old_price": old_price,
            "new_price": updated.base_price,
            "old_active": old_active,
            "new_active": updated.is_active,
            "changes_summary": change_desc,
            "changes": changes
        }
    )

    return ServiceResponse(
        id=str(updated.id),
        category=updated.category,
        subcategory=updated.subcategory,
        name=updated.name,
        base_price=updated.base_price,
        max_demand_increase=updated.max_demand_increase,
        max_discount=updated.max_discount,
        distinct_features=updated.distinct_features or [],
        suggested_addons=updated.suggested_addons or [],
        is_active=updated.is_active,
        created_at=updated.created_at.isoformat()
    )

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
