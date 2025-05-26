"""Pydantic models for Synthea immunizations CSV format."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Immunization(BaseModel):
    """Model representing a single immunization record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    date: datetime = Field(description="The date the immunization was administered")
    patient: UUID = Field(description="Foreign key to the Patient")
    encounter: UUID = Field(description="Foreign key to the Encounter where the immunization was administered")
    code: str = Field(description="Immunization code from CVX")
    description: str = Field(description="Description of the immunization")
    cost: Decimal = Field(description="The line item cost of the immunization")