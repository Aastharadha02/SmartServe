import uuid
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import AuthUser
from app.repositories.provider_repository import ProviderRepository
from app.models.provider import Provider, Certificate, Availability, ProviderService
from app.schemas.provider import (
    ProviderProfileUpdate,
    CertificateCreate,
    AvailabilityCreate,
    ProviderServiceCreate,
    ProviderServiceUpdate,
)


class ProviderServiceDomain:
    def __init__(self, db: Session):
        self.repo = ProviderRepository(db)

    # ==========================================
    # PROFILE MANAGEMENT
    # ==========================================

    def get_my_profile(self, user: AuthUser) -> Provider:
        return self.repo.get_or_create(user_id=user.id, default_name=user.full_name)

    def update_my_profile(self, user: AuthUser, update_data: ProviderProfileUpdate) -> Provider:
        provider = self.repo.get_or_create(user_id=user.id, default_name=user.full_name)
        return self.repo.update_profile(provider, update_data)

    def get_provider_profile(self, provider_id: uuid.UUID) -> Provider:
        provider = self.repo.get_by_user_id(provider_id)
        if not provider:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Provider with ID '{provider_id}' not found",
            )
        return provider

    # ==========================================
    # CERTIFICATES & VERIFICATION
    # ==========================================

    def upload_certificate(self, user: AuthUser, data: CertificateCreate) -> Certificate:
        self.repo.get_or_create(user_id=user.id, default_name=user.full_name)
        return self.repo.create_certificate(provider_id=user.id, data=data)

    def get_my_certificates(self, user: AuthUser) -> List[Certificate]:
        return self.repo.list_certificates_by_provider(provider_id=user.id)

    # ==========================================
    # AVAILABILITY SCHEDULE
    # ==========================================

    def add_availability_slot(self, user: AuthUser, data: AvailabilityCreate) -> Availability:
        # Validate time ordering
        if data.start_time >= data.end_time:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Slot start_time must be strictly before end_time",
            )

        self.repo.get_or_create(user_id=user.id, default_name=user.full_name)
        return self.repo.create_availability_slot(provider_id=user.id, data=data)

    def list_availability(self, provider_id: uuid.UUID) -> List[Availability]:
        return self.repo.list_availability_by_provider(provider_id=provider_id)

    def delete_availability_slot(self, user: AuthUser, slot_id: uuid.UUID) -> None:
        slot = self.repo.get_availability_by_id(slot_id)
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Availability slot not found",
            )

        # Resource ownership check
        if slot.provider_id != user.id and user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You cannot delete another provider's availability slot",
            )

        self.repo.delete_availability_slot(slot)

    # ==========================================
    # CUSTOMIZED SERVICES
    # ==========================================

    def add_provider_service(self, user: AuthUser, data: ProviderServiceCreate) -> ProviderService:
        self.repo.get_or_create(user_id=user.id, default_name=user.full_name)
        return self.repo.create_provider_service(provider_id=user.id, data=data)

    def update_provider_service(
        self, user: AuthUser, entry_id: uuid.UUID, data: ProviderServiceUpdate
    ) -> ProviderService:
        entry = self.repo.get_provider_service_by_id(entry_id)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Provider service offering not found",
            )

        if entry.provider_id != user.id and user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You cannot modify another provider's service offering",
            )

        return self.repo.update_provider_service(entry, data)

    def list_provider_services(self, provider_id: uuid.UUID) -> List[ProviderService]:
        return self.repo.list_provider_services(provider_id=provider_id)
