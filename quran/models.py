"""
Models that represents The Holy Qur'an.
"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from api.models import BaseModel


class Juz(BaseModel):
    """
    A model that represents a part of the 30 parts of Quran.
    These columns were extracted from the models provided by King Fahd Glorious Qur'an
    Printing Complex as of 03/16/2022 (https://qurancomplex.gov.sa/techquran/dev/)
    """

    number_worded_ar = models.CharField(max_length=25, null=True, blank=True)
    number_worded_en = models.CharField(max_length=14, null=True, blank=True)
    number = models.PositiveSmallIntegerField(
        unique=True,
        editable=False,
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        verbose_name=_("The number of the part in the Quran. The maximum is 30."),
    )


class Sora(BaseModel):
    """
    A model that represents a chapter in the Quran.
    These columns were extracted from the models provided by King Fahd Glorious Qur'an
    Printing Complex as of 03/16/2022 (https://qurancomplex.gov.sa/techquran/dev/)
    """

    name_en = models.CharField(
        max_length=14,
        editable=False,
        unique=True,
        verbose_name=_(
            "Chapter name in English. The maximum length is 14 as of the current "
            "version."
        ),
    )
    name_ar = models.CharField(
        max_length=14,
        editable=False,
        unique=True,
        verbose_name=_(
            "Chapter name in Arabic in UthmanicHafs ttf font file with "
            "diacritics included. The maximum length is 14 as of the current version."
        ),
    )
    clean_name_ar = models.CharField(
        max_length=14,
        editable=False,
        unique=True,
        verbose_name=_(
            "Clean text of the chapter name in Arabic with no diacritics included."
        ),
    )
    number = models.PositiveSmallIntegerField(
        unique=True,
        editable=False,
        validators=[MinValueValidator(1), MaxValueValidator(114)],
        verbose_name=_(
            "The number of the chapter in the Quran. The maximum is 114 as the last "
            "chapter number is 114."
        ),
    )


class Aya(BaseModel):
    """
    A model that represents a verse in the Quran.
    These columns were interpreted from the models provided by King Fahd Glorious Qur'an
    Printing Complex as of 03/16/2022 (https://qurancomplex.gov.sa/techquran/dev/)
    """

    sora = models.ForeignKey(
        Sora, related_name="ayas", null=False, on_delete=models.PROTECT
    )
    juz = models.ForeignKey(
        Juz, related_name="ayas", null=False, on_delete=models.PROTECT
    )
    text = models.TextField(
        editable=False,
        verbose_name=_(
            "The actual text of the verse in UthmanicHafs ttf font file with "
            "diacritics included."
        ),
    )
    clean_text = models.TextField(
        editable=False,
        verbose_name=_(
            "Clean text of the Aya used for search purpose with no diacritics included."
        ),
    )
    number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(286)],
        verbose_name=_(
            "The number of the verse in the chapter. The maximum is 286 as the longest "
            "chapter only has 286 verses."
        ),
    )
    page = models.PositiveSmallIntegerField(
        editable=False,
        validators=[MinValueValidator(1), MaxValueValidator(604)],
        verbose_name=_("The page number this verse is in. The maximum is 604."),
    )
    line_start = models.PositiveSmallIntegerField(
        editable=False,
        validators=[MinValueValidator(1), MaxValueValidator(15)],
        verbose_name=_("Start line of the verse. The maximum is 15."),
    )
    line_end = models.PositiveSmallIntegerField(
        editable=False,
        validators=[MinValueValidator(1), MaxValueValidator(15)],
        verbose_name=_("End line of the verse. The maximum is 15."),
    )

    class Meta:
        unique_together = ["sora", "number"]
