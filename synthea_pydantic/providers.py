"""Pydantic models for Synthea providers CSV format."""

from decimal import Decimal
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Provider(BaseModel):
    """Model representing a single provider record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Primary key of the Provider/Clinician")
    organization: UUID = Field(description="Foreign key to the Organization that employees this provider")
    name: str = Field(description="First and last name of the Provider")
    gender: Literal["M", "F"] = Field(description="Gender. M is male, F is female")
    speciality: str = Field(description="Provider speciality")
    address: str = Field(description="Provider's street address without commas or newlines")
    city: str = Field(description="Street address city")
    state: Optional[str] = Field(None, description="Street address state abbreviation")
    zip: Optional[str] = Field(None, description="Street address zip or postal code")
    lat: Optional[float] = Field(None, description="Latitude of Provider's address")
    lon: Optional[float] = Field(None, description="Longitude of Provider's address")
    encounters: int = Field(description="The number of Encounters performed by this provider")
    procedures: int = Field(description="The number of Procedures performed by this provider")