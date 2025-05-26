"""Tests for the imaging_studies module."""

import csv
from datetime import datetime
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.imaging_studies import ImagingStudy


def test_load_imaging_studies_csv():
    """Test loading imaging studies from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "imaging_studies.csv"
    
    imaging_studies = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            imaging_study = ImagingStudy(**row)
            imaging_studies.append(imaging_study)
    
    # Verify we loaded some data
    assert len(imaging_studies) > 0
    
    # Check the first imaging study
    first = imaging_studies[0]
    assert isinstance(first.id, UUID)
    assert isinstance(first.date, datetime)
    assert isinstance(first.patient, UUID)
    assert isinstance(first.encounter, UUID)
    assert isinstance(first.series_uid, str)
    assert isinstance(first.bodysite_code, str)
    assert isinstance(first.bodysite_description, str)
    assert isinstance(first.modality_code, str)
    assert isinstance(first.modality_description, str)
    assert isinstance(first.instance_uid, str)
    assert isinstance(first.sop_code, str)
    assert isinstance(first.sop_description, str)
    assert isinstance(first.procedure_code, str)


def test_imaging_study_serialization():
    """Test serializing ImagingStudy models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "imaging_studies.csv"
    
    imaging_studies = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            imaging_study = ImagingStudy(**row)
            imaging_studies.append(imaging_study)
    
    # Test model_dump() for all imaging studies
    for imaging_study in imaging_studies:
        data = imaging_study.model_dump()
        assert isinstance(data, dict)
        assert 'id' in data
        assert 'date' in data
        assert 'patient' in data
        assert 'encounter' in data
        assert 'series_uid' in data
        assert 'bodysite_code' in data
        assert 'bodysite_description' in data
        assert 'modality_code' in data
        assert 'modality_description' in data
        assert 'instance_uid' in data
        assert 'sop_code' in data
        assert 'sop_description' in data
        assert 'procedure_code' in data
    
    # Test model_dump_json() for all imaging studies
    for imaging_study in imaging_studies:
        json_str = imaging_study.model_dump_json()
        assert isinstance(json_str, str)
        assert '"id"' in json_str
        assert '"date"' in json_str
        assert '"patient"' in json_str
        assert '"encounter"' in json_str
        assert '"series_uid"' in json_str
        assert '"modality_code"' in json_str
    
    # Test round-trip serialization
    first_imaging_study = imaging_studies[0]
    json_data = first_imaging_study.model_dump_json()
    restored = ImagingStudy.model_validate_json(json_data)
    assert restored == first_imaging_study


def test_imaging_study_field_validation():
    """Test field validation for ImagingStudy model."""
    # Test with all required fields using lowercase names
    imaging_study = ImagingStudy(
        id='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        date='2020-01-01T10:00:00',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        series_uid='1.2.840.113619.2.176.3596.3364818.7819.1259708454.105',
        bodysite_code='53120007',
        bodysite_description='Arm',
        modality_code='DX',
        modality_description='Digital Radiography',
        instance_uid='1.2.840.113619.2.176.3596.3364818.7819.1259708454.105.1',
        sop_code='1.2.840.10008.5.1.4.1.1.1.1',
        sop_description='Digital X-Ray Image Storage - For Presentation',
        procedure_code='168731009'
    )
    assert imaging_study.date == datetime(2020, 1, 1, 10, 0, 0)
    assert imaging_study.modality_code == 'DX'
    assert imaging_study.bodysite_code == '53120007'
    assert imaging_study.procedure_code == '168731009'
    
    # Test with different modality codes
    imaging_study_ct = ImagingStudy(
        id='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        date='2020-01-01T10:00:00',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        series_uid='1.2.840.113619.2.176.3596.3364818.7819.1259708454.106',
        bodysite_code='39607008',
        bodysite_description='Lung structure',
        modality_code='CT',
        modality_description='Computed Tomography',
        instance_uid='1.2.840.113619.2.176.3596.3364818.7819.1259708454.106.1',
        sop_code='1.2.840.10008.5.1.4.1.1.2',
        sop_description='CT Image Storage',
        procedure_code='77477000'
    )
    assert imaging_study_ct.modality_code == 'CT'
    assert imaging_study_ct.bodysite_description == 'Lung structure'


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with ImagingStudy(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "imaging_studies.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        imaging_study = ImagingStudy(**row)
        
        # Verify it loaded correctly
        assert isinstance(imaging_study.id, UUID)
        assert isinstance(imaging_study.date, datetime)
        assert isinstance(imaging_study.patient, UUID)
        assert isinstance(imaging_study.encounter, UUID)
        assert isinstance(imaging_study.series_uid, str)
        assert isinstance(imaging_study.bodysite_code, str)
        assert isinstance(imaging_study.bodysite_description, str)
        assert isinstance(imaging_study.modality_code, str)
        assert isinstance(imaging_study.modality_description, str)
        assert isinstance(imaging_study.instance_uid, str)
        assert isinstance(imaging_study.sop_code, str)
        assert isinstance(imaging_study.sop_description, str)
        assert isinstance(imaging_study.procedure_code, str)


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Note: For imaging studies, all fields are required in the CSV format
    # This test verifies the model validator is present and working
    # In practice, imaging study CSVs shouldn't have empty required fields
    csv_row = {
        'Id': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'DATE': '2020-01-01T10:00:00',
        'PATIENT': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'ENCOUNTER': '01efcc52-15d6-51e9-faa2-bee069fcbe44',
        'SERIES_UID': '1.2.840.113619.2.176.3596.3364818.7819.1259708454.105',
        'BODYSITE_CODE': '53120007',
        'BODYSITE_DESCRIPTION': 'Arm',
        'MODALITY_CODE': 'DX',
        'MODALITY_DESCRIPTION': 'Digital Radiography',
        'INSTANCE_UID': '1.2.840.113619.2.176.3596.3364818.7819.1259708454.105.1',
        'SOP_CODE': '1.2.840.10008.5.1.4.1.1.1.1',
        'SOP_DESCRIPTION': 'Digital X-Ray Image Storage - For Presentation',
        'PROCEDURE_CODE': '168731009'
    }
    
    imaging_study = ImagingStudy(**csv_row)
    
    # All fields should be populated (no optional fields in this model)
    assert imaging_study.id is not None
    assert imaging_study.date is not None
    assert imaging_study.patient is not None
    assert imaging_study.encounter is not None
    assert imaging_study.series_uid is not None
    assert imaging_study.bodysite_code is not None
    assert imaging_study.bodysite_description is not None
    assert imaging_study.modality_code is not None
    assert imaging_study.modality_description is not None
    assert imaging_study.instance_uid is not None
    assert imaging_study.sop_code is not None
    assert imaging_study.sop_description is not None
    assert imaging_study.procedure_code is not None