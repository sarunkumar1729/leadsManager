# Generated by Django 5.0.3 on 2024-06-20 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_notifications_date_alter_notifications_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]