# Generated by Django 5.0.3 on 2024-06-20 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_lead_cs_background'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='editing',
            field=models.BooleanField(default=False),
        ),
    ]