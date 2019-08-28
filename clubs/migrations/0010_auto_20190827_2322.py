# Generated by Django 2.2.4 on 2019-08-27 23:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0009_auto_20190825_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='favorite',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]