class Vehicle:
    def start(self):
        print("Vehicle Started")
    
    def stop(self):
        print("Vehicle Stopped")

class Car(Vehicle):
    def play_music(self):
        print("Playing Music")

class ElectricMixin():
    def start(self):
        print("Checking battery...")
        super().start()
        

class AutopilotMixin():
    def start(self):
        print("Calibrating sensors...")
        super().start()

class Tesla(AutopilotMixin, ElectricMixin, Car):
    pass

tesla = Tesla()
tesla.start()
tesla.play_music()
tesla.stop()
print(Tesla.mro())