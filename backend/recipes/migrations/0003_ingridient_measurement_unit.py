# Generated by Django 4.2.4 on 2023-08-31 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_rename_ingridients_recipe_ingridient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingridient',
            name='measurement_unit',
            field=models.CharField(default=1, max_length=20, verbose_name='Единица измерения'),
            preserve_default=False,
        ),
    ]