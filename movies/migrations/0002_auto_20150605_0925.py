# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.IntegerField(db_index=True, blank=True, verbose_name='Year of Release', null=True),
        ),
        migrations.AddField(
            model_name='servicemovie',
            name='service_data',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='servicemovie',
            name='updated',
            field=models.DateField(db_index=True, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.IntegerField(db_index=True, default=0, choices=[(0, 'Cinema'), (2, 'Retail Purchase')], help_text='Send notification when movie is available for ...'),
        ),
    ]
