# Generated by Django 3.2.12 on 2022-05-12 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0004_topic_public'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='text',
            new_name='entry',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='text',
            new_name='topic',
        ),
    ]