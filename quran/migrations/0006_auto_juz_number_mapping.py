# Generated by Django 4.0.3 on 2022-03-26 21:13

import json
from django.conf import settings
from django.db import migrations


def add_juz_worded_number(apps, schema_editor):
    """
    Will add the name of the juz to Juz model.
    """
    Juz = apps.get_model("quran", "Juz")

    data_file = open(settings.BASE_DIR / "preflight" / "juz_number.json")

    juzs = json.load(data_file)
    for key, value in juzs.items():
        juz = Juz.objects.get(number=key)
        juz.number_worded_ar = value["ar"]
        juz.number_worded_en = value["en"]
        juz.save()


class Migration(migrations.Migration):

    dependencies = [
        ("quran", "0005_juz_number_worded_ar_juz_number_worded_en"),
    ]

    operations = [
        migrations.RunPython(add_juz_worded_number),
    ]