import os
import pandas as pd


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

        if os.path.exists(filename):
            return pd.read_parquet(filename)

        print(f"Error loading data")
        return None
