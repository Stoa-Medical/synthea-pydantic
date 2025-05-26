"""Pydantic models for Synthea devices CSV format."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Device(BaseModel):
    """Model representing a single device record from Synthea CSV output."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,  # Accept both field name and alias
    )
    
    start: datetime = Field(alias='START', description="The date and time the device was associated to the patient")
    stop: Optional[datetime] = Field(None, alias='STOP', description="The date and time the device was removed, if applicable")
    patient: UUID = Field(alias='PATIENT', description="Foreign key to the Patient")
    encounter: UUID = Field(alias='ENCOUNTER', description="Foreign key to the Encounter when the device was associated")
    code: str = Field(alias='CODE', description="Type of device, from SNOMED-CT")
    description: str = Field(alias='DESCRIPTION', description="Description of the device")
    udi: str = Field(alias='UDI', description="Unique Device Identifier for the device")
    
    @model_validator(mode='before')
    @classmethod
    def preprocess_csv(cls, data):
        """Convert empty strings to None for proper optional field handling."""
        if isinstance(data, dict):
            return {k: v if v != '' else None for k, v in data.items()}
        return data