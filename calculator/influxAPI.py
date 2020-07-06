import os
import time
from datetime import datetime

from influxdb import InfluxDBClient, DataFrameClient
from requests.exceptions import ConnectionError

DB_HOST = os.getenv("DB_HOST", "influxdb")
DB_PORT = int(os.getenv("DB_PORT", "8086"))
DB_USERNAME = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "sensor_data")


class InfluxConnection():
    """Influx DB API assistant Class."""

    def __init__(
        self,
        db_host=DB_HOST,
        db_port=DB_PORT,
        db_username=DB_USERNAME,
        db_password=DB_PASSWORD,
        database=DB_NAME
    ):

        self.host = db_host
        self.port = db_port
        self.username = db_username
        self.password = db_password
        self.database = database

        self.db_client = InfluxDBClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database
        )
        self.wait_for_influxdb()

        self.df_client = DataFrameClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database
        )
        self.wait_for_dataFrameClient()

    def wait_for_influxdb(self):
        """Function to wait for the influxdb service to be available."""
        try:
            self.db_client.ping()
            print(f"InfluxDBClient Connected | {datetime.now()}")
            return None
        except ConnectionError:
            print("InfluxDBClient Connection FAILED: Trying again (1s)")
            time.sleep(1)
            self.wait_for_influxdb()

    def wait_for_dataFrameClient(self):
        """Function to wait for the influxdb service to be available."""
        try:
            self.df_client.ping()
            print(f"DataFrameClient Connected | {datetime.now()} ")
            return None
        except ConnectionError:
            print("DataFrameClient Connection FAILED: Trying again (1s)")
            time.sleep(1)
            self.wait_for_dataFrameClient()

    def get_n_recent_readings(
        self,
        number_of_readings,
        table_name="measurements"
    ):
        query_to_execute = (
            'select * from "{}" group by * order by DESC limit {}'
        ).format(table_name, number_of_readings)

        return self.db_client.query(query_to_execute).raw['series']

    def get_n_recent_readings_with_condition(
        self,
        number_of_readings,
        adc,
        channel,
        table_name="measurements"
    ):
        query_to_execute = (
            'select * from "{}" where adc=\'{}\' and channel=\'{}\' group by *'
            ' order by DESC limit {}'
        ).format(table_name, adc, channel, number_of_readings)

        return self.db_client.query(query_to_execute).raw['series']

    def push_to_database(self, json_data, table_name="converted_measurements"):
        pass
