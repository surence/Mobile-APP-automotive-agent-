import os
import shutil
import uuid

from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from pydantic import BaseModel, Field

from langchain_groq import ChatGroq

from langchain.agents import create_agent

from tools import (
    diagnose_car_problem,
    repair_cost_estimator,
    obd_code_lookup,
    maintenance_schedule_generator
)

from image_analyzer import analyze_vehicle_damage
from pdf_report import generate_pdf_report


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found inside .env"
    )


# ==========================================================
# Create Upload Folder
# ==========================================================

from pathlib import Path

UPLOAD_FOLDER = Path("uploads")

if UPLOAD_FOLDER.exists():
    if not UPLOAD_FOLDER.is_dir():
        raise RuntimeError(
            "'uploads' exists but is a file. Delete or rename it."
        )
else:
    UPLOAD_FOLDER.mkdir(parents=True)


# ==========================================================
# FastAPI App
# ==========================================================

app = FastAPI(
    title="AI Automotive Diagnostic Assistant",
    version="1.0.0"
)


# ==========================================================
# Enable Flutter Access
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# Groq LLM
# ==========================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    api_key=GROQ_API_KEY
)


# ==========================================================
# LangChain Agent
# ==========================================================

agent = create_agent(
    model=llm,
    tools=[
        diagnose_car_problem,
        repair_cost_estimator,
        obd_code_lookup,
        maintenance_schedule_generator,
    ]
)


# ==========================================================
# Request Model
# ==========================================================

class VehicleRequest(BaseModel):

    make: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    model: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    year: str = Field(
        ...,
        pattern=r"^\d{4}$"
    )

    mileage: str = Field(
        ...,
        min_length=1
    )

    symptom_category: str = Field(
        ...,
        min_length=3
    )

    symptoms: str = Field(
        ...,
        min_length=10
    )

    obd_code: str = ""


# ==========================================================
# Health Check
# ==========================================================

@app.get("/")
def home():

    return {
        "message": "AI Automotive Diagnostic Assistant API Running"
    }


# ==========================================================
# Prompt Builder
# ==========================================================

def build_prompt(vehicle: VehicleRequest):

    prompt = f"""
You are an experienced Master Automotive Technician.

Analyse the customer's vehicle carefully.

Vehicle Information

Make:
{vehicle.make}

Model:
{vehicle.model}

Year:
{vehicle.year}

Mileage:
{vehicle.mileage}

Symptom Category:
{vehicle.symptom_category}

Customer Complaint:
{vehicle.symptoms}

OBD-II Code:
{vehicle.obd_code}

Provide a professional workshop report.

Include:

1. Possible Causes

2. Components Affected

3. Diagnostic Procedure

4. Recommended Repairs

5. Estimated Repair Cost

6. Safety Concerns

7. Maintenance Advice

Be detailed.

Respond professionally.
"""

    return prompt
# ==========================================================
# AI Diagnosis Endpoint
# ==========================================================

