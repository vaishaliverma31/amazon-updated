# Generated by Django 3.2.4 on 2021-06-23 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0003_auto_20210623_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amazon_admin',
            name='state',
        ),
    ]
