# Generated by Django 3.2.12 on 2022-06-01 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0008_entry_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
