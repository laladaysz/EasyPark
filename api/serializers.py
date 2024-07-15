from rest_framework import serializers
from base.models import owner

class PlateSpotSerializer(serializers.Serializer):
    spot_id = serializers.IntegerField()
    plate = serializers.CharField(max_length=7)

class ownerSerializer(serializers.ModelSerializer):
    class Meta:
        model = owner
        fields = ['area', 'number_plate']

class StatusSpotserializer(serializers.Serializer):
    spot_id = serializers.IntegerField()
    status = serializers.CharField()