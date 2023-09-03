# Generated by Django 4.2.4 on 2023-09-03 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0012_alter_favorite_recipe'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'ordering': ('recipe',), 'verbose_name': 'Ингридиент в рецепте', 'verbose_name_plural': 'Ингридиенты в рецепте'},
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.recipe', verbose_name='В избранном'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=200, verbose_name='Единица измерения'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, verbose_name='Цвет'),
        ),
    ]
