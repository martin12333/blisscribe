# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bliss_webapp', '0002_auto_20170902_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translationmodel',
            name='font_fam',
            field=models.CharField(choices=[(b'/Library/Fonts/Times New Roman.ttf', b'Times New Roman'), (b'/Library/Fonts/Arial.ttf', b'Arial'), (b'/Library/Fonts/Helvetica.dfont', b'Helvetica')], default=b'/Library/Fonts/Arial.ttf', max_length=30),
        ),
        migrations.AlterField(
            model_name='translationmodel',
            name='font_size',
            field=models.SmallIntegerField(default=12),
        ),
        migrations.AlterField(
            model_name='translationmodel',
            name='lang',
            field=models.CharField(choices=[(b'English', b'English'), (b'Spanish', b'Spanish'), (b'German', b'German'), (b'French', b'French'), (b'Italian', b'Italian'), (b'Dutch', b'Dutch'), (b'Polish', b'Polish')], default=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='translationmodel',
            name='page_nums',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='translationmodel',
            name='phrase',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='translationmodel',
            name='sub_all',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='translationmodel',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
