# Generated by Django 3.2.12 on 2022-05-12 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_topic_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
