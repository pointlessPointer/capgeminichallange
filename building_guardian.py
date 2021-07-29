import api_communicator
import json
import time

check_interval = 5


def main():
    # read configs
    with open("buildingconfig.json", "r") as f:
        config = json.load(f)

    while True:

            api_json = api_communicator.read_livedata(check_interval)
            api_communicator.write_livedata_to_influx(api_json)
            pi_data = api_communicator.read_most_recent_pi_data()
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
                print(f"call checks with bd:{building_data}, rd:{roomdata}, op:{outside_pi}, rp:{room_pi}, pt: {pref_temp}")
                pass

if __name__ == '__main__':
    main()