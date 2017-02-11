from django.db import models
import RPIO
import os
import glob
import time
import git


class Pin(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=False)
    pin_number = models.IntegerField(null=False)
    is_thermometer = models.BooleanField(default=False, null=False)

    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.is_thermometer:
            self.thermometer = Thermometer('28') #todo update this one day

    def get_direction(self):
        return RPIO.OUT if self.is_thermometer is False else RPIO.IN

    def get_temp(self):
        self.thermometer.refresh()

        return self.thermometer.celsius

    def get_state(self):
        try:
            return RPIO.input(self.pin_number)
        except:
            return None

    def get_state_opposite(self):
        return not self.get_state()

    def set_state(self, state):
        return RPIO.output(self.pin_number, RPIO.HIGH if state else RPIO.LOW)


class Thermometer(object):
    def __init__(self, serial):
        self.celsius = 0
        self.fahrenheit = 0
        self.serial = serial

        self.refresh()

    def read_temp_raw(self):
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '{serial}*'.format(serial=self.serial))[0]
        device_file = device_folder + '/w1_slave'

        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()

        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()

        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            self.celsius = round(temp_c, 1)

    def refresh(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        self.read_temp()


class Git(object):
    def __init__(self):
        self.repo = git.Repo(os.getcwd())
        self.branch = 'origin/master'

    def check(self):
        self.repo.remote().fetch()

        diff = self.repo.index.diff(self.branch)
        return bool(diff)

    def update(self):
        try:
            self.repo.remote().pull()
            return True
        except git.GitCommandError:
            return False
