"""Pydantic models for Synthea payers CSV format."""

from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Payer(BaseModel):
    """Model representing a single payer record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Primary Key")
    name: str = Field(description="Name of the payer")
    ownership: Optional[str] = Field(None, description="The ownership of the payer. Typically `Government` or `Private`")
    address: Optional[str] = Field(None, description="Payer's street address without commas or newlines")
    city: Optional[str] = Field(None, description="Street address city")
    state_headquartered: Optional[str] = Field(None, description="Street address state abbreviation")
    zip: Optional[str] = Field(None, description="Street address zip or postal code")
    phone: Optional[str] = Field(None, description="Payer's phone number")
    amount_covered: Decimal = Field(description="The monetary amount paid to Organizations during the entire simulation")
    amount_uncovered: Decimal = Field(description="The monetary amount not paid to Organizations during the entire simulation, and covered out of pocket by patients")
    revenue: Decimal = Field(description="The monetary revenue of the Payer during the entire simulation")
    covered_encounters: int = Field(description="Number of encounter costs covered by the Payer")
    uncovered_encounters: int = Field(description="Number of encounter costs not covered by the Payer")
    covered_medications: int = Field(description="Number of medication costs covered by the Payer")
    uncovered_medications: int = Field(description="Number of medication costs not covered by the Payer")
    covered_procedures: int = Field(description="Number of procedure costs covered by the Payer")
    uncovered_procedures: int = Field(description="Number of procedure costs not covered by the Payer")
    covered_immunizations: int = Field(description="Number of immunization costs covered by the Payer")
    uncovered_immunizations: int = Field(description="Number of immunization costs not covered by the Payer")
    unique_customers: int = Field(description="Number of unique patients enrolled with the Payer")
    qols_avg: float = Field(description="Average patient's Quality of Life scores for those enrolled in the Payer during the entire simulation")
    member_months: int = Field(description="The total number of months that patients were enrolled with this Payer during the simulation and paid monthly premiums (if any)")