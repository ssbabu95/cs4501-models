# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=16)),
                ('description', models.TextField(blank=True)),
                ('date_listed', models.DateTimeField()),
                ('available', models.BooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=40)),
                ('body', models.CharField(max_length=250)),
                ('review_rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=24)),
                ('date_joined', models.DateTimeField()),
                ('first_name', models.CharField(max_length=16)),
                ('last_name', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=16)),
                ('is_active', models.BooleanField()),
                ('type_of_user', models.CharField(choices=[('artist', 'Artist'), ('producer', 'Producer'), ('general', 'General')], default='general', max_length=16)),
                ('type_of_instrument', models.CharField(blank=True, null=True, max_length=16)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(to='cs4501.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='listing',
            name='creator',
            field=models.ForeignKey(to='cs4501.User'),
            preserve_default=True,
        ),
    ]
