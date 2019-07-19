from datetime import datetime
from influxdb import InfluxDBClient, DataFrameClient
import time

class InfluxConnection():

	def __init__(self, db_host='10.128.189.236', db_port=8086, db_username='root', db_password='root', database='testing'):

		self.host = db_host
		self.port = db_port
		self.username = db_username
		self.password = db_password
		self.database = database

		self.db_client = InfluxDBClient(host=self.host, port=self.port, username=self.username, password=self.password, database=self.database)
		self.wait_for_influxdb()

		self.df_client = DataFrameClient(host=self.host, port=self.port, username=self.username, password=self.password, database=self.database)
		self.wait_for_dataFrameClient()


	def wait_for_influxdb(self):
		"""Function to wait for the influxdb service to be available"""
		try:
			self.db_client.ping()
			print(f"InfluxDBClient Connected | {datetime.now()}")
			return None
		except:
			print("InfluxDBClient Connection FAILED: Trying again (1s)")
			time.sleep(1)
			self.wait_for_influxdb()

	def wait_for_dataFrameClient(self):
		"""Function to wait for the influxdb service to be available"""
		try:
			self.df_client.ping()
			print(f"DataFrameClient Connected | {datetime.now()} ")
			return None
		except:
			print("DataFrameClient Connection FAILED: Trying again (1s)")
			time.sleep(1)
			self.wait_for_dataFrameClient()


	def get_n_recent_readings(self, number_of_readings, table_name="measurements"):
		query_to_execute = f'select * from "{table_name}" group by * order by DESC limit {number_of_readings}'

		return self.db_client.query(query_to_execute).raw['series']

	def get_n_recent_readings_with_condition(self, number_of_readings, adc, channel, table_name="measurements"):
		query_to_execute = f'select * from "{table_name}" where adc=\'{adc}\' and channel=\'{channel}\' group by * order by DESC limit {number_of_readings}'

		return self.db_client.query(query_to_execute).raw['series']

	def push_to_database(self, json_data, table_name="converted_measurements"):
		pass
