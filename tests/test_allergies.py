"""Tests for the allergies module."""

import csv
from datetime import date
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.allergies import Allergy


def test_load_allergies_csv():
    """Test loading allergies from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "allergies.csv"
    
    allergies = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            allergy = Allergy(
                start=row['START'],
                stop=row['STOP'] if row['STOP'] else None,
                patient=row['PATIENT'],
                encounter=row['ENCOUNTER'],
                code=row['CODE'],
                system=row['SYSTEM'],
                description=row['DESCRIPTION'],
                type=row['TYPE'] if row['TYPE'] else None,
                category=row['CATEGORY'] if row['CATEGORY'] else None,
                reaction1=row['REACTION1'] if row['REACTION1'] else None,
                description1=row['DESCRIPTION1'] if row['DESCRIPTION1'] else None,
                severity1=row['SEVERITY1'] if row['SEVERITY1'] else None,
                reaction2=row['REACTION2'] if row['REACTION2'] else None,
                description2=row['DESCRIPTION2'] if row['DESCRIPTION2'] else None,
                severity2=row['SEVERITY2'] if row['SEVERITY2'] else None,
            )
            allergies.append(allergy)
    
    # Verify we loaded some data
    assert len(allergies) > 0
    
    # Check the first allergy
    first = allergies[0]
    assert first.start == date(2020, 2, 17)
    assert first.stop is None
    assert first.patient == UUID('b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85')
    assert first.encounter == UUID('01efcc52-15d6-51e9-faa2-bee069fcbe44')
    assert first.code == '111088007'
    assert first.system == 'Unknown'
    assert first.description == 'Latex (substance)'
    assert first.type == 'allergy'
    assert first.category == 'environment'
    assert first.reaction1 == '247472004'
    assert first.description1 == 'Wheal (finding)'
    assert first.severity1 == 'MILD'
    assert first.reaction2 is None
    assert first.description2 is None
    assert first.severity2 is None


def test_allergy_serialization():
    """Test serializing Allergy models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "allergies.csv"
    
    allergies = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            allergy = Allergy(
                start=row['START'],
                stop=row['STOP'] if row['STOP'] else None,
                patient=row['PATIENT'],
                encounter=row['ENCOUNTER'],
                code=row['CODE'],
                system=row['SYSTEM'],
                description=row['DESCRIPTION'],
                type=row['TYPE'] if row['TYPE'] else None,
                category=row['CATEGORY'] if row['CATEGORY'] else None,
                reaction1=row['REACTION1'] if row['REACTION1'] else None,
                description1=row['DESCRIPTION1'] if row['DESCRIPTION1'] else None,
                severity1=row['SEVERITY1'] if row['SEVERITY1'] else None,
                reaction2=row['REACTION2'] if row['REACTION2'] else None,
                description2=row['DESCRIPTION2'] if row['DESCRIPTION2'] else None,
                severity2=row['SEVERITY2'] if row['SEVERITY2'] else None,
            )
            allergies.append(allergy)
    
    # Test model_dump() for all allergies
    for allergy in allergies:
        data = allergy.model_dump()
        assert isinstance(data, dict)
        assert 'start' in data
        assert 'patient' in data
        assert 'encounter' in data
        assert 'code' in data
        assert 'description' in data
    
    # Test model_dump_json() for all allergies
    for allergy in allergies:
        json_str = allergy.model_dump_json()
        assert isinstance(json_str, str)
        assert '"start"' in json_str
        assert '"patient"' in json_str
        assert '"encounter"' in json_str
    
    # Test round-trip serialization
    first_allergy = allergies[0]
    json_data = first_allergy.model_dump_json()
    restored = Allergy.model_validate_json(json_data)
    assert restored == first_allergy


def test_allergy_field_validation():
    """Test field validation for Allergy model."""
    # Test with minimal required fields
    allergy = Allergy(
        start='2020-01-01',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='123456',
        system='SNOMED-CT',
        description='Test allergy'
    )
    assert allergy.start == date(2020, 1, 1)
    assert allergy.stop is None
    assert allergy.type is None
    assert allergy.category is None
    
    # Test with all fields
    allergy_full = Allergy(
        start='2020-01-01',
        stop='2021-01-01',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='123456',
        system='RxNorm',
        description='Test medication allergy',
        type='allergy',
        category='medication',
        reaction1='789012',
        description1='Reaction description',
        severity1='SEVERE',
        reaction2='345678',
        description2='Second reaction',
        severity2='MILD'
    )
    assert allergy_full.stop == date(2021, 1, 1)
    assert allergy_full.type == 'allergy'
    assert allergy_full.category == 'medication'
    assert allergy_full.severity1 == 'SEVERE'
    assert allergy_full.severity2 == 'MILD'