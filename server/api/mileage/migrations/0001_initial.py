# Generated by Django 4.2.2 on 2023-07-04 10:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mileage',
            fields=[
                ('mileage_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('kilometres', models.IntegerField()),
                ('date', models.DateField(default=datetime.date.today)),
            ],
        ),
    ]
