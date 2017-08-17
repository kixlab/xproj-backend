from rest_framework.filters import BaseFilterBackend
from django.template import loader
from rest_framework.compat import template_render
import coreapi
from spatial.utils import reverse_geocode_closest

class GeoLocationFilter(BaseFilterBackend):
    """Filter that enables reverse geocoding of Areas"""
    template = 'rest_framework/filters/geolocation.html'

    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(name="lon", required=False, location='query',
                schema=coreschema.String(
                    title="Longitude coordinate",
                    description="Provide both coordinates to reverse geocode a location."
                )
            ),
            coreapi.Field(name="lat", required=False, location='query',
                schema=coreschema.String(
                    title="Latitude coordinate",
                    description="Provide both coordinates to reverse geocode a location."
                )
            ),
        ]
        return fields

    def filter_queryset(self, request, queryset, view):
        lat = request.query_params.get('lat', False)
        lon = request.query_params.get('lon', False)
        if lat and lon:
            return reverse_geocode_closest(lat, lon)
        return queryset

    def to_html(self, request, queryset, view):
        context = {
            'lon': request.query_params.get('lon', ''),
            'lat': request.query_params.get('lat', '')
        }
        template = loader.get_template(self.template)
        return template_render(template, context)