from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PiControl', '0002_pin_tempcontrol'),
        ('PiControl', '0003_time_bands_changes_to_tempcontro'),
    ]

    operations = [
        migrations.AddField(
            model_name='TempControl',
            name='manuel_off_at',
            field=models.DateTimeField(null=True)
        ),
        migrations.AddField(
            model_name='TempControl',
            name='manuel_off',
            field=models.BooleanField(default=False)
        ),
    ]
