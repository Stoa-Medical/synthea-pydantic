"""Tests for the providers module."""

import csv
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.providers import Provider


def test_load_providers_csv():
    """Test loading providers from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "providers.csv"
    
    providers = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            provider = Provider(**row)
            providers.append(provider)
    
    # Verify we loaded some data
    assert len(providers) > 0
    
    # Check the first provider
    first = providers[0]
    assert first.id == UUID('c23e8780-6030-37ec-8d02-8c6e3def10ac')
    assert first.organization == UUID('ef58ea08-d883-3957-8300-150554edc8fb')
    assert first.name == 'Reginald96 Bruen238'
    assert first.gender == 'M'
    assert first.speciality == 'GENERAL PRACTICE'
    assert first.address == '60 HOSPITAL ROAD'
    assert first.city == 'LEOMINSTER'
    assert first.state == 'MA'
    assert first.zip == '01453'
    assert first.lat == 42.520838
    assert first.lon == -71.770876
    assert first.utilization == 1214


def test_provider_serialization():
    """Test serializing Provider models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "providers.csv"
    
    providers = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            provider = Provider(**row)
            providers.append(provider)
    
    # Test model_dump() for all providers
    for provider in providers:
        data = provider.model_dump()
        assert isinstance(data, dict)
        assert 'id' in data
        assert 'organization' in data
        assert 'name' in data
        assert 'gender' in data
        assert 'speciality' in data
        assert 'address' in data
        assert 'city' in data
        assert 'utilization' in data
    
    # Test model_dump_json() for all providers
    for provider in providers:
        json_str = provider.model_dump_json()
        assert isinstance(json_str, str)
        assert '"id"' in json_str
        assert '"organization"' in json_str
        assert '"name"' in json_str
        assert '"utilization"' in json_str
    
    # Test round-trip serialization
    first_provider = providers[0]
    json_data = first_provider.model_dump_json()
    restored = Provider.model_validate_json(json_data)
    assert restored == first_provider


def test_provider_field_validation():
    """Test field validation for Provider model."""
    # Test with all required fields using lowercase names
    provider = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Provider',
        gender='F',
        speciality='CARDIOLOGY',
        address='123 Main Street',
        city='Boston',
        state='MA',
        zip='02101',
        lat=42.3601,
        lon=-71.0589,
        utilization=500
    )
    assert provider.id == UUID('c23e8780-6030-37ec-8d02-8c6e3def10ac')
    assert provider.organization == UUID('ef58ea08-d883-3957-8300-150554edc8fb')
    assert provider.name == 'Test Provider'
    assert provider.gender == 'F'
    assert provider.speciality == 'CARDIOLOGY'
    assert provider.address == '123 Main Street'
    assert provider.city == 'Boston'
    assert provider.state == 'MA'
    assert provider.zip == '02101'
    assert provider.lat == 42.3601
    assert provider.lon == -71.0589
    assert provider.utilization == 500
    
    # Test with minimal required fields (optional fields as None)
    provider_minimal = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Minimal Provider',
        gender='M',
        speciality='GENERAL PRACTICE',
        address='456 Oak Street',
        city='Cambridge',
        utilization=0
    )
    assert provider_minimal.state is None
    assert provider_minimal.zip is None
    assert provider_minimal.lat is None
    assert provider_minimal.lon is None


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with Provider(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "providers.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        provider = Provider(**row)
        
        # Verify it loaded correctly
        assert provider.id == UUID('c23e8780-6030-37ec-8d02-8c6e3def10ac')
        assert provider.name == 'Reginald96 Bruen238'
        assert provider.gender == 'M'
        assert provider.speciality == 'GENERAL PRACTICE'
        assert provider.utilization == 1214


def test_provider_specialties_validation():
    """Test that different provider specialties are handled correctly."""
    csv_path = Path(__file__).parent / "data" / "csv" / "providers.csv"
    
    providers = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 150:  # Test first 150 rows to get variety
                break
            provider = Provider(**row)
            providers.append(provider)
    
    # Verify we have different specialties
    specialties = {provider.speciality for provider in providers}
    
    # Should have multiple different specialties
    assert len(specialties) > 1
    
    # Check some expected specialties from the data
    expected_specialties = {
        'GENERAL PRACTICE', 'CLINICAL PSYCHOLOGIST', 'PHYSICAL THERAPY',
        'CLINICAL SOCIAL WORKER', 'CHIROPRACTIC', 'NURSE PRACTITIONER',
        'NEUROLOGY', 'FAMILY PRACTICE', 'OPTOMETRY', 'PSYCHIATRY'
    }
    found_specialties = specialties.intersection(expected_specialties)
    assert len(found_specialties) > 0


def test_gender_validation():
    """Test gender field validation."""
    # Test valid genders
    provider_male = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Male Provider',
        gender='M',
        speciality='GENERAL PRACTICE',
        address='123 Main Street',
        city='Boston',
        utilization=100
    )
    assert provider_male.gender == 'M'
    
    provider_female = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Female Provider',
        gender='F',
        speciality='GENERAL PRACTICE',
        address='123 Main Street',
        city='Boston',
        utilization=100
    )
    assert provider_female.gender == 'F'


