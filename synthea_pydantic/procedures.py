"""Pydantic models for Synthea procedures CSV format."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Procedure(BaseModel):
    """Model representing a single procedure record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    start: datetime = Field(description="The date and time the procedure was performed")
    stop: Optional[datetime] = Field(None, description="The date and time the procedure was completed, if applicable")
    patient: UUID = Field(description="Foreign key to the Patient")
    encounter: UUID = Field(description="Foreign key to the Encounter where the procedure was performed")
    system: str = Field(description="Terminology system for the Code, typically SNOMED-CT")
    code: str = Field(description="Procedure code from SNOMED-CT")
    description: str = Field(description="Description of the procedure")
    base_cost: Decimal = Field(description="The line item cost of the procedure")
    reasoncode: Optional[str] = Field(None, description="Diagnosis code from SNOMED-CT specifying why this procedure was performed")
    reasondescription: Optional[str] = Field(None, description="Description of the reason code")