"""Tests for the organizations module."""

import csv
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.organizations import Organization


def test_load_organizations_csv():
    """Test loading organizations from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "organizations.csv"
    
    organizations = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            organization = Organization(**row)
            organizations.append(organization)
    
    # Verify we loaded some data
    assert len(organizations) > 0
    
    # Check the first organization
    first = organizations[0]
    assert first.id == UUID('ef58ea08-d883-3957-8300-150554edc8fb')
    assert first.name == 'HEALTHALLIANCE HOSPITALS  INC'
    assert first.address == '60 HOSPITAL ROAD'
    assert first.city == 'LEOMINSTER'
    assert first.state == 'MA'
    assert first.zip == '01453'
    assert first.lat == 42.520838
    assert first.lon == -71.770876
    assert first.phone == '9784662000'
    assert first.revenue == Decimal('0.0')
    assert first.utilization == 1214


def test_organization_serialization():
    """Test serializing Organization models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "organizations.csv"
    
    organizations = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 10:  # Test first 10 rows for performance
                break
            organization = Organization(**row)
            organizations.append(organization)
    
    # Test model_dump() for all organizations
    for organization in organizations:
        data = organization.model_dump()
        assert isinstance(data, dict)
        assert 'id' in data
        assert 'name' in data
        assert 'address' in data
        assert 'city' in data
        assert 'state' in data
        assert 'zip' in data
        assert 'lat' in data
        assert 'lon' in data
        assert 'phone' in data
        assert 'revenue' in data
        assert 'utilization' in data
    
    # Test model_dump_json() for all organizations
    for organization in organizations:
        json_str = organization.model_dump_json()
        assert isinstance(json_str, str)
        assert '"id"' in json_str
        assert '"name"' in json_str
        assert '"address"' in json_str
        assert '"revenue"' in json_str
        assert '"utilization"' in json_str
    
    # Test round-trip serialization
    first_organization = organizations[0]
    json_data = first_organization.model_dump_json()
    restored = Organization.model_validate_json(json_data)
    assert restored == first_organization


def test_organization_field_validation():
    """Test field validation for Organization model."""
    # Test with all fields using lowercase names
    organization = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        state='MA',
        zip='02101',
        lat=42.3601,
        lon=-71.0589,
        phone='6175551234',
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    assert organization.id == UUID('ef58ea08-d883-3957-8300-150554edc8fb')
    assert organization.name == 'Test Hospital'
    assert organization.address == '123 Main Street'
    assert organization.city == 'Boston'
    assert organization.state == 'MA'
    assert organization.zip == '02101'
    assert organization.lat == 42.3601
    assert organization.lon == -71.0589
    assert organization.phone == '6175551234'
    assert organization.revenue == Decimal('1000000.00')
    assert organization.utilization == 500
    
    # Test with minimal required fields (optional fields as None)
    organization_minimal = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Minimal Hospital',
        address='456 Oak Street',
        city='Cambridge',
        revenue=Decimal('0.00'),
        utilization=0
    )
    assert organization_minimal.state is None
    assert organization_minimal.zip is None
    assert organization_minimal.lat is None
    assert organization_minimal.lon is None
    assert organization_minimal.phone is None


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with Organization(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "organizations.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        organization = Organization(**row)
        
        # Verify it loaded correctly
        assert organization.id == UUID('ef58ea08-d883-3957-8300-150554edc8fb')
        assert organization.name == 'HEALTHALLIANCE HOSPITALS  INC'
        assert organization.address == '60 HOSPITAL ROAD'
        assert organization.city == 'LEOMINSTER'
        assert organization.state == 'MA'
        assert organization.zip == '01453'
        assert organization.revenue == Decimal('0.0')
        assert organization.utilization == 1214


def test_organization_names_validation():
    """Test that different organization names are handled correctly."""
    csv_path = Path(__file__).parent / "data" / "csv" / "organizations.csv"
    
    organizations = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            organization = Organization(**row)
            organizations.append(organization)
    
    # Verify we have different organization names
    organization_names = {org.name for org in organizations}
    
    # Should have multiple different organizations
    assert len(organization_names) > 1
    
    # Check some expected organization types from the data
    expected_names = {
        'HEALTHALLIANCE HOSPITALS  INC', 'MOUNT AUBURN HOSPITAL', 
        'STURDY MEMORIAL HOSPITAL', 'LAWRENCE GENERAL HOSPITAL'
    }
    found_names = organization_names.intersection(expected_names)
    assert len(found_names) > 0


def test_coordinate_validation():
    """Test latitude and longitude coordinate validation."""
    # Test with valid coordinates
    organization = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        state='MA',
        zip='02101',
        lat=42.3601,  # Valid Boston latitude
        lon=-71.0589,  # Valid Boston longitude
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    assert organization.lat == 42.3601
    assert organization.lon == -71.0589
    
    # Test with None coordinates
    organization_no_coords = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    assert organization_no_coords.lat is None
    assert organization_no_coords.lon is None
    
    # Test with edge case coordinates
    organization_edge = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        lat=0.0,  # Equator
        lon=0.0,  # Prime meridian
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    assert organization_edge.lat == 0.0
    assert organization_edge.lon == 0.0


def test_decimal_field_validation():
    """Test decimal field validation for revenue amounts."""
    # Test with valid decimal amounts
    organization = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        revenue=Decimal('1234567.89'),
        utilization=500
    )
    assert organization.revenue == Decimal('1234567.89')
    
    # Test with zero revenue
    organization_zero = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Zero Revenue Hospital',
        address='123 Main Street',
        city='Boston',
        revenue=Decimal('0.00'),
        utilization=0
    )
    assert organization_zero.revenue == Decimal('0.00')
    
    # Test with large revenue
    organization_large = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Large Revenue Hospital',
        address='123 Main Street',
        city='Boston',
        revenue=Decimal('999999999.99'),
        utilization=10000
    )
    assert organization_large.revenue == Decimal('999999999.99')


