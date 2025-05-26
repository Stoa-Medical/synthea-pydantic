"""Pydantic models for Synthea claims CSV format."""

from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Claim(BaseModel):
    """Model representing a single claim record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Primary Key. Unique Identifier of the claim")
    patientid: UUID = Field(description="Foreign key to the Patient")
    providerid: UUID = Field(description="Foreign key to the Provider")
    primarypatientinsuranceid: Optional[UUID] = Field(None, description="Foreign key to the primary Payer")
    secondarypatientinsuranceid: Optional[UUID] = Field(None, description="Foreign key to the second Payer")
    departmentid: int = Field(description="Placeholder for department")
    patientdepartmentid: int = Field(description="Placeholder for patient department")
    diagnosis1: Optional[str] = Field(None, description="SNOMED-CT code corresponding to a diagnosis related to the claim")
    diagnosis2: Optional[str] = Field(None, description="SNOMED-CT code corresponding to a diagnosis related to the claim")
    diagnosis3: Optional[str] = Field(None, description="SNOMED-CT code corresponding to a diagnosis related to the claim")
    diagnosis4: Optional[str] = Field(None, description="SNOMED-CT code corresponding to a diagnosis related to the claim")
    diagnosis5: Optional[str] = Field(None, description="SNOMED-CT code corresponding to a diagnosis related to the claim")
    diagnosis6: Optional[str] = Field(None, description="SNOMED-CT code corresponding to a diagnosis related to the claim")
    diagnosis7: Optional[str] = Field(None, description="SNOMED-CT code corresponding to a diagnosis related to the claim")
    diagnosis8: Optional[str] = Field(None, description="SNOMED-CT code corresponding to a diagnosis related to the claim")
    referringproviderid: Optional[UUID] = Field(None, description="Foreign key to the Provider who made the referral")
    appointmentid: Optional[UUID] = Field(None, description="Foreign key to the Encounter")
    currentillnessdate: datetime = Field(description="The date the patient experienced symptoms")
    servicedate: datetime = Field(description="The date of the services on the claim")
    supervisingproviderid: Optional[UUID] = Field(None, description="Foreign key to the supervising Provider")
    status1: Optional[Literal["BILLED", "CLOSED"]] = Field(None, description="Status of the claim from the Primary Insurance. BILLED or CLOSED")
    status2: Optional[Literal["BILLED", "CLOSED"]] = Field(None, description="Status of the claim from the Secondary Insurance. BILLED or CLOSED")
    statusp: Optional[Literal["BILLED", "CLOSED"]] = Field(None, description="Status of the claim from the Patient. BILLED or CLOSED")
    outstanding1: Optional[Decimal] = Field(None, description="Total amount of money owed by Primary Insurance")
    outstanding2: Optional[Decimal] = Field(None, description="Total amount of money owed by Secondary Insurance")
    outstandingp: Optional[Decimal] = Field(None, description="Total amount of money owed by Patient")
    lastbilleddate1: Optional[datetime] = Field(None, description="Date the claim was sent to Primary Insurance")
    lastbilleddate2: Optional[datetime] = Field(None, description="Date the claim was sent to Secondary Insurance")
    lastbilleddatep: Optional[datetime] = Field(None, description="Date the claim was sent to the Patient")
    healthcareclaimtypeid1: Optional[Literal[1, 2]] = Field(None, description="Type of claim: 1 is professional, 2 is institutional")
    healthcareclaimtypeid2: Optional[Literal[1, 2]] = Field(None, description="Type of claim: 1 is professional, 2 is institutional")