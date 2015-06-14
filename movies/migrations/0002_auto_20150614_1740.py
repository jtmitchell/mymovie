# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.IntegerField(choices=[(0, 'Cinema'), (1, 'Retail Purchase'), (2, 'Rental'), (3, 'Online Streaming')], default=0, help_text='Send notification when movie is available for ...', db_index=True),
        ),
    ]
