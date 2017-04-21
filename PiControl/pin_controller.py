from PiControl.models import Pin, TempControl
import rollbar
import sys
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
            try:
                RPIO.setup(pin.pin_number, pin.get_direction())

            except:
                rollbar.report_exc_info(sys.exc_info())
                self.my_pins.exclude(id=pin.id)

    def get_dashboard_data(self):
        temp_control = TempControl.objects.first()

        if not temp_control:
            rollbar.report_message("Unable to find the temp control, creating a new one")
            temp_control = TempControl()
            temp_control.name = "Control the spas temperature"
            temp_control.range = 2.5
            temp_control.temp = 23
            temp_control.temp_pin_id = 1
            temp_control.pump_pin_id = 2
            temp_control.heater_pin_id = 3
            temp_control.save(force_insert=True)

        data = {
            'thermometers': self.get_thermometers(),
            'pins': [], #self.my_pins.filter(is_thermometer=False),
            'temp_control': temp_control
        }

        return data

    def get_all_pins(self):
        return {'pins': self.my_pins}
