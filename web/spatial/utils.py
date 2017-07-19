from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from .models import Area

def reverse_geocode(lat, lon):
    pnt = GEOSGeometry('POINT({0} {1})'.format(lon, lat), srid=4326)
    return Area.objects.get(mpoly__contains=pnt)

def reverse_geocode_closest(lat, lon, max_distance=2500):
    pnt = GEOSGeometry('POINT({0} {1})'.format(lon, lat), srid=4326)
    qs = Area.objects.annotate(distance=Distance('mpoly', pnt))
    return qs.filter(mpoly__distance_lte=(pnt, D(m=max_distance))).order_by('distance')

