"""Pydantic models for Synthea payer_transitions CSV format."""

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PayerTransition(BaseModel):
    """Model representing a single payer transition record from Synthea CSV output."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,  # Accept both field name and alias
    )
    
    patient: UUID = Field(alias='PATIENT', description="Foreign key to the Patient")
    memberid: Optional[UUID] = Field(None, alias='MEMBERID', description="Member ID for the Insurance Plan")
    start_year: int = Field(alias='START_YEAR', description="The year the coverage started (inclusive)")
    end_year: int = Field(alias='END_YEAR', description="The year the coverage ended (inclusive)")
    payer: UUID = Field(alias='PAYER', description="Foreign key to the Payer")
    secondary_payer: Optional[UUID] = Field(None, alias='SECONDARY_PAYER', description="Foreign key to the Secondary Payer")
    ownership: Optional[Literal["Guardian", "Self", "Spouse"]] = Field(None, alias='OWNERSHIP', description="The owner of the insurance policy. Legal values: Guardian, Self, Spouse")
    owner_name: Optional[str] = Field(None, alias='OWNERNAME', description="The name of the insurance policy owner")
    
    @field_validator('start_year', 'end_year', mode='before')
    @classmethod
    def parse_year_from_datetime(cls, v):
        """Extract year from datetime string if needed."""
        if isinstance(v, str) and 'T' in v:
            # Parse datetime string and extract year
            dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
            return dt.year
        return v
    
    @field_validator('ownership', mode='before')
    @classmethod
    def strip_ownership(cls, v):
        """Strip whitespace from ownership field before validation."""
        if isinstance(v, str):
            return v.strip()
        return v
    
    @model_validator(mode='before')
    @classmethod
    def preprocess_csv(cls, data):
        """Convert empty strings to None for proper optional field handling."""
        if isinstance(data, dict):
            return {k: v if v != '' else None for k, v in data.items()}
        return data