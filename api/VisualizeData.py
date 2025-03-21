import copy
import os
from matplotlib.colors import LinearSegmentedColormap
from DataLoading import DataLoader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class VisualizeData:
    def __init__(self, device_id):
        self.device_id = device_id
        config_file = os.getenv("CONFIG_SHARE", "default_config_path")
        self.data_loader = DataLoader(config_file)

        self.df2021 = self.data_loader.load_table(device_id=self.device_id, year_month=[
            "202101", "202102", "202103", "202104", "202105", "202106", "202107", "202108", "202109", "202110",
            "202111", "202112"])
        print(self.df2021.head())

        self.df2020 = self.data_loader.load_table(device_id=self.device_id, year_month=[
            "202005", "202006", "202007", "202008", "202009", "202010", "202011", "202012", ])

        print(self.df2020.head())

    def visualize_delta_t_data(self):
        df21 = copy.deepcopy(self.df2021)
        df20 = copy.deepcopy(self.df2020)

        # Ensure datetime format
        df21["sample_time"] = pd.to_datetime(df21["sample_time"])
        df20["sample_time"] = pd.to_datetime(df20["sample_time"])

        # Extract only month (not year-month) for comparison
        df21["month"] = df21["sample_time"].dt.strftime("%B")
        df20["month"] = df20["sample_time"].dt.strftime("%B")

        # Compute average Delta T per month for each year
        df_avg_delta_t = df21.groupby("month")["DeltaT_K"].mean().reset_index()
        df_avg_delta_t2 = df20.groupby("month")["DeltaT_K"].mean().reset_index()

        # Sort by month order
        month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                       "November", "December"]

        df_avg_delta_t["month"] = pd.Categorical(df_avg_delta_t["month"], categories=month_order, ordered=True)
        df_avg_delta_t2["month"] = pd.Categorical(df_avg_delta_t2["month"], categories=month_order, ordered=True)

        df_avg_delta_t = df_avg_delta_t.sort_values("month").reset_index(drop=True)
        df_avg_delta_t2 = df_avg_delta_t2.sort_values("month").reset_index(drop=True)


        # Plot bar chart
        plt.figure(figsize=(12, 6))
        plt.bar(df_avg_delta_t["month"], df_avg_delta_t["DeltaT_K"], color="skyblue", label="2021", width=0.4,
                align="edge")
        plt.bar(df_avg_delta_t2["month"], df_avg_delta_t2["DeltaT_K"], color="salmon", label="2020", width=-0.4,
                align="edge")

        # Labels and formatting
        plt.xlabel("Month", fontsize=12, fontweight="bold")
        plt.ylabel("Average Delta T (K)", fontsize=12, fontweight="bold")
        plt.title("Comparison of Average Delta Temperature Efficiency by Month (2020 vs 2021)", fontsize=14,
                  fontweight="bold")
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        plt.legend(fontsize=12, frameon=True, shadow=True, fancybox=True)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

    def visualize_system_uptime(self):
        df = copy.deepcopy(self.df2021)

        # Ensure timestamps are in datetime format
        df["sample_time"] = pd.to_datetime(df["sample_time"])
        df["cloud_received_time"] = pd.to_datetime(df["cloud_received_time"])

        # Sort by timestamp
        df = df.sort_values(by="sample_time")

        # Compute time gaps between consecutive records
        df["time_gap_h"] = df["sample_time"].diff().dt.total_seconds() / 3600

        # Define threshold for downtime (e.g., gaps > 1 hour indicate a possible downtime)
        downtime_threshold = 1
        df["downtime_event"] = df["time_gap_h"] > downtime_threshold

        downtime_events = df[df["downtime_event"]]

        # Compute Uptime Percentage
        uptime_hours = df["time_gap_h"].sum()
        total_hours = (df["sample_time"].max() - df["sample_time"].min()).total_seconds() / 3600
        uptime_percentage = (uptime_hours / total_hours) * 100

        # Error Status Analysis
        df["Error_Status_Cloud"] = df["Error_Status_Cloud"].fillna(0)  # Replace NaN with 0
        df["error_occurrence"] = df["Error_Status_Cloud"] > 0

        error_heatmap = df.pivot_table(values="error_occurrence", index=df["sample_time"].dt.date,
                                       columns=df["sample_time"].dt.hour, aggfunc="sum")
        # Ensure index is in datetime format
        error_heatmap.index = pd.to_datetime(error_heatmap.index)  # Convert index to datetime

        # Create plot with seaborn
        plt.figure(figsize=(12, 6))
        ax = sns.heatmap(error_heatmap, cmap="Reds", cbar_kws={"label": "Error Occurrences"})

        # Set title and labels
        plt.title("System Error Occurrences Over Time")
        plt.xlabel("Hour of the Day")
        plt.ylabel("Date")

        # Calculate tick positions based on the number of rows in the pivot table.
        tick_step = 20  # Change this value as needed
        num_rows = len(error_heatmap.index)
        tick_positions = np.arange(0, num_rows, tick_step)
        tick_labels = error_heatmap.index[::tick_step].strftime("%Y-%m-%d")

        # Set y-axis ticks and labels
        ax.set_yticks(tick_positions)
        ax.set_yticklabels(tick_labels, rotation=0)

    def visualize_occupant_comfort(self):
        df = copy.deepcopy(self.df2021)

        # Ensure 'sample_time' is in datetime format
        df["sample_time"] = pd.to_datetime(df["sample_time"])
        df["hour"] = df["sample_time"].dt.hour  # Extract hour of the day

        df["date"] = df["sample_time"].dt.date  # Extract date for heatmap index

        # Compute temperature variation (difference between remote and embedded sensors)
        df["Temp_Variation_K"] = df["T1_remote_K"] - df["T2_embeded_K"]

        # Filter data for a specific time range (e.g., one week or one month)
        start_date = "2021-03-01"  # Change this as needed
        end_date = "2021-03-07"  # Display only one week
        filtered_df = df[(df["sample_time"] >= start_date) & (df["sample_time"] <= end_date)]

        # Pivot table for heatmap
        filtered_pivot = filtered_df.pivot_table(values="Temp_Variation_K", index="date", columns="hour",
                                                 aggfunc="mean")

        # Convert DataFrame to NumPy array
        temp_variation_data = filtered_pivot.values

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot heatmap using imshow with improved scaling and interpolation
        cax = ax.imshow(temp_variation_data, cmap="coolwarm", aspect="auto", interpolation="nearest",
                        vmin=np.nanmin(temp_variation_data), vmax=np.nanmax(temp_variation_data))

        # Add colorbar
        cbar = plt.colorbar(cax)
        cbar.set_label("Temperature Variation (K)")

        # Set x-axis (Hours)
        ax.set_xticks(np.arange(len(filtered_pivot.columns)))  # Ensure numerical axis
        ax.set_xticklabels(filtered_pivot.columns.astype(str))  # Convert to string explicitly

        # Set y-axis (Dates)
        ax.set_yticks(np.arange(0, len(filtered_pivot.index)))
        ax.set_yticklabels(filtered_pivot.index)

        # Labels and Title
        plt.xlabel("Hour of the Day")
        plt.ylabel("Date")
        plt.title("Temperature Variation Heatmap")

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)

    def visualize_cooling_energy(self):
        df = copy.deepcopy(self.df2021)
        # visualize sum of Cooling_E_J and Heating_E_J over time

        df["sample_time"] = pd.to_datetime(df["sample_time"])
        df["sample_time"] = pd.to_datetime(df["sample_time"])
        df["Cooling_E_J"] = df["Cooling_E_J"].astype(float)
        df["Heating_E_J"] = df["Heating_E_J"].astype(float)

        df_grouped = df.groupby("sample_time", as_index=False)[["Cooling_E_J", "Heating_E_J"]].sum()

        # Apply cumulative sum so it only goes up
        df_grouped["Cooling_E_J"] = df_grouped["Cooling_E_J"].cumsum()
        df_grouped["Heating_E_J"] = df_grouped["Heating_E_J"].cumsum()

        # Define plot
        plt.figure(figsize=(12, 6))
        plt.plot(df_grouped["sample_time"], df_grouped["Cooling_E_J"], label="Cooling Energy", color="royalblue",
                 marker="o", linestyle="--", markersize=6, linewidth=2)

        # Enhance styling
        plt.xlabel("Date", fontsize=12, fontweight="bold")
        plt.ylabel("Energy (10^12 Joules)", fontsize=12, fontweight="bold")
        plt.title("Cooling Energy Over Time", fontsize=14, fontweight="bold")
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend(fontsize=12, loc="upper left", frameon=True, shadow=True, fancybox=True)

    def visualize_heating_energy(self):
        df = copy.deepcopy(self.df2021)

        # visualize sum of Cooling_E_J and Heating_E_J over time

        df["sample_time"] = pd.to_datetime(df["sample_time"])
        df["sample_time"] = pd.to_datetime(df["sample_time"])
        df["Cooling_E_J"] = df["Cooling_E_J"].astype(float)
        df["Heating_E_J"] = df["Heating_E_J"].astype(float)

        df_grouped = df.groupby("sample_time", as_index=False)[["Cooling_E_J", "Heating_E_J"]].sum()

        # Apply cumulative sum so it only goes up
        df_grouped["Cooling_E_J"] = df_grouped["Cooling_E_J"].cumsum()
        df_grouped["Heating_E_J"] = df_grouped["Heating_E_J"].cumsum()

        # Plot Heating Energy
        plt.figure(figsize=(10, 5))
        plt.plot(df_grouped["sample_time"], df_grouped["Heating_E_J"], label="Heating Energy", color="red", marker="o")
        plt.xlabel("Date")
        plt.ylabel("Energy (Joules)")
        plt.title("Heating Energy Over Time")
        plt.xticks(rotation=45)
        plt.grid()
        plt.legend()

    def visualize_co2(self):
        df = copy.deepcopy(self.df2021)

        # visualize sum of Cooling_E_J and Heating_E_J over time

        df["sample_time"] = pd.to_datetime(df["sample_time"])
        df["sample_time"] = pd.to_datetime(df["sample_time"])
        df["Cooling_E_J"] = df["Cooling_E_J"].astype(float)
        df["Heating_E_J"] = df["Heating_E_J"].astype(float)

        df_grouped = df.groupby("sample_time", as_index=False)[["Cooling_E_J", "Heating_E_J"]].sum()

        # Apply cumulative sum so it only goes up
        df_grouped["Cooling_E_J"] = df_grouped["Cooling_E_J"].cumsum()
        df_grouped["Heating_E_J"] = df_grouped["Heating_E_J"].cumsum()

        # Energy source emission factors in kg CO₂ per kWh (source: IPCC, EPA)
        CO2_EMISSION_FACTORS = {
            "Coal": 0.95,  # kg CO₂ per kWh
            "Natural Gas": 0.45,  # kg CO₂ per kWh
            "Oil": 0.74,  # kg CO₂ per kWh
            "Electricity (EU Mix)": 0.30,  # kg CO₂ per kWh
            "Electricity (US Mix)": 0.40,  # kg CO₂ per kWh
            "Renewable (Solar/Wind)": 0.05,  # kg CO₂ per kWh
        }

        def convert_energy_to_co2(df, energy_column, energy_type):
            """
            Converts energy consumption to CO₂ emissions.

            :param df: Pandas DataFrame containing energy data.
            :param energy_column: Column name containing energy consumption (in Joules).
            :param energy_type: Type of energy source (must be in CO2_EMISSION_FACTORS).
            :return: Pandas DataFrame with added 'CO2_Emissions_kg' column.
            """
            if energy_type not in CO2_EMISSION_FACTORS:
                raise ValueError(f"Unknown energy type: {energy_type}. Choose from {list(CO2_EMISSION_FACTORS.keys())}")

            # Convert Joules to kWh (1 kWh = 3.6 million Joules)
            df["Energy_kWh"] = df[energy_column] / 3.6e6

            # Calculate CO₂ emissions
            df["CO2_Emissions_kg"] = df["Energy_kWh"] * CO2_EMISSION_FACTORS[energy_type]

            return df

        # Example usage:
        energy_type = "Electricity (EU Mix)"  # User input (can be replaced with input())
        df = convert_energy_to_co2(df_grouped, "Heating_E_J", energy_type)


        # Define plot
        plt.figure(figsize=(12, 6))
        plt.plot(df["sample_time"], df["CO2_Emissions_kg"], label=f"CO2 Emissions ({energy_type})", color="forestgreen",
                 marker="o", linestyle="-", markersize=4, linewidth=2)

        # Enhance styling
        plt.xlabel("Date", fontsize=12, fontweight="bold")
        plt.ylabel("CO2 Emissions (Megatonnen)", fontsize=12, fontweight="bold")
        plt.title(f"CO2 Emissions from {energy_type} Energy Over Time", fontsize=14, fontweight="bold")
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend(fontsize=12, loc="upper left", frameon=True, shadow=True, fancybox=True)
