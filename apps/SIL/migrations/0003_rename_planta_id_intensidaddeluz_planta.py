# Generated by Django 4.2.3 on 2023-07-13 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SIL', '0002_intensidaddeluz_planta_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='intensidaddeluz',
            old_name='planta_id',
            new_name='planta',
        ),
    ]
