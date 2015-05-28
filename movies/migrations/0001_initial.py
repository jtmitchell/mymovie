# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('poster', models.URLField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('notified', models.BooleanField(default=False)),
                ('notified_date', models.DateField(help_text='Date when the notification was sent', null=True, blank=True)),
                ('type', models.IntegerField(help_text='Type of the notification', default=0, choices=[(0, 'Cinema'), (2, 'Retail Purchase')], db_index=True)),
            ],
            options={
                'ordering': ('watchlist', 'type'),
            },
        ),
        migrations.CreateModel(
            name='ServiceMovie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('service_id', models.CharField(max_length=50, db_index=True)),
                ('service', models.CharField(default='omdb', db_index=True, choices=[('omdb', 'Open Movie Database')], max_length=10)),
                ('movie', models.ForeignKey(to='movies.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
