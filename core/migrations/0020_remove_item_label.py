# Generated by Django 3.0 on 2020-05-11 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20200511_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='label',
        ),
    ]
