# Generated by Django 5.1.1 on 2024-09-16 18:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MCU_Regis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_antrean', models.IntegerField()),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('username', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=250)),
                ('role', models.IntegerField(choices=[(1, 'Doctor'), (2, 'User')], default=2)),
            ],
        ),
        migrations.CreateModel(
            name='MCU_Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal')], max_length=20)),
                ('no_document', models.CharField(max_length=50, unique=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('notes', models.TextField(blank=True, null=True)),
                ('id_mcu_regis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MCU.mcu_regis')),
                ('id_doctor', models.ForeignKey(limit_choices_to={'role': 1}, on_delete=django.db.models.deletion.CASCADE, to='MCU.users')),
            ],
        ),
        migrations.AddField(
            model_name='mcu_regis',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MCU.users'),
        ),
    ]
