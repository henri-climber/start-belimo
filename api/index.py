from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from VisualizeData import VisualizeData
from CreatePdf import ESGReportPDF

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
# Initialize the VisualizeData class
visualizer = VisualizeData(device_id="1a9da8fa-6fa8-49f3-8aaa-420b34eefe57")


@app.get("/")
async def root():
    """
       Root endpoint for the API.
       Returns a simple greeting message.
    """
    return {"message": "Hello World"}


@app.get("/create_pdf")
async def create_pdf():
    pdf = ESGReportPDF()

    # Cover Page
    pdf.add_cover("ESG Energy Report", "Annual Sustainability and Efficiency Analysis", "March 2025")

    # Introduction
    intro_text = (
        "This report provides an in-depth analysis of the energy efficiency, system uptime, "
        "occupant comfort, cooling and heating energy consumption, and emissions. The analysis "
        "focuses on identifying trends, efficiency gains, and areas for further improvement based "
        "on the collected data from 2020 to 2021."
    )
    pdf.add_section("1. Introduction", intro_text, None)

    # Temperature Analysis
    temp_text = (
        "This section compares the average temperature performance across different months in "
        "2020 and 2021. The data indicates a notable improvement in energy efficiency in 2021, "
        "particularly in colder months. Understanding these variations helps in optimizing energy usage "
        "and improving climate control within facilities."
    )
    pdf.add_section("2. Temperature Analysis", temp_text, visualizer.visualize_delta_t_data)

    # System Uptime Analysis
    uptime_text = (
        "System uptime data reveals critical downtime periods and potential inefficiencies. "
        "Through a heatmap visualization, we identify specific hours and dates where errors occurred, "
        "suggesting areas where maintenance schedules and system reliability can be enhanced."
    )
    pdf.add_section("3. System Uptime Analysis", uptime_text, visualizer.visualize_system_uptime)

    # Occupant Comfort
    comfort_text = (
        "Occupant comfort is a crucial factor in energy management. The temperature variation "
        "heatmap highlights significant fluctuations, particularly in early March, which could "
        "indicate potential issues with insulation or HVAC system inefficiencies. Addressing these "
        "concerns will enhance overall comfort while optimizing energy consumption."
    )
    pdf.add_section("4. Occupant Comfort Analysis", comfort_text, visualizer.visualize_occupant_comfort)

    # Cooling Energy Consumption
    cooling_text = (
        "Cooling energy consumption trends indicate a steady increase over time. This pattern suggests "
        "that cooling demand is rising, likely due to external weather factors and internal heat loads. "
        "Analyzing these trends helps in devising energy-efficient cooling strategies."
    )
    pdf.add_section("5. Cooling Energy Consumption", cooling_text, visualizer.visualize_cooling_energy)

    # Heating Energy Consumption
    heating_text = (
        "Heating energy usage has shown a continuous increase. This data suggests that additional "
        "efficiency measures should be explored, including improved insulation, optimized heating "
        "schedules, and alternative heating solutions to reduce energy costs."
    )
    pdf.add_section("6. Heating Energy Consumption", heating_text, visualizer.visualize_heating_energy)

    # Emissions
    emissions_text = (
        "Energy consumption directly impacts emissions. The data shows a rising trend in emissions, "
        "which suggests a strong need for integrating renewable energy sources and improving energy "
        "efficiency across operations to reduce environmental impact."
    )
    pdf.add_section("7. Emissions Analysis", emissions_text, visualizer.visualize_co2)

    # Conclusion and Recommendations
    conclusion_text = (
        "This report highlights key trends in energy efficiency, system uptime, occupant comfort, and emissions. "
        "Future efforts should focus on reducing energy waste, increasing system reliability, and integrating "
        "sustainable energy solutions to minimize the environmental impact and improve operational efficiency."
    )
    pdf.add_section("8. Conclusion and Recommendations", conclusion_text, None)

    # Save PDF
    pdf_path = "ESG_Energy_Report.pdf"
    pdf.output(pdf_path)
    return FileResponse(
        path=pdf_path,
        filename="ESG_Energy_Report.pdf",
        media_type="application/pdf"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
