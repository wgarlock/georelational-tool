from django.test import TestCase

from region_builder.geo_mapper import GeoJSONMapper
from region_builder.models import State


# Create your tests here.
class ShpFileTest(TestCase):
    def test_GEOJSONMapper(self):
        mappings = dict(
            name="minnesota"
        )
        mapper = GeoJSONMapper(file="minnesota.json", obj=State, mappings=mappings)
        geometry = mapper.get_geos_geometry()
        assert geometry.valid
        mapper.load_data()
        state = State.objects.get(name=mappings["name"])
        assert state.geo_collection.valid
