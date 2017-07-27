from django import forms
from django.views.generic.edit import FormView
from spatial.utils import reverse_geocode, reverse_geocode_closest
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, mixins, generics, filters
from rest_framework.views import APIView
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils.datastructures import MultiValueDictKeyError
from .models import Area, VotingDistrict
from promises.models import Person, Promise

class LatLonForm(forms.Form):
    lat = forms.CharField(label="Latitude", initial='36.372306')
    lon = forms.CharField(label="Longitude", initial='127.365111')

class ReverseGeocodeView(FormView):
    template_name = 'form.html'
    form_class = LatLonForm

    def form_valid(self, form, **kwargs):
        result = reverse_geocode(form.cleaned_data['lat'], form.cleaned_data['lon'])
        context = self.get_context_data(**kwargs)
        context['result'] = result
        context['form'] = form
        return self.render_to_response(context)

"""
API views
"""
class PersonSerializer(serializers.HyperlinkedModelSerializer):
    promises_url = serializers.HyperlinkedIdentityField(view_name='person-promises')

    class Meta:
        model = Person
        fields = ('url', 'name', 'mop_for_district', 'promises_url')

class PromiseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promise
        fields = ('url', 'title', 'categories', 'target_groups',)

class VotingDistrictSerializer(serializers.HyperlinkedModelSerializer):
    #current_mop = serializers.HyperlinkedRelatedField(many=False, view_name='person-detail', read_only=True)
    current_mop = PersonSerializer()

    class Meta:
        model = VotingDistrict
        fields = ('url', 'name', 'current_mop')

class AreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Area
        fields = ('url', 'name', 'precinct', 'province', 'voting_district_name', 'voting_district', )

class AreaDistanceSerializer(serializers.HyperlinkedModelSerializer):
    distance = serializers.CharField()

    class Meta:
        model = Area
        fields = ('name', 'precinct', 'province', 'voting_district_name', 'voting_district', 'distance', )

class ReverseGeocodeAPIView(viewsets.ReadOnlyModelViewSet):
    """
    Returns the areas within a 2.5km radius of the requested location.
    For example, ?lat=36.372306&lon=127.365111
    """
    serializer_class = AreaDistanceSerializer
    # permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        errors = {}
        for field in ('lat', 'lon', ):
            if not self.request.GET.get(field, False):
                errors[field] = ["Required parameter"]
        if errors:
            raise serializers.ValidationError(errors)
        
        results = reverse_geocode_closest(self.request.GET['lat'], self.request.GET['lon'])            
        return results

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'province', 'precinct', 'voting_district_name',)

class VotingDistrictViewSet(viewsets.ModelViewSet):
    queryset = VotingDistrict.objects.all()
    serializer_class = VotingDistrictSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

class PromiseViewSet(viewsets.ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @detail_route()
    def promises(self, request, pk=None):
        """
        Returns a list of all the person's promises
        """
        person = self.get_object()
        promises = person.promises.all()
        context = {
            'request': request
        }
        promise_serializer = PromiseSerializer(promises, many=True, context=context)
        return Response(promise_serializer.data)