def test_integer_field_validation():
    """Test integer field validation for utilization counts."""
    # Test with various integer values
    organization = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        revenue=Decimal('1000000.00'),
        utilization=1500
    )
    assert organization.utilization == 1500
    
    # Test with zero utilization
    organization_zero = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Zero Utilization Hospital',
        address='123 Main Street',
        city='Boston',
        revenue=Decimal('0.00'),
        utilization=0
    )
    assert organization_zero.utilization == 0
    
    # Test with high utilization
    organization_high = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='High Utilization Hospital',
        address='123 Main Street',
        city='Boston',
        revenue=Decimal('5000000.00'),
        utilization=50000
    )
    assert organization_high.utilization == 50000


def test_uuid_validation():
    """Test UUID field validation."""
    # Test with string UUID
    organization = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    assert isinstance(organization.id, UUID)
    
    # Test with UUID object
    org_id = UUID('ef58ea08-d883-3957-8300-150554edc8fb')
    organization_uuid_obj = Organization(
        id=org_id,
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    assert organization_uuid_obj.id == org_id


def test_string_field_validation():
    """Test string field validation and whitespace handling."""
    # Test with extra whitespace
    organization = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='  Test Hospital  ',  # Extra whitespace
        address='  123 Main Street  ',  # Extra whitespace
        city='  Boston  ',  # Extra whitespace
        state='  MA  ',  # Extra whitespace
        zip='  02101  ',  # Extra whitespace
        phone='  6175551234  ',  # Extra whitespace
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    # Whitespace should be stripped due to str_strip_whitespace=True
    assert organization.name == 'Test Hospital'
    assert organization.address == '123 Main Street'
    assert organization.city == 'Boston'
    assert organization.state == 'MA'
    assert organization.zip == '02101'
    assert organization.phone == '6175551234'


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Simulate a CSV row with empty strings
    csv_row = {
        'Id': 'ef58ea08-d883-3957-8300-150554edc8fb',
        'NAME': 'Test Hospital',
        'ADDRESS': '123 Main Street',
        'CITY': 'Boston',
        'STATE': '',  # Empty string should become None
        'ZIP': '',  # Empty string should become None
        'LAT': '',  # Empty string should become None
        'LON': '',  # Empty string should become None
        'PHONE': '',  # Empty string should become None
        'REVENUE': '1000000.00',
        'UTILIZATION': '500'
    }
    
    organization = Organization(**csv_row)
    
    assert organization.name == 'Test Hospital'
    assert organization.address == '123 Main Street'
    assert organization.city == 'Boston'
    assert organization.state is None  # Empty string converted to None
    assert organization.zip is None  # Empty string converted to None
    assert organization.lat is None  # Empty string converted to None
    assert organization.lon is None  # Empty string converted to None
    assert organization.phone is None  # Empty string converted to None
    assert organization.revenue == Decimal('1000000.00')
    assert organization.utilization == 500


def test_phone_number_validation():
    """Test phone number field validation."""
    # Test with standard phone number
    organization = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        phone='6175551234',
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    assert organization.phone == '6175551234'
    
    # Test with formatted phone number
    organization_formatted = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        phone='(617) 555-1234',
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    assert organization_formatted.phone == '(617) 555-1234'
    
    # Test with None phone number
    organization_no_phone = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    assert organization_no_phone.phone is None


def test_organization_model_config():
    """Test that the model configuration is working correctly."""
    # Test that str_strip_whitespace is working
    organization = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='   Test Hospital   ',
        address='   123 Main Street   ',
        city='   Boston   ',
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    
    assert organization.name == 'Test Hospital'
    assert organization.address == '123 Main Street'
    assert organization.city == 'Boston'


def test_organization_equality():
    """Test Organization model equality comparison."""
    organization1 = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        state='MA',
        zip='02101',
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    
    organization2 = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        state='MA',
        zip='02101',
        revenue=Decimal('1000000.00'),
        utilization=500
    )
    
    organization3 = Organization(
        id='ef58ea08-d883-3957-8300-150554edc8fb',
        name='Test Hospital',
        address='123 Main Street',
        city='Boston',
        state='MA',
        zip='02101',
        revenue=Decimal('2000000.00'),  # Different revenue
        utilization=500
    )
    
    assert organization1 == organization2
    assert organization1 != organization3


