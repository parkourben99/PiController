from decimal import Decimal
from django.db import models
import os
import glob
import time
import git
import datetime
import RPIO
import rollbar


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
            try:
                self.thermometer = Thermometer('28')  # todo update this one day
            except:
                # rollbar.report_exc_info()
                # rollbar.report_message('could not set thermometer')
                self.thermometer = None

    def get_direction(self):
        return RPIO.OUT if self.is_thermometer is False else RPIO.IN

    def get_temp(self):
        if self.thermometer:
            self.thermometer.refresh()
            return self.thermometer.celsius

        return '?'

    def get_state(self):
        try:
            return RPIO.input(self.pin_number)
        except:
            rollbar.report_message('could not get_state')
            return None

    def get_state_opposite(self):
        return not self.get_state()

    def set_state(self, state):
        return RPIO.output(self.pin_number, RPIO.HIGH if state else RPIO.LOW)

    def set_state_upside_down(self, state):
        return RPIO.output(self.pin_number, RPIO.HIGH if not state else RPIO.LOW)


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
            self.fahrenheit = ((self.celsius * 9) / 5.0) + 32

    def refresh(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        self.read_temp()


class Git(object):
    def __init__(self):
        self.repo = git.Repo(os.getcwd())
        self.branch = 'origin/PiPool'

    def check(self):
        self.repo.remote().fetch()

        diff = self.repo.index.diff(self.branch)
        return bool(diff)

    def update(self):
        try:
            self.repo.remote().pull()
            return True
        except git.GitCommandError:
            rollbar.report_message('could not update git')
            return False


class TimeBand(models.Model):
    start_at = models.TimeField(null=True)
    end_at = models.TimeField(null=True)
    day_of_week = models.IntegerField(null=False)
    active = models.BooleanField(default=True, null=False)


class TempControl(models.Model):
    name = models.CharField(max_length=200, null=False)
    manuel = models.BooleanField(default=False, null=False)
    manuel_at = models.DateTimeField(null=True)
    temp = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    range = models.DecimalField(max_digits=5, decimal_places=2, null=False, default=2)
    temp_pin_id = models.IntegerField(null=False)
    pump_pin_id = models.IntegerField(null=False)
    heater_pin_id = models.IntegerField(null=False)

    def __get_pin(self, id):
        return Pin.objects.filter(id=id).first()

    def __get_manuel_period(self):
        return 30

    def __allowed_to_run(self):
        now = datetime.datetime.now()
        time = now.time()
        result = False

        time_bands = TimeBand.objects.filter(active=True)

        for time_band in time_bands:
            if now.day == time_band.day_of_week:
                if time > time_band.start_at and time < time_band.end_at:
                    result = True
                    break

        return result

    def maintain(self):
        if self.manuel:
            future = datetime.datetime.now() + datetime.timedelta(minutes=self.__get_manuel_period())
            self.manuel_at = self.manuel_at.replace(tzinfo=None)
            future = future.replace(tzinfo=None)

            if self.manuel_at > future:
                self.manuel = False
                self.manuel_at = None
                self.save()

                self.__turn_off()
                return
        else:
            pass
            # todo finish: create view and way to edit
            # if not self.__allowed_to_run:
            #     self.__turn_off()
            #     return

        pin = self.__get_pin(self.temp_pin_id)

        if not pin:
            Exception("No pins has been set, unable to maintain")
        else:
            temp = Decimal(pin.get_temp())
            cold = self.temp - self.range

            if temp <= cold:
                self.__turn_on()
                return

            if temp >= self.temp:
                self.__turn_off()
                return

    def outside_turn_on(self):
        self.__set_state(True)

    def __turn_on(self):
        self.__set_state(True)

    def __turn_off(self):
        self.__set_state(False)

    def __set_state(self, state):
        pump = self.__get_pin(self.pump_pin_id)
        heater = self.__get_pin(self.heater_pin_id)

        if self.manuel:
            pump.set_state_upside_down(True)
            pump.set_state_upside_down(state)
        else:
            if state:
                pump.set_state_upside_down(state)
                time.sleep(3)
                heater.set_state_upside_down(state)
            else:
                heater.set_state_upside_down(state)
                time.sleep(3)
                pump.set_state_upside_down(state)
