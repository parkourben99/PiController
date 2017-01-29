from PiPool.models import Pin
try:
    import RPIO
except:
    class RPIO(object): pass


class PinController(object):
    def __init__(self):
        self.set_all_pins()

        # for pin in self.my_pins:
        #     self.__setup_pin__(pin)

    def get_thermometers(self):
        return self.my_pins.filter(is_thermometer=True)

    def set_all_pins(self):
        self.my_pins = Pin.objects.all()

    def get_dashboard_data(self):
        data = {'thermometers': self.get_thermometers(), 'pins': self.my_pins.filter(is_thermometer=False)}

        return data

    def get_all_pins(self):
        return {'pins': self.my_pins}

    def __setup_pin__(self, pin):
        RPIO.setup(pin, RPIO.IN)

    def set_pin_state(self, pin_id, state):
        if pin_id or state is None:
            return False

        pin = self.my_pins.filter(id=pin_id)

        if pin is None:
            return False

        pin.set_state(state)

        if pin.get_state() == state:
            return True

        return False