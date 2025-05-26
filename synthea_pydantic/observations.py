"""Pydantic models for Synthea observations CSV format."""

from datetime import datetime
from typing import Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Observation(BaseModel):
    """Model representing a single observation record from Synthea CSV output."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,  # Accept both field name and alias
    )
    
    date: datetime = Field(alias='DATE', description="The date and time the observation was performed")
    patient: UUID = Field(alias='PATIENT', description="Foreign key to the Patient")
    encounter: Optional[UUID] = Field(None, alias='ENCOUNTER', description="Foreign key to the Encounter where the observation was performed")
    category: Optional[str] = Field(None, alias='CATEGORY', description="Category of the observation")
    code: str = Field(alias='CODE', description="Observation or Lab code from LOINC")
    description: str = Field(alias='DESCRIPTION', description="Description of the observation")
    value: Optional[Union[str, float]] = Field(None, alias='VALUE', description="The recorded value of the observation. Often numeric, but some values can be verbose, for example, multiple-choice questionnaire responses")
    units: Optional[str] = Field(None, alias='UNITS', description="The units of measure for the value, if applicable")
    type: str = Field(alias='TYPE', description="The datatype of value: text or numeric")
    
    @model_validator(mode='before')
    @classmethod
    def preprocess_csv(cls, data):
        """Convert empty strings to None for proper optional field handling."""
        if isinstance(data, dict):
            processed = {}
            for k, v in data.items():
                # Convert empty strings to None
                if v == '':
                    processed[k] = None
                # Try to convert numeric values in VALUE field when TYPE is numeric
                elif k == 'VALUE' and data.get('TYPE') == 'numeric' and v:
                    try:
                        processed[k] = float(v)
                    except ValueError:
                        processed[k] = v
                else:
                    processed[k] = v
            return processed
        return data