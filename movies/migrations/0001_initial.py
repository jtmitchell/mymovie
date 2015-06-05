# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('poster', models.URLField(null=True, blank=True, max_length=255)),
                ('year', models.IntegerField(null=True, blank=True, verbose_name='Year of Release', db_index=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('notified', models.BooleanField(default=False)),
                ('notified_date', models.DateField(null=True, blank=True, help_text='Date when the notification was sent')),
                ('type', models.IntegerField(choices=[(0, 'Cinema'), (2, 'Retail Purchase')], db_index=True, default=0, help_text='Send notification when movie is available for ...')),
            ],
            options={
                'ordering': ('watchlist', 'type'),
            },
        ),
        migrations.CreateModel(
            name='ServiceMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('service_id', models.CharField(db_index=True, max_length=50)),
                ('service', models.CharField(choices=[('omdb', 'Open Movie Database')], db_index=True, default='omdb', max_length=10)),
                ('service_data', jsonfield.fields.JSONField(null=True, blank=True)),
                ('updated', models.DateField(null=True, blank=True, db_index=True)),
                ('movie', models.ForeignKey(to='movies.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('movie', models.ForeignKey(to='movies.Movie')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='watchlist',
            field=models.ForeignKey(to='movies.Watchlist'),
        ),
        migrations.AddField(
            model_name='movie',
            name='subscribers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='movies.Watchlist'),
        ),
        migrations.AlterUniqueTogether(
            name='servicemovie',
            unique_together=set([('service_id', 'service')]),
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('watchlist', 'type')]),
        ),
    ]
