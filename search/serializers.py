from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from quran.documents import AyaDocument


class ArticleDocumentSerializer(DocumentSerializer):
    class Meta:
        document = AyaDocument

        fields = (
            "id",
            "text",
            "clean_text",
            "sora",
            "juz",
            "number",
        )
