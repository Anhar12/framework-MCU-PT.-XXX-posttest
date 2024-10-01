# Generated by Django 5.1.1 on 2024-10-01 17:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MCU', '0004_alter_result_id_mcu_regis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regis',
            name='id_user',
            field=models.ForeignKey(limit_choices_to={'is_superuser': False, 'role': 2}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
