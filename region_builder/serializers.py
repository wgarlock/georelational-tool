from rest_framework import serializers

from region_builder.models import District, State


class MapboxField(serializers.JSONField):
    def to_representation(self, value):
        return {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': value.coords[0]
                }
            }
        }


class DistrictSerializer(serializers.ModelSerializer):
    geo_collection = MapboxField()

    class Meta:
        model = District
        fields = ["name", "geo_collection"]


class StateSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True)
    geo_collection = MapboxField()

    class Meta:
        model = State
        fields = ["name", "geo_collection", "districts"]
