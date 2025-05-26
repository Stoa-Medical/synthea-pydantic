"""Pydantic models for Synthea claims_transactions CSV format."""

from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClaimTransaction(BaseModel):
    """Model representing a single claim transaction record from Synthea CSV output."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: UUID = Field(description="Primary Key. Unique Identifier of the claim transaction")
    claimid: UUID = Field(description="Foreign key to the Claim")
    chargeid: int = Field(description="Charge ID")
    patientid: UUID = Field(description="Foreign key to the Patient")
    type: Literal["CHARGE", "PAYMENT", "ADJUSTMENT", "TRANSFERIN", "TRANSFEROUT"] = Field(
        description="CHARGE: original line item. PAYMENT: payment made against a charge by an insurance company (aka Payer) or patient. ADJUSTMENT: change in the charge without a payment, made by an insurance company. TRANSFERIN and TRANSFEROUT: transfer of the balance from one insurance company to another, or to a patient"
    )
    amount: Optional[Decimal] = Field(None, description="Dollar amount for a CHARGE or TRANSFERIN")
    method: Optional[Literal["CASH", "CHECK", "ECHECK", "COPAY", "SYSTEM", "CC"]] = Field(
        None, description="Payment made by CASH, CHECK, ECHECK, COPAY, SYSTEM (adjustments without payment), or CC (credit card)"
    )
    fromdate: Optional[datetime] = Field(None, description="Transaction start date")
    todate: Optional[datetime] = Field(None, description="Transaction end date")
    placeofservice: UUID = Field(description="Foreign key to the Organization")
    procedurecode: str = Field(description="SNOMED-CT or other code (e.g. CVX for Vaccines) for the service")
    modifier1: Optional[str] = Field(None, description="Unused. Modifier on procedure code")
    modifier2: Optional[str] = Field(None, description="Unused. Modifier on procedure code")
    diagnosisref1: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8]] = Field(
        None, description="Number indicating which diagnosis code from the claim applies to this transaction, 1-8 are valid options"
    )
    diagnosisref2: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8]] = Field(
        None, description="Number indicating which diagnosis code from the claim applies to this transaction, 1-8 are valid options"
    )
    diagnosisref3: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8]] = Field(
        None, description="Number indicating which diagnosis code from the claim applies to this transaction, 1-8 are valid options"
    )
    diagnosisref4: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8]] = Field(
        None, description="Number indicating which diagnosis code from the claim applies to this transaction, 1-8 are valid options"
    )
    units: Optional[int] = Field(None, description="Number of units of the service")
    departmentid: Optional[int] = Field(None, description="Placeholder for department")
    notes: Optional[str] = Field(None, description="Description of the service or transaction")
    unitamount: Optional[Decimal] = Field(None, description="Cost per unit")
    transferoutid: Optional[int] = Field(None, description="If the transaction is a TRANSFERIN, the Charge ID of the corresponding TRANSFEROUT row")
    transfertype: Optional[Literal["1", "2", "p"]] = Field(
        None, description="1 if transferred to the primary insurance, 2 if transferred to the secondary insurance, or p if transferred to the patient"
    )
    payments: Optional[Decimal] = Field(None, description="Dollar amount of a payment for a PAYMENT row")
    adjustments: Optional[Decimal] = Field(None, description="Dollar amount of an adjustment for an ADJUSTMENTS row")
    transfers: Optional[Decimal] = Field(None, description="Dollar amount of a transfer for a TRANSFERIN or TRANSFEROUT row")
    outstanding: Optional[Decimal] = Field(None, description="Dollar amount left unpaid after this transaction was applied")
    appointmentid: Optional[UUID] = Field(None, description="Foreign key to the Encounter")
    linenote: Optional[str] = Field(None, description="Note")
    patientinsuranceid: Optional[UUID] = Field(None, description="Foreign key to the Payer Transitions table member ID")
    feescheduleid: Optional[int] = Field(None, description="Fixed to 1")
    providerid: UUID = Field(description="Foreign key to the Provider")
    supervisingproviderid: Optional[UUID] = Field(None, description="Foreign key to the supervising Provider")