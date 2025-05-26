"""Pydantic models for Synthea patients CSV format."""

from datetime import date
from decimal import Decimal
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Patient(BaseModel):
    """Model representing a single patient record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Primary Key. Unique Identifier of the patient")
    birthdate: date = Field(description="The date the patient was born")
    deathdate: Optional[date] = Field(None, description="The date the patient died")
    ssn: str = Field(description="Patient Social Security identifier")
    drivers: Optional[str] = Field(None, description="Patient Drivers License identifier")
    passport: Optional[str] = Field(None, description="Patient Passport identifier")
    prefix: Optional[str] = Field(None, description="Name prefix, such as Mr., Mrs., Dr., etc")
    first: str = Field(description="First name of the patient")
    middle: Optional[str] = Field(None, description="Middle name of the patient")
    last: str = Field(description="Last or surname of the patient")
    suffix: Optional[str] = Field(None, description="Name suffix, such as PhD, MD, JD, etc")
    maiden: Optional[str] = Field(None, description="Maiden name of the patient")
    marital: Optional[Literal["M", "S"]] = Field(None, description="Marital Status. M is married, S is single. Currently no support for divorce (D) or widowing (W)")
    race: str = Field(description="Description of the patient's primary race")
    ethnicity: str = Field(description="Description of the patient's primary ethnicity")
    gender: Literal["M", "F"] = Field(description="Gender. M is male, F is female")
    birthplace: str = Field(description="Name of the town where the patient was born")
    address: str = Field(description="Patient's street address without commas or newlines")
    city: str = Field(description="Patient's address city")
    state: str = Field(description="Patient's address state")
    county: Optional[str] = Field(None, description="Patient's address county")
    fips: Optional[str] = Field(None, description="Patient's FIPS county code")
    zip: Optional[str] = Field(None, description="Patient's zip code")
    lat: Optional[Decimal] = Field(None, description="Latitude of Patient's address")
    lon: Optional[Decimal] = Field(None, description="Longitude of Patient's address")
    healthcare_expenses: Decimal = Field(description="The total lifetime cost of healthcare to the patient (i.e. what the patient paid)")
    healthcare_coverage: Decimal = Field(description="The total lifetime cost of healthcare services that were covered by Payers (i.e. what the insurance company paid)")
    income: Decimal = Field(description="Annual income for the Patient")