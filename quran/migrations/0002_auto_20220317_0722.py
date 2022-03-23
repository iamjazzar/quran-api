"""
Initializes the database from hafsData_v18
"""

import json

from django.db import migrations
from django.conf import settings


def copy_ayas(apps, schema_editor):
    """
    Will copy the data from the hafsData_v18 JSON formatted file to our database.

    We can't import the models directly as they may be a newer
    version than this migration expects. We use the historical version.
    """
    Aya = apps.get_model("quran", "Aya")
    Sora = apps.get_model("quran", "Sora")
    Juz = apps.get_model("quran", "Juz")

    data_file = open(settings.BASE_DIR / "preflight" / "hafsData_v18.json")
    surahs_mapping_file = open(
        settings.BASE_DIR / "preflight" / "hafsData_clean_arabic_sura_v18.json"
    )

    ayas = json.load(data_file)
    surahs_mapping = json.load(surahs_mapping_file)

    for aya in ayas:
        juz, _ = Juz.objects.get_or_create(number=aya["jozz"])
        sora, _ = Sora.objects.get_or_create(
            number=aya["sora"],
            defaults={
                "name_en": aya["sora_name_en"],
                "name_ar": aya["sora_name_ar"],
                "clean_name_ar": surahs_mapping[aya["sora_name_ar"]],
            },
        )

        Aya.objects.create(
            sora=sora,
            juz=juz,
            text=aya["aya_text"],
            clean_text=aya["aya_text_emlaey"],
            number=aya["aya_no"],
            page=aya["page"],
            line_start=aya["line_start"],
            line_end=aya["line_end"],
        )


class Migration(migrations.Migration):
    """
    Runs the data migration of data copy
    """

    dependencies = [
        ("quran", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(copy_ayas),
    ]
