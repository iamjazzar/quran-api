from ddt import data, ddt, unpack
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status


@ddt
class TestViewSetSearchList(TestCase):
    def test_search_no_query(self):
        """
        When no query is supplied, all Ayas in the database are going to be returned
        """
        url = reverse("search:aya-search-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        self.assertEqual(6236, response.data["count"])
        self.assertEqual(100, len(response.data["results"]))
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

    @unpack
    @data(
        {
            "term": "الصيام",
            "expected_count": 2,
            "mentions_expected_order": [
                (2, 183),
                (2, 187),
            ],
        },
        {
            "term": "الضالين",
            "expected_count": 6,
            "mentions_expected_order": [
                (1, 7),
                (2, 198),
                (6, 77),
                (26, 20),
                (26, 86),
                (56, 92),
            ],
        },
    )
    def test_search_with_query(self, term, expected_count, mentions_expected_order):
        """
        Searching for a term, we expect all mentions to be returned in the correct
        order. First by sora and ayas in soras.
        """
        query = {"search": term}
        url = reverse("search:aya-search-list")

        response = self.client.get(f"{url}?{urlencode(query)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        self.assertEqual(expected_count, response.data["count"])
        self.assertEqual(expected_count, len(response.data["results"]))
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

        for result, (sora_number, aya_number) in zip(
            response.data["results"], mentions_expected_order
        ):
            self.assertEqual(sora_number, result["sora"]["number"])
            self.assertEqual(aya_number, result["number"])

    @unpack
    @data(
        {"phrase": "لعنة الله", "expected_count": 6},
        {"phrase": "(لعنة | الله)", "expected_count": 1569},
    )
    def test_phrase_search_with_query(self, phrase, expected_count):
        """
        Searching for a phrase, the default operator between words is "and" as defined
        in the view. Searching with "or" operator should return the results of each
        word combined.
        """
        query = {"search_simple_query_string": phrase}
        url = reverse("search:aya-search-list")

        response = self.client.get(f"{url}?{urlencode(query)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        self.assertEqual(expected_count, response.data["count"])

    def test_suggest_search(self):
        """
        localhost:8000/api/search/aya/suggest/?clean_text__completion=يا
        """
        term = "يا"
        query = {"clean_text__completion": term}
        url = reverse("search:aya-search-suggest")
        expected_count = 5

        response = self.client.get(f"{url}?{urlencode(query)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        options = response.data["clean_text__completion"][0]["options"]
        self.assertEqual(expected_count, len(options))

        for option in options:
            self.assertIn(term, option["text"])
