# Generated by Django 4.2.2 on 2023-07-28 08:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OKR', '0002_alter_objective_objective_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='okr',
            name='ratio',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
