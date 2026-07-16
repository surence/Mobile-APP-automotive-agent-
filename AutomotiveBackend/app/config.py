"""
Application configuration.
Loads environment variables from the .env file.
"""

from pathlib import Path

from dotenv import load_dotenv
import os

# --------------------------------------------------
# Base Directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# Application
# --------------------------------------------------

APP_NAME = os.getenv(
    "APP_NAME",
    "AI Automotive Diagnostic Assistant",
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0",
)

# --------------------------------------------------
# API Keys
# --------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# --------------------------------------------------
# Models
# --------------------------------------------------

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
)

# --------------------------------------------------
# Storage
# --------------------------------------------------

UPLOAD_FOLDER = BASE_DIR / os.getenv(
    "UPLOAD_FOLDER",
    "uploads",
)

REPORT_FOLDER = BASE_DIR / os.getenv(
    "REPORT_FOLDER",
    "reports",
)

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True,
)

REPORT_FOLDER.mkdir(
    parents=True,
    exist_ok=True,
)

# --------------------------------------------------
# Validation
# --------------------------------------------------

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing in the .env file."
    )

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing in the .env file."
    )