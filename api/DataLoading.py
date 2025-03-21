import os
import pandas as pd
import requests
from io import BytesIO


class DataLoader:

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.data_table_name = "config.share#start_hack_2025.start_hack_2025.ev3_device_data"

        self.storage_path = "loaded_data"

    def load_table(self, limit: int = None, device_id: str = None, year_month: list = None):
        """
        Loads data from the Delta Sharing table with optional filtering.

        :param limit: Maximum number of records to load (default: 5000).
        :param device_id: Optional filter for a specific device_id.
        :param year_month: Optional filter for a specific year_month.
        :return: Data as a Pandas DataFrame.
        """
        path = f"loaded_data"
        name = f"{device_id}_{year_month}_{limit}.parquet"
        filename = os.path.join(path, name)

        print(f"Loading data from {filename}")
        if filename == "loaded_data/1a9da8fa-6fa8-49f3-8aaa-420b34eefe57_['202101', '202102', '202103', '202104', '202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112']_None.parquet":
            """response = requests.get(
                "https://firebasestorage.googleapis.com/v0/b/starthack25.firebasestorage.app/o/data_2021.pkl?alt=media&token=2b1f74cb-1a10-4b37-b7b5-780bfc295e62")
            return pd.read_pickle(BytesIO(response.content))"""
            return pd.read_pickle("data/data_2021.pkl")
        elif filename == "loaded_data/1a9da8fa-6fa8-49f3-8aaa-420b34eefe57_['202005', '202006', '202007', '202008', '202009', '202010', '202011', '202012']_None.parquet":
            """ response = requests.get(
                "https://firebasestorage.googleapis.com/v0/b/starthack25.firebasestorage.app/o/data_2020.pkl?alt=media&token=5bdb018f-67f8-45e5-a9a4-141a8e764153")
            return pd.read_pickle(BytesIO(response.content))"""
            return pd.read_pickle("data/data_2020.pkl")

        print(f"Error loading data")
        return None
