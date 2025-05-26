"""Pydantic models for Synthea immunizations CSV format."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Immunization(BaseModel):
    """Model representing a single immunization record from Synthea CSV output."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,  # Accept both field name and alias
    )
    
    date: datetime = Field(alias='DATE', description="The date the immunization was administered")
    patient: UUID = Field(alias='PATIENT', description="Foreign key to the Patient")
    encounter: UUID = Field(alias='ENCOUNTER', description="Foreign key to the Encounter where the immunization was administered")
    code: str = Field(alias='CODE', description="Immunization code from CVX")
    description: str = Field(alias='DESCRIPTION', description="Description of the immunization")
    base_cost: Decimal = Field(alias='BASE_COST', description="The line item cost of the immunization")
    
    @model_validator(mode='before')
    @classmethod
    def preprocess_csv(cls, data):
        """Convert empty strings to None for proper optional field handling."""
        if isinstance(data, dict):
            return {k: v if v != '' else None for k, v in data.items()}
        return data