"""Tests for the patients module."""

import csv
from datetime import date
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.patients import Patient


def test_load_patients_csv():
    """Test loading patients from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "patients.csv"
    
    patients = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            patient = Patient(**row)
            patients.append(patient)
    
    # Verify we loaded some data
    assert len(patients) > 0
    
    # Check the first patient
    first = patients[0]
    assert isinstance(first.id, UUID)
    assert isinstance(first.birthdate, date)
    assert first.deathdate is None or isinstance(first.deathdate, date)
    assert isinstance(first.ssn, str)
    assert first.drivers is None or isinstance(first.drivers, str)
    assert first.passport is None or isinstance(first.passport, str)
    assert first.prefix is None or isinstance(first.prefix, str)
    assert isinstance(first.first, str)
    assert isinstance(first.last, str)
    assert first.suffix is None or isinstance(first.suffix, str)
    assert first.maiden is None or isinstance(first.maiden, str)
    assert first.marital is None or first.marital in ["M", "S"]
    assert isinstance(first.race, str)
    assert isinstance(first.ethnicity, str)
    assert first.gender in ["M", "F"]
    assert isinstance(first.birthplace, str)
    assert isinstance(first.address, str)
    assert isinstance(first.city, str)
    assert isinstance(first.state, str)
    assert first.county is None or isinstance(first.county, str)
    assert first.zip is None or isinstance(first.zip, str)
    assert first.lat is None or isinstance(first.lat, Decimal)
    assert first.lon is None or isinstance(first.lon, Decimal)
    assert isinstance(first.healthcare_expenses, Decimal)
    assert isinstance(first.healthcare_coverage, Decimal)


def test_patient_serialization():
    """Test serializing Patient models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "patients.csv"
    
    patients = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            patient = Patient(**row)
            patients.append(patient)
    
    # Test model_dump() for all patients
    for patient in patients:
        data = patient.model_dump()
        assert isinstance(data, dict)
        assert 'id' in data
        assert 'birthdate' in data
        assert 'ssn' in data
        assert 'first' in data
        assert 'last' in data
        assert 'gender' in data
        assert 'race' in data
        assert 'ethnicity' in data
        assert 'birthplace' in data
        assert 'address' in data
        assert 'city' in data
        assert 'state' in data
        assert 'healthcare_expenses' in data
        assert 'healthcare_coverage' in data
    
    # Test model_dump_json() for all patients
    for patient in patients:
        json_str = patient.model_dump_json()
        assert isinstance(json_str, str)
        assert '"id"' in json_str
        assert '"birthdate"' in json_str
        assert '"first"' in json_str
        assert '"last"' in json_str
    
    # Test round-trip serialization
    first_patient = patients[0]
    json_data = first_patient.model_dump_json()
    restored = Patient.model_validate_json(json_data)
    assert restored == first_patient


def test_patient_field_validation():
    """Test field validation for Patient model."""
    # Test with minimal required fields using lowercase names
    patient = Patient(
        id='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        birthdate='1990-01-01',
        ssn='999-99-9999',
        first='John',
        last='Doe',
        gender='M',
        race='white',
        ethnicity='nonhispanic',
        birthplace='Boston MA US',
        address='123 Main St',
        city='Boston',
        state='MA',
        healthcare_expenses='1234.56',
        healthcare_coverage='5678.90'
    )
    assert patient.birthdate == date(1990, 1, 1)
    assert patient.deathdate is None
    assert patient.drivers is None
    assert patient.passport is None
    assert patient.prefix is None
    assert patient.suffix is None
    assert patient.maiden is None
    assert patient.marital is None
    assert patient.county is None
    assert patient.zip is None
    assert patient.lat is None
    assert patient.lon is None
    
    # Test with all fields
    patient_full = Patient(
        id='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        birthdate='1990-01-01',
        deathdate='2050-01-01',
        ssn='999-99-9999',
        drivers='S99999999',
        passport='X99999999',
        prefix='Mr.',
        first='John',
        last='Doe',
        suffix='Jr.',
        maiden='Smith',
        marital='M',
        race='white',
        ethnicity='nonhispanic',
        gender='M',
        birthplace='Boston MA US',
        address='123 Main St',
        city='Boston',
        state='MA',
        county='Suffolk County',
        zip='02101',
        lat='42.3601',
        lon='-71.0589',
        healthcare_expenses='1234.56',
        healthcare_coverage='5678.90'
    )
    assert patient_full.deathdate == date(2050, 1, 1)
    assert patient_full.drivers == 'S99999999'
    assert patient_full.passport == 'X99999999'
    assert patient_full.prefix == 'Mr.'
    assert patient_full.suffix == 'Jr.'
    assert patient_full.maiden == 'Smith'
    assert patient_full.marital == 'M'
    assert patient_full.county == 'Suffolk County'
    assert patient_full.zip == '02101'
    assert patient_full.lat == Decimal('42.3601')
    assert patient_full.lon == Decimal('-71.0589')


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with Patient(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "patients.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        patient = Patient(**row)
        
        # Verify it loaded correctly
        assert isinstance(patient.id, UUID)
        assert isinstance(patient.birthdate, date)
        assert isinstance(patient.ssn, str)
        assert isinstance(patient.first, str)
        assert isinstance(patient.last, str)
        assert patient.gender in ["M", "F"]
        assert isinstance(patient.healthcare_expenses, Decimal)
        assert isinstance(patient.healthcare_coverage, Decimal)


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Simulate a CSV row with empty strings
    csv_row = {
        'Id': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'BIRTHDATE': '1990-01-01',
        'DEATHDATE': '',  # Empty string should become None
        'SSN': '999-99-9999',
        'DRIVERS': '',  # Empty string should become None
        'PASSPORT': '',  # Empty string should become None
        'PREFIX': '',  # Empty string should become None
        'FIRST': 'John',
        'LAST': 'Doe',
        'SUFFIX': '',  # Empty string should become None
        'MAIDEN': '',  # Empty string should become None
        'MARITAL': '',  # Empty string should become None
        'RACE': 'white',
        'ETHNICITY': 'nonhispanic',
        'GENDER': 'M',
        'BIRTHPLACE': 'Boston MA US',
        'ADDRESS': '123 Main St',
        'CITY': 'Boston',
        'STATE': 'MA',
        'COUNTY': '',  # Empty string should become None
        'ZIP': '',  # Empty string should become None
        'LAT': '',  # Empty string should become None
        'LON': '',  # Empty string should become None
        'HEALTHCARE_EXPENSES': '1234.56',
        'HEALTHCARE_COVERAGE': '5678.90'
    }
    
    patient = Patient(**csv_row)
    
    assert patient.deathdate is None
    assert patient.drivers is None
    assert patient.passport is None
    assert patient.prefix is None
    assert patient.suffix is None
    assert patient.maiden is None
    assert patient.marital is None
    assert patient.county is None
    assert patient.zip is None
    assert patient.lat is None
    assert patient.lon is None
