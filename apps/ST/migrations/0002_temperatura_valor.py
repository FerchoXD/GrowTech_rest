# Generated by Django 4.2.3 on 2023-07-13 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ST', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='temperatura',
            name='valor',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
