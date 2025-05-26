"""Pydantic models for Synthea encounters CSV format."""

from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Encounter(BaseModel):
    """Model representing a single encounter record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Primary Key. Unique Identifier of the encounter")
    start: datetime = Field(description="The date and time the encounter started")
    stop: Optional[datetime] = Field(None, description="The date and time the encounter concluded")
    patient: UUID = Field(description="Foreign key to the Patient")
    organization: UUID = Field(description="Foreign key to the Organization")
    provider: UUID = Field(description="Foreign key to the Provider")
    payer: UUID = Field(description="Foreign key to the Payer")
    encounterclass: Literal["ambulatory", "emergency", "inpatient", "outpatient", "urgentcare", "wellness"] = Field(description="The class of the encounter, such as `ambulatory`, `emergency`, `inpatient`, `outpatient`, `urgentcare`, or `wellness`")
    code: str = Field(description="Encounter code from SNOMED-CT")
    description: str = Field(description="Description of the encounter")
    base_encounter_cost: Decimal = Field(description="The base cost of the encounter, not including any line item costs related to medications, immunizations, procedures, or other services")
    total_claim_cost: Decimal = Field(description="The total cost of the encounter, including all line items")
    payer_coverage: Decimal = Field(description="The amount of cost covered by the Payer")
    reasoncode: Optional[str] = Field(None, description="Diagnosis code from SNOMED-CT, only if this encounter targeted a specific condition")
    reasondescription: Optional[str] = Field(None, description="Description of the reason code")