import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import pandas as pd

possible_device_ids = ['26245f9f-8f9f-41b8-90bc-fa47640395f2',
                       '25ff3a33-6eba-4238-9b8f-c0dea3f2e2c3',
                       '5dd3b941-aab6-44de-bdb6-b5e82026cc54',
                       '96e6013a-9e90-4dbd-9070-d6b4732f42b8',
                       '968cc402-586d-4d47-ba8b-97c065762d0d',
                       '25f08a63-be6a-430f-aa10-1f80af9450f7',
                       'c6569cbb-ab19-41bd-97b8-4a60651ab3b4',
                       '277ebacd-749c-4f9c-9a6f-43b871ec1e5d',
                       'c6893e87-1c36-4dd5-a412-42fe04dd2054',
                       '1cd9e95f-7338-4b7a-ade9-07d6d10d6fe9',
                       '1d0d2869-41d3-4bbc-aa6a-6bb5b3b7e958',
                       '1d3f72a5-6b6f-48aa-85b6-099ee2f6521d',
                       'c9be13ef-db36-4a8e-ba91-87d226345cee',
                       '1c3b788f-55f3-4be4-ba52-0a9c63014836',
                       'bdfb474b-db7c-4ee9-8c06-dfe29a870e3f',
                       '1c76dc41-d7c4-4c34-94e4-9d4285c4cbfe',
                       'f2b9c3cd-04de-4c7d-a46b-f1d60eaac900',
                       'b277316c-1e6e-4893-9206-3c580ac1e677',
                       'e2c21321-36cb-43bc-a831-a5c390aa8a3c',
                       'dcab0762-b0d9-4b86-8038-2c8cfc5f20be',
                       'e2aef88e-ca82-4be1-a68a-39a4634fee57',
                       'a196e561-3f4a-4031-b1f2-3bc96a39cf87',
                       'f9f5777e-985f-4642-9bd6-869bf5fa7b54',
                       'b2cd6c04-53ec-4265-83c2-304b8feef4ae',
                       'db693a87-a33a-4757-8af8-0588233823d3',
                       'f8f8b25b-9af8-4c08-8a0c-3fcc4df82727',
                       '509ee4ad-a2ae-48b1-bebb-e3df49da645a',
                       '50b6259c-c98b-4ce3-b4b0-8e9988cc6e64',
                       '4a3cd440-7a55-4cae-99c1-4a55f5dc265b',
                       'f5e85b70-ed6e-4404-b9b8-4ff66bbf98b1',
                       '7e0efd40-7ccb-402e-b736-5f18a8690987',
                       'f436ea42-644a-4cf1-b3cc-d5bb5340c920',
                       'b47efbc5-af61-468c-8415-eede982661a6',
                       '7e637e2e-bb9b-43b5-9fa0-90541f8176af',
                       'f5e7db86-1490-48d4-a419-3e96f0d6cde5',
                       '7baa9b48-ca1a-428c-89d8-38acb02d8b19',
                       '154c4794-3856-4302-930d-3721e22f806b',
                       'b47b4cfe-34b8-4ea0-9f53-889896c7643c',
                       'b42aa654-3614-4b6e-b9f0-5350c6342d0b',
                       'f42a563f-56fb-474c-a37b-52466d2854ab',
                       '7b056817-a5c0-4ce2-b5d1-6ec060b7a6fe',
                       'f58de9b9-2395-446d-bfb4-43bf23b24589',
                       'ca81390e-8e40-4f84-8823-d9f72e5ef9f1',
                       '44d2b1db-548b-4d2d-9253-e5c8e66a35e6',
                       'edfa4049-caa6-4706-964a-2db4bf4b2fa3',
                       'd427fa6a-a1c5-4a55-870a-d4c706e97af2',
                       'b7904af5-0ff2-4ee8-98b1-b2c63071a2f1',
                       'b8537f7c-440f-4e91-9267-29088647f235',
                       '4445c4e3-9287-4dd4-8ee8-197fe08fb787',
                       '8efaa357-f444-4f57-8c16-9932e9586c99',
                       '90ce2e32-b4f7-43e5-9946-3221ce792e64',
                       '8f40cbf8-bc2c-4713-adaa-61cd8731514d',
                       'b1b9977f-84e3-4583-91d3-fdcfafaa25eb',
                       '69363abf-b8cd-4ef6-9f85-1a34ab174e32',
                       '3b51ed98-e0ee-4c4c-84bd-081a557deec8',
                       '84d5def1-33c3-427b-98ec-5214c12df4b9',
                       '3c0e2712-ab4c-46b4-823e-bcabe6a98141',
                       '9dc2fedc-a1eb-42ad-9635-ee9472f083e7',
                       '9944c91c-346e-4568-a912-d3b977705ee6',
                       '83c1e3dd-d35a-44c2-9436-0e7ce95b802f',
                       '6ac761d1-6081-42d2-b92f-5b5d896fa886',
                       '3d32e5f2-2c65-40f5-bd7a-850df96ed5ec',
                       '843a1bf0-b66e-4317-80ce-a74be097f515',
                       'eae041f0-536b-4f9a-8a17-b42b8dcf8686',
                       'b0b16562-df9d-4f1d-971a-d0cf86169292',
                       'eba83b6b-b98f-4388-af04-26cc556f6453',
                       'eb4064fc-531a-4642-9a6a-53e12d302157',
                       '0df6e1fb-f7a0-4412-83d6-b8013fa7c4a7',
                       'd5982297-3e61-4b45-b40f-7bbcb72c976f',
                       '3949c3c1-94d3-4600-bdac-a8bd34cbd483',
                       '37dbf169-dd20-4161-a9ef-1540636818c7',
                       '0fccd4a0-a11d-40f0-a6f5-0762664f424d',
                       '73ec993f-14a1-495e-bf7c-2f49a0ecede6',
                       'fd1497cd-ef6c-499a-b3a4-992e21a418b7',
                       '75452182-91fe-4c41-a81d-03c49dbe6793',
                       'c81038fb-450e-4160-a097-aff368f1119b',
                       '74471ab8-0527-4611-b5d1-e22183269fd7',
                       'fe152576-14f0-4198-8e36-fe1d0abddce3',
                       '2021a494-7f52-4e04-99b1-861cd61e0a10',
                       '5258b69b-c282-411c-be30-a1ae38b2d498',
                       '21281d3c-2283-492d-9fc5-5f3591996856',
                       '526013e7-e3ad-49e6-a30f-6d458f851b2d',
                       '35491907-17c8-46bd-b0ec-cbc8d6d626ea',
                       'fff0df7f-8856-4054-8103-2e4b33423af6',
                       '33e8b77b-5c1c-42cb-a2fb-93bdf6e08eb4',
                       '830bdd9e-d05c-42f9-bb13-346dea34bb1f',
                       '49c15030-1403-4edd-880d-b011c330020a',
                       '539c36bf-5dd9-4fee-90b3-7df08d75a1bc',
                       'f1e87ad9-7c1b-4a5c-9e78-976152fcb186',
                       '13105404-7f2b-47ed-be8d-efb5a6c3c571',
                       'ccc3f70f-ec34-4390-ab9d-6b5ca5136773',
                       'fa1dccea-819e-4bbb-9ac5-0f6adea99515',
                       'a5b32425-b961-4f31-9754-262094717342',
                       'a65c0a1d-12e9-44f8-a154-bbbbde49c3c2',
                       '3e6d4b5b-b5a8-4d66-ae2b-df70b0da7652',
                       '2f111380-509e-48ea-829f-0b9589ac994f',
                       'fbaeba5b-89fd-4f79-a785-ba8befb15b6b',
                       'fb4cf03c-aaf6-40e8-a7fa-e13a7a5b82ec',
                       '41e6641e-96d0-41fa-81e5-e1e4069b41f7',
                       '2e94a4b6-33e0-4c7a-938b-435e7423f032']


