"""Pydantic models for Synthea conditions CSV format."""

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Condition(BaseModel):
    """Model representing a single condition record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    start: date = Field(description="The date the condition was diagnosed")
    stop: Optional[date] = Field(None, description="The date the condition resolved, if applicable")
    patient: UUID = Field(description="Foreign key to the Patient")
    encounter: UUID = Field(description="Foreign key to the Encounter when the condition was diagnosed")
    system: str = Field(description="Specifies the code system, typically SNOMED")
    code: str = Field(description="Diagnosis code from SNOMED-CT")
    description: str = Field(description="Description of the condition")