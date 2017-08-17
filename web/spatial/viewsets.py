from rest_framework import viewsets, filters
from spatial.models import Area, VotingDistrict
from spatial.filters import GeoLocationFilter
from spatial.serializers import *

class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    An area is the smallest supported South Korean administrative unit,
    e.g. 대전광역시, 유성구, 온천2동 (Daejeon Metropolitan City, Yuseong-gu, Oncheon2-dong).
    
    Multiple areas can share the same voting district.

    You can search for an area by name, province, precint, and voting_district's name.

    If you provide lon and lat coordinates as query parameters, you can reverse geocode a location, e.g. ?lat=36.372306&lon=127.365111
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    filter_backends = (filters.SearchFilter, GeoLocationFilter,)
    search_fields = ('name', 'province', 'precinct', 'voting_district__name',)

    def get_serializer_class(self):
        if self.request.GET.get('lat', False) and self.request.GET.get('lon', False):
            return AreaDistanceSerializer
        return AreaSerializer


class VotingDistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """
    South Korean voting districts, based on the election for the 20th National Assembly.

    You can search for a district by name.
    Alternatively, see the [areas](/api/areas) endpoint to find
    a location and its associated voting district.
    """
    queryset = VotingDistrict.objects.all()
    serializer_class = VotingDistrictSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
