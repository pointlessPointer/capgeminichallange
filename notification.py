from enum import Enum
import datetime
ALARM = "ALARM"
WARNING = "WARNING"
SUGGESTION = "SUGGESTION"

class Notification:
    def __init__(self, severity:str, target:str="all", text="",timestamp=datetime.datetime.now()):
        self.severity=severity
        self.target=target
        self.timestamp=timestamp
        self.text=text

    def __eq__(self, other):
        if not type(other)==Notification:
            return False
        return self.severity == other.severity and self.target == other.target \
               and self.text == other.text

    def __hash__(self):
        return hash((self.severity, self.target, self.text))

    def send(self):
        print(f"{self.timestamp} {self.severity}@{self.target}: {self.text}")

    def __str__(self):
        f"{self.timestamp} {self.severity}@{self.target}: {self.text}"

class NotificationWatcher:
    def __init__(self):
        self.notifications = set()

    def set_notification(self, notification):
        if notification not in self.notifications:
            self.notifications.add(notification)
            notification.send()

    def reset_notification(self, notification):
        if notification in self.notifications:
            self.notifications.remove(notification)

if __name__ == '__main__':
    n1 = Notification("a","a")
    n2 = Notification("a","a")
    nw = NotificationWatcher()
    nw.set_notification(n1)
    nw.reset_notification(n1)
    pass
