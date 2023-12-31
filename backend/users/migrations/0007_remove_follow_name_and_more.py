# Generated by Django 4.2.4 on 2023-09-05 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_password'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='name',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(('user', models.F('author')), _negated=True), name='check_self_follow_constraint'),
        ),
    ]
