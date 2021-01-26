from django.db.models.signals import post_save
from django.dispatch import receiver

from region_builder.geo_mapper import GeoJSONMapper

from .models import District, State


@receiver(post_save, sender=State)
@receiver(post_save, sender=District)
def post_save_create_geo_collection(sender, instance, created, **kwargs):
    if not instance.geo_collection and instance.geo_json_file and created:
        with instance.geo_json_file.open() as _file:
            mapper = GeoJSONMapper(file=_file, obj=instance)
            geo_collection = mapper.get_geos_geometry()
            instance.geo_collection = geo_collection
            instance.save()
