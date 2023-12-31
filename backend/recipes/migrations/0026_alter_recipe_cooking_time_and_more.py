# Generated by Django 4.2.4 on 2023-09-25 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0025_alter_recipe_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(verbose_name='Время готовки'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient_quantity',
            field=models.PositiveSmallIntegerField(verbose_name='Колличество ингредиента'),
        ),
    ]
