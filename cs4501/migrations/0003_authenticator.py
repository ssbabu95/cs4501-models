# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cs4501', '0002_auto_20150925_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('user_id', models.IntegerField()),
                ('authenticator', models.CharField(primary_key=True, serialize=False, max_length=128)),
                ('date_created', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
