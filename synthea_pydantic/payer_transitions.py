"""Pydantic models for Synthea payer_transitions CSV format."""

from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PayerTransition(BaseModel):
    """Model representing a single payer transition record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    patient: UUID = Field(description="Foreign key to the Patient")
    memberid: Optional[UUID] = Field(None, description="Member ID for the Insurance Plan")
    start_year: int = Field(description="The year the coverage started (inclusive)")
    end_year: int = Field(description="The year the coverage ended (inclusive)")
    payer: UUID = Field(description="Foreign key to the Payer")
    secondary_payer: Optional[UUID] = Field(None, description="Foreign key to the Secondary Payer")
    ownership: Optional[Literal["Guardian", "Self", "Spouse"]] = Field(None, description="The owner of the insurance policy. Legal values: Guardian, Self, Spouse")
    owner_name: Optional[str] = Field(None, description="The name of the insurance policy owner")