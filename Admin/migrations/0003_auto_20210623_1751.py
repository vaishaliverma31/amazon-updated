# Generated by Django 3.2.4 on 2021-06-23 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.in_.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Admin', '0002_alter_amazon_admin_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='amazon_admin',
            name='password',
            field=models.CharField(blank=True, editable=False, max_length=300, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='amazon_admin',
            name='state',
            field=localflavor.in_.models.INStateField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='amazon_admin',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
