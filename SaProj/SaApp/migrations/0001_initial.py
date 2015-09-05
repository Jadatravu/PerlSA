# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('revision', models.IntegerField(default=0)),
                ('build_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('file_name', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('sevierity', models.IntegerField(default=0)),
                ('build', models.ManyToManyField(to='SaApp.Build')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='build',
            unique_together=set([('name', 'revision', 'build_date')]),
        ),
    ]
