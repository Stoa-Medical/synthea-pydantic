"""Tests for the procedures module."""

import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.procedures import Procedure


def test_load_procedures_csv():
    """Test loading procedures from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "procedures.csv"
    
    procedures = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 100:  # Test first 100 rows for performance
                break
            procedure = Procedure(**row)
            procedures.append(procedure)
    
    # Verify we loaded some data
    assert len(procedures) > 0
    
    # Check the first procedure
    first = procedures[0]
    assert isinstance(first.start, datetime)
    assert first.stop is None or isinstance(first.stop, datetime)
    assert isinstance(first.patient, UUID)
    assert isinstance(first.encounter, UUID)
    assert isinstance(first.code, str)
    assert isinstance(first.description, str)
    assert isinstance(first.base_cost, Decimal)
    assert first.reasoncode is None or isinstance(first.reasoncode, str)
    assert first.reasondescription is None or isinstance(first.reasondescription, str)


def test_procedure_serialization():
    """Test serializing Procedure models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "procedures.csv"
    
    procedures = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 10:  # Test first 10 rows for performance
                break
            procedure = Procedure(**row)
            procedures.append(procedure)
    
    # Test model_dump() for all procedures
    for procedure in procedures:
        data = procedure.model_dump()
        assert isinstance(data, dict)
        assert 'start' in data
        assert 'stop' in data
        assert 'patient' in data
        assert 'encounter' in data
        assert 'code' in data
        assert 'description' in data
        assert 'base_cost' in data
        assert 'reasoncode' in data
        assert 'reasondescription' in data
    
    # Test model_dump_json() for all procedures
    for procedure in procedures:
        json_str = procedure.model_dump_json()
        assert isinstance(json_str, str)
        assert '"start"' in json_str
        assert '"patient"' in json_str
        assert '"encounter"' in json_str
        assert '"code"' in json_str
        assert '"description"' in json_str
        assert '"base_cost"' in json_str
    
    # Test round-trip serialization
    first_procedure = procedures[0]
    json_data = first_procedure.model_dump_json()
    restored = Procedure.model_validate_json(json_data)
    assert restored == first_procedure


