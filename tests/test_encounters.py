"""Tests for the encounters module."""

import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.encounters import Encounter


def test_load_encounters_csv():
    """Test loading encounters from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "encounters.csv"
    
    encounters = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            encounter = Encounter(**row)
            encounters.append(encounter)
    
    # Verify we loaded some data
    assert len(encounters) > 0
    
    # Check the first encounter
    first = encounters[0]
    assert isinstance(first.id, UUID)
    assert isinstance(first.start, datetime)
    assert first.stop is None or isinstance(first.stop, datetime)
    assert isinstance(first.patient, UUID)
    assert isinstance(first.organization, UUID)
    assert isinstance(first.provider, UUID)
    assert isinstance(first.payer, UUID)
    assert first.encounterclass in ["ambulatory", "emergency", "inpatient", "wellness", "urgentcare", "outpatient"]
    assert isinstance(first.code, str)
    assert isinstance(first.description, str)
    assert isinstance(first.base_encounter_cost, Decimal)
    assert isinstance(first.total_claim_cost, Decimal)
    assert isinstance(first.payer_coverage, Decimal)
    assert first.reasoncode is None or isinstance(first.reasoncode, str)
    assert first.reasondescription is None or isinstance(first.reasondescription, str)


def test_encounter_serialization():
    """Test serializing Encounter models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "encounters.csv"
    
    encounters = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            encounter = Encounter(**row)
            encounters.append(encounter)
    
    # Test model_dump() for all encounters
    for encounter in encounters:
        data = encounter.model_dump()
        assert isinstance(data, dict)
        assert 'id' in data
        assert 'start' in data
        assert 'patient' in data
        assert 'organization' in data
        assert 'provider' in data
        assert 'payer' in data
        assert 'encounterclass' in data
        assert 'code' in data
        assert 'description' in data
        assert 'base_encounter_cost' in data
        assert 'total_claim_cost' in data
        assert 'payer_coverage' in data
    
    # Test model_dump_json() for all encounters
    for encounter in encounters:
        json_str = encounter.model_dump_json()
        assert isinstance(json_str, str)
        assert '"id"' in json_str
        assert '"start"' in json_str
        assert '"patient"' in json_str
        assert '"organization"' in json_str
        assert '"provider"' in json_str
        assert '"encounterclass"' in json_str
    
    # Test round-trip serialization
    first_encounter = encounters[0]
    json_data = first_encounter.model_dump_json()
    restored = Encounter.model_validate_json(json_data)
    assert restored == first_encounter


def test_encounter_field_validation():
    """Test field validation for Encounter model."""
    # Test with minimal required fields using lowercase names
    encounter = Encounter(
        id='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        start='2020-01-01T10:00:00',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        organization='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        provider='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        payer='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounterclass='ambulatory',
        code='308646001',
        description='Encounter for check up',
        base_encounter_cost='50.00',
        total_claim_cost='125.00',
        payer_coverage='100.00'
    )
    assert encounter.start == datetime(2020, 1, 1, 10, 0, 0)
    assert encounter.stop is None
    assert encounter.encounterclass == 'ambulatory'
    assert encounter.base_encounter_cost == Decimal('50.00')
    assert encounter.total_claim_cost == Decimal('125.00')
    assert encounter.payer_coverage == Decimal('100.00')
    assert encounter.reasoncode is None
    assert encounter.reasondescription is None
    
    # Test with all fields
    encounter_full = Encounter(
        id='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        start='2020-01-01T10:00:00',
        stop='2020-01-01T10:30:00',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        organization='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        provider='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        payer='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounterclass='emergency',
        code='50849002',
        description='Emergency room admission',
        base_encounter_cost='250.00',
        total_claim_cost='1250.00',
        payer_coverage='1000.00',
        reasoncode='410620009',
        reasondescription='Acute bronchitis (disorder)'
    )
    assert encounter_full.stop == datetime(2020, 1, 1, 10, 30, 0)
    assert encounter_full.encounterclass == 'emergency'
    assert encounter_full.reasoncode == '410620009'
    assert encounter_full.reasondescription == 'Acute bronchitis (disorder)'


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with Encounter(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "encounters.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        encounter = Encounter(**row)
        
        # Verify it loaded correctly
        assert isinstance(encounter.id, UUID)
        assert isinstance(encounter.start, datetime)
        assert isinstance(encounter.patient, UUID)
        assert isinstance(encounter.organization, UUID)
        assert isinstance(encounter.provider, UUID)
        assert isinstance(encounter.payer, UUID)
        assert encounter.encounterclass in ["ambulatory", "emergency", "inpatient", "wellness", "urgentcare", "outpatient"]
        assert isinstance(encounter.code, str)
        assert isinstance(encounter.description, str)
        assert isinstance(encounter.base_encounter_cost, Decimal)
        assert isinstance(encounter.total_claim_cost, Decimal)
        assert isinstance(encounter.payer_coverage, Decimal)


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Simulate a CSV row with empty strings
    csv_row = {
        'Id': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'START': '2020-01-01T10:00:00',
        'STOP': '',  # Empty string should become None
        'PATIENT': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'ORGANIZATION': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'PROVIDER': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'PAYER': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'ENCOUNTERCLASS': 'ambulatory',
        'CODE': '308646001',
        'DESCRIPTION': 'Encounter for check up',
        'BASE_ENCOUNTER_COST': '50.00',
        'TOTAL_CLAIM_COST': '125.00',
        'PAYER_COVERAGE': '100.00',
        'REASONCODE': '',  # Empty string should become None
        'REASONDESCRIPTION': '',  # Empty string should become None
    }
    
    encounter = Encounter(**csv_row)
    
    assert encounter.stop is None
    assert encounter.reasoncode is None
    assert encounter.reasondescription is None