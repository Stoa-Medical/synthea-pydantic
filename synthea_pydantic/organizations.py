"""Pydantic models for Synthea organizations CSV format."""

from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Organization(BaseModel):
    """Model representing a single organization record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Primary Key. Unique Identifier of the organization")
    name: str = Field(description="Name of the organization")
    address: str = Field(description="Organization's street address without commas or newlines")
    city: str = Field(description="Street address city")
    state: str = Field(description="Street address state abbreviation")
    zip: str = Field(description="Street address zip or postal code")
    lat: float = Field(description="Latitude of the organization")
    lon: float = Field(description="Longitude of the organization")
    phone: Optional[str] = Field(None, description="Organization phone number")
    revenue: Decimal = Field(description="Revenue in USD")
    utilization: int = Field(description="Number of encounters performed by this organization")