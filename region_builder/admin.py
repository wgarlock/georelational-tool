from django.contrib import admin

from .models import District, State


class StateAdmin(admin.ModelAdmin):
    pass


class DistrictAdmin(admin.ModelAdmin):
    pass


admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
