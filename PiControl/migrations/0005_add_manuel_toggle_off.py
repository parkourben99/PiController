from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('PiControl', '0004_merge_20170416_1556'),
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
