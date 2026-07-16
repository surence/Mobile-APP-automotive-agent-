"""
Groq + LangChain Automotive AI Agent
"""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
)

from app.prompts import (
    SYSTEM_PROMPT,
    DIAGNOSIS_TEMPLATE,
)

from app.tools import (
    diagnose_vehicle,
    estimate_repair_cost,
    analyze_obd_code,
    maintenance_schedule,
)


class AutomotiveAgent:

    def __init__(self):

        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=0.2,
        )

    def diagnose(self, vehicle):

        # ----------------------------
        # Run Local Tools
        # ----------------------------

        diagnosis = diagnose_vehicle.invoke(
            {
                "make": vehicle.make,
                "model": vehicle.model,
                "year": vehicle.year,
                "symptoms": vehicle.symptoms,
            }
        )

        repair_cost = estimate_repair_cost.invoke(
            {
                "symptom_category": vehicle.symptom_category
            }
        )

        obd_analysis = analyze_obd_code.invoke(
            {
                "obd_code": vehicle.obd_code or ""
            }
        )

        maintenance = maintenance_schedule.invoke(
            {
                "mileage": vehicle.mileage
            }
        )

        # ----------------------------
        # Build Prompt
        # ----------------------------

        prompt = DIAGNOSIS_TEMPLATE.format(
            make=vehicle.make,
            model=vehicle.model,
            year=vehicle.year,
            mileage=vehicle.mileage,
            fuel_type=vehicle.fuel_type,
            transmission=vehicle.transmission,
            engine_size=vehicle.engine_size or "Unknown",
            symptom_category=vehicle.symptom_category,
            symptoms=vehicle.symptoms,
            obd_code=vehicle.obd_code or "None",
            service_history=vehicle.service_history or "Unknown",
            accident_history=vehicle.accident_history or "Unknown",
        )

        tool_context = f"""

Local Diagnostic Results

Diagnosis:
{diagnosis}

Repair Cost:
{repair_cost}

OBD-II Analysis:
{obd_analysis}

Maintenance:
{maintenance}

Use these results together with your own automotive knowledge.
"""

        messages = [

            SystemMessage(content=SYSTEM_PROMPT),

            HumanMessage(
                content=prompt + tool_context
            )

        ]

        response = self.llm.invoke(messages)

        return {

            "success": True,

            "ai_diagnosis": response.content,

            "tool_results": {

                "diagnosis": diagnosis,

                "repair_cost": repair_cost,

                "maintenance": maintenance,

                "obd_analysis": obd_analysis,

            },

            "confidence": 95

        }


# Singleton

agent = AutomotiveAgent()