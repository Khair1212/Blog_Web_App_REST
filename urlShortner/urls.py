from django.urls import path

from urlShortner.views import RetrieveLongURL, CreateShortURL

urlpatterns = [
    path('create_short_url/', CreateShortURL.as_view(), name='create_short_url'),
    path('retrieve_long_url/', RetrieveLongURL.as_view(), name='retrieve_long_url'),
]