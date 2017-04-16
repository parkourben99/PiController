from django.core.management.base import BaseCommand, CommandError
from PiControl.models import TempControl


class Command(BaseCommand):
    help = 'Maintain the temp for the pool'

    def handle(self, *args, **options):
        TempControl.objects.first().maintain()

        self.stdout.write(self.style.SUCCESS('Success'))


# Rasberry Pi Spa Pool Controller
#
# Outputs to control:
# Relay Switching: Pump
# Relay Switching: Heater
#
# Inputs to Control
# Water Temp Thermometer
# Water Flow sensor (This is optional as its used so the heater cannot be turned on with out water flow from pump)
        # This can be done with a simple relay in the heater circut to take it out of the Rasberry Pi
#
#
# Web Login or App to control Set Temp of pool, Pump on/off, display current Water Temp
# Touch screen Control at the pool of these same settings plus * Settings
#
# The way the spa should operate is that it requires a minimum run time per 24hrs ie 2* hours (To allow for Filtering)
# This can but doesnt have to include time where the spa is set manually on (To have running while I sit in it)
# It needs to be able to automatically keep itself within a 2.5* degree range of a set temperature (automatically turning the pump and heater on and off)
# It needs to have Time bands* that it operates (When outside set Time bands the Pool doesnt need to filter or heat
# A Manual ON mode where the Pump runs but the Heater only runs as required
#
#
# *= adjustble through GUI on Touch screen

# crontab -e
# */3 * * * * python3 /home/PiPool/projects/PiController/manage.py control-temp