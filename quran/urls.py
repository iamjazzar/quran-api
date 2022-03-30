from django.urls import include, path
from rest_framework import routers

from quran.views import AyaViewSet, JuzViewSet, QuranMetadataView, SoraViewSet

router = routers.DefaultRouter()
router.register(r"aya", AyaViewSet)
router.register(r"juz", JuzViewSet)
router.register(r"sora", SoraViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("metadata/", QuranMetadataView.as_view(), name="metadata"),
]
