"""Tests for the payers module."""

import csv
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.payers import Payer


def test_load_payers_csv():
    """Test loading payers from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "payers.csv"
    
    payers = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            payer = Payer(**row)
            payers.append(payer)
    
    # Verify we loaded some data
    assert len(payers) > 0
    
    # Check the first payer (Dual Eligible)
    first = payers[0]
    assert first.id == UUID('b3221cfc-24fb-339e-823d-bc4136cbc4ed')
    assert first.name == 'Dual Eligible'
    assert first.address == '7500 Security Blvd'
    assert first.city == 'Baltimore'
    assert first.state_headquartered == 'MD'
    assert first.zip == '21244'
    assert first.phone == '1-877-267-2323'
    assert first.amount_covered == Decimal('2786029.66')
    assert first.amount_uncovered == Decimal('358233.14')
    assert first.revenue == Decimal('1439000.00')
    assert first.covered_encounters == 1121
    assert first.uncovered_encounters == 0
    assert first.covered_medications == 1141
    assert first.uncovered_medications == 0
    assert first.covered_procedures == 551
    assert first.uncovered_procedures == 0
    assert first.covered_immunizations == 280
    assert first.uncovered_immunizations == 0
    assert first.unique_customers == 20
    assert first.qols_avg == 0.5370553777293092
    assert first.member_months == 3060


def test_payer_serialization():
    """Test serializing Payer models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "payers.csv"
    
    payers = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            payer = Payer(**row)
            payers.append(payer)
    
    # Test model_dump() for all payers
    for payer in payers:
        data = payer.model_dump()
        assert isinstance(data, dict)
        assert 'id' in data
        assert 'name' in data
        assert 'amount_covered' in data
        assert 'amount_uncovered' in data
        assert 'revenue' in data
        assert 'unique_customers' in data
        assert 'qols_avg' in data
        assert 'member_months' in data
    
    # Test model_dump_json() for all payers
    for payer in payers:
        json_str = payer.model_dump_json()
        assert isinstance(json_str, str)
        assert '"id"' in json_str
        assert '"name"' in json_str
        assert '"amount_covered"' in json_str
        assert '"revenue"' in json_str
    
    # Test round-trip serialization
    first_payer = payers[0]
    json_data = first_payer.model_dump_json()
    restored = Payer.model_validate_json(json_data)
    assert restored == first_payer


