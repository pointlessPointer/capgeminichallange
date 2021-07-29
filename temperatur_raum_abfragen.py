import notification
import datetime

class RoomCheck:

    def __init__(self, temperature_difference, CO2_want, CO2_danger, humidity_want, TVOC_good, TVOC_danger):
        # Ab welchem Unterschied wird eine Notification rausgegeben?
        self.temperature_difference = temperature_difference


        self.CO2_want = CO2_want
        self.CO2_danger = CO2_danger
        self.humidity_want = humidity_want
        self.TVOC_good = TVOC_good
        self.TVOC_danger = TVOC_danger

        self.NotificationWatcher = notification.NotificationWatcher()

    ################################################################
    #Notifications
    ################################################################
    def send_open_window(self):
        print("Bitte öffnen Sie das Fenster.")
        window_notification = notification.Notification("SUGGESTION", "all in room", "Bitte öffnen Sie das Fenster.",timestamp=datetime.datetime.now())
        self.NotificationWatcher.set_notification(window_notification)

    def send_TVOC_outdoor_alarm(self):
        print("Bitte öffnen Sie keine Fenster.")
        TVOC_oudoor_notification = notification.Notification("ALARM", "all in room", "Bitte öffnen Sie keine Fenster.",timestamp=datetime.datetime.now())
        self.NotificationWatcher.set_notification(TVOC_oudoor_notification)

    def send_TVOC_indoor_alarm(self):
        print("Sehr hoher VOC-Wert im Raum, bitte verlassen Sie umgehend das Gebäude.")
        TVOC_indoor_notification = notification.Notification("ALARM", "all", "Sehr hoher VOC-Wert im Raum, bitte verlassen Sie umgehend das Gebäude.",timestamp=datetime.datetime.now())
        self.NotificationWatcher.set_notification(TVOC_indoor_notification)

    def send_CO2_indoor_alarm(self):
        print("Sehr hoher CO2-Wert im Raum, bitte verlassen Sie umgehend das Gebäude.")
        CO2_indoor_notification = notification.Notification("ALARM", "all", "Sehr hoher CO2-Wert im Raum, bitte verlassen Sie umgehend das Gebäude.",timestamp=datetime.datetime.now())
        self.NotificationWatcher.set_notification(CO2_indoor_notification)

    def send_temperature_indoor_alarm(self):
        print("Sehr hohe Temperatur im Raum, bitte verlassen Sie umgehend das Gebäude.")
        temperature_indoor_notification = notification.Notification("ALARM", "all", "Sehr hohe Temperatur im Raum, bitte verlassen Sie umgehend das Gebäude.",timestamp=datetime.datetime.now())
        self.NotificationWatcher.set_notification(temperature_indoor_notification)

    ################################################################
    #TVOC check
    ################################################################

    #Das Umweltbundesamt gibt Empfehlungen für das Vorkommen von Flüchtigen Organischen Verbindungen (VOCs) von hygienisch unbedenklich (unter 1 mg/m³ – unter 150 ppb) über hygienisch auffällig (zwischen 1 bis 3 mg/m³ – 150 bis 1300 ppb) bis hin zu hygienisch inakzeptabel (über 10 mg/m³ – über 1500 bis 4000 ppb)

    def check_outside_TVOC(self,messwerte_outdoor_pi):
        TVOC_oudoor_notification = notification.Notification("ALARM", "all in room", "Bitte öffnen Sie keine Fenster. (Hoher VOC-Wert)",timestamp=datetime.datetime.now())

        if messwerte_outdoor_pi.get("TVOC") > self.TVOC_danger:  
            self.NotificationWatcher.set_notification(TVOC_oudoor_notification)

        else:  
            self.NotificationWatcher.reset_notification(TVOC_oudoor_notification)


    def check_inside_TVOC(self, messwerte_indoor_pi, messwerte_outdoor_pi):
        TVOC_indoor_notification = notification.Notification("ALARM", "all", "Sehr hoher VOC-Wert im Raum, bitte verlassen Sie umgehend das Gebäude.",timestamp=datetime.datetime.now())
        window_notification = notification.Notification("SUGGESTION", "all in room", "Bitte öffnen Sie das Fenster. (VOC-Wert zu hoch)",timestamp=datetime.datetime.now())

        if messwerte_indoor_pi.get("TVOC") > self.TVOC_danger:
            
            self.NotificationWatcher.set_notification(TVOC_indoor_notification)
        
        else:
            self.NotificationWatcher.reset_notification(TVOC_indoor_notification)
        
        if messwerte_indoor_pi.get("TVOC") > self.TVOC_good:
           

            if messwerte_outdoor_pi.get("TVOC") < messwerte_indoor_pi.get("TVOC"):
                
                self.NotificationWatcher.set_notification(window_notification)
            
        else:
            self.NotificationWatcher.reset_notification(window_notification)


    ################################################################
    #CO2 check
    ################################################################

    #Ziel sollte sein, einen CO2-Wert von 1.000 ppm nicht zu überschreiten. 1.400 ppm ist die obere Grenze für akzeptable Raumluft.

    def run_CO2(self, messwerte_indoor_pi, room_id="all in room"):

        CO2_indoor_notification = notification.Notification("ALARM", "all", "Sehr hoher CO2-Wert im Raum, bitte verlassen Sie umgehend das Gebäude.",timestamp=datetime.datetime.now())
        
        if messwerte_indoor_pi.get("eCO2") > self.CO2_danger:
            
            self.NotificationWatcher.set_notification(CO2_indoor_notification)

        else:
            self.NotificationWatcher.reset_notification(CO2_indoor_notification)

        window_notification = notification.Notification("SUGGESTION", room_id, "Bitte öffnen Sie das Fenster. (Der CO2-Wert ist hoch)",timestamp=datetime.datetime.now())
        
        if messwerte_indoor_pi.get("eCO2") > self.CO2_want:
            
            self.NotificationWatcher.set_notification(window_notification)

        else:
            self.NotificationWatcher.set_notification(window_notification)


    ################################################################
    #Humidity check
    ################################################################

    #Die optimale Luftfeuchtigkeit ist keine feste Größe, sondern eine prozentuale Spanne. Als optimal gilt eine relative Luftfeuchtigkeit von etwa 50%, mit einer Abweichung von +/- 10%.

    def run_humidity(self, messwerte_indoor_pi,messwerte_outdoor_pi):
        humidity_inside = messwerte_indoor_pi.get("humidity")
        humidity_outdoor = messwerte_outdoor_pi.get("humidity")
        
        #if humidity is too high
        if humidity_inside > humidity_inside + 10.0:
            window_notification = notification.Notification("SUGGESTION", "all in room", "Bitte öffnen Sie das Fenster. (Luftfeuchtigkeit zu hoch)",timestamp=datetime.datetime.now())
            if humidity_outdoor < humidity_inside:
                
                self.NotificationWatcher.set_notification(window_notification)

            else:
                self.NotificationWatcher.reset_notification(window_notification)

        
        #if humidity is too low
        elif humidity_inside < humidity_inside - 10.0:
            window_notification = notification.Notification("SUGGESTION", "all in room", "Bitte öffnen Sie das Fenster. (Luftfeuchtigkeit zu niedrig)",timestamp=datetime.datetime.now())
            if humidity_outdoor > humidity_inside:
                self.NotificationWatcher.set_notification(window_notification)

            else:
                self.NotificationWatcher.reset_notification(window_notification)



    ################################################################
    #Temperature-Check
    #Temperature to high or to low?
    ################################################################
    def check_temperature(self, temperature, room_temperature_want, temperature_difference, outdoor_temperature, window_open, room_id="all in room"):
        #check if room temperature too high
        if temperature > (room_temperature_want - temperature_difference):
            
            #if it is colder outside
            if outdoor_temperature < temperature:
                window_notification = notification.Notification("SUGGESTION", room_id, "Bitte öffnen Sie das Fenster. (Temperatur ist hoch)",timestamp=datetime.datetime.now())
                
                if window_open == False:
                    self.NotificationWatcher.set_notification(window_notification)

                else:
                    self.NotificationWatcher.reset_notification(window_notification)
                    
            
            else:
                #send_run_air_conditioning()
                print("run air cond")
        
        #check if room temperature too low
        elif temperature < (room_temperature_want + temperature_difference):
            #if it is warmer outside
            if outdoor_temperature > temperature:
                window_notification = notification.Notification("SUGGESTION", "all in room", "Bitte öffnen Sie das Fenster. (Temperatur ist niedrig)",timestamp=datetime.datetime.now())
                
                if window_open == False:
                    self.NotificationWatcher.set_notification(window_notification)

                else:
                    self.NotificationWatcher.reset_notification(window_notification)
            
            else:
            #send_run_heating()
                print("run heating")

    def run_temperature_check(self, messwerte_room_sensors, messwerte_building, room_temperature_want):
        temperature = messwerte_room_sensors.get("temperature")
        outdoor_temperature = messwerte_building.get("outdoorTemperature")
        window_open = messwerte_room_sensors.get("windowsOpen")

        self.check_temperature(temperature, room_temperature_want, self.temperature_difference, outdoor_temperature, window_open, room_id=messwerte_room_sensors["id"])


    ################################################################
    #Heizung und Klimaanlage
    ################################################################

    def check_heating_aircond(self,messwerte_room_sensors):
        window_notification = notification.Notification("WARNING", "all in room", "Heizung und Klimaanlage laufen beide!",timestamp=datetime.datetime.now())
        if messwerte_room_sensors.get("heaterRunning"):
            if messwerte_room_sensors.get("airConditioningRunning"):
                self.NotificationWatcher.set_notification(window_notification)
        
        if not messwerte_room_sensors.get("heaterRunning"):
            if not messwerte_room_sensors.get("airConditioningRunning"):
                self.NotificationWatcher.reset_notification(window_notification)
            
        

        
                



    ################################################################
    #Main Function
    ################################################################


    def main(self, messwerte_building,messwerte_room_sensors, messwerte_indoor_pi, messwerte_outdoor_pi, room_temperature_want):
        
        self.run_temperature_check(messwerte_room_sensors, messwerte_building,room_temperature_want)
        self.check_heating_aircond(messwerte_room_sensors)

        if messwerte_indoor_pi:
            self.run_CO2(messwerte_indoor_pi, room_id=messwerte_room_sensors["id"])
             

            if messwerte_outdoor_pi:
                self.run_humidity(messwerte_indoor_pi,messwerte_outdoor_pi)
                self.check_inside_TVOC(messwerte_indoor_pi, messwerte_outdoor_pi)

        if messwerte_outdoor_pi:
            self.check_outside_TVOC(messwerte_outdoor_pi)


