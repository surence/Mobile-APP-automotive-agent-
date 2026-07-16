"""
FastAPI API Routes
"""

from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.agent import agent
from app.config import (
    REPORT_FOLDER,
    UPLOAD_FOLDER,
)
from app.image_analyzer import image_analyzer
from app.models import VehicleRequest
from app.pdf_report import pdf_generator

router = APIRouter()


@router.get("/")
async def root():

    return {
        "success": True,
        "application": "AI Automotive Diagnostic Assistant",
        "version": "1.0.0",
        "status": "Running"
    }


@router.post("/diagnose")
async def diagnose_vehicle(vehicle: VehicleRequest):

    try:

        result = agent.diagnose(vehicle)

        result["vehicle"] = vehicle.model_dump()

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/analyze-image")
async def analyze_vehicle_image(
    image: UploadFile = File(...)
):

    try:

        suffix = Path(image.filename).suffix

        file_path = UPLOAD_FOLDER / f"vehicle{suffix}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                image.file,
                buffer,
            )

        analysis = image_analyzer.analyze_damage(
            str(file_path)
        )

        return {

            "success": True,

            "damage_analysis": analysis

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.post("/generate-report")
async def generate_report(
    vehicle: VehicleRequest
):

    try:

        result = agent.diagnose(vehicle)

        pdf = pdf_generator.generate(

            vehicle=vehicle,

            ai_diagnosis=result["ai_diagnosis"],

            tool_results=result["tool_results"],

            damage_analysis=result.get(
                "damage_analysis",
                "",
            ),

            confidence=result.get(
                "confidence",
                95,
            ),
        )

        return {

            "success": True,

            "report": pdf

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )