# Generated by Django 4.2.2 on 2023-07-05 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OKR', '0005_remove_okr_formula_id_remove_okr_key_result_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='okr',
            name='files',
            field=models.URLField(),
        ),
    ]
