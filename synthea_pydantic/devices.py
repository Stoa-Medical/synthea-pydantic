"""Pydantic models for Synthea devices CSV format."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Device(BaseModel):
    """Model representing a single device record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    start: datetime = Field(description="The date and time the device was associated to the patient")
    stop: Optional[datetime] = Field(None, description="The date and time the device was removed, if applicable")
    patient: UUID = Field(description="Foreign key to the Patient")
    encounter: UUID = Field(description="Foreign key to the Encounter when the device was associated")
    code: str = Field(description="Type of device, from SNOMED-CT")
    description: str = Field(description="Description of the device")
    udi: str = Field(description="Unique Device Identifier for the device")