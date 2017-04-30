from django.core.management.base import BaseCommand, CommandError
from PiControl.models import TempControl
import rollbar
from django.conf import settings


class Command(BaseCommand):
    help = 'Maintain the temp for the pool'

    def handle(self, *args, **options):
        try:
            rollbar.init(settings.ROLLBAR['access_token'])
            TempControl.objects.first().maintain()
        except:
            rollbar.report_exc_info()
            rollbar.report_message('maintain command failure')

        self.stdout.write(self.style.SUCCESS('Success'))
