from django.contrib.gis.db import models


class GenericGeoLocation(models.Model):
    name = models.CharField(max_length=255)
    geo_json_file = models.FileField(blank=True, null=True)
    geo_collection = models.GeometryCollectionField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class State(GenericGeoLocation):
    pass


class District(GenericGeoLocation):
    parent = models.ForeignKey(State, on_delete=models.CASCADE, related_name="districts")
