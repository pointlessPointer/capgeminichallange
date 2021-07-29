import requests
import datetime
import time

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class Api_communicator:
    def __init__(self, config):
        #api config
        self.basepoint= config["basepoint"]

        #influxdb config
        self.token = config["token"]
        self.org = config["org"]
        self.bucket = config["bucket"]

        self.client = InfluxDBClient(url=config["influxdb_url"], token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()


    def read_livedata(self, interval=1):
        url=self.basepoint+"live-data"
        params={'interval':interval}
        r = requests.get(url, params)
        if not r.ok:
            return None
        else:
            return r.json()

    def write_livedata_to_influx(self, api_json):
        building_Point = Point("building").tag("host", "api_scraper")#.time(datetime.utcfromtimestamp(api_json["samplingStartTime"]), WritePrecision.S)
        for k,v in api_json["building"].items():
            building_Point = building_Point.field(k,v)
        building_Point = building_Point.time(datetime.datetime.utcnow(), WritePrecision.MS)
        self.write_api.write(self.bucket, self.org, building_Point)

        for roomdata in api_json["rooms"]:
            room_point = Point("room").tag("host", "api_scraper").tag("id", roomdata["id"])
            room_point = room_point.time(datetime.datetime.utcnow(), WritePrecision.MS)
            for name in ["powerConsumption", "temperature", "workplaceReservations"]:
                room_point = room_point.field(name, roomdata[name])
            for sname, svalue in roomdata["sensors"].items():
                room_point = room_point.field(sname, roomdata["sensors"][sname])
            self.write_api.write(self.bucket, self.org, room_point)

    def read_most_recent_pi_data(self)->dict:
        data_frame = self.query_api.query(f'from(bucket:"{self.bucket}")|>range(start:-1h)|>filter(fn: (r) => '
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
    pass
    #read_most_recent_pi_data()
    #while True:
    #    write_livedata_to_influx(read_livedata(interval=2))
    #    time.sleep(2)