"""Tests for the supplies module."""

import csv
from datetime import date
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.supplies import Supply


def test_load_supplies_csv():
    """Test loading supplies from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "supplies.csv"
    
    supplies = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            supply = Supply(**row)
            supplies.append(supply)
    
    # Verify we loaded some data
    assert len(supplies) > 0
    
    # Check the first supply
    first = supplies[0]
    assert first.date == date(2021, 2, 8)
    assert first.patient == UUID('8fa5a097-1970-9370-4193-a7baa3d235b5')
    assert first.encounter == UUID('b6358095-06f1-cc6a-ac12-3d46550a254a')
    assert first.code == '409534002'
    assert first.description == 'Disposable air-purifying respirator (physical object)'
    assert first.quantity == 2


def test_supply_serialization():
    """Test serializing Supply models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "supplies.csv"
    
    supplies = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            supply = Supply(**row)
            supplies.append(supply)
    
    # Test model_dump() for all supplies
    for supply in supplies:
        data = supply.model_dump()
        assert isinstance(data, dict)
        assert 'date' in data
        assert 'patient' in data
        assert 'encounter' in data
        assert 'code' in data
        assert 'description' in data
        assert 'quantity' in data
    
    # Test model_dump_json() for all supplies
    for supply in supplies:
        json_str = supply.model_dump_json()
        assert isinstance(json_str, str)
        assert '"date"' in json_str
        assert '"patient"' in json_str
        assert '"encounter"' in json_str
        assert '"quantity"' in json_str
    
    # Test round-trip serialization
    first_supply = supplies[0]
    json_data = first_supply.model_dump_json()
    restored = Supply.model_validate_json(json_data)
    assert restored == first_supply


def test_supply_field_validation():
    """Test field validation for Supply model."""
    # Test with all required fields using lowercase names
    supply = Supply(
        date='2021-01-01',
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='409534002',
        description='Test supply item',
        quantity=5
    )
    assert supply.date == date(2021, 1, 1)
    assert supply.patient == UUID('8fa5a097-1970-9370-4193-a7baa3d235b5')
    assert supply.encounter == UUID('b6358095-06f1-cc6a-ac12-3d46550a254a')
    assert supply.code == '409534002'
    assert supply.description == 'Test supply item'
    assert supply.quantity == 5
    
    # Test with different quantity values
    supply_large_qty = Supply(
        date='2021-01-01',
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='713779008',
        description='Nitrile examination/treatment glove',
        quantity=24
    )
    assert supply_large_qty.quantity == 24


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with Supply(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "supplies.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        supply = Supply(**row)
        
        # Verify it loaded correctly
        assert supply.date == date(2021, 2, 8)
        assert supply.patient == UUID('8fa5a097-1970-9370-4193-a7baa3d235b5')
        assert supply.code == '409534002'
        assert supply.quantity == 2


def test_supply_types_validation():
    """Test that different supply types are handled correctly."""
    csv_path = Path(__file__).parent / "data" / "csv" / "supplies.csv"
    
    supplies = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 10:  # Just test first 10 rows for variety
                break
            supply = Supply(**row)
            supplies.append(supply)
    
    # Verify we have different types of supplies
    codes = {supply.code for supply in supplies}
    descriptions = {supply.description for supply in supplies}
    
    # Should have multiple different supply codes
    assert len(codes) > 1
    assert len(descriptions) > 1
    
    # Check some expected supply types from the data
    expected_codes = {'409534002', '713779008', '469673003', '706724001', '419343004', '470618009'}
    assert any(code in expected_codes for code in codes)


def test_quantity_validation():
    """Test quantity field validation."""
    # Test positive quantities
    supply = Supply(
        date='2021-01-01',
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='409534002',
        description='Test supply',
        quantity=1
    )
    assert supply.quantity == 1
    
    # Test larger quantities
    supply_large = Supply(
        date='2021-01-01',
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='713779008',
        description='Gloves',
        quantity=100
    )
    assert supply_large.quantity == 100


def test_date_parsing():
    """Test that dates are parsed correctly from various formats."""
    # Test ISO format
    supply = Supply(
        date='2021-02-08',
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='409534002',
        description='Test supply',
        quantity=1
    )
    assert supply.date == date(2021, 2, 8)
    
    # Test with date object
    supply_date_obj = Supply(
        date=date(2021, 2, 8),
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='409534002',
        description='Test supply',
        quantity=1
    )
    assert supply_date_obj.date == date(2021, 2, 8)


def test_uuid_validation():
    """Test UUID field validation."""
    # Test with string UUIDs
    supply = Supply(
        date='2021-01-01',
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='409534002',
        description='Test supply',
        quantity=1
    )
    assert isinstance(supply.patient, UUID)
    assert isinstance(supply.encounter, UUID)
    
    # Test with UUID objects
    patient_uuid = UUID('8fa5a097-1970-9370-4193-a7baa3d235b5')
    encounter_uuid = UUID('b6358095-06f1-cc6a-ac12-3d46550a254a')
    
    supply_uuid_obj = Supply(
        date='2021-01-01',
        patient=patient_uuid,
        encounter=encounter_uuid,
        code='409534002',
        description='Test supply',
        quantity=1
    )
    assert supply_uuid_obj.patient == patient_uuid
    assert supply_uuid_obj.encounter == encounter_uuid


def test_string_field_validation():
    """Test string field validation and whitespace handling."""
    # Test with extra whitespace
    supply = Supply(
        date='2021-01-01',
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='  409534002  ',  # Extra whitespace
        description='  Test supply with spaces  ',  # Extra whitespace
        quantity=1
    )
    # Whitespace should be stripped due to str_strip_whitespace=True
    assert supply.code == '409534002'
    assert supply.description == 'Test supply with spaces'


def test_supply_model_config():
    """Test that the model configuration is working correctly."""
    # Test that str_strip_whitespace is working
    supply = Supply(
        date='2021-01-01',
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='   123456   ',
        description='   Test description   ',
        quantity=1
    )
    
    assert supply.code == '123456'
    assert supply.description == 'Test description'


def test_supply_equality():
    """Test Supply model equality comparison."""
    supply1 = Supply(
        date='2021-01-01',
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='409534002',
        description='Test supply',
        quantity=1
    )
    
    supply2 = Supply(
        date='2021-01-01',
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='409534002',
        description='Test supply',
        quantity=1
    )
    
    supply3 = Supply(
        date='2021-01-01',
        patient='8fa5a097-1970-9370-4193-a7baa3d235b5',
        encounter='b6358095-06f1-cc6a-ac12-3d46550a254a',
        code='409534002',
        description='Test supply',
        quantity=2  # Different quantity
    )
    
    assert supply1 == supply2
    assert supply1 != supply3 