def test_procedure_field_validation():
    """Test field validation for Procedure model."""
    # Test with all fields using lowercase names
    procedure = Procedure(
        start='2023-01-15T10:30:00Z',
        stop='2023-01-15T11:00:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Medication Reconciliation (procedure)',
        base_cost=Decimal('608.11'),
        reasoncode='195967001',
        reasondescription='Asthma'
    )
    assert isinstance(procedure.start, datetime)
    assert isinstance(procedure.stop, datetime)
    assert procedure.patient == UUID('b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85')
    assert procedure.encounter == UUID('748f8357-6cc7-551d-f31a-32fa2cf84126')
    assert procedure.code == '430193006'
    assert procedure.description == 'Medication Reconciliation (procedure)'
    assert procedure.base_cost == Decimal('608.11')
    assert procedure.reasoncode == '195967001'
    assert procedure.reasondescription == 'Asthma'
    
    # Test with minimal required fields (optional fields as None)
    procedure_minimal = Procedure(
        start='2023-01-15T10:30:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Medication Reconciliation (procedure)',
        base_cost=Decimal('608.11')
    )
    assert procedure_minimal.stop is None
    assert procedure_minimal.reasoncode is None
    assert procedure_minimal.reasondescription is None


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with Procedure(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "procedures.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        procedure = Procedure(**row)
        
        # Verify it loaded correctly
        assert isinstance(procedure.start, datetime)
        assert isinstance(procedure.patient, UUID)
        assert isinstance(procedure.encounter, UUID)
        assert isinstance(procedure.code, str)
        assert isinstance(procedure.description, str)
        assert isinstance(procedure.base_cost, Decimal)


def test_procedure_codes_validation():
    """Test that different procedure codes are handled correctly."""
    csv_path = Path(__file__).parent / "data" / "csv" / "procedures.csv"
    
    procedures = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 50:  # Test first 50 rows for performance
                break
            procedure = Procedure(**row)
            procedures.append(procedure)
    
    # Verify we have different procedure codes
    procedure_codes = {proc.code for proc in procedures}
    
    # Should have multiple different procedure codes
    assert len(procedure_codes) > 1
    
    # All codes should be non-empty strings
    for code in procedure_codes:
        assert isinstance(code, str)
        assert len(code.strip()) > 0


def test_datetime_validation():
    """Test datetime field validation for start and stop times."""
    # Test with valid datetime strings
    procedure = Procedure(
        start='2023-01-15T10:30:00Z',
        stop='2023-01-15T11:00:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Test Procedure',
        base_cost=Decimal('500.00')
    )
    assert isinstance(procedure.start, datetime)
    assert isinstance(procedure.stop, datetime)
    assert procedure.stop > procedure.start  # Stop should be after start
    
    # Test with None stop time
    procedure_no_stop = Procedure(
        start='2023-01-15T10:30:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Test Procedure',
        base_cost=Decimal('500.00')
    )
    assert procedure_no_stop.stop is None
    
    # Test with datetime objects
    start_dt = datetime(2023, 1, 15, 10, 30, 0)
    stop_dt = datetime(2023, 1, 15, 11, 0, 0)
    procedure_dt = Procedure(
        start=start_dt,
        stop=stop_dt,
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Test Procedure',
        base_cost=Decimal('500.00')
    )
    assert procedure_dt.start == start_dt
    assert procedure_dt.stop == stop_dt


def test_decimal_field_validation():
    """Test decimal field validation for base_cost amounts."""
    # Test with valid decimal amounts
    procedure = Procedure(
        start='2023-01-15T10:30:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Test Procedure',
        base_cost=Decimal('1234.56')
    )
    assert procedure.base_cost == Decimal('1234.56')
    
    # Test with zero cost
    procedure_zero = Procedure(
        start='2023-01-15T10:30:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Free Procedure',
        base_cost=Decimal('0.00')
    )
    assert procedure_zero.base_cost == Decimal('0.00')
    
    # Test with high cost
    procedure_expensive = Procedure(
        start='2023-01-15T10:30:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Expensive Procedure',
        base_cost=Decimal('99999.99')
    )
    assert procedure_expensive.base_cost == Decimal('99999.99')


def test_uuid_validation():
    """Test UUID field validation for patient and encounter."""
    # Test with string UUIDs
    procedure = Procedure(
        start='2023-01-15T10:30:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Test Procedure',
        base_cost=Decimal('500.00')
    )
    assert isinstance(procedure.patient, UUID)
    assert isinstance(procedure.encounter, UUID)
    
    # Test with UUID objects
    patient_id = UUID('b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85')
    encounter_id = UUID('748f8357-6cc7-551d-f31a-32fa2cf84126')
    procedure_uuid_obj = Procedure(
        start='2023-01-15T10:30:00Z',
        patient=patient_id,
        encounter=encounter_id,
        code='430193006',
        description='Test Procedure',
        base_cost=Decimal('500.00')
    )
    assert procedure_uuid_obj.patient == patient_id
    assert procedure_uuid_obj.encounter == encounter_id


def test_string_field_validation():
    """Test string field validation and whitespace handling."""
    # Test with extra whitespace
    procedure = Procedure(
        start='2023-01-15T10:30:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='  430193006  ',  # Extra whitespace
        description='  Test Procedure  ',  # Extra whitespace
        base_cost=Decimal('500.00'),
        reasoncode='  195967001  ',  # Extra whitespace
        reasondescription='  Test Reason  '  # Extra whitespace
    )
    # Whitespace should be stripped due to str_strip_whitespace=True
    assert procedure.code == '430193006'
    assert procedure.description == 'Test Procedure'
    assert procedure.reasoncode == '195967001'
    assert procedure.reasondescription == 'Test Reason'


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Simulate a CSV row with empty strings
    csv_row = {
        'START': '2023-01-15T10:30:00Z',
        'STOP': '',  # Empty string should become None
        'PATIENT': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'ENCOUNTER': '748f8357-6cc7-551d-f31a-32fa2cf84126',
        'CODE': '430193006',
        'DESCRIPTION': 'Test Procedure',
        'BASE_COST': '500.00',
        'REASONCODE': '',  # Empty string should become None
        'REASONDESCRIPTION': ''  # Empty string should become None
    }
    
    procedure = Procedure(**csv_row)
    
    assert isinstance(procedure.start, datetime)
    assert procedure.stop is None  # Empty string converted to None
    assert procedure.code == '430193006'
    assert procedure.description == 'Test Procedure'
    assert procedure.base_cost == Decimal('500.00')
    assert procedure.reasoncode is None  # Empty string converted to None
    assert procedure.reasondescription is None  # Empty string converted to None


def test_reason_code_validation():
    """Test reason code and description field validation."""
    # Test with reason code and description
    procedure = Procedure(
        start='2023-01-15T10:30:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Test Procedure',
        base_cost=Decimal('500.00'),
        reasoncode='195967001',
        reasondescription='Asthma'
    )
    assert procedure.reasoncode == '195967001'
    assert procedure.reasondescription == 'Asthma'
    
    # Test with None reason fields
    procedure_no_reason = Procedure(
        start='2023-01-15T10:30:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Test Procedure',
        base_cost=Decimal('500.00')
    )
    assert procedure_no_reason.reasoncode is None
    assert procedure_no_reason.reasondescription is None


def test_procedure_model_config():
    """Test that the model configuration is working correctly."""
    # Test that str_strip_whitespace is working
    procedure = Procedure(
        start='2023-01-15T10:30:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='   430193006   ',
        description='   Test Procedure   ',
        base_cost=Decimal('500.00')
    )
    
    assert procedure.code == '430193006'
    assert procedure.description == 'Test Procedure'


def test_procedure_equality():
    """Test Procedure model equality comparison."""
    procedure1 = Procedure(
        start='2023-01-15T10:30:00Z',
        stop='2023-01-15T11:00:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Test Procedure',
        base_cost=Decimal('500.00'),
        reasoncode='195967001',
        reasondescription='Asthma'
    )
    
    procedure2 = Procedure(
        start='2023-01-15T10:30:00Z',
        stop='2023-01-15T11:00:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Test Procedure',
        base_cost=Decimal('500.00'),
        reasoncode='195967001',
        reasondescription='Asthma'
    )
    
    procedure3 = Procedure(
        start='2023-01-15T10:30:00Z',
        stop='2023-01-15T11:00:00Z',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='748f8357-6cc7-551d-f31a-32fa2cf84126',
        code='430193006',
        description='Test Procedure',
        base_cost=Decimal('1000.00'),  # Different cost
        reasoncode='195967001',
        reasondescription='Asthma'
    )
    
    assert procedure1 == procedure2
    assert procedure1 != procedure3


def test_medication_reconciliation_procedures():
    """Test medication reconciliation procedures (common in the data)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "procedures.csv"
    
    procedures = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 100:  # Test first 100 rows for performance
                break
            procedure = Procedure(**row)
            procedures.append(procedure)
    
    # Find medication reconciliation procedures
    med_recon_procedures = [
        proc for proc in procedures 
        if 'Medication Reconciliation' in proc.description
    ]
    
    # Should have some medication reconciliation procedures in the data
    if med_recon_procedures:
        # Verify they have the expected code
        for proc in med_recon_procedures:
            assert proc.code == '430193006'
            assert 'Medication Reconciliation' in proc.description
            assert isinstance(proc.base_cost, Decimal)
            assert proc.base_cost > 0


def test_procedure_cost_distribution():
    """Test the distribution of procedure costs."""
    csv_path = Path(__file__).parent / "data" / "csv" / "procedures.csv"
    
    procedures = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 100:  # Test first 100 rows for performance
                break
            procedure = Procedure(**row)
            procedures.append(procedure)
    
    # Verify cost distribution
    costs = [proc.base_cost for proc in procedures]
    
    # Should have various costs
    assert len(set(costs)) > 1
    
    # All costs should be non-negative
    for cost in costs:
        assert cost >= 0
    
    # Calculate basic statistics
    min_cost = min(costs)
    max_cost = max(costs)
    avg_cost = sum(costs) / len(costs)
    
    assert isinstance(min_cost, Decimal)
    assert isinstance(max_cost, Decimal)
    assert isinstance(avg_cost, Decimal)
    assert min_cost <= avg_cost <= max_cost


def test_procedure_timing_validation():
    """Test that procedure timing makes sense."""
    csv_path = Path(__file__).parent / "data" / "csv" / "procedures.csv"
    
    procedures = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 50:  # Test first 50 rows for performance
                break
            procedure = Procedure(**row)
            procedures.append(procedure)
    
    # Verify timing relationships
    for proc in procedures:
        assert isinstance(proc.start, datetime)
        
        # If stop time exists, it should be after start time
        if proc.stop is not None:
            assert isinstance(proc.stop, datetime)
            assert proc.stop >= proc.start
        
        # Start time should be reasonable (not too far in past/future)
        assert proc.start.year >= 1900
        assert proc.start.year <= 2030


def test_procedure_description_completeness():
    """Test that procedures have complete description information."""
    csv_path = Path(__file__).parent / "data" / "csv" / "procedures.csv"
    
    procedures = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 20:  # Test first 20 procedures
                break
            procedure = Procedure(**row)
            procedures.append(procedure)
    
    # Verify all procedures have required fields
    for proc in procedures:
        assert proc.code is not None and len(proc.code.strip()) > 0
        assert proc.description is not None and len(proc.description.strip()) > 0
        assert isinstance(proc.base_cost, Decimal)
        
        # If reason fields are present, they should be non-empty
        if proc.reasoncode is not None:
            assert len(proc.reasoncode.strip()) > 0
        if proc.reasondescription is not None:
            assert len(proc.reasondescription.strip()) > 0 