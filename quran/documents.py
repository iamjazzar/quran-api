from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from quran.models import Aya


@registry.register_document
class AyaDocument(Document):
    sora = fields.ObjectField(
        properties={
            "id": fields.TextField(),
            "name_en": fields.TextField(),
            "name_ar": fields.TextField(),
            "clean_name_ar": fields.TextField(
                fields={
                    "raw": fields.TextField(),
                    "suggest": fields.CompletionField(),
                },
            ),
            "number": fields.ShortField(),
        }
    )
    juz = fields.ObjectField(
        properties={
            "id": fields.TextField(),
            "number_worded_ar": fields.TextField(),
            "number_worded_en": fields.TextField(),
            "number": fields.ShortField(),
        }
    )

    number = fields.TextField(
        fields={
            "raw": fields.ShortField(),
        },
    )

    clean_text = fields.TextField(
        fields={
            "raw": fields.TextField(),
            "suggest": fields.CompletionField(),
        },
    )

    class Index:
        name = "quran-aya"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Aya
        fields = [
            "id",
            "text",
        ]
