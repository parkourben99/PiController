from PiPool.models import Pin


class PinController(object):
    def __init__(self):
        self.my_pins = Pin.objects.all()

    def get_thermometers(self):
        return self.my_pins.filter(is_thermometer=True)

    def get_dashboard_data(self):
        data = {'thermometers': self.get_thermometers()}

        return data
