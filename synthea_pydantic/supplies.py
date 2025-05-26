"""Pydantic models for Synthea supplies CSV format."""

from datetime import date as Date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Supply(BaseModel):
    """Model representing a single supply record from Synthea CSV output."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,  # Accept both field name and alias
    )
    
    date: Date = Field(alias='DATE', description="The date the supplies were used")
    patient: UUID = Field(alias='PATIENT', description="Foreign key to the Patient")
    encounter: UUID = Field(alias='ENCOUNTER', description="Foreign key to the Encounter when the supplies were used")
    code: str = Field(alias='CODE', description="Code for the type of supply used, from SNOMED-CT")
    description: str = Field(alias='DESCRIPTION', description="Description of supply used")
    quantity: int = Field(alias='QUANTITY', description="Quantity of supply used")
    
    @model_validator(mode='before')
    @classmethod
    def preprocess_csv(cls, data):
        """Convert empty strings to None for proper optional field handling."""
        if isinstance(data, dict):
            return {k: v if v != '' else None for k, v in data.items()}
        return data