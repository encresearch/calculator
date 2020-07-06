import time
import json
from datetime import datetime

import paho.mqtt.client as mqtt
import pandas as pd

from calculator.influxAPI import InfluxConnection
from calculator.conversionFunctions import sensor_functions

BROKER_HOST = 'mqtt.eclipse.org'
BROKER_PORT = 1883
BROKER_KEEPALIVE = 120
MQTT_CLIENT_ID = "/Calculator"
# MQTT Topic to communicate with Connector and Inpsector
CONNECTOR_MQTT_TOPIC = "communication/influxdbUpdate"
INPECTOR_MQTT_TOPIC = "communication/influxdbConverted"


def connect_to_broker(
    client_id,
    host,
    port,
    keepalive,
    on_connect,
    on_message
):
    """Returns an mqtt.Client and mqtt.Client.connection object."""
    client = mqtt.Client(client_id=client_id, clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    connection = client.connect(host, port, keepalive)
    return (client, connection)


def main():
    """The main event."""
    influxdb = InfluxConnection(db_host='localhost')

    def on_connect(client, userdata, flags, rc):
        """On Connect Function for MQTT Broker."""
        if rc == 0:
            print(f"Connected to MQTT Broker | {datetime.now()}")
            client.subscribe(CONNECTOR_MQTT_TOPIC, 2)
        else:
            print(f"Bad Connection Returned (Code: {rc})")
        pass

    def on_message(client, userdata, message):
        """On Message function for MQTT Broker."""
        initialTime = time.time()
        payload = message.payload.decode()
        print("----------Message Received----------")
        print(datetime.now())

        location, newDataIndexes = json.loads(payload)

        # Array to store converted Data that will all be pushed to influxDB
        # after all conversions.
        converted_data = []
        # Array that will store index information on the new data added to send
        # to inspector.
        inspectorPayload = []

        for adc_channel_pair in newDataIndexes:
            # Unpacking Dictionary
            adc = adc_channel_pair['adc']
            channel = adc_channel_pair['channel']
            newDataAmount = adc_channel_pair['amountOfData']

            # Running Query
            results = influxdb.get_n_recent_readings_with_condition(
                newDataAmount,
                adc,
                channel
            )

            # Parsing to actual data from results
            data = results[0]['values']

            # Getting name of sensor to add to array that will be sent
            sensorNames, _, _, = sensor_functions[adc][channel](data[0][1])

            # Building Array that will be sent to inspector
            if len(sensorNames) == 1:
                inspectorPayload.append(dict(
                    sensorName=sensorNames[0],
                    adc=adc,
                    channel=channel,
                    amountOfNewData=newDataAmount
                ))
            else:
                for sensor in sensorNames:
                    inspectorPayload.append(dict(
                        sensorName=sensor,
                        adc=adc,
                        channel=channel,
                        amountOfNewData=newDataAmount
                    ))

            # Converting data points for current ADC and Channel
            for i in range(newDataAmount):
                rawVoltageValue = data[i][1]
                timestamp = data[i][0]

                sensorName, units, converted = sensor_functions[adc][channel](
                    rawVoltageValue
                )

                # Handling Special Case where one sensor reading becomes
                # multiple data points
                # (i.e. MQ9 Sensor records 1 voltage --> 3 Gas Readings)
                lengthOfConverted = len(converted)
                if lengthOfConverted == 1:
                    newData = converted[0]
                    converted_data.append(dict(
                        adc=adc,
                        channel=channel,
                        sensorName=sensorName[0],
                        units=units[0],
                        timestamp=timestamp,
                        data=newData
                    ))
                else:
                    for j in range(lengthOfConverted):
                        newData = converted[j]
                        converted_data.append(dict(dict(
                            adc=adc,
                            channel=channel,
                            sensorName=sensorName[j],
                            units=units[j],
                            timestamp=timestamp,
                            data=newData
                        )))

        print(f"Conversions Done  | {time.time()-initialTime}")

        # Converting data into a pandas dataframe to be appended to database
        df = pd.DataFrame(converted_data)

        df['date_time'] = pd.to_datetime(df['timestamp'])
        # set a DateTime index and delete the old time_stamp columns
        df = df.set_index(pd.DatetimeIndex(df['date_time']))
        del df['timestamp'], df['date_time']
        # Seperate the dataframe by groups of adc'

        grouped = df.groupby(["sensorName", 'adc', 'channel', 'units'])
        print(f"Beginning to write to database | {time.time()-initialTime}")
        for group in grouped.groups:

            sensorName = group[0]
            adc = group[1]
            channel = group[2]
            units = group[3]

            tags = dict(sensorName=sensorName, adc=adc, channel=channel)

            sub_df = grouped.get_group(group)[['data']]
            sub_df.rename(
                columns={'date_time': 'date_time', 'data': str(units)},
                inplace=True
            )

            measurementName = location + "_" + sensorName

            influxdb.df_client.write_points(sub_df, measurementName, tags=tags)

        print(f"Written to database | {time.time()-initialTime}")

        # Potential Issue. Message still sends even if data fails to get pushed
        #  to influx because of try/except statement
        client.publish(
            INPECTOR_MQTT_TOPIC,
            json.dumps([location, inspectorPayload])
        )
        print(f"Published to Inspector  | {time.time()-initialTime}")
        print("\n")

    # Establish Connection to the MQTT Broker
    client, connection = connect_to_broker(
        client_id=MQTT_CLIENT_ID,
        host=BROKER_HOST,
        port=BROKER_PORT,
        keepalive=BROKER_KEEPALIVE,
        on_connect=on_connect,
        on_message=on_message
    )

    # Begin the connection loop, where within the loop, messages can be sent
    client.loop_forever()


if __name__ == "__main__":
    main()
