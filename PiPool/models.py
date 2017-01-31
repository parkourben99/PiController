from django.db import models
import RPIO


class Pin(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=False)
    pin_number = models.IntegerField(null=False)
    is_thermometer = models.BooleanField(default=False, null=False)

    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        direction = RPIO.OUT if self.is_thermometer is False else RPIO.IN

        RPIO.setup(self.pin_number, direction)
        RPIO.output(self.pin_number, RPIO.HIGH)

    def get_temp(self):
        return 5

    def get_state(self):
        return RPIO.input(self.pin_number)

    def set_state(self, state):
        output = RPIO.HIGH if state is True else RPIO.LOW

        return RPIO.output(self.pin_number, output)
