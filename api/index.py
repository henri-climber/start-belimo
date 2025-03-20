from fastapi import FastAPI, Response
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

from VisualizeData import VisualizeData

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
