from django.urls import include, path

urlpatterns = [
    path("api/quran/", include("quran.urls")),
]
