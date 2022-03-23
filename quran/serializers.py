from rest_framework import serializers

from quran import models


class JuzSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Juz
        fields = ["id", "number", "created", "updated"]


class SoraSerializer(serializers.HyperlinkedModelSerializer):
    ayas_count = serializers.SerializerMethodField()

    def get_ayas_count(self, obj):
        return obj.ayas.count()

    class Meta:
        model = models.Sora
        fields = [
            "id",
            "name_en",
            "name_ar",
            "ayas_count",
            "clean_name_ar",
            "number",
            "created",
            "updated",
        ]


class AyaSerializer(serializers.HyperlinkedModelSerializer):
    sora = serializers.SlugRelatedField(read_only=True, slug_field="number")
    juz = serializers.SlugRelatedField(read_only=True, slug_field="number")

    class Meta:
        model = models.Aya
        fields = [
            "id",
            "sora",
            "juz",
            "text",
            "clean_text",
            "number",
            "page",
            "line_start",
            "line_end",
            "created",
            "updated",
        ]
