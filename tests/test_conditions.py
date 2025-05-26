"""Tests for the conditions module."""

import csv
from datetime import date
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.conditions import Condition


def test_load_conditions_csv():
    """Test loading conditions from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "conditions.csv"
    
    conditions = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            condition = Condition(**row)
            conditions.append(condition)
    
    # Verify we loaded some data
    assert len(conditions) > 0
    
    # Check the first condition
    first = conditions[0]
    assert isinstance(first.start, date)
    assert first.stop is None or isinstance(first.stop, date)
    assert isinstance(first.patient, UUID)
    assert isinstance(first.encounter, UUID)
    assert isinstance(first.code, str)
    assert isinstance(first.description, str)


def test_condition_serialization():
    """Test serializing Condition models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "conditions.csv"
    
    conditions = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            condition = Condition(**row)
            conditions.append(condition)
    
    # Test model_dump() for all conditions
    for condition in conditions:
        data = condition.model_dump()
        assert isinstance(data, dict)
        assert 'start' in data
        assert 'patient' in data
        assert 'encounter' in data
        assert 'code' in data
        assert 'description' in data
    
    # Test model_dump_json() for all conditions
    for condition in conditions:
        json_str = condition.model_dump_json()
        assert isinstance(json_str, str)
        assert '"start"' in json_str
        assert '"patient"' in json_str
        assert '"encounter"' in json_str
        assert '"code"' in json_str
    
    # Test round-trip serialization
    first_condition = conditions[0]
    json_data = first_condition.model_dump_json()
    restored = Condition.model_validate_json(json_data)
    assert restored == first_condition


def test_condition_field_validation():
    """Test field validation for Condition model."""
    # Test with minimal required fields using lowercase names
    condition = Condition(
        start='2020-01-01',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='368009',
        description='Heart valve disorder'
    )
    assert condition.start == date(2020, 1, 1)
    assert condition.stop is None
    
    # Test with all fields
    condition_full = Condition(
        start='2020-01-01',
        stop='2021-01-01',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='368009',
        description='Heart valve disorder'
    )
    assert condition_full.stop == date(2021, 1, 1)


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with Condition(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "conditions.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        condition = Condition(**row)
        
        # Verify it loaded correctly
        assert isinstance(condition.start, date)
        assert isinstance(condition.patient, UUID)
        assert isinstance(condition.encounter, UUID)
        assert isinstance(condition.code, str)
        assert isinstance(condition.description, str)


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Simulate a CSV row with empty strings
    csv_row = {
        'START': '2020-01-01',
        'STOP': '',  # Empty string should become None
        'PATIENT': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'ENCOUNTER': '01efcc52-15d6-51e9-faa2-bee069fcbe44',
        'CODE': '368009',
        'DESCRIPTION': 'Heart valve disorder',
    }
    
    condition = Condition(**csv_row)
    
    assert condition.stop is None