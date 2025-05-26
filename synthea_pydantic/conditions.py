"""Pydantic models for Synthea conditions CSV format."""

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Condition(BaseModel):
    """Model representing a single condition record from Synthea CSV output."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,  # Accept both field name and alias
    )
    
    start: date = Field(alias='START', description="The date the condition was diagnosed")
    stop: Optional[date] = Field(None, alias='STOP', description="The date the condition resolved, if applicable")
    patient: UUID = Field(alias='PATIENT', description="Foreign key to the Patient")
    encounter: UUID = Field(alias='ENCOUNTER', description="Foreign key to the Encounter when the condition was diagnosed")
    code: str = Field(alias='CODE', description="Diagnosis code from SNOMED-CT")
    description: str = Field(alias='DESCRIPTION', description="Description of the condition")
    
    @model_validator(mode='before')
    @classmethod
    def preprocess_csv(cls, data):
        """Convert empty strings to None for proper optional field handling."""
        if isinstance(data, dict):
            return {k: v if v != '' else None for k, v in data.items()}
        return data