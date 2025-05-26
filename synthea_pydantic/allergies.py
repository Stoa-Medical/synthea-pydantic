"""Pydantic models for Synthea allergies CSV format."""

from datetime import date
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Allergy(BaseModel):
    """Model representing a single allergy record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    start: date = Field(description="The date the allergy was diagnosed")
    stop: Optional[date] = Field(None, description="The date the allergy ended, if applicable")
    patient: UUID = Field(description="Foreign key to the Patient")
    encounter: UUID = Field(description="Foreign key to the Encounter when the allergy was diagnosed")
    code: str = Field(description="Allergy code")
    system: str = Field(description="Terminology system of the Allergy code. RxNorm if this is a medication allergy, otherwise SNOMED-CT")
    description: str = Field(description="Description of the Allergy")
    type: Optional[Literal["allergy", "intolerance"]] = Field(None, description="Identify entry as an allergy or intolerance")
    category: Optional[Literal["drug", "medication", "food", "environment"]] = Field(None, description="Identify the category")
    reaction1: Optional[str] = Field(None, description="Optional SNOMED code of the patients reaction")
    description1: Optional[str] = Field(None, description="Optional description of the Reaction1 SNOMED code")
    severity1: Optional[Literal["MILD", "MODERATE", "SEVERE"]] = Field(None, description="Severity of the reaction")
    reaction2: Optional[str] = Field(None, description="Optional SNOMED code of the patients second reaction")
    description2: Optional[str] = Field(None, description="Optional description of the Reaction2 SNOMED code")
    severity2: Optional[Literal["MILD", "MODERATE", "SEVERE"]] = Field(None, description="Severity of the second reaction")