def test_coordinate_validation():
    """Test latitude and longitude field validation."""
    # Test with valid coordinates
    provider = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Provider',
        gender='M',
        speciality='GENERAL PRACTICE',
        address='123 Main Street',
        city='Boston',
        lat=42.3601,
        lon=-71.0589,
        utilization=100
    )
    assert provider.lat == 42.3601
    assert provider.lon == -71.0589
    
    # Test with None coordinates
    provider_no_coords = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Provider',
        gender='M',
        speciality='GENERAL PRACTICE',
        address='123 Main Street',
        city='Boston',
        utilization=100
    )
    assert provider_no_coords.lat is None
    assert provider_no_coords.lon is None


def test_uuid_validation():
    """Test UUID field validation."""
    # Test with string UUIDs
    provider = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Provider',
        gender='M',
        speciality='GENERAL PRACTICE',
        address='123 Main Street',
        city='Boston',
        utilization=100
    )
    assert isinstance(provider.id, UUID)
    assert isinstance(provider.organization, UUID)
    
    # Test with UUID objects
    provider_id = UUID('c23e8780-6030-37ec-8d02-8c6e3def10ac')
    org_id = UUID('ef58ea08-d883-3957-8300-150554edc8fb')
    
    provider_uuid_obj = Provider(
        id=provider_id,
        organization=org_id,
        name='Test Provider',
        gender='M',
        speciality='GENERAL PRACTICE',
        address='123 Main Street',
        city='Boston',
        utilization=100
    )
    assert provider_uuid_obj.id == provider_id
    assert provider_uuid_obj.organization == org_id


def test_string_field_validation():
    """Test string field validation and whitespace handling."""
    # Test with extra whitespace
    provider = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='  Test Provider  ',  # Extra whitespace
        gender='M',
        speciality='  GENERAL PRACTICE  ',  # Extra whitespace
        address='  123 Main Street  ',  # Extra whitespace
        city='  Boston  ',  # Extra whitespace
        state='  MA  ',  # Extra whitespace
        zip='  02101  ',  # Extra whitespace
        utilization=100
    )
    # Whitespace should be stripped due to str_strip_whitespace=True
    assert provider.name == 'Test Provider'
    assert provider.speciality == 'GENERAL PRACTICE'
    assert provider.address == '123 Main Street'
    assert provider.city == 'Boston'
    assert provider.state == 'MA'
    assert provider.zip == '02101'


def test_utilization_validation():
    """Test utilization field validation."""
    # Test zero utilization
    provider_zero = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Zero Utilization Provider',
        gender='M',
        speciality='GENERAL PRACTICE',
        address='123 Main Street',
        city='Boston',
        utilization=0
    )
    assert provider_zero.utilization == 0
    
    # Test high utilization
    provider_high = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='High Utilization Provider',
        gender='F',
        speciality='EMERGENCY MEDICINE',
        address='456 Hospital Ave',
        city='Boston',
        utilization=5000
    )
    assert provider_high.utilization == 5000


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Simulate a CSV row with empty strings
    csv_row = {
        'Id': 'c23e8780-6030-37ec-8d02-8c6e3def10ac',
        'ORGANIZATION': 'ef58ea08-d883-3957-8300-150554edc8fb',
        'NAME': 'Test Provider',
        'GENDER': 'M',
        'SPECIALITY': 'GENERAL PRACTICE',
        'ADDRESS': '123 Main Street',
        'CITY': 'Boston',
        'STATE': '',  # Empty string should become None
        'ZIP': '',  # Empty string should become None
        'LAT': '',  # Empty string should become None
        'LON': '',  # Empty string should become None
        'UTILIZATION': '100'
    }
    
    provider = Provider(**csv_row)
    
    assert provider.state is None
    assert provider.zip is None
    assert provider.lat is None
    assert provider.lon is None
    assert provider.utilization == 100


def test_provider_model_config():
    """Test that the model configuration is working correctly."""
    # Test that str_strip_whitespace is working
    provider = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='   Test Provider   ',
        gender='M',
        speciality='   GENERAL PRACTICE   ',
        address='   123 Main Street   ',
        city='   Boston   ',
        utilization=100
    )
    
    assert provider.name == 'Test Provider'
    assert provider.speciality == 'GENERAL PRACTICE'
    assert provider.address == '123 Main Street'
    assert provider.city == 'Boston'


def test_provider_equality():
    """Test Provider model equality comparison."""
    provider1 = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Provider',
        gender='M',
        speciality='GENERAL PRACTICE',
        address='123 Main Street',
        city='Boston',
        utilization=100
    )
    
    provider2 = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Provider',
        gender='M',
        speciality='GENERAL PRACTICE',
        address='123 Main Street',
        city='Boston',
        utilization=100
    )
    
    provider3 = Provider(
        id='c23e8780-6030-37ec-8d02-8c6e3def10ac',
        organization='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Provider',
        gender='M',
        speciality='GENERAL PRACTICE',
        address='123 Main Street',
        city='Boston',
        utilization=200  # Different utilization
    )
    
    assert provider1 == provider2
    assert provider1 != provider3 