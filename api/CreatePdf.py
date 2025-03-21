from fpdf import FPDF
from VisualizeData import VisualizeData
from io import BytesIO
import matplotlib.pyplot as plt

# Initialize the VisualizeData class
visualizer = VisualizeData(device_id="1a9da8fa-6fa8-49f3-8aaa-420b34eefe57")


def generate_plot(plot_function, plot_filename):
    """
    Utility function to generate a plot, save it to disk, and return the image buffer.
    """
    buffer = BytesIO()
    plt.figure()
    plot_function()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.savefig(f"{plot_filename}.png", format="png", bbox_inches="tight")  # Save to disk
    plt.close()
    buffer.seek(0)
    return buffer


# ========== PDF DESIGN ==========
class ESGReportPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
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
        self.image('data/bg.png', x=0, y=0, w=self.w, h=self.h)
        self.set_y(30)
        self.set_font("Helvetica", "B", 24)
        self.cell(0, 10, title, ln=True, align="C")
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, subtitle, ln=True, align="C")
        self.set_font("Helvetica", "I", 12)
        self.cell(0, 10, date, ln=True, align="C")

    def add_page_1(self):
        # Table of Contents
        self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Table of Contents", ln=True, align="L")
        self.ln(5)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, "1. Introduction", align="L")
        self.multi_cell(0, 8, "2. Temperature Analysis", align="L")
        self.multi_cell(0, 8, "3. System Uptime Analysis", align="L")
        self.multi_cell(0, 8, "4. Occupant Comfort Analysis", align="L")
        self.multi_cell(0, 8, "5. Cooling Energy Consumption", align="L")
        self.multi_cell(0, 8, "6. Heating Energy Consumption", align="L")
        self.multi_cell(0, 8, "7. Emissions Analysis", align="L")
        self.multi_cell(0, 8, "8. Conclusion and Recommendations", align="L")
        self.ln(10)

        intro_text = (
            "This report provides an in-depth analysis of the energy efficiency, system uptime, "
            "occupant comfort, cooling and heating energy consumption, and emissions. The analysis "
            "focuses on identifying trends, efficiency gains, and areas for further improvement based "
            "on the collected data from 2020 to 2021. Key performance indicators (KPIs) are used to benchmark "
            "the building's operational performance against industry standards, enabling actionable insights "
            "for strategic planning. Additionally, seasonal variations and usage patterns are taken into account "
            "to better understand the impact of environmental and behavioral factors on system efficiency. "
            "\n"
            "The data presented in this report was gathered through a network of Belimo devices installed "
            "across the monitored facilities. These devices are known for their high precision, reliability, "
            "and compliance with international standards for energy and environmental monitoring. Belimos "
            "sensors and actuators are certified for performance and calibration, ensuring the integrity and "
            "consistency of the collected data. The use of Belimo technology enables continuous, real-time monitoring "
            "of key building parameters, which serves as a robust foundation for accurate ESG reporting and data-driven "
            "optimization strategies."
        )

        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "1. Introduction", ln=True, align="L")
        self.ln(3)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, intro_text, align="J")
        self.ln()

        # ESG Section Explanation
        esg_explanation = (
            "Environmental, Social, and Governance (ESG) Considerations \n"
            "ESG reporting ensures transparency and accountability in building operations. This section explains "
            "how each aspect of energy efficiency and building performance aligns with ESG principles:\n\n"
            "Environmental: Reducing carbon emissions, optimizing energy consumption, and improving sustainability.\n"
            "Social: Enhancing occupant comfort, indoor air quality, and well-being.\n"
            "Governance: Ensuring compliance with energy efficiency regulations and corporate responsibility initiatives.\n"
        )

        self.add_page()
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "Environmental, Social, and Governance (ESG) Considerations", ln=True, align="L")
        self.ln(3)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, esg_explanation, align="J")
        self.ln(5)

    def add_section(self, title, text, plot_function, plot_filename, text2=None):
        self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(3)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, text, align="J")
        self.ln(3)

        if plot_function is not None and plot_filename is not None:
            generate_plot(plot_function, plot_filename)
            self.image(f"{plot_filename}.png", x=10, w=190)

        if text2 is not None:
            self.ln(3)
            self.multi_cell(0, 8, text2, align="J")
            self.ln(3)


