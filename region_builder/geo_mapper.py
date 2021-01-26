import inspect
import os
from django.conf import settings
from django.contrib.gis.geos import fromfile


class GeoJSONMapper:
    def __init__(self, file, obj, mappings=dict()):
        self.file = file
        self.is_class = inspect.isclass(obj)
        self.mappings = mappings
        if self.is_class:
            self.obj = obj(**self.mappings)
        else:
            self.obj = obj

    def load_data(self):
        geo_metry_obj = self.get_geos_geometry()
        self.obj.geo_collection = geo_metry_obj
        self.obj.save()

    def get_file_path(self):
        if self.is_class:
            current_dir = os.getcwd()
            return os.path.join(current_dir, settings.GEO_DATA_DIR, self.file)
        else:
            return self.file.path

    def get_geos_geometry(self):
        _file = self.get_file_path()
        return fromfile(open(_file))
