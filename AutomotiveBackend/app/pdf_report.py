"""
Professional PDF Report Generator
"""

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.config import REPORT_FOLDER


class PDFReportGenerator:

    def generate(
        self,
        vehicle,
        ai_diagnosis: str,
        tool_results: dict,
        damage_analysis: str = "",
        confidence: int = 95,
    ) -> str:

        REPORT_FOLDER.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = (
            f"diagnostic_report_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        pdf_path = REPORT_FOLDER / filename

        doc = SimpleDocTemplate(str(pdf_path))

        styles = getSampleStyleSheet()

        title_style = styles["Heading1"]
        title_style.alignment = TA_CENTER

        heading_style = styles["Heading2"]

        normal_style = styles["BodyText"]

        story = []

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        story.append(
            Paragraph(
                "AI Automotive Diagnostic Report",
                title_style,
            )
        )

        story.append(Spacer(1, 20))

        # --------------------------------------------------
        # Vehicle Information
        # --------------------------------------------------

        story.append(
            Paragraph(
                "Vehicle Information",
                heading_style,
            )
        )

        vehicle_table = Table(
            [
                ["Make", vehicle.make],
                ["Model", vehicle.model],
                ["Year", str(vehicle.year)],
                ["Mileage", str(vehicle.mileage)],
                ["Fuel Type", vehicle.fuel_type],
                ["Transmission", vehicle.transmission],
                ["Engine", vehicle.engine_size or "N/A"],
                ["Symptom Category", vehicle.symptom_category],
                ["OBD-II Code", vehicle.obd_code or "None"],
            ],
            colWidths=[150, 300],
        )

        vehicle_table.setStyle(

            TableStyle(

                [

                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                    ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

                ]

            )

        )

        story.append(vehicle_table)

        story.append(Spacer(1, 20))

        # --------------------------------------------------
        # Symptoms
        # --------------------------------------------------

        story.append(
            Paragraph(
                "Customer Symptoms",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                vehicle.symptoms,
                normal_style,
            )
        )

        story.append(Spacer(1, 20))

        # --------------------------------------------------
        # AI Diagnosis
        # --------------------------------------------------

        story.append(
            Paragraph(
                "AI Diagnosis",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                ai_diagnosis.replace("\n", "<br/>"),
                normal_style,
            )
        )

        story.append(Spacer(1, 20))

        # --------------------------------------------------
        # Image Analysis
        # --------------------------------------------------

        if damage_analysis:

            story.append(
                Paragraph(
                    "Vehicle Damage Analysis",
                    heading_style,
                )
            )

            story.append(
                Paragraph(
                    damage_analysis.replace("\n", "<br/>"),
                    normal_style,
                )
            )

            story.append(Spacer(1, 20))

        # --------------------------------------------------
        # Tool Results
        # --------------------------------------------------

        story.append(
            Paragraph(
                "Diagnostic Tools",
                heading_style,
            )
        )

        tools_table = Table(
            [
                [
                    "Diagnosis",
                    tool_results.get(
                        "diagnosis",
                        "",
                    ),
                ],
                [
                    "Repair Cost",
                    tool_results.get(
                        "repair_cost",
                        "",
                    ),
                ],
                [
                    "Maintenance",
                    tool_results.get(
                        "maintenance",
                        "",
                    ),
                ],
                [
                    "OBD-II",
                    tool_results.get(
                        "obd_analysis",
                        "",
                    ),
                ],
            ],
            colWidths=[150, 300],
        )

        tools_table.setStyle(

            TableStyle(

                [

                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                    ("BACKGROUND", (0, 0), (0, -1), colors.beige),

                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

                ]

            )

        )

        story.append(tools_table)

        story.append(Spacer(1, 20))

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        story.append(
            Paragraph(
                "AI Confidence Score",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                f"{confidence}%",
                normal_style,
            )
        )

        story.append(Spacer(1, 20))

        # --------------------------------------------------
        # Footer
        # --------------------------------------------------

        story.append(
            Paragraph(
                f"Generated on: {datetime.now()}",
                normal_style,
            )
        )

        story.append(
            Paragraph(
                "Powered by Groq + LangChain + Gemini Vision",
                normal_style,
            )
        )

        doc.build(story)

        return str(pdf_path)


pdf_generator = PDFReportGenerator()