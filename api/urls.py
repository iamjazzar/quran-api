from django.urls import include, path

urlpatterns = [
    path("api/quran/", include(("quran.urls", "quran"), namespace="quran")),
    path("api/search/", include(("search.urls", "search"), namespace="search")),
]
