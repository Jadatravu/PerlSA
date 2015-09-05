# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SaApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='sevierity',
            new_name='column',
        ),
        migrations.AddField(
            model_name='build',
            name='complete_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='issue',
            name='line',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='issue',
            name='severity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='issue',
            unique_together=set([('file_name', 'description', 'line', 'column')]),
        ),
    ]
