from django.urls import include, path
from rest_framework import routers

from search.views import AyaDocumentView

router = routers.DefaultRouter()
router.register(r"aya", AyaDocumentView, basename="aya-search")


urlpatterns = [
    path("", include(router.urls)),
]
