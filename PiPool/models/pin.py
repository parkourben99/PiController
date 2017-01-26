from django.db import models
import RPIO
from datetime import datetime


class Pin(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    pin_number = models.IntegerField()
    is_thermometer = models.BooleanField(default=False)
    updated_at = models.DateTimeField()

    def get_state(self):
        return RPIO.input(self.pin_number)

    def set_state(self, state):
        RPIO.output(self.pin_number, state)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        super(Pin, self).save(force_insert, force_update, using, update_fields)
