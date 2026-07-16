from langchain_core.tools import tool


@tool
def diagnose_car_problem(symptoms: str) -> str:
    """
    Diagnose vehicle problems based on symptoms.
    """

    symptoms = symptoms.lower()

    diagnosis = {
        "won't start": """
Possible Causes
• Dead battery
• Faulty starter motor
• Weak alternator
• Fuel pump failure

Recommended Checks
• Battery voltage
• Starter relay
• Fuel pressure
""",
        "overheating": """
Possible Causes
• Low coolant
• Faulty thermostat
• Water pump failure
• Radiator blockage

Recommended Checks
• Coolant level
• Radiator fan
• Thermostat
""",
        "brake": """
Possible Causes
• Worn brake pads
• Damaged brake discs
• Brake fluid leak

Recommended Checks
• Brake pads
• Rotors
• Brake fluid
""",
        "smoke": """
Possible Causes
• Blown head gasket
• Oil leak
• Turbo failure
• Coolant leak
"""
    }

    for key, value in diagnosis.items():
        if key in symptoms:
            return value

    return """
No exact match found.

Recommended Inspection

• Engine
• Battery
• Electrical System
• Fluids
• Sensors
"""


@tool
def repair_cost_estimator(problem: str) -> str:
    """
    Estimate repair costs.
    """

    estimates = {
        "battery": "Estimated Cost: R1,500 - R3,500",
        "starter": "Estimated Cost: R2,500 - R7,500",
        "alternator": "Estimated Cost: R3,000 - R8,000",
        "thermostat": "Estimated Cost: R800 - R2,500",
        "radiator": "Estimated Cost: R3,500 - R12,000",
        "head gasket": "Estimated Cost: R8,000 - R25,000",
        "brake": "Estimated Cost: R1,500 - R6,000"
    }

    problem = problem.lower()

    for key, value in estimates.items():
        if key in problem:
            return value

    return "Cost requires workshop inspection."


@tool
def obd_code_lookup(code: str) -> str:
    """
    Lookup OBD-II codes.
    """

    database = {

        "P0300": "Random Engine Misfire Detected",

        "P0171": "Fuel System Too Lean",

        "P0420": "Catalytic Converter Efficiency Below Threshold",

        "P0128": "Coolant Thermostat Below Regulating Temperature",

        "P0500": "Vehicle Speed Sensor Malfunction",

        "P0113": "Intake Air Temperature Sensor High Input"

    }

    return database.get(
        code.upper(),
        "Unknown OBD-II fault code."
    )


@tool
def maintenance_schedule_generator(mileage: str) -> str:
    """
    Generate maintenance schedule.
    """

    try:

        mileage = int(mileage)

        if mileage < 10000:

            return """
Maintenance Due

• Engine oil inspection

• Tyre inspection

• Brake inspection
"""

        elif mileage < 50000:

            return """
Maintenance Due

• Engine oil change

• Air filter replacement

• Brake inspection

• Tyre rotation
"""

        else:

            return """
Maintenance Due

• Spark plug replacement

• Coolant flush

• Transmission service

• Brake service

• Engine oil change
"""

    except Exception:

        return "Invalid mileage."


@tool
def vehicle_information(make: str, model: str, year: str) -> str:
    """
    Vehicle details.
    """

    return f"""
Vehicle Details

Make : {make}

Model : {model}

Year : {year}
"""