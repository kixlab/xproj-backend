from django.contrib.gis import admin
from django.urls import reverse
from .models import Area, VotingDistrict

admin.site.register(Area, admin.OSMGeoAdmin)

class AreaInline(admin.TabularInline):
    model = Area
    fields = ('name',)
    readonly_fields = ('name',)
    can_delete = False
    show_change_link = True

class VotingDistrictAdmin(admin.OSMGeoAdmin):
    inlines = (AreaInline,)

admin.site.register(VotingDistrict, VotingDistrictAdmin)
