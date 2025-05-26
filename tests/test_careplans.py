"""Tests for the careplans module."""

import csv
from datetime import date
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.careplans import CarePlan


def test_load_careplans_csv():
    """Test loading careplans from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "careplans.csv"
    
    careplans = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            careplan = CarePlan(**row)
            careplans.append(careplan)
    
    # Verify we loaded some data
    assert len(careplans) > 0
    
    # Check the first careplan
    first = careplans[0]
    assert isinstance(first.id, UUID)
    assert isinstance(first.start, date)
    assert first.stop is None or isinstance(first.stop, date)
    assert isinstance(first.patient, UUID)
    assert isinstance(first.encounter, UUID)
    assert isinstance(first.code, str)
    assert isinstance(first.description, str)
    assert first.reasoncode is None or isinstance(first.reasoncode, str)
    assert first.reasondescription is None or isinstance(first.reasondescription, str)


def test_careplan_serialization():
    """Test serializing CarePlan models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "careplans.csv"
    
    careplans = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            careplan = CarePlan(**row)
            careplans.append(careplan)
    
    # Test model_dump() for all careplans
    for careplan in careplans:
        data = careplan.model_dump()
        assert isinstance(data, dict)
        assert 'id' in data
        assert 'start' in data
        assert 'patient' in data
        assert 'encounter' in data
        assert 'code' in data
        assert 'description' in data
    
    # Test model_dump_json() for all careplans
    for careplan in careplans:
        json_str = careplan.model_dump_json()
        assert isinstance(json_str, str)
        assert '"id"' in json_str
        assert '"start"' in json_str
        assert '"patient"' in json_str
        assert '"encounter"' in json_str
    
    # Test round-trip serialization
    first_careplan = careplans[0]
    json_data = first_careplan.model_dump_json()
    restored = CarePlan.model_validate_json(json_data)
    assert restored == first_careplan


def test_careplan_field_validation():
    """Test field validation for CarePlan model."""
    # Test with minimal required fields using lowercase names
    careplan = CarePlan(
        id='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        start='2020-01-01',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='385669000',
        description='Routine antenatal care'
    )
    assert careplan.start == date(2020, 1, 1)
    assert careplan.stop is None
    assert careplan.reasoncode is None
    assert careplan.reasondescription is None
    
    # Test with all fields
    careplan_full = CarePlan(
        id='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        start='2020-01-01',
        stop='2021-01-01',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='385669000',
        description='Routine antenatal care',
        reasoncode='72892002',
        reasondescription='Normal pregnancy'
    )
    assert careplan_full.stop == date(2021, 1, 1)
    assert careplan_full.reasoncode == '72892002'
    assert careplan_full.reasondescription == 'Normal pregnancy'


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with CarePlan(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "careplans.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        careplan = CarePlan(**row)
        
        # Verify it loaded correctly
        assert isinstance(careplan.id, UUID)
        assert isinstance(careplan.start, date)
        assert isinstance(careplan.patient, UUID)
        assert isinstance(careplan.encounter, UUID)
        assert isinstance(careplan.code, str)
        assert isinstance(careplan.description, str)


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Simulate a CSV row with empty strings
    csv_row = {
        'Id': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'START': '2020-01-01',
        'STOP': '',  # Empty string should become None
        'PATIENT': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'ENCOUNTER': '01efcc52-15d6-51e9-faa2-bee069fcbe44',
        'CODE': '385669000',
        'DESCRIPTION': 'Routine antenatal care',
        'REASONCODE': '',  # Empty string should become None
        'REASONDESCRIPTION': '',  # Empty string should become None
    }
    
    careplan = CarePlan(**csv_row)
    
    assert careplan.stop is None
    assert careplan.reasoncode is None
    assert careplan.reasondescription is None