# Generated by Django 3.0.8 on 2020-12-14 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0005_category_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ratingstar',
            options={'ordering': ['-value'], 'verbose_name': 'Звезда рейтинга', 'verbose_name_plural': 'Звезды рейтинга'},
        ),
    ]