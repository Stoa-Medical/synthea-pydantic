"""Tests for the devices module."""

import csv
from datetime import datetime
from pathlib import Path
from uuid import UUID

import pytest

from synthea_pydantic.devices import Device


def test_load_devices_csv():
    """Test loading devices from CSV file."""
    csv_path = Path(__file__).parent / "data" / "csv" / "devices.csv"
    
    devices = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            device = Device(**row)
            devices.append(device)
    
    # Verify we loaded some data
    assert len(devices) > 0
    
    # Check the first device
    first = devices[0]
    assert isinstance(first.start, datetime)
    assert first.stop is None or isinstance(first.stop, datetime)
    assert isinstance(first.patient, UUID)
    assert isinstance(first.encounter, UUID)
    assert isinstance(first.code, str)
    assert isinstance(first.description, str)
    assert isinstance(first.udi, str)


def test_device_serialization():
    """Test serializing Device models."""
    csv_path = Path(__file__).parent / "data" / "csv" / "devices.csv"
    
    devices = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            device = Device(**row)
            devices.append(device)
    
    # Test model_dump() for all devices
    for device in devices:
        data = device.model_dump()
        assert isinstance(data, dict)
        assert 'start' in data
        assert 'patient' in data
        assert 'encounter' in data
        assert 'code' in data
        assert 'description' in data
        assert 'udi' in data
    
    # Test model_dump_json() for all devices
    for device in devices:
        json_str = device.model_dump_json()
        assert isinstance(json_str, str)
        assert '"start"' in json_str
        assert '"patient"' in json_str
        assert '"encounter"' in json_str
        assert '"code"' in json_str
        assert '"udi"' in json_str
    
    # Test round-trip serialization
    first_device = devices[0]
    json_data = first_device.model_dump_json()
    restored = Device.model_validate_json(json_data)
    assert restored == first_device


def test_device_field_validation():
    """Test field validation for Device model."""
    # Test with minimal required fields using lowercase names
    device = Device(
        start='2020-01-01T10:00:00',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='360030002',
        description='Insulin delivery device',
        udi='(01)00844588003288(17)141120(10)7654321D(21)10987654'
    )
    assert device.start == datetime(2020, 1, 1, 10, 0, 0)
    assert device.stop is None
    
    # Test with all fields
    device_full = Device(
        start='2020-01-01T10:00:00',
        stop='2021-01-01T10:00:00',
        patient='b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        encounter='01efcc52-15d6-51e9-faa2-bee069fcbe44',
        code='360030002',
        description='Insulin delivery device',
        udi='(01)00844588003288(17)141120(10)7654321D(21)10987654'
    )
    assert device_full.stop == datetime(2021, 1, 1, 10, 0, 0)


def test_csv_direct_loading():
    """Test that CSV rows can be loaded directly with Device(**row)."""
    csv_path = Path(__file__).parent / "data" / "csv" / "devices.csv"
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        
        # This should work directly now
        device = Device(**row)
        
        # Verify it loaded correctly
        assert isinstance(device.start, datetime)
        assert isinstance(device.patient, UUID)
        assert isinstance(device.encounter, UUID)
        assert isinstance(device.code, str)
        assert isinstance(device.description, str)
        assert isinstance(device.udi, str)


def test_empty_string_handling():
    """Test that empty strings in CSV are converted to None."""
    # Simulate a CSV row with empty strings
    csv_row = {
        'START': '2020-01-01T10:00:00',
        'STOP': '',  # Empty string should become None
        'PATIENT': 'b9c610cd-28a6-4636-ccb6-c7a0d2a4cb85',
        'ENCOUNTER': '01efcc52-15d6-51e9-faa2-bee069fcbe44',
        'CODE': '360030002',
        'DESCRIPTION': 'Insulin delivery device',
        'UDI': '(01)00844588003288(17)141120(10)7654321D(21)10987654'
    }
    
    device = Device(**csv_row)
    
    assert device.stop is None