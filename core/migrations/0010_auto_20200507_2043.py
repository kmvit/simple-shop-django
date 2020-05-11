# Generated by Django 3.0 on 2020-05-07 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_auto_20200507_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='ordered',
            field=models.BooleanField(default=False, verbose_name='Заказал'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]