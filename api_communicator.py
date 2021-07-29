import requests
import datetime
import time

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#api config
basepoint="https://rvj6rnbpxj.execute-api.eu-central-1.amazonaws.com/prod/"

#influxdb config
token = "TCMe2_x68tFNRIjVqcvE56aMhy0u5X5y_UY-6ejXpc3-UvCVGg5Yy_NOjjoi8vOu5wy64EQM1t8x-fKGx-I6_Q=="
org = "org_dj"
bucket = "environment_monitoring"

client = InfluxDBClient(url="http://85.214.63.110:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


def read_livedata(interval=1):
    url=basepoint+"live-data"
    params={'interval':interval}
    r = requests.get(url, params)
    if not r.ok:
        return None
    else:
        return r.json()

def write_livedata_to_influx(api_json):
    building_Point = Point("building").tag("host", "api_scraper")#.time(datetime.utcfromtimestamp(api_json["samplingStartTime"]), WritePrecision.S)
    for k,v in api_json["building"].items():
        building_Point = building_Point.field(k,v)
    building_Point = building_Point.time(datetime.datetime.utcnow(), WritePrecision.MS)
    write_api.write(bucket, org, building_Point)

    for roomdata in api_json["rooms"]:
        room_point = Point("room").tag("host", "api_scraper").tag("id", roomdata["id"])
        room_point = room_point.time(datetime.datetime.utcnow(), WritePrecision.MS)
        for name in ["powerConsumption", "temperature", "workplaceReservations"]:
            room_point = room_point.field(name, roomdata[name])
        for sname, svalue in roomdata["sensors"].items():
            room_point = room_point.field(sname, roomdata["sensors"][sname])
        write_api.write(bucket, org, room_point)

def read_most_recent_pi_data()->dict:
    data_frame = query_api.query(f'from(bucket:"{bucket}")|>range(start:-1h)|>filter(fn: (r) => '
                                 f'r._measurement == "environment")'
                                 f'|>last()')
    pi_values = {}
    for table in data_frame:
        values = table.records[0].values
        if values["host"] not in pi_values:
            pi_values[values["host"]] = {}
        pi_values[values["host"]][values["_field"]]=values["_value"]
    return pi_values



if __name__ == '__main__':
    read_most_recent_pi_data()
    #while True:
    #    write_livedata_to_influx(read_livedata(interval=2))
    #    time.sleep(2)