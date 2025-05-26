"""Pydantic models for Synthea careplans CSV format."""

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CarePlan(BaseModel):
    """Model representing a single care plan record from Synthea CSV output."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,  # Accept both field name and alias
    )
    
    id: UUID = Field(alias='Id', description="Primary Key. Unique Identifier of the care plan")
    start: date = Field(alias='START', description="The date the care plan was initiated")
    stop: Optional[date] = Field(None, alias='STOP', description="The date the care plan ended, if applicable")
    patient: UUID = Field(alias='PATIENT', description="Foreign key to the Patient")
    encounter: UUID = Field(alias='ENCOUNTER', description="Foreign key to the Encounter when the care plan was initiated")
    code: str = Field(alias='CODE', description="Code from SNOMED-CT")
    description: str = Field(alias='DESCRIPTION', description="Description of the care plan")
    reasoncode: Optional[str] = Field(None, alias='REASONCODE', description="Diagnosis code from SNOMED-CT that this care plan addresses")
    reasondescription: Optional[str] = Field(None, alias='REASONDESCRIPTION', description="Description of the reason code")
    
    @model_validator(mode='before')
    @classmethod
    def preprocess_csv(cls, data):
        """Convert empty strings to None for proper optional field handling."""
        if isinstance(data, dict):
            return {k: v if v != '' else None for k, v in data.items()}
        return data