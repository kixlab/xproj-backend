from django.contrib.gis import admin
from django.urls import reverse
from .models import Area, VotingDistrict
from promises.admin import PersonInline

admin.site.register(Area, admin.OSMGeoAdmin)

class AreaInline(admin.TabularInline):
    model = Area
    fields = ('name',)
    readonly_fields = ('name',)
    can_delete = False
    show_change_link = True

class VotingDistrictAdmin(admin.OSMGeoAdmin):
    inlines = (PersonInline, AreaInline, )

admin.site.register(VotingDistrict, VotingDistrictAdmin)
