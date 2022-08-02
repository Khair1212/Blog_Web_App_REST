import requests
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from urlShortner.models import UrlShortner


class ShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlShortner
        fields = ['long_url', 'time_date_created']

    def validate(self, attrs):
        longurl = attrs.get('long_url')
        try:
            # Get Url
            get = requests.get(longurl)
            # if the request succeeds
            if get.status_code == 200:
                return attrs
            else:
                raise ValidationError("The URL is not Valid!")
            # Exception
        except requests.exceptions.RequestException as e:
            # print URL with Errs
            raise SystemExit(f"{longurl}: is Not reachable \nErr: {e}")

    def create(self, validate_data):
        return UrlShortner.objects.create(**validate_data)


class LongURLRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlShortner
        fields = ['short_url', 'time_date_created']
