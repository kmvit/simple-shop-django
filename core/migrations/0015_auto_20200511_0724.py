# Generated by Django 3.0 on 2020-05-11 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200510_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='billing_adress',
            new_name='billing_address',
        ),
    ]