def test_payer_field_validation():
    """Test field validation for Payer model."""
    # Test with all fields using lowercase names
    payer = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='Test Payer',
        address='123 Main Street',
        city='Boston',
        state_headquartered='MA',
        zip='02101',
        phone='1-800-555-0123',
        amount_covered=Decimal('1000000.00'),
        amount_uncovered=Decimal('50000.00'),
        revenue=Decimal('2000000.00'),
        covered_encounters=500,
        uncovered_encounters=10,
        covered_medications=300,
        uncovered_medications=5,
        covered_procedures=200,
        uncovered_procedures=3,
        covered_immunizations=100,
        uncovered_immunizations=2,
        unique_customers=150,
        qols_avg=0.85,
        member_months=1800
    )
    assert payer.id == UUID('b3221cfc-24fb-339e-823d-bc4136cbc4ed')
    assert payer.name == 'Test Payer'
    assert payer.address == '123 Main Street'
    assert payer.city == 'Boston'
    assert payer.state_headquartered == 'MA'
    assert payer.zip == '02101'
    assert payer.phone == '1-800-555-0123'
    assert payer.amount_covered == Decimal('1000000.00')
    assert payer.amount_uncovered == Decimal('50000.00')
    assert payer.revenue == Decimal('2000000.00')
    assert payer.covered_encounters == 500
    assert payer.uncovered_encounters == 10
    assert payer.covered_medications == 300
    assert payer.uncovered_medications == 5
    assert payer.covered_procedures == 200
    assert payer.uncovered_procedures == 3
    assert payer.covered_immunizations == 100
    assert payer.uncovered_immunizations == 2
    assert payer.unique_customers == 150
    assert payer.qols_avg == 0.85
    assert payer.member_months == 1800
    
    # Test with minimal required fields (optional fields as None)
    payer_minimal = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='Minimal Payer',
        amount_covered=Decimal('0.00'),
        amount_uncovered=Decimal('0.00'),
        revenue=Decimal('0.00'),
        covered_encounters=0,
        uncovered_encounters=0,
        covered_medications=0,
        uncovered_medications=0,
        covered_procedures=0,
        uncovered_procedures=0,
        covered_immunizations=0,
        uncovered_immunizations=0,
        unique_customers=0,
        qols_avg=0.0,
        member_months=0
    )
    assert payer_minimal.address is None
    assert payer_minimal.city is None
    assert payer_minimal.state_headquartered is None
    assert payer_minimal.zip is None
    assert payer_minimal.phone is None


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with Payer(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "payers.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        payer = Payer(**row)
        
        # Verify it loaded correctly
        assert payer.id == UUID('b3221cfc-24fb-339e-823d-bc4136cbc4ed')
        assert payer.name == 'Dual Eligible'
        assert payer.amount_covered == Decimal('2786029.66')
        assert payer.revenue == Decimal('1439000.00')
        assert payer.unique_customers == 20


def test_payer_names_validation():
    """Test that different payer names are handled correctly."""
    csv_path = Path(__file__).parent / "data" / "csv" / "payers.csv"
    
    payers = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            payer = Payer(**row)
            payers.append(payer)
    
    # Verify we have different payer names
    payer_names = {payer.name for payer in payers}
    
    # Should have multiple different payers
    assert len(payer_names) > 1
    
    # Check some expected payer names from the data
    expected_names = {
        'Dual Eligible', 'Medicare', 'Medicaid', 'Humana',
        'Blue Cross Blue Shield', 'UnitedHealthcare', 'Aetna',
        'Cigna Health', 'Anthem', 'NO_INSURANCE'
    }
    found_names = payer_names.intersection(expected_names)
    assert len(found_names) > 0


def test_decimal_field_validation():
    """Test decimal field validation for monetary amounts."""
    # Test with valid decimal amounts
    payer = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='Test Payer',
        amount_covered=Decimal('1234567.89'),
        amount_uncovered=Decimal('987654.32'),
        revenue=Decimal('5000000.00'),
        covered_encounters=100,
        uncovered_encounters=0,
        covered_medications=50,
        uncovered_medications=0,
        covered_procedures=25,
        uncovered_procedures=0,
        covered_immunizations=10,
        uncovered_immunizations=0,
        unique_customers=75,
        qols_avg=0.75,
        member_months=900
    )
    assert payer.amount_covered == Decimal('1234567.89')
    assert payer.amount_uncovered == Decimal('987654.32')
    assert payer.revenue == Decimal('5000000.00')
    
    # Test with zero amounts
    payer_zero = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='Zero Amounts Payer',
        amount_covered=Decimal('0.00'),
        amount_uncovered=Decimal('0.00'),
        revenue=Decimal('0.00'),
        covered_encounters=0,
        uncovered_encounters=0,
        covered_medications=0,
        uncovered_medications=0,
        covered_procedures=0,
        uncovered_procedures=0,
        covered_immunizations=0,
        uncovered_immunizations=0,
        unique_customers=0,
        qols_avg=0.0,
        member_months=0
    )
    assert payer_zero.amount_covered == Decimal('0.00')
    assert payer_zero.amount_uncovered == Decimal('0.00')
    assert payer_zero.revenue == Decimal('0.00')


def test_integer_field_validation():
    """Test integer field validation for counts."""
    # Test with various integer values
    payer = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='Test Payer',
        amount_covered=Decimal('1000.00'),
        amount_uncovered=Decimal('100.00'),
        revenue=Decimal('2000.00'),
        covered_encounters=1000,
        uncovered_encounters=50,
        covered_medications=800,
        uncovered_medications=25,
        covered_procedures=600,
        uncovered_procedures=15,
        covered_immunizations=400,
        uncovered_immunizations=10,
        unique_customers=500,
        qols_avg=0.8,
        member_months=6000
    )
    assert payer.covered_encounters == 1000
    assert payer.uncovered_encounters == 50
    assert payer.covered_medications == 800
    assert payer.uncovered_medications == 25
    assert payer.covered_procedures == 600
    assert payer.uncovered_procedures == 15
    assert payer.covered_immunizations == 400
    assert payer.uncovered_immunizations == 10
    assert payer.unique_customers == 500
    assert payer.member_months == 6000


