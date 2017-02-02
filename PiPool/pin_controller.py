from PiPool.models import Pin
import RPIO


class PinController(object):
    def __init__(self):
        RPIO.setmode(RPIO.BCM)

        self.my_pins = None
        self.set_all_pins()

    def get_thermometers(self):
        return self.my_pins.filter(is_thermometer=True)

    def set_all_pins(self):
        RPIO.cleanup()

        self.my_pins = Pin.objects.all()

        for pin in self.my_pins:
            RPIO.setup(pin.pin_number, pin.get_direction())
            RPIO.output(pin.pin_number, RPIO.HIGH)

    def get_dashboard_data(self):
        data = {'thermometers': self.get_thermometers(), 'pins': self.my_pins.filter(is_thermometer=False)}

        return data

    def get_all_pins(self):
        return {'pins': self.my_pins}
