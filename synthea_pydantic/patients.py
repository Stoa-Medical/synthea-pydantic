"""Pydantic models for Synthea patients CSV format."""

from datetime import date
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Patient(BaseModel):
    """Model representing a single patient record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Primary Key. Unique Identifier of the patient")
    birthdate: date = Field(description="The date the patient was born")
    deathdate: Optional[date] = Field(None, description="The date the patient died")
    ssn: str = Field(description="Patient Social Security Number")
    drivers: Optional[str] = Field(None, description="Patient Drivers License Identifier")
    passport: Optional[str] = Field(None, description="Patient Passport Identifier")
    prefix: Optional[str] = Field(None, description="Name prefix, such as Mr., Mrs., Dr., etc.")
    first: str = Field(description="First name of the patient")
    last: str = Field(description="Last or surname of the patient")
    suffix: Optional[str] = Field(None, description="Name suffix, such as PhD, MD, JD, etc.")
    maiden: Optional[str] = Field(None, description="Maiden name of the patient")
    marital: Optional[Literal["M", "S", "D", "W"]] = Field(None, description="Marital Status. M = Married, S = Single, D = Divorced, W = Widowed")
    race: Literal["white", "black", "asian", "native", "other"] = Field(description="Description of patient's race")
    ethnicity: Literal["hispanic", "nonhispanic"] = Field(description="Description of patient's ethnicity")
    gender: Literal["M", "F"] = Field(description="Gender. M = Male, F = Female")
    birthplace: str = Field(description="Name of the town where the patient was born")
    address: str = Field(description="Patient's street address without commas or newlines")
    city: str = Field(description="Patient's address city")
    state: str = Field(description="Patient's address state abbreviation")
    county: Optional[str] = Field(None, description="Patient's address county")
    fips: Optional[str] = Field(None, description="Patient's FIPS code")
    zip: str = Field(description="Patient's zip code")
    lat: float = Field(description="Latitude of Patient's address")
    lon: float = Field(description="Longitude of Patient's address")
    healthcare_expenses: float = Field(description="The total lifetime cost of healthcare to the patient (i.e. what the patient paid)")
    healthcare_coverage: float = Field(description="The total lifetime cost of healthcare services that were covered by Payers (i.e. what the insurance company paid)")
    income: int = Field(description="Annual income for the Patient")