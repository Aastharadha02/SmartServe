import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.provider import Provider, Certificate, Availability, ProviderService
from app.schemas.provider import (
    ProviderProfileUpdate,
    CertificateCreate,
    AvailabilityCreate,
    ProviderServiceCreate,
    ProviderServiceUpdate,
)


class ProviderRepository:
    def __init__(self, db: Session):
        self.db = db

    # ==========================================
    # PROVIDER OPERATIONS
    # ==========================================

    def get_by_user_id(self, user_id: uuid.UUID) -> Optional[Provider]:
        return self.db.query(Provider).filter(Provider.user_id == user_id).first()

    def get_or_create(self, user_id: uuid.UUID, default_name: str = "Service Provider") -> Provider:
        provider = self.get_by_user_id(user_id)
        if not provider:
            provider = Provider(
                user_id=user_id,
                full_name=default_name,
            )
            self.db.add(provider)
            self.db.commit()
            self.db.refresh(provider)
        return provider

    def update_profile(self, provider: Provider, update_data: ProviderProfileUpdate) -> Provider:
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(provider, field, value)
        self.db.commit()
        self.db.refresh(provider)
        return provider

    # ==========================================
    # CERTIFICATE OPERATIONS
    # ==========================================

    def create_certificate(self, provider_id: uuid.UUID, data: CertificateCreate) -> Certificate:
        cert = Certificate(
            provider_id=provider_id,
            document_url=data.document_url,
            certificate_type=data.certificate_type,
            verification_status="PENDING",
        )
        self.db.add(cert)
        self.db.commit()
        self.db.refresh(cert)
        return cert

    def list_certificates_by_provider(self, provider_id: uuid.UUID) -> List[Certificate]:
        return (
            self.db.query(Certificate)
            .filter(Certificate.provider_id == provider_id)
            .order_by(Certificate.uploaded_at.desc())
            .all()
        )

    # ==========================================
    # AVAILABILITY OPERATIONS
    # ==========================================

    def create_availability_slot(self, provider_id: uuid.UUID, data: AvailabilityCreate) -> Availability:
        slot = Availability(
            provider_id=provider_id,
            slot_date=data.slot_date,
            start_time=data.start_time,
            end_time=data.end_time,
            status="FREE",
        )
        self.db.add(slot)
        self.db.commit()
        self.db.refresh(slot)
        return slot

    def list_availability_by_provider(self, provider_id: uuid.UUID) -> List[Availability]:
        return (
            self.db.query(Availability)
            .filter(Availability.provider_id == provider_id)
            .order_by(Availability.slot_date.asc(), Availability.start_time.asc())
            .all()
        )

    def get_availability_by_id(self, slot_id: uuid.UUID) -> Optional[Availability]:
        return self.db.query(Availability).filter(Availability.id == slot_id).first()

    def delete_availability_slot(self, slot: Availability) -> None:
        self.db.delete(slot)
        self.db.commit()

    # ==========================================
    # PROVIDER SERVICE OPERATIONS
    # ==========================================

    def create_provider_service(self, provider_id: uuid.UUID, data: ProviderServiceCreate) -> ProviderService:
        entry = ProviderService(
            provider_id=provider_id,
            service_id=data.service_id,
            price=data.price,
            duration_minutes=data.duration_minutes,
            active=data.active,
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_provider_service_by_id(self, entry_id: uuid.UUID) -> Optional[ProviderService]:
        return self.db.query(ProviderService).filter(ProviderService.id == entry_id).first()

    def update_provider_service(self, entry: ProviderService, data: ProviderServiceUpdate) -> ProviderService:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(entry, field, value)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def list_provider_services(self, provider_id: uuid.UUID) -> List[ProviderService]:
        return (
            self.db.query(ProviderService)
            .filter(ProviderService.provider_id == provider_id)
            .order_by(ProviderService.created_at.desc())
            .all()
        )
