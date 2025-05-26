"""Pydantic models for Synthea careplans CSV format."""

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CarePlan(BaseModel):
    """Model representing a single care plan record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Primary Key. Unique Identifier of the care plan")
    start: date = Field(description="The date the care plan was initiated")
    stop: Optional[date] = Field(None, description="The date the care plan ended, if applicable")
    patient: UUID = Field(description="Foreign key to the Patient")
    encounter: UUID = Field(description="Foreign key to the Encounter when the care plan was initiated")
    code: str = Field(description="Code from SNOMED-CT")
    description: str = Field(description="Description of the care plan")
    reasoncode: Optional[str] = Field(None, description="Diagnosis code from SNOMED-CT that this care plan addresses")
    reasondescription: Optional[str] = Field(None, description="Description of the reason code")