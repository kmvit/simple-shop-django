# Generated by Django 3.0 on 2020-05-07 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200507_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='discout_price',
            new_name='discount_price',
        ),
    ]