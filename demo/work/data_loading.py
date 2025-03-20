from pyspark.sql import SparkSession
import delta_sharing
from pyspark.sql.functions import col

class DataLoader:
    def __init__(self):
        self.spark = SparkSession \
            .builder \
            .appName("Python Spark SQL basic example") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .config("spark.jars.packages", "io.delta:delta-sharing-spark_2.12:3.3.0") \
            .getOrCreate()
        self.config = "config.share"
        self.client = delta_sharing.SharingClient(self.config)

    def load_table(self, device_id = None, year_month = None):
        df_data = self.spark.read.format("deltaSharing").load(
            "config.share#start_hack_2025.start_hack_2025.ev3_device_data").filter(
            (col("device_id") == device_id) & (col("year_month") == year_month)).toPandas()
        return df_data

    def save_table(self, df, table_name):
        df.to_parquet(f"{table_name}.parquet")


# main
if __name__ == "__main__":
    data_loader = DataLoader()
    df = data_loader.load_table(device_id="1a9da8fa-6fa8-49f3-8aaa-420b34eefe57", year_month="202103")
    data_loader.save_table(df, "device_data")
    print(df)
