class RoomCheck:

    def __init__(self, temperature_difference, room_temperature_want, CO2_want, CO2_danger, humidity_want, TVOC_good, TVOC_danger):
        # Ab welchem Unterschied wird eine Notification rausgegeben?
        self.temperature_difference = temperature_difference

        self.room_temperature_want = room_temperature_want
        self.CO2_want = CO2_want
        self.CO2_danger = CO2_danger
        self.humidity_want = humidity_want
        self.TVOC_good = TVOC_good
        self.TVOC_danger = TVOC_danger

    ################################################################
    #Notifications
    ################################################################
    def send_open_window():
        print("Bitte öffnen Sie das Fenster.")

    def send_TVOC_outdoor_alarm():
        print("Bitte öffnen Sie keine Fenster.")

    def send_TVOC_indoor_alarm():
        print("Sehr hoher VOC-Wert im Raum, bitte verlassen Sie umgehend das Gebäude.")

    def send_CO2_indoor_alarm():
        print("Sehr hoher CO2-Wert im Raum, bitte verlassen Sie umgehend das Gebäude.")

    def send_temperature_indoor_alarm():
        print("Sehr hohe Temperatur im Raum, bitte verlassen Sie umgehend das Gebäude.")

    ################################################################
    #TVOC check
    ################################################################

    #Das Umweltbundesamt gibt Empfehlungen für das Vorkommen von Flüchtigen Organischen Verbindungen (VOCs) von hygienisch unbedenklich (unter 1 mg/m³ – unter 150 ppb) über hygienisch auffällig (zwischen 1 bis 3 mg/m³ – 150 bis 1300 ppb) bis hin zu hygienisch inakzeptabel (über 10 mg/m³ – über 1500 bis 4000 ppb)

    def check_outside_TVOC(self,messwerte_outdoor_pi):
        if messwerte_outdoor_pi.get("TVOC") > self.TVOC_danger:
            self.send_TVOC_outdoor_alarm()


    def check_inside_TVOC(self, messwerte_indoor_pi, messwerte_outdoor_pi):
        if messwerte_indoor_pi.get("TVOC") > self.TVOC_danger:
            self.send_TVOC_indoor_alarm()
        
        elif messwerte_indoor_pi.get("TVOC") > self.TVOC_good:
            if messwerte_outdoor_pi.get("TVOC") < messwerte_indoor_pi.get("TVOC"):
                self.send_open_window()


    ################################################################
    #CO2 check
    ################################################################

    #Ziel sollte sein, einen CO2-Wert von 1.000 ppm nicht zu überschreiten. 1.400 ppm ist die obere Grenze für akzeptable Raumluft.

    def run_CO2(self, messwerte_indoor_pi):

        if messwerte_indoor_pi.get("eCO2") > self.CO2_danger:
            self.send_CO2_indoor_alarm()

        if messwerte_indoor_pi.get("eCO2") > self.CO2_want:
            self.send_open_window()


    ################################################################
    #Humidity check
    ################################################################

    #Die optimale Luftfeuchtigkeit ist keine feste Größe, sondern eine prozentuale Spanne. Als optimal gilt eine relative Luftfeuchtigkeit von etwa 50%, mit einer Abweichung von +/- 10%.

    def run_humidity(self, messwerte_indoor_pi,messwerte_outdoor_pi):
        humidity_inside = messwerte_indoor_pi.get("humidity")
        humidity_outdoor = messwerte_outdoor_pi.get("humidity")
        
        #if humidity is too high
        if humidity_inside > humidity_inside + 10.0:

            if humidity_outdoor < humidity_inside:
                self.send_open_window()
        
        #if humidity is too low
        elif humidity_inside < humidity_inside - 10.0:
            if humidity_outdoor > humidity_inside:
                self.send_open_window()



    ################################################################
    #Temperature-Check
    #Temperature to high or to low?
    ################################################################
    def check_temperature(self, temperature, room_temperature_want, temperature_difference, outdoor_temperature, window_open):
        #check if room temperature too high
        if temperature > (room_temperature_want - temperature_difference):
            
            #if it is colder outside
            if outdoor_temperature < temperature:
                
                if window_open == False:
                    self.send_open_window()
            
            else:
                #send_run_air_conditioning()
                print("run air cond")
        
        #check if room temperature too low
        elif temperature < (room_temperature_want + temperature_difference):
            #if it is warmer outside
            if outdoor_temperature > temperature:
                if window_open == False:
                    self.send_open_window()
            
            else:
            #send_run_heating()
                print("run heating")

    def run_temperature_check(self, messwerte_room_sensors, messwerte_building):
        temperature = messwerte_room_sensors.get("temperature")
        outdoor_temperature = messwerte_building.get("outdoorTemperature")
        window_open = messwerte_room_sensors.get("windowsOpen")

        self.check_temperature(temperature, self.room_temperature_want, self.temperature_difference, outdoor_temperature, window_open)




    ################################################################
    #Main Function
    ################################################################


    def main(self, messwerte_building,messwerte_room_sensors, messwerte_indoor_pi, messwerte_outdoor_pi):
        
        self.run_temperature_check(messwerte_room_sensors, messwerte_building)

        if messwerte_indoor_pi:
            self.run_CO2(messwerte_indoor_pi)

            if messwerte_outdoor_pi:
                self.run_humidity(messwerte_indoor_pi,messwerte_outdoor_pi)


    if __name__ == "__main__":
        # execute only if run as a script
        main()