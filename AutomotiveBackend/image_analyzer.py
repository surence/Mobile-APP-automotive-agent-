import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_vehicle_damage(image_path: str) -> str:
    """
    Analyze a vehicle image using Gemini Vision.
    """

    try:

        image = Image.open(image_path)

        prompt = """
You are an experienced automotive damage assessor.

Analyze the uploaded vehicle image.

Provide a professional report using the following format:

1. Visible Damage
2. Possible Damaged Components
3. Severity
   - Minor
   - Moderate
   - Severe
4. Safety Concerns
5. Recommended Repairs
6. Estimated Repair Difficulty
7. Additional Observations

If no visible damage exists, clearly state that.
"""

        response = model.generate_content(
            [prompt, image]
        )

        return response.text

    except Exception as e:

        return f"Image Analysis Error:\n{str(e)}"