# Generated by Django 3.2.8 on 2023-03-07 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20230307_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='post/', verbose_name='Картинка'),
        ),
    ]
