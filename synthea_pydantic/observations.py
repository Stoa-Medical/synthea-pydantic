"""Pydantic models for Synthea observations CSV format."""

from datetime import datetime
from typing import Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Observation(BaseModel):
    """Model representing a single observation record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    date: datetime = Field(description="The date and time the observation was performed")
    patient: UUID = Field(description="Foreign key to the Patient")
    encounter: UUID = Field(description="Foreign key to the Encounter where the observation was performed")
    category: Optional[str] = Field(None, description="Category of the observation")
    code: str = Field(description="Observation or Lab code from LOINC")
    description: str = Field(description="Description of the observation")
    value: Optional[Union[str, float]] = Field(None, description="The recorded value of the observation. Often numeric, but some values can be verbose, for example, multiple-choice questionnaire responses")
    units: Optional[str] = Field(None, description="The units of measure for the value, if applicable")
    type: Literal["numeric", "text"] = Field(description="The datatype of value: text or numeric")