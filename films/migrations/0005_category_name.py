# Generated by Django 3.0.3 on 2020-12-10 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0004_remove_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='Категории'),
        ),
    ]