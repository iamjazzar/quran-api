from random import randrange
from uuid import uuid4

from django.test import TestCase
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from rest_framework import status

from quran.models import Aya, Juz, Sora
from quran.pagination import NumberCursorPagination


class TestJuzViewSet(TestCase):
    def test_list(self):
        url = reverse("quran:juz-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        # All 30 Juz's are available
        self.assertEqual(30, len(response.data["results"]))

        # Pagination is 100 item/page, we have 30 Juz's only
        self.assertIn("next", response.data)
        self.assertIsNone(response.data["next"])

        self.assertIn("previous", response.data)
        self.assertIsNone(response.data["previous"])

    def test_retrieve(self):
        juz_number = 13
        url = reverse("quran:juz-detail", kwargs={"number": juz_number})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(6, len(response.data))

        instance = Juz.objects.get(number=juz_number)
        self.assertEqual(str(instance.id), response.data["id"])
        self.assertEqual(instance.number, response.data["number"])
        self.assertEqual(instance.number_worded_ar, response.data["number_worded_ar"])
        self.assertEqual(instance.number_worded_en, response.data["number_worded_en"])
        self.assertEqual(instance.created, parse_datetime(response.data["created"]))
        self.assertEqual(instance.updated, parse_datetime(response.data["updated"]))

    def test_delete(self):
        juz_number = 13
        url = reverse("quran:juz-detail", kwargs={"number": juz_number})
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )

        # Make sure instance still exists
        Juz.objects.get(number=juz_number)

    def test_create(self):
        juz_number = 31
        url = reverse("quran:juz-list")
        response = self.client.post(url, data={"number": juz_number})

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )

        # Make sure it wasn't created
        with self.assertRaises(Juz.DoesNotExist):
            Juz.objects.get(number=juz_number)

    def test_update(self):
        juz_number = 13
        url = reverse("quran:juz-detail", kwargs={"number": juz_number})

        response = self.client.patch(url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )

        response = self.client.put(url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )


