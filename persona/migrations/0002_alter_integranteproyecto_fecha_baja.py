# Generated by Django 4.2.5 on 2023-10-13 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integranteproyecto',
            name='fecha_baja',
            field=models.DateField(blank=True, null=True),
        ),
    ]