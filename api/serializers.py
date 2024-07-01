from rest_framework import serializers
from base.models import crop_spaces


class crop_spacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = crop_spaces
        fields = ('id', 'image')