from django.urls import include, path
from rest_framework import routers

from quran.views import AyaViewSet, JuzViewSet, SoraViewSet

router = routers.DefaultRouter()
router.register(r"aya", AyaViewSet)
router.register(r"juz", JuzViewSet)
router.register(r"sora", SoraViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
