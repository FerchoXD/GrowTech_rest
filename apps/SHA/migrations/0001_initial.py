# Generated by Django 4.2.3 on 2023-07-13 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plants', '0002_rename_usuario_planta_usuario_id_planta_nombreu'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumedadDeAmbiente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('fecha_hora', models.DateTimeField(auto_now_add=True)),
                ('planta', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='plants.planta')),
            ],
            options={
                'verbose_name': 'Humedad de ambiente',
                'verbose_name_plural': 'Humedades de ambiente',
            },
        ),
    ]