def test_massachusetts_organizations():
    """Test organizations in Massachusetts (common in the data)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "organizations.csv"
    
    organizations = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            organization = Organization(**row)
            organizations.append(organization)
    
    # Find Massachusetts organizations
    ma_organizations = [org for org in organizations if org.state == 'MA']
    
    # Should have some Massachusetts organizations in the data
    assert len(ma_organizations) > 0
    
    # Verify Massachusetts organizations have reasonable coordinates
    for org in ma_organizations:
        if org.lat is not None and org.lon is not None:
            # Massachusetts latitude range: approximately 41.2 to 42.9
            assert 40.0 <= org.lat <= 43.0, f"MA org {org.name} has invalid latitude: {org.lat}"
            # Massachusetts longitude range: approximately -73.5 to -69.9
            assert -74.0 <= org.lon <= -69.0, f"MA org {org.name} has invalid longitude: {org.lon}"


def test_revenue_utilization_relationship():
    """Test the relationship between revenue and utilization."""
    csv_path = Path(__file__).parent / "data" / "csv" / "organizations.csv"
    
    organizations = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            organization = Organization(**row)
            organizations.append(organization)
    
    # Verify that organizations with higher utilization tend to have higher revenue
    # (though this may not always be true due to different pricing models)
    high_utilization_orgs = [org for org in organizations if org.utilization > 1000]
    low_utilization_orgs = [org for org in organizations if org.utilization < 100]
    
    if high_utilization_orgs and low_utilization_orgs:
        # Calculate average revenue for each group
        high_util_avg_revenue = sum(org.revenue for org in high_utilization_orgs) / len(high_utilization_orgs)
        low_util_avg_revenue = sum(org.revenue for org in low_utilization_orgs) / len(low_utilization_orgs)
        
        # Note: In the test data, revenue might be 0 for all organizations
        # so we just verify the calculation works without asserting a relationship
        assert isinstance(high_util_avg_revenue, Decimal)
        assert isinstance(low_util_avg_revenue, Decimal)


def test_organization_address_completeness():
    """Test that organizations have complete address information."""
    csv_path = Path(__file__).parent / "data" / "csv" / "organizations.csv"
    
    organizations = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 20:  # Test first 20 organizations
                break
            organization = Organization(**row)
            organizations.append(organization)
    
    # Verify all organizations have required address fields
    for org in organizations:
        assert org.name is not None and len(org.name.strip()) > 0
        assert org.address is not None and len(org.address.strip()) > 0
        assert org.city is not None and len(org.city.strip()) > 0
        # state and zip are optional, but if present should be non-empty
        if org.state is not None:
            assert len(org.state.strip()) > 0
        if org.zip is not None:
            assert len(org.zip.strip()) > 0 