"""Pydantic models for Synthea supplies CSV format."""

from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Supply(BaseModel):
    """Model representing a single supply record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    date: date = Field(description="The date the supply was used")
    patient: UUID = Field(description="Foreign key to the Patient")
    encounter: UUID = Field(description="Foreign key to the Encounter when the supply was used")
    code: str = Field(description="Supply code from SNOMED-CT")
    description: str = Field(description="Description of the supply")
    quantity: int = Field(description="Quantity of supply used")