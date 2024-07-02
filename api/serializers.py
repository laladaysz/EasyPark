from rest_framework import serializers
from base.models import owner


# class crop_spacesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = crop_spaces
#         fields = ('id', 'image')


class ownerSerializer(serializers.ModelSerializer):
    class Meta:
        model = owner
        fields = '__all__'

class StatusSpotserializer(serializers.Serializer):
    spot_id = serializers.IntegerField()
    status = serializers.CharField()