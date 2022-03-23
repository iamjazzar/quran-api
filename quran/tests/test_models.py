from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.forms import ValidationError
from django.test import TestCase

from quran.constants import LETTERS
from quran.factories import JuzFactory, SoraFactory
from quran.models import Aya, Juz, Sora


class TestJuz(TestCase):
    def test_count_30(self):
        self.assertEqual(30, Juz.objects.count())

    def test_number_unique(self):
        initial_count = Juz.objects.count()

        # Any number between 1 and 30 (inclusive) should cause a conflict
        with self.assertRaises(IntegrityError), transaction.atomic():
            JuzFactory.create(number=15)

        # The result shouldn't be saved
        self.assertEqual(initial_count, Juz.objects.count())

    def test_number_max_30(self):
        juz = JuzFactory.create(number=31)

        with self.assertRaises(ValidationError), transaction.atomic():
            juz.full_clean()

    def test_number_min_1(self):
        juz = JuzFactory.create(number=0)

        with self.assertRaises(ValidationError), transaction.atomic():
            juz.full_clean()


class TestSora(TestCase):
    def test_count_114(self):
        self.assertEqual(114, Sora.objects.count())

    def test_number_unique(self):
        initial_count = Sora.objects.count()

        # Any number between 1 and 114 (inclusive) should cause a conflict
        with self.assertRaises(IntegrityError), transaction.atomic():
            SoraFactory.create(number=57)

        # The result shouldn't be saved
        self.assertEqual(initial_count, Sora.objects.count())

    def test_number_max_114(self):
        sora = SoraFactory.create(number=115)

        with self.assertRaises(ValidationError), transaction.atomic():
            sora.full_clean()

    def test_number_min_1(self):
        sora = SoraFactory.create(number=0)

        with self.assertRaises(ValidationError), transaction.atomic():
            sora.full_clean()

    def test_clean_name_ar_no_diacritics(self):
        for sora in Sora.objects.all():
            clean_name = sora.clean_name_ar.replace(" ", "")
            letters_set = set(clean_name)
            self.assertTrue(letters_set.issubset(LETTERS))

    def test_clean_name_ar_max_length(self):
        max_length = 14

        for sora in Sora.objects.all():
            self.assertLessEqual(len(sora.clean_name_ar), max_length)

    def test_name_ar_max_length(self):
        max_length = 14

        for sora in Sora.objects.all():
            self.assertLessEqual(len(sora.name_ar), max_length)

    def test_name_en_max_length(self):
        max_length = 14

        for sora in Sora.objects.all():
            self.assertLessEqual(len(sora.name_en), max_length)


class TestAya(TestCase):
    def test_count_6236(self):
        self.assertEqual(6236, Aya.objects.count())

    def test_clean_text_no_diacritics(self):
        for aya in Aya.objects.all():
            clean_text = aya.clean_text.replace(" ", "")
            letters_set = set(clean_text)
            self.assertTrue(letters_set.issubset(LETTERS))

    def test_clean_text_not_null(self):
        for aya in Aya.objects.all():
            self.assertIsNotNone(aya.clean_text)

    def test_juz_remove_protection(self):
        with self.assertRaises(ProtectedError):
            Juz.objects.first().delete()

    def test_sora_remove_protection(self):
        with self.assertRaises(ProtectedError):
            Sora.objects.first().delete()


class TestAyaNotNone(TestCase):
    def test_clean_text_not_null(self):
        for aya in Aya.objects.all():
            self.assertIsNotNone(aya.clean_text)

    def test_text_not_null(self):
        for aya in Aya.objects.all():
            self.assertIsNotNone(aya.text)

    def test_sora_not_null(self):
        for aya in Aya.objects.all():
            self.assertIsNotNone(aya.sora)

    def test_juz_not_null(self):
        for aya in Aya.objects.all():
            self.assertIsNotNone(aya.juz)

    def test_number_not_null(self):
        for aya in Aya.objects.all():
            self.assertIsNotNone(aya.number)

    def test_page_not_null(self):
        for aya in Aya.objects.all():
            self.assertIsNotNone(aya.page)

    def test_line_start_not_null(self):
        for aya in Aya.objects.all():
            self.assertIsNotNone(aya.line_start)

    def test_line_end_not_null(self):
        for aya in Aya.objects.all():
            self.assertIsNotNone(aya.line_end)


class TestAyaValidations(TestCase):
    def test_number_min_1(self):
        aya = Aya.objects.first()
        aya.number = 0

        with self.assertRaises(ValidationError), transaction.atomic():
            aya.full_clean()

    def test_number_max_286(self):
        aya = Aya.objects.first()
        aya.number = 500

        with self.assertRaises(ValidationError), transaction.atomic():
            aya.full_clean()

    def test_page_min_1(self):
        aya = Aya.objects.first()
        aya.page = 0

        with self.assertRaises(ValidationError), transaction.atomic():
            aya.full_clean()

    def test_page_max_604(self):
        aya = Aya.objects.first()
        aya.page = 1000

        with self.assertRaises(ValidationError), transaction.atomic():
            aya.full_clean()

    def test_line_start_min_1(self):
        aya = Aya.objects.first()
        aya.line_start = 0

        with self.assertRaises(ValidationError), transaction.atomic():
            aya.full_clean()

    def test_line_start_max_15(self):
        aya = Aya.objects.first()
        aya.line_start = 20

        with self.assertRaises(ValidationError), transaction.atomic():
            aya.full_clean()

    def test_line_end_min_1(self):
        aya = Aya.objects.first()
        aya.line_end = 0

        with self.assertRaises(ValidationError), transaction.atomic():
            aya.full_clean()

    def test_line_end_max_15(self):
        aya = Aya.objects.first()
        aya.line_end = 20

        with self.assertRaises(ValidationError), transaction.atomic():
            aya.full_clean()
