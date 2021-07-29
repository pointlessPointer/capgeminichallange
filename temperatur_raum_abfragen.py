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

messwerte_indoor_pi = {
    "TVOC" : 0,
    "eCO2" : 0,
    "humidity" : 0,
    "temperature" : 0
    }

messwerte_outdoor_pi = {
    "TVOC" : 0,
    "eCO2" : 0,
    "humidity" : 0,
    "temperature" : 0
    }

#Temperatur, die im Raum angestrebt wird
room_temperature_want = 20.0
CO2_want = 800.0

room_has_pi = True

################################################################
#Notifications
################################################################
def send_open_window():
    print("Bitte öffnen Sie das Fenster.")


################################################################
#CO2 check
################################################################

#Ziel sollte sein, einen CO2-Wert von 1.000 ppm nicht zu überschreiten. 1.400 ppm ist die obere Grenze für akzeptable Raumluft.

def run_CO2():
    if messwerte_indoor_pi.get("eCO2") > CO2_want:
        send_open_window()


################################################################
#CO2 check
################################################################

#Ziel sollte sein, einen CO2-Wert von 1.000 ppm nicht zu überschreiten. 1.400 ppm ist die obere Grenze für akzeptable Raumluft.

def run_CO2():
    if messwerte_indoor_pi.get("eCO2") > CO2_want:
        send_open_window()



################################################################
#Temperature-Check
#Temperature to high or to low?
################################################################
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

def run_temperature_check():
    temperature = messwerte_room_sensors.get("temperature")
    outdoor_temperature = messwerte_Building.get("outdoorTemperature")
    window_open = messwerte_room_sensors.get("windowsOpen")

    check_temperature(temperature, room_temperature_want, temperature_difference, outdoor_temperature, window_open)




#Set functions
def set_messwerte_building(dictionary):
    messwerte_building = dictionary

def set_messwerte_room_sensors(dictionary):
    messwerte_room_sensors = dictionary

def set_messwerte_room_pi(dictionary):
    messwerte_room_pi = dictionary

def set_messwerte_outdoor_pi(dictionary):
    messwerte_room_pi = dictionary

def set_room_temperature(value):
    raum_temperatur = value

def set_room_has_pi(bool):
    room_has_pi = bool


################################################################
#Main Function
################################################################


def main():
    run_temperature_check()

    if room_has_pi:
        run_CO2()


if __name__ == "__main__":
    # execute only if run as a script
    main()