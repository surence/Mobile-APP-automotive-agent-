"""
Pydantic models used throughout the application.
"""

from typing import Optional

from pydantic import BaseModel, Field


# ==========================================================
# Vehicle Request
# ==========================================================

class VehicleRequest(BaseModel):
    make: str = Field(..., min_length=2)
    model: str = Field(..., min_length=1)
    year: int = Field(..., ge=1980, le=2100)

    mileage: int = Field(..., ge=0)

    fuel_type: str = Field(
        default="Petrol"
    )

    transmission: str = Field(
        default="Automatic"
    )

    engine_size: Optional[str] = None

    symptom_category: str

    symptoms: str = Field(
        ...,
        min_length=10
    )

    obd_code: Optional[str] = None

    vin: Optional[str] = None

    service_history: Optional[str] = None

    accident_history: Optional[str] = None


# ==========================================================
# Tool Results
# ==========================================================

class ToolResults(BaseModel):
    diagnosis: str

    repair_cost: str

    maintenance: str

    obd_analysis: str


# ==========================================================
# Successful Response
# ==========================================================

class DiagnosisResponse(BaseModel):

    success: bool = True

    vehicle: VehicleRequest

    ai_diagnosis: str

    damage_analysis: Optional[str] = None

    tool_results: ToolResults

    confidence: int


# ==========================================================
# Error Response
# ==========================================================

class ErrorResponse(BaseModel):

    success: bool = False

    message: str