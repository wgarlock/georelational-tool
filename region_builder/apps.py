from django.apps import AppConfig


class RegionBuilderConfig(AppConfig):
    name = 'region_builder'

    def ready(self):
        import region_builder.signal_handlers  # noqa