@app.post("/diagnose")
async def diagnose(vehicle: VehicleRequest):

    try:

        prompt = build_prompt(vehicle)

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        ai_response = response["messages"][-1].content

        # ------------------------------------
        # Tool Results
        # ------------------------------------

        diagnosis = diagnose_car_problem.invoke(
            {
                "symptoms": vehicle.symptoms
            }
        )

        repair_cost = repair_cost_estimator.invoke(
            {
                "problem": vehicle.symptoms
            }
        )

        maintenance = maintenance_schedule_generator.invoke(
            {
                "mileage": vehicle.mileage
            }
        )

        if vehicle.obd_code.strip() == "":
            obd_result = "No OBD-II fault code supplied."
        else:
            obd_result = obd_code_lookup.invoke(
                {
                    "code": vehicle.obd_code
                }
            )

        return {

            "success": True,

            "vehicle": {
                "make": vehicle.make,
                "model": vehicle.model,
                "year": vehicle.year
            },

            "ai_diagnosis": ai_response,

            "tool_results": {

                "diagnosis": diagnosis,

                "repair_cost": repair_cost,

                "maintenance": maintenance,

                "obd_analysis": obd_result

            }

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# PDF Report Endpoint
# ==========================================================

@app.post("/generate-report")
async def generate_report(vehicle: VehicleRequest):

    try:

        prompt = build_prompt(vehicle)

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        ai_response = response["messages"][-1].content

        diagnosis = diagnose_car_problem.invoke(
            {
                "symptoms": vehicle.symptoms
            }
        )

        repair_cost = repair_cost_estimator.invoke(
            {
                "problem": vehicle.symptoms
            }
        )

        maintenance = maintenance_schedule_generator.invoke(
            {
                "mileage": vehicle.mileage
            }
        )

        filename = f"{uuid.uuid4()}.pdf"

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        generate_pdf_report(

            filename=filepath,

            vehicle_make=vehicle.make,

            vehicle_model=vehicle.model,

            vehicle_year=vehicle.year,

            symptoms=vehicle.symptoms,

            diagnosis=ai_response,

            image_analysis="No vehicle image supplied.",

            repair_cost=repair_cost,

            maintenance=maintenance

        )

        return FileResponse(

            filepath,

            filename="diagnostic_report.pdf",

            media_type="application/pdf"

        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
    # ==========================================================
# Vehicle Image Analysis Endpoint
# ==========================================================

@app.post("/analyze-image")
async def analyze_image(

    make: str = Form(...),

    model: str = Form(...),

    year: str = Form(...),

    mileage: str = Form(...),

    symptom_category: str = Form(...),

    symptoms: str = Form(...),

    obd_code: str = Form(""),

    image: UploadFile = File(...)
):

    filepath = None

    try:

        extension = image.filename.split(".")[-1]

        filename = f"{uuid.uuid4()}.{extension}"

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        with open(filepath, "wb") as buffer:

            shutil.copyfileobj(
                image.file,
                buffer
            )

        image_report = analyze_vehicle_damage(
            filepath
        )

        vehicle = VehicleRequest(

            make=make,

            model=model,

            year=year,

            mileage=mileage,

            symptom_category=symptom_category,

            symptoms=symptoms,

            obd_code=obd_code

        )

        prompt = build_prompt(vehicle)

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        ai_response = response["messages"][-1].content

        diagnosis = diagnose_car_problem.invoke(
            {
                "symptoms": symptoms
            }
        )

        repair_cost = repair_cost_estimator.invoke(
            {
                "problem": symptoms
            }
        )

        maintenance = maintenance_schedule_generator.invoke(
            {
                "mileage": mileage
            }
        )

        if obd_code.strip():

            obd_result = obd_code_lookup.invoke(
                {
                    "code": obd_code
                }
            )

        else:

            obd_result = "No OBD-II code supplied."

        pdf_filename = f"{uuid.uuid4()}.pdf"

        pdf_path = os.path.join(
            UPLOAD_FOLDER,
            pdf_filename
        )

        generate_pdf_report(

            filename=pdf_path,

            vehicle_make=make,

            vehicle_model=model,

            vehicle_year=year,

            symptoms=symptoms,

            diagnosis=ai_response,

            image_analysis=image_report,

            repair_cost=repair_cost,

            maintenance=maintenance

        )

        return {

            "success": True,

            "vehicle": {

                "make": make,

                "model": model,

                "year": year

            },

            "ai_diagnosis": ai_response,

            "damage_analysis": image_report,

            "tool_results": {

                "diagnosis": diagnosis,

                "repair_cost": repair_cost,

                "maintenance": maintenance,

                "obd_analysis": obd_result

            },

            "pdf_report": f"/download-report/{pdf_filename}"

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if filepath and os.path.exists(filepath):

            os.remove(filepath)


# ==========================================================
# Download PDF
# ==========================================================

@app.get("/download-report/{filename}")
async def download_report(filename: str):

    path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if not os.path.exists(path):

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )

    return FileResponse(

        path,

        filename="diagnostic_report.pdf",

        media_type="application/pdf"

    )


# ==========================================================
# Startup Event
# ==========================================================

@app.on_event("startup")
async def startup_event():

    print("=" * 60)
    print(" AI Automotive Diagnostic Assistant Started")
    print("=" * 60)
    print("Groq Model : llama-3.3-70b-versatile")
    print("Gemini Vision : Enabled")
    print("FastAPI : Running")
    print("=" * 60)