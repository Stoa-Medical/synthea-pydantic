"""Tests for the medications module."""

import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.medications import Medication


def test_load_medications_csv():
    """Test loading medications from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "medications.csv"
    
    medications = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            medication = Medication(**row)
            medications.append(medication)
    
    # Verify we loaded some data
    assert len(medications) > 0
    
    # Check the first medication
    first = medications[0]
    assert isinstance(first.start, datetime)
    assert first.stop is None or isinstance(first.stop, datetime)
    assert isinstance(first.patient, UUID)
    assert isinstance(first.payer, UUID)
    assert isinstance(first.encounter, UUID)
    assert isinstance(first.code, str)
    assert isinstance(first.description, str)
    assert isinstance(first.base_cost, Decimal)
    assert isinstance(first.payer_coverage, Decimal)
    assert isinstance(first.dispenses, int)
    assert isinstance(first.totalcost, Decimal)
    assert first.reasoncode is None or isinstance(first.reasoncode, str)
    assert first.reasondescription is None or isinstance(first.reasondescription, str)


def test_medication_serialization():
    """Test serializing Medication models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "medications.csv"
    
    medications = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            medication = Medication(**row)
            medications.append(medication)
    
    # Test model_dump() for all medications
    for medication in medications:
        data = medication.model_dump()
        assert isinstance(data, dict)
        assert 'start' in data
        assert 'patient' in data
        assert 'payer' in data
        assert 'encounter' in data
        assert 'code' in data
        assert 'description' in data
        assert 'base_cost' in data
        assert 'payer_coverage' in data
        assert 'dispenses' in data
        assert 'totalcost' in data
    
    # Test model_dump_json() for all medications
    for medication in medications:
        json_str = medication.model_dump_json()
        assert isinstance(json_str, str)
        assert '"start"' in json_str
        assert '"patient"' in json_str
        assert '"payer"' in json_str
        assert '"encounter"' in json_str
        assert '"code"' in json_str
        assert '"description"' in json_str
    
    # Test round-trip serialization
    first_medication = medications[0]
    json_data = first_medication.model_dump_json()
    restored = Medication.model_validate_json(json_data)
    assert restored == first_medication


def test_medication_field_validation():
    """Test field validation for Medication model."""
    # Test with minimal required fields using lowercase names
    medication = Medication(
        start='2020-01-01T10:00:00',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        payer='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='849727',
        description='Naproxen sodium 220 MG Oral Tablet',
        base_cost='5.49',
        payer_coverage='4.00',
        dispenses=1,
        totalcost='5.49'
    )
    assert medication.start == datetime(2020, 1, 1, 10, 0, 0)
    assert medication.stop is None
    assert medication.code == '849727'
    assert medication.base_cost == Decimal('5.49')
    assert medication.payer_coverage == Decimal('4.00')
    assert medication.dispenses == 1
    assert medication.totalcost == Decimal('5.49')
    assert medication.reasoncode is None
    assert medication.reasondescription is None
    
    # Test with all fields
    medication_full = Medication(
        start='2020-01-01T10:00:00',
        stop='2020-01-31T10:00:00',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        payer='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='748856',
        description='Amoxicillin 250 MG / Clavulanate 125 MG Oral Tablet',
        base_cost='15.00',
        payer_coverage='12.00',
        dispenses=2,
        totalcost='30.00',
        reasoncode='444814009',
        reasondescription='Viral sinusitis (disorder)'
    )
    assert medication_full.stop == datetime(2020, 1, 31, 10, 0, 0)
    assert medication_full.reasoncode == '444814009'
    assert medication_full.reasondescription == 'Viral sinusitis (disorder)'
    assert medication_full.dispenses == 2
    assert medication_full.totalcost == Decimal('30.00')


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with Medication(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "medications.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        medication = Medication(**row)
        
        # Verify it loaded correctly
        assert isinstance(medication.start, datetime)
        assert isinstance(medication.patient, UUID)
        assert isinstance(medication.payer, UUID)
        assert isinstance(medication.encounter, UUID)
        assert isinstance(medication.code, str)
        assert isinstance(medication.description, str)
        assert isinstance(medication.base_cost, Decimal)
        assert isinstance(medication.payer_coverage, Decimal)
        assert isinstance(medication.dispenses, int)
        assert isinstance(medication.totalcost, Decimal)


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Simulate a CSV row with empty strings
    csv_row = {
        'START': '2020-01-01T10:00:00',
        'STOP': '',  # Empty string should become None
        'PATIENT': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'PAYER': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'ENCOUNTER': '01efcc52-15d6-51e9-faa2-bee069fcbe44',
        'CODE': '849727',
        'DESCRIPTION': 'Naproxen sodium 220 MG Oral Tablet',
        'BASE_COST': '5.49',
        'PAYER_COVERAGE': '4.00',
        'DISPENSES': '1',
        'TOTALCOST': '5.49',
        'REASONCODE': '',  # Empty string should become None
        'REASONDESCRIPTION': '',  # Empty string should become None
    }
    
    medication = Medication(**csv_row)
    
    assert medication.stop is None
    assert medication.reasoncode is None
    assert medication.reasondescription is None