def test_float_field_validation():
    """Test float field validation for quality of life scores."""
    # Test with various float values
    payer_low_qol = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='Low QOL Payer',
        amount_covered=Decimal('1000.00'),
        amount_uncovered=Decimal('100.00'),
        revenue=Decimal('2000.00'),
        covered_encounters=100,
        uncovered_encounters=0,
        covered_medications=50,
        uncovered_medications=0,
        covered_procedures=25,
        uncovered_procedures=0,
        covered_immunizations=10,
        uncovered_immunizations=0,
        unique_customers=75,
        qols_avg=0.25,
        member_months=900
    )
    assert payer_low_qol.qols_avg == 0.25
    
    payer_high_qol = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='High QOL Payer',
        amount_covered=Decimal('1000.00'),
        amount_uncovered=Decimal('100.00'),
        revenue=Decimal('2000.00'),
        covered_encounters=100,
        uncovered_encounters=0,
        covered_medications=50,
        uncovered_medications=0,
        covered_procedures=25,
        uncovered_procedures=0,
        covered_immunizations=10,
        uncovered_immunizations=0,
        unique_customers=75,
        qols_avg=0.95,
        member_months=900
    )
    assert payer_high_qol.qols_avg == 0.95


def test_uuid_validation():
    """Test UUID field validation."""
    # Test with string UUID
    payer = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='Test Payer',
        amount_covered=Decimal('1000.00'),
        amount_uncovered=Decimal('100.00'),
        revenue=Decimal('2000.00'),
        covered_encounters=100,
        uncovered_encounters=0,
        covered_medications=50,
        uncovered_medications=0,
        covered_procedures=25,
        uncovered_procedures=0,
        covered_immunizations=10,
        uncovered_immunizations=0,
        unique_customers=75,
        qols_avg=0.8,
        member_months=900
    )
    assert isinstance(payer.id, UUID)
    
    # Test with UUID object
    payer_id = UUID('b3221cfc-24fb-339e-823d-bc4136cbc4ed')
    payer_uuid_obj = Payer(
        id=payer_id,
        name='Test Payer',
        amount_covered=Decimal('1000.00'),
        amount_uncovered=Decimal('100.00'),
        revenue=Decimal('2000.00'),
        covered_encounters=100,
        uncovered_encounters=0,
        covered_medications=50,
        uncovered_medications=0,
        covered_procedures=25,
        uncovered_procedures=0,
        covered_immunizations=10,
        uncovered_immunizations=0,
        unique_customers=75,
        qols_avg=0.8,
        member_months=900
    )
    assert payer_uuid_obj.id == payer_id


def test_string_field_validation():
    """Test string field validation and whitespace handling."""
    # Test with extra whitespace
    payer = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='  Test Payer  ',  # Extra whitespace
        address='  123 Main Street  ',  # Extra whitespace
        city='  Boston  ',  # Extra whitespace
        state_headquartered='  MA  ',  # Extra whitespace
        zip='  02101  ',  # Extra whitespace
        phone='  1-800-555-0123  ',  # Extra whitespace
        amount_covered=Decimal('1000.00'),
        amount_uncovered=Decimal('100.00'),
        revenue=Decimal('2000.00'),
        covered_encounters=100,
        uncovered_encounters=0,
        covered_medications=50,
        uncovered_medications=0,
        covered_procedures=25,
        uncovered_procedures=0,
        covered_immunizations=10,
        uncovered_immunizations=0,
        unique_customers=75,
        qols_avg=0.8,
        member_months=900
    )
    # Whitespace should be stripped due to str_strip_whitespace=True
    assert payer.name == 'Test Payer'
    assert payer.address == '123 Main Street'
    assert payer.city == 'Boston'
    assert payer.state_headquartered == 'MA'
    assert payer.zip == '02101'
    assert payer.phone == '1-800-555-0123'


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Simulate a CSV row with empty strings (like NO_INSURANCE row)
    csv_row = {
        'Id': 'b1c428d6-4f07-31e0-90f0-68ffa6ff8c76',
        'NAME': 'NO_INSURANCE',
        'ADDRESS': '',  # Empty string should become None
        'CITY': '',  # Empty string should become None
        'STATE_HEADQUARTERED': '',  # Empty string should become None
        'ZIP': '',  # Empty string should become None
        'PHONE': '',  # Empty string should become None
        'AMOUNT_COVERED': '0.00',
        'AMOUNT_UNCOVERED': '321243274.87',
        'REVENUE': '0.00',
        'COVERED_ENCOUNTERS': '0',
        'UNCOVERED_ENCOUNTERS': '35195',
        'COVERED_MEDICATIONS': '0',
        'UNCOVERED_MEDICATIONS': '13776',
        'COVERED_PROCEDURES': '0',
        'UNCOVERED_PROCEDURES': '53599',
        'COVERED_IMMUNIZATIONS': '0',
        'UNCOVERED_IMMUNIZATIONS': '6629',
        'UNIQUE_CUSTOMERS': '60',
        'QOLS_AVG': '1.9318087533676167',
        'MEMBER_MONTHS': '23664'
    }
    
    payer = Payer(**csv_row)
    
    assert payer.name == 'NO_INSURANCE'
    assert payer.address is None
    assert payer.city is None
    assert payer.state_headquartered is None
    assert payer.zip is None
    assert payer.phone is None
    assert payer.amount_covered == Decimal('0.00')
    assert payer.amount_uncovered == Decimal('321243274.87')
    assert payer.unique_customers == 60


