"""Pydantic models for Synthea medications CSV format."""

from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Medication(BaseModel):
    """Model representing a single medication record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    start: datetime = Field(description="The date and time the medication was prescribed")
    stop: Optional[datetime] = Field(None, description="The date and time the medication was stopped, if applicable")
    patient: UUID = Field(description="Foreign key to the Patient")
    payer: UUID = Field(description="Foreign key to the Payer")
    encounter: UUID = Field(description="Foreign key to the Encounter where the medication was prescribed")
    code: str = Field(description="Medication code from RxNorm")
    description: str = Field(description="Description of the medication")
    base_cost: Decimal = Field(description="The line item cost of the medication")
    payer_coverage: Decimal = Field(description="The amount covered or reimbursed by the Payer")
    dispenses: int = Field(description="The number of times the prescription was filled")
    totalcost: Decimal = Field(description="The total cost of the prescription, including all dispenses")
    reasoncode: Optional[str] = Field(None, description="The SNOMED-CT code specifying the reason the medication was prescribed, if applicable")
    reasondescription: Optional[str] = Field(None, description="Description of the reason code")