class TestAyaViewSet(TestCase):
    def test_list(self):
        url = reverse("quran:aya-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        # The first 100 Aya's only in the first page
        self.assertEqual(100, len(response.data["results"]))

        # Pagination is 100 item/page, still have more to show
        self.assertIn("next", response.data)
        self.assertIsNotNone(response.data["next"])

        self.assertIn("previous", response.data)
        self.assertIsNone(response.data["previous"])

    def test_pagination_max(self):
        url = reverse("quran:aya-list")
        query = (
            f"?{NumberCursorPagination.page_size_query_param}"
            f"={NumberCursorPagination.max_page_size}"
        )
        response = self.client.get(url + query)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(
            NumberCursorPagination.max_page_size, len(response.data["results"])
        )

    def test_pagination_specific(self):
        url = reverse("quran:aya-list")
        results_per_page = 10
        query = f"?{NumberCursorPagination.page_size_query_param}={results_per_page}"
        response = self.client.get(url + query)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(results_per_page, len(response.data["results"]))

    def test_retrieve(self):
        # Pick a random aya
        aya = Aya.objects.order_by("?").first()

        url = reverse("quran:aya-detail", kwargs={"pk": aya.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(11, len(response.data))

        instance = Aya.objects.get(pk=aya.pk)
        self.assertEqual(str(instance.id), response.data["id"])
        self.assertEqual(instance.sora.number, response.data["sora"])
        self.assertEqual(instance.juz.number, response.data["juz"])
        self.assertEqual(instance.text, response.data["text"])
        self.assertEqual(instance.clean_text, response.data["clean_text"])
        self.assertEqual(instance.number, response.data["number"])
        self.assertEqual(instance.page, response.data["page"])
        self.assertEqual(instance.line_start, response.data["line_start"])
        self.assertEqual(instance.line_end, response.data["line_end"])

        self.assertEqual(instance.created, parse_datetime(response.data["created"]))
        self.assertEqual(instance.updated, parse_datetime(response.data["updated"]))

    def test_delete(self):
        # Pick a random aya
        aya = Aya.objects.order_by("?").first()
        url = reverse("quran:aya-detail", kwargs={"pk": aya.pk})
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )

        # Make sure instance still exists
        Aya.objects.get(pk=aya.pk)

    def test_create(self):
        url = reverse("quran:aya-list")
        new_object_id = uuid4()

        response = self.client.post(
            url,
            data={
                "id": new_object_id,
                "text": "text",
                "clean_text": "clean_text",
                "number": "number",
                "page": "page",
                "line_start": "line_start",
                "line_end": "line_end",
            },
        )

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )

        # Make sure it wasn't created
        with self.assertRaises(Aya.DoesNotExist):
            Aya.objects.get(pk=new_object_id)

    def test_update(self):
        # Pick a random aya
        aya = Aya.objects.order_by("?").first()
        url = reverse("quran:aya-detail", kwargs={"pk": aya.pk})

        response = self.client.patch(url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )

        response = self.client.put(url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )


class TestSoraViewSet(TestCase):
    def test_list(self):
        url = reverse("quran:sora-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        # The first 100 Soras only in the first page
        self.assertEqual(100, len(response.data["results"]))

        # Pagination is 100 item/page, still have more to show
        self.assertIn("next", response.data)
        self.assertIsNotNone(response.data["next"])

        self.assertIn("previous", response.data)
        self.assertIsNone(response.data["previous"])

    def test_pagination_max(self):
        url = reverse("quran:sora-list")
        query = (
            f"?{NumberCursorPagination.page_size_query_param}"
            f"={NumberCursorPagination.max_page_size}"
        )
        response = self.client.get(url + query)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(114, len(response.data["results"]))

    def test_pagination_specific(self):
        url = reverse("quran:sora-list")
        results_per_page = 10
        query = f"?{NumberCursorPagination.page_size_query_param}={results_per_page}"
        response = self.client.get(url + query)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(results_per_page, len(response.data["results"]))

    def test_retrieve(self):
        # Pick a random sora
        sora = Sora.objects.order_by("?").first()

        url = reverse("quran:sora-detail", kwargs={"number": sora.number})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(8, len(response.data))

        instance = Sora.objects.get(number=sora.number)
        self.assertEqual(str(instance.id), response.data["id"])
        self.assertEqual(instance.name_en, response.data["name_en"])
        self.assertEqual(instance.name_ar, response.data["name_ar"])
        self.assertEqual(instance.ayas.count(), response.data["ayas_count"])
        self.assertEqual(instance.clean_name_ar, response.data["clean_name_ar"])
        self.assertEqual(instance.number, response.data["number"])

        self.assertEqual(instance.created, parse_datetime(response.data["created"]))
        self.assertEqual(instance.updated, parse_datetime(response.data["updated"]))

    def test_retrieve_sora_ayas(self):
        # Pick a random sora
        sora = Sora.objects.order_by("?").first()

        url = reverse("quran:sora-ayas", kwargs={"number": sora.number})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(sora.ayas.count(), len(response.data))

        aya_response = response.data[randrange(1, sora.ayas.count())]
        self.assertEqual(11, len(aya_response))

        instance = Aya.objects.get(pk=aya_response["id"])

        self.assertEqual(str(instance.id), aya_response["id"])
        self.assertEqual(instance.sora.number, aya_response["sora"])
        self.assertEqual(instance.juz.number, aya_response["juz"])
        self.assertEqual(instance.text, aya_response["text"])
        self.assertEqual(instance.clean_text, aya_response["clean_text"])
        self.assertEqual(instance.number, aya_response["number"])
        self.assertEqual(instance.page, aya_response["page"])
        self.assertEqual(instance.line_start, aya_response["line_start"])
        self.assertEqual(instance.line_end, aya_response["line_end"])

        self.assertEqual(instance.created, parse_datetime(aya_response["created"]))
        self.assertEqual(instance.updated, parse_datetime(aya_response["updated"]))

    def test_retrieve_sora_ayas_detail(self):
        # Pick a random sora
        sora = Sora.objects.order_by("?").first()

        url = reverse(
            "quran:sora-ayas-detail",
            kwargs={
                "number": sora.number,
                "aya_number": randrange(1, sora.ayas.count()),
            },
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(11, len(response.data))

        instance = Aya.objects.get(pk=response.data["id"])

        self.assertEqual(str(instance.id), response.data["id"])
        self.assertEqual(instance.sora.number, response.data["sora"])
        self.assertEqual(instance.juz.number, response.data["juz"])
        self.assertEqual(instance.text, response.data["text"])
        self.assertEqual(instance.clean_text, response.data["clean_text"])
        self.assertEqual(instance.number, response.data["number"])
        self.assertEqual(instance.page, response.data["page"])
        self.assertEqual(instance.line_start, response.data["line_start"])
        self.assertEqual(instance.line_end, response.data["line_end"])

        self.assertEqual(instance.created, parse_datetime(response.data["created"]))
        self.assertEqual(instance.updated, parse_datetime(response.data["updated"]))

    def test_retrieve_sora_ayas_detail_not_found(self):
        # Pick a random sora
        sora = Sora.objects.order_by("?").first()

        url = reverse(
            "quran:sora-ayas-detail",
            kwargs={
                "number": sora.number,
                "aya_number": sora.ayas.count() + 10,
            },
        )
        response = self.client.get(url)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, msg=response.data
        )

    def test_delete(self):
        # Pick a random sora
        sora = Sora.objects.order_by("?").first()
        url = reverse("quran:sora-detail", kwargs={"number": sora.number})
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )

        # Make sure instance still exists
        Sora.objects.get(number=sora.number)

    def test_create(self):
        url = reverse("quran:sora-list")
        new_object_id = uuid4()

        response = self.client.post(
            url,
            data={
                "id": new_object_id,
                "name_en": "name_en",
                "name_ar": "name_ar",
                "clean_name_ar": "clean_name_ar",
                "number": 555,
            },
        )

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )

        # Make sure it wasn't created
        with self.assertRaises(Sora.DoesNotExist):
            Sora.objects.get(pk=new_object_id)

    def test_update(self):
        # Pick a random sora
        sora = Sora.objects.order_by("?").first()
        url = reverse("quran:sora-detail", kwargs={"number": sora.number})

        response = self.client.patch(url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )

        response = self.client.put(url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data
        )


class TestQuranMetadataView(TestCase):
    def test_get(self):
        url = reverse("quran:metadata")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        self.assertEqual(3, len(response.data))
        self.assertEqual(response.data["aya_count"], Aya.objects.count())
        self.assertEqual(response.data["sora_count"], Sora.objects.count())
        self.assertEqual(response.data["juz_count"], Juz.objects.count())
