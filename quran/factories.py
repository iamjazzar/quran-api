import random

import factory
from factory.django import DjangoModelFactory

from quran import models


class JuzFactory(DjangoModelFactory):
    number = random.randrange(1, 30 + 1)

    class Meta:
        model = models.Juz


class SoraFactory(DjangoModelFactory):
    number = random.randrange(1, 114 + 1)

    class Meta:
        model = models.Sora


class AyaFactory(DjangoModelFactory):
    juz = factory.SubFactory(JuzFactory)
    sora = factory.SubFactory(SoraFactory)

    number = random.randrange(1, 286 + 1)
    page = random.randrange(1, 604 + 1)
    line_start = random.randrange(1, 15 + 1)
    line_end = random.randrange(1, 15 + 1)

    class Meta:
        model = models.Aya
