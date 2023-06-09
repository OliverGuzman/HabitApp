# Generated by Django 4.1.7 on 2023-05-21 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('idHabit', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('habitDescription', models.CharField(max_length=256, verbose_name='Description')),
                ('habitPeriodicity', models.IntegerField()),
                ('habitStatus', models.BooleanField(default=False)),
            ],
        ),
    ]
