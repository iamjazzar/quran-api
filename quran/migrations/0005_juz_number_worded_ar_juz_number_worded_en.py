# Generated by Django 4.0.3 on 2022-03-26 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quran', '0004_auto_20220326_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='juz',
            name='number_worded_ar',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='juz',
            name='number_worded_en',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