# ========== REPORT CONTENT ==========
if __name__ == "__main__":
    pdf = ESGReportPDF()

    # Cover Page
    pdf.add_cover("ESG Energy Report", "Annual Sustainability and Efficiency Analysis", "March 2025")
    pdf.add_page_1()

    # Temperature Analysis
    temp_text = (
        "This section compares the average temperature performance across different months in "
        "2020 and 2021. The data indicates a notable improvement in energy efficiency in 2021, "
        "particularly in colder months. Understanding these variations helps in optimizing energy usage "
        "and improving climate control within facilities."
    )

    temp_text2 = (
        "The comparison of average Delta T (temperature difference) between 2020 and 2021 reveals "
        "significant improvements in energy efficiency. The average Delta T values for 2021 are consistently "
        "lower than those of 2020, indicating better thermal performance and reduced energy waste. These findings "
        "suggest that operational changes or system upgrades have positively impacted the building's energy efficiency."
    )
    pdf.add_section("2. System efficiency Analysis", temp_text, visualizer.visualize_delta_t_data, "delta_t.png",
                    text2=temp_text2)

    # Occupant Comfort
    comfort_text = (
        "Occupant comfort is a crucial factor in energy management. The temperature variation "
        "heatmap highlights significant fluctuations, particularly in early March, which could "
        "indicate potential issues with insulation or HVAC system inefficiencies. Addressing these "
        "concerns will enhance overall comfort while optimizing energy consumption."
    )
    comfort_text2 = (
        "The temperature variation heatmap provides insights into fluctuations in indoor climate conditions "
        "across different hours of the day. Higher temperature variations, indicated in red, suggest periods "
        "of instability that could affect occupant comfort. These fluctuations may be attributed to external "
        "weather conditions, HVAC system cycling, or insulation inefficiencies. \n\n"
        "By analyzing this data, facility managers can identify peak variation periods and take corrective actions, "
        "such as adjusting thermostat schedules, improving insulation, or optimizing ventilation strategies. "
        "Ensuring stable indoor temperatures not only enhances comfort but also contributes to energy efficiency "
        "and sustainability goals."
    )
    pdf.add_section("3. Occupant Comfort Analysis", comfort_text, visualizer.visualize_occupant_comfort, "comfort.png",
                    text2=comfort_text2)

    # Cooling Energy Consumption
    cooling_text = (
        "Cooling energy consumption trends indicate a steady increase over time. This pattern suggests "
        "that cooling demand is rising, likely due to external weather factors and internal heat loads. "
        "Analyzing these trends helps in devising energy-efficient cooling strategies."
    )
    cooling_text2 = (
        "Cooling energy consumption trends indicate variations in demand throughout the day and across seasons. "
        "Higher consumption periods, often observed during peak daytime hours, can be attributed to external temperatures, "
        "building occupancy levels, and HVAC system performance. Understanding these patterns helps in optimizing cooling "
        "strategies to reduce energy waste and improve efficiency. \n\n"
        "By analyzing cooling energy trends over time, facility managers can implement demand-based cooling schedules, "
        "adjust thermostat settings, and explore energy-efficient technologies such as automated shading and adaptive "
        "HVAC controls. These measures contribute to lowering operational costs while maintaining occupant comfort."
    )
    pdf.add_section("4. Cooling Energy Consumption", cooling_text, visualizer.visualize_cooling_energy, "cooling.png",
                    text2=cooling_text2)

    # Heating Energy Consumption
    heating_text = (
        "Heating energy usage has shown a continuous increase. This data suggests that additional "
        "efficiency measures should be explored, including improved insulation, optimized heating "
        "schedules, and alternative heating solutions to reduce energy costs."
    )
    heating_text2 = (
        "Heating energy consumption varies based on seasonal and daily temperature fluctuations, building insulation quality, "
        "and occupancy behavior. Peaks in heating demand often occur during early mornings and late evenings when external "
        "temperatures drop. Identifying these trends allows for better control of heating systems to enhance efficiency. \n\n"
        "Optimizing heating schedules, improving insulation, and leveraging smart thermostat technology can significantly reduce "
        "energy waste. By implementing data-driven heating strategies, facilities can maintain comfortable indoor temperatures "
        "while minimizing energy costs and environmental impact."
    )
    pdf.add_section("5. Heating Energy Consumption", heating_text, visualizer.visualize_heating_energy, "heating.png",
                    text2=heating_text2)

    # Emissions
    emissions_text = (
        "Energy consumption directly impacts emissions. The data shows a rising trend in emissions, "
        "which suggests a strong need for integrating renewable energy sources and improving energy "
        "efficiency across operations to reduce environmental impact."
    )
    co2_text2 = (
        "CO2 emissions are directly linked to energy consumption patterns and the energy sources used within a facility. "
        "Higher emissions indicate increased reliance on non-renewable energy sources, inefficient HVAC operation, or suboptimal "
        "building performance. Monitoring these emissions over time helps identify areas where sustainability improvements "
        "can be made. \n\n"
        "By integrating renewable energy sources, optimizing heating and cooling efficiency, and adopting energy conservation "
        "practices, facilities can reduce their carbon footprint. Proactive emissions management supports corporate ESG goals, "
        "regulatory compliance, and long-term sustainability initiatives."
    )
    pdf.add_section("6. Emissions Analysis", emissions_text, visualizer.visualize_co2, "emissions.png", text2=co2_text2)

    # System Uptime Analysis
    uptime_text = (
        "System uptime data reveals critical downtime periods and potential inefficiencies. "
        "Through a heatmap visualization, we identify specific hours and dates where errors occurred, "
        "suggesting areas where maintenance schedules and system reliability can be enhanced."
    )
    uptime_text2 = (
        "System uptime is a critical factor in ensuring the reliability and efficiency of building operations. "
        "Frequent system downtimes can lead to operational disruptions, increased energy consumption due to system "
        "restarts, and reduced occupant comfort. Analyzing uptime trends helps in identifying recurring failures, "
        "maintenance needs, and opportunities for system optimization. \n\n"
        "By monitoring system uptime over time, facility managers can proactively address issues before they lead to "
        "major failures, schedule preventive maintenance more effectively, and improve overall equipment reliability. "
        "Ensuring high uptime not only enhances energy efficiency but also extends the lifespan of HVAC systems and other "
        "critical infrastructure components."
    )
    pdf.add_section("7. System Uptime Analysis", uptime_text, visualizer.visualize_system_uptime, "uptime.png",
                    text2=uptime_text2)

    # Conclusion and Recommendations
    conclusion_text = (
        "This report provides a comprehensive analysis of energy efficiency, system uptime, occupant comfort, cooling and heating energy consumption, "
        "and CO2 emissions. By examining historical trends and performance indicators, we have identified key areas for improvement that will contribute "
        "to enhanced operational efficiency, sustainability, and cost savings. \n\n"

        "Key Insights: \n"
        "- Cooling Energy Consumption: Cooling demand fluctuates significantly, particularly during peak hours. By optimizing cooling schedules, "
        "adjusting setpoints, and implementing energy-efficient cooling strategies such as automated shading and dynamic load balancing, energy waste "
        "can be reduced while maintaining a comfortable indoor climate. \n\n"

        "- Heating Energy Consumption: Seasonal temperature variations have a direct impact on heating demand, with peak usage observed during colder months. "
        "Improving insulation, utilizing smart thermostats, and implementing predictive heating algorithms can enhance energy efficiency while ensuring "
        "consistent indoor temperatures. \n\n"

        "- System Uptime and Reliability: Frequent system downtime leads to increased energy waste, operational inefficiencies, and potential occupant discomfort. "
        "Proactive maintenance strategies, real-time monitoring, and predictive analytics can minimize unexpected failures and extend the lifespan of HVAC and other "
        "critical infrastructure systems. \n\n"

        "- Occupant Comfort: Large fluctuations in temperature variation, especially during early mornings and peak occupancy hours, indicate potential HVAC "
        "inefficiencies or insulation issues. Addressing these inconsistencies through optimized ventilation, insulation enhancements, and improved control algorithms "
        "will enhance both comfort and energy performance. \n\n"

        "- CO2 Emissions: The direct correlation between energy consumption and emissions highlights the need for sustainable energy solutions. "
        "Incorporating renewable energy sources, improving equipment efficiency, and implementing demand-response strategies can significantly lower the buildings "
        "carbon footprint. \n\n"

        "Recommendations for Future Improvement: \n"
        "1. Energy Optimization: Implement AI-driven energy management solutions to optimize cooling, heating, and overall HVAC performance.\n"
        "2. Sustainable Practices: Integrate renewable energy sources where possible, such as solar panels or green power procurement.\n"
        "3. Predictive Maintenance: Utilize real-time monitoring and predictive analytics to anticipate and prevent system failures.\n"
        "4. Smart Automation: Deploy intelligent automation strategies, such as dynamic temperature adjustments and demand-response systems, to reduce unnecessary energy consumption.\n"
        "5. Occupant-Centered Design: Continuously analyze comfort data to fine-tune HVAC settings based on real occupancy patterns, improving both efficiency and user experience.\n"
        "6. Regulatory Compliance: Ensure alignment with the latest ESG reporting standards and sustainability regulations to maintain corporate responsibility and compliance.\n\n"

        "By implementing these strategies, facility managers can significantly reduce operational costs, enhance occupant satisfaction, and contribute to global sustainability efforts. "
        "Continuous data monitoring, combined with proactive decision-making, will be key to achieving long-term energy efficiency and environmental responsibility."
    )
    pdf.add_section("8. Conclusion and Recommendations", conclusion_text, None, None)

    # Save PDF
    pdf.output("ESG_Energy_Report.pdf")
