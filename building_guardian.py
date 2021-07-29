import api_communicator
import json
import time

check_interval = 5


def main():
    # read configs
    with open("buildingconfig.json", "r") as f:
        config = json.load(f)
    
    apicomm = api_communicator.Api_communicator(config)

    while True:
            api_json = apicomm.read_livedata(check_interval)
            apicomm.write_livedata_to_influx(api_json)
            pi_data = apicomm.read_most_recent_pi_data()
            outside_pi_key = config["pi_locations"].get("outside")
            if outside_pi_key:
                outside_pi = pi_data.get(outside_pi_key)


            building_data = api_json["building"]


            for roomdata in api_json["rooms"]:
                if roomdata["id"] in config["preferred_temperature"]:
                    pref_temp = config["preferred_temperature"][roomdata["id"]]
                else:
                    pref_temp = config["default_preferred_temperature"]
                room_pi_key = config["pi_locations"].get(roomdata["id"])
                room_pi = None
                if room_pi_key:
                    room_pi = pi_data.get(room_pi_key)

if __name__ == '__main__':
    main()