# Generated by Django 3.2.4 on 2021-06-28 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0007_auto_20210624_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='amazon_admin',
            name='Active',
            field=models.BooleanField(default=False),
        ),
    ]
