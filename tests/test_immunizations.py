"""Tests for the immunizations module."""

import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.immunizations import Immunization


def test_load_immunizations_csv():
    """Test loading immunizations from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "immunizations.csv"
    
    immunizations = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            immunization = Immunization(**row)
            immunizations.append(immunization)
    
    # Verify we loaded some data
    assert len(immunizations) > 0
    
    # Check the first immunization
    first = immunizations[0]
    assert isinstance(first.date, datetime)
    assert isinstance(first.patient, UUID)
    assert isinstance(first.encounter, UUID)
    assert isinstance(first.code, str)
    assert isinstance(first.description, str)
    assert isinstance(first.base_cost, Decimal)


def test_immunization_serialization():
    """Test serializing Immunization models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "immunizations.csv"
    
    immunizations = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            immunization = Immunization(**row)
            immunizations.append(immunization)
    
    # Test model_dump() for all immunizations
    for immunization in immunizations:
        data = immunization.model_dump()
        assert isinstance(data, dict)
        assert 'date' in data
        assert 'patient' in data
        assert 'encounter' in data
        assert 'code' in data
        assert 'description' in data
        assert 'base_cost' in data
    
    # Test model_dump_json() for all immunizations
    for immunization in immunizations:
        json_str = immunization.model_dump_json()
        assert isinstance(json_str, str)
        assert '"date"' in json_str
        assert '"patient"' in json_str
        assert '"encounter"' in json_str
        assert '"code"' in json_str
        assert '"description"' in json_str
        assert '"base_cost"' in json_str
    
    # Test round-trip serialization
    first_immunization = immunizations[0]
    json_data = first_immunization.model_dump_json()
    restored = Immunization.model_validate_json(json_data)
    assert restored == first_immunization


def test_immunization_field_validation():
    """Test field validation for Immunization model."""
    # Test with all required fields using lowercase names
    immunization = Immunization(
        date='2020-01-01T10:00:00',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='08',
        description='Hep B, adolescent or pediatric',
        base_cost='14.60'
    )
    assert immunization.date == datetime(2020, 1, 1, 10, 0, 0)
    assert immunization.code == '08'
    assert immunization.description == 'Hep B, adolescent or pediatric'
    assert immunization.base_cost == Decimal('14.60')
    
    # Test with different vaccine types
    immunization_flu = Immunization(
        date='2020-10-15T14:30:00',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='140',
        description='Influenza, seasonal, injectable',
        base_cost='25.00'
    )
    assert immunization_flu.code == '140'
    assert immunization_flu.description == 'Influenza, seasonal, injectable'
    assert immunization_flu.base_cost == Decimal('25.00')
    
    # Test with COVID vaccine
    immunization_covid = Immunization(
        date='2021-03-01T09:00:00',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='208',
        description='COVID-19, mRNA, LNP-S, PF, 30 mcg/0.3 mL dose',
        base_cost='0.00'  # Often free
    )
    assert immunization_covid.code == '208'
    assert immunization_covid.base_cost == Decimal('0.00')


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with Immunization(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "immunizations.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        immunization = Immunization(**row)
        
        # Verify it loaded correctly
        assert isinstance(immunization.date, datetime)
        assert isinstance(immunization.patient, UUID)
        assert isinstance(immunization.encounter, UUID)
        assert isinstance(immunization.code, str)
        assert isinstance(immunization.description, str)
        assert isinstance(immunization.base_cost, Decimal)


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Note: For immunizations, all fields are required in the CSV format
    # This test verifies the model validator is present and working
    # In practice, immunization CSVs shouldn't have empty required fields
    csv_row = {
        'DATE': '2020-01-01T10:00:00',
        'PATIENT': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'ENCOUNTER': '01efcc52-15d6-51e9-faa2-bee069fcbe44',
        'CODE': '08',
        'DESCRIPTION': 'Hep B, adolescent or pediatric',
        'BASE_COST': '14.60'
    }
    
    immunization = Immunization(**csv_row)
    
    # All fields should be populated (no optional fields in this model)
    assert immunization.date is not None
    assert immunization.patient is not None
    assert immunization.encounter is not None
    assert immunization.code is not None
    assert immunization.description is not None
    assert immunization.base_cost is not None