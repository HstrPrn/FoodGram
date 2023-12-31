# Generated by Django 4.2.4 on 2023-09-04 21:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_alter_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', message='Цвет должен быть указан в Hex формате')], verbose_name='Цвет'),
        ),
    ]
