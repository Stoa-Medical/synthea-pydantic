"""Shared test configuration and fixtures for synthea-pydantic tests."""

import csv
from pathlib import Path

import pytest

from synthea_pydantic import (
    Allergy,
    CarePlan,
    Claim,
    ClaimTransaction,
    Condition,
    Device,
    Encounter,
    ImagingStudy,
    Immunization,
    Medication,
    Observation,
    Organization,
    Patient,
    PayerTransition,
    Payer,
    Procedure,
    Provider,
    Supply,
)

# All models to test generically
ALL_MODELS = [
    (Allergy, "allergies"),
    (CarePlan, "careplans"),
    (Claim, "claims"),
    (ClaimTransaction, "claims_transactions"),
    (Condition, "conditions"),
    (Device, "devices"),
    (Encounter, "encounters"),
    (ImagingStudy, "imaging_studies"),
    (Immunization, "immunizations"),
    (Medication, "medications"),
    (Observation, "observations"),
    (Organization, "organizations"),
    (Patient, "patients"),
    (PayerTransition, "payer_transitions"),
    (Payer, "payers"),
    (Procedure, "procedures"),
    (Provider, "providers"),
    (Supply, "supplies"),
]


@pytest.fixture(params=ALL_MODELS, ids=lambda x: x[1])
def model_and_csv(request):
    """Fixture that yields each model class and its CSV name."""
    model_class, csv_name = request.param
    csv_path = Path(__file__).parent / "data" / "csv" / f"{csv_name}.csv"
    
    if not csv_path.exists():
        pytest.skip(f"CSV file {csv_path} not found")
    
    return model_class, csv_name, csv_path


@pytest.fixture
def csv_data(model_and_csv):
    """Fixture that loads CSV data for a model."""
    model_class, csv_name, csv_path = model_and_csv
    
    models = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            model = model_class(**row)
            models.append(model)
    
    if not models:
        pytest.skip(f"No data in {csv_path}")
    
    return models


@pytest.fixture
def first_csv_row(model_and_csv):
    """Fixture that yields the first row of CSV data."""
    model_class, csv_name, csv_path = model_and_csv
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader, None)
        
        if row is None:
            pytest.skip(f"No data in {csv_path}")
        
        return model_class, row