# Generated by Django 3.0 on 2020-05-11 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20200511_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrendItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Бренд товара',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='item', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Изображение товара',
                'verbose_name_plural': 'Изображения товара',
            },
        ),
        migrations.RemoveField(
            model_name='item',
            name='character_item',
        ),
        migrations.AddField(
            model_name='item',
            name='brend_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.BrendItem', verbose_name='Бренд товара'),
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.ImageItem', verbose_name='Изображение'),
        ),
    ]
