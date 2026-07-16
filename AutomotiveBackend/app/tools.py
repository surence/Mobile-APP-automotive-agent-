"""
AI Automotive Diagnostic Tools
Compatible with LangChain 1.3.11
"""

from langchain_core.tools import tool


# ==========================================================
# Car Diagnosis Tool
# ==========================================================

@tool
def diagnose_vehicle(
    make: str,
    model: str,
    year: int,
    symptoms: str
) -> str:
    """
    Diagnose a vehicle problem from symptoms.
    """

    symptoms = symptoms.lower()

    if "overheat" in symptoms:
        return (
            "Possible causes:\n"
            "- Low coolant\n"
            "- Faulty thermostat\n"
            "- Failed water pump\n"
            "- Cooling fan failure"
        )

    if "engine" in symptoms and "shake" in symptoms:
        return (
            "Possible causes:\n"
            "- Misfiring cylinder\n"
            "- Worn spark plugs\n"
            "- Faulty ignition coil\n"
            "- Vacuum leak"
        )

    if "brake" in symptoms:
        return (
            "Possible causes:\n"
            "- Worn brake pads\n"
            "- Warped brake discs\n"
            "- Brake fluid issue"
        )

    if "battery" in symptoms:
        return (
            "Possible causes:\n"
            "- Weak battery\n"
            "- Faulty alternator\n"
            "- Loose battery terminals"
        )

    return (
        f"No specific diagnosis found for "
        f"{year} {make} {model}. "
        f"A complete inspection is recommended."
    )


# ==========================================================
# Repair Cost Estimator
# ==========================================================

@tool
def estimate_repair_cost(symptom_category: str) -> str:
    """
    Estimate repair cost.
    """

    prices = {

        "Engine":
            "Estimated cost: R4,500 - R18,000",

        "Transmission":
            "Estimated cost: R8,000 - R35,000",

        "Brakes":
            "Estimated cost: R1,500 - R6,000",

        "Battery":
            "Estimated cost: R1,200 - R3,500",

        "Suspension":
            "Estimated cost: R2,000 - R12,000",

        "Electrical":
            "Estimated cost: R900 - R8,000",

        "Cooling":
            "Estimated cost: R1,800 - R7,000"

    }

    return prices.get(

        symptom_category,

        "Repair cost requires inspection."

    )


# ==========================================================
# OBD-II Analyzer
# ==========================================================

@tool
def analyze_obd_code(
    obd_code: str
) -> str:
    """
    Analyze OBD-II fault code.
    """

    if not obd_code:
        return "No OBD-II code supplied."

    obd = obd_code.upper()

    codes = {

        "P0300":
            "Random cylinder misfire detected.",

        "P0301":
            "Cylinder 1 misfire detected.",

        "P0420":
            "Catalytic converter efficiency below threshold.",

        "P0171":
            "System too lean (Bank 1).",

        "P0128":
            "Coolant temperature below thermostat regulating temperature.",

        "P0455":
            "Large EVAP system leak detected."

    }

    return codes.get(

        obd,

        "Unknown OBD-II code. Manufacturer documentation required."

    )


# ==========================================================
# Maintenance Tool
# ==========================================================

@tool
def maintenance_schedule(
    mileage: int
) -> str:
    """
    Recommend maintenance based on mileage.
    """

    if mileage < 10000:

        return (
            "Next service:\n"
            "- Engine oil\n"
            "- Oil filter\n"
            "- General inspection"
        )

    elif mileage < 30000:

        return (
            "Recommended:\n"
            "- Oil service\n"
            "- Air filter\n"
            "- Cabin filter\n"
            "- Brake inspection"
        )

    elif mileage < 60000:

        return (
            "Recommended:\n"
            "- Spark plugs\n"
            "- Transmission fluid\n"
            "- Coolant\n"
            "- Brake fluid"
        )

    elif mileage < 100000:

        return (
            "Recommended:\n"
            "- Timing belt inspection\n"
            "- Suspension inspection\n"
            "- Full diagnostic scan"
        )

    else:

        return (
            "High mileage vehicle.\n"
            "Complete inspection recommended."
        )


# ==========================================================
# Export Tools
# ==========================================================

TOOLS = [

    diagnose_vehicle,

    estimate_repair_cost,

    analyze_obd_code,

    maintenance_schedule

]