def test_payer_model_config():
    """Test that the model configuration is working correctly."""
    # Test that str_strip_whitespace is working
    payer = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='   Test Payer   ',
        address='   123 Main Street   ',
        city='   Boston   ',
        amount_covered=Decimal('1000.00'),
        amount_uncovered=Decimal('100.00'),
        revenue=Decimal('2000.00'),
        covered_encounters=100,
        uncovered_encounters=0,
        covered_medications=50,
        uncovered_medications=0,
        covered_procedures=25,
        uncovered_procedures=0,
        covered_immunizations=10,
        uncovered_immunizations=0,
        unique_customers=75,
        qols_avg=0.8,
        member_months=900
    )
    
    assert payer.name == 'Test Payer'
    assert payer.address == '123 Main Street'
    assert payer.city == 'Boston'


def test_payer_equality():
    """Test Payer model equality comparison."""
    payer1 = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='Test Payer',
        amount_covered=Decimal('1000.00'),
        amount_uncovered=Decimal('100.00'),
        revenue=Decimal('2000.00'),
        covered_encounters=100,
        uncovered_encounters=0,
        covered_medications=50,
        uncovered_medications=0,
        covered_procedures=25,
        uncovered_procedures=0,
        covered_immunizations=10,
        uncovered_immunizations=0,
        unique_customers=75,
        qols_avg=0.8,
        member_months=900
    )
    
    payer2 = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='Test Payer',
        amount_covered=Decimal('1000.00'),
        amount_uncovered=Decimal('100.00'),
        revenue=Decimal('2000.00'),
        covered_encounters=100,
        uncovered_encounters=0,
        covered_medications=50,
        uncovered_medications=0,
        covered_procedures=25,
        uncovered_procedures=0,
        covered_immunizations=10,
        uncovered_immunizations=0,
        unique_customers=75,
        qols_avg=0.8,
        member_months=900
    )
    
    payer3 = Payer(
        id='b3221cfc-24fb-339e-823d-bc4136cbc4ed',
        name='Test Payer',
        amount_covered=Decimal('2000.00'),  # Different amount
        amount_uncovered=Decimal('100.00'),
        revenue=Decimal('2000.00'),
        covered_encounters=100,
        uncovered_encounters=0,
        covered_medications=50,
        uncovered_medications=0,
        covered_procedures=25,
        uncovered_procedures=0,
        covered_immunizations=10,
        uncovered_immunizations=0,
        unique_customers=75,
        qols_avg=0.8,
        member_months=900
    )
    
    assert payer1 == payer2
    assert payer1 != payer3


def test_no_insurance_payer():
    """Test the special NO_INSURANCE payer case."""
    csv_path = Path(__file__).parent / "data" / "csv" / "payers.csv"
    
    payers = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            payer = Payer(**row)
            payers.append(payer)
    
    # Find the NO_INSURANCE payer
    no_insurance = next((p for p in payers if p.name == 'NO_INSURANCE'), None)
    assert no_insurance is not None
    
    # Verify NO_INSURANCE characteristics
    assert no_insurance.name == 'NO_INSURANCE'
    assert no_insurance.address is None
    assert no_insurance.city is None
    assert no_insurance.state_headquartered is None
    assert no_insurance.zip is None
    assert no_insurance.phone is None
    assert no_insurance.amount_covered == Decimal('0.00')
    assert no_insurance.revenue == Decimal('0.00')
    assert no_insurance.covered_encounters == 0
    assert no_insurance.uncovered_encounters > 0  # Should have uncovered encounters
    assert no_insurance.amount_uncovered > 0  # Should have uncovered amounts 