class DataLoader:

    def __init__(self, config_file_path):

        self.config_file_path = config_file_path
        self.spark = SparkSession \
            .builder \
            .appName("Python Spark SQL basic example") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .config("spark.jars.packages", "io.delta:delta-sharing-spark_2.12:3.3.0") \
            .getOrCreate()
        self.spark.conf.set("spark.sql.debug.maxToStringFields", 100)

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


        try:
            # Load the data from Delta Sharing
            df = self.spark.read.format("deltaSharing").load(self.data_table_name)
            # Apply optional filters
            if device_id is not None:
                df = df.filter(col("device_id") == device_id)

            if year_month is not None:
                df = df.filter(col("year_month").isin(year_month))

            # apply the limit
            if limit is not None:
                df = df.limit(limit)

            df = df.toPandas()

            self.save_file(device_id, year_month, limit, df)

            return df

        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def save_file(self, device_id, year_month, limit, df):
        path = f"loaded_data"
        name = f"{device_id}_{year_month}_{limit}.parquet"
        if not os.path.exists(path):
            os.makedirs(path)
        df.to_parquet(os.path.join(path, name))


if __name__ == "__main__":
    # Load the data
    loader = DataLoader("config.share")
    data = loader.load_table(device_id="1a9da8fa-6fa8-49f3-8aaa-420b34eefe57", year_month=["202103"])
    print(data.head())
    print(data.columns)
    print(data.shape)
