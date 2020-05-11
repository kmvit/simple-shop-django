# Generated by Django 3.0 on 2020-05-09 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_billingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_adress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.BillingAddress'),
        ),
    ]