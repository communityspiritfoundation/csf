# Generated by Django 4.2.2 on 2023-07-01 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254, unique=True)),
                ('join_code', models.CharField(default=None, unique=True)),
            ],
        ),
    ]