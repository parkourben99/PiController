from django.db import models
try:
    import RPIO
except:
    class RPIO(object): pass


class Pin(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=False)
    pin_number = models.IntegerField(null=False)
    is_thermometer = models.BooleanField(default=False, null=False)

    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_temp(self):
        return 5

    def get_state(self):
        return False #RPIO.input(self.pin_number)

    def set_state(self, state):
        return True #RPIO.output(self.pin_number, state)
