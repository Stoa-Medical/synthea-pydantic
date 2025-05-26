"""Pydantic models for Synthea supplies CSV format."""

from datetime import date as Date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Supply(BaseModel):
    """Model representing a single supply record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    date: Date = Field(description="The date the supplies were used")
    patient: UUID = Field(description="Foreign key to the Patient")
    encounter: UUID = Field(description="Foreign key to the Encounter when the supplies were used")
    code: str = Field(description="Code for the type of supply used, from SNOMED-CT")
    description: str = Field(description="Description of supply used")
    quantity: int = Field(description="Quantity of supply used")