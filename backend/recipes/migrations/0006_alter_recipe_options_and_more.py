# Generated by Django 4.2.4 on 2023-08-31 15:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_recipeingridients_ingredient_quantity_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterField(
            model_name='recipeingridients',
            name='ingredient_quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Колличество ингридиента'),
        ),
        migrations.AlterField(
            model_name='recipeingridients',
            name='ingridient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingridient', verbose_name='Ингридиент'),
        ),
        migrations.AlterField(
            model_name='recipeingridients',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название'),
        ),
    ]