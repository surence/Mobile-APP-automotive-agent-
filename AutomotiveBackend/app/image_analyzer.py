"""
Vehicle Image Analyzer using Google Gen AI SDK
Compatible with google-genai 1.30+
"""

from pathlib import Path

from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)

# --------------------------------------------------
# Configure Gemini Client
# --------------------------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


class ImageAnalyzer:

    def analyze_damage(
        self,
        image_path: str,
    ) -> str:
        """
        Analyse a vehicle image and identify visible damage.
        """

        try:

            image_file = Path(image_path)

            if not image_file.exists():
                return "Image not found."

            image_bytes = image_file.read_bytes()

            prompt = """
You are an experienced automotive damage assessor.

Analyse this vehicle image.

Provide:

1. Visible damage
2. Damaged components
3. Severity (Minor / Moderate / Severe)
4. Is the vehicle safe to drive?
5. Recommended repairs
6. Estimated repair cost (South African Rand)
7. Additional observations

Be concise and professional.
"""

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[
                    prompt,
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg",
                    ),
                ],
            )

            return response.text

        except Exception as e:

            return f"Image analysis failed: {str(e)}"

image_analyzer = ImageAnalyzer()
