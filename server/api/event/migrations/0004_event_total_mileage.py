# Generated by Django 4.2.3 on 2024-02-25 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_event_team_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='total_mileage',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
