from rest_framework import serializers

from checker.models import Url


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ('pk', 'url', 'status', 'is_paused')
        read_only_fields = ('pk', 'url', 'status')
