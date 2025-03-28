from fastapi import FastAPI, Response
import matplotlib.pyplot as plt
from io import BytesIO
from src.data.VisualizeData import VisualizeData

app = FastAPI()

# Initialize the VisualizeData class
visualizer = VisualizeData(device_id="your-device-id")


@app.get("/")
def read_root():
    return {"Hello": "World"}

def generate_plot(plot_function):
    """
    Utility function to generate a plot and return it as a PNG response.
    """
    buffer = BytesIO()
    plt.figure()
    plot_function()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    return Response(content=buffer.getvalue(), media_type="image/png")


@app.get("/visualize/delta_t")
def visualize_delta_t():
    return generate_plot(visualizer.visualize_delta_t_data)


@app.get("/visualize/system_uptime")
def visualize_system_uptime():
    return generate_plot(visualizer.visualize_system_uptime)


@app.get("/visualize/occupant_comfort")
def visualize_occupant_comfort():
    return generate_plot(visualizer.visualize_occupant_comfort)


@app.get("/visualize/cooling_energy")
def visualize_cooling_energy():
    return generate_plot(visualizer.visualize_cooling_energy)


@app.get("/visualize/heating_energy")
def visualize_heating_energy():
    return generate_plot(visualizer.visualize_heating_energy)


@app.get("/visualize/co2")
def visualize_co2():
    return generate_plot(visualizer.visualize_co2)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
