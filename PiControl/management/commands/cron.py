from django.core.management.base import BaseCommand
from PiControl.models import Schedule, ScheduleHistory
import rollbar
from django.conf import settings


class Command(BaseCommand):
    help = 'cron for schedule'

    def handle(self, *args, **options):
        rollbar.init(settings.ROLLBAR['access_token'])

        self.stdout.write(self.style.SUCCESS('Success'))