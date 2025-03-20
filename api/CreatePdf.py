from fpdf import FPDF
from VisualizeData import VisualizeData
from io import BytesIO
import matplotlib.pyplot as plt

# Initialize the VisualizeData class
visualizer = VisualizeData(device_id="1a9da8fa-6fa8-49f3-8aaa-420b34eefe57")


def generate_plot(plot_function):
    """
    Utility function to generate a plot and return it as an image buffer.
    """
    buffer = BytesIO()
    plt.figure()
    plot_function()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    return buffer


# ========== PDF DESIGN ==========
class ESGReportPDF(FPDF):
    def header(self):
        if self.page_no() > 2:
            self.set_font("Helvetica", "B", 12)
            self.cell(0, 10, "ESG Energy Consumption and Sustainability Report", ln=True, align="C")
            self.ln(2)
            self.set_line_width(0.5)
            self.line(10, 22, 200, 22)
            self.ln(5)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_line_width(0.2)
            self.line(10, self.get_y(), 200, self.get_y())
            self.set_font("Helvetica", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def add_cover(self, title, subtitle, date):
        self.add_page()
        self.set_y(100)
        self.set_font("Helvetica", "B", 24)
        self.cell(0, 10, title, ln=True, align="C")
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, subtitle, ln=True, align="C")
        self.set_font("Helvetica", "I", 12)
        self.cell(0, 10, date, ln=True, align="C")

    def add_section(self, title, text, plot_function):
        self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(3)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, text, align="J")
        self.ln()

        if plot_function:
            # Add corresponding image
            buffer = generate_plot(plot_function)
            with open(f"temp_plot{plot_function}.png", "wb") as f:
                f.write(buffer.getvalue())  # Save buffer to a temporary file
            self.image(f"temp_plot{plot_function}.png", x=10, w=190)  # Use the file path

            self.ln()


# ========== REPORT CONTENT ==========
if __name__ == "__main__":
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
    pdf.output("ESG_Energy_Report.pdf")
