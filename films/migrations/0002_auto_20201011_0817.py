# Generated by Django 3.1 on 2020-10-11 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.PositiveSmallIntegerField(default=2020, verbose_name='Дата выхода'),
        ),
    ]