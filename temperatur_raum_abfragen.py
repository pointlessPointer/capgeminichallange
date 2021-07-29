#Constants
# Ab welchem Unterschied wird eine Notification rausgegeben?
temperature_difference = 2

messwerte_Building = {
    "totalPowerConsumption": 15.49,
    "powerConsumptionDataCenter": 14.78,
    "solarPowerOutput": 16.13,
    "outdoorTemperature": 25,
    "waterConsumption": 40.13,
    "totalEmployeesIn": 24
    }

# ein Beispielraum
messwerte_room_sensors = {
        "lightOn": False,
        "windowsOpen": False,
        "rollerBlindsClosed": False,
        "airConditioningRunning": False,
        "heaterRunning": True,
        "temperature": 20.369021225136912,
        "powerConsumption": 0.02785408418197808

    }

messwerte_room_pi = {
    "TVOC" : 0,
    "eCO2" : 0,
    "humidity" : 0,
    "temperature" : 0
    }

#Temperatur, die im Raum angestrebt wird
room_temperature_want = 30.0

#check if temperature too high or low
def check_temperature(temperature, room_temperature_want, temperature_difference, outdoor_temperature, window_open):
    #check if room temperature too high
    if temperature > (room_temperature_want - temperature_difference):
        
        #if it is colder outside
        if outdoor_temperature < temperature:
            
            if window_open == False:
                send_open_window()
        
        else:
            #send_run_air_conditioning()
            print("run air cond")
    
    #check if room temperature too low
    elif temperature < (room_temperature_want + temperature_difference):
        #if it is warmer outside
        if outdoor_temperature > temperature:
            if window_open == False:
                send_open_window()
        
        else:
           #send_run_heating()
            print("run heating")

def send_open_window():
    print("Bitte öffnen Sie das Fenster.")



#Set functions
def set_messwerte_building(dictionary):
    messwerte_building = dictionary

def set_messwerte_room_sensors(dictionary):
    messwerte_room_sensors = dictionary

def set_messwerte_room_pi(dictionary):
    messwerte_room_pi = dictionary

def set_room_temperature(value):
    raum_temperatur = value


def run_temperature_check():
    temperature = messwerte_room_sensors.get("temperature")
    outdoor_temperature = messwerte_Building.get("outdoorTemperature")
    window_open = messwerte_room_sensors.get("windowsOpen")

    check_temperature(temperature, room_temperature_want, temperature_difference, outdoor_temperature, window_open)


def main():
    run_temperature_check()

if __name__ == "__main__":
    # execute only if run as a script
    main()