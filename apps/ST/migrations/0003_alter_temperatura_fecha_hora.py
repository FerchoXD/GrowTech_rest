# Generated by Django 4.2.3 on 2023-07-19 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ST', '0002_temperatura_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperatura',
            name='fecha_hora',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
