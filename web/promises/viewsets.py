from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from promises.serializers import *
from promises.models import Person, Promise
from django.db.models import Q

class PromiseViewSet(viewsets.ReadOnlyModelViewSet):
    """This endpoint provides promises made by people.
    You can also access them by going through the people resource."""
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    People are members of the public holding some function, like politicians.
    You can search for them by name and access details in sub resources."""
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @list_route()
    def mayors(self, request):
        qs = Person.objects.filter(Q(mayor_for_province__isnull=False) | Q(mayor_for_district__isnull=False))
        context = {
            'request': request
        }
        serializer = PersonSerializer(qs, many=True, context=context)
        return Response(serializer.data)

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