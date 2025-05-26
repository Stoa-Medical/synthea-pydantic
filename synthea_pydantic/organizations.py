"""Pydantic models for Synthea organizations CSV format."""

from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Organization(BaseModel):
    """Model representing a single organization record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Primary key of the Organization")
    name: str = Field(description="Name of the Organization")
    address: str = Field(description="Organization's street address without commas or newlines")
    city: str = Field(description="Street address city")
    state: Optional[str] = Field(None, description="Street address state abbreviation")
    zip: Optional[str] = Field(None, description="Street address zip or postal code")
    lat: Optional[float] = Field(None, description="Latitude of Organization's address")
    lon: Optional[float] = Field(None, description="Longitude of Organization's address")
    phone: Optional[str] = Field(None, description="Organization's phone number. Sometimes multiple numbers")
    revenue: Decimal = Field(description="The monetary revenue of the organization during the entire simulation")
    utilization: int = Field(description="The number of Encounters performed by this Organization")