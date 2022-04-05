from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    DefaultOrderingFilterBackend,
    OrderingFilterBackend,
    SimpleQueryStringSearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from quran.documents import AyaDocument
from search.serializers import ArticleDocumentSerializer


class AyaDocumentView(DocumentViewSet):
    document = AyaDocument
    serializer_class = ArticleDocumentSerializer

    filter_backends = [
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SuggesterFilterBackend,
        SimpleQueryStringSearchFilterBackend,
    ]

    search_fields = {
        "text": {"boost": 4},
        "clean_text": {"boost": 2},
        "id": None,
        "number": None,
    }

    simple_query_string_search_fields = {
        "text": {"boost": 4},
        "clean_text": {"boost": 2},
    }

    simple_query_string_options = {
        "default_operator": "and",
    }

    multi_match_options = {"type": "phrase"}

    ordering_fields = {
        "sora": "sora.number",
        "number": "number.raw",
    }

    ordering = (
        "sora",
        "number",
    )

    suggester_fields = {
        "sora": {
            "field": "sora.clean_name_ar.suggest",
            "suggesters": [
                SUGGESTER_COMPLETION,
            ],
        },
        "clean_text": {
            "field": "clean_text.suggest",
            "suggesters": [
                SUGGESTER_COMPLETION,
            ],
        },
    }
