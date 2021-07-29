# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT


import sys
import pigpio
import time
import board
from pigpio_dht import DHT22

import ccs811LIBRARY


from datetime import datetime

# influxdb snippet
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "TCMe2_x68tFNRIjVqcvE56aMhy0u5X5y_UY-6ejXpc3-UvCVGg5Yy_NOjjoi8vOu5wy64EQM1t8x-fKGx-I6_Q=="
org = "org_dj"
bucket = "environment_monitoring"

client = InfluxDBClient(url="http://85.214.63.110:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)


# Initial the dht device, with data pin connected to:
gpio_dht22 = 4
sensor_dht22 = DHT22(gpio_dht22)
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)


sensor_ccs811 = ccs811LIBRARY.CCS811()
def setup(mode=1):
    print('Starting CCS811 Read')
    sensor_ccs811.configure_ccs811()
    sensor_ccs811.set_drive_mode(mode)

    if sensor_ccs811.check_for_error():
        sensor_ccs811.print_error()
        raise ValueError('Error at setDriveMode.')

    result = sensor_ccs811.get_base_line()
    sys.stdout.write("baseline for this sensor: 0x")
    if result < 0x100:
        sys.stdout.write('0')
    if result < 0x10:
        sys.stdout.write('0')
    sys.stdout.write(str(result) + "\n")


setup(1) # Setting mode


while True:
    try:
        # Print the values to the serial port
        reading = sensor_dht22.read()
        temperature_c = reading['temp_c']
        humidity = reading['humidity']
        print(f"tmp:{temperature_c}, hum: {humidity}")
        if sensor_ccs811.data_available():
            sensor_ccs811.read_logorithm_results()
            print("eCO2[%d] TVOC[%d]" % (sensor_ccs811.CO2, sensor_ccs811.tVOC))
        eCO2=sensor_ccs811.CO2
        TVOC=sensor_ccs811.tVOC

        if reading['valid'] and not sensor_ccs811.check_for_error():
            data = f"env,host=raspi1 temperature={temperature_c} humidity={humidity}"
            point = Point("environment")\
                .tag("host", "raspi1")\
                .field("temperature", temperature_c)\
                .field("humidity", humidity)\
                .field("eCO2", eCO2)\
                .field("TVOC", TVOC)\
                .time(datetime.utcnow(), WritePrecision.MS)

        write_api.write(bucket, org, point)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        raise error

    time.sleep(2.0)
