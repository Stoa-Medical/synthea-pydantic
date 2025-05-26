"""Pydantic models for Synthea imaging_studies CSV format."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ImagingStudy(BaseModel):
    """Model representing a single imaging study record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Non-unique identifier of the imaging study. An imaging study may have multiple rows.")
    date: datetime = Field(description="The date and time the imaging study was conducted")
    patient: UUID = Field(description="Foreign key to the Patient")
    encounter: UUID = Field(description="Foreign key to the Encounter")
    series_uid: str = Field(description="Imaging Study series DICOM UID.")
    bodysite_code: str = Field(description="A SNOMED Body Structures code describing what part of the body the images in the series were taken of.")
    bodysite_description: str = Field(description="Description of the body site")
    modality_code: Literal["DX", "MR", "CT", "US", "NM", "PT"] = Field(description="A DICOM-DCM code describing the method used to take the images.")
    modality_description: str = Field(description="Description of the image modality")
    instance_uid: str = Field(description="Imaging Study instance DICOM UID.")
    sop_code: str = Field(description="A DICOM-SOP code describing the Subject-Object Pair (SOP) that constitutes the image.")
    sop_description: str = Field(description="Description of the SOP code")
    procedure_code: str = Field(description="Imaging Procedure code from SNOMED-CT")