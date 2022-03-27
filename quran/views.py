from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from quran import pagination, serializers
from quran.models import Aya, Juz, Sora


class JuzViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Juz.objects.all()
    serializer_class = serializers.JuzSerializer
    lookup_field = "number"
    pagination_class = pagination.NumberCursorPagination


class SoraViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Sora.objects.all()
    serializer_class = serializers.SoraSerializer
    lookup_field = "number"
    pagination_class = pagination.NumberCursorPagination

    @action(methods=["GET"], detail=True)
    def ayas(self, *args, **kwargs):
        sora = self.get_object()
        ayas = sora.ayas.all().order_by("number")

        serializer = serializers.AyaSerializer(ayas, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=True, url_path=r"ayas/(?P<aya_number>\d+)")
    def ayas_detail(self, *args, **kwargs):
        sora = self.get_object()
        aya_number = kwargs.get("aya_number")

        aya = get_object_or_404(Aya.objects.all(), sora=sora, number=aya_number)
        serializer = serializers.AyaSerializer(aya, many=False)

        return Response(serializer.data)


class AyaViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Aya.objects.all()
    serializer_class = serializers.AyaSerializer
    pagination_class = pagination.NumberCursorPagination
