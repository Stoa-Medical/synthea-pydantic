"""Pydantic models for Synthea providers CSV format."""

from decimal import Decimal
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Provider(BaseModel):
    """Model representing a single provider record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Primary Key")
    organization: UUID = Field(description="Foreign key to the Organization that employs this provider")
    name: str = Field(description="First and last name of the provider")
    gender: Literal["M", "F"] = Field(description="Gender of the provider")
    speciality: str = Field(description="Provider specialty, such as Pediatrics")
    address: str = Field(description="Provider's street address without commas or newlines")
    city: str = Field(description="Street address city")
    state: str = Field(description="Street address state abbreviation")
    zip: str = Field(description="Street address zip or postal code")
    lat: float = Field(description="Latitude of the provider")
    lon: float = Field(description="Longitude of the provider")
    encounters: int = Field(description="Number of encounters performed by the provider")
    procedures: int = Field(description="Number of procedures performed by the provider")